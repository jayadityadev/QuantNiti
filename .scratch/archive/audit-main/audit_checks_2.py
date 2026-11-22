"""Adversarial audit checks #2: traversal depth, SSE, idempotency, SQLite locking."""
import json, sys, threading, time, tempfile
sys.path.insert(0, "src")

from fastapi.testclient import TestClient
from app.api.app import create_app
from app.data.service import MarketDataService
from app.data.provider import MockDataProvider
from app.data.cache import ParquetMarketCache
from app.data.storage import PortfolioRepository

tmp = tempfile.mkdtemp()
svc = MarketDataService(provider=MockDataProvider(), cache=ParquetMarketCache(cache_dir=tmp, default_ttl_seconds=999999))
app = create_app(service=svc)
client = TestClient(app, raise_server_exceptions=False)

print("=== 1. SPA traversal: hit real file 4 levels up ===")
for p in ["/..%2F..%2F..%2F..%2Fpyproject.toml",
          "/%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fpyproject.toml",
          "/....//....//....//pyproject.toml",
          "/..;/..;/pyproject.toml"]:
    r = client.get(p)
    print(f"GET {p} -> {r.status_code} len={len(r.content)} first80={r.text[:80]!r}")

print("\n=== 2. caching bug: valid cache masks requested date range ===")
r = client.get("/api/v1/market/history", params={"symbol": "TCS", "start_date": "2015-01-01", "end_date": "2015-12-31"})
print("TCS 2015 (fresh symbol):", r.status_code, "count:", (r.json() or {}).get("count"))
# second call: now cached with 2015-only range; request older range -> silent empty
r = client.get("/api/v1/market/history", params={"symbol": "TCS", "start_date": "2010-01-01", "end_date": "2010-12-31"})
print("TCS 2010 (after cache exists):", r.status_code, (r.json() or {}).get("detail"))

print("\n=== 3. GET /portfolios/{id} mutates DB on every call ===")
r = client.post("/api/v1/portfolio/create", json={"name": "idem-test", "capital": 50000})
pid = r.json()["portfolio_id"]
import sqlite3
db = sqlite3.connect(str(tmp and "data/quantniti.db"))
before = db.execute("SELECT updated_at, current_value FROM portfolios WHERE id=?", (pid,)).fetchone()
r1 = client.get(f"/api/v1/portfolios/{pid}")
after = db.execute("SELECT updated_at, current_value FROM portfolios WHERE id=?", (pid,)).fetchone()
print("before:", before)
print("after GET:", after)
print("row mutated by GET:", before != after)

print("\n=== 4. SQLite concurrency: parallel GETs -> 'database is locked'? ===")
errors = []
def hit():
    for _ in range(5):
        rr = client.get(f"/api/v1/portfolios/{pid}")
        if rr.status_code >= 500:
            errors.append((rr.status_code, rr.text[:200]))
threads = [threading.Thread(target=hit) for _ in range(6)]
for t in threads: t.start()
for t in threads: t.join()
print("errors:", errors if errors else "none in 30 parallel calls")

print("\n=== 5. parallel save_portfolio raw repository ===")
from app.core.models import PortfolioState, MarketRegimeType, RiskPersona
repo = PortfolioRepository(database_url=f"sqlite:///{tmp}/lock_test.db")
def save_many(i):
    try:
        st = PortfolioState(
            portfolio_id=f"p{i}", name="x", initial_capital=1, cash=0, invested_capital=1,
            current_value=1, total_pnl=0, total_pnl_pct=0,
            holdings=[], initial_regime=MarketRegimeType.LOW_VOLATILITY_BULL,
            current_regime=MarketRegimeType.LOW_VOLATILITY_BULL,
            risk_persona=RiskPersona.BALANCED, horizon="6M", created_at="now", as_of_date="today")
        for _ in range(10):
            repo.save_portfolio(st)
    except Exception as e:
        errors.append(f"thread{i}: {type(e).__name__}: {e}")
errs2 = []
errors, errs2 = errs2, []
threads = [threading.Thread(target=save_many, args=(i,)) for i in range(8)]
for t in threads: t.start()
for t in threads: t.join()
print("raw repo concurrent errors:", errors if errors else "none (80 writes, 8 threads)")

print("\n=== 6. SSE stream ===")
with client.stream("GET", "/api/v1/stream/ticks", params={"interval": 0.01, "max_ticks": 2}) as resp:
    print("status:", resp.status_code, "content-type:", resp.headers.get("content-type"))
    chunks = []
    for line in resp.iter_lines():
        chunks.append(line)
        if len(chunks) > 12: break
print("first lines:", chunks[:8])

print("\n=== 7. XSS payload round-trip on reviews read ===")
r = client.get("/api/v1/reviews/basket/x")
names = [rev["user_name"] for rev in r.json()["reviews"]]
print("stored+returned usernames:", names[:3])

print("\n=== 8. /docs exposed + OpenAPI in production build ===")
r = client.get("/docs"); print("docs:", r.status_code)
r = client.get("/openapi.json"); print("openapi:", r.status_code, "paths:", len((r.json() or {}).get("paths", {})))

client.delete(f"/api/v1/portfolios/{pid}")

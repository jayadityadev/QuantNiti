"""Adversarial audit execution checks #1: traversal, auth, CORS, contracts."""
import json, os, sys
sys.path.insert(0, "src")

from fastapi.testclient import TestClient
from app.api.app import create_app
from app.data.service import MarketDataService
from app.data.provider import MockDataProvider

svc = MarketDataService(provider=MockDataProvider(), cache=None.__class__ and None or None)
from app.data.cache import ParquetMarketCache
import tempfile
tmp = tempfile.mkdtemp()
svc.cache = ParquetMarketCache(cache_dir=tmp, default_ttl_seconds=999999)
app = create_app(service=svc)
client = TestClient(app, raise_server_exceptions=False)

print("=== 1. SPA fallback path traversal ===")
for p in ["/..%2F..%2Fpyproject.toml", "/%2e%2e/pyproject.toml",
          "/static/%2e%2e/%2e%2e/%2e%2e/pyproject.toml",
          "/..%5C..%5Cpyproject.toml",
          "/../../pyproject.toml"]:
    r = client.get(p)
    body = r.text[:120].replace("\n", " ")
    print(f"GET {p} -> {r.status_code} len={len(r.content)} body={body!r}")

print("\n=== 2. CORS allow-credentials wildcard ===")
r = client.options("/", headers={
    "Origin": "https://evil.example.com",
    "Access-Control-Request-Method": "DELETE",
})
print("preflight:", r.status_code, dict(r.headers))
r2 = client.get("/api/health", headers={"Origin": "https://evil.example.com"})
print("GET ACAO:", r2.headers.get("access-control-allow-origin"), "ACAC:", r2.headers.get("access-control-allow-credentials"))

print("\n=== 3. Unauthenticated mutating endpoints ===")
r = client.delete("/api/v1/portfolios/nonexistent-id")
print("DELETE portfolio:", r.status_code, r.json())

r = client.patch("/api/v1/alerts/whatever/read")
print("PATCH alert:", r.status_code, r.json())

r = client.post("/api/v1/alerts/mark-all-read")
print("POST mark-all-read:", r.status_code, r.json())

r = client.post("/api/v1/reviews/submit", json={
    "target_id": "x", "user_name": "attacker<script>alert(1)</script>",
    "rating": 3, "review_text": "x" * 2000})
print("POST review (2000-char text, XSS username):", r.status_code, json.dumps(r.json())[:200])

print("\n=== 4. Chat status leaks model/env info ===")
r = client.get("/api/v1/chat/status")
print("chat/status:", r.status_code, r.json())

print("\n=== 5. Validation gaps ===")
r = client.post("/api/v1/chat", json={"message": "x" * 500000})
print("chat 500KB message:", r.status_code, str(r.json())[:120])

r = client.post("/api/v1/portfolio/create", json={"name": "", "capital": 1000})
print("create portfolio bad:", r.status_code, str(r.json())[:150])

print("\n=== 6. /market/history date slicing contract ===")
r = client.get("/api/v1/market/history", params={"symbol": "RELIANCE", "start_date": "2018-01-01", "end_date": "2018-12-31"})
d = r.json()
print("history 2018:", r.status_code, "count:", d.get("count"), "start:", d.get("start_date"), "end:", d.get("end_date"))

print("\n=== 7. reviews fallback leaks other targets ===")
r = client.get("/api/v1/reviews/basket/UNKNOWN_BASKET_ID_123")
print("reviews unknown basket:", r.status_code, "reviews:", len(r.json().get("reviews", [])), "target_id:", r.json().get("target_id"))

print("\n=== 8. compounding arbitrary lump sum ===")
r = client.post("/api/v1/portfolio/compounding", json={"initial_lump_sum": 1e308, "monthly_sip": 1e30, "tenure_years": 10, "expected_return_pct": 100.0})
print("compounding huge:", r.status_code, str(r.json())[:150])

print("\n=== 9. portfolio full lifecycle (unauth) ===")
r = client.post("/api/v1/portfolio/create", json={"name": "auditor", "capital": 100000, "horizon": "6M"})
print("create:", r.status_code, (r.json() or {}).get("portfolio_id"))
pid = r.json().get("portfolio_id")
r2 = client.get(f"/api/v1/portfolios/{pid}")
print("get:", r2.status_code, r2.json().get("current_value"))
r3 = client.get("/api/v1/portfolios")
print("list count (cross-user exposure):", len(r3.json()))
r4 = client.delete(f"/api/v1/portfolios/{pid}")
print("delete:", r4.status_code, r4.json())

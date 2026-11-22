"""Final checks: .env traversal, runtime/realtime modules, dockerignore."""
import sys
sys.path.insert(0, "src")
from fastapi.testclient import TestClient
from app.api.app import create_app
from app.data.service import MarketDataService
from app.data.provider import MockDataProvider
from app.data.cache import ParquetMarketCache
import tempfile, os

tmp = tempfile.mkdtemp()
svc = MarketDataService(provider=MockDataProvider(), cache=ParquetMarketCache(cache_dir=tmp, default_ttl_seconds=60))
app = create_app(service=svc)
client = TestClient(app, raise_server_exceptions=False)

print("=== CRITICAL: arbitrary file read reaching repo root .env ===")
r = client.get("/..%2F..%2F..%2F..%2F.env")
print("GET /..%2F..%2F..%2F..%2F.env ->", r.status_code, "len:", len(r.content))
print("first 200 chars:", r.text[:200])

print("\n=== secrets via absolute-ish path? (uvicorn rejects empty segments; try .git config) ===")
r = client.get("/..%2F..%2F..%2F..%2F.git%2Fconfig")
print("git config ->", r.status_code, "len:", len(r.content))

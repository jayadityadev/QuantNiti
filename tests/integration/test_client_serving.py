"""Integration tests for Client Serving endpoints and static assets."""

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.app import create_app
from app.data.cache import ParquetMarketCache
from app.data.provider import MockDataProvider
from app.data.service import MarketDataService


@pytest.fixture
def test_app(tmp_path):
    cache = ParquetMarketCache(cache_dir=tmp_path / "cache")
    provider = MockDataProvider()
    service = MarketDataService(provider=provider, cache=cache)
    return create_app(service=service)


@pytest.mark.asyncio
async def test_root_serves_html(test_app):
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
        content = response.text
        assert "QuantNiti" in content
        assert 'id="root"' in content


@pytest.mark.asyncio
async def test_app_route_serves_html(test_app):
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/app")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
        assert "QuantNiti" in response.text
        assert 'id="root"' in response.text


@pytest.mark.asyncio
async def test_static_assets_served(test_app):
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Check manifest endpoint
        manifest_resp = await client.get("/manifest.json")
        assert manifest_resp.status_code == 200
        assert "application/manifest+json" in manifest_resp.headers.get("content-type", "")

        # Check static icon
        icon_resp = await client.get("/static/icons/icon-192.png")
        assert icon_resp.status_code == 200
        assert len(icon_resp.content) > 0


@pytest.mark.asyncio
async def test_vite_build_assets_served(test_app):
    """Verify that Vite build artifacts in /static/dist and /vite endpoint are served."""
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        vite_resp = await client.get("/vite")
        assert vite_resp.status_code == 200
        assert "text/html" in vite_resp.headers.get("content-type", "")
        assert "QuantNiti" in vite_resp.text
        assert 'id="root"' in vite_resp.text
        assert "/static/dist/assets/" in vite_resp.text

        dist_html_resp = await client.get("/static/dist/index.html")
        assert dist_html_resp.status_code == 200
        assert 'id="root"' in dist_html_resp.text


@pytest.mark.asyncio
async def test_competitor_benchmark_assets_served(test_app):
    """Verify that the SPA bundle serves root shell with linked Vite assets."""
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert 'id="root"' in response.text
        assert "/static/dist/assets/index-" in response.text

"""Comprehensive async unit and integration tests for Database, Authentication, and Workspace routes."""

import os
from typing import AsyncGenerator
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.api.app import app
from app.auth.dependencies import get_current_user, get_optional_user
from app.auth.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.db.base import Base
from app.db.models import (
    BasketHolding,
    PaperTradeOrder,
    PortfolioBasket,
    RiskCalibration,
    User,
    Workspace,
)
from app.db.session import (
    get_db,
    init_db,
    normalize_database_url,
)


# ============================================================================
# Fixtures: In-Memory Async DB & Test Client
# ============================================================================

@pytest_asyncio.fixture
async def test_session_factory():
    """Create an isolated in-memory SQLite database and session factory."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_maker = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    yield session_maker
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_session_factory) -> AsyncGenerator[AsyncSession, None]:
    """Yield an isolated test DB session with automatic rollback/close."""
    async with test_session_factory() as session:
        yield session


@pytest_asyncio.fixture
async def client(test_session_factory) -> AsyncGenerator[AsyncClient, None]:
    """Provide AsyncClient with get_db dependency overridden to the test DB."""
    async def override_get_db():
        async with test_session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


# ============================================================================
# 1. Database URL Normalization & Engine Fallback Tests
# ============================================================================

class TestDatabaseUrlHandling:
    def test_empty_or_none_falls_back_to_sqlite(self):
        assert "sqlite+aiosqlite" in normalize_database_url(None)
        assert "sqlite+aiosqlite" in normalize_database_url("")
        assert "sqlite+aiosqlite" in normalize_database_url("   ")

    def test_postgres_protocol_converted_to_asyncpg(self):
        url = "postgres://user:pass@ep-cool-fog.neon.tech/neondb"
        normalized = normalize_database_url(url)
        assert normalized.startswith("postgresql+asyncpg://")

        url_pg = "postgresql://user:pass@ep-cool-fog.neon.tech/neondb"
        normalized_pg = normalize_database_url(url_pg)
        assert normalized_pg.startswith("postgresql+asyncpg://")

    def test_neon_sslmode_require_converted_to_ssl_require(self):
        url = "postgresql://user:pass@ep-cool-fog.neon.tech/neondb?sslmode=require"
        normalized = normalize_database_url(url)
        assert "ssl=require" in normalized
        assert "sslmode" not in normalized


# ============================================================================
# 2. Database Models & Schema Tests
# ============================================================================

@pytest.mark.asyncio
class TestDomainModels:
    async def test_user_and_workspace_lifecycle(self, db_session: AsyncSession):
        user = User(
            email="investor@example.com",
            hashed_password=hash_password("SuperSecret123!"),
            full_name="Alpha Investor",
        )
        db_session.add(user)
        await db_session.flush()

        assert user.id is not None
        assert user.is_active is True

        ws = Workspace(
            user_id=user.id,
            name="Alpha Workspace",
            is_default=True,
        )
        db_session.add(ws)
        await db_session.flush()

        basket = PortfolioBasket(
            workspace_id=ws.id,
            name="Tech Growth",
            capital=150000.0,
            risk_persona="Aggressive Growth",
        )
        db_session.add(basket)
        await db_session.flush()

        holding = BasketHolding(
            basket_id=basket.id,
            symbol="NVDA",
            target_weight=0.50,
            actual_shares=20.0,
            avg_price=120.0,
        )
        db_session.add(holding)

        risk_cal = RiskCalibration(
            workspace_id=ws.id,
            persona="Aggressive Growth",
            max_volatility=0.25,
            max_drawdown_limit=0.20,
            esg_preference=True,
        )
        db_session.add(risk_cal)

        order = PaperTradeOrder(
            workspace_id=ws.id,
            symbol="NVDA",
            order_type="MARKET",
            side="BUY",
            shares=10.0,
            executed_price=122.50,
            status="EXECUTED",
        )
        db_session.add(order)
        await db_session.commit()

        # Verify query and serialization
        stmt = select(User).where(User.id == user.id)
        res = await db_session.execute(stmt)
        queried_user = res.scalar_one()

        assert queried_user.email == "investor@example.com"
        assert len(queried_user.workspaces) == 1
        ws_dict = queried_user.workspaces[0].to_dict(include_children=True)
        assert ws_dict["name"] == "Alpha Workspace"
        assert len(ws_dict["baskets"]) == 1
        assert ws_dict["baskets"][0]["holdings"][0]["symbol"] == "NVDA"
        assert len(ws_dict["risk_calibrations"]) == 1
        assert ws_dict["risk_calibrations"][0]["persona"] == "Aggressive Growth"
        assert len(ws_dict["paper_trades"]) == 1
        assert ws_dict["paper_trades"][0]["status"] == "EXECUTED"

    async def test_cascade_delete_user_cleans_workspace_and_children(self, db_session: AsyncSession):
        user = User(
            email="delete_me@example.com",
            hashed_password=hash_password("Pass12345"),
            full_name="Ephemeral User",
        )
        db_session.add(user)
        await db_session.flush()

        ws = Workspace(user_id=user.id, name="Ephemeral Workspace", is_default=True)
        db_session.add(ws)
        await db_session.flush()

        basket = PortfolioBasket(workspace_id=ws.id, name="Temp Basket")
        db_session.add(basket)
        await db_session.commit()

        # Delete user
        await db_session.delete(user)
        await db_session.commit()

        # Verify workspace and basket are also gone
        ws_res = await db_session.execute(select(Workspace).where(Workspace.id == ws.id))
        assert ws_res.scalar_one_or_none() is None

        basket_res = await db_session.execute(select(PortfolioBasket).where(PortfolioBasket.id == basket.id))
        assert basket_res.scalar_one_or_none() is None


# ============================================================================
# 3. Security, Hashing & JWT Tests
# ============================================================================

class TestSecurityAndTokens:
    def test_bcrypt_hashing_and_verification(self):
        password = "SecurePassword@2026"
        hashed = hash_password(password)

        assert hashed != password
        assert hashed.startswith("$2b$")
        assert verify_password(password, hashed) is True
        assert verify_password("WrongPassword!", hashed) is False
        assert verify_password("", hashed) is False

    def test_access_and_refresh_token_lifecycle(self):
        user_id = "test-user-id-42"
        access_tok = create_access_token(user_id, extra_claims={"role": "quant"})
        refresh_tok = create_refresh_token(user_id)

        # Decode access token
        access_payload = decode_token(access_tok)
        assert access_payload["sub"] == user_id
        assert access_payload["token_type"] == "access"
        assert access_payload["role"] == "quant"

        # Decode refresh token
        refresh_payload = decode_token(refresh_tok)
        assert refresh_payload["sub"] == user_id
        assert refresh_payload["token_type"] == "refresh"


# ============================================================================
# 4. Auth Dependencies Tests
# ============================================================================

@pytest.mark.asyncio
class TestAuthDependencies:
    async def test_get_current_user_valid(self, db_session: AsyncSession):
        user = User(
            email="auth_dep@example.com",
            hashed_password=hash_password("Password999"),
            is_active=True,
        )
        db_session.add(user)
        await db_session.commit()

        token = create_access_token(user.id)
        current = await get_current_user(token=token, db=db_session)
        assert current.id == user.id
        assert current.email == "auth_dep@example.com"

    async def test_get_current_user_invalid_or_missing_raises_401(self, db_session: AsyncSession):
        with pytest.raises(Exception) as exc:
            await get_current_user(token=None, db=db_session)
        assert "401" in str(exc.value)

        with pytest.raises(Exception) as exc2:
            await get_current_user(token="malformed.jwt.token", db=db_session)
        assert "401" in str(exc2.value)

    async def test_get_optional_user_frictionless_guest(self, db_session: AsyncSession):
        # Missing token returns None smoothly
        guest_res = await get_optional_user(token=None, db=db_session)
        assert guest_res is None

        # Invalid token returns None smoothly without raising
        invalid_res = await get_optional_user(token="bad-token", db=db_session)
        assert invalid_res is None


# ============================================================================
# 5. REST API Route Integration Tests (auth.py & workspace.py)
# ============================================================================

@pytest.mark.asyncio
class TestAuthAndWorkspaceEndpoints:
    async def test_register_creates_user_and_auto_provisions_workspace(self, client: AsyncClient):
        payload = {
            "email": "fresh_trader@example.com",
            "password": "Password123!",
            "full_name": "Fresh Trader",
        }
        res = await client.post("/api/v1/auth/register", json=payload)
        assert res.status_code == 201

        data = res.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == "fresh_trader@example.com"
        assert data["workspace"]["name"] == "Fresh Trader's Workspace"
        assert data["workspace"]["is_default"] is True

    async def test_register_duplicate_email_fails(self, client: AsyncClient):
        payload = {
            "email": "duplicate@example.com",
            "password": "Password123!",
            "full_name": "Trader One",
        }
        res1 = await client.post("/api/v1/auth/register", json=payload)
        assert res1.status_code == 201

        res2 = await client.post("/api/v1/auth/register", json=payload)
        assert res2.status_code == 400
        assert "already exists" in res2.json()["detail"]

    async def test_login_success_and_failure(self, client: AsyncClient):
        # Register user first
        await client.post(
            "/api/v1/auth/register",
            json={"email": "login_test@example.com", "password": "CorrectPassword1"},
        )

        # Login with correct password
        login_res = await client.post(
            "/api/v1/auth/login",
            json={"email": "login_test@example.com", "password": "CorrectPassword1"},
        )
        assert login_res.status_code == 200
        token_data = login_res.json()
        assert "access_token" in token_data

        # Login with wrong password
        bad_pw_res = await client.post(
            "/api/v1/auth/login",
            json={"email": "login_test@example.com", "password": "WrongPassword!"},
        )
        assert bad_pw_res.status_code == 401

        # Login with non-existent email
        not_found_res = await client.post(
            "/api/v1/auth/login",
            json={"email": "ghost@example.com", "password": "SomePassword"},
        )
        assert not_found_res.status_code == 401

    async def test_token_refresh(self, client: AsyncClient):
        reg_res = await client.post(
            "/api/v1/auth/register",
            json={"email": "refresher@example.com", "password": "ValidPassword99"},
        )
        tokens = reg_res.json()
        refresh_tok = tokens["refresh_token"]

        # Exchange refresh token
        exchange_res = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_tok},
        )
        assert exchange_res.status_code == 200
        new_tokens = exchange_res.json()
        assert "access_token" in new_tokens
        assert "refresh_token" in new_tokens

        # Attempt exchange with invalid token
        bad_refresh_res = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "garbage-token"},
        )
        assert bad_refresh_res.status_code == 401

    async def test_get_me_authenticated_and_guest(self, client: AsyncClient):
        # 1. Guest fallback
        guest_res = await client.get("/api/v1/auth/me")
        assert guest_res.status_code == 200
        guest_data = guest_res.json()
        assert guest_data["is_guest"] is True
        assert guest_data["email"] == "guest@quantniti.local"
        assert len(guest_data["workspaces"]) == 1

        # 2. Authenticated user
        reg_res = await client.post(
            "/api/v1/auth/register",
            json={"email": "me_user@example.com", "password": "PassMe1234", "full_name": "Me User"},
        )
        access_tok = reg_res.json()["access_token"]

        auth_res = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {access_tok}"},
        )
        assert auth_res.status_code == 200
        auth_data = auth_res.json()
        assert auth_data["is_guest"] is False
        assert auth_data["email"] == "me_user@example.com"
        assert auth_data["full_name"] == "Me User"
        assert len(auth_data["workspaces"]) == 1

    async def test_workspace_active_guest_fallback(self, client: AsyncClient):
        # Without auth header -> returns demo multi-asset workspace
        res = await client.get("/api/v1/workspace/active")
        assert res.status_code == 200
        data = res.json()
        assert data["is_guest"] is True
        assert data["id"] == "demo-workspace"
        assert len(data["baskets"]) >= 1
        assert len(data["baskets"][0]["holdings"]) >= 3
        assert len(data["risk_calibrations"]) >= 1
        assert len(data["paper_trades"]) >= 1

    async def test_workspace_active_authenticated(self, client: AsyncClient):
        reg_res = await client.post(
            "/api/v1/auth/register",
            json={"email": "ws_user@example.com", "password": "SecurePassword9!"},
        )
        access_tok = reg_res.json()["access_token"]

        res = await client.get(
            "/api/v1/workspace/active",
            headers={"Authorization": f"Bearer {access_tok}"},
        )
        assert res.status_code == 200
        data = res.json()
        assert data["is_guest"] is False
        assert "Workspace" in data["name"]
        assert len(data["baskets"]) == 1
        assert data["baskets"][0]["name"] == "Core Alpha Growth Basket"
        assert len(data["baskets"][0]["holdings"]) == 3
        assert len(data["risk_calibrations"]) == 1

    async def test_workspace_basket_and_paper_trade_operations(self, client: AsyncClient):
        reg_res = await client.post(
            "/api/v1/auth/register",
            json={"email": "trade_user@example.com", "password": "SecurePassword9!"},
        )
        access_tok = reg_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_tok}"}

        # Create new custom basket
        basket_res = await client.post(
            "/api/v1/workspace/baskets",
            headers=headers,
            json={"name": "Tactical Swing", "capital": 50000.0, "risk_persona": "Aggressive"},
        )
        assert basket_res.status_code == 201
        assert basket_res.json()["name"] == "Tactical Swing"

        # Place a paper trade
        trade_res = await client.post(
            "/api/v1/workspace/trades",
            headers=headers,
            json={
                "symbol": "AAPL",
                "order_type": "MARKET",
                "side": "BUY",
                "shares": 10.0,
                "executed_price": 185.50,
            },
        )
        assert trade_res.status_code == 201
        trade_data = trade_res.json()
        assert trade_data["symbol"] == "AAPL"
        assert trade_data["shares"] == 10.0
        assert trade_data["status"] == "EXECUTED"

        # Re-fetch active workspace to verify updated children
        ws_res = await client.get("/api/v1/workspace/active", headers=headers)
        ws_data = ws_res.json()
        assert len(ws_data["baskets"]) == 2  # default basket + new basket
        assert len(ws_data["paper_trades"]) == 1

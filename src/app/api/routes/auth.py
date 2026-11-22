"""Authentication and user management REST API routes."""

import logging
import re
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth.dependencies import get_current_user, get_optional_user
from app.auth.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.db.models import (
    BasketHolding,
    PortfolioBasket,
    RiskCalibration,
    User,
    Workspace,
)
from app.db.session import get_db

logger = logging.getLogger("quantniti.auth.api")

router = APIRouter(tags=["Authentication & Multi-Tenant Access"])

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# Request & Response Schemas
class RegisterRequest(BaseModel):
    email: str = Field(..., description="Valid email address")
    password: str = Field(..., min_length=6, max_length=72, description="Password (6 to 72 characters)")
    full_name: Optional[str] = Field(None, max_length=255, description="Full display name")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        clean = v.strip().lower()
        if not EMAIL_REGEX.match(clean):
            raise ValueError("Invalid email format")
        return clean


class LoginRequest(BaseModel):
    email: str = Field(..., description="Account email address")
    password: str = Field(..., min_length=1, max_length=72)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        return v.strip().lower()


class RefreshRequest(BaseModel):
    refresh_token: str = Field(..., description="Valid JWT refresh token")


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: Optional[str] = None
    created_at: Optional[str] = None
    is_active: bool
    is_guest: bool = False


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]
    workspace: Optional[Dict[str, Any]] = None


class TokenRefreshResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class MeResponse(BaseModel):
    id: str
    email: str
    full_name: Optional[str] = None
    created_at: Optional[str] = None
    is_active: bool
    is_guest: bool = False
    workspaces: List[Dict[str, Any]] = []


@router.post("/auth/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    """Register a new user and automatically provision an isolated default workspace."""
    clean_email = payload.email.strip().lower()

    # Check if user already exists
    stmt = select(User).where(User.email == clean_email)
    res = await db.execute(stmt)
    existing_user = res.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists.",
        )

    # Hash password and create user
    hashed_pw = hash_password(payload.password)
    user = User(
        email=clean_email,
        hashed_password=hashed_pw,
        full_name=payload.full_name.strip() if payload.full_name else None,
        is_active=True,
    )
    db.add(user)
    await db.flush()  # populate user.id

    # Auto-provision default workspace
    ws_name = f"{user.full_name or 'Personal'}'s Workspace"
    workspace = Workspace(
        user_id=user.id,
        name=ws_name,
        is_default=True,
    )
    db.add(workspace)
    await db.flush()  # populate workspace.id

    # Auto-provision default Risk Calibration
    risk_cal = RiskCalibration(
        workspace_id=workspace.id,
        persona="Moderate",
        max_volatility=0.20,
        max_drawdown_limit=0.15,
        esg_preference=False,
    )
    db.add(risk_cal)

    # Auto-provision default Core Portfolio Basket
    basket = PortfolioBasket(
        workspace_id=workspace.id,
        name="Core Alpha Growth Basket",
        capital=100000.0,
        risk_persona="Moderate",
    )
    db.add(basket)
    await db.flush()  # populate basket.id

    # Add standard default holdings
    holdings = [
        BasketHolding(basket_id=basket.id, symbol="AAPL", target_weight=0.35, actual_shares=10, avg_price=185.0),
        BasketHolding(basket_id=basket.id, symbol="MSFT", target_weight=0.35, actual_shares=8, avg_price=420.0),
        BasketHolding(basket_id=basket.id, symbol="NVDA", target_weight=0.30, actual_shares=15, avg_price=125.0),
    ]
    db.add_all(holdings)
    await db.commit()

    # Generate JWT pair
    access_token = create_access_token(subject=user.id, extra_claims={"email": user.email})
    refresh_token = create_refresh_token(subject=user.id)

    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=user.to_dict(),
        workspace=workspace.to_dict(),
    )


@router.post("/auth/login", response_model=AuthResponse)
async def login(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """Authenticate with email and password to receive JWT credentials."""
    clean_email = payload.email.strip().lower()

    stmt = select(User).where(User.email == clean_email)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated.",
        )

    # Fetch default workspace
    ws_stmt = select(Workspace).where(Workspace.user_id == user.id, Workspace.is_default == True)
    ws_res = await db.execute(ws_stmt)
    workspace = ws_res.scalar_one_or_none()

    access_token = create_access_token(subject=user.id, extra_claims={"email": user.email})
    refresh_token = create_refresh_token(subject=user.id)

    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=user.to_dict(),
        workspace=workspace.to_dict() if workspace else None,
    )


@router.post("/auth/refresh", response_model=TokenRefreshResponse)
async def refresh_token(
    payload: RefreshRequest,
    db: AsyncSession = Depends(get_db),
):
    """Exchange a valid refresh token for a new access token and refresh token."""
    try:
        token_data = decode_token(payload.refresh_token)
        if token_data.get("token_type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type: expected refresh token.",
            )
        user_id = token_data.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload.",
            )
    except Exception as exc:
        logger.debug(f"Refresh token error: {exc}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    stmt = select(User).where(User.id == user_id)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account no longer active or found.",
        )

    new_access = create_access_token(subject=user.id, extra_claims={"email": user.email})
    new_refresh = create_refresh_token(subject=user.id)

    return TokenRefreshResponse(
        access_token=new_access,
        refresh_token=new_refresh,
        token_type="bearer",
    )


@router.get("/auth/me", response_model=MeResponse)
async def get_me(
    user: Optional[User] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve current user profile and workspaces, with frictionless guest fallback."""
    if user is not None:
        # Load user workspaces
        ws_stmt = select(Workspace).where(Workspace.user_id == user.id)
        ws_res = await db.execute(ws_stmt)
        workspaces = [w.to_dict() for w in ws_res.scalars().all()]

        return MeResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            created_at=user.created_at.isoformat() if user.created_at else None,
            is_active=user.is_active,
            is_guest=False,
            workspaces=workspaces,
        )

    # Guest preview fallback mode
    return MeResponse(
        id="guest-demo",
        email="guest@quantniti.local",
        full_name="Guest Investor",
        created_at="2026-01-01T00:00:00Z",
        is_active=True,
        is_guest=True,
        workspaces=[
            {
                "id": "demo-workspace",
                "user_id": "guest-demo",
                "name": "Demo Guest Workspace",
                "is_default": True,
            }
        ],
    )

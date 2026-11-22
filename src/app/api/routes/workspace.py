"""Multi-tenant Workspace and Portfolio management REST API routes."""

import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth.dependencies import get_current_user, get_optional_user
from app.db.models import (
    BasketHolding,
    PaperTradeOrder,
    PortfolioBasket,
    RiskCalibration,
    User,
    Workspace,
)
from app.db.session import get_db

logger = logging.getLogger("quantniti.workspace.api")

router = APIRouter(tags=["Multi-Tenant Workspace & Portfolio"])


# Request & Response Schemas
class CreateBasketRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    capital: float = Field(default=100000.0, gt=0)
    risk_persona: str = Field(default="Moderate")
    workspace_id: Optional[str] = None


class HoldingItem(BaseModel):
    symbol: str = Field(..., min_length=1)
    target_weight: float = Field(default=0.0, ge=0.0, le=1.0)
    actual_shares: float = Field(default=0.0, ge=0.0)
    avg_price: float = Field(default=0.0, ge=0.0)


class UpdateHoldingsRequest(BaseModel):
    basket_id: str
    holdings: List[HoldingItem]


class RiskCalibrationRequest(BaseModel):
    workspace_id: Optional[str] = None
    persona: str = Field(default="Moderate")
    max_volatility: float = Field(default=0.20, gt=0.0, le=1.0)
    max_drawdown_limit: float = Field(default=0.15, gt=0.0, le=1.0)
    esg_preference: bool = False


class PaperTradeRequest(BaseModel):
    workspace_id: Optional[str] = None
    symbol: str = Field(..., min_length=1)
    order_type: str = Field(default="MARKET", pattern="^(MARKET|LIMIT)$")
    side: str = Field(default="BUY", pattern="^(BUY|SELL)$")
    shares: float = Field(..., gt=0.0)
    executed_price: float = Field(default=0.0, ge=0.0)


def build_demo_workspace() -> Dict[str, Any]:
    """Construct demo guest workspace with realistic multi-asset data."""
    return {
        "id": "demo-workspace",
        "user_id": "guest-demo",
        "name": "Demo Multi-Asset Workspace",
        "created_at": "2026-01-01T00:00:00Z",
        "is_default": True,
        "is_guest": True,
        "baskets": [
            {
                "id": "demo-basket-alpha",
                "workspace_id": "demo-workspace",
                "name": "Flagship HRP Alpha Basket",
                "capital": 100000.0,
                "risk_persona": "Moderate",
                "created_at": "2026-01-01T00:00:00Z",
                "updated_at": "2026-01-01T00:00:00Z",
                "holdings": [
                    {
                        "id": "demo-h-1",
                        "basket_id": "demo-basket-alpha",
                        "symbol": "AAPL",
                        "target_weight": 0.25,
                        "actual_shares": 50.0,
                        "avg_price": 182.50,
                    },
                    {
                        "id": "demo-h-2",
                        "basket_id": "demo-basket-alpha",
                        "symbol": "MSFT",
                        "target_weight": 0.25,
                        "actual_shares": 40.0,
                        "avg_price": 415.00,
                    },
                    {
                        "id": "demo-h-3",
                        "basket_id": "demo-basket-alpha",
                        "symbol": "NVDA",
                        "target_weight": 0.25,
                        "actual_shares": 100.0,
                        "avg_price": 120.00,
                    },
                    {
                        "id": "demo-h-4",
                        "basket_id": "demo-basket-alpha",
                        "symbol": "GOOGL",
                        "target_weight": 0.25,
                        "actual_shares": 60.0,
                        "avg_price": 165.00,
                    },
                ],
            }
        ],
        "risk_calibrations": [
            {
                "id": "demo-risk-1",
                "workspace_id": "demo-workspace",
                "persona": "Moderate",
                "max_volatility": 0.18,
                "max_drawdown_limit": 0.12,
                "esg_preference": False,
            }
        ],
        "paper_trades": [
            {
                "id": "demo-trade-1",
                "workspace_id": "demo-workspace",
                "symbol": "NVDA",
                "order_type": "MARKET",
                "side": "BUY",
                "shares": 25.0,
                "executed_price": 119.50,
                "status": "EXECUTED",
                "created_at": "2026-01-15T14:30:00Z",
            }
        ],
    }


@router.get("/workspace/active")
async def get_active_workspace(
    workspace_id: Optional[str] = Query(None, description="Specific workspace ID to retrieve"),
    user: Optional[User] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve active workspace with baskets, holdings, risk calibrations, and paper trades.

    Includes automatic frictionless fallback to demo workspace if unauthenticated.
    """
    if user is None:
        return build_demo_workspace()

    # User is authenticated: find specified or default workspace
    stmt = (
        select(Workspace)
        .options(
            selectinload(Workspace.baskets).selectinload(PortfolioBasket.holdings),
            selectinload(Workspace.risk_calibrations),
            selectinload(Workspace.paper_trades),
        )
        .where(Workspace.user_id == user.id)
    )

    if workspace_id:
        stmt = stmt.where(Workspace.id == workspace_id)
    else:
        stmt = stmt.order_by(Workspace.is_default.desc(), Workspace.created_at.asc())

    res = await db.execute(stmt)
    workspace = res.scalars().first()

    if not workspace:
        # If user has no workspace, automatically provision one
        workspace = Workspace(
            user_id=user.id,
            name=f"{user.full_name or 'Personal'}'s Workspace",
            is_default=True,
        )
        db.add(workspace)
        await db.flush()

        risk_cal = RiskCalibration(
            workspace_id=workspace.id,
            persona="Moderate",
            max_volatility=0.20,
            max_drawdown_limit=0.15,
            esg_preference=False,
        )
        db.add(risk_cal)
        await db.commit()

        # Re-fetch with loaded relationships
        res = await db.execute(
            select(Workspace)
            .options(
                selectinload(Workspace.baskets).selectinload(PortfolioBasket.holdings),
                selectinload(Workspace.risk_calibrations),
                selectinload(Workspace.paper_trades),
            )
            .where(Workspace.id == workspace.id)
        )
        workspace = res.scalar_one()

    data = workspace.to_dict(include_children=True)
    data["is_guest"] = False
    return data


@router.get("/workspaces")
async def list_workspaces(
    user: Optional[User] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """List all workspaces owned by the user, with guest demo fallback."""
    if user is None:
        return [
            {
                "id": "demo-workspace",
                "user_id": "guest-demo",
                "name": "Demo Guest Workspace",
                "is_default": True,
                "is_guest": True,
            }
        ]

    stmt = select(Workspace).where(Workspace.user_id == user.id).order_by(Workspace.created_at.asc())
    res = await db.execute(stmt)
    workspaces = res.scalars().all()
    return [w.to_dict(include_children=False) for w in workspaces]


@router.post("/workspace/baskets", status_code=status.HTTP_201_CREATED)
async def create_basket(
    payload: CreateBasketRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new portfolio basket in the user's workspace."""
    target_ws_id = payload.workspace_id

    if not target_ws_id:
        stmt = select(Workspace).where(Workspace.user_id == user.id, Workspace.is_default == True)
        res = await db.execute(stmt)
        ws = res.scalar_one_or_none()
        if not ws:
            raise HTTPException(status_code=404, detail="Workspace not found")
        target_ws_id = ws.id
    else:
        stmt = select(Workspace).where(Workspace.id == target_ws_id, Workspace.user_id == user.id)
        res = await db.execute(stmt)
        if not res.scalar_one_or_none():
            raise HTTPException(status_code=403, detail="Unauthorized workspace access")

    basket = PortfolioBasket(
        workspace_id=target_ws_id,
        name=payload.name,
        capital=payload.capital,
        risk_persona=payload.risk_persona,
    )
    db.add(basket)
    await db.commit()
    await db.refresh(basket)

    return basket.to_dict(include_holdings=False)


@router.post("/workspace/trades", status_code=status.HTTP_201_CREATED)
async def place_paper_trade(
    payload: PaperTradeRequest,
    user: Optional[User] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """Execute a simulated paper trade order within the active workspace."""
    if user is None:
        # In guest mode, echo back simulated execution
        return {
            "id": "demo-order-simulated",
            "workspace_id": "demo-workspace",
            "symbol": payload.symbol.upper(),
            "order_type": payload.order_type,
            "side": payload.side,
            "shares": payload.shares,
            "executed_price": payload.executed_price or 150.0,
            "status": "EXECUTED",
            "is_guest": True,
        }

    target_ws_id = payload.workspace_id
    if not target_ws_id:
        stmt = select(Workspace).where(Workspace.user_id == user.id, Workspace.is_default == True)
        res = await db.execute(stmt)
        ws = res.scalar_one_or_none()
        if not ws:
            raise HTTPException(status_code=404, detail="Workspace not found")
        target_ws_id = ws.id
    else:
        stmt = select(Workspace).where(Workspace.id == target_ws_id, Workspace.user_id == user.id)
        res = await db.execute(stmt)
        if not res.scalar_one_or_none():
            raise HTTPException(status_code=403, detail="Unauthorized workspace access")

    order = PaperTradeOrder(
        workspace_id=target_ws_id,
        symbol=payload.symbol.upper(),
        order_type=payload.order_type,
        side=payload.side,
        shares=payload.shares,
        executed_price=payload.executed_price,
        status="EXECUTED",
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)

    return order.to_dict()


@router.put("/workspace/baskets/{basket_id}/holdings")
async def update_basket_holdings(
    basket_id: str,
    payload: UpdateHoldingsRequest,
    user: Optional[User] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """Replace and update holdings for a specific portfolio basket."""
    if user is None:
        return {
            "basket_id": basket_id,
            "status": "UPDATED_GUEST",
            "holdings_count": len(payload.holdings),
            "is_guest": True,
        }

    # Verify basket ownership through user's workspaces
    stmt = (
        select(PortfolioBasket)
        .join(Workspace, PortfolioBasket.workspace_id == Workspace.id)
        .where(PortfolioBasket.id == basket_id, Workspace.user_id == user.id)
    )
    res = await db.execute(stmt)
    basket = res.scalar_one_or_none()
    if not basket:
        raise HTTPException(status_code=404, detail="Basket not found or unauthorized")

    # Delete existing holdings
    del_stmt = select(BasketHolding).where(BasketHolding.basket_id == basket_id)
    existing_res = await db.execute(del_stmt)
    for h in existing_res.scalars().all():
        await db.delete(h)

    # Insert new holdings
    new_holdings = []
    for item in payload.holdings:
        holding = BasketHolding(
            basket_id=basket_id,
            symbol=item.symbol.upper(),
            target_weight=item.target_weight,
            actual_shares=item.actual_shares,
            avg_price=item.avg_price,
        )
        db.add(holding)
        new_holdings.append(holding)

    await db.commit()
    return {
        "basket_id": basket_id,
        "status": "SUCCESS",
        "holdings_count": len(new_holdings),
        "holdings": [h.to_dict() for h in new_holdings],
    }


@router.put("/workspace/risk-calibration")
async def update_risk_calibration(
    payload: RiskCalibrationRequest,
    user: Optional[User] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db),
):
    """Update risk calibration settings for user's workspace."""
    if user is None:
        return {
            "status": "UPDATED_GUEST",
            "persona": payload.persona,
            "max_volatility": payload.max_volatility,
            "max_drawdown_limit": payload.max_drawdown_limit,
            "esg_preference": payload.esg_preference,
            "is_guest": True,
        }

    target_ws_id = payload.workspace_id
    if not target_ws_id:
        stmt = select(Workspace).where(Workspace.user_id == user.id, Workspace.is_default == True)
        res = await db.execute(stmt)
        ws = res.scalar_one_or_none()
        if not ws:
            raise HTTPException(status_code=404, detail="Default workspace not found")
        target_ws_id = ws.id
    else:
        stmt = select(Workspace).where(Workspace.id == target_ws_id, Workspace.user_id == user.id)
        res = await db.execute(stmt)
        if not res.scalar_one_or_none():
            raise HTTPException(status_code=403, detail="Unauthorized workspace access")

    stmt = select(RiskCalibration).where(RiskCalibration.workspace_id == target_ws_id)
    res = await db.execute(stmt)
    calib = res.scalar_one_or_none()
    if not calib:
        calib = RiskCalibration(
            workspace_id=target_ws_id,
            persona=payload.persona,
            max_volatility=payload.max_volatility,
            max_drawdown_limit=payload.max_drawdown_limit,
            esg_preference=payload.esg_preference,
        )
        db.add(calib)
    else:
        calib.persona = payload.persona
        calib.max_volatility = payload.max_volatility
        calib.max_drawdown_limit = payload.max_drawdown_limit
        calib.esg_preference = payload.esg_preference

    await db.commit()
    await db.refresh(calib)
    return calib.to_dict()

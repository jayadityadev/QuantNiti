"""Domain models for QuantNiti Multi-Tenant Database Architecture.

Supports PostgreSQL (Neon Serverless) and async SQLite fallback.
"""

from datetime import datetime, timezone
from typing import List, Optional
import uuid

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


def generate_uuid() -> str:
    """Generate a UUID4 hex string."""
    return str(uuid.uuid4())


def utc_now() -> datetime:
    """Return timezone-aware current UTC datetime."""
    return datetime.now(timezone.utc)


class User(Base):
    """User account model for authentication and multi-tenancy."""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    workspaces: Mapped[List["Workspace"]] = relationship(
        "Workspace",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "is_active": self.is_active,
        }


class Workspace(Base):
    """Workspace partition for multi-tenant isolation."""

    __tablename__ = "workspaces"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="workspaces")
    baskets: Mapped[List["PortfolioBasket"]] = relationship(
        "PortfolioBasket",
        back_populates="workspace",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    risk_calibrations: Mapped[List["RiskCalibration"]] = relationship(
        "RiskCalibration",
        back_populates="workspace",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    paper_trades: Mapped[List["PaperTradeOrder"]] = relationship(
        "PaperTradeOrder",
        back_populates="workspace",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def to_dict(self, include_children: bool = False) -> dict:
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "is_default": self.is_default,
        }
        if include_children:
            data["baskets"] = [b.to_dict(include_holdings=True) for b in self.baskets]
            data["risk_calibrations"] = [r.to_dict() for r in self.risk_calibrations]
            data["paper_trades"] = [p.to_dict() for p in self.paper_trades]
        return data


class PortfolioBasket(Base):
    """Portfolio basket holding an investment strategy or asset allocation."""

    __tablename__ = "portfolio_baskets"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    workspace_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    capital: Mapped[float] = mapped_column(Float, default=100000.0, nullable=False)
    risk_persona: Mapped[str] = mapped_column(String(50), default="Moderate", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    # Relationships
    workspace: Mapped["Workspace"] = relationship("Workspace", back_populates="baskets")
    holdings: Mapped[List["BasketHolding"]] = relationship(
        "BasketHolding",
        back_populates="basket",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def to_dict(self, include_holdings: bool = True) -> dict:
        data = {
            "id": self.id,
            "workspace_id": self.workspace_id,
            "name": self.name,
            "capital": self.capital,
            "risk_persona": self.risk_persona,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_holdings:
            data["holdings"] = [h.to_dict() for h in self.holdings]
        return data


class BasketHolding(Base):
    """Individual stock/asset holding within a portfolio basket."""

    __tablename__ = "basket_holdings"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    basket_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("portfolio_baskets.id", ondelete="CASCADE"), nullable=False, index=True
    )
    symbol: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    target_weight: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    actual_shares: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    avg_price: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # Relationships
    basket: Mapped["PortfolioBasket"] = relationship("PortfolioBasket", back_populates="holdings")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "basket_id": self.basket_id,
            "symbol": self.symbol,
            "target_weight": self.target_weight,
            "actual_shares": self.actual_shares,
            "avg_price": self.avg_price,
        }


class RiskCalibration(Base):
    """User risk profile, constraints, and ESG preferences for a workspace."""

    __tablename__ = "risk_calibrations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    workspace_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True
    )
    persona: Mapped[str] = mapped_column(String(50), default="Moderate", nullable=False)
    max_volatility: Mapped[float] = mapped_column(Float, default=0.20, nullable=False)
    max_drawdown_limit: Mapped[float] = mapped_column(Float, default=0.15, nullable=False)
    esg_preference: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    workspace: Mapped["Workspace"] = relationship("Workspace", back_populates="risk_calibrations")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "workspace_id": self.workspace_id,
            "persona": self.persona,
            "max_volatility": self.max_volatility,
            "max_drawdown_limit": self.max_drawdown_limit,
            "esg_preference": self.esg_preference,
        }


class PaperTradeOrder(Base):
    """Simulated paper trading order for execution tracking."""

    __tablename__ = "paper_trade_orders"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    workspace_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True
    )
    symbol: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    order_type: Mapped[str] = mapped_column(String(50), default="MARKET", nullable=False)
    side: Mapped[str] = mapped_column(String(20), default="BUY", nullable=False)
    shares: Mapped[float] = mapped_column(Float, nullable=False)
    executed_price: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="EXECUTED", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    # Relationships
    workspace: Mapped["Workspace"] = relationship("Workspace", back_populates="paper_trades")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "workspace_id": self.workspace_id,
            "symbol": self.symbol,
            "order_type": self.order_type,
            "side": self.side,
            "shares": self.shares,
            "executed_price": self.executed_price,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

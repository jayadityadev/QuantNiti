"""Pre-Trade Indian Statutory Friction and Transaction Cost Engine.

Calculates statutory taxes, regulatory fees, and market impact for Indian equities (NSE):
- Securities Transaction Tax (STT): 0.1% on equity delivery buy/sell
- NSE Exchange Turnover Charges: 0.00325%
- SEBI Turnover Fee: ₹10 per crore (0.0001% = 0.000001 fraction)
- Stamp Duty: 0.015% on buy orders only
- GST: 18% on exchange fees and brokerage
- Slippage / Impact Cost: Configurable 5-10 bps based on asset liquidity tier
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field


@dataclass
class OrderFrictionItem:
    symbol: str
    action: Literal["BUY", "SELL"]
    shares: int
    price: float
    liquidity_tier: Literal["large", "mid", "small"] = "large"
    slippage_bps: Optional[float] = None


class StatutoryFrictionBreakdown(BaseModel):
    total_turnover: float = Field(..., description="Gross order value in INR")
    buy_turnover: float = Field(default=0.0)
    sell_turnover: float = Field(default=0.0)
    stt: float = Field(..., description="Securities Transaction Tax (0.1% on delivery buy/sell)")
    exchange_charges: float = Field(..., description="NSE Exchange Turnover Charges (0.00325%)")
    sebi_fee: float = Field(..., description="SEBI Turnover Fee (₹10/crore = 0.0001%)")
    stamp_duty: float = Field(..., description="Stamp Duty (0.015% on buy transactions)")
    gst: float = Field(..., description="GST (18% on exchange charges and SEBI fee)")
    slippage: float = Field(..., description="Estimated market impact/slippage (5-10 bps)")
    brokerage: float = Field(default=0.0, description="Brokerage commission (0 for discount delivery)")
    total_friction: float = Field(..., description="Total friction sum in INR")
    friction_bps: float = Field(..., description="Friction expressed in basis points of turnover")
    friction_summary: str = Field(..., description="Formatted summary breakdown string")


def get_slippage_bps_for_tier(tier: str) -> float:
    t = (tier or "large").lower()
    if t in ("large", "largecap", "nifty50", "index"):
        return 5.0
    elif t in ("mid", "midcap"):
        return 7.5
    elif t in ("small", "smallcap", "micro"):
        return 10.0
    return 5.0


def calculate_indian_statutory_friction(
    orders: List[Union[Dict[str, Any], OrderFrictionItem]],
    brokerage_per_order: float = 0.0,
    default_slippage_bps: float = 5.0,
) -> StatutoryFrictionBreakdown:
    """Calculate exact pre-trade statutory friction for Indian equity delivery orders."""
    buy_turnover = 0.0
    sell_turnover = 0.0
    total_slippage = 0.0

    for item in orders:
        if isinstance(item, OrderFrictionItem):
            sym = item.symbol
            act = item.action.upper()
            qty = abs(item.shares)
            px = max(0.0, float(item.price))
            tier = item.liquidity_tier
            bps = item.slippage_bps if item.slippage_bps is not None else get_slippage_bps_for_tier(tier)
        else:
            sym = str(item.get("symbol", ""))
            act = str(item.get("action", "BUY")).upper()
            qty = abs(int(item.get("shares") or item.get("quantity") or 0))
            px = max(0.0, float(item.get("price") or item.get("current_price") or 0.0))
            tier = str(item.get("liquidity_tier", "large"))
            bps = float(item["slippage_bps"]) if "slippage_bps" in item else get_slippage_bps_for_tier(tier)

        order_val = qty * px
        if act == "BUY":
            buy_turnover += order_val
        else:
            sell_turnover += order_val

        # Impact / Slippage per asset tier
        effective_bps = bps if bps is not None else default_slippage_bps
        total_slippage += order_val * (effective_bps / 10000.0)

    total_turnover = buy_turnover + sell_turnover

    if total_turnover <= 0.0:
        return StatutoryFrictionBreakdown(
            total_turnover=0.0,
            buy_turnover=0.0,
            sell_turnover=0.0,
            stt=0.0,
            exchange_charges=0.0,
            sebi_fee=0.0,
            stamp_duty=0.0,
            gst=0.0,
            slippage=0.0,
            brokerage=0.0,
            total_friction=0.0,
            friction_bps=0.0,
            friction_summary="Est. Friction: ₹0 — STT: ₹0, Stamp Duty: ₹0, GST: ₹0, Slippage: ₹0",
        )

    # 1. STT: 0.1% on equity delivery buy and sell
    stt = total_turnover * 0.0010

    # 2. NSE Exchange Turnover Charges: 0.00325%
    exchange_charges = total_turnover * 0.0000325

    # 3. SEBI Turnover Fee: ₹10 per crore = 0.0001% = 0.000001 fraction
    sebi_fee = total_turnover * 0.000001

    # 4. Stamp Duty: 0.015% on BUY orders only
    stamp_duty = buy_turnover * 0.00015

    # 5. Brokerage (e.g. 0 on delivery or fixed per order)
    total_brokerage = len(orders) * brokerage_per_order

    # 6. GST: 18% on exchange charges + SEBI fee + brokerage
    taxable_services = exchange_charges + sebi_fee + total_brokerage
    gst = taxable_services * 0.18

    # Total friction
    total_friction = stt + exchange_charges + sebi_fee + stamp_duty + gst + total_slippage + total_brokerage
    friction_bps = (total_friction / total_turnover) * 10000.0 if total_turnover > 0 else 0.0

    # Summary format: Est. Friction: ₹48 — STT: ₹25, Stamp Duty: ₹8, GST: ₹7, Slippage: ₹8
    summary = (
        f"Est. Friction: ₹{round(total_friction)} — "
        f"STT: ₹{round(stt)}, Stamp Duty: ₹{round(stampDuty := stamp_duty)}, GST: ₹{round(gst)}, Slippage: ₹{round(total_slippage)}"
    )

    return StatutoryFrictionBreakdown(
        total_turnover=round(total_turnover, 2),
        buy_turnover=round(buy_turnover, 2),
        sell_turnover=round(sell_turnover, 2),
        stt=round(stt, 2),
        exchange_charges=round(exchange_charges, 2),
        sebi_fee=round(sebi_fee, 2),
        stamp_duty=round(stamp_duty, 2),
        gst=round(gst, 2),
        slippage=round(total_slippage, 2),
        brokerage=round(total_brokerage, 2),
        total_friction=round(total_friction, 2),
        friction_bps=round(friction_bps, 2),
        friction_summary=summary,
    )

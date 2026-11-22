"""Unit tests for Indian Statutory Friction Engine (src/app/core/friction.py)."""

import pytest
from app.core.friction import (
    calculate_indian_statutory_friction,
    get_slippage_bps_for_tier,
    OrderFrictionItem,
)


def test_slippage_bps_tiers():
    assert get_slippage_bps_for_tier("large") == 5.0
    assert get_slippage_bps_for_tier("nifty50") == 5.0
    assert get_slippage_bps_for_tier("mid") == 7.5
    assert get_slippage_bps_for_tier("small") == 10.0


def test_friction_calculation_buy_order():
    # Buy 100 shares @ Rs 2,500 = Turnover Rs 250,000
    orders = [
        OrderFrictionItem(
            symbol="RELIANCE",
            action="BUY",
            shares=100,
            price=2500.0,
            liquidity_tier="large",
        )
    ]
    res = calculate_indian_statutory_friction(orders)

    assert res.total_turnover == 250000.0
    assert res.buy_turnover == 250000.0
    assert res.sell_turnover == 0.0

    # STT: 0.1% of 250,000 = 250.00
    assert res.stt == 250.00

    # Exchange charges: 0.00325% of 250,000 = 8.125 -> 8.12 or 8.13
    assert abs(res.exchange_charges - 8.125) < 0.02

    # SEBI turnover fee: Rs 10 per crore = 250,000 * 0.000001 = 0.25
    assert res.sebi_fee == 0.25

    # Stamp duty: 0.015% of 250,000 = 37.50
    assert res.stamp_duty == 37.50

    # GST: 18% on (8.125 + 0.25) = 1.5075 -> 1.51
    assert abs(res.gst - 1.51) < 0.02

    # Slippage: 5 bps (0.05%) of 250,000 = 125.00
    assert res.slippage == 125.00

    # Total friction
    expected_total = 250.0 + 8.125 + 0.25 + 37.50 + 1.5075 + 125.0
    assert abs(res.total_friction - expected_total) < 0.1
    assert "Est. Friction: ₹" in res.friction_summary


def test_friction_calculation_sell_order_no_stamp_duty():
    # Sell order: Stamp duty must be 0.0
    orders = [
        OrderFrictionItem(
            symbol="TCS",
            action="SELL",
            shares=10,
            price=4000.0,
            liquidity_tier="large",
        )
    ]
    res = calculate_indian_statutory_friction(orders)

    assert res.buy_turnover == 0.0
    assert res.sell_turnover == 40000.0
    assert res.stamp_duty == 0.0  # Stamp duty applies only to buy delivery
    assert res.stt == 40.0  # 0.1% on sell delivery

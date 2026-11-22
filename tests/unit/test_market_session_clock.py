"""Unit tests for Centralized 5-State IST Market Session Clock (src/app/core/market_clock.py)."""

from datetime import datetime
import pytest
from app.core.market_clock import (
    evaluate_market_session,
    MarketSessionState,
    IST_TIMEZONE,
)


def test_market_session_live_trading_hours():
    # Wednesday 11:30 AM IST (Normal trading day, active market hours)
    wed_dt = datetime(2026, 3, 11, 11, 30, 0, tzinfo=IST_TIMEZONE)
    last_tick = datetime(2026, 3, 11, 11, 29, 55, tzinfo=IST_TIMEZONE)  # 5s ago

    info = evaluate_market_session(now_dt=wed_dt, last_tick_timestamp=last_tick)
    assert info.state == MarketSessionState.LIVE
    assert info.is_market_hours is True
    assert info.is_trading_day is True
    assert info.label == "NSE Live"


def test_market_session_stale_tick():
    # Wednesday 11:30 AM IST, but last tick was 25s ago (> 15s)
    wed_dt = datetime(2026, 3, 11, 11, 30, 0, tzinfo=IST_TIMEZONE)
    last_tick = datetime(2026, 3, 11, 11, 29, 35, tzinfo=IST_TIMEZONE)  # 25s ago

    info = evaluate_market_session(now_dt=wed_dt, last_tick_timestamp=last_tick)
    assert info.state == MarketSessionState.STALE
    assert info.label == "Feed Stale"
    assert "Last tick 25s ago" in info.status_text


def test_market_session_resyncing():
    wed_dt = datetime(2026, 3, 11, 11, 30, 0, tzinfo=IST_TIMEZONE)
    info = evaluate_market_session(now_dt=wed_dt, is_resyncing=True)
    assert info.state == MarketSessionState.RESYNCING
    assert info.label == "Resyncing"


def test_market_session_closed_weekend():
    # Sunday 14:00 IST
    sun_dt = datetime(2026, 3, 15, 14, 0, 0, tzinfo=IST_TIMEZONE)
    info = evaluate_market_session(now_dt=sun_dt)

    assert info.state == MarketSessionState.CLOSED
    assert info.is_trading_day is False
    assert info.label == "Market Closed"
    assert "Reopens Mon 09:15 IST" in info.status_text


def test_market_session_closed_holiday():
    # Republic Day: Jan 26, 2026
    holiday_dt = datetime(2026, 1, 26, 10, 30, 0, tzinfo=IST_TIMEZONE)
    info = evaluate_market_session(now_dt=holiday_dt)

    assert info.state == MarketSessionState.CLOSED
    assert info.is_trading_day is False
    assert "Market Closed" in info.status_text


def test_market_session_eod_snapshot():
    # Wednesday 17:00 IST (Off-market trading day hours)
    eod_dt = datetime(2026, 3, 11, 17, 0, 0, tzinfo=IST_TIMEZONE)
    info = evaluate_market_session(now_dt=eod_dt)

    assert info.state == MarketSessionState.SNAPSHOT
    assert info.is_trading_day is True
    assert info.is_market_hours is False
    assert "15:30 IST" in info.status_text

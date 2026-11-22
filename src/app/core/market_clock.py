"""Centralized 5-State IST Market Session and Telemetry Freshness Engine.

States:
- LIVE: During market hours (09:15 to 15:30 IST on NSE trading days) with active streaming updates.
- SNAPSHOT: Off-market hours displaying authoritative End-of-Day (EOD) closing data.
- CLOSED: Weekend or market holiday (e.g. 'NSE: Market Closed · Reopens Mon 09:15 IST').
- STALE: Ticks older than 15s during active market hours flagged with a warning pill.
- RESYNCING: Connection drop / recovery state.
"""

from datetime import datetime, time as dtime, timedelta, timezone
from enum import Enum
from typing import Optional, Set
from pydantic import BaseModel, Field

IST_TIMEZONE = timezone(timedelta(hours=5, minutes=30), name="IST")

# Known National Stock Exchange (NSE) Trading Holidays (2025/2026 standard calendar)
NSE_HOLIDAYS_YYYY_MM_DD: Set[str] = {
    # 2025
    "2025-01-26", "2025-02-26", "2025-03-14", "2025-03-31", "2025-04-10",
    "2025-04-14", "2025-04-18", "2025-05-01", "2025-08-15", "2025-08-27",
    "2025-10-02", "2025-10-21", "2025-10-22", "2025-11-05", "2025-12-25",
    # 2026
    "2026-01-26", "2026-03-03", "2026-03-20", "2026-04-03", "2026-04-14",
    "2026-05-01", "2026-08-15", "2026-09-04", "2026-10-02", "2026-10-20",
    "2026-11-08", "2026-11-10", "2026-12-25",
}


class MarketSessionState(str, Enum):
    LIVE = "LIVE"
    SNAPSHOT = "SNAPSHOT"
    CLOSED = "CLOSED"
    STALE = "STALE"
    RESYNCING = "RESYNCING"


class MarketSessionInfo(BaseModel):
    state: MarketSessionState
    label: str
    status_text: str
    ist_time_str: str
    is_trading_day: bool
    is_market_hours: bool
    next_open_str: Optional[str] = None
    last_tick_age_seconds: Optional[float] = None


def get_current_ist_datetime() -> datetime:
    return datetime.now(IST_TIMEZONE)


def is_nse_holiday(dt: datetime) -> bool:
    date_str = dt.strftime("%Y-%m-%d")
    return date_str in NSE_HOLIDAYS_YYYY_MM_DD


def get_next_trading_day_open(dt: datetime) -> datetime:
    """Find the next trading day 09:15 IST."""
    candidate = dt + timedelta(days=1)
    while candidate.weekday() in (5, 6) or is_nse_holiday(candidate):
        candidate += timedelta(days=1)
    return candidate.replace(hour=9, minute=15, second=0, microsecond=0)


def evaluate_market_session(
    now_dt: Optional[datetime] = None,
    last_tick_timestamp: Optional[datetime] = None,
    is_resyncing: bool = False,
) -> MarketSessionInfo:
    """Evaluate 5-state IST market session clock with authoritative labels."""
    now_ist = now_dt.astimezone(IST_TIMEZONE) if now_dt else get_current_ist_datetime()
    weekday = now_ist.weekday()  # 0=Mon ... 4=Fri, 5=Sat, 6=Sun
    is_weekend = weekday in (5, 6)
    is_holiday = is_nse_holiday(now_ist)
    is_trading_day = not is_weekend and not is_holiday

    market_open_time = dtime(9, 15, 0)
    market_close_time = dtime(15, 30, 0)
    current_time = now_ist.time()

    is_market_hours = is_trading_day and (market_open_time <= current_time <= market_close_time)
    ist_time_str = now_ist.strftime("%H:%M:%S IST")

    last_tick_age = None
    if last_tick_timestamp is not None:
        last_tick_ist = last_tick_timestamp.astimezone(IST_TIMEZONE)
        last_tick_age = max(0.0, (now_ist - last_tick_ist).total_seconds())

    # 1. Recovery / Resyncing
    if is_resyncing:
        return MarketSessionInfo(
            state=MarketSessionState.RESYNCING,
            label="Resyncing",
            status_text="Connection drop · Recovering NSE stream...",
            ist_time_str=ist_time_str,
            is_trading_day=is_trading_day,
            is_market_hours=is_market_hours,
            last_tick_age_seconds=last_tick_age,
        )

    # 2. Weekend or Market Holiday -> CLOSED
    if not is_trading_day:
        next_open = get_next_trading_day_open(now_ist)
        weekday_name = next_open.strftime("%a")
        reopen_label = f"Reopens {weekday_name} 09:15 IST"
        return MarketSessionInfo(
            state=MarketSessionState.CLOSED,
            label="Market Closed",
            status_text=f"NSE: Market Closed · {reopen_label}",
            ist_time_str=ist_time_str,
            is_trading_day=False,
            is_market_hours=False,
            next_open_str=next_open.strftime("%Y-%m-%d 09:15:00 IST"),
            last_tick_age_seconds=last_tick_age,
        )

    # 3. Trading day during 09:15 - 15:30 IST
    if is_market_hours:
        if last_tick_age is not None and last_tick_age > 15.0:
            return MarketSessionInfo(
                state=MarketSessionState.STALE,
                label="Feed Stale",
                status_text=f"NSE Telemetry Stale · Last tick {int(last_tick_age)}s ago",
                ist_time_str=ist_time_str,
                is_trading_day=True,
                is_market_hours=True,
                last_tick_age_seconds=last_tick_age,
            )
        return MarketSessionInfo(
            state=MarketSessionState.LIVE,
            label="NSE Live",
            status_text="Live NSE Feed · Active Market Session",
            ist_time_str=ist_time_str,
            is_trading_day=True,
            is_market_hours=True,
            last_tick_age_seconds=last_tick_age,
        )

    # 4. Off-market hours on trading day (e.g. after 15:30 or pre-market before 09:15) -> SNAPSHOT
    if current_time > market_close_time:
        next_open = get_next_trading_day_open(now_ist)
        weekday_name = next_open.strftime("%a")
        return MarketSessionInfo(
            state=MarketSessionState.SNAPSHOT,
            label="EOD Snapshot",
            status_text=f"Authoritative EOD 15:30 IST · Reopens {weekday_name} 09:15 IST",
            ist_time_str=ist_time_str,
            is_trading_day=True,
            is_market_hours=False,
            next_open_str=next_open.strftime("%Y-%m-%d 09:15:00 IST"),
            last_tick_age_seconds=last_tick_age,
        )
    else:
        # Pre-market before 09:15
        return MarketSessionInfo(
            state=MarketSessionState.SNAPSHOT,
            label="Pre-Market",
            status_text="Authoritative EOD Snapshot · Market Opens Today 09:15 IST",
            ist_time_str=ist_time_str,
            is_trading_day=True,
            is_market_hours=False,
            next_open_str=now_ist.replace(hour=9, minute=15, second=0).strftime("%Y-%m-%d 09:15:00 IST"),
            last_tick_age_seconds=last_tick_age,
        )

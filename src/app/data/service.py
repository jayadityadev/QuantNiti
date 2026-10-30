"""Market Data Service layer coordinating Providers, Cleaner, and Local Cache."""

import logging
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union
import pandas as pd

from app.core.config import settings
from app.core.models import StockQuote, UniverseStock, SyncResult
from app.core.validation import validate_date_range
from app.data.cache import ParquetMarketCache
from app.data.cleaner import align_to_trading_calendar, calculate_returns, validate_ohlcv_dataframe
from app.data.provider import MarketDataProvider, MockDataProvider, YahooFinanceProvider
from app.universe import (
    get_sector_for_symbol,
    get_universe_metadata,
    get_universe_symbols,
    normalize_symbol,
    _SYMBOL_MAP,
)

logger = logging.getLogger(__name__)

# Live quotes are reused for this long so list views (Explore, Top Movers) don't
# make one blocking provider round-trip per symbol on every request.
QUOTE_TTL_SECONDS = 60.0


class MarketDataService:
    """Core public service boundary for NIFTY 50 universe market data."""

    def __init__(
        self,
        provider: Optional[MarketDataProvider] = None,
        cache: Optional[ParquetMarketCache] = None,
        auto_cache: bool = True,
    ):
        self.provider = provider or YahooFinanceProvider()
        self.cache = cache or ParquetMarketCache()
        self.auto_cache = auto_cache
        self._quote_cache: Dict[str, Tuple[float, StockQuote]] = {}

    def get_universe(
        self,
        include_benchmarks: bool = True,
        include_expanded: bool = True,
    ) -> List[UniverseStock]:
        """Return list of all universe members and benchmark indices as Pydantic models."""
        raw_meta = get_universe_metadata(include_benchmarks=include_benchmarks, include_expanded=include_expanded)
        return [
            UniverseStock(
                symbol=item["symbol"],
                name=item["name"],
                sector=item["sector"],
                is_benchmark=item.get("is_benchmark", False),
                asset_class=item.get("asset_class").value if hasattr(item.get("asset_class"), "value") else str(item.get("asset_class", "EQUITY")),
                esg_composite=item.get("esg_composite"),
                esg_environment=item.get("esg_environment"),
                esg_social=item.get("esg_social"),
                esg_governance=item.get("esg_governance"),
            )
            for item in raw_meta
        ]

    def get_esg_score(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Retrieve curated ESG score for a given symbol."""
        from app.universe import get_esg_score_for_symbol
        return get_esg_score_for_symbol(symbol)

    def get_history(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        force_refresh: bool = False,
    ) -> pd.DataFrame:
        """Get cleaned, validated OHLCV history with returns computed.

        Loads from local cache if valid; otherwise fetches from provider and updates cache.
        """
        validate_date_range(start_date, end_date)
        canonical = normalize_symbol(symbol)
        df: Optional[pd.DataFrame] = None

        if not force_refresh and self.cache.has_valid_cache(canonical):
            df = self.cache.load_history(canonical)

        if df is None or df.empty:
            df = self.provider.fetch_history(canonical, start_date=start_date, end_date=end_date)
            used_synthetic_fallback = False
            # Fallback to mock data if external provider is offline, rate-limited, or symbol delisted
            if (df is None or df.empty) and isinstance(self.provider, YahooFinanceProvider):
                used_synthetic_fallback = True
                logger.warning(
                    "No live market data for %s; serving synthetic fallback (not cached).",
                    canonical,
                )
                df = MockDataProvider().fetch_history(canonical, start_date=start_date, end_date=end_date)

            if df is not None and not df.empty:
                df = calculate_returns(df)
                # Never persist synthetic fallback rows: doing so would poison the
                # cache and keep serving fabricated prices as if they were live.
                if self.auto_cache and not used_synthetic_fallback:
                    self.cache.save_history(canonical, df)

        if df is None or df.empty:
            return pd.DataFrame()

        # Slice by requested dates if provided
        if start_date:
            df = df[df.index >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df.index <= pd.to_datetime(end_date)]

        if "daily_return" not in df.columns:
            df = calculate_returns(df)

        return df

    def get_daily_returns(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.Series:
        """Get daily return series for a given ticker."""
        df = self.get_history(symbol, start_date=start_date, end_date=end_date)
        if df.empty or "daily_return" not in df.columns:
            return pd.Series(dtype=float)
        return df["daily_return"]

    def get_latest_quote(self, symbol: str) -> StockQuote:
        """Retrieve latest real-time/EOD quote for a ticker."""
        canonical = normalize_symbol(symbol)
        cached = self._quote_cache.get(canonical)
        if cached and time.monotonic() - cached[0] < QUOTE_TTL_SECONDS:
            return cached[1]
        try:
            quote_dict = self.provider.fetch_quote(canonical)
        except Exception:
            # Synthetic fallback is never cached so the next request retries the provider.
            return StockQuote(**MockDataProvider().fetch_quote(canonical))
        quote = StockQuote(**quote_dict)
        self._quote_cache[canonical] = (time.monotonic(), quote)
        return quote

    def prefetch_quotes(self, symbols: Iterable[str], max_workers: int = 8) -> None:
        """Warm the quote cache concurrently; provider calls are network-bound."""
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            list(pool.map(self.get_latest_quote, symbols))

    def get_aligned_dataset(
        self,
        symbols: List[str],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        field: str = "close",
    ) -> pd.DataFrame:
        """Return a multi-asset aligned matrix (Date index, Columns = symbols)

        Uses NIFTY 50 index (^NSEI) trading calendar as the alignment anchor,
        forward-filling any individual stock holidays/trading halts to prevent lookahead bias.
        """
        canonical_symbols = [normalize_symbol(s) for s in symbols]

        # Anchor against benchmark index calendar
        benchmark_df = self.get_history("^NSEI", start_date=start_date, end_date=end_date)
        if not benchmark_df.empty:
            calendar_dates = benchmark_df.index
        else:
            # Fallback to first available stock calendar
            first_df = self.get_history(canonical_symbols[0], start_date=start_date, end_date=end_date)
            calendar_dates = first_df.index if not first_df.empty else pd.date_range("2020-01-01", periods=10, freq="B")

        aligned_cols = {}
        for sym in canonical_symbols:
            stock_df = self.get_history(sym, start_date=start_date, end_date=end_date)
            if stock_df.empty:
                continue

            target_field = "adj_close" if field in ("adj_close", "close") and "adj_close" in stock_df.columns else field
            if target_field not in stock_df.columns:
                target_field = "close" if "close" in stock_df.columns else stock_df.columns[0]

            aligned_stock = align_to_trading_calendar(stock_df, calendar_dates)
            aligned_cols[sym] = aligned_stock[target_field]

        aligned_matrix = pd.DataFrame(aligned_cols, index=calendar_dates)
        aligned_matrix.dropna(how="all", inplace=True)
        aligned_matrix.ffill(inplace=True)
        aligned_matrix.bfill(inplace=True)

        return aligned_matrix

    def sync_universe(
        self,
        symbols: Optional[List[str]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> SyncResult:
        """Batch-sync and cache historical market data for universe stocks."""
        target_symbols = symbols or get_universe_symbols(include_benchmarks=True)
        target_symbols = [normalize_symbol(s) for s in target_symbols]

        successful = 0
        failed = []

        for sym in target_symbols:
            try:
                df = self.provider.fetch_history(sym, start_date=start_date, end_date=end_date)
                if not df.empty:
                    df = calculate_returns(df)
                    self.cache.save_history(sym, df)
                    successful += 1
                else:
                    failed.append(sym)
            except Exception:
                failed.append(sym)

        return SyncResult(
            total_symbols=len(target_symbols),
            successful_symbols=successful,
            failed_symbols=failed,
            cache_path=str(self.cache.cache_dir),
            synced_at=datetime.now(timezone.utc).isoformat(),
        )

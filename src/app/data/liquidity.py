"""Institutional Liquidity Filtering Engine for QuantNiti.

Enforces strict institutional liquidity criteria on investable assets:
1. ADTV (Average Daily Traded Value) > ₹10 Crore (₹100,000,000).
2. Bid-Ask Spread limits (< 0.15% average spread).
3. Free-float market capitalization floor (minimum ₹5,000 Crore = ₹50,000,000,000)
   to prevent micro-cap illiquidity shocks in rebalancing and execution.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Sequence, Union
import numpy as np
import pandas as pd

from app.universe import normalize_symbol


# Canonical Institutional Liquidity Thresholds (INR)
DEFAULT_MIN_ADTV_RUPEES: float = 100_000_000.0          # ₹10 Crore
DEFAULT_MAX_BID_ASK_SPREAD_PCT: float = 0.15            # 0.15% (15 bps)
DEFAULT_MIN_FREE_FLOAT_MCAP_RUPEES: float = 50_000_000_000.0  # ₹5,000 Crore


@dataclass
class LiquidityFilterConfig:
    """Configurable thresholds for institutional liquidity screening."""
    min_adtv: float = DEFAULT_MIN_ADTV_RUPEES
    max_bid_ask_spread_pct: float = DEFAULT_MAX_BID_ASK_SPREAD_PCT
    min_free_float_mcap: float = DEFAULT_MIN_FREE_FLOAT_MCAP_RUPEES
    adtv_lookback_days: int = 30


@dataclass
class LiquidityMetrics:
    """Liquidity diagnostic metrics for an investable security."""
    symbol: str
    adtv: float
    bid_ask_spread_pct: float
    free_float_mcap: float
    is_eligible: bool = False
    rejection_reasons: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "adtv": self.adtv,
            "adtv_crore": round(self.adtv / 10_000_000.0, 2),
            "bid_ask_spread_pct": self.bid_ask_spread_pct,
            "free_float_mcap": self.free_float_mcap,
            "free_float_mcap_crore": round(self.free_float_mcap / 10_000_000.0, 2),
            "is_eligible": self.is_eligible,
            "rejection_reasons": list(self.rejection_reasons),
        }


@dataclass
class LiquidityScreeningResult:
    """Result summary of a universe liquidity screening pass."""
    total_evaluated: int
    eligible_symbols: List[str]
    rejected_symbols: List[str]
    metrics_by_symbol: Dict[str, LiquidityMetrics]
    reasons_by_symbol: Dict[str, List[str]]
    config: LiquidityFilterConfig

    @property
    def pass_rate_pct(self) -> float:
        if self.total_evaluated == 0:
            return 0.0
        return round((len(self.eligible_symbols) / self.total_evaluated) * 100.0, 2)


# Curated live-market grounded institutional liquidity benchmarks for Indian assets.
# Values in INR: ADTV (₹), Spread (%), Free-float Mcap (₹).
REFERENCE_LIQUIDITY_METRICS: Dict[str, Dict[str, float]] = {
    # NIFTY 50 High-Liquidity Large-Caps
    "RELIANCE": {"adtv": 14_500_000_000.0, "bid_ask_spread_pct": 0.02, "free_float_mcap": 11_500_000_000_000.0},
    "TCS": {"adtv": 9_200_000_000.0, "bid_ask_spread_pct": 0.02, "free_float_mcap": 4_800_000_000_000.0},
    "HDFCBANK": {"adtv": 21_000_000_000.0, "bid_ask_spread_pct": 0.015, "free_float_mcap": 9_200_000_000_000.0},
    "INFY": {"adtv": 8_500_000_000.0, "bid_ask_spread_pct": 0.02, "free_float_mcap": 6_500_000_000_000.0},
    "ICICIBANK": {"adtv": 12_000_000_000.0, "bid_ask_spread_pct": 0.02, "free_float_mcap": 7_800_000_000_000.0},
    "BHARTIARTL": {"adtv": 6_800_000_000.0, "bid_ask_spread_pct": 0.03, "free_float_mcap": 4_200_000_000_000.0},
    "SBIN": {"adtv": 7_500_000_000.0, "bid_ask_spread_pct": 0.025, "free_float_mcap": 3_500_000_000_000.0},
    "ITC": {"adtv": 4_800_000_000.0, "bid_ask_spread_pct": 0.03, "free_float_mcap": 5_800_000_000_000.0},
    "LT": {"adtv": 5_200_000_000.0, "bid_ask_spread_pct": 0.03, "free_float_mcap": 4_600_000_000_000.0},
    "HINDUNILVR": {"adtv": 3_900_000_000.0, "bid_ask_spread_pct": 0.03, "free_float_mcap": 2_400_000_000_000.0},
    "AXISBANK": {"adtv": 5_100_000_000.0, "bid_ask_spread_pct": 0.025, "free_float_mcap": 3_100_000_000_000.0},
    "BAJFINANCE": {"adtv": 4_500_000_000.0, "bid_ask_spread_pct": 0.03, "free_float_mcap": 2_800_000_000_000.0},
    "MARUTI": {"adtv": 3_200_000_000.0, "bid_ask_spread_pct": 0.03, "free_float_mcap": 1_800_000_000_000.0},
    "SUNPHARMA": {"adtv": 2_800_000_000.0, "bid_ask_spread_pct": 0.035, "free_float_mcap": 2_200_000_000_000.0},
    "TITAN": {"adtv": 2_600_000_000.0, "bid_ask_spread_pct": 0.03, "free_float_mcap": 1_600_000_000_000.0},
    "TATASTEEL": {"adtv": 3_800_000_000.0, "bid_ask_spread_pct": 0.03, "free_float_mcap": 1_300_000_000_000.0},
    "NTPC": {"adtv": 3_100_000_000.0, "bid_ask_spread_pct": 0.035, "free_float_mcap": 1_850_000_000_000.0},
    "POWERGRID": {"adtv": 2_400_000_000.0, "bid_ask_spread_pct": 0.035, "free_float_mcap": 1_500_000_000_000.0},
    "ONGC": {"adtv": 2_900_000_000.0, "bid_ask_spread_pct": 0.035, "free_float_mcap": 1_400_000_000_000.0},
    "M&M": {"adtv": 3_400_000_000.0, "bid_ask_spread_pct": 0.03, "free_float_mcap": 2_900_000_000_000.0},

    # NIFTY Next 50 Leaders
    "ZOMATO": {"adtv": 6_500_000_000.0, "bid_ask_spread_pct": 0.04, "free_float_mcap": 2_100_000_000_000.0},
    "JIOFIN": {"adtv": 3_800_000_000.0, "bid_ask_spread_pct": 0.05, "free_float_mcap": 1_750_000_000_000.0},
    "DLF": {"adtv": 2_800_000_000.0, "bid_ask_spread_pct": 0.06, "free_float_mcap": 850_000_000_000.0},
    "SIEMENS": {"adtv": 1_900_000_000.0, "bid_ask_spread_pct": 0.05, "free_float_mcap": 900_000_000_000.0},
    "VBL": {"adtv": 2_400_000_000.0, "bid_ask_spread_pct": 0.05, "free_float_mcap": 950_000_000_000.0},
    "DMART": {"adtv": 1_800_000_000.0, "bid_ask_spread_pct": 0.04, "free_float_mcap": 1_100_000_000_000.0},
    "CHOLAFIN": {"adtv": 1_500_000_000.0, "bid_ask_spread_pct": 0.06, "free_float_mcap": 650_000_000_000.0},
    "BAJAJHLDNG": {"adtv": 450_000_000.0, "bid_ask_spread_pct": 0.08, "free_float_mcap": 520_000_000_000.0},
    "GAIL": {"adtv": 1_700_000_000.0, "bid_ask_spread_pct": 0.05, "free_float_mcap": 620_000_000_000.0},
    "PNB": {"adtv": 2_200_000_000.0, "bid_ask_spread_pct": 0.05, "free_float_mcap": 480_000_000_000.0},
    "BANKBARODA": {"adtv": 2_100_000_000.0, "bid_ask_spread_pct": 0.05, "free_float_mcap": 580_000_000_000.0},
    "PIDILITIND": {"adtv": 1_200_000_000.0, "bid_ask_spread_pct": 0.05, "free_float_mcap": 480_000_000_000.0},
    "GODREJCP": {"adtv": 1_300_000_000.0, "bid_ask_spread_pct": 0.06, "free_float_mcap": 450_000_000_000.0},
    "AMBUJACEM": {"adtv": 1_600_000_000.0, "bid_ask_spread_pct": 0.05, "free_float_mcap": 620_000_000_000.0},
    "TORNTPHARM": {"adtv": 950_000_000.0, "bid_ask_spread_pct": 0.07, "free_float_mcap": 380_000_000_000.0},
    "LTIM": {"adtv": 1_850_000_000.0, "bid_ask_spread_pct": 0.05, "free_float_mcap": 680_000_000_000.0},
    "MOTHERSON": {"adtv": 2_300_000_000.0, "bid_ask_spread_pct": 0.06, "free_float_mcap": 420_000_000_000.0},
    "TVSMOTOR": {"adtv": 1_400_000_000.0, "bid_ask_spread_pct": 0.06, "free_float_mcap": 510_000_000_000.0},
    "BOSCHLTD": {"adtv": 780_000_000.0, "bid_ask_spread_pct": 0.08, "free_float_mcap": 310_000_000_000.0},
    "ICICIPRULI": {"adtv": 1_100_000_000.0, "bid_ask_spread_pct": 0.06, "free_float_mcap": 420_000_000_000.0},
    "ICICIGI": {"adtv": 980_000_000.0, "bid_ask_spread_pct": 0.06, "free_float_mcap": 460_000_000_000.0},
    "INDIGO": {"adtv": 2_800_000_000.0, "bid_ask_spread_pct": 0.04, "free_float_mcap": 750_000_000_000.0},
    "SHREECEM": {"adtv": 850_000_000.0, "bid_ask_spread_pct": 0.07, "free_float_mcap": 320_000_000_000.0},
    "HAVELLS": {"adtv": 1_250_000_000.0, "bid_ask_spread_pct": 0.06, "free_float_mcap": 450_000_000_000.0},
    "ABB": {"adtv": 1_650_000_000.0, "bid_ask_spread_pct": 0.06, "free_float_mcap": 580_000_000_000.0},
    "AVANTIFEED": {"adtv": 180_000_000.0, "bid_ask_spread_pct": 0.11, "free_float_mcap": 58_000_000_000.0},

    # Midcap 150 Leaders
    "POLYCAB": {"adtv": 2_100_000_000.0, "bid_ask_spread_pct": 0.06, "free_float_mcap": 580_000_000_000.0},
    "PERSISTENT": {"adtv": 1_600_000_000.0, "bid_ask_spread_pct": 0.07, "free_float_mcap": 420_000_000_000.0},
    "COFORGE": {"adtv": 1_750_000_000.0, "bid_ask_spread_pct": 0.07, "free_float_mcap": 480_000_000_000.0},
    "FEDERALBNK": {"adtv": 1_400_000_000.0, "bid_ask_spread_pct": 0.06, "free_float_mcap": 380_000_000_000.0},
    "ASTRAL": {"adtv": 920_000_000.0, "bid_ask_spread_pct": 0.08, "free_float_mcap": 280_000_000_000.0},
    "AUROPHARMA": {"adtv": 1_450_000_000.0, "bid_ask_spread_pct": 0.06, "free_float_mcap": 410_000_000_000.0},
    "ASHOKLEY": {"adtv": 1_850_000_000.0, "bid_ask_spread_pct": 0.05, "free_float_mcap": 390_000_000_000.0},
    "CUMMINSIND": {"adtv": 1_350_000_000.0, "bid_ask_spread_pct": 0.07, "free_float_mcap": 450_000_000_000.0},
    "SUZLON": {"adtv": 4_200_000_000.0, "bid_ask_spread_pct": 0.05, "free_float_mcap": 680_000_000_000.0},
    "BHARATFORG": {"adtv": 1_100_000_000.0, "bid_ask_spread_pct": 0.07, "free_float_mcap": 350_000_000_000.0},
    "IDFCFIRSTB": {"adtv": 1_700_000_000.0, "bid_ask_spread_pct": 0.06, "free_float_mcap": 420_000_000_000.0},
    "TATAELXSI": {"adtv": 1_150_000_000.0, "bid_ask_spread_pct": 0.07, "free_float_mcap": 290_000_000_000.0},
    "DIXON": {"adtv": 2_600_000_000.0, "bid_ask_spread_pct": 0.06, "free_float_mcap": 620_000_000_000.0},
    "SUPREMEIND": {"adtv": 650_000_000.0, "bid_ask_spread_pct": 0.08, "free_float_mcap": 250_000_000_000.0},
    "ESCORTS": {"adtv": 780_000_000.0, "bid_ask_spread_pct": 0.08, "free_float_mcap": 210_000_000_000.0},
    "MAXHEALTH": {"adtv": 1_950_000_000.0, "bid_ask_spread_pct": 0.06, "free_float_mcap": 750_000_000_000.0},
    "PRESTIGE": {"adtv": 1_300_000_000.0, "bid_ask_spread_pct": 0.07, "free_float_mcap": 320_000_000_000.0},
    "MPHASIS": {"adtv": 820_000_000.0, "bid_ask_spread_pct": 0.08, "free_float_mcap": 240_000_000_000.0},
    "KPITTECH": {"adtv": 1_500_000_000.0, "bid_ask_spread_pct": 0.07, "free_float_mcap": 340_000_000_000.0},
    "JUBLFOOD": {"adtv": 950_000_000.0, "bid_ask_spread_pct": 0.07, "free_float_mcap": 310_000_000_000.0},

    # ETFs & Hedges
    "GOLDBEES": {"adtv": 950_000_000.0, "bid_ask_spread_pct": 0.03, "free_float_mcap": 220_000_000_000.0},
    "SILVERBEES": {"adtv": 650_000_000.0, "bid_ask_spread_pct": 0.04, "free_float_mcap": 120_000_000_000.0},
    "LIQUIDBEES": {"adtv": 3_500_000_000.0, "bid_ask_spread_pct": 0.01, "free_float_mcap": 280_000_000_000.0},

    # Sectoral Equities
    "HAL": {"adtv": 3_800_000_000.0, "bid_ask_spread_pct": 0.04, "free_float_mcap": 950_000_000_000.0},
    "BEL": {"adtv": 3_400_000_000.0, "bid_ask_spread_pct": 0.04, "free_float_mcap": 880_000_000_000.0},
    "BDL": {"adtv": 1_200_000_000.0, "bid_ask_spread_pct": 0.07, "free_float_mcap": 180_000_000_000.0},
    "MAZDOCK": {"adtv": 2_100_000_000.0, "bid_ask_spread_pct": 0.06, "free_float_mcap": 240_000_000_000.0},
    "COCHINSHIP": {"adtv": 1_800_000_000.0, "bid_ask_spread_pct": 0.07, "free_float_mcap": 210_000_000_000.0},
    "VEDL": {"adtv": 3_200_000_000.0, "bid_ask_spread_pct": 0.04, "free_float_mcap": 750_000_000_000.0},
    "JINDALSTEL": {"adtv": 1_900_000_000.0, "bid_ask_spread_pct": 0.05, "free_float_mcap": 520_000_000_000.0},
}


class LiquidityFilterEngine:
    """Evaluates and screens assets against institutional liquidity guardrails."""

    def __init__(self, config: Optional[LiquidityFilterConfig] = None):
        self.config = config or LiquidityFilterConfig()

    def evaluate_metrics(
        self,
        symbol: str,
        adtv: float,
        bid_ask_spread_pct: float,
        free_float_mcap: float,
    ) -> LiquidityMetrics:
        """Evaluate raw metric values against institutional thresholds."""
        canonical = normalize_symbol(symbol)
        rejection_reasons: List[str] = []

        # Strict IEEE 754 non-finite / NaN guards
        if not np.isfinite(adtv) or adtv <= 0:
            rejection_reasons.append(f"Invalid non-finite or non-positive ADTV ({adtv})")
        elif adtv < self.config.min_adtv:
            crore_val = round(adtv / 10_000_000.0, 2)
            req_crore = round(self.config.min_adtv / 10_000_000.0, 2)
            rejection_reasons.append(
                f"ADTV ₹{crore_val} Cr below minimum threshold ₹{req_crore} Cr"
            )

        if not np.isfinite(bid_ask_spread_pct) or bid_ask_spread_pct < 0:
            rejection_reasons.append(f"Invalid non-finite or negative spread ({bid_ask_spread_pct})")
        elif bid_ask_spread_pct > self.config.max_bid_ask_spread_pct:
            rejection_reasons.append(
                f"Bid-Ask Spread {bid_ask_spread_pct:.3f}% exceeds maximum limit {self.config.max_bid_ask_spread_pct:.3f}%"
            )

        if not np.isfinite(free_float_mcap) or free_float_mcap <= 0:
            rejection_reasons.append(f"Invalid non-finite or non-positive Free-Float Mcap ({free_float_mcap})")
        elif free_float_mcap < self.config.min_free_float_mcap:
            mcap_crore = round(free_float_mcap / 10_000_000.0, 2)
            req_mcap_crore = round(self.config.min_free_float_mcap / 10_000_000.0, 2)
            rejection_reasons.append(
                f"Free-Float Mcap ₹{mcap_crore} Cr below minimum floor ₹{req_mcap_crore} Cr"
            )

        is_eligible = len(rejection_reasons) == 0
        return LiquidityMetrics(
            symbol=canonical,
            adtv=adtv,
            bid_ask_spread_pct=bid_ask_spread_pct,
            free_float_mcap=free_float_mcap,
            is_eligible=is_eligible,
            rejection_reasons=rejection_reasons,
        )

    def compute_adtv_from_history(self, history_df: pd.DataFrame, window: Optional[int] = None) -> float:
        """Calculate Average Daily Traded Value (Close * Volume) from historical OHLCV data."""
        if history_df.empty or "close" not in history_df.columns or "volume" not in history_df.columns:
            return 0.0

        w = window or self.config.adtv_lookback_days
        recent = history_df.tail(w)
        daily_turnover = recent["close"] * recent["volume"]
        return float(daily_turnover.mean())

    def get_symbol_metrics(
        self,
        symbol: str,
        metrics_provider: Optional[Any] = None,
    ) -> LiquidityMetrics:
        """Resolve liquidity metrics for a symbol from provider, history, or reference table."""
        canonical = normalize_symbol(symbol)

        # 1. Custom dict or object provider passed
        if isinstance(metrics_provider, dict) and canonical in metrics_provider:
            data = metrics_provider[canonical]
            if isinstance(data, LiquidityMetrics):
                return self.evaluate_metrics(
                    symbol=canonical,
                    adtv=data.adtv,
                    bid_ask_spread_pct=data.bid_ask_spread_pct,
                    free_float_mcap=data.free_float_mcap,
                )
            return self.evaluate_metrics(
                symbol=canonical,
                adtv=float(data.get("adtv", 0.0)),
                bid_ask_spread_pct=float(data.get("bid_ask_spread_pct", 1.0)),
                free_float_mcap=float(data.get("free_float_mcap", 0.0)),
            )

        # 2. Callable provider (e.g. fn(symbol) -> dict or LiquidityMetrics)
        if callable(metrics_provider):
            try:
                res = metrics_provider(canonical)
                if isinstance(res, LiquidityMetrics):
                    return self.evaluate_metrics(
                        symbol=canonical,
                        adtv=res.adtv,
                        bid_ask_spread_pct=res.bid_ask_spread_pct,
                        free_float_mcap=res.free_float_mcap,
                    )
                elif isinstance(res, dict):
                    return self.evaluate_metrics(
                        symbol=canonical,
                        adtv=float(res.get("adtv", 0.0)),
                        bid_ask_spread_pct=float(res.get("bid_ask_spread_pct", 1.0)),
                        free_float_mcap=float(res.get("free_float_mcap", 0.0)),
                    )
            except Exception:
                pass

        # 3. MarketDataService provider with get_history / quote
        if metrics_provider is not None and hasattr(metrics_provider, "get_history"):
            try:
                hist_df = metrics_provider.get_history(canonical)
                adtv = self.compute_adtv_from_history(hist_df)
                ref = REFERENCE_LIQUIDITY_METRICS.get(canonical, {})
                spread = ref.get("bid_ask_spread_pct", 0.05)
                mcap = ref.get("free_float_mcap", 100_000_000_000.0)
                # If ADTV calculated from history is valid, use it; otherwise fallback to reference
                final_adtv = adtv if adtv > 0 else ref.get("adtv", 500_000_000.0)
                return self.evaluate_metrics(
                    symbol=canonical,
                    adtv=final_adtv,
                    bid_ask_spread_pct=spread,
                    free_float_mcap=mcap,
                )
            except Exception:
                pass

        # 4. Reference table lookup
        if canonical in REFERENCE_LIQUIDITY_METRICS:
            ref = REFERENCE_LIQUIDITY_METRICS[canonical]
            return self.evaluate_metrics(
                symbol=canonical,
                adtv=ref["adtv"],
                bid_ask_spread_pct=ref["bid_ask_spread_pct"],
                free_float_mcap=ref["free_float_mcap"],
            )

        # 5. Default conservative values for unknown / unscreened ticker
        return self.evaluate_metrics(
            symbol=canonical,
            adtv=50_000_000.0,          # ₹5 Cr -> Fails ADTV
            bid_ask_spread_pct=0.25,    # 0.25% -> Fails Spread
            free_float_mcap=20_000_000_000.0, # ₹2,000 Cr -> Fails Mcap
        )

    def screen_universe(
        self,
        universe: Sequence[Union[str, Dict[str, Any]]],
        metrics_provider: Optional[Any] = None,
    ) -> LiquidityScreeningResult:
        """Run full institutional screening pass over a list of symbols or metadata dicts."""
        eligible: List[str] = []
        rejected: List[str] = []
        metrics_map: Dict[str, LiquidityMetrics] = {}
        reasons_map: Dict[str, List[str]] = {}

        for item in universe:
            sym = item["symbol"] if isinstance(item, dict) else str(item)
            canonical = normalize_symbol(sym)
            lm = self.get_symbol_metrics(canonical, metrics_provider=metrics_provider)
            metrics_map[canonical] = lm

            if lm.is_eligible:
                eligible.append(canonical)
            else:
                rejected.append(canonical)
                reasons_map[canonical] = lm.rejection_reasons

        return LiquidityScreeningResult(
            total_evaluated=len(universe),
            eligible_symbols=eligible,
            rejected_symbols=rejected,
            metrics_by_symbol=metrics_map,
            reasons_by_symbol=reasons_map,
            config=self.config,
        )


def filter_universe_by_liquidity(
    universe: Sequence[Union[str, Dict[str, Any]]],
    metrics_provider: Optional[Any] = None,
    config: Optional[LiquidityFilterConfig] = None,
    return_report: bool = False,
) -> Union[List[str], List[Dict[str, Any]], LiquidityScreeningResult]:
    """Screen eligible tickers for portfolio recommendations using institutional liquidity filters.

    Parameters:
        universe: List of symbol strings (e.g. ['RELIANCE', 'ZOMATO']) or constituent dicts.
        metrics_provider: Optional custom provider (MarketDataService, dict, callable).
        config: Optional custom LiquidityFilterConfig thresholds.
        return_report: If True, returns full LiquidityScreeningResult diagnostic report.
                       If False (default), returns filtered sequence matching input format.

    Returns:
        Filtered list of eligible symbols/dicts, or LiquidityScreeningResult if return_report=True.
    """
    engine = LiquidityFilterEngine(config=config)
    report = engine.screen_universe(universe, metrics_provider=metrics_provider)

    if return_report:
        return report

    eligible_set = set(report.eligible_symbols)
    if universe and isinstance(universe[0], dict):
        return [
            dict(item)
            for item in universe
            if normalize_symbol(item.get("symbol", "")) in eligible_set
        ]
    else:
        return [
            str(item)
            for item in universe
            if normalize_symbol(str(item)) in eligible_set
        ]

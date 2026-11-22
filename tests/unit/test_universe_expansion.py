"""Unit tests for Universe Expansion & Institutional Liquidity Filters (Phase 2).

Verifies:
1. Asset taxonomy expansion (AssetClass.FIXED_INCOME, EQUITY, COMMODITY_ETF, SECTORAL).
2. NIFTY Next 50 leaders incorporation (ZOMATO, JIOFIN, DLF, SIEMENS, VBL, DMART, AVANTIFEED, etc.).
3. High-liquidity Midcap 150 leaders incorporation (POLYCAB, PERSISTENT, COFORGE, FEDERALBNK, etc.).
4. Fixed income & commodity hedges (LIQUIDBEES, GOLDBEES, SILVERBEES).
5. Ground-truth NSE/.NS ticker denormalization and Indian macro baseline grounding (NIFTY ~25,800, VIX ~16.8, Repo rate 5.50%).
6. Institutional liquidity filter engine enforcing ADTV > ₹10 Cr, Spread < 0.15%, and Free-float Mcap >= ₹5,000 Cr.
"""

import pandas as pd
import pytest

from app.core.config import settings
from app.core.models import AssetClass
from app.data.liquidity import (
    DEFAULT_MAX_BID_ASK_SPREAD_PCT,
    DEFAULT_MIN_ADTV_RUPEES,
    DEFAULT_MIN_FREE_FLOAT_MCAP_RUPEES,
    LiquidityFilterConfig,
    LiquidityFilterEngine,
    LiquidityMetrics,
    LiquidityScreeningResult,
    filter_universe_by_liquidity,
)
from app.data.service import MarketDataService
from app.universe import (
    COMMODITY_ETF_CONSTITUENTS,
    DEFAULT_NIFTY50_BASELINE,
    DEFAULT_RBI_REPO_RATE,
    DEFAULT_VIX_BASELINE,
    DEFENSE_CONSTITUENTS,
    FIXED_INCOME_CONSTITUENTS,
    FULL_INVESTMENT_UNIVERSE,
    INVESTMENT_UNIVERSE,
    METALS_CONSTITUENTS,
    MIDCAP150_CONSTITUENTS,
    NIFTY50_CONSTITUENTS,
    NIFTY_NEXT50_CONSTITUENTS,
    denormalize_symbol,
    get_asset_class_for_symbol,
    get_full_universe_metadata,
    get_full_universe_symbols,
    get_sector_for_symbol,
    get_universe_metadata,
    get_universe_symbols,
    is_valid_symbol,
    normalize_symbol,
)


# ==========================================
# 1. Asset Taxonomy & Universe Constituents
# ==========================================

def test_asset_class_expanded_members():
    """Taxonomy must include FIXED_INCOME alongside EQUITY, COMMODITY_ETF, and SECTORAL."""
    assert AssetClass.EQUITY == "EQUITY"
    assert AssetClass.COMMODITY_ETF == "COMMODITY_ETF"
    assert AssetClass.SECTORAL == "SECTORAL"
    assert AssetClass.FIXED_INCOME == "FIXED_INCOME"


def test_nifty_next50_constituents():
    """NIFTY Next 50 leaders must be registered with EQUITY taxonomy."""
    next50_symbols = {item["symbol"] for item in NIFTY_NEXT50_CONSTITUENTS}
    expected_leaders = {
        "ZOMATO", "JIOFIN", "DLF", "SIEMENS", "VBL", "DMART", "AVANTIFEED",
        "CHOLAFIN", "BAJAJHLDNG", "GAIL", "PNB", "BANKBARODA", "PIDILITIND",
        "GODREJCP", "AMBUJACEM", "TORNTPHARM", "LTIM", "MOTHERSON", "TVSMOTOR",
        "BOSCHLTD", "ICICIPRULI", "ICICIGI", "INDIGO", "SHREECEM", "HAVELLS", "ABB",
    }
    assert expected_leaders.issubset(next50_symbols)
    assert len(NIFTY_NEXT50_CONSTITUENTS) >= 25

    for item in NIFTY_NEXT50_CONSTITUENTS:
        assert item["asset_class"] == AssetClass.EQUITY
        assert len(item["symbol"]) > 0
        assert len(item["name"]) > 0
        assert len(item["sector"]) > 0


def test_midcap150_constituents():
    """High-liquidity Midcap 150 leaders must be registered with EQUITY taxonomy."""
    midcap_symbols = {item["symbol"] for item in MIDCAP150_CONSTITUENTS}
    expected_midcaps = {
        "POLYCAB", "PERSISTENT", "COFORGE", "FEDERALBNK", "ASTRAL",
        "AUROPHARMA", "ASHOKLEY", "CUMMINSIND", "SUZLON", "BHARATFORG",
        "IDFCFIRSTB", "TATAELXSI", "DIXON", "SUPREMEIND", "ESCORTS",
        "MAXHEALTH", "PRESTIGE", "MPHASIS", "KPITTECH", "JUBLFOOD",
    }
    assert expected_midcaps.issubset(midcap_symbols)
    assert len(MIDCAP150_CONSTITUENTS) >= 20

    for item in MIDCAP150_CONSTITUENTS:
        assert item["asset_class"] == AssetClass.EQUITY
        assert len(item["symbol"]) > 0
        assert len(item["name"]) > 0
        assert len(item["sector"]) > 0


def test_fixed_income_and_commodity_hedges():
    """LIQUIDBEES must be registered as FIXED_INCOME, GOLDBEES and SILVERBEES as COMMODITY_ETF."""
    fi_symbols = {item["symbol"] for item in FIXED_INCOME_CONSTITUENTS}
    assert "LIQUIDBEES" in fi_symbols
    for item in FIXED_INCOME_CONSTITUENTS:
        assert item["asset_class"] == AssetClass.FIXED_INCOME
        assert item["sector"] == "Fixed Income"

    etf_symbols = {item["symbol"] for item in COMMODITY_ETF_CONSTITUENTS}
    assert "GOLDBEES" in etf_symbols
    assert "SILVERBEES" in etf_symbols
    for item in COMMODITY_ETF_CONSTITUENTS:
        assert item["asset_class"] == AssetClass.COMMODITY_ETF
        assert item["sector"] == "Commodities"


def test_full_expanded_universe_count_and_deduplication():
    """Complete expanded universe must contain >= 100 unique investable assets."""
    all_symbols = get_full_universe_symbols(include_benchmarks=False)
    assert len(all_symbols) >= 100
    assert len(set(all_symbols)) == len(all_symbols)  # Zero duplicates

    # Benchmarks inclusion adds ^NSEI and ^INDIAVIX
    with_benchmarks = get_full_universe_symbols(include_benchmarks=True)
    assert len(with_benchmarks) == len(all_symbols) + 2
    assert "^NSEI" in with_benchmarks
    assert "^INDIAVIX" in with_benchmarks

    # Metadata helper parity
    full_meta = get_full_universe_metadata()
    assert len(full_meta) == len(all_symbols)


def test_tier_selection_in_get_universe():
    """get_universe_symbols and get_universe_metadata support tier selection cleanly."""
    # NIFTY 50 unexpanded
    nifty = get_universe_symbols(include_expanded=False)
    assert len(nifty) == 50

    # Core Phase 1 universe (58 assets)
    core = get_universe_symbols(include_expanded=True)
    assert len(core) == 58

    # Full expanded universe via tier='all' or include_phase2=True
    tier_all = get_universe_symbols(tier="all")
    assert len(tier_all) >= 100
    phase2 = get_universe_symbols(include_phase2=True)
    assert len(phase2) >= 100
    assert tier_all == phase2


# ==========================================
# 2. Live Ground-Truth Grounding & Tickers
# ==========================================

def test_nse_yahoo_ticker_mapping():
    """Every equity and ETF in the expanded universe must map to Yahoo Finance .NS suffix."""
    all_symbols = get_full_universe_symbols(include_benchmarks=False)
    for sym in all_symbols:
        assert is_valid_symbol(sym) is True
        assert is_valid_symbol(f"{sym}.NS") is True
        assert normalize_symbol(f"{sym}.ns") == sym
        assert normalize_symbol(f"{sym}.NS") == sym
        denorm = denormalize_symbol(sym, provider="yahoo")
        assert denorm == f"{sym}.NS"

    # Benchmark tickers keep caret and do NOT get .NS suffix
    assert denormalize_symbol("^NSEI", provider="yahoo") == "^NSEI"
    assert denormalize_symbol("^INDIAVIX", provider="yahoo") == "^INDIAVIX"


def test_macro_baseline_grounding():
    """Default Indian macro metrics must be grounded to current levels."""
    assert DEFAULT_NIFTY50_BASELINE == pytest.approx(25800.0, rel=0.01)
    assert 16.5 <= DEFAULT_VIX_BASELINE <= 17.5
    assert DEFAULT_RBI_REPO_RATE == pytest.approx(0.055, rel=1e-3)

    assert settings.default_nifty50_baseline == pytest.approx(25800.0, rel=0.01)
    assert 16.5 <= settings.default_vix_baseline <= 17.5
    assert settings.rbi_repo_rate == pytest.approx(0.055, rel=1e-3)


def test_symbol_metadata_and_asset_class_lookups():
    """Lookup helpers return accurate asset class and sector for new additions."""
    assert get_asset_class_for_symbol("LIQUIDBEES") == AssetClass.FIXED_INCOME
    assert get_sector_for_symbol("LIQUIDBEES") == "Fixed Income"

    assert get_asset_class_for_symbol("ZOMATO") == AssetClass.EQUITY
    assert get_sector_for_symbol("ZOMATO") == "Consumer Services"

    assert get_asset_class_for_symbol("POLYCAB") == AssetClass.EQUITY
    assert get_sector_for_symbol("POLYCAB") == "Capital Goods"

    assert get_asset_class_for_symbol("DLF") == AssetClass.EQUITY
    assert get_sector_for_symbol("DLF") == "Real Estate"


# ==========================================
# 3. Institutional Liquidity Filters
# ==========================================

def test_liquidity_filter_default_thresholds():
    """Institutional thresholds must enforce: ADTV > ₹10 Cr, Spread < 0.15%, Free Float >= ₹5,000 Cr."""
    config = LiquidityFilterConfig()
    assert config.min_adtv == 100_000_000.0          # ₹10 Crore
    assert config.max_bid_ask_spread_pct == 0.15      # 0.15% (15 bps)
    assert config.min_free_float_mcap == 50_000_000_000.0  # ₹5,000 Crore

    assert DEFAULT_MIN_ADTV_RUPEES == 100_000_000.0
    assert DEFAULT_MAX_BID_ASK_SPREAD_PCT == 0.15
    assert DEFAULT_MIN_FREE_FLOAT_MCAP_RUPEES == 50_000_000_000.0


def test_liquidity_filter_engine_evaluations():
    """Filter engine evaluates compliance and provides detailed rejection reasons."""
    engine = LiquidityFilterEngine()

    # Highly liquid large cap (Passes all)
    reliance_metrics = engine.evaluate_metrics(
        symbol="RELIANCE",
        adtv=14_500_000_000.0,
        bid_ask_spread_pct=0.02,
        free_float_mcap=11_500_000_000_000.0,
    )
    assert reliance_metrics.is_eligible is True
    assert len(reliance_metrics.rejection_reasons) == 0

    # High growth Next 50 leader (Passes all)
    zomato_metrics = engine.evaluate_metrics(
        symbol="ZOMATO",
        adtv=6_500_000_000.0,
        bid_ask_spread_pct=0.04,
        free_float_mcap=2_100_000_000_000.0,
    )
    assert zomato_metrics.is_eligible is True
    assert len(zomato_metrics.rejection_reasons) == 0

    # Illiquid stock failing ADTV (< ₹10 Cr)
    low_adtv = engine.evaluate_metrics(
        symbol="LOW_VOL_CO",
        adtv=50_000_000.0,  # ₹5 Cr < ₹10 Cr
        bid_ask_spread_pct=0.05,
        free_float_mcap=80_000_000_000.0,
    )
    assert low_adtv.is_eligible is False
    assert any("ADTV" in r for r in low_adtv.rejection_reasons)

    # Illiquid stock failing Spread (> 0.15%)
    wide_spread = engine.evaluate_metrics(
        symbol="WIDE_SPREAD_CO",
        adtv=250_000_000.0,
        bid_ask_spread_pct=0.25,  # 0.25% > 0.15%
        free_float_mcap=90_000_000_000.0,
    )
    assert wide_spread.is_eligible is False
    assert any("Bid-Ask Spread" in r for r in wide_spread.rejection_reasons)

    # Micro-cap failing Market Cap floor (< ₹5,000 Cr)
    micro_cap = engine.evaluate_metrics(
        symbol="MICRO_CAP_CO",
        adtv=150_000_000.0,
        bid_ask_spread_pct=0.10,
        free_float_mcap=25_000_000_000.0,  # ₹2,500 Cr < ₹5,000 Cr
    )
    assert micro_cap.is_eligible is False
    assert any("Free-Float Mcap" in r for r in micro_cap.rejection_reasons)

    # Triple failure
    illiquid_all = engine.evaluate_metrics(
        symbol="PENNY_STOCK",
        adtv=10_000_000.0,
        bid_ask_spread_pct=0.85,
        free_float_mcap=5_000_000_000.0,
    )
    assert illiquid_all.is_eligible is False
    assert len(illiquid_all.rejection_reasons) == 3


def test_filter_universe_by_liquidity_string_list():
    """filter_universe_by_liquidity screens a list of symbol strings."""
    test_universe = ["RELIANCE", "TCS", "ZOMATO", "LIQUIDBEES", "POLYCAB", "ILLIQUID_TEST"]
    custom_provider = {
        "RELIANCE": {"adtv": 10_000_000_000.0, "bid_ask_spread_pct": 0.02, "free_float_mcap": 10_000_000_000_000.0},
        "TCS": {"adtv": 8_000_000_000.0, "bid_ask_spread_pct": 0.02, "free_float_mcap": 5_000_000_000_000.0},
        "ZOMATO": {"adtv": 6_000_000_000.0, "bid_ask_spread_pct": 0.04, "free_float_mcap": 2_000_000_000_000.0},
        "LIQUIDBEES": {"adtv": 3_500_000_000.0, "bid_ask_spread_pct": 0.01, "free_float_mcap": 280_000_000_000.0},
        "POLYCAB": {"adtv": 2_000_000_000.0, "bid_ask_spread_pct": 0.06, "free_float_mcap": 580_000_000_000.0},
        "ILLIQUID_TEST": {"adtv": 20_000_000.0, "bid_ask_spread_pct": 0.35, "free_float_mcap": 10_000_000_000.0},
    }

    filtered = filter_universe_by_liquidity(test_universe, metrics_provider=custom_provider)
    assert isinstance(filtered, list)
    assert "RELIANCE" in filtered
    assert "ZOMATO" in filtered
    assert "LIQUIDBEES" in filtered
    assert "POLYCAB" in filtered
    assert "ILLIQUID_TEST" not in filtered
    assert len(filtered) == 5


def test_filter_universe_by_liquidity_dict_list():
    """filter_universe_by_liquidity preserves dict format when passed metadata list."""
    meta_list = [
        {"symbol": "RELIANCE", "name": "Reliance Industries Ltd."},
        {"symbol": "ZOMATO", "name": "Zomato Ltd."},
        {"symbol": "MICRO_STOCK", "name": "Micro Stock Ltd."},
    ]
    custom_provider = {
        "RELIANCE": {"adtv": 10_000_000_000.0, "bid_ask_spread_pct": 0.02, "free_float_mcap": 10_000_000_000_000.0},
        "ZOMATO": {"adtv": 6_000_000_000.0, "bid_ask_spread_pct": 0.04, "free_float_mcap": 2_000_000_000_000.0},
        "MICRO_STOCK": {"adtv": 10_000_000.0, "bid_ask_spread_pct": 0.50, "free_float_mcap": 5_000_000_000.0},
    }

    filtered = filter_universe_by_liquidity(meta_list, metrics_provider=custom_provider)
    assert isinstance(filtered, list)
    assert len(filtered) == 2
    symbols = {item["symbol"] for item in filtered}
    assert symbols == {"RELIANCE", "ZOMATO"}


def test_filter_universe_by_liquidity_return_report():
    """return_report=True returns LiquidityScreeningResult with pass rate and diagnostic details."""
    symbols = ["RELIANCE", "INFY", "ZOMATO", "JIOFIN", "BAD_TICKER"]
    custom_provider = {
        "RELIANCE": {"adtv": 10_000_000_000.0, "bid_ask_spread_pct": 0.02, "free_float_mcap": 10_000_000_000_000.0},
        "INFY": {"adtv": 8_000_000_000.0, "bid_ask_spread_pct": 0.02, "free_float_mcap": 6_000_000_000_000.0},
        "ZOMATO": {"adtv": 6_000_000_000.0, "bid_ask_spread_pct": 0.04, "free_float_mcap": 2_000_000_000_000.0},
        "JIOFIN": {"adtv": 3_500_000_000.0, "bid_ask_spread_pct": 0.05, "free_float_mcap": 1_700_000_000_000.0},
        "BAD_TICKER": {"adtv": 15_000_000.0, "bid_ask_spread_pct": 0.30, "free_float_mcap": 12_000_000_000.0},
    }

    report = filter_universe_by_liquidity(
        symbols, metrics_provider=custom_provider, return_report=True
    )
    assert isinstance(report, LiquidityScreeningResult)
    assert report.total_evaluated == 5
    assert len(report.eligible_symbols) == 4
    assert len(report.rejected_symbols) == 1
    assert "BAD_TICKER" in report.rejected_symbols
    assert report.pass_rate_pct == 80.0
    assert "BAD_TICKER" in report.reasons_by_symbol
    assert len(report.reasons_by_symbol["BAD_TICKER"]) >= 2


def test_compute_adtv_from_historical_dataframe():
    """compute_adtv_from_history accurately aggregates rolling dollar turnover."""
    engine = LiquidityFilterEngine()
    dates = pd.bdate_range("2026-01-01", periods=30)
    # Price = ₹2,000, Daily Volume = 100,000 -> Turnover = ₹20 Crore / day
    df = pd.DataFrame(
        {
            "close": [2000.0] * 30,
            "volume": [100_000] * 30,
        },
        index=dates,
    )
    adtv = engine.compute_adtv_from_history(df, window=30)
    assert adtv == pytest.approx(200_000_000.0, rel=1e-3)
    # ₹20 Crore > ₹10 Crore threshold
    assert adtv > DEFAULT_MIN_ADTV_RUPEES


def test_market_data_service_historical_ohlcv_for_new_assets():
    """All newly added assets have accessible OHLCV data through MarketDataService."""
    market_svc = MarketDataService()
    test_symbols = ["ZOMATO", "JIOFIN", "DLF", "POLYCAB", "PERSISTENT", "LIQUIDBEES"]
    for sym in test_symbols:
        df = market_svc.get_history(sym)
        assert not df.empty, f"History for {sym} is empty"
        assert len(df) >= 200, f"History for {sym} has {len(df)} bars, expected >= 200"
        for col in ("open", "high", "low", "close", "volume"):
            assert col in df.columns, f"Missing {col} in {sym}"

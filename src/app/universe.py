"""NIFTY Universe, Sector Mapping, and Multi-Asset Constituent Definitions for QuantNiti.

Provides canonical constituent lists for:
- NIFTY 50 (core benchmark index large-caps)
- NIFTY Next 50 leaders (e.g. ZOMATO, JIOFIN, DLF, SIEMENS, VBL, DMART, AVANTIFEED)
- High-liquidity Midcap 150 leaders (e.g. POLYCAB, PERSISTENT, COFORGE, FEDERALBNK)
- Commodity ETFs (GOLDBEES, SILVERBEES)
- Fixed Income / Cash parking yield ETF (LIQUIDBEES)
- High-conviction Sectoral equities (Indian Defense and Metals leaders)
- Benchmark and regime volatility indices (^NSEI, ^INDIAVIX)
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union

from app.core.models import AssetClass

# Live Ground-Truth Indian Macroeconomic Baselines
DEFAULT_NIFTY50_BASELINE: float = 25800.00
DEFAULT_VIX_BASELINE: float = 16.80
DEFAULT_RBI_REPO_RATE: float = 0.055  # 5.50% current RBI policy repo rate

# Benchmark indices tracked by QuantNiti
BENCHMARK_SYMBOLS: Set[str] = {
    "^NSEI",      # NIFTY 50 Index (Benchmark)
    "^INDIAVIX",  # India Volatility Index (Regime Detection)
}

BENCHMARK_METADATA: List[Dict[str, Any]] = [
    {
        "symbol": "^NSEI",
        "name": "NIFTY 50 Index",
        "sector": "Benchmark Index",
        "is_benchmark": True,
        "baseline_price": DEFAULT_NIFTY50_BASELINE,
    },
    {
        "symbol": "^INDIAVIX",
        "name": "India Volatility Index",
        "sector": "Volatility Index",
        "is_benchmark": True,
        "baseline_price": DEFAULT_VIX_BASELINE,
    },
]

# Canonical NIFTY 50 constituents list (50 large-cap Indian companies)
NIFTY50_CONSTITUENTS: List[Dict[str, Any]] = [
    {"symbol": "ADANIENT", "name": "Adani Enterprises Ltd.", "sector": "Metals & Mining", "asset_class": AssetClass.EQUITY},
    {"symbol": "ADANIPORTS", "name": "Adani Ports and Special Economic Zone Ltd.", "sector": "Services & Logistics", "asset_class": AssetClass.EQUITY},
    {"symbol": "APOLLOHOSP", "name": "Apollo Hospitals Enterprise Ltd.", "sector": "Healthcare", "asset_class": AssetClass.EQUITY},
    {"symbol": "ASIANPAINT", "name": "Asian Paints Ltd.", "sector": "Consumer Goods", "asset_class": AssetClass.EQUITY},
    {"symbol": "AXISBANK", "name": "Axis Bank Ltd.", "sector": "Financial Services", "asset_class": AssetClass.EQUITY},
    {"symbol": "BAJAJ-AUTO", "name": "Bajaj Auto Ltd.", "sector": "Automobile", "asset_class": AssetClass.EQUITY},
    {"symbol": "BAJFINANCE", "name": "Bajaj Finance Ltd.", "sector": "Financial Services", "asset_class": AssetClass.EQUITY},
    {"symbol": "BAJAJFINSV", "name": "Bajaj Finserv Ltd.", "sector": "Financial Services", "asset_class": AssetClass.EQUITY},
    {"symbol": "BEL", "name": "Bharat Electronics Ltd.", "sector": "Capital Goods", "asset_class": AssetClass.EQUITY},
    {"symbol": "BHARTIARTL", "name": "Bharti Airtel Ltd.", "sector": "Telecommunication", "asset_class": AssetClass.EQUITY},
    {"symbol": "BPCL", "name": "Bharat Petroleum Corporation Ltd.", "sector": "Energy & Oil", "asset_class": AssetClass.EQUITY},
    {"symbol": "BRITANNIA", "name": "Britannia Industries Ltd.", "sector": "Consumer Goods", "asset_class": AssetClass.EQUITY},
    {"symbol": "CIPLA", "name": "Cipla Ltd.", "sector": "Healthcare", "asset_class": AssetClass.EQUITY},
    {"symbol": "COALINDIA", "name": "Coal India Ltd.", "sector": "Energy & Mining", "asset_class": AssetClass.EQUITY},
    {"symbol": "DRREDDY", "name": "Dr. Reddy's Laboratories Ltd.", "sector": "Healthcare", "asset_class": AssetClass.EQUITY},
    {"symbol": "EICHERMOT", "name": "Eicher Motors Ltd.", "sector": "Automobile", "asset_class": AssetClass.EQUITY},
    {"symbol": "GRASIM", "name": "Grasim Industries Ltd.", "sector": "Materials & Chemicals", "asset_class": AssetClass.EQUITY},
    {"symbol": "HCLTECH", "name": "HCL Technologies Ltd.", "sector": "Information Technology", "asset_class": AssetClass.EQUITY},
    {"symbol": "HDFCBANK", "name": "HDFC Bank Ltd.", "sector": "Financial Services", "asset_class": AssetClass.EQUITY},
    {"symbol": "HDFCLIFE", "name": "HDFC Life Insurance Company Ltd.", "sector": "Financial Services", "asset_class": AssetClass.EQUITY},
    {"symbol": "HEROMOTOCO", "name": "Hero MotoCorp Ltd.", "sector": "Automobile", "asset_class": AssetClass.EQUITY},
    {"symbol": "HINDALCO", "name": "Hindalco Industries Ltd.", "sector": "Metals & Mining", "asset_class": AssetClass.EQUITY},
    {"symbol": "HINDUNILVR", "name": "Hindustan Unilever Ltd.", "sector": "Consumer Goods", "asset_class": AssetClass.EQUITY},
    {"symbol": "ICICIBANK", "name": "ICICI Bank Ltd.", "sector": "Financial Services", "asset_class": AssetClass.EQUITY},
    {"symbol": "INDUSINDBK", "name": "IndusInd Bank Ltd.", "sector": "Financial Services", "asset_class": AssetClass.EQUITY},
    {"symbol": "INFY", "name": "Infosys Ltd.", "sector": "Information Technology", "asset_class": AssetClass.EQUITY},
    {"symbol": "ITC", "name": "ITC Ltd.", "sector": "Consumer Goods", "asset_class": AssetClass.EQUITY},
    {"symbol": "JSWSTEEL", "name": "JSW Steel Ltd.", "sector": "Metals & Mining", "asset_class": AssetClass.EQUITY},
    {"symbol": "KOTAKBANK", "name": "Kotak Mahindra Bank Ltd.", "sector": "Financial Services", "asset_class": AssetClass.EQUITY},
    {"symbol": "LT", "name": "Larsen & Toubro Ltd.", "sector": "Construction & Engineering", "asset_class": AssetClass.EQUITY},
    {"symbol": "M&M", "name": "Mahindra & Mahindra Ltd.", "sector": "Automobile", "asset_class": AssetClass.EQUITY},
    {"symbol": "MARUTI", "name": "Maruti Suzuki India Ltd.", "sector": "Automobile", "asset_class": AssetClass.EQUITY},
    {"symbol": "NESTLEIND", "name": "Nestle India Ltd.", "sector": "Consumer Goods", "asset_class": AssetClass.EQUITY},
    {"symbol": "NTPC", "name": "NTPC Ltd.", "sector": "Power & Energy", "asset_class": AssetClass.EQUITY},
    {"symbol": "ONGC", "name": "Oil & Natural Gas Corporation Ltd.", "sector": "Energy & Oil", "asset_class": AssetClass.EQUITY},
    {"symbol": "POWERGRID", "name": "Power Grid Corporation of India Ltd.", "sector": "Power & Energy", "asset_class": AssetClass.EQUITY},
    {"symbol": "RELIANCE", "name": "Reliance Industries Ltd.", "sector": "Energy & Oil", "asset_class": AssetClass.EQUITY},
    {"symbol": "SBILIFE", "name": "SBI Life Insurance Company Ltd.", "sector": "Financial Services", "asset_class": AssetClass.EQUITY},
    {"symbol": "SBIN", "name": "State Bank of India", "sector": "Financial Services", "asset_class": AssetClass.EQUITY},
    {"symbol": "SHRIRAMFIN", "name": "Shriram Finance Ltd.", "sector": "Financial Services", "asset_class": AssetClass.EQUITY},
    {"symbol": "SUNPHARMA", "name": "Sun Pharmaceutical Industries Ltd.", "sector": "Healthcare", "asset_class": AssetClass.EQUITY},
    {"symbol": "TATACONSUM", "name": "Tata Consumer Products Ltd.", "sector": "Consumer Goods", "asset_class": AssetClass.EQUITY},
    {"symbol": "TATAMOTORS", "name": "Tata Motors Ltd.", "sector": "Automobile", "asset_class": AssetClass.EQUITY},
    {"symbol": "TATASTEEL", "name": "Tata Steel Ltd.", "sector": "Metals & Mining", "asset_class": AssetClass.EQUITY},
    {"symbol": "TCS", "name": "Tata Consultancy Services Ltd.", "sector": "Information Technology", "asset_class": AssetClass.EQUITY},
    {"symbol": "TECHM", "name": "Tech Mahindra Ltd.", "sector": "Information Technology", "asset_class": AssetClass.EQUITY},
    {"symbol": "TITAN", "name": "Titan Company Ltd.", "sector": "Consumer Goods", "asset_class": AssetClass.EQUITY},
    {"symbol": "TRENT", "name": "Trent Ltd.", "sector": "Consumer Retail", "asset_class": AssetClass.EQUITY},
    {"symbol": "ULTRACEMCO", "name": "UltraTech Cement Ltd.", "sector": "Materials & Construction", "asset_class": AssetClass.EQUITY},
    {"symbol": "WIPRO", "name": "Wipro Ltd.", "sector": "Information Technology", "asset_class": AssetClass.EQUITY},
]

# Commodity ETFs (Gold and Silver)
COMMODITY_ETF_CONSTITUENTS: List[Dict[str, Any]] = [
    {
        "symbol": "GOLDBEES",
        "name": "Nippon India ETF Gold BeES",
        "sector": "Commodities",
        "asset_class": AssetClass.COMMODITY_ETF,
    },
    {
        "symbol": "SILVERBEES",
        "name": "Nippon India ETF Silver BeES",
        "sector": "Commodities",
        "asset_class": AssetClass.COMMODITY_ETF,
    },
]

# Fixed Income & Cash Parking Yield ETF
FIXED_INCOME_CONSTITUENTS: List[Dict[str, Any]] = [
    {
        "symbol": "LIQUIDBEES",
        "name": "Nippon India ETF Liquid BeES",
        "sector": "Fixed Income",
        "asset_class": AssetClass.FIXED_INCOME,
    },
]

# Indian Defense Equities
DEFENSE_CONSTITUENTS: List[Dict[str, Any]] = [
    {
        "symbol": "HAL",
        "name": "Hindustan Aeronautics Ltd.",
        "sector": "Defense",
        "asset_class": AssetClass.SECTORAL,
    },
    {
        "symbol": "BEL",
        "name": "Bharat Electronics Ltd.",
        "sector": "Defense",
        "asset_class": AssetClass.SECTORAL,
    },
    {
        "symbol": "BDL",
        "name": "Bharat Dynamics Ltd.",
        "sector": "Defense",
        "asset_class": AssetClass.SECTORAL,
    },
    {
        "symbol": "MAZDOCK",
        "name": "Mazagon Dock Shipbuilders Ltd.",
        "sector": "Defense",
        "asset_class": AssetClass.SECTORAL,
    },
    {
        "symbol": "COCHINSHIP",
        "name": "Cochin Shipyard Ltd.",
        "sector": "Defense",
        "asset_class": AssetClass.SECTORAL,
    },
]

# Metals Leaders
METALS_CONSTITUENTS: List[Dict[str, Any]] = [
    {
        "symbol": "TATASTEEL",
        "name": "Tata Steel Ltd.",
        "sector": "Metals",
        "asset_class": AssetClass.SECTORAL,
    },
    {
        "symbol": "HINDALCO",
        "name": "Hindalco Industries Ltd.",
        "sector": "Metals",
        "asset_class": AssetClass.SECTORAL,
    },
    {
        "symbol": "JSWSTEEL",
        "name": "JSW Steel Ltd.",
        "sector": "Metals",
        "asset_class": AssetClass.SECTORAL,
    },
    {
        "symbol": "VEDL",
        "name": "Vedanta Ltd.",
        "sector": "Metals",
        "asset_class": AssetClass.SECTORAL,
    },
    {
        "symbol": "JINDALSTEL",
        "name": "Jindal Steel & Power Ltd.",
        "sector": "Metals",
        "asset_class": AssetClass.SECTORAL,
    },
]

# NIFTY Next 50 Leaders (High-Growth Large-Caps)
NIFTY_NEXT50_CONSTITUENTS: List[Dict[str, Any]] = [
    {"symbol": "ZOMATO", "name": "Zomato Ltd.", "sector": "Consumer Services", "asset_class": AssetClass.EQUITY},
    {"symbol": "JIOFIN", "name": "Jio Financial Services Ltd.", "sector": "Financial Services", "asset_class": AssetClass.EQUITY},
    {"symbol": "DLF", "name": "DLF Ltd.", "sector": "Real Estate", "asset_class": AssetClass.EQUITY},
    {"symbol": "SIEMENS", "name": "Siemens Ltd.", "sector": "Capital Goods", "asset_class": AssetClass.EQUITY},
    {"symbol": "VBL", "name": "Varun Beverages Ltd.", "sector": "Consumer Goods", "asset_class": AssetClass.EQUITY},
    {"symbol": "DMART", "name": "Avenue Supermarts Ltd.", "sector": "Consumer Retail", "asset_class": AssetClass.EQUITY},
    {"symbol": "AVANTIFEED", "name": "Avanti Feeds Ltd.", "sector": "Consumer Goods", "asset_class": AssetClass.EQUITY},
    {"symbol": "CHOLAFIN", "name": "Cholamandalam Investment and Finance Company Ltd.", "sector": "Financial Services", "asset_class": AssetClass.EQUITY},
    {"symbol": "BAJAJHLDNG", "name": "Bajaj Holdings & Investment Ltd.", "sector": "Financial Services", "asset_class": AssetClass.EQUITY},
    {"symbol": "GAIL", "name": "GAIL (India) Ltd.", "sector": "Energy & Utilities", "asset_class": AssetClass.EQUITY},
    {"symbol": "PNB", "name": "Punjab National Bank", "sector": "Financial Services", "asset_class": AssetClass.EQUITY},
    {"symbol": "BANKBARODA", "name": "Bank of Baroda", "sector": "Financial Services", "asset_class": AssetClass.EQUITY},
    {"symbol": "PIDILITIND", "name": "Pidilite Industries Ltd.", "sector": "Materials & Chemicals", "asset_class": AssetClass.EQUITY},
    {"symbol": "GODREJCP", "name": "Godrej Consumer Products Ltd.", "sector": "Consumer Goods", "asset_class": AssetClass.EQUITY},
    {"symbol": "AMBUJACEM", "name": "Ambuja Cements Ltd.", "sector": "Materials & Construction", "asset_class": AssetClass.EQUITY},
    {"symbol": "TORNTPHARM", "name": "Torrent Pharmaceuticals Ltd.", "sector": "Healthcare", "asset_class": AssetClass.EQUITY},
    {"symbol": "LTIM", "name": "LTIMindtree Ltd.", "sector": "Information Technology", "asset_class": AssetClass.EQUITY},
    {"symbol": "MOTHERSON", "name": "Samvardhana Motherson International Ltd.", "sector": "Automobile", "asset_class": AssetClass.EQUITY},
    {"symbol": "TVSMOTOR", "name": "TVS Motor Company Ltd.", "sector": "Automobile", "asset_class": AssetClass.EQUITY},
    {"symbol": "BOSCHLTD", "name": "Bosch Ltd.", "sector": "Automobile", "asset_class": AssetClass.EQUITY},
    {"symbol": "ICICIPRULI", "name": "ICICI Prudential Life Insurance Company Ltd.", "sector": "Financial Services", "asset_class": AssetClass.EQUITY},
    {"symbol": "ICICIGI", "name": "ICICI Lombard General Insurance Company Ltd.", "sector": "Financial Services", "asset_class": AssetClass.EQUITY},
    {"symbol": "INDIGO", "name": "InterGlobe Aviation Ltd.", "sector": "Services & Logistics", "asset_class": AssetClass.EQUITY},
    {"symbol": "SHREECEM", "name": "Shree Cement Ltd.", "sector": "Materials & Construction", "asset_class": AssetClass.EQUITY},
    {"symbol": "HAVELLS", "name": "Havells India Ltd.", "sector": "Consumer Goods", "asset_class": AssetClass.EQUITY},
    {"symbol": "ABB", "name": "ABB India Ltd.", "sector": "Capital Goods", "asset_class": AssetClass.EQUITY},
]

# High-Liquidity Midcap 150 Leaders
MIDCAP150_CONSTITUENTS: List[Dict[str, Any]] = [
    {"symbol": "POLYCAB", "name": "Polycab India Ltd.", "sector": "Capital Goods", "asset_class": AssetClass.EQUITY},
    {"symbol": "PERSISTENT", "name": "Persistent Systems Ltd.", "sector": "Information Technology", "asset_class": AssetClass.EQUITY},
    {"symbol": "COFORGE", "name": "Coforge Ltd.", "sector": "Information Technology", "asset_class": AssetClass.EQUITY},
    {"symbol": "FEDERALBNK", "name": "The Federal Bank Ltd.", "sector": "Financial Services", "asset_class": AssetClass.EQUITY},
    {"symbol": "ASTRAL", "name": "Astral Ltd.", "sector": "Building Materials", "asset_class": AssetClass.EQUITY},
    {"symbol": "AUROPHARMA", "name": "Aurobindo Pharma Ltd.", "sector": "Healthcare", "asset_class": AssetClass.EQUITY},
    {"symbol": "ASHOKLEY", "name": "Ashok Leyland Ltd.", "sector": "Automobile", "asset_class": AssetClass.EQUITY},
    {"symbol": "CUMMINSIND", "name": "Cummins India Ltd.", "sector": "Capital Goods", "asset_class": AssetClass.EQUITY},
    {"symbol": "SUZLON", "name": "Suzlon Energy Ltd.", "sector": "Power & Energy", "asset_class": AssetClass.EQUITY},
    {"symbol": "BHARATFORG", "name": "Bharat Forge Ltd.", "sector": "Capital Goods", "asset_class": AssetClass.EQUITY},
    {"symbol": "IDFCFIRSTB", "name": "IDFC First Bank Ltd.", "sector": "Financial Services", "asset_class": AssetClass.EQUITY},
    {"symbol": "TATAELXSI", "name": "Tata Elxsi Ltd.", "sector": "Information Technology", "asset_class": AssetClass.EQUITY},
    {"symbol": "DIXON", "name": "Dixon Technologies (India) Ltd.", "sector": "Consumer Goods", "asset_class": AssetClass.EQUITY},
    {"symbol": "SUPREMEIND", "name": "Supreme Industries Ltd.", "sector": "Materials", "asset_class": AssetClass.EQUITY},
    {"symbol": "ESCORTS", "name": "Escorts Kubota Ltd.", "sector": "Automobile", "asset_class": AssetClass.EQUITY},
    {"symbol": "MAXHEALTH", "name": "Max Healthcare Institute Ltd.", "sector": "Healthcare", "asset_class": AssetClass.EQUITY},
    {"symbol": "PRESTIGE", "name": "Prestige Estates Projects Ltd.", "sector": "Real Estate", "asset_class": AssetClass.EQUITY},
    {"symbol": "MPHASIS", "name": "MphasiS Ltd.", "sector": "Information Technology", "asset_class": AssetClass.EQUITY},
    {"symbol": "KPITTECH", "name": "KPIT Technologies Ltd.", "sector": "Information Technology", "asset_class": AssetClass.EQUITY},
    {"symbol": "JUBLFOOD", "name": "Jubilant Foodworks Ltd.", "sector": "Consumer Retail", "asset_class": AssetClass.EQUITY},
]


# ==========================================
# Universe Construction
# ==========================================

# 1. Canonical Core 58-asset Investment Universe (Phase 1 backward-compatible)
CORE_INVESTMENT_UNIVERSE: List[Dict[str, Any]] = []
_seen_core: Set[str] = set()

# Sectoral and Commodity ETFs take precedence for specific taxonomy in core universe
for item in COMMODITY_ETF_CONSTITUENTS + DEFENSE_CONSTITUENTS + METALS_CONSTITUENTS:
    if item["symbol"] not in _seen_core:
        CORE_INVESTMENT_UNIVERSE.append(dict(item))
        _seen_core.add(item["symbol"])

for item in NIFTY50_CONSTITUENTS:
    if item["symbol"] not in _seen_core:
        c_item = dict(item)
        if "asset_class" not in c_item:
            c_item["asset_class"] = AssetClass.EQUITY
        CORE_INVESTMENT_UNIVERSE.append(c_item)
        _seen_core.add(item["symbol"])

# Standard alias for Phase 1 compatibility
INVESTMENT_UNIVERSE: List[Dict[str, Any]] = CORE_INVESTMENT_UNIVERSE
EXPANDED_CONSTITUENTS = INVESTMENT_UNIVERSE


# 2. Comprehensive Expanded Universe (Phase 2 Universe Expansion)
# Incorporates: Fixed Income, Commodity ETFs, Defense, Metals, NIFTY 50, Next 50, Midcap 150
FULL_INVESTMENT_UNIVERSE: List[Dict[str, Any]] = []
_seen_full: Set[str] = set()

# Fixed Income and Commodity Hedges first
for item in FIXED_INCOME_CONSTITUENTS + COMMODITY_ETF_CONSTITUENTS:
    if item["symbol"] not in _seen_full:
        FULL_INVESTMENT_UNIVERSE.append(dict(item))
        _seen_full.add(item["symbol"])

# Sectoral themes
for item in DEFENSE_CONSTITUENTS + METALS_CONSTITUENTS:
    if item["symbol"] not in _seen_full:
        FULL_INVESTMENT_UNIVERSE.append(dict(item))
        _seen_full.add(item["symbol"])

# Large-Cap Core & Next 50 Leaders
for item in NIFTY50_CONSTITUENTS + NIFTY_NEXT50_CONSTITUENTS:
    if item["symbol"] not in _seen_full:
        c_item = dict(item)
        if "asset_class" not in c_item:
            c_item["asset_class"] = AssetClass.EQUITY
        FULL_INVESTMENT_UNIVERSE.append(c_item)
        _seen_full.add(item["symbol"])

# Midcap 150 High-Liquidity Leaders
for item in MIDCAP150_CONSTITUENTS:
    if item["symbol"] not in _seen_full:
        c_item = dict(item)
        if "asset_class" not in c_item:
            c_item["asset_class"] = AssetClass.EQUITY
        FULL_INVESTMENT_UNIVERSE.append(c_item)
        _seen_full.add(item["symbol"])

EXPANDED_INVESTMENT_UNIVERSE = FULL_INVESTMENT_UNIVERSE


# Load curated ESG scores dataset
_ESG_DATA_PATH = Path(__file__).resolve().parent / "data" / "esg_scores.json"
ESG_DATA: Dict[str, Dict[str, Any]] = {}
if _ESG_DATA_PATH.exists():
    try:
        with open(_ESG_DATA_PATH, "r", encoding="utf-8") as f:
            ESG_DATA = json.load(f)
    except Exception:
        ESG_DATA = {}

# Enrich constituents with ESG scores
for col_list in (NIFTY50_CONSTITUENTS, CORE_INVESTMENT_UNIVERSE, FULL_INVESTMENT_UNIVERSE):
    for item in col_list:
        sym = item["symbol"]
        if sym in ESG_DATA:
            esg = ESG_DATA[sym]
            item["esg_composite"] = esg.get("esg_composite")
            item["esg_environment"] = esg.get("esg_environment")
            item["esg_social"] = esg.get("esg_social")
            item["esg_governance"] = esg.get("esg_governance")

# Master lookup map from symbol to metadata dict (indexes ALL constituents + benchmarks)
_SYMBOL_MAP: Dict[str, Dict[str, Any]] = {
    item["symbol"]: item for item in FULL_INVESTMENT_UNIVERSE
}
# Ensure core overrides or benchmark metadata are mapped
for item in CORE_INVESTMENT_UNIVERSE:
    if item["symbol"] not in _SYMBOL_MAP:
        _SYMBOL_MAP[item["symbol"]] = item
for bm in BENCHMARK_METADATA:
    _SYMBOL_MAP[bm["symbol"]] = bm


def get_esg_badge(score: float) -> str:
    """Return ESG badge with color indicator based on composite score."""
    if score >= 70.0:
        return "🟢 High ESG"
    elif score >= 40.0:
        return "🟡 Moderate ESG"
    else:
        return "🔴 Low ESG"


def get_esg_score_for_symbol(symbol: str) -> Optional[Dict[str, Any]]:
    """Retrieve curated ESG score dictionary for a canonical symbol."""
    canonical = normalize_symbol(symbol)
    if canonical in ESG_DATA:
        esg = dict(ESG_DATA[canonical])
        esg["badge"] = get_esg_badge(esg.get("esg_composite", 50.0))
        return esg
    return None


def normalize_symbol(symbol: str) -> str:
    """Normalize input ticker string to standard uppercase canonical symbol.

    Examples:
        'reliance' -> 'RELIANCE'
        'RELIANCE.NS' -> 'RELIANCE'
        'TCS.BO' -> 'TCS'
        'liquidbees.ns' -> 'LIQUIDBEES'
        '^NSEI' -> '^NSEI'
    """
    cleaned = symbol.strip().upper()
    if cleaned in BENCHMARK_SYMBOLS:
        return cleaned
    if cleaned.endswith(".NS") or cleaned.endswith(".BO"):
        cleaned = cleaned[:-3]
    if cleaned == "M_M":
        cleaned = "M&M"
    return cleaned


def denormalize_symbol(symbol: str, provider: str = "yahoo") -> str:
    """Convert canonical symbol into provider-specific symbol format.

    For Yahoo Finance on Indian markets, equity/ETF stocks require '.NS' suffix,
    while index tickers (starting with '^') remain unchanged.
    """
    canonical = normalize_symbol(symbol)
    if canonical in BENCHMARK_SYMBOLS:
        return canonical
    if provider == "yahoo":
        if canonical in ("M&M", "M_M"):
            return "M&M.NS"
        return f"{canonical}.NS"
    return canonical


def get_asset_class_for_symbol(symbol: str) -> Optional[AssetClass]:
    """Retrieve the asset class taxonomy for a given symbol."""
    canonical = normalize_symbol(symbol)
    meta = _SYMBOL_MAP.get(canonical)
    if not meta:
        return None
    ac = meta.get("asset_class", AssetClass.EQUITY)
    return AssetClass(ac) if isinstance(ac, str) else ac


def get_universe_symbols(
    include_benchmarks: bool = False,
    include_expanded: bool = True,
    asset_classes: Optional[List[Union[AssetClass, str]]] = None,
    tier: Optional[str] = None,
    include_phase2: bool = False,
) -> List[str]:
    """Return list of canonical symbols in the universe.

    Tiers:
        - include_expanded=False or tier='nifty50': returns 50 NIFTY constituents.
        - include_phase2=True or tier in ('all', 'full', 'phase2'): returns full expanded universe (104 assets).
        - default (include_expanded=True): returns canonical core 58-asset universe.
    """
    if include_phase2 or tier in ("all", "full", "phase2", "expanded_full"):
        base = FULL_INVESTMENT_UNIVERSE
    elif not include_expanded or tier == "nifty50":
        base = NIFTY50_CONSTITUENTS
    else:
        base = CORE_INVESTMENT_UNIVERSE

    if asset_classes:
        str_classes = {(ac.value if hasattr(ac, "value") else str(ac)) for ac in asset_classes}
        symbols = [
            item["symbol"]
            for item in base
            if (item.get("asset_class").value if hasattr(item.get("asset_class"), "value") else str(item.get("asset_class", "EQUITY"))) in str_classes
        ]
    else:
        symbols = [item["symbol"] for item in base]

    if include_benchmarks:
        symbols.extend(sorted(list(BENCHMARK_SYMBOLS)))
    return symbols


def get_universe_metadata(
    include_benchmarks: bool = False,
    include_expanded: bool = True,
    asset_classes: Optional[List[Union[AssetClass, str]]] = None,
    tier: Optional[str] = None,
    include_phase2: bool = False,
) -> List[Dict[str, Any]]:
    """Return list of metadata dictionaries for stocks in the universe."""
    if include_phase2 or tier in ("all", "full", "phase2", "expanded_full"):
        base = list(FULL_INVESTMENT_UNIVERSE)
    elif not include_expanded or tier == "nifty50":
        base = list(NIFTY50_CONSTITUENTS)
    else:
        base = list(CORE_INVESTMENT_UNIVERSE)

    if asset_classes:
        str_classes = {(ac.value if hasattr(ac, "value") else str(ac)) for ac in asset_classes}
        result = [
            dict(item)
            for item in base
            if (item.get("asset_class").value if hasattr(item.get("asset_class"), "value") else str(item.get("asset_class", "EQUITY"))) in str_classes
        ]
    else:
        result = [dict(item) for item in base]

    if include_benchmarks:
        result.extend(BENCHMARK_METADATA)
    return result


def get_full_universe_symbols(
    include_benchmarks: bool = False,
    asset_classes: Optional[List[Union[AssetClass, str]]] = None,
) -> List[str]:
    """Convenience helper to retrieve all symbols in the complete expanded universe."""
    return get_universe_symbols(
        include_benchmarks=include_benchmarks,
        include_phase2=True,
        asset_classes=asset_classes,
    )


def get_full_universe_metadata(
    include_benchmarks: bool = False,
    asset_classes: Optional[List[Union[AssetClass, str]]] = None,
) -> List[Dict[str, Any]]:
    """Convenience helper to retrieve metadata for all symbols in the complete expanded universe."""
    return get_universe_metadata(
        include_benchmarks=include_benchmarks,
        include_phase2=True,
        asset_classes=asset_classes,
    )


def get_sector_for_symbol(symbol: str) -> Optional[str]:
    """Retrieve sector name for a given ticker, or None if unknown."""
    canonical = normalize_symbol(symbol)
    meta = _SYMBOL_MAP.get(canonical)
    return meta["sector"] if meta else None


def is_valid_symbol(symbol: str) -> bool:
    """Check whether a symbol belongs to the investment universe or benchmarks."""
    canonical = normalize_symbol(symbol)
    return canonical in _SYMBOL_MAP

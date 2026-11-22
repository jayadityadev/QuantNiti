"""Feature engineering for unsupervised market regime detection."""

import numpy as np
import pandas as pd
from typing import Optional


def calculate_rolling_log_returns(series: pd.Series, window: int = 20) -> pd.Series:
    """Calculate rolling cumulative log return over a specified window."""
    daily_log_returns = np.log(series / series.shift(1))
    return daily_log_returns.rolling(window=window).sum()


def calculate_realized_volatility(
    series: pd.Series, window: int = 20, annualize: bool = True
) -> pd.Series:
    """Calculate rolling realized volatility of daily log returns."""
    daily_log_returns = np.log(series / series.shift(1))
    vol = daily_log_returns.rolling(window=window).std()
    if annualize:
        vol = vol * np.sqrt(252)
    return vol


def calculate_parkinson_volatility(
    high: pd.Series, low: pd.Series, window: int = 20, annualize: bool = True
) -> pd.Series:
    """Calculate Parkinson high-low rolling volatility estimate."""
    log_hl = np.log(high / low)
    factor = 1.0 / (4.0 * np.log(2.0))
    daily_parkinson_var = factor * (log_hl**2)
    rolling_var = daily_parkinson_var.rolling(window=window).mean()
    pvol = np.sqrt(rolling_var)
    if annualize:
        pvol = pvol * np.sqrt(252)
    return pvol


def calculate_garman_klass_volatility(
    open_s: pd.Series,
    high_s: pd.Series,
    low_s: pd.Series,
    close_s: pd.Series,
    window: int = 20,
    annualize: bool = True,
) -> pd.Series:
    """Calculate Garman-Klass volatility estimate utilizing OHLC prices."""
    log_hl = np.log(high_s / low_s)
    log_co = np.log(close_s / open_s)
    term1 = 0.5 * (log_hl**2)
    term2 = (2.0 * np.log(2.0) - 1.0) * (log_co**2)
    daily_gk_var = term1 - term2
    rolling_var = daily_gk_var.rolling(window=window).mean().clip(lower=1e-8)
    gk_vol = np.sqrt(rolling_var)
    if annualize:
        gk_vol = gk_vol * np.sqrt(252)
    return gk_vol


def calculate_hurst_exponent(series: pd.Series, max_lag: int = 50) -> float:
    """Calculate the Hurst Exponent (H) via Rescaled Range (R/S) analysis.
    
    H < 0.45: Mean-Reverting regime
    0.45 <= H <= 0.55: Geometric Brownian Motion (Random Walk)
    H > 0.55: Persistent / Strongly Trending regime
    """
    if series.empty:
        return 0.50

    clean_series = pd.to_numeric(series, errors="coerce").dropna()
    clean_series = clean_series[clean_series > 0]
    if len(clean_series) < 30:
        return 0.50

    log_returns = np.log(clean_series / clean_series.shift(1)).dropna().values
    log_returns = log_returns[np.isfinite(log_returns)]
    n = len(log_returns)
    if n < 30:
        return 0.50

    lags = [lag for lag in [10, 15, 20, 30, 40, max_lag] if lag < n // 2]
    if len(lags) < 3:
        return 0.50

    rs_values = []
    valid_lags = []

    for lag in lags:
        num_chunks = n // lag
        if num_chunks < 2:
            continue
        chunk_rs = []
        for i in range(num_chunks):
            chunk = log_returns[i * lag : (i + 1) * lag]
            m = np.mean(chunk)
            y = np.cumsum(chunk - m)
            r = np.max(y) - np.min(y)
            s = np.std(chunk, ddof=1)
            if s > 1e-7:
                chunk_rs.append(r / s)
        if chunk_rs:
            rs_values.append(np.mean(chunk_rs))
            valid_lags.append(lag)

    if len(valid_lags) < 3 or len(rs_values) < 3:
        return 0.50

    try:
        log_lags = np.log(valid_lags)
        log_rs = np.log(rs_values)
        if not np.all(np.isfinite(log_lags)) or not np.all(np.isfinite(log_rs)):
            return 0.50
        poly = np.polyfit(log_lags, log_rs, 1)
        h = float(poly[0])
        if not np.isfinite(h):
            return 0.50
        return float(np.clip(h, 0.05, 0.95))
    except Exception:
        return 0.50


def extract_regime_features(
    index_df: pd.DataFrame,
    vix_df: Optional[pd.DataFrame] = None,
    window: int = 20,
) -> pd.DataFrame:
    """Extract and align multi-dimensional feature set for market regime clustering.

    Features generated:
    - log_return_20d: 20-day cumulative log return of index
    - log_return_50d: 50-day cumulative log return of index
    - realized_vol_20d: 20-day annualized realized volatility
    - parkinson_vol_20d: 20-day annualized Parkinson volatility
    - garman_klass_vol_20d: 20-day annualized Garman-Klass volatility (if open price available)
    - vix_level: India VIX close level (or realized vol proxy if vix_df missing)
    - vix_change_20d: 20-day absolute change in VIX
    """
    if index_df.empty:
        return pd.DataFrame()

    close = index_df["close"]
    high = index_df["high"]
    low = index_df["low"]
    has_open = "open" in index_df.columns

    features = pd.DataFrame(index=index_df.index)

    features["log_return_20d"] = calculate_rolling_log_returns(close, window=window)
    features["log_return_50d"] = calculate_rolling_log_returns(close, window=50)
    features["realized_vol_20d"] = calculate_realized_volatility(close, window=window, annualize=True)
    features["parkinson_vol_20d"] = calculate_parkinson_volatility(high, low, window=window, annualize=True)

    if has_open:
        features["garman_klass_vol_20d"] = calculate_garman_klass_volatility(
            index_df["open"], high, low, close, window=window, annualize=True
        )

    if vix_df is not None and not vix_df.empty:
        # Align VIX to index dates
        aligned_vix = vix_df["close"].reindex(index_df.index).ffill().bfill()
        features["vix_level"] = aligned_vix
        features["vix_change_20d"] = aligned_vix.diff(periods=window).fillna(0.0)
    else:
        # Fallback proxy if VIX is unavailable
        features["vix_level"] = features["realized_vol_20d"] * 100.0
        features["vix_change_20d"] = features["vix_level"].diff(periods=window).fillna(0.0)

    # Drop warm-up NaN rows
    features.dropna(inplace=True)
    return features

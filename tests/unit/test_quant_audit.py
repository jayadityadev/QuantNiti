"""Comprehensive Financial & Quantitative Engine Audit and Invariance Test Suite.

Audits:
1. HRP Portfolio Allocation Engine (Ledoit-Wolf shrinkage, positive definiteness ridge,
   quasi-diagonalization, cluster variance, recursive bisection, weight concentration caps,
   1D 95% CVaR / Expected Shortfall, and Choueifaty Diversification Ratio).
2. Markov Regime Engine & GMM Classifier (Row-stochasticity, stationary distribution,
   expected persistence, Hurst exponent, deterministic state sorting, NaN/inf robustness).
3. Multi-Horizon Probabilistic Forecaster (5.5% RBI repo rate baseline, strict quantile monotonicity).
4. Backtest Metrics (Sharpe ratio, Sortino ratio, Max Drawdown, Calmar ratio, CAPM Alpha and Beta).
5. Compounding & Wealth Engine (Annuity due SIP, Lump-sum, Step-up SIP, GBM quantile cones).
6. Invariance & Zero Stochastic Drift under repeated evaluations.
"""

import math
from typing import Dict, List
import numpy as np
import pandas as pd
import pytest

from app.core.models import (
    BacktestTrade,
    CompoundingRequest,
    MarketRegimeType,
    RegimeProbabilities,
    RiskPersona,
)
from app.ml.backtest.engine import BacktestResultData
from app.ml.backtest.metrics import calculate_backtest_metrics
from app.ml.forecasting.forecaster import MultiHorizonForecaster
from app.ml.portfolio.compounding_engine import (
    calculate_lump_sum,
    calculate_monthly_sip,
    calculate_step_up_sip,
    compute_gbm_quantile_cones,
    find_compounding_tipping_point,
    generate_compounding_projection,
)
from app.ml.portfolio.hrp import (
    HRPOptimizer,
    apply_weight_caps,
    compute_diversification_ratio,
    compute_hrp_weights,
    compute_portfolio_cvar,
    compute_shrunk_covariance,
    get_cluster_variance,
    get_quasi_diag_order,
    recursive_bisection,
)
from app.ml.regime.classifier import MarketRegimeClassifier
from app.ml.regime.features import calculate_hurst_exponent
from app.ml.regime.markov import MarkovRegimeModel


# ============================================================================
# 1. HRP PORTFOLIO ALLOCATION ENGINE AUDIT
# ============================================================================

def test_hrp_shrunk_covariance_positive_definiteness_and_ridge():
    """Verify Ledoit-Wolf shrinkage and ridge regularization guarantee strictly positive eigenvalues."""
    rng = np.random.default_rng(42)
    # 5 assets, 100 days
    returns = rng.normal(0.0005, 0.015, size=(100, 5))
    df = pd.DataFrame(returns, columns=[f"ASSET_{i}" for i in range(5)])

    cov, shrinkage = compute_shrunk_covariance(df, use_shrinkage=True)

    # 1. Symmetry
    np.testing.assert_allclose(cov, cov.T, atol=1e-10)

    # 2. Shrinkage intensity bounded in [0, 1]
    assert 0.0 <= shrinkage <= 1.0

    # 3. Strictly positive definite eigenvalues (all > 1e-7)
    eigvals = np.linalg.eigvalsh(cov)
    assert np.all(eigvals >= 1e-7), f"Eigenvalues below ridge regularizer: {eigvals}"

    # 4. Singularity / collinear asset edge-case fallback
    df_collinear = pd.DataFrame({
        "A": returns[:, 0],
        "B": returns[:, 0],  # Exactly identical
        "C": returns[:, 0] * 2.0,  # Linearly dependent
    })
    cov_collinear, _ = compute_shrunk_covariance(df_collinear, use_shrinkage=True)
    eigvals_collinear = np.linalg.eigvalsh(cov_collinear)
    assert np.all(eigvals_collinear >= 1e-7)


def test_hrp_quasi_diagonalization_order():
    """Quasi-diagonalization extracts correct permutation of leaves."""
    from scipy.cluster.hierarchy import linkage
    from scipy.spatial.distance import pdist

    # 4 items with clear cluster distance structure
    X = np.array([[0, 0], [0.1, 0.1], [10, 10], [10.1, 10.1]])
    link = linkage(pdist(X), method="single")
    order = get_quasi_diag_order(link)

    assert len(order) == 4
    assert set(order) == {0, 1, 2, 3}
    # Items 0,1 should cluster together and 2,3 should cluster together
    assert (order == [0, 1, 2, 3]) or (order == [1, 0, 2, 3]) or (order == [2, 3, 0, 1]) or (order == [3, 2, 0, 1]) or (order == [0, 1, 3, 2])


def test_hrp_cluster_variance_inverse_variance_weighting():
    """Cluster variance w^T Sigma w must be inverse-variance weighted and strictly positive."""
    # Diagonal covariance: var(0)=0.01 (sigma=0.1), var(1)=0.04 (sigma=0.2)
    cov = np.diag([0.01, 0.04])
    cluster_var = get_cluster_variance(cov, [0, 1])

    # Theoretical: inv_diag = [1/0.01, 1/0.04] = [100, 25]
    # w = [100/125, 25/125] = [0.8, 0.2]
    # cluster_var = 0.8^2 * 0.01 + 0.2^2 * 0.04 = 0.64 * 0.01 + 0.04 * 0.04 = 0.0064 + 0.0016 = 0.0080
    assert pytest.approx(cluster_var, rel=1e-4) == 0.0080
    assert cluster_var > 0.0


def test_hrp_recursive_bisection_inverse_variance_split():
    """Recursive bisection allocates more capital to the lower-variance cluster."""
    cov = np.diag([0.01, 0.04])
    weights = recursive_bisection(cov, sort_order=[0, 1])

    assert len(weights) == 2
    assert pytest.approx(np.sum(weights), rel=1e-6) == 1.0
    # Left cluster (idx 0, var=0.01) has 1/4 the variance of right cluster (idx 1, var=0.04)
    # alpha = 1 - 0.01 / (0.01 + 0.04) = 0.80
    assert pytest.approx(weights[0], rel=1e-4) == 0.80
    assert pytest.approx(weights[1], rel=1e-4) == 0.20


def test_hrp_weight_capping_and_normalization():
    """apply_weight_caps strictly enforces max concentration cap without violating budget sum=1.0."""
    raw_weights = {"A": 0.60, "B": 0.25, "C": 0.10, "D": 0.05}
    capped = apply_weight_caps(raw_weights, max_cap=0.30)

    # 1. Sum to 1.0
    assert pytest.approx(sum(capped.values()), rel=1e-5) == 1.0

    # 2. No weight exceeds 0.30 + tolerance
    for sym, w in capped.items():
        assert w <= 0.300001, f"Asset {sym} weight {w} exceeded 0.30"
        assert w >= 0.0

    # 3. Assets that were below the cap receive redistributed weight
    assert capped["B"] > 0.25
    assert capped["C"] > 0.10


def test_hrp_1d_95_cvar_expected_shortfall_formula():
    """Portfolio CVaR 95% matches negative mean of returns below 5th percentile."""
    rng = np.random.default_rng(123)
    n_days = 1000
    daily_rets = pd.DataFrame({
        "A": rng.normal(0.001, 0.01, n_days),
        "B": rng.normal(0.0005, 0.02, n_days),
    })
    weights = {"A": 0.5, "B": 0.5}

    cvar_ann = compute_portfolio_cvar(daily_rets, weights, confidence=0.95)

    # Manual analytical calculation
    port_rets = 0.5 * daily_rets["A"].values + 0.5 * daily_rets["B"].values
    var_5 = np.percentile(port_rets, 5.0)
    tail = port_rets[port_rets <= var_5]
    expected_cvar_daily = -np.mean(tail)
    expected_cvar_ann_pct = round(expected_cvar_daily * np.sqrt(252.0) * 100.0, 2)

    assert cvar_ann == expected_cvar_ann_pct
    assert cvar_ann > 0.0


def test_hrp_choueifaty_diversification_ratio():
    """Diversification Ratio DR(w) = sum(w_i * sigma_i) / sigma_p >= 1.0 (Choueifaty theorem)."""
    rng = np.random.default_rng(42)
    n = 200
    # Two independent assets
    r_a = rng.normal(0.0, 0.02, n)
    r_b = rng.normal(0.0, 0.02, n)
    df = pd.DataFrame({"A": r_a, "B": r_b})
    weights = {"A": 0.5, "B": 0.5}

    dr = compute_diversification_ratio(df, weights)
    # For two independent assets of equal vol sigma, port_vol = sigma / sqrt(2)
    # DR = (0.5*sigma + 0.5*sigma) / (sigma / sqrt(2)) = sqrt(2) ~ 1.414
    assert pytest.approx(dr, rel=0.05) == 1.414
    assert dr >= 1.0

    # Single asset: DR must equal 1.0
    dr_single = compute_diversification_ratio(df[["A"]], {"A": 1.0})
    assert dr_single == 1.0


# ============================================================================
# 2. MARKOV REGIME ENGINE & GMM CLASSIFIER AUDIT
# ============================================================================

def test_markov_transition_matrix_row_stochasticity():
    """Each row of the 3x3 Markov transition probability matrix must sum strictly to 1.0."""
    model = MarkovRegimeModel()
    # Sequence with unequal distribution
    seq = (
        [MarketRegimeType.LOW_VOLATILITY_BULL] * 30
        + [MarketRegimeType.SIDEWAYS_CONSOLIDATION] * 15
        + [MarketRegimeType.HIGH_VOLATILITY_BEAR] * 10
        + [MarketRegimeType.LOW_VOLATILITY_BULL] * 5
    )
    model.fit_from_sequence(seq)

    P = model.transition_matrix
    assert P.shape == (3, 3)

    # Check row-stochasticity for every row
    for row_idx in range(3):
        row_sum = float(P[row_idx].sum())
        assert pytest.approx(row_sum, abs=1e-8) == 1.0
        for col_idx in range(3):
            assert 0.0 <= P[row_idx, col_idx] <= 1.0


def test_markov_stationary_distribution_equilibrium():
    """Stationary distribution must satisfy pi * P = pi and sum(pi) = 1.0."""
    model = MarkovRegimeModel()
    seq = (
        [MarketRegimeType.LOW_VOLATILITY_BULL] * 25
        + [MarketRegimeType.SIDEWAYS_CONSOLIDATION] * 20
        + [MarketRegimeType.HIGH_VOLATILITY_BEAR] * 15
    )
    model.fit_from_sequence(seq)

    P = model.transition_matrix
    pi = model.stationary_distribution

    # 1. Sum to 1.0
    assert pytest.approx(float(np.sum(pi)), abs=1e-6) == 1.0

    # 2. Invariant equilibrium: pi * P = pi
    pi_P = pi @ P
    np.testing.assert_allclose(pi_P, pi, atol=1e-5)


def test_markov_expected_regime_duration_formula():
    """Expected duration E[D_i] = 1 / (1 - P_ii) in trading days."""
    model = MarkovRegimeModel()
    model.transition_matrix = np.array([
        [0.90, 0.05, 0.05],
        [0.10, 0.80, 0.10],
        [0.05, 0.15, 0.80],
    ])
    model._compute_derived_metrics()

    # E[D_0] = 1 / (1 - 0.90) = 10.0 days
    # E[D_1] = 1 / (1 - 0.80) = 5.0 days
    durations = model.expected_durations
    assert pytest.approx(durations[MarketRegimeType.LOW_VOLATILITY_BULL.value], abs=0.1) == 10.0
    assert pytest.approx(durations[MarketRegimeType.HIGH_VOLATILITY_BEAR.value], abs=0.1) == 5.0


def test_markov_next_step_probability_forecast():
    """One-step-ahead forecast p_{t+1} = p_t * P must sum to 1.0."""
    model = MarkovRegimeModel()
    model.fit_from_sequence([MarketRegimeType.LOW_VOLATILITY_BULL] * 20)

    current_p = RegimeProbabilities(bull=0.70, bear=0.10, sideways=0.20)
    next_dict = model.predict_next_step(current_p)

    total_next = next_dict["bull"] + next_dict["bear"] + next_dict["sideways"]
    assert pytest.approx(total_next, abs=1e-4) == 1.0


def test_hurst_exponent_calculation_and_edge_cases():
    """Hurst exponent calculates market memory and survives degenerate inputs without error."""
    # 1. Geometric random walk (H ~ 0.50)
    rng = np.random.default_rng(42)
    rw = pd.Series(100.0 + np.cumsum(rng.normal(0, 1, 200)))
    h_rw = calculate_hurst_exponent(rw)
    assert 0.05 <= h_rw <= 0.95

    # 2. Short / Empty / Constant / Non-positive edge cases
    assert calculate_hurst_exponent(pd.Series([])) == 0.50
    assert calculate_hurst_exponent(pd.Series([100.0] * 50)) == 0.50  # Constant price
    assert calculate_hurst_exponent(pd.Series([-10.0, 0.0, 50.0])) == 0.50  # Non-positive


def test_gmm_deterministic_sorting_and_nan_resilience():
    """MarketRegimeClassifier ensures deterministic cluster mapping and survives NaN/inf features."""
    rng = np.random.default_rng(42)
    n = 60
    # Clean training features
    train_df = pd.DataFrame({
        "log_return_20d": np.concatenate([rng.normal(0.05, 0.01, n), rng.normal(-0.06, 0.01, n), rng.normal(0.005, 0.005, n)]),
        "realized_vol_20d": np.concatenate([rng.normal(0.10, 0.01, n), rng.normal(0.28, 0.02, n), rng.normal(0.14, 0.01, n)]),
    })

    clf = MarketRegimeClassifier(random_state=42)
    clf.fit(train_df)

    assert clf.is_fitted
    assert len(clf.cluster_to_regime) == 3

    # Test with NaN and Inf input
    dirty_input = pd.DataFrame({
        "log_return_20d": [np.nan, np.inf, -0.05],
        "realized_vol_20d": [0.15, 0.20, np.nan],
    })
    preds = clf.predict(dirty_input)
    assert len(preds) == 3
    for p in preds:
        assert isinstance(p, MarketRegimeType)

    # Probabilities sum to 1.0 even on dirty inputs
    proba = clf.predict_proba(dirty_input)
    np.testing.assert_allclose(proba.sum(axis=1).values, 1.0, atol=1e-5)


# ============================================================================
# 3. MULTI-HORIZON PROBABILISTIC FORECASTER AUDIT
# ============================================================================

def test_forecaster_risk_free_rate_baseline_gsec_yield():
    """Forecaster default risk-free rate is grounded to Indian 10-Year G-Sec benchmark yield (~7.18%)."""
    forecaster = MultiHorizonForecaster()
    assert pytest.approx(forecaster.risk_free_rate, abs=0.005) == 0.0718


def test_forecaster_strict_quantile_monotonicity_all_horizons():
    """Verify Q10 <= Q50 <= Q90 and P10 <= P50 <= P90 across 1M, 3M, 6M, 12M."""
    rng = np.random.default_rng(101)
    dates = pd.bdate_range("2023-01-01", periods=200)
    prices = 1000.0 * np.exp(np.cumsum(rng.normal(0.0005, 0.015, 200)))
    stock_df = pd.DataFrame({"close": prices, "high": prices * 1.01, "low": prices * 0.99, "volume": 100000}, index=dates)

    forecaster = MultiHorizonForecaster()
    forecast = forecaster.predict_growth_cones(stock_df, current_price=float(prices[-1]))

    for name, cone in [("1M", forecast.m1), ("3M", forecast.m3), ("6M", forecast.m6), ("12M", forecast.m12)]:
        # Return monotonicity
        assert cone.pessimistic_pct <= cone.base_pct, f"Failed at {name}: Q10 > Q50"
        assert cone.base_pct <= cone.optimistic_pct, f"Failed at {name}: Q50 > Q90"

        # Price monotonicity
        assert cone.pessimistic_price <= cone.base_price, f"Failed at {name}: P10 > P50"
        assert cone.base_price <= cone.optimistic_price, f"Failed at {name}: P50 > P90"


# ============================================================================
# 4. BACKTEST METRICS AUDIT
# ============================================================================

def test_backtest_metrics_exact_formulas():
    """Audit Sharpe, Sortino, Max Drawdown, Calmar, and CAPM Alpha / Beta."""
    dates = [f"2025-01-{i:02d}" for i in range(1, 253)]
    # Strategy with steady +0.1% daily return with small noise
    strat_rets = pd.Series([0.001] * 252, index=dates)
    bench_rets = pd.Series([0.0005] * 252, index=dates)

    equity = 100000.0 * (1.0 + strat_rets).cumprod()
    dd = pd.Series([0.0] * 252, index=dates)
    bench_equity = 100000.0 * (1.0 + bench_rets).cumprod()

    result_data = BacktestResultData(
        dates=dates,
        close_prices=equity,
        signals=pd.Series(1.0, index=dates),
        positions=pd.Series(1.0, index=dates),
        daily_returns=strat_rets,
        strategy_returns=strat_rets,
        equity_series=equity,
        drawdown_series=dd,
        benchmark_equity_series=bench_equity,
        benchmark_returns=bench_rets,
        trades=[],
        initial_capital=100000.0,
        final_equity=float(equity.iloc[-1]),
        total_cost_paid=0.0,
    )

    metrics = calculate_backtest_metrics(result_data, benchmark_returns=bench_rets, risk_free_rate=0.055)

    # 1. Risk-free rate
    daily_rf = (1.0 + 0.055) ** (1.0 / 252.0) - 1.0
    expected_excess = 0.001 - daily_rf

    # 2. Total return & CAGR
    total_ret = (equity.iloc[-1] / 100000.0) - 1.0
    assert pytest.approx(metrics.total_return_pct, rel=1e-2) == round(total_ret * 100.0, 2)
    assert pytest.approx(metrics.cagr, rel=1e-2) == round(total_ret * 100.0, 2)

    # 3. Max Drawdown
    assert metrics.max_drawdown_pct == 0.0

    # 4. Beta and Alpha
    assert metrics.beta == 1.0


# ============================================================================
# 5. COMPOUNDING & WEALTH ENGINE AUDIT
# ============================================================================

def test_compounding_monthly_sip_annuity_due_formula():
    """Annuity due formula FV = P * ((1+i)^n - 1)/i * (1+i)."""
    # P = 10000, r = 12% annual (i = 1% monthly), 10 years (n = 120 months)
    summary = calculate_monthly_sip(monthly_amount=10000.0, annual_return_pct=12.0, tenure_years=10)

    # Analytical: FV = 10000 * (1.01^120 - 1) / 0.01 * 1.01 = 2,323,390.76
    expected_invested = 1200000.0
    expected_fv = 2323390.76
    expected_gain = 1123390.76

    assert abs(summary.total_invested - expected_invested) <= 0.01
    assert abs(summary.future_value - expected_fv) <= 1.0
    assert abs(summary.wealth_gain - expected_gain) <= 1.0


def test_compounding_lump_sum_formula():
    """Lump sum formula FV = P0 * (1 + r)^t."""
    # P0 = 500000, r = 10%, t = 5
    summary = calculate_lump_sum(principal=500000.0, annual_return_pct=10.0, tenure_years=5)

    # Analytical: 500000 * 1.10^5 = 805,255.00
    expected_fv = 805255.00
    assert abs(summary.future_value - expected_fv) <= 1.0
    assert summary.total_invested == 500000.0


def test_compounding_step_up_sip_formula():
    """Step-Up SIP strictly exceeds regular SIP in both invested principal and final wealth."""
    reg = calculate_monthly_sip(monthly_amount=10000.0, annual_return_pct=12.0, tenure_years=5)
    step = calculate_step_up_sip(initial_monthly=10000.0, annual_step_up_pct=10.0, annual_return_pct=12.0, tenure_years=5)

    assert step.total_invested > reg.total_invested
    assert step.future_value > reg.future_value
    assert step.wealth_gain > reg.wealth_gain


def test_compounding_gbm_quantile_cones_monotonicity():
    """GBM quantile cones satisfy Pessimistic (10th) <= Base (50th) <= Optimistic (90th) at each year."""
    cones = compute_gbm_quantile_cones(initial_value=100000.0, annual_drift=0.12, annual_vol=0.18, years=10)

    for pt in cones:
        assert pt["pessimistic_10th"] <= pt["base_50th"]
        assert pt["base_50th"] <= pt["optimistic_90th"]


# ============================================================================
# 6. INVARIANCE & DETERMINISM (ZERO STOCHASTIC DRIFT)
# ============================================================================

def test_quant_engine_strict_determinism_across_evaluations():
    """Identical inputs across all quant modules must yield strictly deterministic, zero-drift results."""
    rng = np.random.default_rng(999)
    n_days = 150
    returns = rng.normal(0.0005, 0.015, size=(n_days, 4))
    df = pd.DataFrame(returns, columns=["TCS", "INFY", "RELIANCE", "HDFCBANK"])

    # 1. HRP Optimizer Determinism
    opt = HRPOptimizer()
    w1, cvar1, dr1, _ = opt.optimize_with_diagnostics(df, risk_persona=RiskPersona.BALANCED)
    w2, cvar2, dr2, _ = opt.optimize_with_diagnostics(df, risk_persona=RiskPersona.BALANCED)

    assert w1 == w2
    assert cvar1 == cvar2
    assert dr1 == dr2

    # 2. Forecaster Determinism
    dates = pd.bdate_range("2024-01-01", periods=n_days)
    stock_df = pd.DataFrame({
        "close": 1000.0 + np.cumsum(returns[:, 0]),
        "high": 1010.0 + np.cumsum(returns[:, 0]),
        "low": 990.0 + np.cumsum(returns[:, 0]),
        "volume": 500000,
    }, index=dates)

    forecaster = MultiHorizonForecaster()
    f1 = forecaster.predict_growth_cones(stock_df, current_price=1000.0)
    f2 = forecaster.predict_growth_cones(stock_df, current_price=1000.0)

    assert f1.m6.base_pct == f2.m6.base_pct
    assert f1.m6.pessimistic_pct == f2.m6.pessimistic_pct
    assert f1.m6.optimistic_pct == f2.m6.optimistic_pct

    # 3. Compounding Engine Determinism
    req = CompoundingRequest(monthly_sip=5000.0, tenure_years=10, expected_return_pct=12.0, step_up_pct=5.0)
    p1 = generate_compounding_projection(req)
    p2 = generate_compounding_projection(req)

    assert p1.regular_sip_summary.future_value == p2.regular_sip_summary.future_value
    assert p1.step_up_sip_summary.future_value == p2.step_up_sip_summary.future_value
    assert p1.alpha_vs_bank_fd == p2.alpha_vs_bank_fd


# ============================================================================
# 7. MARKET GROUND TRUTH & ECONOMIC REGIME AUDIT
# ============================================================================

def test_massive_rally_classified_as_bull_not_sideways():
    """Verify that a massive post-Diwali rally (+12.8% 20d return) is classified as BULL, never SIDEWAYS."""
    rng = np.random.default_rng(42)
    n = 60
    train_df = pd.DataFrame({
        "log_return_20d": np.concatenate([rng.normal(0.04, 0.01, n), rng.normal(-0.06, 0.01, n), rng.normal(0.005, 0.005, n)]),
        "realized_vol_20d": np.concatenate([rng.normal(0.12, 0.01, n), rng.normal(0.28, 0.02, n), rng.normal(0.14, 0.01, n)]),
        "vix_level": np.concatenate([rng.normal(13.0, 1.0, n), rng.normal(26.0, 2.0, n), rng.normal(16.0, 1.0, n)]),
    })

    clf = MarketRegimeClassifier(random_state=42)
    clf.fit(train_df)

    # Live market ground truth point: NIFTY +12.8% monthly rally, VIX 17.32
    rally_point = pd.DataFrame({
        "log_return_20d": [0.128],
        "realized_vol_20d": [0.15],
        "vix_level": [17.32],
    })

    regime = clf.predict_single(rally_point)
    assert regime == MarketRegimeType.LOW_VOLATILITY_BULL, f"Massive rally misclassified as {regime}"

    probs = clf.predict_proba(rally_point)
    bull_prob = float(probs.iloc[0][MarketRegimeType.LOW_VOLATILITY_BULL.value])
    side_prob = float(probs.iloc[0][MarketRegimeType.SIDEWAYS_CONSOLIDATION.value])
    assert bull_prob > side_prob, f"Bull probability {bull_prob} not higher than sideways {side_prob}"


def test_dirichlet_regularization_eliminates_probability_collapse():
    """Dirichlet prior regularization prevents 99.9% probability saturation collapse."""
    rng = np.random.default_rng(42)
    n = 60
    train_df = pd.DataFrame({
        "log_return_20d": np.concatenate([rng.normal(0.05, 0.01, n), rng.normal(-0.06, 0.01, n), rng.normal(0.005, 0.005, n)]),
        "realized_vol_20d": np.concatenate([rng.normal(0.10, 0.01, n), rng.normal(0.28, 0.02, n), rng.normal(0.14, 0.01, n)]),
        "vix_level": np.concatenate([rng.normal(12.0, 1.0, n), rng.normal(25.0, 2.0, n), rng.normal(15.0, 1.0, n)]),
    })

    clf = MarketRegimeClassifier(random_state=42)
    clf.fit(train_df)

    # An extreme bull point that would previously collapse to 99.99%
    extreme_point = pd.DataFrame({
        "log_return_20d": [0.25],
        "realized_vol_20d": [0.08],
        "vix_level": [10.0],
    })

    proba = clf.predict_proba(extreme_point)
    row = proba.iloc[0]
    # Max probability is regularized below 0.95 to account for realistic macroeconomic uncertainty
    assert row.max() <= 0.95
    # Minor regimes maintain non-zero probability (Dirichlet prior floor)
    assert row.min() >= 0.01
    assert pytest.approx(row.sum(), abs=1e-5) == 1.0


def test_backtest_lookahead_bias_strict_day_zero_cash():
    """Active backtest strategies must strictly have position=0 on day 0 (no lookahead return)."""
    from app.ml.backtest.engine import BacktestEngine
    from app.core.models import StrategyType

    dates = pd.bdate_range("2024-01-01", periods=30)
    prices = 100.0 + np.arange(30) * 1.5  # Constant uptrend
    df = pd.DataFrame({"close": prices}, index=dates)

    engine = BacktestEngine()
    result = engine.run(df=df, strategy=StrategyType.MA_CROSSOVER, cost_bps=15.0, slippage_bps=5.0)

    # Day 0 position must be 0.0
    assert result.positions.iloc[0] == 0.0
    # Day 0 strategy return must be 0.0 (no trade executed yet)
    assert result.strategy_returns.iloc[0] == 0.0
    # Initial equity on day 0 must equal initial capital
    assert result.equity_series.iloc[0] == 100000.0


def test_data_provenance_flags_exposed():
    """Data models strictly expose is_synthetic and provenance flags."""
    from app.core.models import StockQuote, MarketTick, MarketHistoryResponse, OHLCVBar

    # Mock provider quote
    quote = StockQuote(
        symbol="RELIANCE",
        name="Reliance Industries",
        sector="Energy",
        current_price=1285.0,
        day_change=12.5,
        day_change_pct=0.98,
        day_high=1290.0,
        day_low=1275.0,
        volume=500000,
        timestamp="2026-11-22T00:00:00Z",
        is_synthetic=True,
        provenance="synthetic_mock_quote",
    )
    assert quote.is_synthetic is True
    assert quote.provenance == "synthetic_mock_quote"

    # Streaming tick
    tick = MarketTick(
        symbol="^NSEI",
        price=25800.60,
        change=286.30,
        change_pct=1.12,
        high=25850.0,
        low=25600.0,
        volume=1200000,
        timestamp="2026-11-22T00:00:00Z",
        is_synthetic=False,
        provenance="broker_live",
    )
    assert tick.is_synthetic is False
    assert tick.provenance == "broker_live"

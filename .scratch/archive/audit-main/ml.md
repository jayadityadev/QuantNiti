# ADVERSARIAL QUANTITATIVE ML AUDIT REPORT: QUANTNITI

**Auditor:** Senior Quantitative ML Engineer & Adversarial Auditor  
**Date:** November 15, 2026  
**Target Repository:** `QuantNiti` (`D:\Codebase\QuantNiti`)  
**Scope:** `src/app/ml/**`, `src/app/data/**`, `src/app/core/config.py`, and test suites.  
**Mode:** READ-ONLY Verification & Dynamic Execution

---

## 1. EXECUTIVE SUMMARY & VERDICT

### Overall Verdict: `heuristic-disguised-as-ML`

While QuantNiti presents itself as an *"AI-driven regime-adaptive portfolio intelligence platform"* powered by *"multi-factor quantile growth forecasting (LightGBM Q10/Q50/Q90)"* and *"unsupervised Gaussian Mixture Model regime classification"*, an adversarial audit reveals that **the centerpiece machine learning claim is fictitious**:

1. **LightGBM Quantile Regression is Completely Missing**: Despite `lightgbm>=4.7.0` appearing in `pyproject.toml` and being touted in architecture documentation, **there is zero LightGBM code in the codebase**. The forecaster (`src/app/ml/forecasting/forecaster.py`) is a deterministic heuristic formula combining CAPM, momentum, and EMA spreads. Even worse, it contains a critical mathematical bug: it scales volatility linearly with horizon time ($\tau$) instead of diffusion scaling ($\sqrt{\tau}$), underestimating 1-month confidence intervals by a factor of **3.46x**.
2. **GMM Regime Inversion Bug**: The Gaussian Mixture Model in `src/app/ml/regime/classifier.py` clusters 6 rolling features, but maps clusters to semantic regimes using `score = return / volatility`. For negative return regimes, dividing by high volatility makes the score *less negative*, causing a severe market crash to be classified as *"Sideways Consolidation"* while a mild market dip is classified as *"High-Volatility Bear"*. In addition, GMM fits on the entire 5-year history in-sample with zero train/test separation, introducing severe look-ahead leakage.
3. **Ledoit-Wolf & HRP are Mathematically Sound**: The portfolio optimization module (`src/app/ml/portfolio/hrp.py`) correctly implements Lopez de Prado's Hierarchical Risk Parity with scikit-learn Ledoit-Wolf shrinkage, verified numerically with `max diff = 0.0` against a standard reference.
4. **Backtest Engine Flaws**: The backtest engine assumes instant execution at yesterday's close after calculating signals at close (overnight gap leakage). Its Sortino ratio divides downside variance by downside days ($N_{down}$) instead of total periods ($N_{total}$), distorting downside risk by 30–50%+.
5. **Silent Mock Data Cache Pollution**: If Yahoo Finance fails or rate-limits, `MarketDataService` silently generates synthetic geometric random-walk data and saves it to disk Parquet cache, where it is served to users and ML models as real historical market data for 12 hours.

---

## 2. PER-MODEL SCORECARD

| Component | Claimed Technology | Actual Implementation | Real ML? | Score (/10) |
| :--- | :--- | :--- | :---: | :---: |
| **Market Regime Classifier** | Unsupervised GMM Clustering | `sklearn.mixture.GaussianMixture` (3 components) | **Yes** (Poorly Calibrated) | **4.5 / 10** |
| **Multi-Horizon Forecaster** | LightGBM Quantile Regression (Q10/Q50/Q90) | Analytical normal formula with CAPM + momentum heuristic | **No** (Fictitious Claim) | **1.5 / 10** |
| **Portfolio Optimizer** | Ledoit-Wolf Covariance + HRP | Scikit-learn `LedoitWolf` + SciPy single linkage HRP | **Yes** (Stat. Learning) | **8.5 / 10** |
| **Discrete Allocation** | Whole-share Integer Allocation | `scipy.optimize.milp` + greedy deficit allocator | **Yes** (Opt. Operations) | **8.0 / 10** |
| **Backtest Engine & Metrics** | Quantitative Strategy Engine | Vectorized Pandas simulation with shifted signals | **No** (Rule-based) | **5.0 / 10** |
| **Smart Alert System** | 6-Trigger Intelligence Engine | Deterministic threshold checks (`if val > threshold`) | **No** (Heuristic) | **6.0 / 10** |
| **Review Fact-Checker** | 3-Tier Multi-Modal Fact-Checker | Regex patterns + math tolerance + optional Gemini API | **Hybrid** (Rules + LLM) | **7.0 / 10** |
| **NitiBot Assistant** | Gemini RAG Assistant | In-memory text concatenation + Google GenAI API | **Hybrid** (LLM API) | **6.5 / 10** |
| **Data Ingestion & Cleaner** | Clean Market Data Provider | `yfinance` + synthetic random-walk fallback + Parquet | **No** (Data Pipeline) | **5.5 / 10** |

---

## 3. REAL ML VS. HEURISTIC AUDIT

### Summary Breakdown

```
[Real Machine Learning]
└── src/app/ml/regime/classifier.py: GaussianMixture(n_components=3)
└── src/app/ml/portfolio/hrp.py: LedoitWolf() covariance shrinkage

[Optimization & Linear Programming]
└── src/app/ml/portfolio/allocation.py: scipy.optimize.milp

[External Foundation Models (LLM API)]
└── src/app/ml/reviews/tier3_llm.py: Google GenAI Client (gemini-2.5-flash)
└── src/app/ml/assistant/service.py: Google GenAI Client (gemini-2.5-flash)

[Pure Deterministic Heuristics & Hardcoded Formulas]
└── src/app/ml/forecasting/forecaster.py: Deterministic CAPM/Momentum formula (Zero LightGBM)
└── src/app/ml/forecasting/suitability.py: Hardcoded linear piecewise scoring
└── src/app/ml/portfolio/growth_calculator.py: Arithmetic compounding
└── src/app/ml/backtest/engine.py: Rule-based MA/RSI/Momentum signals
└── src/app/ml/alerts/evaluator.py: If-else threshold checks
└── src/app/ml/reviews/tier1_filters.py: Regular expressions
└── src/app/ml/reviews/tier2_factchecker.py: Regex parser + percentage difference check
```

### Detailed Inspection per Model

#### Model A: Market Regime GMM
- **Algorithm**: `sklearn.mixture.GaussianMixture(n_components=3, covariance_type="full", random_state=42, max_iter=200, n_init=3)`.
- **Features**: 6 engineered rolling features (`log_return_20d`, `log_return_50d`, `realized_vol_20d`, `parkinson_vol_20d`, `vix_level`, `vix_change_20d`).
- **Data Source**: Daily NIFTY 50 index (`^NSEI`) and India VIX (`^INDIAVIX`).
- **Train/Val/Test Split**: **None**. Fitted on the entire historical dataset on the fly.
- **Hyperparameters**: `n_components=3` (fixed); no BIC/AIC hyperparameter tuning.
- **Metrics**: None logged or validated. Log-likelihood and convergence (`converged_`) are recorded on manual train response, but no validation score exists.
- **Reproducibility**: Seed fixed at 42, but mapping heuristic causes cluster flipping.

#### Model B: Multi-Horizon Growth Forecaster
- **Claimed**: "Multi-factor quantile growth forecasting (LightGBM Q10/Q50/Q90)".
- **Actual**: No machine learning model exists. Lines 40–57 of `forecaster.py`:
  ```python
  capm_drift = self.risk_free_rate + beta * (self.benchmark_market_return - self.risk_free_rate) + alpha
  mom_blend = 0.4 * mom_3m + 0.3 * mom_6m + 0.3 * mom_12m
  trend_adj = 0.5 * ema_20_50_spread + 0.5 * ema_50_200_spread
  drift = 0.50 * capm_drift + 0.30 * mom_blend + 0.20 * trend_adj
  drift = float(np.clip(drift, -0.30, 0.50))
  ```
  Then quantiles are estimated via analytical normal z-scores:
  ```python
  q50 = float(np.exp(drift * tau) - 1.0)
  q10 = float(np.exp((drift - self.z_score_90 * vol) * tau) - 1.0)
  q90 = float(np.exp((drift + self.z_score_90 * vol) * tau) - 1.0)
  ```
- **Train/Val/Test Split**: N/A.
- **Seeds/Reproducibility**: Purely deterministic arithmetic.

---

## 4. REGIME GMM DEEP-DIVE

### 1. In-Sample Fitting & Look-Ahead Leakage
In `src/app/ml/regime/service.py` (lines 31–46 and 93–102):
```python
def _ensure_fitted(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
    index_df = self.market_service.get_history("^NSEI", start_date=start_date, end_date=end_date)
    vix_df = self.market_service.get_history("^INDIAVIX", start_date=start_date, end_date=end_date)
    features_df = extract_regime_features(index_df, vix_df)
    if not self.classifier.is_fitted:
        self.classifier.fit(features_df)
    return features_df
```
When `get_regime_history()` is called over a 5-year period, `features_df` contains all 5 years. `StandardScaler` and `GaussianMixture` fit on all 5 years simultaneously. Predictions for day $t=1$ in 2021 are computed using centroids and scaler statistics computed from market data in 2026. This is **severe look-ahead bias and scaler leakage**.

### 2. Negative Return Inversion Bug in Cluster Mapping
In `src/app/ml/regime/classifier.py` (lines 70–82):
```python
scores = {}
for c_idx in range(self.n_components):
    c_ret = centroids_df.loc[c_idx, ret_col]
    c_vol = max(centroids_df.loc[c_idx, vol_col], 1e-4)
    scores[c_idx] = c_ret / c_vol

sorted_clusters = sorted(scores.items(), key=lambda item: item[1], reverse=True)
bull_cluster = sorted_clusters[0][0]
bear_cluster = sorted_clusters[-1][0]
sideways_cluster = sorted_clusters[1][0]
```
**Mathematical Defect**:
When returns are negative, dividing by a higher volatility produces a number *closer to zero* (i.e. larger).
Consider two negative clusters:
- Cluster A (Mild drift): Return = $-0.01$, Volatility = $0.10 \implies \text{Score} = \frac{-0.01}{0.10} = -0.100$.
- Cluster B (Severe crash): Return = $-0.03$, Volatility = $0.35 \implies \text{Score} = \frac{-0.03}{0.35} = -0.086$.

Because $-0.086 > -0.100$, the **crash cluster is ranked HIGHER than the mild drift cluster**.
As a result:
- Cluster B (Crash) is assigned to `SIDEWAYS_CONSOLIDATION`.
- Cluster A (Mild drift) is assigned to `HIGH_VOLATILITY_BEAR`.

**Execution Output Proof**:
```
Sorted clusters: [(2, 0.4167), (1, -0.0857), (0, -0.1000)]
Highest (Bull): 2
Middle (Sideways): 1   <-- Cluster 1 (Severe Crash: ret -3%, vol 35%)
Lowest (Bear): 0       <-- Cluster 0 (Mild Drift: ret -1%, vol 10%)
```

### 3. Artificial Posterior Probability Distortion
In `src/app/ml/regime/classifier.py` (lines 122–128):
```python
# Apply temperature-scaled softmax smoothing to avoid extreme 99.9% probability collapse
temperature = 2.5
log_p = np.log(np.clip(raw_proba, 1e-12, 1.0))
scaled_logits = log_p / temperature
scaled_exp = np.exp(scaled_logits - np.max(scaled_logits, axis=1, keepdims=True))
raw_proba = scaled_exp / np.sum(scaled_exp, axis=1, keepdims=True)
```
The GMM's natural posterior probability $P(\text{Regime} = k \mid X)$ is artificially distorted with an arbitrary temperature hyperparameter ($T=2.5$). This makes the output probabilities uncalibrated and prevents downstream risk systems from receiving true Bayesian posteriors.

---

## 5. FORECASTER (LIGHTGBM QUANTILES) DEEP-DIVE

### 1. Fictitious Model Claim
The project claims a LightGBM multi-quantile regression model ($Q_{10}, Q_{50}, Q_{90}$).
- Search command: `Select-String -Path "src\**\*.py" -Pattern "lightgbm", "LGBM", "lgb"` returned **0 results**.
- There is no model file, no training script, no `.pkl` or `.booster`, and no quantile pinball loss.
- The forecaster is 100% hardcoded parametric math.

### 2. Time-Scaling Volatility Bug ($\tau$ vs. $\sqrt{\tau}$)
In `src/app/ml/forecasting/forecaster.py` (lines 88–98):
```python
# Horizon variance and standard deviation
horizon_vol = vol * np.sqrt(tau)

# Base case (50th percentile)
q50 = float(np.exp(drift * tau) - 1.0)

# 10th percentile (Pessimistic)
q10 = float(np.exp((drift - self.z_score_90 * vol) * tau) - 1.0)

# 90th percentile (Optimistic)
q90 = float(np.exp((drift + self.z_score_90 * vol) * tau) - 1.0)
```
Notice:
1. `horizon_vol = vol * np.sqrt(tau)` is computed on line 89 and **never referenced again**.
2. Lines 95 and 98 compute `(drift \pm z * vol) * tau = drift * tau \pm z * vol * tau`.
In geometric Brownian motion, price diffusion follows:
$$\ln(S_t / S_0) \sim \mathcal{N}\left(\left(\mu - \frac{1}{2}\sigma^2\right)\tau, \sigma^2 \tau\right)$$
The volatility term must scale with $\sqrt{\tau}$, not $\tau$. By multiplying volatility by $\tau$:
For a 1-month horizon ($\tau = 21/252 \approx 0.0833$):
- Code volatility component: $0.20 \times 0.0833 = 0.0167$.
- Correct diffusion volatility component: $0.20 \times \sqrt{0.0833} = 0.0577$.

**Execution Output Proof**:
```
tau: 0.08333333333333333
Code Q10/Q90 spread: 4.31%
Correct diffusion spread: 14.91%
Ratio correct / code: 3.46x
```
The predicted 1-month confidence cone is **3.46 times too narrow**, giving retail investors a dangerously false sense of certainty.

### 3. Fake Monotonicity Enforcement
Line 101 of `forecaster.py`:
```python
# Strict Monotonicity Projection (Isotonic sort guarantees Q10 <= Q50 <= Q90)
q10, q50, q90 = sorted([q10, q50, q90])
```
Instead of training non-crossing quantile regressors or calibrating quantile loss, the code simply sorts three numbers. The unit test `test_strict_quantile_monotonicity` simply asserts that Python's `sorted()` works.

---

## 6. HRP + LEDOIT-WOLF NUMERICAL VERIFICATION

### Numerical Verification Against Reference
A test matrix with 4 assets and 100 observations was evaluated comparing `src/app/ml/portfolio/hrp.py` against scikit-learn `LedoitWolf(assume_centered=False)`.

```python
# Command run via Python 3.12 venv:
cov_our, s_our = compute_shrunk_covariance(df, use_shrinkage=True)
lw = LedoitWolf(assume_centered=False).fit(X)
ref_cov = 0.5 * (lw.covariance_ + lw.covariance_.T) + np.eye(4) * 1e-7
```

**Real Execution Output**:
```
Covariance max diff: 0.0
Shrinkage our vs ref: 1.0 1.0
HRP Weights: {'A': 0.25, 'B': 0.25, 'C': 0.25, 'D': 0.25}
Sum of weights: 1.0
Collinear weights: {'A': 0.2774, 'B': 0.2774, 'C': 0.4452}
Zero variance weights: {'A': 0.5, 'B': 0.5}
```

### Verification Findings
1. **Covariance Shrinkage**: Exact match to scikit-learn (`max diff = 0.0`). Ridge regularization ($10^{-7} I$) ensures well-conditioned covariance.
2. **Correlation Distance**: Uses $D_{i,j} = \sqrt{0.5(1 - \rho_{i,j})}$, correctly clipped to $[0, 1]$ and diagonal set to 0.
3. **Quasi-Diagonalization**: Traverses tree generated by `scipy.cluster.hierarchy.linkage(condensed_dist, method="single")` via DFS. Matches standard single-linkage leaf order.
4. **Recursive Bisection**: Correctly splits clusters and weights clusters inversely proportional to their cluster variance.
5. **Degenerate & Singular Handling**: Collinear assets ($\rho \approx 1.0$) and zero-variance returns do not crash; the ridge fallback safely maintains positive definiteness.
6. **Persona Concentration Capping**: `apply_weight_caps()` iteratively redistributes excess weight to uncapped assets until convergence, with final normalization summing strictly to 1.0.

---

## 7. BACKTEST ENGINE & METRICS VERIFICATION

### 1. Execution Timing / Overnight Gap Mismatch
In `src/app/ml/backtest/engine.py` (lines 220–233):
```python
# Shift position by 1 day to prevent lookahead bias (trade executes on next bar)
positions = signals.shift(1).fillna(signals.iloc[0])
...
strategy_returns = (positions * daily_returns) - trade_costs
```
- `signals` are generated from the `close` series at day $t-1$.
- `daily_returns` is `close.pct_change()`, representing Close-to-Close returns ($(\text{Close}_t - \text{Close}_{t-1}) / \text{Close}_{t-1}$).
- Strategy return on day $t$ is calculated as `positions[t] * daily_returns[t]`.

**The Bug**: If a signal is computed after market close on day $t-1$, the trade cannot execute at $\text{Close}_{t-1}$. In real markets, it executes at $\text{Open}_t$. By using Close-to-Close returns, the strategy captures the overnight gap $(\text{Open}_t - \text{Close}_{t-1})$ before the order has even reached the exchange.

### 2. Sortino Ratio Mathematical Flaw
In `src/app/ml/backtest/metrics.py` (lines 62–64):
```python
downside_rets = daily_rets[daily_rets < daily_rf] - daily_rf
downside_std = float(np.sqrt(np.mean(downside_rets ** 2)) * np.sqrt(252.0)) if len(downside_rets) > 0 else 1e-6
sortino = float(excess_rets.mean() * 252.0 / downside_std) if downside_std > 1e-8 else 0.0
```
**The Flaw**: `np.mean(downside_rets ** 2)` divides the sum of squared downside returns by $N_{down}$ (the count of days with return below risk-free rate) rather than $T$ (the total number of days in the sample).

According to Sortino & Price (1994) and standard financial engineering:
$$\sigma_D = \sqrt{\frac{1}{T} \sum_{t=1}^T \min(0, r_t - r_f)^2} \times \sqrt{252}$$
By dividing by $N_{down} < T$, `downside_std` is inflated by $\sqrt{T / N_{down}}$.

**Execution Output Proof**:
```
Fraction of downside days: 0.4603
Downside std (code vs correct): 0.1462 vs 0.0992
Sortino ratio (code vs correct): 1.2144 vs 1.7899
Understatement error: -32.15%
```
The codebase understates the true Sortino ratio by **32.15%** for a standard series, and by more than **50%** for low-downside strategies.

### 3. Trade Log Non-Compounding Bug
In `src/app/ml/backtest/engine.py` (lines 161–162 and line 259):
```python
shares = initial_capital / entry_price if entry_price > 0 else 0.0
pnl = shares * (exit_price - entry_price) - (initial_capital * 2 * cost_rate)
...
total_cost_paid = float((trade_costs * initial_capital).sum())
```
Every individual trade log recalculates shares using `initial_capital` instead of the accumulated equity at the time of entry. As equity grows (e.g. from 100k to 200k), individual trade P&Ls reflect trades sized at 100k, creating a severe reconciliation discrepancy between the equity curve and the trade table.

---

## 8. DATA PROVENANCE & LEAKAGE

### 1. Silent Synthetic Mock Cache Poisoning
In `src/app/data/service.py` (lines 78–88):
```python
if df is None or df.empty:
    df = self.provider.fetch_history(canonical, start_date=start_date, end_date=end_date)
    # Fallback to mock data if external provider is offline, rate-limited, or symbol delisted
    if (df is None or df.empty) and isinstance(self.provider, YahooFinanceProvider):
        df = MockDataProvider().fetch_history(canonical, start_date=start_date, end_date=end_date)

    if df is not None and not df.empty:
        df = calculate_returns(df)
        if self.auto_cache:
            self.cache.save_history(canonical, df)
```
When Yahoo Finance encounters rate limits, timeouts, or network dropouts, `MockDataProvider` generates synthetic random-walk data. **This synthetic data is then written to the disk Parquet cache**. For the next 12 hours (`cache_ttl_seconds = 43200`), all models, backtests, and portfolio optimizations will load and train on synthetic mock data without warning or error.

### 2. Survivorship Bias in Universe Definition
In `src/app/universe.py` (lines 35–85):
`NIFTY50_CONSTITUENTS` contains the static list of current 2024–2026 constituents (e.g., `BEL`, `SHRIRAMFIN`, `ADANIENT`). Backtesting on a 5-year window (2020–2025) using this constituent list introduces survivorship bias, ignoring companies that were removed during bear phases or distress.

### 3. Calendar Alignment Pre-IPO Price Backfill
In `src/app/data/cleaner.py` (lines 144–146):
```python
reindexed[["open", "high", "low", "close", "adj_close"]] = reindexed[
    ["open", "high", "low", "close", "adj_close"]
].bfill()
```
When aligning a newly listed stock against the 5-year benchmark calendar, `bfill()` back-propagates the first available price to all previous dates before listing, creating artificial flat prices and zero-return bars before the asset's IPO.

---

## 9. TEST QUALITY FOR ML

An audit of `tests/unit/test_*.py` shows 30 passing tests, but reveals critical testing deficits:

1. **Shape-Only and Trivial Assertions**:
   - `tests/unit/test_growth_forecaster.py` (lines 44–56): Only checks `isinstance(forecast, MultiHorizonGrowthForecast)` and `assert forecast.m1 is not None`.
   - `test_strict_quantile_monotonicity` (lines 58–78): Tests that $Q_{10} \le Q_{50} \le Q_{90}$. This is guaranteed by `sorted()` in the implementation, not by model calibration.
2. **Missing Empirical Quantile Invariants**:
   - Zero tests measure empirical pinball loss or coverage probability (e.g., verifying whether approximately 10% of realized returns fall below $Q_{10}$ out-of-sample).
3. **Synthetic Toy Data in GMM Tests**:
   - `tests/unit/test_regime_classifier.py` uses three widely separated synthetic normal distributions with manual means (Return: $+6\%$, $-8\%$, $+0.5\%$; Volatility: $10\%$, $28\%$, $15\%$). This masks the real-world cluster sorting inversion bug that occurs when multiple clusters have negative returns.

---

## 10. REAL EXECUTION LOGS

### Targeted PyTest Execution
```powershell
& "D:\Codebase\QuantNiti\.venv\Scripts\python.exe" -m pytest tests/unit/test_regime_classifier.py tests/unit/test_regime_features.py tests/unit/test_growth_forecaster.py tests/unit/test_hrp_optimizer.py tests/unit/test_backtest_engine.py tests/unit/test_backtest_metrics.py -v
```
**Output**:
```
tests/unit/test_regime_classifier.py::test_classifier_fit_and_predict PASSED [  3%]
tests/unit/test_regime_classifier.py::test_classifier_probabilities_sum_to_one PASSED [  6%]
tests/unit/test_regime_classifier.py::test_classifier_state_label_determinism PASSED [ 10%]
tests/unit/test_regime_features.py::test_calculate_rolling_log_returns PASSED [ 13%]
tests/unit/test_regime_features.py::test_calculate_realized_volatility PASSED [ 16%]
tests/unit/test_regime_features.py::test_calculate_parkinson_volatility PASSED [ 20%]
tests/unit/test_regime_features.py::test_extract_regime_features PASSED  [ 23%]
tests/unit/test_growth_forecaster.py::test_forecast_all_four_horizons PASSED [ 26%]
tests/unit/test_growth_forecaster.py::test_strict_quantile_monotonicity PASSED [ 30%]
tests/unit/test_growth_forecaster.py::test_forecast_cone_widening_over_longer_horizons PASSED [ 33%]
tests/unit/test_hrp_optimizer.py::test_hrp_optimizer_weight_sum_and_positivity PASSED [ 36%]
tests/unit/test_hrp_optimizer.py::test_hrp_optimizer_risk_persona_caps PASSED [ 40%]
tests/unit/test_hrp_optimizer.py::test_hrp_optimizer_lower_volatility_gets_higher_allocation_in_conservative PASSED [ 43%]
tests/unit/test_hrp_optimizer.py::test_compute_hrp_weights_helper_function PASSED [ 46%]
tests/unit/test_hrp_optimizer.py::test_hrp_optimizer_handles_two_assets PASSED [ 50%]
tests/unit/test_hrp_optimizer.py::test_compute_shrunk_covariance_ledoit_wolf PASSED [ 53%]
tests/unit/test_hrp_optimizer.py::test_compute_shrunk_covariance_fallback_on_degenerate_data PASSED [ 56%]
tests/unit/test_hrp_optimizer.py::test_compute_shrunk_covariance_without_shrinkage PASSED [ 60%]
tests/unit/test_hrp_distance_matrix_conditioning_extreme_correlation PASSED [ 63%]
tests/unit/test_hrp_optimizer.py::test_hrp_optimizer_weight_stability_noisy_regime PASSED [ 66%]
tests/unit/test_hrp_optimizer.py::test_hrp_optimizer_all_personas_and_caps PASSED [ 70%]
tests/unit/test_hrp_optimizer.py::test_hrp_optimizer_esg_conscious_favors_high_esg_stocks PASSED [ 73%]
tests/unit/test_backtest_engine.py::test_buy_and_hold_strategy PASSED    [ 76%]
tests/unit/test_backtest_engine.py::test_ma_crossover_strategy PASSED    [ 80%]
tests/unit/test_backtest_engine.py::test_rsi_mean_reversion_strategy PASSED [ 83%]
tests/unit/test_backtest_engine.py::test_bollinger_bands_strategy PASSED [ 86%]
tests/unit/test_backtest_engine.py::test_dual_momentum_strategy PASSED   [ 90%]
tests/unit/test_backtest_engine.py::test_transaction_costs_and_slippage_impact PASSED [ 93%]
tests/unit/test_backtest_metrics.py::test_calculate_backtest_metrics_values PASSED [ 96%]
tests/unit/test_backtest_metrics.py::test_calculate_regime_breakdown PASSED [100%]

============================= 30 passed in 8.36s ==============================
```

---

## 11. PRIORITIZED ACTIONABLE RECOMMENDATIONS

### MUST-FIX (Critical Correctness & Safety)

#### 1. Fix Forecaster Volatility Diffusion Scaling Bug
- **File & Line**: `src/app/ml/forecasting/forecaster.py:95-98`
- **Code Quote**:
  ```python
  q10 = float(np.exp((drift - self.z_score_90 * vol) * tau) - 1.0)
  q90 = float(np.exp((drift + self.z_score_90 * vol) * tau) - 1.0)
  ```
- **Smallest Concrete Fix**: Scale diffusion with $\sqrt{\tau}$ and account for Itô's lemma convexity adjustment:
  ```python
  diffusion = self.z_score_90 * vol * np.sqrt(tau)
  drift_term = (drift - 0.5 * (vol ** 2)) * tau
  q10 = float(np.exp(drift_term - diffusion) - 1.0)
  q90 = float(np.exp(drift_term + diffusion) - 1.0)
  ```

#### 2. Fix GMM Negative-Return Cluster Ranking Inversion
- **File & Line**: `src/app/ml/regime/classifier.py:70-76`
- **Code Quote**:
  ```python
  scores[c_idx] = c_ret / c_vol
  ```
- **Smallest Concrete Fix**: Rank clusters by penalizing volatility directly or using signed risk-adjusted returns:
  ```python
  # Volatility penalty ranking: Bull maximizes return & minimizes vol; Bear maximizes negative return and vol
  scores[c_idx] = c_ret - (0.5 * c_vol)
  ```

#### 3. Fix Sortino Ratio Denominator
- **File & Line**: `src/app/ml/backtest/metrics.py:62-63`
- **Code Quote**:
  ```python
  downside_rets = daily_rets[daily_rets < daily_rf] - daily_rf
  downside_std = float(np.sqrt(np.mean(downside_rets ** 2)) * np.sqrt(252.0))
  ```
- **Smallest Concrete Fix**: Divide downside sum of squares by total observations ($T$), not downside count:
  ```python
  downside_diff = np.minimum(0.0, daily_rets - daily_rf)
  downside_std = float(np.sqrt(np.mean(downside_diff ** 2)) * np.sqrt(252.0))
  ```

#### 4. Stop Caching Synthetic Mock Data as Real History
- **File & Line**: `src/app/data/service.py:80-88`
- **Code Quote**:
  ```python
  if (df is None or df.empty) and isinstance(self.provider, YahooFinanceProvider):
      df = MockDataProvider().fetch_history(canonical, start_date=start_date, end_date=end_date)
  if df is not None and not df.empty:
      df = calculate_returns(df)
      if self.auto_cache:
          self.cache.save_history(canonical, df)
  ```
- **Smallest Concrete Fix**: Only cache real data; never persist mock data to the production Parquet cache:
  ```python
  is_mock = False
  if (df is None or df.empty) and isinstance(self.provider, YahooFinanceProvider):
      df = MockDataProvider().fetch_history(canonical, start_date=start_date, end_date=end_date)
      is_mock = True

  if df is not None and not df.empty:
      df = calculate_returns(df)
      if self.auto_cache and not is_mock:
          self.cache.save_history(canonical, df)
  ```

---

### SHOULD-FIX (High Priority Pipeline Integrity)

#### 5. Implement Actual LightGBM Quantile Regressors or Correct Architecture Docs
- **File & Line**: `src/app/ml/forecasting/forecaster.py:20` & `docs/research/ml-architecture-and-competitive-moat.md:11`
- **Action**: Either build a true LightGBM pipeline (`LGBMRegressor(objective='quantile', alpha=0.1/0.5/0.9)`) trained across rolling multi-factor features with purged cross-validation, or update platform claims to accurately state that return cones are generated via analytical CAPM-momentum diffusion formulas.

#### 6. Eliminate Look-Ahead Bias in Regime Classification
- **File & Line**: `src/app/ml/regime/service.py:31-46`
- **Action**: Fit GMM exclusively on an expanding rolling window up to date $t-1$, or freeze trained GMM parameters on an explicit historical training set and use `transform()` / `predict()` purely out-of-sample.

#### 7. Align Backtest Trade Execution with Market Open
- **File & Line**: `src/app/ml/backtest/engine.py:220-233`
- **Action**: For signals generated at $t-1$ close, calculate strategy return on day $t$ using Open-to-Close returns ($(\text{Close}_t - \text{Open}_t) / \text{Open}_t$) plus entry slippage against open price, rather than Close-to-Close returns.

---

### NICE-TO-HAVE (Medium/Low Priority Polish)

#### 8. Compound Equity in Backtest Trade Extraction Logs
- **File & Line**: `src/app/ml/backtest/engine.py:161-163`
- **Action**: Size trades dynamically using `current_equity / entry_price` instead of fixed `initial_capital / entry_price`.

#### 9. Prevent Pre-IPO Flat Price Backfilling
- **File & Line**: `src/app/data/cleaner.py:144-146`
- **Action**: Truncate benchmark dates to the first valid trading date of the asset rather than using `bfill()`.

#### 10. Add Empirical Quantile Coverage Unit Tests
- **File & Line**: `tests/unit/test_growth_forecaster.py`
- **Action**: Add backtest validation checking that realized asset returns violate $Q_{10}$ with an empirical frequency close to 10% ($\pm 3\%$).

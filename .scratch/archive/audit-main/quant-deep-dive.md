# Quant / ML Deep Dive — main @ 581890f

Reviewer: independent read + dynamic execution (`uv run python`, MockDataProvider, no network).
Complements `.scratch/audit-main/ml.md` and `ml-critique.md`.

## Verdict

The ML surface is **1 real unsupervised model (GMM) + 1 real optimizer (HRP/Ledoit-Wolf) + 1 real MILP allocator**.
The *forecasting* centerpiece is a hand-tuned parametric heuristic (CAPM + momentum + EMA), not a trained model.
There is **no training pipeline, no model artifact, no evaluation/validation, no calibration, no backtest of the
recommendations**, and the "LightGBM quantile regression" claim appears in product copy and in NitiBot's own
system prompt. Any claim of a "robust ML pipeline" is not supported by the code.

## Q1 (Critical, math): Forecaster quantile cones are wrong by up to 2.3x — `forecaster.py:88-98`

```python
horizon_vol = vol * np.sqrt(tau)          # computed, never used (dead code)
q50 = np.exp(drift * tau) - 1.0
q10 = np.exp((drift - z * vol) * tau) - 1.0   # WRONG: vol*tau, should be vol*sqrt(tau)
q90 = np.exp((drift + z * vol) * tau) - 1.0
```

Diffusion scales with √τ, not τ. With drift=12%, vol=20%:

| Horizon | Code P10/P90 | Correct P10/P90 (MC-verified) | Cone understated |
|---|---|---|---|
| 1M | -1.13% / +3.19% | -6.19% / +8.76% | 2.29x |
| 3M | -3.35% / +9.86% | -9.34% / +17.12% | 1.55x |
| 6M | -6.59% / +20.70% | -11.40% / +27.28% | 1.24x |
| 12M | -12.74% / +45.69% | same (τ=1) | 1.00x |

Monte Carlo (2M paths, lognormal) reproduces the "correct" column exactly, so the code's 1M "10th percentile"
is really ~the 31st percentile. Users are shown a downside bound that is ~5x too shallow in rupees at 1M.
Also: `q50` omits the Itô term, so it is really the median, not the mean; `sorted([q10,q50,q90])` fakes
monotonicity instead of fixing inputs. Fix: `exp((drift-0.5*vol²)τ ± z*vol*√τ)`, assert monotonicity instead of sorting.

## Q2 (Critical, integrity): Fabricated accuracy and fabricated ground truth

- `growth_calculator.py:170` — `hit_rate = 84.6 if bull else 81.2`, rendered in the Trust Card as
  *"81.2% historical directional prediction accuracy across 5-year rolling backtests"*. No backtest produces
  this number; it is a literal constant shown to every user on the Grow flow, i.e. a fabricated performance claim
  next to SEBI-sensitive advice.
- `reviews/agent.py:56-103` — the "3-tier AI fact-checker" ground truth for baskets is a hardcoded table
  (`balanced 6M = 12.8%`, `aggressive 12M = 26.0%`), strategies are always `14.5`, unknown stocks `11.5`,
  everything else `13.2`. `tier2_factchecker.py:123` defaults to `12.0` when nothing is passed.
  Consequence: a user claiming +12.8% on a balanced basket is stamped **Verified**; a user honestly claiming
  +30% is rejected as *"Fraudulent or exaggerated claim"*. The badge certifies conformance to a constant.
- `agent.py:58-63` selects the persona row via `"conservative" in str(target_id)`, but basket IDs are
  `bsk_<uuid>` (`portfolio/service.py:280`), so every basket review is scored against the Balanced row. Dead branch.
- `tier2_factchecker.py:35` takes the *first* percentage in the text. "NIFTY fell 8% but I made 12%" parses as +8%
  (the negation list omits "fell"), then gets rejected as exaggerated. Claimed duration is extracted but never
  used to compute the return; only `actual_return_pct` for the detected horizon is compared.

## Q3 (Critical, presentation): Recommender and benchmark are not comparable

- `portfolio/service.py:268-270`: NIFTY baseline is `12.0 if bull else 5.0`, hardcoded, while the basket number
  comes from the drift model clipped to [-30%, +50%]. The "AI Basket beats NIFTY" table is therefore
  apples-to-oranges by construction and cannot lose in a bull regime.
- `growth_calculator.py:83-87`: missing forecasts fall back to +2% / +8% / +15% invented returns.
- `growth_calculator.py:52-65`: horizons >8M silently reuse the **12M cone** for the whole period. A 24M
  request reports a 12M return as the 24M total.
- `portfolio/service.py:192` vs `growth_calculator.py:51`: per-asset `growth_base_pct` maps `"9M"→m6` while the
  basket projection maps `"9M"→m12` — the same basket shows two different numbers for one horizon.
- `compounding_engine.py:290`: GBM cone base is `initial_lump` else `max(monthly_sip*12, 10_000)`, so the
  uncertainty band is drawn on a capital number that has nothing to do with the SIP curve it is plotted against,
  and it ignores SIP contributions entirely.

## Q4 (High, ML methodology): GMM regime layer

- Labels ranked only by `ret/vol` (`classifier.py:70-82`). Empirical run on mock data: the cluster labelled
  **High-Volatility Bear** had mean realised vol 0.1442, *lower* than the cluster labelled **Sideways** (0.1520).
  The volatility semantics in the name are unverified by construction; with two negative-return clusters the
  ranking inverts (verified by the prior audit).
- Fit is in-sample on the full requested window then used to label the same window (`regime/service.py:31-46`):
  look-ahead leakage in every historical regime chart.
- `_ensure_fitted` fits once per process using whatever window the first request happened to supply and never
  refits, so request order changes the model.
- No BIC/AIC selection, no covariance-type choice, no persistence/versioning of fitted params.
- `predict_proba` temperature-divides log-posteriors (`classifier.py:122-128`) purely for display; the returned
  "confidence" is not a model posterior. Live run returned bull=0.0, bear=0.0, sideways=1.0, confidence 1.0
  despite the smoothing.

## Q5 (High, data): synthetic prices are cached and served as real

`data/service.py:78-88`: on any Yahoo failure, `MockDataProvider` data is generated, then `calculate_returns` +
`cache.save_history` persist it for the 12h TTL. No `is_mock` flag anywhere in the response models, so the UI,
the GMM and the HRP all consume synthetic geometric random walks as if they were NSE history. Mock `^INDIAVIX`
is an unconstrained random walk (ran to 64 in the live check) rather than the mean-reverting VIX.

## Q6 (Medium): metrics / backtest

- `backtest/metrics.py:62-64` Sortino denominator uses downside days only (verified: -0.0294 vs -0.0413).
- `backtest/engine.py:161` trade log sizes every trade off `initial_capital`, so trade P&L doesn't reconcile
  with the compounded equity curve.
- `engine.py:221` first bar position = signal at bar 0 (tiny lookahead/cost artifact).
- Signal warm-up uses `min_periods=1`, so MA/BB signals fire on 1-2 observations.

## What is actually good

- `hrp.py`: Ledoit-Wolf + ridge, correlation distance, single linkage, quasi-diagonalisation, bisection,
  cap redistribution — verified against a reference (max diff 0.0). Clean, defensive code.
- `allocation.py`: real MILP with slack variables plus a sensible greedy fallback.
- `factors.py`: Wilder RSI/EMA/MACD/BB/CAPM beta-alpha are implemented correctly.
- Compounding formulas (annuity-due SIP, step-up, FD hurdle) are arithmetically correct.

## Fix priority (ML)

1. Forecaster diffusion + Itô term + delete `horizon_vol`; add pinball/coverage test.
2. Delete the hardcoded 84.6/81.2 hit rate; compute it from an actual walk-forward evaluation or remove the pillar.
3. Reviews: compute ground truth from real price series for every target type; if unavailable, return
   "unverified", never a default 12%.
4. Benchmark NIFTY with the same model used for the basket.
5. Explicit horizon scaling for >12M; remove invented fallback returns.
6. Mark mock data in the API contract and never persist it to the cache.
7. Sign-aware GMM label mapping + purged fit; persist the fitted model.

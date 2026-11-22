# ADVERSARIAL CRITIQUE OF `.scratch/audit-main/ml.md`

**Reviewer:** Independent verification pass (read-only)
**Date:** November 16, 2026
**Scope:** Verify top findings by reading cited code and running small targeted checks. No source modified; no full test suite run.
**Audited document:** `.scratch/audit-main/ml.md` (branch `feat/main-audit-hardening` @ `581890f`)

---

## Verdict key

- **AGREE** — claim matches the code.
- **TIGHTEN** — claim is directionally right but imprecise/overstated; fix-phase wording should be corrected.
- **CORRECT** — claim is wrong or understated; fix-phase must use the corrected fact.

---

## Verification method (targeted checks run)

- Whole-repo grep for `lightgbm` / `LGBM` / `lgb` (incl. non-`.py`): only `pyproject.toml:13`, `uv.lock`, docs, `graphify-out/`, and a throwaway `.tmp/verify_ml_critique.py` probe. Zero in `src/`, `tests/`, `scripts/`.
- Read cited files: `forecaster.py`, `classifier.py`, `service.py` (regime + data), `hrp.py`, `metrics.py`, `engine.py`, `cleaner.py`, `factors.py`.
- Reproduced GMM score ranking with the audit's exact numbers → matched audit "Execution Output Proof".
- Computed volatility spread ratio → 3.47x (audit: 3.46x).
- Computed Sortino understatement on a 500-day synthetic series → -28.7% (audit: -32.15% on its series).
- Verified Ledoit-Wolf covariance against reference → `max diff = 0.0`, shrinkage `1.0`/`1.0`.

---

## Top findings — verdicts

### F1. "No LightGBM code anywhere; forecaster is deterministic heuristic" — **AGREE (tighten wording)**

- Evidence checked: grep of `src/`, `tests/`, `scripts/` returns 0; `pyproject.toml:13` declares `lightgbm>=4.7.0`; `forecaster.py:40-57` is CAPM + momentum + EMA blend; no `.pkl`/`.booster` artifacts in repo (only venv test data).
- Tighten: phrase as "LightGBM is an **unimplemented dependency/claim**, not 'fictitious code'." The model is a real (if simplistic) parametric heuristic producing cones; the defect is the marketing/architecture claim and the unused dependency. `.tmp/verify_ml_critique.py` does import lightgbm, so "zero anywhere in repo" is technically false — scope the claim to production code.

### F2. "Volatility scaling bug: `vol*tau` instead of `vol*sqrt(tau)`; 3.46x underestimate" — **AGREE**

- Evidence checked: `forecaster.py:88-89` computes `horizon_vol = vol * np.sqrt(tau)` then never uses it; lines 95/98 compute `(drift ± z*vol) * tau`. Reproduced: code spread 4.27%, diffusion-correct spread 14.81%, ratio 3.47x for 1M (audit 4.31%/14.91%/3.46x — example-dependent, same conclusion).
- Tighten: also note a second, unflagged defect — the drift term lacks the Itô convexity adjustment (`-0.5*vol²*tau`), so `q50` is slightly overstated; and `horizon_vol` is dead code. Fix should correct both scaling and convexity, not just multiply by sqrt.
- Additional missed: momentum inputs are period returns (`factors.py:114-117`) blended into an annualized drift with no annualization (horizon mismatch); vol floor `max(..., 0.08)` silently floors annualized vol at 8%.

### F3. "GMM negative-return cluster inversion" — **AGREE**

- Evidence checked: `classifier.py:70-82` ranks `c_ret / c_vol`. Reproduced with audit's exact inputs: Cluster 1 (crash: ret -0.03, vol 0.35) scores -0.0857, Cluster 0 (mild drift: ret -0.01, vol 0.10) scores -0.1000; sorted descending puts the crash in the middle → `SIDEWAYS_CONSOLIDATION`, mild drift → `HIGH_VOLATILITY_BEAR`. Audit's "Execution Output Proof" reproduced verbatim.
- Tighten: the inversion requires **two clusters with negative returns** of differing volatility; the bundled test (`test_regime_classifier.py`) uses a single bear cluster, which is why it never catches it. Audit's suggested fix (`c_ret - 0.5*c_vol`) is itself an unvalidated heuristic — a more robust mapping should separate sign of return from volatility magnitude (e.g., rank by return first, break ties/volatility within sign groups). Flag as a fix-phase consideration, not just a one-line change.

### F4. "In-sample fit / no train-test split + temperature-softmax distortion" — **AGREE (look-ahead) / TIGHTEN (temperature severity)**

- Evidence checked: `regime/service.py:31-46` fits `StandardScaler` + `GaussianMixture` on the full requested history (5 years when `get_regime_history` is called) before predicting day-1 points → scaler/centroid look-ahead. `classifier.py:122-128` applies temperature 2.5 to log-posteriors.
- Tighten: the temperature scaling is a **deliberate smoothing choice**, not a mathematical bug; it does make `predict_proba` uncalibrated vs. the GMM posterior, but that's a calibration/contract issue (medium severity), not correctness-critical. Also flag an unmentioned defect: `_ensure_fitted` caches the fitted classifier and **never refits when the date range changes**, so a stale model can persist after `train_model` is called with a different window.

### F5a. "HRP + Ledoit-Wolf mathematically sound" — **AGREE (with scope caveat)**

- Evidence checked: `hrp.py` covariance path matches `LedoitWolf(assume_centered=False)` exactly (`max diff = 0.0`, shrinkage `1.0`/`1.0` on a 100×4 matrix); correlation distance `sqrt(0.5*(1-rho))` clipped to [0,1]; single-linkage + quasi-diagonalization + recursive bisection + cap redistribution all present and internally consistent.
- Tighten: the audit's "sound" verdict rests on **covariance shrinkage only**; HRP weights were not independently checked against a reference implementation, and single-linkage HRP is known to be unstable to perturbations (not incorrect, but the "8.5/10" score is generous). Degenerate/zero-variance and collinear cases handled via ridge fallback — verified by code inspection.

### F5b. "Sortino denominator bug (divides by N_down not T)" — **AGREE**

- Evidence checked: `metrics.py:62-64` computes `np.mean(downside_rets**2)` over only downside days. Standard formula uses all observations. Reproduced on a 500-day series: code Sortino -0.0294 vs. correct -0.0413 (understatement ~29%; audit's 32.15% is series-dependent, same direction and mechanism). Fix via `np.minimum(0.0, daily_rets - daily_rf)` averaged over all days is correct.

---

## Additional missed issues / overstatements to flag

1. **Backtest "overnight gap leakage" is mischaracterized as leakage.** `engine.py:220-233` shifts signals by 1 but uses Close-to-Close returns. This is a **return-basis mismatch**, not information leakage: the strategy is implicitly credited with overnight gaps it could not have captured. Bias direction depends on the sign of overnight gaps; it can inflate or deflate returns. The recommended Open-to-Close fix is right, but the framing should be "execution/return measurement mismatch."
2. **First-bar lookahead in backtest.** `positions = signals.shift(1).fillna(signals.iloc[0])` makes bar 0 carry a position derived from bar 0's own close; `trade_costs` is then charged on bar 0. First bar's return is ~0 (pct_change fillna), so impact is small but the assumption is wrong.
3. **Forecaster momentum units.** `factors.py:114-117` produces period returns (1M/3M/6M/12M), but `forecaster.py:45-49` blends them directly into an annualized drift with no annualization — horizon-mismatched inputs.
4. **Forecaster vol floor.** `vol = max(0.6*rvol_30d + 0.4*rvol_90d, 0.08)` silently floors annualized vol at 8%, distorting low-vol assets.
5. **Mock-data pollution scope.** Audit covers `service.py:78-88` caching mock history. Additionally `get_latest_quote` (`service.py:115-122`) falls back to `MockDataProvider` without any flag, so callers cannot distinguish real vs. synthetic quotes.
6. **Survivorship / pre-IPO backfill (audit covers cleaner; also applies to `get_aligned_dataset`).** `service.py:147-163` calls `align_to_trading_calendar` then `ffill`/`bfill`, producing flat pre-IPO prices and zero-return bars.
7. **GMM no hyperparameter selection and full covariance with 6 features** — minor, audit mentions n_components. Full covariance with limited history can overfit; not flagged by audit.
8. **`_ensure_fitted` staleness** (see F4).
9. **Fake monotonicity enforcement.** `forecaster.py:101` `sorted([q10, q50, q90])` guarantees ordering by construction; `test_strict_quantile_monotonicity` only asserts Python's `sorted()` works. No empirical quantile coverage test exists.
10. **Trade log non-compounding.** `engine.py:161-162` sizes every trade at `initial_capital` instead of accumulated equity, so trade-log P&L reconciles incorrectly against the equity curve as equity grows.
11. **GMM look-ahead via scaler.** `StandardScaler` fit on full history before predicting day-1 (see F4).
12. **No empirical quantile coverage tests.** Zero tests measure pinball loss or coverage probability.

---

## Corrections the fix phase must account for

1. Scope the "no LightGBM" claim to `src/`/`tests/`/`scripts/`; remove or gate the unused `lightgbm>=4.7.0` dependency.
2. Fix forecaster diffusion: use `vol*sqrt(tau)` for the quantile spread **and** apply Itô convexity (`drift - 0.5*vol²`)*tau in the exponent; delete dead `horizon_vol`. Annualize momentum inputs or drop them; reconsider the 8% vol floor.
3. Replace GMM cluster mapping with a sign-aware ranking (not just `c_ret - 0.5*c_vol`), and add a regression test with **two negative-return clusters** of differing volatility to lock in the fix.
4. Eliminate look-ahead in regime: fit on an expanding/purged window up to t-1, or freeze trained params and use `predict` only out-of-sample; fix `_ensure_fitted` to refit when the date range changes. Treat temperature scaling as a documented calibration choice or remove it.
5. Keep HRP/Ledoit-Wolf as-is (verified), but add an independent HRP weight reference test; document single-linkage instability caveat.
6. Fix Sortino by averaging squared downside over **all** observations (`np.minimum`).
7. Reframe backtest "overnight gap" as a return-basis mismatch; switch to Open-to-Close returns when open data is available; fix first-bar `fillna` to 0.0 position; fix trade-log sizing to use accumulated equity.
8. Never persist mock data to the Parquet cache (audit fix); also surface a `is_mock`/source flag from `get_latest_quote` and `get_history`.
9. Truncate pre-IPO dates instead of `bfill` in both `cleaner.py` and `get_aligned_dataset`.
10. Replace `sorted()` monotonicity enforcement with real non-crossing quantile calibration or document it; add empirical quantile coverage tests.
11. Add hyperparameter selection (BIC/AIC) and consider tied/diagonal covariance for GMM with limited history.

---

## Summary checklist for fix phase

| Finding | Original Status | Critique Verdict | Fix Action Required |
|---|---|---|---|
| **F1** (No LightGBM) | MUST-FIX | **AGREE (tighten)** | Scope claim to production code; remove/gate unused dep. |
| **F2** (Vol scaling) | MUST-FIX | **AGREE** | Use `vol*sqrt(tau)` + Itô convexity; delete dead `horizon_vol`; fix momentum units & vol floor. |
| **F3** (GMM inversion) | MUST-FIX | **AGREE** | Sign-aware cluster mapping + two-negative-cluster regression test. |
| **F4** (In-sample fit / temp) | MUST-FIX | **AGREE / TIGHTEN** | Purged/expanding fit; fix `_ensure_fitted` staleness; document or remove temperature. |
| **F5a** (HRP/Ledoit-Wolf) | SOUND | **AGREE (scope caveat)** | Keep as-is; add independent HRP weight reference test; document single-linkage instability. |
| **F5b** (Sortino) | MUST-FIX | **AGREE** | Average squared downside over all observations via `np.minimum`. |
| **Overnight gap** | MUST-FIX (framing) | **TIGHTEN** | Reframe as return-basis mismatch; switch to Open-to-Close; fix first-bar fillna. |
| **Mock cache** | MUST-FIX | **AGREE** | Never cache mock data; surface source flag. |
| **Pre-IPO bfill** | SHOULD-FIX | **AGREE** | Truncate instead of bfill. |
| **Monotonicity** | NICE | **TIGHTEN** | Replace `sorted()` with real calibration or document. |
| **Trade log sizing** | NICE | **AGREE (missed)** | Size trades by accumulated equity. |

---

**Bottom line:** The audit's five headline ML findings are substantively correct and verified; the main corrections needed are (a) scope/wording on the LightGBM claim, (b) the forecaster fix must also handle Itô convexity and momentum units, (c) the GMM fix needs a sign-aware mapping plus a two-negative-cluster test, and (d) the backtest "leakage" framing should be corrected to a return-basis mismatch. HRP/Ledoit-Wolf soundness holds within the verified scope. No false positives beyond the LightGBM "zero anywhere in repo" overstatement.
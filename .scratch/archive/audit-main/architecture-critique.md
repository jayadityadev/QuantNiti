# QuantNiti — Architecture Audit Critique (adversarial, read-only)

Reviewer: independent model family. No source files modified. No test suites run.
Source audited: `.scratch/audit-main/architecture.md` (branch `feat/main-audit-hardening` @ `581890f`).
Method: re-verified every top finding with read-only greps/reads of the cited code. Counts re-run where the audit quotes a number.

## Verdict key
- **AGREE** — claim matches the code.
- **TIGHTEN** — claim is directionally right but imprecise/overstated; fix-phase wording should be corrected.
- **CORRECT** — claim is wrong or understated; fix-phase must use the corrected fact.

---

## Finding 1 — Explore/Home ~58 uncached Yahoo calls + silent synthetic fallback → **AGREE (TIGHTEN location)**

Evidence checked:
- Universe size: `get_universe_symbols(include_benchmarks=False)` = **58** (confirmed via import). `list_explore_stocks` iterates `get_universe_metadata(include_benchmarks=False)` and calls `self.market_service.get_latest_quote(sym)` per symbol (`src/app/ml/forecasting/service.py:252`). Home's `TopRecommendations` hits the same alias (`/api/v1/stocks/explore` → `app.state.explore_service.list_explore_stocks`), so a Home load repeats the loop.
- `MarketDataService.get_latest_quote` (`src/app/data/service.py:115-122`) has **no cache** (only `get_history` is Parquet-cached). Confirmed.
- Fallback chain: `YahooFinanceProvider.fetch_quote` (`src/app/data/provider.py:78-135`) tries `fast_info`, then `fetch_history(period="5d")`, then raises `RuntimeError`. `MarketDataService.get_latest_quote` catches and substitutes `MockDataProvider().fetch_quote` (`service.py:121`). `MockDataProvider` is a deterministic random walk seeded by symbol (`provider.py:141-147`, `fetch_quote:220-249`).

TIGHTEN: the audit says "fetch_quote falls back to fetch_history … and if that also fails it falls back to MockDataProvider". The provider-level fallback is fast_info→history; the **MockDataProvider substitution happens in the service layer** (`service.py:119-122`), not in `fetch_quote`. Behaviour is identical; only the attribution is off. Fix-phase code/docs should name `MarketDataService.get_latest_quote` as the mock-substitution site.

Also note (missed by audit): `TopRecommendations.tsx` has its own hard-coded 4-stock fallback (`RELIANCE/TCS/HDFCBANK/BHARTIARTL`) on fetch error (`TopRecommendations.tsx:29-34`) — a second silent synthetic fallback on the frontend.

---

## Finding 2 — "live" SSE feed is a random walk overwriting real mark-to-market → **AGREE (TIGHTEN seeding)**

Evidence checked:
- `get_tick_generator` mounts `MarketTickGenerator(market_service=market_svc, mode="synthetic")` (`src/app/api/routes/stream.py:20`). Confirmed.
- `generate_tick` uses `random.gauss(0.0, 0.0012)` during market hours (`src/app/data/streaming.py:154`); freezes price outside 09:15–15:30 IST (`streaming.py:160-163`, `is_indian_market_open`).
- `PortfolioPage` subscribes and recomputes `current_value`, `total_pnl`, `unrealized_pnl` from `tick.price` (`PortfolioPage.tsx:69-110`). Confirmed.
- Frontend never calls `GET /portfolios/{id}` (grep: only `/api/v1/portfolios` list on mount). The backend `get_portfolio` (yfinance-based mark-to-market) is never polled. Confirmed.

TIGHTEN: the walk is **seeded from a real quote** — `_get_base_price` calls `market_service.get_latest_quote` on first tick (`streaming.py:96-121`), so the first number is real; it then drifts. The audit's "random number generator" framing is slightly overstated for the seed but accurate for everything after. The credibility point stands: a drifting synthetic price overwrites a real valuation with no label.

---

## Finding 3 — Alerts/notifications are hardcoded fake numbers → **AGREE (TIGHTEN lifecycle)**

Evidence checked:
- Backend: `_seed_initial_alerts` injects 4 alerts with literal numbers ("RSI reached 78.4", "+28% volume expansion", etc.) and titles "SELL SIGNAL"/"BUY SIGNAL" (`src/app/ml/alerts/service.py:58-116`). Injected because `app.py:86` builds `AlertService(seed_defaults=True)`. Confirmed.
- Frontend: 3 literal notification objects in `NotificationDrawer.tsx:30-58` ("IT sector weighting has drifted +3.8%", "Annualized volatility spiked to 19.2%"). Confirmed.
- Push never sends: `_dispatch_push` (`service.py:186-201`) only appends to `_push_dispatch_log`; no push library imported anywhere. `DEFAULT_VAPID_PRIVATE_KEY = "dummy_private_key_for_offline_resilient_testing"`. `/notifications/test-push` replies `{"status":"dispatched","dispatched":true}`. Confirmed.

TIGHTEN: the frontend's 3 seeds are **initial component state**, overwritten by the backend's list once the drawer opens and `/api/alerts` returns a non-empty array (`NotificationDrawer.tsx:69-71`). In production the backend always has ≥4 seeds, so the frontend fakes are transient on first paint. They do still show when the backend returns empty (e.g. after `DELETE /alerts`) and before the first fetch resolves. The "shown even when the backend has nothing to say" claim is accurate in those cases.

---

## Finding 4 — Review fact-checker grades against a hardcoded table; multiplies portfolio returns by 100 twice → **AGREE**

Evidence checked:
- Hardcoded rate tables: `agent.py:58-67` (persona baskets), `:71` (strategy flat 14.5), `:91-100` (per-symbol), `:103` (platform 13.2). Confirmed. (`STOCK` target does have a real computation path via `market_service.get_history` before falling back to the table — `:74-89`.)
- Double multiply: `agent.py:51` does `round(port.total_pnl_pct * 100, 2)`, but `total_pnl_pct` is already a percentage — `(total_current_val / initial_capital - 1) * 100` at `src/app/ml/simulation/portfolio.py:179-180`. A 10% portfolio reports 1000%. Confirmed.
- Consequence: portfolio reviews get a ground truth ~100× the claim → rejected as false claims. Confirmed by `verify_review` flow (`agent.py:131-144`).

---

## Finding 5 — No auth; cross-tenant read/delete → **AGREE**

Evidence checked:
- `GET /portfolios` returns every row (`src/app/data/storage.py:425-429`); `DELETE /portfolios/{id}` deletes by ID with no owner check (`src/app/api/routes/portfolio.py:103-123`); `POST /portfolio/{id}/rebalance/apply` mutates. Confirmed.
- No `user_id` anywhere in the portfolio schema; the only `user_id` field in the codebase is on `PushSubscriptionRequest` (`src/app/core/models.py:792`). Confirmed.
- CORS `allow_origins=["*"]` with `allow_credentials=True` (`src/app/api/app.py:57-61`). Note: that combination is spec-invalid (browsers reject wildcard + credentials); a separate latent bug, but confirms no origin gating.

---

## Finding 6 — 9 frontend call sites bypass `apiUrl()` → **CORRECT (it's 10)**

Evidence checked (raw relative paths, no `apiUrl` wrap):
1. `GrowPage.tsx:53` — `/api/v1/grow/recommend` (in `request(...)`)
2. `PortfolioPage.tsx:132` — `/api/portfolio/compounding` (in `request(...)`)
3. `NitiBotModal.tsx:46` — `/api/chat/status` (raw `fetch`)
4. `NitiBotModal.tsx:81` — `/api/chat` (in `request(...)`)
5. `NotificationDrawer.tsx:69` — `/api/alerts` (in `request(...)`)
6. `RegimeRadar.tsx:20` — `/api/regime/current`
7. `RegimeRadar.tsx:26` — `/api/v1/regime/current`
8. `LearningHub.tsx:29` — `/api/v1/literacy/all`
9. `marketStream.ts:26` — `/api/v1/stream/ticks` (singleton default endpoint)
10. **`TopRecommendations.tsx:21` — `/api/v1/stocks/explore` (in `request(...)`) — NOT in the audit's list.**

The audit counted 9; the actual count is **10**. Consequence in the APK: additionally, Home's "Top Regime Picks" card silently falls back to its 4 hard-coded sample stocks (`TopRecommendations.tsx:29-34`).

Root cause is structural: `useAbortableRequest.request` passes `input` straight to `fetch` without applying `apiUrl` (`src/frontend/hooks/useAbortableRequest.ts:55`), so correctness depends on every caller remembering to wrap. A CI grep (`apiUrl(` vs raw `"/api`) is the right guard, but the count must be 10.

---

## Finding 9 (SQLite WAL) + Finding 8 (blocking async) + Finding 7 (portfolio create/delete/rebalance) + Finding 10 (no CI tests) + Finding 14 (lightgbm) → **AGREE**

Spot checks:
- WAL: `journal_mode` appears nowhere in `src/`; `PortfolioRepository.__init__` sets only `PRAGMA foreign_keys=ON` (`src/app/data/storage.py:196-201`). Confirmed. And `PortfolioService.get_portfolio` calls `repository.save_portfolio(updated)` on every GET (`src/app/ml/simulation/service.py:136`) — a read endpoint that writes. Confirmed.
- Blocking async: handlers in `portfolio.py`, `grow.py`, `backtest.py`, `chat.py` are `async def` and call synchronous services doing Yahoo I/O. Confirmed (grep). `market.py`/`explore.py` already use plain `def` — the audit's "copy that" advice is valid.
- Portfolio CRUD from UI: `handleCreatePortfolio` builds from `DEMO_HOLDINGS` and only `setPortfolios` (no POST); `handleDeleteActivePortfolio` only filters local state; `handleApplyRebalance` does `setTimeout(600)` then clears a field (`PortfolioPage.tsx:165-262`). `PortfolioState` has no `rebalance_alert` field (`src/app/core/models.py:500-518`), so `RebalanceBanner` can never render. Confirmed.
- No CI tests: 3 workflows (`deploy.yml`, `docker-build.yml`, `build-apk.yml`); none runs `pytest`/`vitest`; `docker-build.yml` paths exclude `tests/**`. Confirmed. Backend test count: **270** functions (166 unit + 104 integration) vs README's "272" (off by 2); frontend: **132** `it()/test()` calls in **31** files (matches README exactly). Confirmed by re-counting.
- lightgbm: zero references in `src/`, `tests/`, `scripts/` (only `pyproject.toml`, `uv.lock`, a `.tmp` probe, and docs). It is a runtime dependency (`pyproject.toml:13`). `google-genai` is in the `[ai]` extra and the Dockerfile installs `".[ai]"` — consistent with the audit. Confirmed.

---

## Findings 11, 13, 15, 16, 19, 20 → **AGREE (with one CORRECT on 16)**

- 11 (alert triggers): enum is `REGIME_TRANSITION/PORTFOLIO_DRIFT/RSI_EXTREME/DRAWDOWN_BREACH/WEEK_52_HIGH/FACTOR_ANOMALY` (`src/app/core/models.py:740-745`) — not the README's six. Drawdown breach can never fire: `portfolio.max_drawdown_pct` is `0.0` in every `PortfolioState` and is assigned nowhere in `src/` (only in backtest metrics). `POST /alerts/evaluate` is called by no frontend code. Confirmed.
- 13 (duplicated domain rules): persona limits `Conservative -4.5 / Balanced -7.5 / Aggressive -14.0` in `growth_calculator.py:34-38` vs `0.08/0.12/0.18` in `evaluator.py:131-134` vs ADR-0016's `3%/7%/12%`. FD rate as `7.0*days/365` (`growth_calculator.py:244`, `simulation/portfolio.py:194`) vs `BANK_FD_ANNUAL_RATE = 0.07` (`compounding_engine.py:23`). Confirmed.
- 15 (non-hermetic tests): 12 modules build `MarketDataService()` with no provider override (counts verified: 13 total call sites, incl. 4 in `test_multi_asset_universe.py`); default repository path is `data/quantniti.db`. Confirmed.
- 16 (tracked binaries): **CORRECT** — `graphify-out/` is already in `.gitignore` and is **not tracked** (verified: `git ls-files | grep graphify-out` returns nothing). The audit's "6.4 MB tracked" claim for `graph.json`/`graph.html` is a **false positive**. What IS tracked: `src/app/static/QuantNiti-debug.apk` (5.7 MB) and `.agents/` (574 files). 29 PDFs under `docs/` are also tracked. Fix-phase should drop the graphify-out untrack step (nothing to untrack) and keep the APK + `.agents/` + PDF actions.
- 19 (dead code / duplicate routes / filter tabs): `PortfolioSimulator` is defined and only used by `tests/unit/test_portfolio_simulator.py`; every router mounted twice under `/api` and `/api/v1` (`app.py:164-181`); `NotificationDrawer` filter tabs `["All","Regime","Drift","Technicals","Risk"]` vs backend types `REGIME_TRANSITION/PORTFOLIO_DRIFT/RSI_EXTREME/DRAWDOWN_BREACH/WEEK_52_HIGH/FACTOR_ANOMALY` → "Technicals"/"Risk" match nothing. Confirmed.
- 20 (field mismatch + junk): `AdaptiveHomeCard.tsx:17` reads `activePortfolio.day_pnl` (backend field is `pnl_1d`) → falls back to `420.5`; root junk files `start_all.py`, `test_script.py`, `review2_slides_dump.txt`, `temp_pages_12_26.txt` all present. Confirmed.

---

## Corrections the fix phase must account for

1. **Bypass count is 10, not 9** — add `TopRecommendations.tsx:21` to the fix list (and its 4-stock hardcoded fallback on error).
2. **Quote fallback lives in the service layer** — fix `MarketDataService.get_latest_quote` (not `fetch_quote`) to cache + return stale; the provider change is the fast_info→history chain.
3. **SSE is seeded by a real quote before it drifts** — "delete or relabel" still applies, but the fix should account for the seed path (`_get_base_price`) so a relabelled "simulated" mode keeps working offline.
4. **graphify-out is already gitignored** — drop the untrack step for it; keep APK + `.agents/` + PDFs.
5. **Frontend alert seeds are initial state, not always shown** — deleting them is still right, but the fix should ensure the drawer renders an empty state (not a flash of fakes) when the backend returns nothing.
6. **Double-multiply fix is portfolio-only** — `agent.py:51` is the only `* 100` on an already-percentage field; the basket/strategy/stock paths use already-scaled percentages and are not double-multiplied (they're wrong for a different reason: hardcoded tables).
7. **README test counts**: backend is 270 (not 272); frontend 132/31 is exact. Coverage badge has no enforcing job — delete or wire to CI.
8. **CORS wildcard + credentials** is spec-invalid; if auth (finding 5) is added, `allow_origins` must become an explicit list at the same time.

## Verdict

The audit's top findings are **substantially correct** — every one of the 10 requested items AGREEs on substance. Two need correction (bypass count 9→10; graphify-out not tracked), and several need tightening (quote-fallback attribution, SSE seeding, frontend alert-seed lifecycle, push non-delivery). No false positives beyond the graphify-out tracking claim. The audit's overall verdict stands: the quant engine is real, but the product layer over it is a facade, and the worst defects are the ones where a user is shown a number that is not true (random-walk "live" prices, typed-in alerts, table-graded reviews, 1000% portfolio returns). Fix 1, 2, 3, 4, 5, 6 first.
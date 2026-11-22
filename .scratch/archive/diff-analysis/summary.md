# Repository Change Summary — `581890f1` → `a8f8177` (HEAD)

**Range:** `581890f1adea7cae33b1b22f035041fd98ce2b63` (2026-11-11 23:53) → `a8f8177`
**Commits:** 24
**Raw diff:** ~21,198 insertions / 1,880 deletions across 173 source files.
**Filtered diff** (excluding `graphify-out/**`, images, PDFs, `dist/**`, lockfiles): **20,789 insertions / 1,885 deletions**.
**Source-only** (`src/frontend` + `src/app`): 84 files — **11,539 insertions / 513 deletions**; 49 new files, 35 modified.

Two feature waves landed in this window, plus a backend hardening wave:

| Wave | Scope | Commits |
|---|---|---|
| `sota-integration` (tickets 01–06) | Adaptive responsive workstation, statutory charges, pure rebalancer, Belltalon export, CurrencyInput, mobile fixes | `cf9fae9`, `b4ea181`, `4d623e4`, `266ba53` |
| `belltalon-workstation-upgrades` (tickets 01–07) | Order ticket + tax preview, backtest comparison studio, watchlists, IST clock, quote cache, shortcuts/⌘K, exact decimals | `d5c8fa9` … `fa6158f`, `f9d2d61` |
| `belltalon-backend` (tickets 01–06) | Markov regimes, 3-tier exits, risk guard, idempotent ledger, quote hub/WebSocket, broker OAuth | `a8f8177` (single integration commit) |

Notable: the backend wave shipped as **one squash-style commit** (`a8f8177`) with no intermediate ticket commits; the frontend waves were TDD-style ticket branches merged individually.

---

## 1. Frontend workstation features (`src/frontend/`)

36 new files, 21 modified; 11.5k insertions. Roughly all of it is new capability rather than refactor, except `NitiBotModal.tsx` which was split (−219 lines) into `NitiBotChat.tsx` (+223).

### 1.1 Order ticket + statutory tax preview

| File | Lines | Purpose |
|---|---|---|
| `components/modals/OrderTicketDrawer.tsx` | 963 | Slide-over manual order ticket: 5-phase state machine (`edit → review → submitting → placed → lost`), Beginner/Advanced modes, PAPER/LIVE toggle, `MARKET/LIMIT/SL/SL-M`, `DAY/IOC`, 0.05 tick-size validation, paper-portfolio cash/holdings mutation, `sessionStorage` persistence of in-flight orders with an idempotency key, 1-click Belltalon/Zerodha export |
| `utils/taxCalculator.ts` | 151 | Indian statutory charge engine: CNC/MIS/NRML, STT (0.1% both legs delivery; 0.025% sell-only intraday; 0.02% futures sell; 0.1% options sell), NSE 0.00297%, SEBI 0.0001%, stamp duty 0.015% buy-only, GST 18% on (brokerage + exchange + SEBI), breakeven points/price, net proceeds or cost |
| `components/trading/StatutoryTaxBreakdown.tsx` | 148 | Presentational itemized charge table (turnover, brokerage, STT, exchange, SEBI, stamp, GST, total, breakeven) |

Wiring: `ModalRoot.tsx` gained three new modal entries (`commandPalette`, `shortcuts`, `orderTicket`), with `modalPayload` passed as `initialSide/initialSymbol/initialProduct/initialPrice/initialQuantity`.

### 1.2 Backtest comparison studio

| File | Lines | Purpose |
|---|---|---|
| `components/explore/BacktestComparisonStudio.tsx` | 455 | Multi-run comparison studio (up to 4 runs) with preset demo runs, URL-param driven run selection, beginner takeaway card, share/export |
| `components/explore/ComparisonMetricsTable.tsx` | 394 | Side-by-side metrics vs a reference run; flags differing input parameters; emerald "winner" badges with higher-better/lower-better semantics |
| `components/explore/OverlaidEquityChart.tsx` | 319 | Overlaid equity curves normalized to % return from 0% |
| `utils/lttb.ts` | 87 | Largest-Triangle-Three-Buckets downsampling (deterministic, O(N)) for 60fps charts |
| `pages/BacktestComparisonPage.tsx` | 12 | Route wrapper for `/backtest/compare` |

`ProToolsBacktester.tsx` +246 lines to launch the comparison flow; `AppShell.tsx` registers the new route.

### 1.3 Multi-list watchlists

| File | Lines | Purpose |
|---|---|---|
| `store/useWatchlistStore.ts` | 283 | Zustand store: create/rename/duplicate/delete lists, add/remove symbols, `MAX_WATCHLISTS = 10`, `MAX_SYMBOLS_PER_LIST = 50`, localStorage keys `quantniti_watchlists` / `quantniti_active_watchlist_id`, pre-seeded system lists |
| `components/markets/WatchlistRail.tsx` | 324 | Compact list manager rail (inline create/rename/delete, per-symbol rows) |
| `components/markets/WatchlistStar.tsx` | 61 | Universal bookmark toggle used from cards/modals |
| `components/explore/WatchlistWorkstation.tsx` | 376 | 3-pane surveillance view (lists → table → preview) with filter and profile modal |
| `data/quoteDirectory.ts` | 385 | Static quote directory (`StockQuote` incl. `regime_suitability_score`, `regime_badge`, 6-month bull/base/bear growth) used by watchlists |

`ExplorePage.tsx` (−172 net, restructured) now renders `WatchlistWorkstation`; `StockCard.tsx` / `StockProfileModal.tsx` gained star integration.

### 1.4 IST clock & market session

| File | Lines | Purpose |
|---|---|---|
| `utils/marketSession.ts` | 172 | Pure session model: IST offset 330 min, Mon–Fri 09:15–15:30 IST, `marketSession()`, `barCloseIn()` anchored to 09:15, `formatBarCountdown`, `formatIstTime`, `formatSessionCountdown` ("Closes in 2h 14m" / "Opens Monday 09:15 IST") |
| `hooks/useNow.ts` | 61 | Single shared 1-second clock via `useSyncExternalStore` with ref-counted interval start/stop and `setSharedNow()` test seam |
| `components/ui/IstClock.tsx` | 47 | Monospace IST wall clock |
| `components/ui/SessionStatusBadge.tsx` | 55 | Open/closed session badge with countdown |
| `components/ui/BarCountdown.tsx` | 59 | Candle-close MM:SS countdown |

Rendered in `Header.tsx` (badge + clock) and in a new desktop-only `workstation-footer` in `AppShell.tsx`.

### 1.5 Quote cache + freshness

| File | Lines | Purpose |
|---|---|---|
| `services/quoteCache.ts` | 320 | Singleton cache outside React: per-symbol reference counting (0→1 fetch snapshot, 1→0 stop), per-symbol listener sets (cell-level isolation), snapshot + delta reconciliation, sequence-gap detection → `resyncing`, `/api/v1/market/quote` fallback, 5-state freshness (`live`/`snapshot`/`resyncing`/`stale`/`closed`) with 10s staleness threshold; `useLiveQuote()` hook |
| `components/quotes/LivePrice.tsx` | 108 | Flash-on-tick price cell bound to `useLiveQuote` |
| `components/quotes/ProvenanceTag.tsx` | 48 | Source/freshness chip ("NSE Live Tick", "NSE Closed", snapshot, stale) |
| `components/quotes/RelativeFreshnessBadge.tsx` | 84 | "Updated 3s ago"-style relative freshness |

### 1.6 Keyboard shortcuts & ⌘K palette

| File | Lines | Purpose |
|---|---|---|
| `hooks/useHotkey.ts` | 150 | Hotkey engine: `mod+k` / `mod+d` parsing, `enabled` and `allowInInputs` options, ignores inputs by default |
| `components/modals/CommandPaletteModal.tsx` | 590 | ⌘K/Ctrl+K palette: navigation + quick actions, fuzzy symbol search over a 16-name `STOCK_UNIVERSE`, recent searches persisted to `quantniti_recent_searches`, theme toggle, dialog a11y |
| `components/modals/KeyboardShortcutsModal.tsx` | 172 | Cheat-sheet modal |

`AppShell.tsx` (+175/−~50) binds: `1–5` tabs, `mod+k` palette, `b`/`s` order ticket BUY/SELL, `mod+d` theme, `?` shortcuts, `Escape` close. `Header.tsx` gained a search button.

### 1.7 Exact-decimal money primitives

| File | Lines | Purpose |
|---|---|---|
| `utils/decimal.ts` | 126 | `big.js` wrapper with `Big.RM = Big.roundHalfUp`; `tryDecimal` / `toDecimal` (null-safe, never throws), `formatIndianNumber` (lakh/crore grouping), `formatIndianCurrency` (₹, compact Cr/L/k) |
| `components/trading/Money.tsx` | 47 | Monochrome tabular-nums currency, falls back to `MissingValue` |
| `components/trading/Price.tsx` | 42 | Strict 2-decimal price |
| `components/trading/Pnl.tsx` | 101 | Signed P&L (value + %) with semantic color |
| `components/trading/MissingValue.tsx` | 26 | Explicit "—" placeholder with reason tooltip |
| `components/ui/CurrencyInput.tsx` | 142 | Bounded numeric currency input with quick-add chips (`+10K`, `+50K`, …) and validation |
| `index.ts` barrels | 15 + 5 | Public exports for `trading/`, `quotes/`, `ui/` |

`package.json` adds `big.js ^7.0.1` and `@types/big.js ^7.0.0`. `HoldingsTable.tsx` (+166) now uses `Money`/`Price`/`Pnl` in both desktop table and new mobile stacked cards.

### 1.8 Desktop cockpit / adaptive layout

| File | Lines | Purpose |
|---|---|---|
| `components/layout/DesktopCommandPane.tsx` | 157 | Left rail: portfolio KPI cards, `RegimeRadar`, `WatchlistRail`, Belltalon export button |
| `components/layout/DesktopCopilotPane.tsx` | 70 | Right docked NitiBot pane |
| `components/modals/NitiBotChat.tsx` | 223 | Chat body extracted from `NitiBotModal` for reuse in dock + modal |
| `index.css` | +8 | Layout/token tweaks |

`AppShell.tsx`: container goes `max-w-[520px]` → `lg:max-w-7xl`, adds 3-pane flex layout, desktop status footer, and `BottomNav` is suppressed at `lg`. `BottomNav.tsx`, `MarketPulse.tsx`, `PortfolioHeroCard.tsx`, `GrowPage.tsx` got responsive/mobile fixes.

---

## 2. Backend / ML engine (`src/app/`)

13 new files, 14 modified.

### 2.1 Markov regimes

| File | Lines | Purpose |
|---|---|---|
| `ml/regime/markov.py` | 140 (new) | `MarkovRegimeModel`: 3-state chain over `MarketRegimeType`, empirical + Laplace-smoothed (`alpha=1.0`) transition matrices, forward 15/30-day projection, stability score, Shannon entropy |
| `ml/regime/service.py` | +225 | `get_regime_transitions(horizon_days)` and `simulate_regime_shift(...)` — what-if portfolio restructuring with asset-class shifts, turnover, statutory charges, drawdown reduction, trust card |
| `api/routes/regime.py` | +38 | `GET /regime/transitions`, `POST /regime/simulate` |

### 2.2 3-tier exit engine

| File | Lines | Purpose |
|---|---|---|
| `ml/portfolio/exit_engine.py` | 314 (new) | `PortfolioExitEngine` — Tier 1 regime-shift rotation out of cyclical sectors, Tier 2 HWM trailing stop, Tier 3 momentum exhaustion (RSI-14 > 75 or \|z\| > 2.0); emits `ExitRecommendationCard` with statutory deductions, net proceeds, and 1-click `ExitExecutionPayload`; full and partial liquidation |
| `ml/alerts/trailing_stop.py` | 164 (new) | `DynamicHighWaterMarkTracker`: `HWM_t = max(HWM_{t-1}, P_t)`, persona stops (Conservative 2%, Balanced 3%, Aggressive 4%, ESG 3%), breach → `SmartAlert` |

### 2.3 Risk guard

| File | Lines | Purpose |
|---|---|---|
| `ml/portfolio/risk_guard.py` | 293 (new) | `PreTradeRiskManager`: per-portfolio `RLock` serialization, persona concentration caps (15/25/35/25%), 5% minimum cash buffer, reduce-only oversell checks, bear-regime drawdown circuit breaker (3%) blocking equity buys while allowing gold/defensive and sells; `RiskViolationException` (HTTP 409) |

`api/app.py` registers a dedicated handler emitting the flat 409 envelope (`violated_limit`, `limit_value`, `requested_value`, `suggested_action`, `detail`).

### 2.4 Idempotent order ledger

| File | Lines | Purpose |
|---|---|---|
| `ml/simulation/execution_ledger.py` | 219 (new) | `OrderIntentState` machine (`Submitting → Submitted → Filled/Rejected`, or `Uncertain`), deterministic tag `QN + SHA256(intent_key)[:18]`, two-phase pre-commit before out-of-transaction broker dispatch, timeout → `Uncertain` (never blind retry), startup sweep, `PaperExecutionAdapter`, tag-based reconciler |

### 2.5 Quote hub / WebSocket

| File | Lines | Purpose |
|---|---|---|
| `realtime/hub.py` | 380 (new) | `QuoteHub`: channels `quotes`/`portfolio`/`regime`/`alerts`, token reference counting (0→1 subscribe, 1→0 unsubscribe), 5 Hz (200 ms) tick coalescing with latest-wins, connection tracking, `register`/`unregister`/`handle_message`/`stream_ticks` |
| `realtime/source.py` | 178 (new) | `DualModeMarketAdapter`: Zerodha KiteTicker when connected, else calibrated micro-Brownian synthetic during session and steady last-close off-market; auto-fallback on failure |

`api/app.py` adds `/ws`, `/api/v1/ws`, `/api/ws` gateways plus startup (sweep dangling intents, start hub) and shutdown hooks. `api/routes/stream.py` now prefers `quote_hub.stream_ticks` and falls back to the legacy generator.

### 2.6 Broker OAuth

| File | Lines | Purpose |
|---|---|---|
| `api/routes/broker.py` | 373 (new) | `POST /broker/login-url` (HMAC-signed single-use state), `GET /broker/callback` (state verify + `request_token` exchange + encrypted credential storage), `GET /broker/holdings` (Demat → `PortfolioHolding`, snapshot fallback on expired token), `POST /broker/disconnect` |
| `core/security.py` | 226 (new) | AES-256-GCM encrypt/decrypt with 12-byte nonces, `ENCRYPTION_MASTER_KEY` parsing (64-hex or base64-32), HMAC-SHA256 state sign/verify, daily 06:00 IST token expiry calculation |

### 2.7 Portfolio / rebalancing / export / charges

| File | Lines | Purpose |
|---|---|---|
| `api/routes/portfolio.py` | +121 | `POST /validate-rebalance` (risk check, 409), `GET /{id}/export/belltalon`, `GET /{id}/exit-recommendations`, `POST /execute-exit` |
| `ml/portfolio/rebalancer.py` | 164 (new) | Pure `evaluate_rebalance()` — no IO/clock: discrete integer shares, statutory charges, drift reduction → `BrokerOrderSheet` |
| `ml/portfolio/belltalon_exporter.py` | 158 (new) | Pure `export_portfolio_to_belltalon()` → Belltalon v1 `StrategyDefinition` JSON, regime-conditioned exit tuning |
| `ml/simulation/charges.py` | 123 (new) | `Decimal`-based delivery charges, `ROUND_HALF_EVEN` to paise: STT 0.1%, NSE 0.00345%, SEBI 0.0001%, stamp 0.015% buy, GST 18% |
| `ml/simulation/service.py` | +92 | Applies risk guard + ledger to rebalance application; `include_charges` plumbing |
| `ml/portfolio/compounding_engine.py` | +172 | Optional `include_charges` drag for lump-sum, monthly SIP, and step-up SIP projections; returns `total_charges` |
| `ml/portfolio/service.py`, `ml/alerts/service.py`, `ml/portfolio/__init__.py` | small | Wiring/exports |

---

## 3. Data / model / config changes

| File | Change |
|---|---|
| `src/app/core/models.py` (+123) | New Pydantic models: `RegimeTransitionsResponse`, `SimulateRegimeShiftRequest`, `AssetClassShift`, `RegimeShiftHoldingItem`, `RegimeShiftSimulationResponse`; `RiskViolationDetail`; exit family `ExitTierType`, `ExitExecutionPayload`, `ExitRecommendationCard`, `ExecuteExitRequest`; `include_charges` / `total_charges` fields on compounding and rebalance models |
| `src/app/data/storage.py` (+317) | Three new SQLAlchemy tables — `OrderIntentRecord` (PK `intent_key`, indexed `idempotency_key` + `tag`, state, symbol/side/qty/price/charges, broker_order_id), `BrokerAccountRecord` (encrypted key/secret/access/public tokens, expiry, OAuth state hash), `BrokerSnapshotRecord` (JSON snapshots); repository methods `save/get/get_by_idempotency/list/update_state/sweep_submitting_intents`, `save/get/delete_broker_account`, `save/get_latest_broker_snapshot`, `sweep_expired_broker_tokens` |
| `src/app/api/app.py` (+77) | Registers `broker_router`, 409 risk handler, WebSocket gateways, startup/shutdown lifecycle, QuoteHub construction (synthetic `DualModeMarketAdapter` default), injects `portfolio_service`/`grow_service` into `RegimeService` |
| `src/app/core/security.py` (+226, new) | AES-256-GCM vault + HMAC state + IST token expiry (see §2.6) |
| `package.json` | `big.js`, `@types/big.js` |
| `vite.config.ts` | Vitest `include` now also matches `src/**/*.{test,spec}.*` |
| `.gitignore` | Adds `.tmp/` (reference clones) |
| `.opencode/opencode.json`, `.opencode/plugins/graphify.js` | Tooling/plugin updates |
| `src/app/static/sw.js` | Service-worker cache version bump |
| `docs/` | Deletions only: academic sample text, PDFs, review snapshots (repo slimming) |

---

## 4. Tests added

**31 new test files** (22 frontend Vitest, 9 backend pytest) plus 13 modified.

### Frontend (Vitest)

| Test file | Covers |
|---|---|
| `unit/taxCalculator.test.ts` | Charge math per product/side, breakeven, edge/zero inputs |
| `unit/statutoryVerification.test.ts` | Independent statutory benchmark parity (Zerodha/NSE schedules) |
| `unit/utils/decimal.test.ts` | `tryDecimal`/`toDecimal` safety, lakh/crore formatting, compact units |
| `unit/components/trading/ValuePrimitives.test.tsx` | `Money`/`Price`/`Pnl`/`MissingValue` rendering + tabular-nums + a11y labels |
| `unit/components/trading/StatutoryTaxBreakdown.test.tsx` | Itemized breakdown rendering |
| `unit/OrderTicketDrawer.test.tsx` | Dialog a11y, Beginner/Advanced toggle, 0.05 tick validation, 4-phase transitions, paper cash/holdings mutation, sessionStorage + idempotency key |
| `unit/BacktestComparison.test.tsx` | LTTB downsampling (identity, exact threshold, peak retention), metrics table winners/diffs, normalized overlay |
| `unit/marketSession.test.ts` | IST parts, session open/close boundaries, Fri/weekend rollover, `barCloseIn`, all formatters |
| `unit/components/IstClock.test.tsx` | Clock render/tick behavior |
| `unit/quoteCache.test.ts` | Ref counting, per-symbol isolation, snapshot+delta, sequence-gap resync, reconnect resync, 5-state freshness, `useLiveQuote` mount/unmount |
| `unit/quotes/QuoteComponents.test.tsx` | `LivePrice`, `ProvenanceTag`, `RelativeFreshnessBadge` |
| `unit/useHotkey.test.ts` | Parsing, mod combos, input suppression, `allowInInputs`, cleanup |
| `unit/CommandPaletteModal.test.tsx` | Search/commands/recent searches/keyboard nav |
| `unit/KeyboardShortcutsModal.test.tsx` | Cheat-sheet content + close |
| `unit/WorkstationShortcuts.test.tsx` | Global bindings wired through `AppShell` |
| `unit/AppShellResponsive.test.tsx` | Desktop 3-pane vs mobile layout |
| `unit/useWatchlistStore.test.ts` | CRUD, limits (10 lists / 50 symbols), persistence, active list |
| `unit/WatchlistRail.test.tsx`, `WatchlistStar.test.tsx`, `WatchlistWorkstation.test.tsx` | Rail CRUD, star toggle, 3-pane view |
| `unit/CurrencyInput.test.tsx` | Bounds, chips, invalid input |
| `portfolio/HoldingsTableMobile.test.tsx` | Mobile stacked holding cards |

Modified: `AppShell`, `BottomNav`, `Header`, `HomePage`, `GrowWizard`, `OnboardingIntegration`, `asyncLifecycleIntegration`, `FullAppIntegration`, `DemoPortfolio`, `HoldingsTable`, `PortfolioPage`, `setup.ts`.

### Backend (pytest)

| Test file | Tests | Covers |
|---|---|---|
| `unit/test_risk_guard.py` | 16 | Persona concentration caps, reduce-only oversell, 5% cash buffer, bear circuit breaker (blocks equity buys, allows gold/sells), bull pass-through, per-portfolio locking, order-sheet + alert integration, service-level enforcement, API 409 |
| `unit/test_execution_ledger.py` | 9 | Tag formula/determinism, pre-commit before dispatch, non-blocking dispatch, timeout → `Uncertain`, startup sweep, idempotency dedupe, uncertain→filled reconcile, rebalance integration, API idempotency header |
| `unit/test_exit_engine.py` | 11 | HWM ratchet, persona stop thresholds 2/3/4%, breach detection, all 3 tiers, statutory deductions/net proceeds, full + partial liquidation |
| `unit/test_broker_oauth.py` | 17 | AES-GCM roundtrip/uniqueness/tamper/bad keys, HMAC sign/verify/tamper/expiry, 06:00 IST expiry calc, token sweep, login-url, callback exchange, holdings mapping, expired-token snapshot fallback, disconnect |
| `unit/test_markov_regime.py` | 6 | Row-stochastic matrices, stability + entropy, service outputs, what-if simulator, API endpoints |
| `unit/test_quote_hub.py` | — | Ref counting, channel multiplexing, 5 Hz coalescing, disconnect cleanup (fake upstream + fake websocket) |
| `unit/test_charges.py` | 10 | Buy/sell ₹1L parity, zero turnover, banker's rounding, numeric types, charge drag on lump-sum/SIP/step-up, schema toggle, projection |
| `unit/test_rebalancer.py` | 4 | Deterministic reallocation, charges included, cash-only, empty input safety |
| `unit/test_belltalon_export.py` | 3 | Strategy JSON structure, validator compliance (if installed), regime exit tuning |
| `integration/test_portfolio_api.py` (modified) | 4 | Full lifecycle, 404s, compounding-with-charges, exit recommendations + execute |

---

## 5. Specs / tickets / docs

All new (no spec edits), under `.scratch/`:

| Path | Content |
|---|---|
| `.scratch/belltalon-workstation-upgrades/spec.md` (130) | Problem/solution + user stories for the 7 workstation tickets |
| `.scratch/belltalon-workstation-upgrades/issues/01..07-*.md` | Ticket specs: comparison view, watchlists, quote cache, order ticket, market session, shortcuts/palette, exact decimals |
| `.scratch/belltalon-workstation-upgrades/COORDINATOR_BRIEF.md` (73) | Run brief |
| `.scratch/belltalon-workstation-upgrades/COORDINATION_REPORT.md` (199) | Final run report: 7/7 tickets merged, Vitest 42 suites/202 tests → **53 suites/295 tests**, clean `tsc && vite build` (5.04 s), graph 15,214 nodes / 53,262 edges |
| `.scratch/belltalon-workstation-upgrades/verification/finance.md` (337) | Independent statutory audit: `big.js` half-up verified, 100% CNC parity with Zerodha; **flags** MIS stamp duty 0.015% vs statutory 0.003%, breakeven double-charge heuristic (±6.75–10.6%), frontend 0.00297% vs backend legacy 0.00345% NSE rate divergence |
| `.scratch/belltalon-workstation-upgrades/verification/ui.md` (140) | Chromium verification at 1440×900 and 375×812; 8 flows; documents a fixed `CommandPaletteModal` unbatched-`onClose` defect; 39 suites/240 tests at time of audit |
| `.scratch/belltalon-workstation-upgrades/verification/screenshots/*.png` (11) | Visual evidence (excluded from diff stats) |
| `.scratch/belltalon-backend/spec.md` (150) + `issues/01..06-*.md` (11 files) | Backend spec and tickets: Markov regimes, WebSocket quote hub, 3-tier exits, Zerodha OAuth, async backtest runner, pre-trade risk, idempotent ledger, trailing-stop GTT |
| `.scratch/sota-integration/spec.md` (93, status: completed) + `issues/01..06-*.md` | Adaptive workstation, statutory charges, pure rebalancer, Belltalon export, CurrencyInput/tabular-nums, mobile fixes, desktop workstation |
| `.scratch/code_review_report.md` (141), `deployment_readiness_report.md` (86), `smoke_test_report.md` (134) | Quality/deploy/smoke audit reports |

**Gap worth noting:** `.scratch/belltalon-backend/issues/03-async-backtest-runner.md` exists, but **no implementation landed** — `src/app/ml/backtest/` and `src/app/api/routes/backtest.py` are unchanged in this range. Backend tickets 01, 02, 03(risk), 04, 05, 06 all have code; the async backtest job queue does not. Similarly, ticket `06-trailing-stop-gtt-engine.md` has the HWM/trailing-stop half (`trailing_stop.py`) but no broker GTT placement endpoint.

`docs/` changes in this range are **deletions only** (academic sample text, reference PDFs, review snapshots) — repo slimming, no new documentation.

---

## TL;DR

- **Frontend became a desktop workstation:** `AppShell` expands from a 520px phone frame to a `lg:max-w-7xl` 3-pane cockpit (command pane + workspace + docked NitiBot) with a session/clock footer, while mobile keeps the PWA layout with new stacked holding cards.
- **Seven workstation tickets shipped:** 963-line order ticket with a real Indian statutory tax engine (STT/GST/SEBI/stamp/exchange), multi-run backtest comparison studio with LTTB downsampling, multi-list watchlists, an IST session state machine, a ref-counted 5-state quote cache, ⌘K palette + hotkey engine, and `big.js` exact-decimal money primitives.
- **Backend gained safety-critical execution plumbing:** a 3-state Markov regime model, 3-tier exit engine with persona HWM trailing stops, pre-trade risk guard (concentration caps, 5% cash buffer, bear circuit breaker, per-portfolio locks → HTTP 409), and a durable idempotent order-intent ledger with deterministic `QN+SHA256[:18]` tags and startup reconciliation sweeps.
- **Realtime + broker connectivity:** an asyncio `QuoteHub` WebSocket gateway (`/ws`) with 4 channels, token ref-counting and 5 Hz tick coalescing over a dual live/synthetic adapter, plus Zerodha Kite OAuth with AES-256-GCM credential encryption and 06:00 IST token expiry.
- **Verification is thorough but flags real issues:** 31 new test files (22 Vitest / 9 pytest) covering every new subsystem; the finance audit found a MIS stamp-duty rate mismatch (0.015% vs 0.003%), a breakeven double-charge heuristic, and a frontend/backend NSE fee divergence — and the backend async backtest runner ticket has **no implementation** in this range.

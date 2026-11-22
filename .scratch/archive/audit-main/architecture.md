# QuantNiti — Senior Developer Audit (whole repo)

Audit date: 2026-11-15. Branch: `feat/main-audit-hardening` @ `581890f`.
Read-only audit. No source file was changed.

## What this repo does:

QuantNiti is a portfolio-advice web app for Indian retail investors. A React 18 + Vite PWA (also shipped as an Android WebView APK) talks to a FastAPI backend that classifies the Indian market into three regimes with a Gaussian mixture model, picks a basket of NIFTY-50 stocks with hierarchical risk parity (HRP), sizes them in whole shares, tracks them as a "virtual paper portfolio" in SQLite, and answers questions with a Gemini-backed chatbot. It also serves a learning hub, a stock-explore tab, a backtester, and a review system with an AI fact-checker.

**Load I assumed:** one small AWS Lightsail instance (1 uvicorn worker, 1 SQLite file, no cache server), reached from the public internet by anonymous visitors — so *many anonymous readers, a handful of portfolio creators, zero auth*. I judged every finding against that: "breaks at the expected load" means "breaks for a real visitor on the real deployment", not "breaks in a 10-user lab".

I ran `npm run build` (passes, 18.3 s). I did **not** run the pytest or vitest suites, per instruction.

---

## Must fix

### 1. Every Explore/Home page load makes 58 uncached network calls, and silently shows fake prices when they fail
- **What this is:** `ExploreService.list_explore_stocks` (`src/app/ml/forecasting/service.py:252`) loops over all 58 universe members and calls `market_service.get_latest_quote()` for each one. The Home tab's `TopRecommendations` hits the same endpoint, so every visit to Home or Explore repeats the whole loop.
- **Problem:** `get_latest_quote` (`src/app/data/service.py:115`) has **no cache at all** — only `get_history` is Parquet-cached. Each call is a live Yahoo Finance request, so a page load is 58 sequential HTTP round-trips (~15–45 s). Worse, when Yahoo rate-limits, `fetch_quote` falls back to `fetch_history` (another request), and if that also fails it falls back to `MockDataProvider` (`src/app/data/provider.py:220`), which returns a *deterministic random walk*. The user sees a price that looks live but is synthetic, with no label saying so.
- **Fix:** Cache quotes the same way history is cached (one Parquet/JSON file per symbol, 5-minute TTL), and return the *last known* quote with a `"stale": true` flag instead of substituting mock prices. That deletes the mock fallback from the live path and removes ~58 requests per page load.
- **If we skip it:** The public demo is slow enough that users bounce, and under any load the app quietly shows invented prices as real ones. That is the worst possible failure for a finance product.

### 2. The "live" market feed is a random number generator, and the UI writes its output over real valuations
- **What this is:** `MarketTickGenerator` (`src/app/data/streaming.py:123`) generates prices with `random.gauss(0.0, 0.0012)` and is mounted in `mode="synthetic"` (`src/app/api/routes/stream.py:20`). The frontend `PortfolioPage` subscribes to that stream and **recomputes** `current_value`, `total_pnl` and every holding's `unrealized_pnl` from the synthetic tick price (`src/frontend/components/portfolio/PortfolioPage.tsx:69-110`).
- **Problem:** The README's "Real-Time SSE Ticks" and CONTEXT's "live mark-to-market" are not what runs. The backend's real mark-to-market (`GET /portfolios/{id}` → yfinance quotes) is never called by the frontend at all, so the synthetic random walk *overwrites* the real numbers the moment the stream connects. Prices only move during 09:15–15:30 IST; outside that the number is frozen, so it looks plausible.
- **Fix:** Either make the stream read from the cached real quote and only simulate when no quote exists (label it "simulated"), or delete the frontend tick→valuation recomputation and let the portfolio page poll the real endpoint. Do not keep both.
- **If we skip it:** The flagship "Live Mark-To-Market" feature shows fabricated prices with real-looking P&L. This is the single biggest credibility risk in the repo.

### 3. Fake alerts with invented numbers are presented to users as quantitative signals
- **What this is:** `AlertService._seed_initial_alerts` (`src/app/ml/alerts/service.py:58-116`) injects four hard-coded alerts at startup: "RSI reached 78.4", "printed fresh 52-week highs with +28% volume expansion", etc. The frontend seeds three more (`src/frontend/components/modals/NotificationDrawer.tsx:30-58`): "IT sector weighting has drifted +3.8%", "Annualized volatility spiked to 19.2%".
- **Problem:** These are not computed from any market data. They are literal strings with literal numbers, shown in a "Smart Alert" panel that CONTEXT.md defines as "an objective quantitative signal with Trust Card context". Two of the backend seeds are titled "SELL SIGNAL" and "BUY SIGNAL", which CONTEXT.md explicitly lists under `_Avoid_: Buy signal, Sell signal`. The frontend's three fakes are shown even when the backend has nothing to say.
- **Fix:** Delete `_seed_initial_alerts` and the frontend's three literal notification objects; start both lists empty and let real evaluations fill them. If a demo dataset is wanted for a presentation, put it in a separate seeded/dev-only code path, never in the production default.
- **If we skip it:** The app tells users "TRENT RSI hit 78.4, consider selling" and "Airtel hit a 52-week high" when no such measurement was made. In a SEBI-regulated domain this is the kind of thing that ends the project.

### 4. The review fact-checker verifies claims against a hard-coded table, and multiplies portfolio returns by 100
- **What this is:** `ReviewVerificationAgent.get_ground_truth_return` (`src/app/ml/reviews/agent.py:56-103`) returns made-up returns for most target types: a lookup table of `{"1M": 1.5, "3M": 4.8, "6M": 12.8, "12M": 19.5}` for Balanced baskets, a flat `14.5` for strategies, and a per-symbol table for stocks.
- **Problem:** CONTEXT.md says reviews are "verified against ground-truth mathematical market returns (within a +/- 3% tolerance window)". They are not — for baskets the "ground truth" is a constant the author typed in, so any user claiming 12.5% on a Balanced 6M basket gets a "verified" badge by matching the table. Separately, line 51 does `round(port.total_pnl_pct * 100, 2)`, but `total_pnl_pct` is already a percentage (`(value/capital - 1) * 100`, `src/app/ml/simulation/portfolio.py:179`). A portfolio up 10% reports 1000% as its "actual return", so every portfolio review is rejected as a false claim.
- **Fix:** Compute the basket/strategy ground truth from the same `GrowService.recommend_basket` growth projections the app already produces, and delete the hard-coded rate tables. Delete the `* 100`.
- **If we skip it:** The "AI-verified" badge on a review means nothing, and the portfolio-review path rejects every truthful reviewer.

### 5. There is no login and no user scoping — any visitor can read and delete every portfolio on the server
- **What this is:** `GET /portfolios` returns every portfolio in the SQLite file (`src/app/data/storage.py:425-429`), `DELETE /portfolios/{id}` deletes by ID with no owner check (`src/app/api/routes/portfolio.py:103-123`), and `POST /portfolio/{id}/rebalance/apply` mutates it. CORS is `allow_origins=["*"]` (`src/app/api/app.py:55-61`). There is no user ID anywhere in the schema.
- **Problem:** The production URL is public. Anyone can `curl https://quantniti.jayadityadev.tech/api/v1/portfolios`, read every user's holdings, and `DELETE` them. A portfolio ID is a random 8-hex string, but it is returned by the list endpoint, so guessing is not needed.
- **Fix:** If multi-user is not in scope yet, add a per-browser `client_id` (a UUID in localStorage, sent as a header) and filter every portfolio query by it — one column, one filter. If it is not in scope at all, say so in the README and put the API behind a shared token. Do not leave it open.
- **If we skip it:** Any visitor can wipe the production database's portfolio table. This is the finding that gets you paged.

### 6. The shipped Android app cannot reach most of its own backend
- **What this is:** The app has an `apiUrl()` helper (`src/frontend/config.ts:22`) that prefixes `VITE_API_URL`. The CI APK build sets `VITE_API_URL=https://quantniti.jayadityadev.tech` (`.github/workflows/build-apk.yml:35`). But **9 call sites skip the helper** and use a raw relative path: `GrowPage.tsx:53` (`/api/v1/grow/recommend`), `PortfolioPage.tsx:132` (`/api/portfolio/compounding`), `NitiBotModal.tsx:46,81` (`/api/chat/status`, `/api/chat`), `NotificationDrawer.tsx:69` (`/api/alerts`), `RegimeRadar.tsx:20,26` (`/api/regime/current`), `LearningHub.tsx:29` (`/api/v1/literacy/all`), `marketStream.ts:26` (`/api/v1/stream/ticks`).
- **Problem:** In the APK those requests go to the app's own local origin, not the server. So in the Android app: the Grow wizard fails, NitiBot is dead, the alert drawer is empty, the regime radar is frozen, the learning hub has no cards, the compounding chart is fake, and the live ticker never connects. Only Explore, reviews, portfolio list and the backtester work.
- **Fix:** Wrap all 9 in `apiUrl(...)`. A lint rule or a grep in CI (`apiUrl\(` vs `"\/api`) will stop it coming back.
- **If we skip it:** The headline "Native Android App" deliverable is broken in its main flows, and the README's APK download link ships it to users.

### 7. Portfolio create, delete and rebalance never reach the server — deleted portfolios come back
- **What this is:** In `PortfolioPage.tsx`: `handleCreatePortfolio` (165-226) builds a portfolio from the hard-coded `DEMO_HOLDINGS` list and only writes it to localStorage; `handleDeleteActivePortfolio` (229-240) removes it from local state only; `handleApplyRebalance` (243-262) does `await new Promise(r => setTimeout(r, 600))` and then clears a field. None of them call `POST /portfolios`, `DELETE /portfolios/{id}`, or `POST /portfolio/{id}/rebalance/apply`.
- **Problem:** Deleting a portfolio only deletes it from the browser. The mount effect (`PortfolioPage.tsx:39-51`) then re-fetches `/api/v1/portfolios` and calls `setPortfolios(data)`, which overwrites localStorage with the server list — **the "deleted" portfolio reappears on the next reload**. The rebalance banner can never show: `RebalanceBanner` renders only when `activePortfolio.rebalance_alert` is set, and `PortfolioState` (`src/app/core/models.py`) has no `rebalance_alert` field at all, so the backend can never send one. The "New Goal" button creates a portfolio from demo data, not from the HRP engine.
- **Fix:** Make the three handlers call the endpoints that already exist and are already tested on the server, then update local state from the response. Delete the `setTimeout(600)` rebalance stub.
- **If we skip it:** Delete does not delete, rebalance does not rebalance, and the regime-shift rebalance feature described in ADR 0003 is unreachable from the UI.

### 8. Blocking network calls inside `async def` routes stall the whole server
- **What this is:** `portfolio.py`, `grow.py`, `backtest.py` and `chat.py` declare their handlers `async def`, but the services they call are plain synchronous functions that do blocking Yahoo Finance I/O: `PortfolioService.get_portfolio` fetches a quote per holding plus the benchmark (`src/app/ml/simulation/service.py:95-121`), and `GrowService.recommend_basket` fetches a quote per selected symbol (`src/app/ml/portfolio/service.py:155`).
- **Problem:** In FastAPI an `async def` handler runs on the event loop; a blocking call inside it stalls **every** other request, including the SSE stream and the health check the container healthcheck polls. One portfolio GET with 8 holdings plus a benchmark is ~10 sequential network calls — tens of seconds of a totally silent server.
- **Fix:** Make those handlers plain `def` (FastAPI then runs them in its threadpool) or wrap the blocking calls in `anyio.to_thread.run_sync`. The `market.py` and `explore.py` routes already use plain `def` — copy that.
- **If we skip it:** One slow visitor freezes the site for everyone, and the Docker healthcheck (30 s interval, 3 retries) will kill a healthy container during a spike.

### 9. SQLite WAL mode is claimed in four documents and is not enabled; every portfolio GET writes to the database
- **What this is:** README, `docs/ARCHITECTURE.md:252`, `docs/HOSTING_AND_SCALABILITY.md:59` and the exhibition document all say "SQLite (WAL Mode)". `PortfolioRepository.__init__` (`src/app/data/storage.py:190-203`) calls `create_engine` and sets only `PRAGMA foreign_keys=ON`. `journal_mode=WAL` appears nowhere in the codebase.
- **Problem:** With the default rollback journal, a writer blocks all readers. And `GET /portfolios/{id}` is not a read: `PortfolioService.get_portfolio` calls `self.repository.save_portfolio(updated)` on every call (`src/app/ml/simulation/service.py:136`), which deletes and re-inserts all holdings and upserts a snapshot. `apply_rebalance` does three of those writes in one request. Two concurrent visitors can exhaust SQLite's busy timeout and get a 500.
- **Fix:** Add `cursor.execute("PRAGMA journal_mode=WAL")` next to the existing pragma. Then move the write in `get_portfolio` behind an explicit refresh (e.g. only write when the price actually changed), so a GET stops writing.
- **If we skip it:** The documented concurrency story is fiction, and a read endpoint mutates the database on every call.

### 10. No CI job runs a single test
- **What this is:** The three workflows are `deploy.yml` (SSH to Lightsail, `docker compose up --build`), `docker-build.yml` (build image, curl the health endpoint) and `build-apk.yml` (build the APK). **None of them runs `pytest` or `vitest`.** `docker-build.yml` even filters on `paths:` that exclude `tests/**`.
- **Problem:** A green badge on the README is decorative. The backend test count in the README is **272**; the repo actually contains **270** test functions (166 unit + 104 integration, no `parametrize`, one test class). The frontend claim of **132 tests across 31 suites is exactly correct** — I counted 132 `it()`/`test()` calls in 31 files. The "99% backend coverage" claim cannot be checked by anything in the repo: there is no coverage config, no coverage report, and no job that runs coverage.
- **Fix:** Add one job to `docker-build.yml`: `uv run pytest tests/ --cov=src/app` and `npm test`, both as required checks. Delete the coverage badge from the README until a real number exists, or make CI produce the badge.
- **If we skip it:** Every regression lands on production first and is found by a user.

---

## Should fix

### 11. Four of the six documented alert triggers do not exist, one can never fire, and the evaluator is never called
- **What this is:** README/CONTEXT/ADR-0016 promise six triggers: Regime Shift, Persona Stop-Loss, Profit Target, Weight Drift, Volatility Breakout, ESG Downgrade. The code implements six different ones (`SmartAlertType`): `REGIME_TRANSITION`, `PORTFOLIO_DRIFT`, `RSI_EXTREME`, `DRAWDOWN_BREACH`, `WEEK_52_HIGH`, `FACTOR_ANOMALY`. There is no profit-target, no stop-loss, no volatility-breakout and no ESG trigger in the enum or the evaluator.
- **Problem:** Worse, the drawdown trigger can never fire: it reads `portfolio.max_drawdown_pct` (`src/app/ml/alerts/evaluator.py:139`), which is `0.0` in every `PortfolioState` and is never assigned anywhere in the codebase. And `POST /alerts/evaluate` is called by **no** frontend code — only by one test — so the whole engine runs at zero times in production.
- **Fix:** Pick one list of six triggers and make the code match it. Set `max_drawdown_pct` when it is computed, and have the alert drawer (or a background task) call `/alerts/evaluate` on a timer. Delete the four trigger names that are not implemented.
- **If we skip it:** The "6-Trigger Smart Alert Engine" is a paragraph in a README, and the only alerts users ever see are the four fake ones from finding 3.

### 12. Web Push never pushes anything, and subscriptions die on restart
- **What this is:** `AlertService._dispatch_push` (`src/app/ml/alerts/service.py:186-201`) appends to `self._push_dispatch_log` and returns. No push library is imported anywhere. `POST /notifications/test-push` replies `{"status": "dispatched", "dispatched": true}`.
- **Problem:** The frontend subscribes a browser (`src/frontend/services/pwaService.ts:102`), the server stores the subscription in an in-memory list, and nothing is ever sent. The endpoint tells the user "Web Push and real-time smart risk guardrails are connected successfully" when no push will ever arrive. Subscriptions are also lost whenever the process restarts, because the list is in memory.
- **Fix:** Either send real pushes (add `pywebpush` and call it in `_dispatch_push`), or remove the Web Push UI, the endpoint, the VAPID key and the README claim. A VAPID key that is not a real key pair (`DEFAULT_VAPID_PRIVATE_KEY = "dummy_private_key_for_offline_resilient_testing"`) cannot sign a push anyway.
- **If we skip it:** The user grants notification permission to a system that will never notify them, and the trust card keeps claiming a delivery channel that does not exist.

### 13. The same domain rule is written three times with three different values
- **What this is:** Persona risk limits live in `src/app/ml/portfolio/growth_calculator.py:34` (`Conservative -4.5, Balanced -7.5, Aggressive -14.0`), in `src/app/ml/alerts/evaluator.py:131` (`0.08 / 0.12 / 0.18`) and in ADR-0016 (`3% / 7% / 12%`). The 7% bank FD benchmark is hard-coded in three files: `growth_calculator.py:244` (`7.0 * days/365`), `compounding_engine.py:23` (`BANK_FD_ANNUAL_RATE = 0.07`), `simulation/portfolio.py:194` (`7.0 * elapsed_days/365`).
- **Problem:** Nothing picks a winner. The drawdown number the user sees on the Trust Card comes from one file, the drawdown number an alert uses comes from another, and the documentation states a third. Changing the FD rate means finding three copies.
- **Fix:** One `constants.py` with `PERSONA_RISK_LIMITS` and `BANK_FD_ANNUAL_RATE`; import it from all three places and correct ADR-0016 to match the code you keep.
- **If we skip it:** A user who reads the docs and compares them with the screen sees three different risk limits and has no idea which one is binding.

### 14. Dependency bloat: one dependency is never used, one belongs in a dev extra, one is not installed by default
- **What this is:** `pyproject.toml` lists `lightgbm>=4.7.0` — **zero references anywhere** in `src/`, `tests/` or `scripts/`. It ships in the Docker image for nothing. `matplotlib>=3.11.2` is used only by `scripts/paper_figures/*.py` (7 files, 610 lines) and one untracked script, but it is a runtime dependency of the production image. `google-genai` is in an `[ai]` extra, so plain `uv sync` does not install it — only the Dockerfile's `pip install ".[ai]"` does.
- **Problem:** `lightgbm` alone adds ~150 MB and a slow compile to every Docker build for zero functionality. `matplotlib` adds ~40 MB of image libraries to a service that never draws a chart server-side (the charts are Chart.js in the browser). A developer who follows the README's `uv sync` gets a backend where NitiBot silently reports "google-genai SDK is not installed".
- **Fix:** Delete `lightgbm`. Move `matplotlib` to a `dev` extra alongside the paper-figure scripts. Either move `google-genai` into the main dependencies or add `uv sync --extra ai` to the README and a startup log line that says NitiBot is off.
- **If we skip it:** Every deploy builds and pushes 200 MB of libraries nobody uses, and the "optional" dependency is optional in exactly the way that breaks the feature.

### 15. The test suite is not hermetic: it hits the real internet and writes into the repo's own database
- **What this is:** 12 test modules build `MarketDataService()` with no provider override (`tests/integration/test_grow_api.py:17`, `test_grow_service.py:18`, `test_backtest_api.py:16`, `test_compounding_api.py:18`, `test_multi_asset_integration.py:129`, `test_multi_portfolio_api.py:18`, `test_portfolio_api.py:18`, `test_portfolio_service.py:23`, `test_backtest_service.py:18`, `tests/unit/test_esg_data.py:40`, `tests/unit/test_multi_asset_universe.py:112`, `tests/unit/test_nitibot_edge_cases.py:109`). The default provider is `YahooFinanceProvider`, i.e. the real Yahoo Finance. Separately, `create_app()` with no `portfolio_service` argument builds `PortfolioRepository()` → `sqlite:///./data/quantniti.db` (`src/app/data/storage.py:182-189`), so every such test writes rows into the repo's own database file.
- **Problem:** The working tree now contains a 594 KB `data/quantniti.db` and 59 Parquet files (6 MB) in `data/cache/` produced by test runs. Tests that assert on portfolio counts share that file across modules, so they are order-dependent. On a machine with no network or a rate-limited Yahoo, the suite either hangs on timeouts or passes for the wrong reason (mock fallback).
- **Fix:** Add a `tests/conftest.py` that (a) injects `MockDataProvider` and a `tmp_path` cache for every fixture, and (b) points `PortfolioRepository` at `sqlite:///:memory:` or a `tmp_path` file by default. One file fixes all 12 modules.
- **If we skip it:** The first time you add a CI test job (finding 10), it will be slow, flaky, and will dirty the repo.

### 16. 23 MB of generated binaries and third-party files are tracked in git
- **What this is:** `src/app/static/QuantNiti-debug.apk` (5.7 MB) is a compiled debug APK committed in the source tree and served to users by `GET /apk`. The binary is dated 2026-10-25, but it was committed on 2026-11-11 in `581890f` — the same commit that changed frontend source — so **the shipped APK does not contain the UI fix from the commit that ships it**. `graphify-out/graph.json` (3.6 MB) + `graph.html` (2.8 MB) are generated artifacts (6.4 MB tracked; 113 MB on disk). `.agents/` is 574 tracked files / 10.9 MB of third-party agent skills that have nothing to do with the product. `docs/pdfs/` and `docs/review/` are ~81 MB of research PDFs and slide exports.
- **Problem:** The tracked APK is stale *and* a binary; the graph is regenerated by `graphify update .` on every agent run, so it churns the diff; the skills directory is 10× the size of the entire backend source (8.7k lines) and will be re-read by every agent and every clone. The build itself also dirties the tree: `npm run build` rewrites the tracked `src/app/static/sw.js` with a new `CACHE_VERSION` timestamp (I reverted that file after running the build), so nobody can build without leaving the repo dirty.
- **Fix:** Add `*.apk`, `graphify-out/graph.json`, `graphify-out/graph.html` and `.agents/` to `.gitignore` and `git rm --cached` them (keep `GRAPH_REPORT.md` and the wiki if you use them). Keep the research PDFs out of git — a 40 MB `docs/pdfs/other-references/` folder does not belong in a source repo.
- **If we skip it:** Every clone pulls 23 MB of generated content, every `graphify update` dirties the tree, and users keep getting a stale APK.

### 17. Five deploy configs for one deployment, and two of them would lose the database
- **What this is:** `Dockerfile` + `docker-compose.yml` + `Caddyfile` (the real Lightsail stack), plus `fly.toml`, `railway.toml`, `render.yaml` and `Procfile` for four platforms that are not used. `fly.toml` sets `auto_stop_machines = "stop"` and `min_machines_running = 0`; `render.yaml` uses `plan: free`; `fly.toml` also targets `iad` while the README says the app lives in `ap-south-1`.
- **Problem:** These are unused configurations for machines nobody maintains — five places to update when a port or env var changes. Worse, `fly.toml` and `render.yaml` would run the container with the SQLite file on the instance's ephemeral disk: Fly stops the machine when idle and the file is gone on the next start, and Render's free plan does the same. The data would be silently gone.
- **Fix:** Delete `fly.toml`, `railway.toml`, `render.yaml` and `Procfile` (or move them to a `deploy/unused/` folder with a note). Keep the Lightsail stack plus a `fly.toml` only if you intend to run it, with a volume mounted on `/app/data`.
- **If we skip it:** The next person wires up "the Fly deploy" from the README-adjacent config and loses every user's portfolio.

### 18. The broker order sheet cannot be imported into Zerodha, and omits every statutory charge
- **What this is:** `generate_broker_order_sheet` (`src/app/ml/simulation/rebalance.py:239`) writes a CSV with the header `Instrument,Exchange,Action,Order Type,Quantity,Price,Product Type`. Zerodha Kite's basket upload expects `tradingsymbol, exchange, transaction_type, order_type, quantity, price, product`. The sheet also carries no STT, brokerage, stamp duty, SEBI turnover fee, DP charge or GST.
- **Problem:** ADR-0003 says the app "generates 100% executable whole-share orders". The CSV is shaped like a broker format but is not one — dropping it into Kite's basket tool fails on the header. The `estimated_total` is gross of every charge, so the sheet tells the user to deploy exactly their capital and then the broker debits more than the capital.
- **Fix:** Use Kite's real column names and transaction-type values (`BUY`/`SELL`), and either add the charge lines or drop the word "order sheet" in favour of "allocation plan". Say which brokers it actually targets in the README.
- **If we skip it:** The one-click broker feature is the trust-building moment in the demo, and it breaks the moment a user tries it.

---

## Nice to have

### 19. Dead code and unreachable UI
- **What this is:** `PortfolioSimulator` (`src/app/ml/simulation/portfolio.py:253-294`) is a class whose two methods just forward to the module-level functions; **only a test uses it**, no production code does. `PortfolioState` has no `rebalance_alert` field, so `RebalanceBanner` can never render. Every router is mounted twice, under `/api` and `/api/v1` (`src/app/api/app.py:165-181`), which is why the frontend has a mix of both prefixes — and it produces duplicate operation IDs in the OpenAPI schema. The notification drawer's filter tabs are `["All", "Regime", "Drift", "Technicals", "Risk"]` (`src/frontend/components/modals/NotificationDrawer.tsx:22`) but the backend's alert types are `REGIME_TRANSITION / PORTFOLIO_DRIFT / RSI_EXTREME / DRAWDOWN_BREACH / WEEK_52_HIGH / FACTOR_ANOMALY`, so "Technicals" and "Risk" match nothing and always show zero results.
- **Problem:** ~40 lines of a class that exists only for a test, a banner that can never show, two of the four filter tabs that are dead, and a doubled route table that makes "which URL do I call?" a question every time.
- **Fix:** Delete the `PortfolioSimulator` class and its test, call the functions directly. Pick one API prefix and drop the other. Fix the two filter labels to `RSI` and `Drawdown` (or whatever the real types are).
- **If we skip it:** None of this breaks anything on its own, but it is exactly the stuff that makes the next person slow.

### 20. Field-name mismatches and repo-root junk
- **What this is:** `AdaptiveHomeCard` reads `activePortfolio.day_pnl` (`src/frontend/components/home/AdaptiveHomeCard.tsx:17`) but the backend field is `pnl_1d` — so the "1D P&L" tile always falls back to a hard-coded **₹420.50**, and "Alpha vs NIFTY" falls back to a hard-coded **2.8%**. `PortfolioPage` never calls `setActivePortfolio`, so that card only updates for users who came through the Grow wizard. At the repo root there are loose files: `start_all.py` (a dev launcher that belongs in `scripts/`), `test_script.py` (a LaTeX scratch file that pytest will try to collect, since it matches `test_*.py`), `review2_slides_dump.txt` (9.5 KB), `temp_pages_12_26.txt` (32 KB).
- **Problem:** A user with a real portfolio sees a fixed ₹420.50 day P&L no matter what the market did. And `pytest` run from the repo root picks up `test_script.py`, which writes a file into `docs/academic_docs/...` as a side effect of collection.
- **Fix:** Rename the field on one side (`day_pnl` → `pnl_1d`) and delete the two fallback constants so a missing value shows `—` instead of a made-up one. Move `start_all.py` into `scripts/`, delete `test_script.py`, and delete the two dump files.
- **If we skip it:** Small money, but the ₹420.50 is another number the app invents, and the stray `test_script.py` will confuse the first person who runs pytest from the root.

---

## Verdict:

Not healthy yet. The quant engine is decent and the test suite is real, but the product layer over it is a facade: the "live" prices are a random walk, the alerts are typed-in strings, the reviews are graded against a table, and the Android app cannot reach half the API. Fix 1, 2, 3, 5 and 6 first — those are the ones where a user is shown a number that is not true.

## Lean:

- ~250 lines of code, -2 runtime dependencies, -23 MB and 577 tracked files.
  - Delete `PortfolioSimulator` and its test: ~127 lines.
  - Delete the four dead deploy configs (`fly.toml`, `railway.toml`, `render.yaml`, `Procfile`): ~45 lines.
  - Delete the 4 hard-coded review rate tables in `reviews/agent.py`: ~25 lines.
  - Delete the loose root files (`test_script.py`, `review2_slides_dump.txt`, `temp_pages_12_26.txt`): ~40 lines.
  - Delete `lightgbm` entirely (unused): -1 dependency, ~150 MB off the image.
  - Move `matplotlib` to a dev extra (only the 610-line paper-figure scripts need it): -1 runtime dependency, ~40 MB off the image.
  - Untrack `*.apk` + `graphify-out/graph.json`/`graph.html` + `.agents/`: -23 MB and 577 tracked files.
  - (Not counted, because it is behaviour not code: the duplicate `/api` + `/api/v1` route mount would remove ~12 route registrations; the fake alert/notification seeds would remove ~60 lines of literal data.)

## Not checked:

- **I did not run the test suites.** `pytest` and `vitest` were out of scope per the task, so I could not verify that the 270 backend / 132 frontend tests currently pass, nor their runtime or flakiness. My test findings come from reading the test sources and from the artefacts left in `data/` by earlier runs, not from a live run.
- **I could not verify the "99% backend coverage" claim** — that needs `pytest --cov`, which I was told not to run. I verified only that no CI job, config or report enforces it, and that the backend test count in the README (272) is 2 higher than the 270 test functions in the tree.
- **I did not run the app or hit the live deployment** at `quantniti.jayadityadev.tech`, so the runtime behaviour of the Lightsail stack, Caddy TLS, the real SQLite file and the real Gemini key is inferred from the code and the deploy configs.
- **I did not build the Android APK** — no Android SDK/Java toolchain here — so the APK-specific breakage in finding 6 is derived from reading `build-apk.yml`, `build_apk.py` and the 9 call sites, not from installing the app.
- **The Docker image was not built.** `lightgbm`'s size and build-time impact are stated from the package's known footprint, not measured on this machine.
- **I did not read** `src/app/ml/backtest/` in full (engine, metrics, service), `src/app/ml/regime/` in full, `src/app/ml/forecasting/forecaster.py`, `src/app/ml/forecasting/factors.py`, `src/app/ml/assistant/context_builder.py`, `src/app/ml/reviews/tier1_filters.py`, `src/app/ml/reviews/tier2_factchecker.py`, `src/app/data/cleaner.py`, `src/app/data/reviews_repo.py` beyond its constructor, `src/app/core/models.py` beyond the models I quote, the 16 ADRs beyond 0003 and 0016, the `android/` Gradle project, `docs/ARCHITECTURE.md`, `docs/HOSTING_AND_SCALABILITY.md`, `docs/ML_PIPELINE.md`, `docs/PRD.md`, `docs/USER_GUIDE.md`, the `graphify-out/` graph contents, and the `.agents/` skill files. The backtest and regime engines are the most likely place for further correctness bugs and deserve a separate pass.

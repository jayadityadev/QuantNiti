# QuantNiti Backend & Security Audit — `src/app/**` + Ops

**Auditor:** dispatched worker (adversarial audit, read-only)
**Date:** 2026-11-15
**Scope:** `src/app/api/**`, `src/app/core/**`, `src/app/data/**`, `src/app/realtime/**`, `src/app/static`, `pyproject.toml`, Dockerfile, docker-compose.yml, Caddyfile, fly.toml, railway.toml, `.github/workflows/*`
**Method:** full read of the listed files + live execution checks (FastAPI `TestClient` with offline `MockDataProvider`, raw SQLite concurrency test, and HTTP probes against the production host). Evidence scripts kept in `.scratch/audit-main/audit_checks_{1,2,3}.py`. Full test suite NOT run (baseline owned by coordinator).

> **Environment note on `src/app/realtime/**`:** the directory contains ONLY `__pycache__/` (compiled `hub.pyc`, `source.pyc`) — no `.py` sources exist. The runtime modules are dead/orphaned bytecode; nothing imports `app.realtime` from any audited file. If these are supposed to be the WebSocket hub, they were deleted without cleaning up (or were never committed). Flagging as a repo-integrity issue, not auditable further.

---

## Executive summary

The API is a **fully open, unauthenticated, global-single-tenant service**: there is no user identity model, no auth, no rate limiting, and all portfolios/alerts/reviews are shared across every visitor. The single worst finding is a **proven arbitrary file read on production** via the SPA fallback route (`/..%2F..%2F..%2F..%2Fpyproject.toml` returns real file bytes on `https://quantniti.jayadityadev.tech` today). Locally it also reads `.env`, which contains a live `GEMINI_API_KEY`. Beyond that: silent fake-data fallback (synthetic prices persisted as if real), a GET that mutates the ledger on every hit, blocking network I/O inside the event loop, and an ephemeral SQLite database in the Docker deployment (data loss on every redeploy).

---

# MUST-FIX

## M1. Arbitrary file read on the SPA fallback route — **exploited on production**

- **Where:** `src/app/api/app.py:194-202` (`serve_spa_fallback`), served from route `/{full_path:path}`.
- **Failure (proven, not theoretical):**
  - Local TestClient: `GET /..%2F..%2F..%2F..%2Fpyproject.toml` → `200`, body begins `[project]\nname = "app"…`. `GET /..%2F..%2F..%2F..%2F.env` → `200`, 684 bytes, contains `GEMINI_API_KEY=…`. `GET /..%2F..%2F..%2F..%2F.git%2Fconfig` → `200`.
  - Production: `curl https://quantniti.jayadityadev.tech/..%2F..%2F..%2F..%2Fpyproject.toml` → `200` with the real file content; `…/..%2F..%2F..%2F..%2FREADME.md` → `200` (14623 bytes). The route does `dist_dir / full_path` with **no normalization/containment check**; uvicorn does not decode-and-reject `%2e%2e`/`%2F`, so any client can walk out of `static/` and read any file the process can read. On dev/bare-runtime deployments (Procfile, `serve_production.py` on a host with a checkout) that includes `.env` (live Gemini key) and the entire `.git` directory.
- **Smallest fix:** resolve and verify containment before serving:
  ```python
  candidate = (dist_dir / full_path).resolve()
  if not str(candidate).startswith(str(dist_dir.resolve()) + os.sep):
      return FileResponse(vite_index)  # or 404
  ```
  Do the same for the `potential_static` branch. (Add a regression test asserting `/..%2F..%2F…` never returns file bytes.)

## M2. No authentication, no user identity — anyone can read/modify/delete every user's data

- **Where:** every route in `src/app/api/routes/*.py`; global mutable stores in `src/app/ml/alerts/service.py:50-54` and `src/app/ml/simulation/service.py:44`.
- **Failure (executed):** `POST /api/v1/portfolio/create` → `200 port_a7c4a040`; `GET /api/v1/portfolios` listed **178 portfolios** in the local DB; `DELETE /api/v1/portfolios/{any_id}` → `200 {"deleted": true}`. `POST /api/v1/alerts/mark-all-read` → `200 {"updated": 3}` — one anonymous visitor's click marks *everyone's* alerts read and `DELETE /api/v1/alerts` wipes the shared feed. Portfolios, alerts, push subscriptions, and reviews have no owner column anywhere in `src/app/data/storage.py` (see schema, lines 48-176 — no `user_id` on any table).
- **Concrete harm:** any visitor enumerating IDs can delete another user's portfolio (`DELETE /portfolio/{id}`) or pollute the community-review stream (`POST /api/v1/reviews/submit`, which also feeds the "AI fact-checked" trust UI).
- **Smallest fix:** short term, put an owner key on mutating routes: generate a random `X-Client-Secret` per browser, store `owner_hash` on `PortfolioRecord`/`SmartAlert`/`ReviewRecord`, scope all queries and delete/read by it. Long term: real auth (Cognito/OAuth) — see `.env.example`'s "environment" setting that currently does nothing.

## M3. Silent fallback to **fake market data**, then persisted in cache as if real

- **Where:** `src/app/data/service.py:78-87` (`get_history`), `:118-122` (`get_latest_quote`), fallback generator `src/app/data/provider.py:138-249`.
- **Failure:** when Yahoo Finance fails (offline, rate-limited, yfinance schema break — it is on version >=1.6.0 unpinned), `get_history` silently substitutes `MockDataProvider` output — a random-walk built from `md5(symbol)` — and then `cache.save_history()` **persists the synthetic series under the real symbol for 12h** (`settings.cache_ttl_seconds`, `core/config.py:13`). Every downstream consumer (portfolio MTM at `simulation/service.py:97`, backtests, factor extraction, `/market/history`, `/market/quote`) then prices real user portfolios with invented prices, with zero indication. In a finance product this is a data-integrity failure, not just a bug: a delisted or throttled symbol shows a plausible-but-wrong price.
- **Proof path:** `provider.fetch_history` swallows every exception (`provider.py:75-76: except Exception: return pd.DataFrame()`), so the trigger is invisible in logs.
- **Smallest fix:** mark fallback responses, e.g. add a `source: "mock" | "live"` field to `StockQuote`/`MarketHistoryResponse`, never cache mock data (`if not isinstance(df, MockedSentinel)…` — simplest: pass a flag out of the fallback and skip `save_history`), and `logging.warning` on every fallback.

## M4. Blocking network I/O inside `async` routes freezes the whole event loop

- **Where:**
  - `src/app/api/routes/chat.py:44-57` — `async def post_chat_message` → `NitiBotService.chat` → `GeminiClientAdapter.generate` (`assistant/service.py:78-82`): a synchronous LLM call (typically 2-10 s) executed directly on the event loop.
  - `src/app/api/routes/stream.py:14-22` + `src/app/data/streaming.py:67-86` — first `GET /stream/ticks` lazily constructs `MarketTickGenerator`, whose `_seed_data()` performs **15 sequential blocking `yfinance` quote fetches** (up to `timeout=15` each, `provider.py:38`) — potentially minutes of a fully frozen event loop on a cold start.
  - Same pattern: `evaluate_micro_batch` network loops, `explore` profile calls.
- **Concrete failure case:** open one SSE tab while another user posts `/chat` — all SSE heartbeats stall and every concurrent request queues behind the LLM call; with Uvicorn's single worker (`WEB_CONCURRENCY=1` default in docker-compose) the whole app is unresponsive. A client can freeze the box indefinitely by requesting `interval=0.01` SSE streams repeatedly (no connection cap, `stream.py:29-31`).
- **Smallest fix:** for chat, make the route `def` (threadpool) or `await anyio.to_thread.run_sync(service.chat, payload)`. For the tick generator, build it in `create_app()` (startup) or pre-warm with `run_in_executor`; add a client cap and a coarser `interval` floor.

## M5. Docker deployment loses all portfolio data on every redeploy

- **Where:** `docker-compose.yml` (`quantniti` service has **no volume** for `/app/data`); DB path from `src/app/core/config.py:11` (`data_dir = Path("./data")`) + `src/app/data/storage.py:184-187`.
- **Failure (proven by inspection + prod deploy flow):** `deploy.yml` runs `docker compose down && docker compose up -d --build` on every push to `main`. The SQLite file lives in the container layer at `/app/data/quantniti.db`; `down` destroys it. Every real user portfolio, ledger transaction, daily snapshot, and community review is wiped each deploy. (The container build also doesn't even pre-create the DB; it's created lazily at first write.)
- **Smallest fix:** add `volumes: - ./data:/app/data` to the `quantniti` service in `docker-compose.yml` (and stop `docker compose down` on deploy — `up -d --build` alone is sufficient). Also set `data_dir` from env (`QUANTNITI_DATA_DIR`) since `./data` is CWD-dependent.

## M6. Review submission stores unsanitized attacker-controlled strings and misattributes reviews

- **Where:** `src/app/api/routes/reviews.py:28-48`, `src/app/data/reviews_repo.py:81-87`, schema `src/app/core/models.py:814-823` (`user_name` has **no max_length**, `target_id` no validation, no HTML stripping).
- **Failure (executed):** `POST /api/v1/reviews/submit` with `user_name = "attacker<script>alert(1)</script>"` and a 2000-char text → `200 {"is_approved": true, …}`; the payload round-trips verbatim through `GET /api/v1/reviews/basket/x`. React escapes it today, but the same text is serialized into the APK/webview and any future `innerHTML`/markdown rendering becomes stored XSS. Separately: `GET /reviews/basket/<unknown-id>` **falls back to returning reviews for a different basket** (`reviews_repo.py:81-87`) while stamping them with the requested `target_id` — executed: unknown basket returned 4 seed reviews attributed to `UNKNOWN_BASKET_ID_123`. That's fabricated social proof and a contract bug. Also `routes/reviews.py:44-46` silently coerces an invalid `target_type` to `BASKET` instead of 422.
- **Smallest fix:** `user_name: str = Field(max_length=64)` + strip HTML/whitespace on ingest; **delete the fallback block** in `list_reviews` (return `[]` + empty summary); raise 422 on unknown `target_type`.

---

# SHOULD-FIX

## S1. GET `/portfolios/{id}` mutates the ledger and hits N external APIs per call

- **Where:** `src/app/ml/simulation/service.py:84-138` (`get_portfolio` does quote fetch per holding + benchmark + regime + `save_portfolio` DB write), `src/app/api/routes/portfolio.py:88-100`.
- **Failure (executed):** two consecutive `GET`s changed the DB row: `updated_at` `18:13:37 → 18:13:38`. A read endpoint is neither idempotent nor cheap: with a 15-holding portfolio that's ~17 synchronous yfinance calls + a regime fit + a SQLite write per page view. Under load this both hammers Yahoo (guaranteed rate-limit → M3 fake-data path) and turns every GET into a write (contention, see S2). Also `simulation/service.py:120` uses `nifty_hist["close"].iloc[-30]` which throws on <30 rows (swallowed by bare `except Exception: pass` at `:121-122`, silently dropping the benchmark comparison).
- **Smallest fix:** split read from refresh: `GET` returns stored state with a `stale` flag; MTM refresh happens on an explicit `POST /portfolios/{id}/refresh` or a periodic job. Guard `iloc[-30]` with `len(df) > 30`.

## S2. SQLite: no WAL, no busy timeout, unbounded in-memory cache per worker — multi-worker hazard

- **Where:** `src/app/data/storage.py:190-204` (engine without `journal_mode=WAL`/`busy_timeout`; `check_same_thread=False`), `src/app/data/reviews_repo.py:32-38` (a **second independent engine** to the same file), `src/app/ml/simulation/service.py:44` (`_portfolios` dict cache), `scripts/serve_production.py:44-46` (auto-selects up to 4 workers).
- **Failure:** with `WEB_CONCURRENCY` unset, production starts `min(cpu,4)` Uvicorn processes. Each has its own `PortfolioService._portfolios` cache and its own engine: worker A applies a rebalance, worker B serves the stale pre-rebalance holdings from `_portfolios` (it prefers the memory cache over the DB at `simulation/service.py:86-88`); concurrent writes from 4 processes on a non-WAL SQLite DB trip `database is locked` (default sqlite3 busy timeout 5 s; my 6-thread/30-call test didn't trigger it, but 4 processes × quote-refresh writes per GET raises the probability a lot). Alert read/unread state and push subscriptions are per-process too, so two workers show different alert states.
- **Smallest fix:** enable WAL + `busy_timeout` in the `PRAGMA` listener (`storage.py:197-201`); run **one worker** until SQLite is replaced (set `WEB_CONCURRENCY=1` explicitly in compose/fly/railway); drop `_portfolios` or make it read-through from the DB.

## S3. CORS reflects arbitrary origins together with credentials

- **Where:** `src/app/api/app.py:55-61`.
- **Failure (executed):** `OPTIONS` with `Origin: https://evil.example.com` → `access-control-allow-origin: https://evil.example.com` **plus** `access-control-allow-credentials: true` on both preflight and actual response. Any origin can make credentialed cross-origin requests to the API. Currently low impact because there is no cookie/session auth (M2), but it becomes the enabling layer for any future cookie/token auth — and it's one flag away from a real vulnerability.
- **Smallest fix:** `allow_origins` = explicit list (`https://quantniti.jayadityadev.tech`, localhost dev), or drop `allow_credentials=True` if unused.

## S4. `/chat` has no input-size cap and no rate limit — paid-API cost DoS

- **Where:** `src/app/core/models.py:584-587` (`message: str` with no `max_length`), `src/app/api/routes/chat.py:38-61`, no limiter anywhere in the codebase (grep for `slowapi`/`limiter` = nothing).
- **Failure (executed):** `POST /api/v1/chat` with a **500 KB** message → `200`, sent verbatim to the live Gemini API. Any anonymous visitor can drive up token spend at will, and there's no per-IP throttling on any endpoint. Same shape: `POST /api/v1/regime/train` (regime.py:47-57) lets anyone re-fit the shared regime model whenever they want, and `POST /market/sync` (market.py:153-163) triggers up to ~60 yfinance fetches per call unauthenticated.
- **Smallest fix:** `max_length=2000` on `ChatMessageRequest.message`; add slowapi-style IP rate limits (e.g. 10/min on `/chat`, 1/min on `/regime/train`, `/market/sync`, `/notifications/test-push`).

## S5. Global alert service: fake VAPID keys, no actual push, unbounded logs

- **Where:** `src/app/ml/alerts/service.py:30-33` (`DEFAULT_VAPID_PUBLIC_KEY` is a hard-coded bogus base64 string, private key is `"dummy_private_key_for_offline_resilient_testing"`), `:186-201` (`_dispatch_push` never sends anything — it only appends to `_push_dispatch_log`, which grows forever), `:50-54` (per-process memory only; alerts lost on restart and inconsistent across workers).
- **Failure:** `GET /notifications/vapid-public-key` returns a fake key; the browser successfully subscribes (frontend `pwaService.ts:88-102`) but **no push is ever delivered** — silent feature failure. Every evaluated alert (also `routes/alerts.py:117-131 test-push`) appends another entry to `_push_dispatch_log` for each subscription → unbounded memory growth.
- **Smallest fix:** generate real VAPID keys via env (`VAPID_PUBLIC_KEY`/`VAPID_PRIVATE_KEY`), implement actual `web-push` send (or delete the subscription endpoints), cap `_push_dispatch_log` (e.g. `deque(maxlen=500)`), persist alerts or drop the pretense.

## S6. Cache staleness silently masks requested date ranges

- **Where:** `src/app/data/service.py:75-96`, TTL `core/config.py:13` (12 h).
- **Failure (executed):** with a fresh symbol, `GET /market/history?symbol=TCS&start_date=2015-01-01` → `200, count=261`. After the symbol is cached (e.g. by a basket creation pulling 5 y), the **same symbol with 2010 dates** → `404 "No price history found for 'TCS'"` — the 12 h TTL prevents any re-fetch, so users can't get data older than the cached window for half a day. `has_valid_cache` ignores the requested range entirely.
- **Smallest fix:** when `start_date`/`end_date` are provided and the cached range doesn't cover them, treat cache as invalid (store `first_date`/`last_date` in the parquet metadata or compare `df.index` after load).

## S7. Pinned nothing: Docker builds are non-reproducible and `pandas>=3.0.5`-style ranges will break

- **Where:** `pyproject.toml:10-23` (all `>=` ranges), `Dockerfile` Stage 2 (`pip install ".[ai]"` — ignores the committed `uv.lock`).
- **Failure:** `yfinance>=1.6.0` and `pandas>=3.0.5` are aggressive ranges; a fresh build next month may pull a yfinance with a breaking `Ticker.history` signature — and because of `provider.py:75-76` the failure mode is **silent fake data** (M3), not a crash. The repo has `uv.lock` but the Dockerfile never uses it.
- **Smallest fix:** `uv export --format requirements.txt > requirements.lock` (or `uv sync --frozen` in the image) and install from the lock in the Dockerfile.

## S8. Deploy workflow writes the Gemini key via shell interpolation and never refreshes it

- **Where:** `.github/workflows/deploy.yml` (deploy job script): `echo "GEMINI_API_KEY=${{ secrets.GEMINI_API_KEY }}" >> .env`, guarded by `if ! grep -q "GEMINI_API_KEY" .env`.
- **Failure:** the `grep` guard matches the literal string, so once a line exists (even `GEMINI_API_KEY=` from an empty secret) the key is **never updated** on rotation; shell interpolation breaks on special characters; the secret lands in a world-readable-ish `.env` on the server next to the git checkout. Also `docker compose down` causes a full outage + data wipe each deploy (see M5), and `git reset --hard origin/main` will eat any local server state.
- **Smallest fix:** pass the key via `docker compose run -e`/`.env` managed from a proper secret store, or at minimum: `printf 'GEMINI_API_KEY=%s\n' "$KEY" > /etc/quantniti/gemini.env` outside the repo, and replace `down` with `up -d --build --no-deps quantniti`.

---

# NICE-TO-HAVE

## N1. Exception details leaked to clients
`routes/market.py:107-110`, `routes/explore.py:31-34, 47-50, 63-66`, `routes/regime.py:28-44`, `routes/backtest.py:108-111, 123-126` return `detail=str(e)`. Executed example: `/api/v1/chat` surfaces raw `RuntimeError` text. Return generic 500s + log server-side.

## N2. `/docs` and `/openapi.json` exposed in production (88 paths) — `app.py:48-52`
Disable with `docs_url=None` when `settings.environment == "production"` (the `environment` setting currently does nothing at all — `config.py:9`).

## N3. Duplicate router registration doubles the API surface
`app.py:164-181` mounts every router under both `/api` and `/api/v1` (88 OpenAPI paths, each reachable twice). Contract-wise the frontend already mixes both prefixes (e.g. `NitiBotModal.tsx:46` uses raw `fetch("/api/chat/status")` while `pwaService.ts:88` uses `apiUrl("/api/v1/…")` — the relative fetch breaks in the APK where `VITE_API_URL` is set to the prod host). Pick one canonical prefix + explicit aliases; fix `NitiBotModal` to use `apiUrl`.

## N4. Swallowed exceptions blanket the ML layer
`alerts/service.py:224-225, 249-250, 273-274, 299-302` (`except Exception: pass` in the evaluator), `forecasting/service.py list_explore_stocks` (`except Exception: pass` per symbol → an Explore page can silently render with 0 of N stocks), `data/cache.py:66-73`. At minimum `logging.exception` with symbol context.

## N5. `/explore/stocks` is an N+1 over ~60 symbols with no memoization
`forecasting/service.py list_explore_stocks`: per symbol → `get_latest_quote` (network) + `get_history` + factor extraction + full GBM cone forecast. First cold call is tens of seconds; even warm it recomputes everything. Cache the summary list for the TTL window or precompute on sync.

## N6. Health check is a constant
`routes/health.py:8-14` always returns `healthy` — never touches DB, cache, or provider. Docker/fly/railway healthchecks therefore validate nothing but process liveness. Add a component check (cheap: SQLite `SELECT 1`).

## N7. Misc hardening
- `stream.py:29` allows `interval=0.01` and unlimited concurrent SSE clients (each holding a task + shared mutable dicts in `streaming.py:60-64` mutated without locks — benign for floats but worth a per-symbol lock if "live" mode lands).
- `storage.py:265` deletes and rewrites ALL holdings on every save — a save failure between delete and commit is safe transactionally (single session), but `TransactionRecord` history is only written for *new* portfolios (`:290-305`), so later trades must go through `record_transaction` or the ledger silently diverges from holdings.
- `config.py:11-12` `./data` is CWD-relative (Fly/Render/CWD differences can silently create a second DB).
- `serve_production.py:70` `forwarded_allow_ips="*"` trusts `X-Forwarded-For` from any direct peer — fine behind Caddy, spoofable on Railway/Fly.
- `reviews_repo.py` + `storage.py` creating two separate engines to the same SQLite file — consolidate to one engine per process.
- `alerts` route `list_alerts` calls `service.get_alerts()` twice (`routes/alerts.py:38-39`).
- `.env` contains a live `GEMINI_API_KEY` (local). It's gitignored (verified: `git ls-files` does not track it; `git log --all` shows no `.env` history), but given it has been shared in chat/screenshots, **rotate the key**.

## N8. Windows-only path issue in cache filename
`data/cache.py:28-32` sanitizes `^`, `:`, `/` but not `\`. A symbol like `X\..\..\evil` in an unvalidated `POST /market/sync` (`market.py` never calls `is_valid_symbol`) can write parquet outside the cache dir on Windows. Add `\` (and `..`) to the sanitization, and validate sync symbols against the universe.

---

## What I did NOT check

- Full pytest suite (out of scope by instruction; baseline owned elsewhere).
- Frontend behavior beyond API-contract greps (`src/frontend/**` not deeply audited — separate UI audit).
- `src/app/ml/**` numerics (backtest engine look-ahead bias, HRP math, forecaster statistics) — only their I/O behavior from the API layer.
- Actual Web Push delivery (needs real VAPID keys — currently fake, see S5).
- Load/soak behavior of SSE under many concurrent clients (verified functionally only).
- `graphify-out`, APK signing, Android Gradle config, Caddy TLS termination internals.
- Google Gemini prompt-injection hardening beyond noting user text is passed verbatim with system prompt (`assistant/service.py:160-178`) — RAG context is server-generated, user text clearly delimited; risk is limited to the assistant's own output, which is already labeled AI-generated.

## Evidence artifacts

- `.scratch/audit-main/audit_checks_1.py` — traversal, CORS, unauth mutations, validation, lifecycle.
- `.scratch/audit-main/audit_checks_2.py` — deep traversal, cache masking, GET side-effect, SQLite threads, SSE.
- `.scratch/audit-main/audit_checks_3.py` — `.env`/`.git/config` arbitrary read.
- Production probes executed via `curl` against `quantniti.jayadityadev.tech` (status/size/content-type only; secret not printed).

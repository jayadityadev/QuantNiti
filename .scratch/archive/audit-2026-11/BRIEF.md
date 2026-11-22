# QuantNiti Deep Review 2026-11 — Shared Brief

## Repo
- Branch: `audit/deep-review-2026-11`, forked from `main` @ `581890f`.
- Product: AI-driven portfolio intelligence + financial literacy for Indian retail investors.
- Stack: FastAPI + SQLAlchemy/SQLite backend (`src/app`), React 18 + Vite + Zustand + Tailwind frontend (`src/frontend`), Capacitor Android shell (`android/`), Docker/Caddy/AWS Lightsail deploy.
- ML today: GMM market-regime classifier, heuristic multi-horizon GBM-style forecaster (CAPM + momentum + EMA), HRP + Ledoit-Wolf allocator, backtest engine, review fact-checker, RAG NitiBot (Gemini).
- Real cached daily OHLCV: `data/cache/*.parquet`, ~2021-11-16 .. 2026-11-16, 58 universe symbols + `^NSEI` + `^INDIAVIX`.

## Prior work (READ THESE, do not re-derive)
- `.scratch/audit-main/ml.md` + `ml-critique.md`
- `.scratch/audit-main/backend.md` + `backend-critique.md`
- `.scratch/audit-main/frontend.md` + `frontend-critique.md`
- `.scratch/audit-main/architecture.md` + `architecture-critique.md`
These were produced against the same commit as current HEAD. Treat them as hypotheses: re-verify each cited claim against CURRENT source, then add NEW findings the prior audit missed.

## Already re-confirmed live at HEAD
- `src/app/api/app.py` CORS `allow_origins=["*"]` + credentials; SPA fallback path traversal.
- `src/app/core/config.py` `Settings(BaseModel)` ignores env vars.
- `src/app/ml/forecasting/forecaster.py` uses `(drift ± z*vol) * tau` (missing sqrt), dead `horizon_vol`, 8% vol floor, un-annualized momentum.
- `src/app/ml/regime/classifier.py` ranks clusters by `ret/vol`, inverting negative-return clusters; full-sample scaler/GMM fit in `regime/service.py` (look-ahead); temperature 2.5 distorts probabilities.
- `src/app/data/service.py` caches MockDataProvider synthetic history as if real.

## Agent output contract
Write ONE markdown file to the path assigned in your task. Keep it under ~250 lines. Structure:
1. **Verdict on prior findings** — table: finding | CONFIRMED / STALE / OVERSTATED / UNDERSTATED | evidence (file:line).
2. **NEW findings** — each with severity (CRITICAL/HIGH/MEDIUM/LOW), file:line, concrete failure scenario, and minimal fix.
3. **Quant/ML correctness** (where applicable) — show the math or a numeric repro, not prose.
4. **Recommended fix order** — top 5 only, with exact files.
Do not modify source files. Read-only audit. You may run read-only Python probes and tests.
Return a <=15-line summary in your final response; the file is the deliverable.

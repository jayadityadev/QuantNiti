---
name: verify
description: "Drives and verifies the QuantNiti mobile-first web app and REST API. Use to launch, doctor-check, drive mapped features, and capture screenshot and API contract evidence."
---

# QuantNiti Verification Skill

This skill allows agents to launch, doctor-check, drive, and prove user-facing features of the QuantNiti platform (Vite PWA client + FastAPI quantitative intelligence server).

## 1. Launch

The server runs on an isolated port (default `8000`, or `8008` during concurrent verification) with production Vite integration enabled.

```powershell
# Set environment variables and launch uvicorn
$env:QUANTNITI_USE_VITE = "1"
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe -m uvicorn app.api.app:app --app-dir src --host 127.0.0.1 --port 8000
```

**How to tell it's ready:**
- Terminal logs show: `INFO: Application startup complete.` and `INFO: Uvicorn running on http://127.0.0.1:8000`.
- Health check `GET http://127.0.0.1:8000/api/v1/health` returns HTTP 200 with `{"status": "healthy", "service": "quantniti"}`.

## 2. Doctor

Run the verification doctor command to verify process health, model readiness, and API accessibility:

```powershell
.\.venv\Scripts\python.exe .agents/skills/verify/scripts/verify_driver.py doctor --port 8000
```

Doctor checks:
1. `GET /api/v1/health` answers with `{"status": "healthy"}`.
2. `GET /api/regime/current` answers with a recognized market regime (`Low-Volatility Bull`, `High-Volatility Bear`, or `Sideways Consolidation`) and valid probability sum.

## 3. Drive

Drive mapped user features using the included automated Playwright driver:

```powershell
# Verify Market Regime Radar feature
.\.venv\Scripts\python.exe .agents/skills/verify/scripts/verify_driver.py drive market-regime-radar --port 8000 --output-dir .audit/verify

# Verify Onboarding Risk Profiling Quiz
.\.venv\Scripts\python.exe .agents/skills/verify/scripts/verify_driver.py drive onboarding-quiz --port 8000 --output-dir .audit/verify

# Verify Grow AI Basket & Growth Projections
.\.venv\Scripts\python.exe .agents/skills/verify/scripts/verify_driver.py drive grow-ai-basket --port 8000 --output-dir .audit/verify

# Verify Backtesting Lab
.\.venv\Scripts\python.exe .agents/skills/verify/scripts/verify_driver.py drive backtesting-lab --port 8000 --output-dir .audit/verify

# Verify Virtual Paper Portfolio Tracker
.\.venv\Scripts\python.exe .agents/skills/verify/scripts/verify_driver.py drive virtual-paper-portfolio --port 8000 --output-dir .audit/verify
```

Supported feature recipes are documented under [`features/`](./features/README.md).

## 4. Evidence

All verification runs output verifiable artifacts into the designated output directory (`.audit/verify/`):
- **UI Screenshots:** Full mobile viewport (393x852 @ 2x DPR) `.png` screenshots showing real rendered components with data.
- **API Payloads:** Machine-readable `.json` snapshots of the HTTP responses confirming mathematical models, asset allocations, and confidence metrics.
- **Proof Retention:** Evidence files persist in `.audit/verify/` across server teardowns and cleanups.

## 5. Cleanup

To stop the server after a verification session without killing unrelated background processes:

```powershell
# Stop background server task by TaskId in Antigravity session
# Or find and terminate the specific uvicorn PID started for verification
Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*QuantNiti\.venv*" } | Stop-Process
```

Do not delete `.audit/verify/` during cleanup — proof artifacts must survive teardown.

## 6. Helpers

- **Driver script:** [`.agents/skills/verify/scripts/verify_driver.py`](./scripts/verify_driver.py)
  - `doctor --port <PORT>`: Read-only readiness probe.
  - `drive <feature> --port <PORT> --output-dir <DIR>`: Automated UI + API journey execution.
- **Feature Map Index:** [`features/README.md`](./features/README.md)

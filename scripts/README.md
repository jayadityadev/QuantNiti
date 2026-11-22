# QuantNiti Utility & Verification Scripts

This directory contains the operational, build, and verification scripts for the QuantNiti platform.

---

## Active Scripts

### 1. Production Server
- **Script**: `serve_production.py`
- **Purpose**: Runs the local production server. Serves the built frontend Single Page Application (SPA) alongside the FastAPI REST and Server-Sent Event (SSE) endpoints using Uvicorn.
- **Prerequisites**: Frontend built via `npm run build`.
- **Usage**:
  ```bash
  .\.venv\Scripts\python.exe scripts/serve_production.py
  # Optional custom port/host flags:
  .\.venv\Scripts\python.exe scripts/serve_production.py --host 0.0.0.0 --port 8000
  ```

### 2. Android Capacitor APK Builder
- **Script**: `build_apk.py`
- **Purpose**: Automates building the Android Capacitor package. Syncs frontend assets (`npm run build && npx cap sync android`) and triggers Gradle compilation to produce the debug APK (`android/app/build/outputs/apk/debug/app-debug.apk`).
- **Prerequisites**: Android SDK & Java JDK configured in PATH.
- **Usage**:
  ```bash
  .\.venv\Scripts\python.exe scripts/build_apk.py
  # Also available via npm script:
  npm run apk:build
  ```

### 3. Mobile LAN Development Server
- **Script**: `serve_mobile.py`
- **Purpose**: Detects the host workstation's local LAN IP, spins up the server, and prints an ASCII QR code in the terminal for instant testing on physical Android/iOS devices on the same Wi-Fi network.
- **Usage**:
  ```bash
  npm run mobile:serve
  # Or directly:
  .\.venv\Scripts\python.exe scripts/serve_mobile.py
  ```

### 4. API Endpoints Verification
- **Script**: `verify_all_endpoints.py`
- **Purpose**: Validates all active backend REST routes (`/api/regime`, `/api/grow/*`, `/api/explore/*`, `/api/portfolios/*`, `/api/alerts/*`, `/api/reviews/*`, `/api/chat/*`) against schema contracts and expected HTTP status codes.
- **Usage**:
  ```bash
  # Ensure local server is running on port 8000
  .\.venv\Scripts\python.exe scripts/verify_all_endpoints.py
  # Optional custom base URL:
  .\.venv\Scripts\python.exe scripts/verify_all_endpoints.py --url http://127.0.0.1:8000
  ```

### 5. Paper Portfolio E2E Tracking Verification
- **Script**: `test_portfolio_tracking.py`
- **Purpose**: End-to-end integration verification for paper portfolio creation, real-time tick consumption, day-over-day Mark-to-Market (MTM) calculations, and rebalancing alerts.
- **Usage**:
  ```bash
  .\.venv\Scripts\python.exe scripts/test_portfolio_tracking.py
  ```

### 6. AI Services Verification
- **Script**: `verify_all_ai_services.py`
- **Purpose**: Direct verification runner for all 5 QuantNiti AI/ML engines:
  1. Market Regime Classification (HMM / GMM)
  2. Explore Conformal Forecasting Engine
  3. Grow Regime-Aware Hierarchical Risk Parity (HRP) Basket Engine
  4. Social Review Fact-Checking & Mathematical Verification Agent
  5. NitiBot RAG Assistant Engine
- **Usage**:
  ```bash
  .\.venv\Scripts\python.exe scripts/verify_all_ai_services.py
  ```

### 7. Full UI & Responsiveness Test Suite
- **Script**: `test_and_analyze_all.py`
- **Purpose**: Playwright browser automation test suite checking tab navigation, modal sheets, theme toggling, error boundaries, and mobile viewport compliance.
- **Usage**:
  ```bash
  .\.venv\Scripts\python.exe scripts/test_and_analyze_all.py
  ```

### 8. Visual Snapshot Capture Utilities
- **Scripts**: `capture_all_snapshots.py`, `capture_snapshots.py`, `capture_modals.py`
- **Purpose**: Automated headless browser capture tools saving standardized PNG screenshots of UI views and modals into `docs/review/ours/snapshots/` for audits and presentations.
- **Usage**:
  ```bash
  .\.venv\Scripts\python.exe scripts/capture_all_snapshots.py
  ```

### 9. Academic Paper Figure Reproduction
- **Directory**: `paper_figures/`
- **Purpose**: Standalone vector graphics (`.pdf` and 300 DPI `.png`) generators used by `.agents/skills/paper-builder` to reproduce IEEE/ACM academic paper figures.

---

## Archive

- **Directory**: `archive/`
- **Purpose**: Stores historical, one-off report generation and export scripts (e.g., DOCX converters, presentation PPT generators, LaTeX underscore sanitizers, and exhibition PDF renderers).

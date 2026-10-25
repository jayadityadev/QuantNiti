# QuantNiti
### AI-Driven Regime-Adaptive Portfolio Intelligence & Quantitative Decision Support System

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg?logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-6.0-646CFF.svg?logo=vite&logoColor=white)](https://vitejs.dev/)
[![Production](https://img.shields.io/badge/Production-Live%20on%20AWS-7C3AED.svg?logo=amazon-aws&logoColor=white)](https://quantniti.jayadityadev.tech/)
[![Android App](https://img.shields.io/badge/Android%20App-Debug%20%26%20Release%20APK-3DDC84.svg?logo=android&logoColor=white)](https://github.com/jayadityadev/QuantNiti/actions)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF.svg?logo=github-actions&logoColor=white)](https://github.com/jayadityadev/QuantNiti/actions)
[![Coverage](https://img.shields.io/badge/Backend%20Coverage-99%25-brightgreen.svg)]()
[![Frontend Tests](https://img.shields.io/badge/Frontend%20Tests-132%2F132%20Pass-success.svg)]()
[![PWA Ready](https://img.shields.io/badge/PWA-Installable-7C3AED.svg?logo=pwa&logoColor=white)]()

> [!TIP]
> **🚀 Live Production System:** QuantNiti is deployed in production at **[https://quantniti.jayadityadev.tech/](https://quantniti.jayadityadev.tech/)**, hosted on AWS Lightsail (`ap-south-1` Mumbai) behind Caddy v2 automated Let's Encrypt TLS/SSL with continuous deployment via GitHub Actions.

> [!NOTE]
> **QuantNiti** bridges the deep divide in Indian retail finance between black-box speculative trading tips, high-commission bank wealth advisors (1.5%–2.5% AUM fees), and low-yielding fixed deposits. It provides retail investors with unsupervised machine learning market regime detection, multi-factor quantile growth forecasting, hierarchical risk parity (HRP) portfolio optimization, transparent explainable AI (XAI) Trust Cards, and contextual financial literacy.

---

## 📱 Key Product Capabilities

* 🎨 **Electric Violet & Indigo Design System:** Modern squircle interface (`rounded-3xl`), hairline border glow strokes, and physics-based spring transitions (`Framer Motion`). Light mode default with persistent dark mode toggle.
* 🚀 **Onboarding & Persona Quiz:** 3-question scenario-based quiz that evaluates real behavioral loss tolerance and determines risk personas (*Conservative*, *Balanced*, *Aggressive*, *ESG-Conscious*) without confusing financial jargon.
* 🧙 **5-Step Guided Grow Wizard:** Multi-step narrative flow (Capital → Horizon → Persona → Allocation Overview → Deep Dive) with tactile quick-pick chips, word-form reassurance (e.g., `₹50,000 — Fifty Thousand Only`), and discrete whole-share sizing.
* 📊 **Dual-State Portfolio Tracker:** Instant pre-populated **Demo Portfolio** for first-time visitors with realistic synthetic data, seamlessly transitioning to a live **Virtual Paper Portfolio** with real-time mark-to-market and regime-shift rebalance alerts.
* 🔍 **Explore Tab & Hidden Pro Tools:** Streamlined stock cards with visual regime suitability badges, with the advanced **Quant Lab Backtester** (MA Crossover, RSI Reversion, Dual Momentum) cleanly tucked behind a Pro Tools accordion.
* 🤖 **NitiBot RAG Copilot:** Grounded conversational AI assistant answering portfolio questions citing live regime dynamics, risk bounds, and backtest data via Google Gemini.
* 🎥 **Playable Video Explainer Hub:** Responsive 16:9 embedded YouTube quantitative breakdowns with key takeaways, conceptual analogies, and difficulty ratings across 4 learning tracks (*Basics*, *Regimes*, *Risk*, *Quant*).
* ⚡ **Multi-Condition Smart Alert Engine:** Automated rules-and-regime event detection evaluating 6 distinct triggers (Regime Shift, Stop-Loss Breach, Profit Target Reached, Target Weights Drift >5%, Volatility Breakout, ESG Conscience Downgrade) with in-app notification toasts and Web Push support.
* 📱 **Native Android Container & PWA:** Dual distribution model featuring standalone browser PWA installation and a native Android container app (`com.quantniti.app`) compiled via automated GitHub Actions CI/CD workflows using AndroidX `WebViewAssetLoader`.

---

## 🏗️ System Architecture

QuantNiti follows a decoupled architecture where a reactive mobile-first client interacts with an asynchronous Python quantitative backend:

```mermaid
flowchart TD
    subgraph Client["📱 QuantNiti Frontend (React 18 + Vite PWA / Android APK)"]
        Hero["🚀 Onboarding Hero<br/>• 3-Q Scenario Quiz<br/>• Persona Deduction"]
        Tabs["📱 4-Tab Navigation<br/>• Home (Pulse & Video Hub)<br/>• Explore (Stock Cards & Pro Tools)<br/>• Grow (5-Step Wizard)<br/>• Portfolio (MTM & Demo)"]
        Modals["💬 Overlays & Modals<br/>• NitiBot RAG Chat<br/>• Competitor Matrix<br/>• Video Explainer Modal<br/>• 6-Trigger Smart Alerts"]
        Zustand["⚡ Zustand State Engine<br/>• AbortController Registry<br/>• Violet / Dark Theme Toggle"]
    end

    subgraph API["⚡ FastAPI Async Core (Python 3.12)"]
        Gateway["REST Gateway & SSE Stream<br/>• /api/v1/market<br/>• /api/v1/grow<br/>• /api/v1/explore<br/>• /api/v1/portfolio<br/>• /api/v1/stream<br/>• /api/v1/chat<br/>• /api/v1/alerts<br/>• /api/v1/reviews"]
    end

    subgraph ML["🧠 Quantitative & ML Engine"]
        Regime["🔍 Unsupervised Regime Classifier<br/>(Gaussian Mixture Model)"]
        Forecasting["📈 Quantile Forecaster<br/>(Q10, Q50, Q90 Cones)"]
        Covariance["📐 Ledoit-Wolf Shrinkage<br/>(Optimal Regularization)"]
        HRP["🌳 Hierarchical Risk Parity<br/>(Tree Clustering & Bisection)"]
        Allocation["💰 Discrete Allocator<br/>(Whole Shares + Cash Buffer)"]
        AlertEngine["⚡ 6-Trigger Smart Alert Evaluator<br/>(Regime, SL, TP, Drift, Vol, ESG)"]
    end

    subgraph Data["💾 Persistence & External Cloud"]
        DB[("🗄️ SQLite DB (WAL Mode)<br/>Portfolios, Goals & Reviews")]
        MarketFeed["📡 Real-Time SSE Ticks<br/>& yfinance Ingestion"]
        Gemini["🤖 Google Gemini GenAI<br/>(RAG & Fact-Checker)"]
        ESG["🌱 SEBI BRSR & CRISIL<br/>ESG Scores Database"]
        Cloud["☁️ AWS Lightsail (Mumbai)<br/>Caddy v2 Automated TLS/SSL"]
    end

    Client <==>|JSON REST & SSE| Gateway
    Gateway --> Regime
    Gateway --> Forecasting
    Gateway --> HRP
    Regime --> HRP
    Covariance --> HRP
    HRP --> Allocation
    Gateway --> AlertEngine
    Gateway <==> DB
    Gateway <==> MarketFeed
    Gateway <==> Gemini
    Gateway <==> ESG
    Cloud --- API
```

---

## ⚡ Quick Start

### 1. Prerequisites
- **Python 3.12+**
- **Node.js 18+** & **npm**
- **uv** (recommended high-speed Python package manager)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/jayadityadev/QuantNiti.git
cd QuantNiti

# Install Python backend dependencies
uv sync

# Install Node.js frontend dependencies
npm install
```

### 3. Running Locally

#### Development Mode (Hot Reloading Frontend & Backend):
```bash
# Terminal 1: Launch FastAPI Backend Server
uv run uvicorn src.app.api.app:app --reload --port 8000

# Terminal 2: Launch Vite Frontend Dev Server
npm run dev
```

#### Production Unified Mode:
```bash
# Build React client into src/app/static/dist/
npm run build

# Start FastAPI production server (serves the precompiled Vite PWA)
uv run uvicorn src.app.api.app:app --port 8000
```
Open [http://localhost:8000](http://localhost:8000) in your browser. (Toggle Chrome DevTools Device Mode for the mobile experience).

### 4. Running the Native Android App

#### Option A: Direct APK Download
Download the latest pre-compiled debug APK directly from the project's [GitHub Actions Releases / Artifacts](https://github.com/jayadityadev/QuantNiti/actions).

#### Option B: Compile with Android SDK
```bash
cd android
./gradlew assembleDebug
# Generated APK: android/app/build/outputs/apk/debug/app-debug.apk
adb install app/build/outputs/apk/debug/app-debug.apk
```

---

## 🧪 Testing & Verification

The project is engineered under strict Test-Driven Development (TDD) principles, featuring frontend component test coverage and backend quant pipeline verification.

```bash
# Run Frontend Test Suite (Vitest + React Testing Library)
npm test

# Run Backend Unit & Integration Test Suite with Coverage
uv run pytest tests/ --cov=src/app
```

| Test Suite | Total Tests | Status | Coverage |
| :--- | :--- | :--- | :--- |
| **Frontend (Vitest + RTL)** | 132 Tests across 31 Suites | `PASSING` | Full Component Seams |
| **Backend (Pytest + AnyIO)** | 272 Tests across ML, API, Stream | `PASSING` | 99% Line Coverage |

---

## 📂 Project Structure

```
├── .github/
│   └── workflows/            # GitHub Actions CI/CD (Lightsail deploy & Android APK build)
├── .scratch/                 # Local issue tracker & specification records
│   ├── quantniti-core/       # Core platform specs & completed issue records
│   └── ui-redesign/          # UI redesign specs & completed issue records
├── android/                  # Native Android container project (Gradle, WebViewAssetLoader)
├── docs/                     # Architectural decision records (ADRs), PRD, guides
│   ├── ARCHITECTURE.md       # Complete system architecture blueprint
│   ├── HOSTING_AND_SCALABILITY.md # AWS Lightsail, Caddy SSL & hosting guide
│   ├── ML_PIPELINE.md        # Mathematical & econometric ML specification
│   ├── PRD.md                # Master product requirement document
│   ├── USER_GUIDE.md         # Comprehensive user & evaluator walkthrough
│   └── adr/                  # 16 Architectural Decision Records (ADRs)
├── src/
│   ├── app/
│   │   ├── api/              # FastAPI application, middleware, and route handlers
│   │   ├── core/             # Configuration & Pydantic domain models
│   │   ├── data/             # Market data, RAG services, ESG scores, SQLite DB
│   │   ├── ml/               # Quantitative ML algorithms (Regime, HRP, Forecaster)
│   │   └── static/           # PWA manifest, service worker, icons & dist/ bundle
│   └── frontend/             # Modern React 18 SPA codebase:
│       ├── components/       # UI components, layout shell, tabs & modals
│       ├── context/          # ThemeContext & global React providers
│       ├── hooks/            # useAbortableRequest, useAlertPolling hooks
│       ├── services/         # Market stream SSE & AbortController registry
│       └── store/            # Central Zustand application state store
└── tests/                    # Vitest frontend tests & Pytest backend tests
```

---

## 🎯 Core Mathematical & Algorithmic Methodologies

<details>
<summary><b>1. Unsupervised Gaussian Mixture Model (GMM) Market Regime Classification</b></summary>

Uses rolling 20-day returns, realized volatility, Parkinson volatility, and India VIX to categorize macro equity regimes:

$$
\text{Regime} \in \{\text{Low-Vol Bull}, \text{High-Vol Bear}, \text{Sideways Consolidation}\}
$$

Centroids are ranked deterministically by their return-to-volatility ratio.
</details>

<details>
<summary><b>2. Ledoit-Wolf Covariance Matrix Regularization</b></summary>

Replaces ill-conditioned empirical sample covariance $\mathbf{S}$ with an optimal shrinkage combination against a constant-correlation target $\mathbf{F}$:

$$
\boldsymbol{\Sigma}_{\text{LW}} = \delta^* \mathbf{F} + (1 - \delta^*) \mathbf{S}
$$

Prevents matrix inversion singularity and extreme portfolio weight distortion.
</details>

<details>
<summary><b>3. Hierarchical Risk Parity (HRP) Tree Clustering</b></summary>

Applies hierarchical single-linkage tree clustering on correlation distances:

$$
d_{i,j} = \sqrt{\frac{1}{2}(1 - \rho_{i,j})}
$$

Conducts top-down recursive bisection, allocating risk inversely proportional to cluster variance without requiring covariance matrix inversion.
</details>

<details>
<summary><b>4. Multi-Horizon Quantile Growth Forecast Cones</b></summary>

Outputs bounded probabilistic return distributions across 1M, 3M, 6M, and 12M holding horizons with isotonic monotonicity guarantees:

$$
Q_{0.10} \le Q_{0.50} \le Q_{0.90}
$$
</details>

<details>
<summary><b>5. Discrete Integer Share Sizing & Cash Buffer</b></summary>

Converts continuous mathematical weights into executable whole-share quantities for Indian retail brokers (Zerodha, Groww):

$$
n_i = \left\lfloor \frac{w_i \cdot C}{P_i} \right\rfloor, \quad \text{Cash Buffer} = C - \sum_{i=1}^N n_i P_i
$$
</details>

<details>
<summary><b>6. Multi-Condition Quantitative Smart Alert Engine</b></summary>

Evaluates 6 automated triggers across market regimes, price boundaries, and portfolio allocations:
1. **Macro Regime Transition:** $\text{Regime}_t \ne \text{Regime}_{t-1}$ triggering rebalance warnings.
2. **Dynamic Persona Stop-Loss:** $P_t \le P_{\text{entry}} \times (1 - \text{SL}_{\text{persona}})$.
3. **Profit Target Reached:** $P_t \ge P_{\text{entry}} \times (1 + \text{TP}_{\text{persona}})$.
4. **Target Weights Drift:** $\sum |w_{i, \text{current}} - w_{i, \text{target}}| > 5\%$.
5. **Volatility Breakout Alert:** $\sigma_{i, 20\text{d}} > 2 \times \bar{\sigma}_i$ or price breaking Bollinger Bands.
6. **ESG Conscience Downgrade:** BRSR score reduction or sector governance alert.
</details>

---

## 📚 Technical Documentation Links

* 📘 [System Architecture Blueprint (`docs/ARCHITECTURE.md`)](docs/ARCHITECTURE.md)
* ☁️ [Hosting, AWS Lightsail & Scalability Guide (`docs/HOSTING_AND_SCALABILITY.md`)](docs/HOSTING_AND_SCALABILITY.md)
* 📖 [User & Evaluator Guide (`docs/USER_GUIDE.md`)](docs/USER_GUIDE.md)
* 🧠 [Machine Learning & Quantitative Pipeline (`docs/ML_PIPELINE.md`)](docs/ML_PIPELINE.md)
* 📑 [Product Requirements Document (`docs/PRD.md`)](docs/PRD.md)
* 🏷️ [Domain Model & Glossary (`CONTEXT.md`)](CONTEXT.md)
* 🏛️ [Architectural Decision Records (`docs/adr/`)](docs/adr/)

---

## 📄 License & Attribution
Developed for the Major Project initiative by **Jayaditya Dev** (with project teammates Aryaman Tiwari, Chirag T., and Durgashree M., under the guidance of Prof. Beena K). Sourced market data provided via NSE indices and public BRSR/CRISIL reporting.

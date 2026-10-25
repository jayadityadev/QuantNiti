# QuantNiti User Guide & Academic Demonstration Walkthrough

**Version:** 2.1.0 (Full Production & Native Android Release)  
**Target Market:** Indian Equity Markets (NIFTY 50 Universe)  
**Live Production URL:** [https://quantniti.jayadityadev.tech/](https://quantniti.jayadityadev.tech/)  
**Authors:** Aryaman Tiwari, Chirag T., Durgashree M., Jayaditya Dev  
**Guide:** Prof. Beena K (KSIT, CSE Dept)

---

## 1. System Overview

QuantNiti is an AI-driven equity portfolio intelligence, probabilistic growth forecasting, and regime-adaptive quantitative decision support platform designed for Indian retail investors and academic evaluators. It combines rigorous unsupervised machine learning (Gaussian Mixture Models for market regime detection), Hierarchical Risk Parity (HRP) portfolio optimization, transparent Explainable AI (XAI) Trust Cards, and contextual financial microlearning into an Electric Violet & Indigo themed mobile application shell.

### 4-Tab Navigation Architecture

1. 🏠 **Home (`Tab 1`)**: Real-time Market Pulse ticker, Unsupervised Market Regime Radar (Bull, Bear, Sideways probabilities), 4-category Financial Learning Hub (*Basics*, *Regimes*, *Risk*, *Quant*), Playable 16:9 Video Explainer Hub, In-App Competitor Benchmark Drawer, and Notification Center.
2. 🔍 **Explore (`Tab 2`)**: Complete NIFTY 50 universe browser, sector filtering, 360° Stock Intelligence Profiles with multi-horizon quantile return cones (1M, 3M, 6M, 12M), and the **Quant Lab Backtesting Studio** accessible via the collapsible "Pro Tools" accordion.
3. 🌱 **Grow (`Tab 3`)**: 5-Step Guided Investment Wizard (Capital slider with word-form display -> Horizon -> Persona -> Results Donut -> Deep Dive with 4-Pillar Trust Card & ESG Conscience breakdown).
4. 💼 **Portfolio (`Tab 4`)**: Dual-state investment tracker featuring an instant pre-populated read-only **Demo Portfolio** for first-time visitors that transitions into a live **Virtual Paper Portfolio** with real-time mark-to-market P&L, 6-trigger smart alert notifications, regime-shift rebalance diffs, and 1-Click Broker Order Sheet exports (Zerodha CSV / Groww summary).
5. 🤖 **NitiBot Copilot (Floating FAB)**: Persistent floating action button accessible from every tab, providing conversational explanations grounded in QuantNiti's live regime data and portfolio distributions via Google Gemini.

---

## 2. Accessing & Launching the Application

### Option A: Live Production Cloud (Recommended)
Visit the live production deployment at **[https://quantniti.jayadityadev.tech/](https://quantniti.jayadityadev.tech/)** on any smartphone, tablet, or desktop browser.

### Option B: Native Android App (APK)
1. Download the latest debug APK from the project's [GitHub Actions Releases](https://github.com/jayadityadev/QuantNiti/actions).
2. Install `app-debug.apk` on any Android device (Android 8.0+ / API 26+).
3. The app launches fullscreen with native navigation and offline caching via AndroidX `WebViewAssetLoader`.

### Option C: Mobile Progressive Web App (PWA)
* **Android (Chrome):** Tap the browser menu `⋮` -> Select **"Install app"** or **"Add to Home screen"**.
* **iOS (Safari):** Tap the Share icon -> Select **"Add to Home Screen"**.

### Option D: Local Development Mode
```bash
# Clone the repository
git clone https://github.com/jayadityadev/QuantNiti.git
cd QuantNiti

# Install dependencies
uv sync
npm install

# Terminal 1: Launch FastAPI Backend
uv run uvicorn src.app.api.app:app --reload --port 8000

# Terminal 2: Launch Vite Frontend Dev Server
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 3. Academic Demonstration & Evaluation Scenarios

### Demonstration 1: First-Time Onboarding & Behavioral Persona Quiz
1. On initial visit, the **Onboarding Hero** introduces QuantNiti's value proposition.
2. Tap **"Discover My Risk Persona"** to launch the 3-question scenario quiz:
   - Evaluates behavioral loss tolerance under market stress (e.g., reacting to a 15% index drop).
   - Determines optimal Risk Persona: *Conservative*, *Balanced*, *Aggressive*, or *ESG-Conscious*.
3. Completing the quiz seamlessly lands the user on the **Home** tab with persona preferences pre-calibrated.

---

### Demonstration 2: Interactive Financial Literacy & Video Explainer Hub (`Home` Tab)
1. Scroll to the **Learning Hub** carousel on the Home tab.
2. Switch between the 4 structured learning tracks:
   - 🔰 **Basics**: Core diversification and portfolio building fundamentals.
   - 🔄 **Regimes**: Why markets transition across Bull, Bear, and Sideways states.
   - 🛡️ **Risk**: Maximum drawdowns, stop-losses, and capital preservation.
   - ⚡ **Quant**: Hierarchical Risk Parity, Ledoit-Wolf shrinkage, and factor models.
3. Tap **"Watch Video"** on any card:
   - Opens a responsive 16:9 embedded YouTube video breakdown without cookie tracking (`youtube-nocookie.com`).
   - Displays key quantitative takeaways, conceptual analogies, and difficulty ratings.

---

### Demonstration 3: 5-Step Guided Grow Wizard (`Grow` Tab)
1. Navigate to the **Grow** tab from the bottom bar.
2. **Step 1 (Capital Allocation)**:
   - Adjust capital using the smooth touch slider or quick-tap preset chips (`+₹10k`, `+₹25k`, `+₹50k`, `+₹1L`).
   - Notice the real-time word-form reassurance: `₹50,000 — Fifty Thousand Only`.
3. **Step 2 (Time Horizon)**:
   - Select investment horizon: `1M`, `3M`, `6M` (Strategic Stance), or `12M` (Structural Growth).
4. **Step 3 (Risk Persona)**:
   - Review or modify the pre-selected persona with plain-language drawdown bounds.
5. **Step 4 (Results Overview)**:
   - Tap **"Generate AI Recommended Basket"**.
   - Review the **Asset Allocation Donut Chart**, whole-share discrete counts, and 3-tier Rupee growth scenarios (Optimistic $Q_{90}$, Base $Q_{50}$, Pessimistic $Q_{10}$).
6. **Step 5 (Deep Dive)**:
   - Inspect the **4-Pillar Explainable AI Trust Card**: Active Regime Context, 5-Year Hit Rate, Stress Drawdown Guardrails, and Disintermediation Fee Savings vs private bank wealth managers.
   - Review the **ESG Conscience Score** breakdown.
7. Tap **"Track in Virtual Paper Portfolio"** to activate live simulated tracking.

---

### Demonstration 4: Stock Explorer & Quant Lab Backtesting (`Explore` Tab)
1. Navigate to the **Explore** tab.
2. Filter the universe by Sector (e.g., *Information Technology*, *Banking & Fin*, *Metals*, *Commodities*).
3. Tap any stock card (e.g., `TCS` or `INFY`) to open the **360° Stock Intelligence Profile**:
   - Inspect multi-horizon return cones ($1\text{M}, 3\text{M}, 6\text{M}, 12\text{M}$).
   - Review technical indicators, beta, alpha, and Regime Suitability badge.
4. Expand the **🧪 Advanced Quantitative Backtester (Pro Tools)** accordion:
   - Select Strategy: *Buy & Hold*, *Moving Average Crossover*, *RSI Mean Reversion*, *Bollinger Band Breakout*, or *Dual Momentum*.
   - Tap **"Run Vectorized Simulation"**:
   - Inspect CAGR, Sharpe Ratio, Sortino Ratio, Max Drawdown, interactive equity curve, and regime attribution table.

---

### Demonstration 5: Dual-State Portfolio Tracking & Smart Alerts (`Portfolio` Tab)
1. Navigate to the **Portfolio** tab.
2. If visiting for the first time, examine the pre-populated **Demo Portfolio**:
   - Shows realistic synthetic holdings, mark-to-market valuations, and a persistent showcase banner.
3. Switch to your live **Virtual Paper Portfolio**:
   - Inspect live mark-to-market performance, unrealized P&L in Indian Rupees (`₹`), and benchmark alpha vs NIFTY 50.
4. **Smart Alerts & Regime Rebalancing**:
   - When a market regime shifts or price triggers occur, review the alert badge.
   - Click **"View Rebalance Diff"** to inspect the interactive before/after asset allocation diff.
   - Tap **"Apply Rebalance"** to update simulated holdings to the new regime-optimal weights.
5. **Broker Order Sheet**:
   - Tap **"Broker Order Sheet"** to generate 1-click executable whole-share orders formatted for Zerodha (CSV) or Groww (text summary).

---

### Demonstration 6: NitiBot Grounded Conversational AI Copilot
1. Tap the floating **NitiBot FAB** in the bottom-right corner.
2. Ask natural language questions:
   - *"Why did the AI allocate to Infosys and Gold ETF?"*
   - *"What will happen to my portfolio if the market crashes into a High-Vol Bear regime?"*
   - *"Explain how Hierarchical Risk Parity works in simple terms."*
3. NitiBot synthesizes answers citing live market regime probabilities, Trust Card risk bounds, and SEBI-compliant educational disclaimers.

---

## 4. Test Suite Execution & Verification

Run all automated unit and integration tests:

```bash
# Frontend Vitest Suite (132 tests passing across 31 suites)
npm test

# Backend Pytest Suite with Coverage (272 tests passing, 99% coverage)
uv run pytest tests/ --cov=src/app
```

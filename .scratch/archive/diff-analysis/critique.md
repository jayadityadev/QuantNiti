# QuantNiti Post-Mortem Architecture & Product Critique

**Target Review Range:** `581890f1adea7cae33b1b22f035041fd98ce2b63` (2026-11-11 23:53) to `a8f817783260b86c11a1d6efe991a6d090323435` (HEAD)  
**Total Changes:** 24 commits, 229 files changed, ~19,739 insertions / ~1,873 deletions (excluding generated graphs and build artifacts)  
**Reviewer:** Senior Staff Engineer & Quantitative Product Architect  
**Date:** November 15, 2026  
**Final Verdict:** **MIXED (5.6 / 10)** — High-leverage financial primitives and algorithmic depth, compromised by severe institutional feature creep, disconnected phantom backends, UI duplication, and dilution of QuantNiti's beginner-first identity.

---

## 1. Executive Summary & Context

QuantNiti was founded on a distinct and compelling value proposition:
> **Original Identity / Mission:** A retail-investor-focused quantitative investing app. Beginner-friendly, plain-English, safe, simple, and transparent. Its purpose is to bridge the Indian retail investing gap between reckless tip-trading channels, exorbitant private wealth management fees (1.5%–2.5% AUM), and low-yielding fixed deposits. It provides retail investors with unsupervised machine learning regime detection, whole-share portfolio sizing, behavioral persona guidance, and long-term compounding clarity.

Across the 24 commits under review (`581890f1..a8f8177`), the development team executed two concurrent workstreams:
1. **Adaptive Workstation & Belltalon Integration (`cf9fae9` & `bwt-01..07`):** Embedding institutional terminal capabilities from a reference professional workstation (Belltalon).
2. **Quantitative Backend Engine Integration (`a8f8177`):** Integrating Markov regime transition dynamics, 3-tier portfolio exits, trailing stops, pre-trade risk controls, idempotent SQLite execution ledgers, and a WebSocket quote hub.

### The Central Question
*Did these changes make QuantNiti better, or did they clutter the codebase and dilute its retail-beginner identity?*

### The Verdict: MIXED (5.6 / 10)
The changes represent a **bifurcated codebase**:
- **Genuine Engineering Wins (Net Positive):** The introduction of exact decimal money architecture (`big.js` with `roundHalfUp`), monospace tabular typography, mobile stacked holding cards, Indian statutory charges engines (STT, GST, Stamp Duty, NSE fees), fee-adjusted long-term compounding trajectories, and the IST market session state machine significantly elevated QuantNiti's financial rigor and mobile usability.
- **Severe Product & Architectural Failures (Net Negative):** The project suffered from aggressive institutional terminal envy. It grafted an intimidating Bloomberg-style 3-column workstation cockpit onto a clean consumer app, introduced speculative day-trading derivative jargon (`MIS`, `NRML`, `Options`, `SL-M`) into an app designed to protect retail beginners from speculation, and built hundreds of lines of complex backend infrastructure (WebSocket QuoteHub, Zerodha Kite OAuth, durable SQLite execution ledgers, pre-trade risk guards) that are **100% disconnected from the frontend client**.

---

## 2. Quantitative Scorecard

| Area | Score (/10) | Summary Judgment |
| :--- | :---: | :--- |
| **Frontend Architecture** | **6.5 / 10** | Outstanding decimal primitives (`Money`, `Price`, `Pnl`) and mobile holding cards; marred by an overwhelming 3-column desktop layout, duplicated watchlists, and client-side mock order execution. |
| **Backend Architecture** | **6.0 / 10** | High algorithmic quality in Markov chains, pure rebalancing, and risk limits; severely penalized because major subsystems (OAuth, WebSocket, Ledger) are orphaned dead code without UI consumers. |
| **Test Quality & Coverage** | **7.0 / 10** | High test count (295 Vitest tests, 75 Pytest tests) and rigorous mathematical assertions; hampered by unhandled React `act(...)` state warnings in `AppShell` and a slow 7-minute Pytest runtime. |
| **Documentation & Git Hygiene** | **4.5 / 10** | Extensive coordination logs, but severely marred by accidental deletions of academic PDFs and UI snapshots in `b4ea181`, coupled with 800k+ lines of noisy graphify JSON commits. |
| **Scope & Originality Alignment** | **4.0 / 10** | Heavily diluted QuantNiti's beginner-first ethos. Replaced simple long-term goal compounding with institutional day-trading terminology and external "Belltalon" branding. |
| **OVERALL COMPOSITE** | **5.6 / 10** | **MIXED** — Genuine financial engineering achievements weighed down by scope creep, phantom backends, and brand confusion. |

---

## 3. Deep-Dive Codebase Findings

### 3.1 Frontend/Backend Consistency & Financial Engine Discrepancies

#### A. Statutory Charge Rate Mismatch (NSE Exchange Turnover Fee)
A direct inconsistency exists between the newly added frontend and backend statutory fee engines:
- **Frontend (`src/frontend/utils/taxCalculator.ts`, L38, L98):**
  ```ts
  // 3. NSE Exchange Charges (0.00297%)
  const exchangeCharges = turnover.mul(0.0000297).round(2);
  ```
  The frontend uses **`0.00297%`**, which is the statutory rate mandated by SEBI's uniform "true-to-label" circular effective **October 1, 2024** (NSE Circular NSE/INSP/63045).
- **Backend (`src/app/ml/simulation/charges.py`, L23, L91):**
  ```python
  NSE_TURNOVER_RATE = Decimal("0.0000345")  # 0.00345%
  raw_exchange = turnover_dec * NSE_TURNOVER_RATE
  ```
  The backend simulation engine uses **`0.00345%`**, the legacy pre-October 2024 rate.
- **Concrete Impact:**
  For a standard delivery transaction of ₹1,00,000 on NSE:
  - Frontend Order Ticket computes: NSE Fee = **₹2.97**, GST = **₹0.55**, Total Charges = **₹118.62**.
  - Backend Simulation computes: NSE Fee = **₹3.45**, GST = **₹0.64**, Total Charges = **₹119.19**.
  - Both engines have automated unit tests (`tests/frontend/unit/taxCalculator.test.ts` vs `tests/unit/test_charges.py`) asserting completely different numbers for the exact same transaction, codifying a permanent **₹0.57 per lakh** divergence between client and server.

#### B. Rounding Paradigm Collision
- **Backend (`src/app/ml/simulation/charges.py`, L99–L104):** Strictly enforces Banker's Rounding (`ROUND_HALF_EVEN`) to 2 decimal places (paise) via Python's `decimal` module.
- **Frontend (`src/frontend/utils/decimal.ts`, L14):** Configures `big.js` with `Big.RM = Big.roundHalfUp` (commercial rounding away from zero).
- **Impact:** On boundary odd turnovers ending in half-paise (`0.005`), the backend rounds to the nearest even paise while the frontend rounds up, creating synthetic reconciliation breaks between frontend order tickets and backend ledger records.

#### C. Type Leakage & Premature Float Coercion
While Ticket BWT-07 claimed to establish an "Exact Decimal Architecture", `src/frontend/utils/taxCalculator.ts` immediately destroys type safety at its boundary:
```ts
return {
  turnover: turnover.round(2).toNumber(),
  brokerage: brokerage.toNumber(),
  totalCharges: totalCharges.toNumber(),
  // ...
};
```
Every single exact `Big` instance is coerced back into a standard JavaScript IEEE 754 floating-point `number`. The UI components consuming `StatutoryChargesBreakdown` receive imprecise floats rather than boxed decimals.

---

### 3.2 Integration Quality: Well-Integrated vs. Bolted-On

#### A. Disconnected "Phantom" Backend Subsystems
Commit `a8f8177` added ~3,000 lines of backend Python code that are completely orphaned from the user-facing web application:
1. **WebSocket QuoteHub (`src/app/realtime/hub.py`, 380 lines & `source.py`, 178 lines):**
   - Implements a sophisticated 5Hz tick-coalescing WebSocket server with channel multiplexing.
   - **Frontend Reality:** Grepping `src/frontend/` reveals **zero** WebSocket connections. The frontend exclusively uses the legacy SSE endpoint (`/api/v1/stream/market`) via `marketStream.ts` or static directories. The entire WebSocket engine is dead code in production.
2. **Zerodha Kite OAuth Suite (`src/app/api/routes/broker.py`, 373 lines & `src/app/core/security.py`, 226 lines):**
   - Implements KiteConnect OAuth login, TOTP handling, state HMAC validation, and AES-256-GCM encrypted database storage for broker API keys and secrets.
   - **Frontend Reality:** There is **zero** UI in QuantNiti to connect a broker. There is no settings page, no "Connect Zerodha" button, and no token refresh flow.
3. **Idempotent Order Ledger (`src/app/ml/simulation/execution_ledger.py`, 219 lines & `storage.py`):**
   - Implements durable SQLite tables (`order_intents`, `broker_accounts`, `broker_snapshots`) with serialized state transitions (`Submitting -> Submitted -> Filled`).
   - **Frontend Reality:** The frontend manual order drawer (`OrderTicketDrawer.tsx`, L250–L316) does not call the backend execution ledger. It executes trades by directly mutating local React state inside Zustand!
4. **Proactive 3-Tier Exit Engine (`src/app/ml/portfolio/exit_engine.py`, 314 lines):**
   - Exposes `/api/v1/portfolios/{id}/exit-recommendations` and `/execute-exit`.
   - **Frontend Reality:** Neither endpoint is ever fetched by `src/frontend`.

#### B. The Bolted-On Desktop "Cockpit" (`AppShell.tsx`, L152–L189)
QuantNiti was designed as an elegant, focused, mobile-first web app with a max-width container (`max-w-[520px]`). 
Commit `cf9fae9` modified `AppShell.tsx` to force a 3-column workstation cockpit on screens $\ge 1024\text{px}$:
- **Left Column:** `DesktopCommandPane.tsx` (320px–350px)
- **Center Column:** Main application workspace
- **Right Column:** `DesktopCopilotPane.tsx` (320px–360px)

This causes severe user experience issues:
- **Visual Clutter:** A beginner looking to understand their ₹50,000 portfolio is bombarded with a persistent left surveillance rail, an active IST clock, a market countdown badge, a regime radar, and an always-docked AI copilot taking up 700px of horizontal space.
- **Brand Intrusion:** The left pane permanently features a gradient CTA: *"Belltalon Live Execution Seam: Export this regime-adaptive portfolio as a verified strategy definition JSON for 1-click execution in Belltalon."* QuantNiti's own UI is used as a billboard for an institutional trading terminal that retail beginners do not own or understand.

---

### 3.3 Institutional Jargon & Mission Dilution

QuantNiti's founding identity is to protect retail investors from gambling, day-trading tips, and complex derivative pitfalls. The changes in `OrderTicketDrawer.tsx` (963 lines) completely violate this premise:
- **Speculative Order Types:** The drawer introduces `MIS` (Margin Intraday Square-off), `NRML` (Normal Margin for Derivatives), `SL` (Stop-Loss Limit), `SL-M` (Stop-Loss Market), `Day`, `IOC` (Immediate or Cancel), and `Disclosed Quantity`.
- **F&O Derivative Leaks:** Lines 85–93 in `taxCalculator.ts` introduce options premium turnover and futures STT rates (`0.02%` and `0.1%`).
- **Retail Danger:** Encouraging a retail beginner to toggle between CNC and MIS intraday leverage, or exposing Stop-Loss Market order types that SEBI specifically restricted due to flash crash risks, is completely contrary to QuantNiti's educational mission.
- **Synthetic Illusion:** Despite the intimidating institutional UI, clicking "Place Order" does not place an actual order with a broker—it modifies an in-memory array and renders a receipt with an "Export to Belltalon JSON" copy button.

---

### 3.4 Duplication, Dead Code & Bloat

1. **Watchlist Surveillance Duplication:**
   - `src/frontend/components/markets/WatchlistRail.tsx` (324 lines) sits in the desktop left pane.
   - `src/frontend/components/explore/WatchlistWorkstation.tsx` (376 lines) sits inside the Explore tab.
   - When a user on desktop navigates to Explore $\rightarrow$ "Watchlist Surveillance", they are presented with **two identical watchlist tables side by side**, querying the exact same Zustand store (`useWatchlistStore.ts`).
2. **Static Quote Directory Sprawl:**
   - `src/frontend/data/quoteDirectory.ts` adds **385 lines** of hardcoded stock quotes.
   - `src/frontend/pages/ExplorePage.tsx` already maintained `DEFAULT_STOCKS`.
   - `src/frontend/components/portfolio/demoPortfolioData.ts` maintains a third set of hardcoded stock data.
   - `src/app/universe.py` on the backend maintains a fourth set.
3. **Execution Export Fragmentation:**
   - QuantNiti now has **three separate export modals**:
     - `OrderSheetModal.tsx`: Generates clean Zerodha CSV and Groww text (the original beginner-friendly pattern).
     - `OrderTicketDrawer.tsx`: Generates Belltalon/Zerodha JSON.
     - `DesktopCommandPane.tsx`: Generates Belltalon StrategyDefinition JSON.
     - `src/app/ml/portfolio/rebalancer.py`: Generates another version of Zerodha CSV.

---

### 3.5 Test Quality, Performance & Fragility

- **Frontend Test Suite Health:**
  - 52 of 53 test suites pass; 294 of 295 tests pass.
  - **The Defect:** `tests/frontend/unit/AppShell.test.tsx` fails during full parallel test execution due to a timeout waiting for `findByText(/Home Page/i)`.
  - **Root Cause:** In `AppShell.tsx`, `DesktopCommandPane`, `DesktopCopilotPane`, and `ModalRoot` are rendered unconditionally when `isOnboarded=true`. Mounting `App` in a test now mounts `IstClock` (active intervals), `useNow` (active intervals), `RegimeRadar`, `NitiBotChat`, and `OrderTicketDrawer`. This floods the React DOM with dozens of concurrent timers and generates cascading `act(...)` warnings:
    ```text
    Warning: An update to Header inside a test was not wrapped in act(...).
    Warning: An update to RegimeRadar inside a test was not wrapped in act(...).
    Warning: An update to NitiBotChat inside a test was not wrapped in act(...).
    Warning: An update to OrderTicketDrawer inside a test was not wrapped in act(...).
    ```
- **Backend Test Suite Performance:**
  - 75 tests pass across 9 test files, but execution takes **411 seconds (6 minutes 51 seconds)** on Windows.
  - The runtime is bloated by repeated SQLite on-disk table creation and teardown in `test_execution_ledger.py` and `test_broker_oauth.py`.
  - Generates 57 deprecation warnings regarding `@app.on_event("startup")` and deprecated Starlette `TestClient` usage.

---

### 3.6 Documentation & Git Hygiene Failures

In commit `b4ea181715d9312a5028ba224b1c0ececfa44793` (`docs(sota): update spec.md status to completed`):
- **Catastrophic Deletions:** The commit accidentally deleted critical academic project documentation and UI verification assets:
  - `docs/academic_docs/samples/other-references/ProjectPhase1-FinalReview.pdf` (1.25 MB)
  - `docs/academic_docs/samples/other-references/ProjectPhase1-Synopsis.pdf` (275 KB)
  - `docs/academic_docs/samples/other-references/ProjectPhase1-ZeroethReview.pdf` (360 KB)
  - `docs/academic_docs/samples/phase1_text.txt` (1,162 lines of primary project documentation)
  - 15 PNG snapshots under `docs/review/ours/snapshots/`
- **Knowledge Graph Noise:** Over 800,000 lines of generated graph AST data (`graphify-out/graph.json`) were repeatedly committed across merge commits, causing massive git history bloat.

---

## 4. Prioritized Action Lists

### 4.1 Top 5 Items to KEEP (Genuine High-Leverage Improvements)

| Rank | Component / File Path | Why It Must Be Kept | Concrete Evidence |
| :---: | :--- | :--- | :--- |
| **1** | `src/frontend/utils/decimal.ts`<br/>`src/frontend/components/trading/` (`Money.tsx`, `Price.tsx`, `Pnl.tsx`) | Completely eliminates IEEE 754 floating-point display bugs (`0.1 + 0.2 = 0.30000000000000004`). Provides standard Indian number formatting (`1,00,000`) and tabular-nums typography. | Tested by `ValuePrimitives.test.tsx` and `decimal.test.ts`. Handles edge cases (`NaN`, `Infinity`, `null`) safely. |
| **2** | `src/frontend/components/portfolio/HoldingsTable.tsx` (Mobile Card View) | Replaces the broken mobile horizontal scroll-trap on viewports $< 640\text{px}$ with responsive stacked cards. | `HoldingsTableMobile.test.tsx`. Dramatically improves handheld usability for retail users. |
| **3** | `src/app/ml/simulation/charges.py` & `src/frontend/utils/taxCalculator.ts` (CNC Mode) | Provides complete statutory cost transparency (STT, SEBI fee, Stamp duty, GST) for retail delivery trades, showing exact net capital required. | Backed by `test_charges.py` and `taxCalculator.test.ts`. Eliminates broker hidden-fee surprises. |
| **4** | `src/app/ml/portfolio/compounding_engine.py` (Statutory Fee Drag) | Integrates statutory fee deductions directly into long-term compounding SIP/lump-sum projections and contrasts them against 7% Bank FDs. | Lines 46–80, 126–160 in `compounding_engine.py`. Highly educational for retail beginners planning 10-year wealth journeys. |
| **5** | `src/frontend/utils/marketSession.ts`<br/>`src/frontend/components/ui/IstClock.tsx` | Accurate Indian market session state machine (Pre-open, 09:15–15:30 IST Regular, Post-close, Weekend) with live opening countdown. | Validated by `marketSession.test.ts` and `IstClock.test.tsx`. Educates beginners on when exchange execution actually occurs. |

---

### 4.2 Top 5 Items to FIX (High-Value Code Needing Remediation)

| Rank | Component / File Path | Problem & Concrete Evidence | Prescribed Remediation |
| :---: | :--- | :--- | :--- |
| **1** | `src/app/ml/simulation/charges.py` vs<br/>`src/frontend/utils/taxCalculator.ts` | **Exchange Rate & Rounding Divergence:** Backend uses outdated `0.00345%` and Banker's rounding; frontend uses post-Oct 2024 `0.00297%` and `roundHalfUp`. Divergence: ₹0.57 per lakh. | Update backend `NSE_TURNOVER_RATE = Decimal("0.0000297")` in `charges.py`. Align rounding policies across both tiers. |
| **2** | `src/frontend/components/modals/OrderTicketDrawer.tsx` | **Client-Side State Mutation & Disconnect:** The drawer modifies React state directly (`L302–L316`) instead of dispatching to the backend execution ledger. | Refactor drawer to call `POST /api/portfolio/{id}/rebalance/apply` or a dedicated execution endpoint backed by `execution_ledger.py`. |
| **3** | `src/frontend/pages/ExplorePage.tsx` vs<br/>`WatchlistWorkstation.tsx` & `WatchlistRail.tsx` | **Double Watchlist Collision:** Navigating to Explore on desktop renders two full watchlist surveillance panels side by side. | Remove the full-screen watchlist view from Explore. Make the watchlist a dedicated modal or drawer accessible on demand. |
| **4** | `src/frontend/components/layout/AppShell.tsx` | **Eager Timer Mounting & act(...) Warnings:** Renders sidebars and modals unconditionally, causing background interval leaks and test timeouts in `AppShell.test.tsx`. | Lazy-load `DesktopCopilotPane` and `DesktopCommandPane`. Unmount interval timers when components are hidden. |
| **5** | `src/frontend/components/portfolio/PortfolioPage.tsx` | **Orphaned Rebalance Engine:** Rebalance alerts do not invoke `rebalancer.py` or `PreTradeRiskManager`, calculating diffs client-side. | Wire `handleRebalance` to `POST /api/portfolio/{id}/rebalance/validate` and `apply` to leverage the Python risk guardrails. |

---

### 4.3 Top 5 Items to REMOVE (Institutional Bloat & Distractions)

| Rank | Component / File Path | Why It Must Be Removed | Concrete Evidence |
| :---: | :--- | :--- | :--- |
| **1** | `src/frontend/components/layout/DesktopCommandPane.tsx` & `DesktopCopilotPane.tsx` (Persistent 3-Column Layout) | Destroys QuantNiti's clean, distraction-free aesthetic by turning it into a cluttered Bloomberg terminal clone. Eats 700px of screen space. | Lines 152–189 in `AppShell.tsx`. Overwhelms retail beginners with institutional data density. Make Copilot a floating floating action button (FAB) / slide-over drawer. |
| **2** | Prominent "Belltalon Live Execution Seam" CTAs (`DesktopCommandPane.tsx`, L126–L154 & `OrderTicketDrawer.tsx`, L869–L886) | Retail beginners have no idea what "Belltalon" is. Promoting an external proprietary institutional terminal dilutes QuantNiti's brand and confuses users. | In-app advertising for a reference codebase. Exporting should be framed as standard "Export Order CSV / JSON". |
| **3** | Intraday & Derivative Order Types (`MIS`, `NRML`, `SL-M`, `IOC`) in `OrderTicketDrawer.tsx` | Directly contradicts QuantNiti's foundational thesis of steering retail investors away from high-risk speculative trading. | Lines 370–430 in `OrderTicketDrawer.tsx`. QuantNiti should strictly support Cash Delivery (CNC) equity investing. |
| **4** | Orphaned Zerodha OAuth Suite (`src/app/api/routes/broker.py` & `src/app/core/security.py`) | 600+ lines of backend code, encryption vaults, and background sweep tasks that have zero user interface in the app. | Zero references to `/api/v1/broker` in `src/frontend`. Dead code that increases maintenance and attack surface. |
| **5** | Hardcoded Static Quote Directory (`src/frontend/data/quoteDirectory.ts`) | 385 lines of duplicate static stock data duplicating `DEFAULT_STOCKS` in `ExplorePage.tsx` and `universe.py` on the backend. | Dead data bloat. All symbol metadata should be served dynamically from the single source of truth (`/api/explore/stocks`). |

---

## 5. Architectural Recommendations for Next Milestone

1. **Re-anchor to the Retail Beginner:**
   Strip away day-trading artifacts (MIS, F&O derivatives, Stop-Loss Market orders). Position QuantNiti as the premier, trusted tool for disciplined, regime-aware wealth accumulation.
2. **Bridge the Frontend/Backend Chasm:**
   Either build the user interfaces for the advanced backend features (Kite OAuth connection, live WebSocket price streaming, execution ledger history) or prune the orphaned backend code from the primary repo.
3. **Consolidate Order Export to the Zerodha/Groww Standard:**
   Retire the "Belltalon JSON" branding. Standardize on the proven `OrderSheetModal.tsx` pattern that generates 1-click Zerodha Basket CSVs and Groww text lists.
4. **Restore Git & Documentation Hygiene:**
   Restore the deleted academic project PDFs (`ProjectPhase1-FinalReview.pdf`, etc.) deleted in commit `b4ea181`, add `graphify-out/graph.json` to `.gitignore` or track it via LFS/clean hooks, and refactor `AppShell.test.tsx` to eliminate test fragility.

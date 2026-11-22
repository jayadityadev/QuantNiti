# Adversarial Critique: Frontend Audit Report (`.scratch/audit-main/frontend.md`)

**Reviewer:** Independent Adversarial Reviewer (Dispatched Worker)  
**Target:** `.scratch/audit-main/frontend.md` (`src/frontend/**`, `index.html`, `vite.config.ts`, `tailwind.config.js`)  
**Mode:** READ-ONLY verification; no application source code was modified.  
**Verdict:** **SUBSTANTIALLY VALID with Targeted Corrections**. The original audit accurately uncovers systemic integrity, state desynchronization, rendering, and accessibility defects. However, one top finding contains a technical overstatement regarding JavaScript truthiness (`(0).toFixed(1)`), and the proposed fix for the `PortfolioPage` stale closure overlooks the current method signature in `useAppStore`.

---

## 1. Top Findings Verification Matrix

| # | Auditor Finding | Verdict | Code Verification & Evidence |
|---|---|---|---|
| **1.1** | MarketPulse hardcoded NIFTY (`38-41`) | **AGREE** | `MarketPulse.tsx:38-41`: Initial state hardcoded to `niftyPrice = 23010.0`, `niftyChange = 73.25`, `niftyChangePct = 0.32`, `lastUpdated = "Live"`. The `fetchSnapshot` catch block swallows errors (`:65-67`), permanently displaying fake prices and a green "Market Open" pulse when offline or when backend fails. |
| **1.2** | PortfolioPage invented profit (`171-221`) | **AGREE** | `PortfolioPage.tsx:184-185`: Creates goals with `pnl_1d: Math.round(invested_amount * 0.008)` and `pnl_1d_pct: 0.8` (+0.8% daily profit guaranteed out of thin air). Pairs with `PortfolioHeroCard.tsx:34-39` which renders a `LIVE STREAM` indicator next to this simulated profit. |
| **1.3** | ProToolsBacktester fake metrics (`63-125`) & hardcoded SVG curve (`368-405`) | **AGREE** | `ProToolsBacktester.tsx:63-125`: Catch block sets `fallbackResult` with `total_return_pct: 48.5`, `cagr: 16.2`, `sharpe_ratio: 1.45`, `win_rate_pct: 64.0`. Lines `381-401`: SVG curve uses static bezier control points (`M 10 100 Q 100 80 200 48 T 390 20`) that completely ignore `backtestResult.equity_curve`. Every asset/strategy displays the exact same trajectory. |
| **1.4** | Step5DeepDive fake testimonials & metrics (`24-55`, `92-104`, `187-213`) | **AGREE** | `Step5DeepDive.tsx:24-55`: Hardcoded `SAMPLE_REVIEWS` ("Arjun M. (Bengaluru)", "Pooja S. (Mumbai)") shown under trust headings. Lines `92-104`: Fallbacks fabricate ESG 78.4 and QuantNiti 9.8% vs NIFTY 6.2%. Lines `187, 200, 213`: Hardcodes "68.4% Backtested Win Rate" and "Save ~₹3,200/yr vs Traditional PMS". |
| **1.5** | Fallback turning 0% into +48.5% (`ProToolsBacktester.tsx:301`, etc.) | **TIGHTEN / CORRECT** | **Technical Overstatement by Auditor:** Line `301` is `+{backtestResult.metrics?.total_return_pct?.toFixed(1) || "48.5"}%`. In JavaScript, `(0).toFixed(1)` returns `"0.0"`. Because `"0.0"` is a non-empty string, it is **truthy**, so `"0.0" || "48.5"` evaluates to `"0.0"`, NOT `"48.5"`.<br><br>**However, the finding is valid in two other critical respects:**<br>1. If `total_return_pct` is `null` or `undefined` (e.g. partial response), `undefined?.toFixed(1)` is `undefined`, triggering `"48.5"`.<br>2. **Unformatted numeric `||` fallbacks DO corrupt genuine zeros** in the exact same file: `ProToolsBacktester.tsx:336-337` renders `{metrics?.winning_trades || 18}W` and `{metrics?.losing_trades || 10}L`. A strategy with 0 winning trades renders as **18W**! Similarly, `TopRecommendations.tsx:74` renders `stock.growth_6m_base_pct || 12.5` (a 0% forecast displays as **+12.5%**). |
| **2.1** | PortfolioPage stale-closure tick handler (`69-117`) | **AGREE** | `PortfolioPage.tsx:69-110`: `marketStream.subscribe` captures `portfolios` from render scope. The effect dependency array is `[activePortfolio?.portfolio_id, activePortfolio?.holdings?.length]`. Because `portfolios` is not in deps, any tick after the initial render writes back the stale `portfolios` snapshot. Adding or updating another portfolio while `activePortfolioId` remains unchanged results in that portfolio being completely wiped on the next market tick.<br><br>Furthermore, `setPortfolios` in `useAppStore.ts:181` executes synchronous `localStorage.setItem` of the entire portfolio list on every tick. |
| **2.2** | PortfolioPage compounding POST storm (`162`) | **AGREE** | `PortfolioPage.tsx:162`: `useEffect` depends on `[activePortfolio?.portfolio_id, activePortfolio?.current_value]`. Because market ticks update `current_value` on every holding price change, `POST /api/portfolio/compounding` is re-dispatched on every single market tick without debounce or abort controller. |
| **2.3** | ModalSheet clipped inside GlassCard (`LearningHub.tsx:203, 316`) | **AGREE** | `GlassCard.tsx:26` applies `backdrop-blur-md` and `overflow-hidden`. Per W3C CSS Filter Effects and CSS Transforms, non-none `backdrop-filter` forces the card to establish a new containing block for `position: fixed` descendants. Descendant `ModalSheet.tsx:48` (`fixed inset-0`) is constrained to the GlassCard boundaries and clipped by `overflow-hidden`. On Chrome and Android WebView, modal sheets render trapped inside the learning card. |
| **2.4** | Div onClick discovery cards (`StockCard.tsx:78`, `LearningHub.tsx:156`) | **AGREE** | `StockCard.tsx:78-85` and `LearningHub.tsx:156-159` use `<motion.div onClick={...}>` and `<div onClick={...}>` with no `role="button"`, no `tabIndex={0}`, and no keyboard listeners (`onKeyDown`). They are completely invisible to keyboard Tab order and assistive switch controllers. |
| **2.5** | ModalSheet missing focus trap and focus restore (`ModalSheet.tsx`) | **AGREE** | `ModalSheet.tsx` declares `role="dialog"` and `aria-modal="true"`, but does not manage focus: active focus remains on the background trigger; Tab escapes to underlying DOM elements; closing the sheet fails to restore focus to the trigger; and `title` is not wired via `aria-labelledby`. |
| **2.6** | PortfolioPage light-theme contrast failure (`PortfolioPage.tsx:272`) | **AGREE** | `PortfolioPage.tsx:272`: `<h1 className="text-xl sm:text-2xl font-black text-white tracking-tight">`. In `index.css:7`, light mode `--bg-primary` is `#F8FAFC`. White text (`#FFFFFF`) on `#F8FAFC` produces a contrast ratio of **~1.04:1** (pure illegibility). Subtitle `text-slate-400` produces **~2.5:1**, failing WCAG AA (minimum 4.5:1). |
| **2.7** | Zoom disabled in viewport (`index.html:5`) | **AGREE** | `index.html:5`: `<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />`. Forcibly disables pinch-zoom, directly violating WCAG 2.1 Success Criterion 1.4.4 (Resize text). |

---

## 2. In-Depth Adversarial Analysis: Corrections & Tightening

### 2.1 The `0 || fallback` Assertion Nuance
- **Auditor Claim:** `metrics?.total_return_pct?.toFixed(1) || "48.5"` causes genuine 0% return to render as `+48.5%`.
- **Adversarial Check:**
  ```javascript
  const val = 0;
  console.log(val?.toFixed(1) || "48.5"); // Output: "0.0"
  ```
  Because `"0.0"` is truthy, this exact line does not turn `0` into `48.5`.
- **Correction:** The audit report should state that `x?.toFixed(n) || "fallback"` is dangerous when `x` is `null` or `undefined` (masking missing data).
- **The True Zero Bug:** Unformatted numeric expressions using `||` in the same component *do* corrupt genuine zeros:
  - `ProToolsBacktester.tsx:336`: `backtestResult.metrics?.winning_trades || 18` -> `0 || 18` yields `18`.
  - `ProToolsBacktester.tsx:337`: `backtestResult.metrics?.losing_trades || 10` -> `0 || 10` yields `10`.
  - `TopRecommendations.tsx:74`: `stock.growth_6m_base_pct || 12.5` -> `0 || 12.5` yields `12.5`.
  - `AdaptiveHomeCard.tsx:17, 22`: `activePortfolio.day_pnl ?? 420.5` -> defaults missing data to positive profit.
  - `Step4ResultsOverview.tsx:48`: `basket?.active_regime || "Low-Volatility Bull"` -> fabricates market regime.

### 2.2 PortfolioPage Fix Feasibility (`useAppStore` Contract)
- **Auditor Suggestion:** Use functional state updater: `setPortfolios(prev => prev.map(...))` to eliminate the stale closure.
- **Adversarial Check:**
  Examine `src/frontend/store/useAppStore.ts:179-199`:
  ```typescript
  setPortfolios: (portfolios) => {
    if (typeof window !== "undefined" && window.localStorage) {
      window.localStorage.setItem(PORTFOLIOS_STORAGE_KEY, JSON.stringify(portfolios));
    }
    set((state) => {
      // ...
      return { portfolios, activePortfolioId: nextActiveId };
    });
  }
  ```
  `useAppStore`'s `setPortfolios` accepts **only a raw `PortfolioData[]` array**, NOT an updater function `(prev: PortfolioData[]) => PortfolioData[]`. Calling `setPortfolios(prev => ...)` in `PortfolioPage.tsx` will fail type checks and break `localStorage.setItem(JSON.stringify(portfolios))`.
- **Correction for Fix Phase:**
  The fix phase must update `useAppStore.ts` to either:
  1. Support `portfolios: PortfolioData[] | ((prev: PortfolioData[]) => PortfolioData[])`; or
  2. Provide a specialized store action `updateHoldingTick(symbol: string, tick: MarketTick)` that updates holdings and recalculates portfolio P&L atomically inside Zustand, eliminating both the stale closure in `PortfolioPage` and the synchronous `localStorage.setItem` per tick.

### 2.3 `useAbortableRequest` Controller Deregistration (M8)
- **Auditor Finding:** `hooks/useAbortableRequest.ts:76` calls `abortRegistry.unregister(key)` with no controller argument, prematurely removing newer controllers when an earlier request is superseded.
- **Adversarial Check:**
  In `services/abortRegistry.ts:12-25`:
  `register(key: string): AbortSignal` returns **only the signal**, not the `AbortController` instance.
  In `services/abortRegistry.ts:59-64`:
  `unregister(key: string, controller?: AbortController)` checks `if (!controller || existing === controller)`. Because `useAbortableRequest.ts` does not have access to the controller instance, it cannot pass it.
- **Correction for Fix Phase:**
  `AbortRegistry.register(key)` must return `{ signal: AbortSignal, controller: AbortController }` (or an unregister token/callback), allowing `useAbortableRequest.ts` to unregister strictly its own controller in its `finally` block.

---

## 3. Missed & Underemphasized Issues in Original Audit

1. **Test Suite Locks in Fabricated Data (Critical for CI):**
   `tests/frontend/modals/NotificationDrawer.test.tsx:19-20` explicitly asserts:
   ```typescript
   expect(screen.getByText("Market Regime Active: Bull Market")).toBeInTheDocument();
   expect(screen.getByText("Asset Allocation Drift Notice")).toBeInTheDocument();
   ```
   Removing the hardcoded mock notifications in `NotificationDrawer.tsx` will immediately break this test. The fix phase must rewrite this test to assert the offline/empty state.

2. **Uncaught Unhandled Rejection on Compounding Fetch:**
   In `PortfolioPage.tsx:130-143`, `loadTrajectory()` calls `request("portfolio-compounding", "/api/portfolio/compounding", { method: "POST", ... })`. If the request fails, the catch block (`:148-150`) falls back to `getDemoCompoundingTrajectory()`, but `request()` throws before returning unless caught. Because it runs unmocked in `PortfolioPage.test.tsx`, it produces unhandled promise rejections and React `act(...)` warnings.

3. **Silent Review Filter Bypass (S29):**
   In `Step5DeepDive.tsx:316-350`:
   ```tsx
   {dynamicReviews.length > 0
     ? dynamicReviews.map(...) // Entire dynamic array mapped without filter!
     : filteredReviews.map(...) // Only sample reviews respect activeReviewCategory
   }
   ```
   When the backend actually returns reviews, the category filter tabs ("Transparency", "Educational", "Usability") become completely non-functional dead controls.

---

## 4. Guidance for the Fix Phase

When implementing the fixes:

1. **Data Honesty:**
   - Replace fabricated market metrics with clear empty/loading/offline indicators (`—` or `<StaleBadge status="offline" />`).
   - Replace `|| "48.5"` or `|| 12.5` with nullish checks `x == null ? "—" : x.toFixed(n)`.
   - Never default `winning_trades` or `losing_trades` to positive non-zero integers with `||`.
2. **Store & Tick Architecture:**
   - Refactor `useAppStore.ts` so `setPortfolios` can accept functional updates or introduce a dedicated action `updatePortfolioHoldingPrice(tick)`.
   - Debounce `localStorage.setItem` for portfolios (e.g. 500ms) or move it to window `beforeunload` and infrequent checkpoints.
   - Decouple compounding projection from `activePortfolio.current_value` so it only fetches on portfolio selection or explicit user interaction.
3. **Modal Rendering:**
   - In `ModalSheet.tsx`, wrap the rendered sheet in `createPortal(..., document.body)` so modals escape parent CSS containing blocks (such as `GlassCard`'s `backdrop-blur-md` and `overflow-hidden`).
   - Add focus trapping and return focus to the trigger on close.
4. **Accessibility & Contrast:**
   - Convert `StockCard` and `LearningHub` concept cards to `<button type="button">` or `<motion.button>`.
   - Replace hardcoded `text-white` in `PortfolioPage.tsx:272` with `text-[var(--text-main)]`.
   - Remove `maximum-scale=1.0, user-scalable=no` from `index.html`.
5. **Test Maintenance:**
   - Update `NotificationDrawer.test.tsx` to assert loading/offline states instead of hardcoded strings.
   - Mock network and `EventSource` in `PortfolioPage.test.tsx` to eliminate test `act(...)` warnings.

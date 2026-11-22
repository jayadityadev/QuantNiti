# Frontend Audit — QuantNiti (`src/frontend/**`, `index.html`, `vite.config.ts`, `tailwind.config.js`)

Auditor: adversarial frontend + a11y review. **Read-only**: no source was modified.
Scope: React 18 + Vite + TS + Tailwind + Zustand + Framer Motion + Chart.js, PWA + Capacitor Android, mobile-first for Indian retail beginners.

**Headline:** the engineering scaffolding is decent (build passes, abort registry exists, one modal primitive, one chart wrapper, PWA shell precached), but the product has a systemic integrity defect: **when an API fails, the app invents plausible financial numbers and presents them as live** — NIFTY price, portfolio P&L, backtest metrics, ESG scores, community reviews, market regime. For a first-time investor in a paper-trading app, that is worse than an error message. The second systemic defect is that **the two primary discovery surfaces (stock cards, learning cards) are `<div onClick>`** — unusable by keyboard/switch users — and **modals have no focus management**.

---

## Evidence collected

### `npm run build` — PASS

```
> tsc && vite build
vite v6.4.3 building for production...
✓ 2028 modules transformed.
dist/index.html                              1.70 kB │ gzip:   0.82 kB
dist/assets/index-B-XWNszT.js              228.00 kB │ gzip:  54.70 kB
dist/assets/vendor-react-DfLoQNdm.js       181.02 kB │ gzip:  59.63 kB
dist/assets/vendor-charts-DlUnshmL.js      175.26 kB │ gzip:  61.34 kB
dist/assets/vendor-motion-C3LQ1OXF.js      115.44 kB │ gzip:  38.31 kB
dist/assets/vendor-icons-Cpk3wOA8.js        31.24 kB │ gzip:   6.77 kB
dist/assets/PortfolioReportCard-*.js         5.09 kB │ gzip:   1.44 kB
dist/assets/index-*.css                     54.56 kB │ gzip:   9.27 kB
✓ built in 11.42s
```

Built `index.html` contains `<link rel="modulepreload" href="/static/dist/assets/vendor-charts-...js">` — **Chart.js (61 kB gzip) is downloaded on first paint for every visitor**, including the onboarding splash.

### Targeted vitest — PASS (19 tests, 4 files, 5.75 s)

```
npx vitest run tests/frontend/unit/hooks/useAbortableRequest.test.tsx \
  tests/frontend/unit/pages/ExplorePage.test.tsx \
  tests/frontend/modals/NotificationDrawer.test.tsx \
  tests/frontend/portfolio/PortfolioPage.test.tsx
→ Test Files 4 passed (4) | Tests 19 passed (19)
→ stderr: 4× "An update to PortfolioPage inside a test was not wrapped in act(...)"
→ stderr: React does not recognize the `layoutId` prop on a DOM element (framer-motion mock)
```

Suite is green; the warnings are symptoms, not flakiness (see §7).

### Verified non-issues (do not spend time here)

- `index.html` manifest/icon paths and `/static/dist/...` base are consistent in the build output.
- `main.tsx` registering `/sw.js` with scope `/` works: backend `src/app/api/app.py:128-134` serves `/sw.js` with `Service-Worker-Allowed: /`.
- **XSS: clean.** Zero `dangerouslySetInnerHTML`, `innerHTML`, or `eval` in `src/frontend`. All review/chat/user text is rendered as JSX text. `window.open` in `VideoFacades.tsx:87` passes `noopener,noreferrer`. The only `iframe` is a hardcoded `youtube-nocookie` embed (`LearningHub.tsx:326`). No unsafe URL construction from user input.
- No `localStorage` JSON parse without a guard; no token in storage.
- `DemoPortfolio.tsx` is the *correct* honesty pattern (explicit "This is a demo portfolio" + `isDemo` badges). Use it as the template for the fixes below.

---

## MUST-FIX

### M1. Fabricated market/portfolio/backtest data rendered as real when requests fail

This is one class of bug repeated in ten files. A beginner sees confident numbers with no "offline/demo" marker.

| Where | What is invented | User case |
|---|---|---|
| `components/home/MarketPulse.tsx:38-41` | `niftyPrice = 23010.0`, `+73.25`, `+0.32%`, `lastUpdated = "Live"` as *initial state*; a failed fetch leaves them forever | Airplane mode / backend down → "NIFTY 50 ₹23,010.00 +73.25 (+0.32%)" with a green "Market Open" pill. Beginner believes the market is at a specific level. |
| `components/portfolio/PortfolioPage.tsx:171-221` | "New Goal" fabricates holdings from `DEMO_HOLDINGS` at hardcoded prices, and sets `pnl_1d: Math.round(invested_amount * 0.008)`, `pnl_1d_pct: 0.8` — a **guaranteed fake +0.8% daily profit** | User creates a ₹50,000 goal → sees "+₹400 (+0.8%)" 1D P&L and a `LIVE STREAM` badge (`PortfolioHeroCard.tsx:34-39`) for money that was never invested. |
| `components/explore/ProToolsBacktester.tsx:63-125` | On any error, a full fake result: `total_return_pct 48.5`, `sharpe 1.45`, `win_rate 64`, `total_trades 28`, plus a fabricated `equity_curve` | User taps "Run Backtest" offline → a +48.5% strategy with 64% win rate, indistinguishable from a real run. |
| `components/explore/ProToolsBacktester.tsx:368-405` | The "Equity Curve" SVG is **three hardcoded `path` strings**; `backtestResult.equity_curve` is never read | Every strategy, every asset, every user sees the identical curve. The chart cannot contradict the fake metrics. |
| `components/explore/ProToolsBacktester.tsx:301,304,313,323,333` | `metrics?.total_return_pct?.toFixed(1) \|\| "48.5"` | A genuine **0% return renders as +48.5%** (`0 \|\| "48.5"` → `"48.5"`). Same `\|\|` pattern at `StockProfileModal.tsx:295,318,328,338,348,358`. |
| `components/grow/Step5DeepDive.tsx:24-55` | `SAMPLE_REVIEWS`: "Arjun M. (Bengaluru)", "Pooja S. (Mumbai)", 5 stars, under a heading "Community Reviews & Legitimacy" | Fabricated testimonials with fake names/cities presented as social proof in a SEBI-adjacent fintech product. Also `:100-104` fake benchmarks (QuantNiti 9.8% vs NIFTY 6.2%), `:92-98` fake ESG 78.4, `:187` "68.4% Backtested Win Rate", `:213` "Save ~₹3,200/yr". |
| `components/explore/StockProfileModal.tsx:102-169` | `generateFallbackProfile` returns price ₹2,450, RSI 61.5, "Strong Buy" suitability, 4 forecast cones — **for any symbol** | Tap TCS while offline → a "360° Intelligence Profile" for TCS at ₹2,450 with a Strong Buy badge. |
| `pages/ExplorePage.tsx:26-197` | `DEFAULT_STOCKS` with real tickers, real-looking prices, "Strong Buy" badges | Same, at list level: 10 stocks with prices from an unknown date. |
| `components/modals/NotificationDrawer.tsx:30-58` | Hardcoded alerts ("Market Regime Active: Bull Market", "10 mins ago") kept when polling fails | User is told the regime is Bull with a fake timestamp. |
| `components/home/RegimeRadar.tsx:32-37` | Fallback `{regime:"BULL", probabilities:{0.65,0.25,0.1}, confidence:0.82}` | Regime gauge shows a confident Bull reading that no model produced. |
| `components/home/TopRecommendations.tsx:29-34,74` | Fallback picks + `const growth = stock.growth_6m_base_pct \|\| 12.5` | A stock with 0/undefined forecast is displayed as "+12.5% (6M)". |
| `components/home/AdaptiveHomeCard.tsx:17,22` | `dayPnl = activePortfolio.day_pnl ?? 420.5`, `alpha = ... ?? 2.8` | A missing field becomes a green "+₹421" 1D P&L. |

**Smallest fix (one seam, not ten):** add `src/frontend/components/ui/DataState.tsx` exporting a `StaleBadge` + a `useAsyncData` hook that returns `{data, status: 'live'|'stale'|'offline'|'demo'}`. Then, per surface: delete the fabricated fallback, keep the last good value, and render `<StaleBadge status="offline" asOf={lastUpdated} />` ("Offline — last updated 09:41 IST"). Where a demo value is genuinely useful for first-run (ExplorePage, Step5), keep it **only** behind the `isDemo` badge pattern already used by `DemoPortfolio.tsx`, and label reviews `Sample` instead of a person's name. Also replace every `x?.toFixed(n) || "48.5"` with `x == null ? "—" : x.toFixed(n)`.

### M2. `PortfolioPage` tick handler corrupts state and hammers the API

`components/portfolio/PortfolioPage.tsx:69-117`

```tsx
const unsubscribe = marketStream.subscribe((tick) => {
  setPortfolios(portfolios.map(...))   // `portfolios` captured at effect time
});
...
}, [activePortfolio?.portfolio_id, activePortfolio?.holdings?.length]);  // :117
```

- `portfolios` is a stale closure. Create a second goal while the stream is live (`holdings.length` unchanged → effect does not re-run): the next tick writes back the **old array** and the new portfolio vanishes from the UI *and* from `localStorage` (because `setPortfolios` persists synchronously — `store/useAppStore.ts:179-199`).
- Every tick calls `setPortfolios` → a synchronous `localStorage.setItem` of all portfolios. On a 1 s tick cadence with 20 holdings that is a main-thread write per second on a low-end Android device.
- `:162` — the trajectory effect depends on `activePortfolio?.current_value`, which changes on **every tick**, so `POST /api/portfolio/compounding` is fired on every price update (request storm; the 600 ms `setTimeout`-free POST is not debounced or aborted).

**Smallest fix:** functional update — `setPortfolios(prev => prev.map(...))` and drop `portfolios` from the closure; move the `localStorage` write out of `setPortfolios` into a debounced (500 ms) subscriber; change the trajectory effect to depend on `activePortfolio?.portfolio_id` only (plus an explicit "Refresh projection" button), not `current_value`.

### M3. Modals rendered inside `GlassCard` are clipped and mis-positioned

`components/home/LearningHub.tsx:203-313` and `:316-340` render `<ModalSheet>` **inside** a `<GlassCard>`.

`GlassCard.tsx:26` applies `backdrop-blur-md` **and** `overflow-hidden`. Per CSS Filter Effects, a non-`none` `backdrop-filter` makes the element a **containing block for `position: fixed` descendants**, and `overflow-hidden` then clips them. `ModalSheet.tsx:48,57` are `fixed inset-0`.

**User case (Chrome/Android WebView, i.e. the actual Capacitor target):** tap a learning card → the "concept detail" sheet appears as a small panel *inside* the learning-hub card, its backdrop covering only that card, with the page still scrollable behind it. Same for the video modal.

**Smallest fix:** render `ModalSheet` through `createPortal(document.body)` (one change inside `ModalSheet.tsx`), or hoist both modals out of `LearningHub` into `ModalRoot`. Portal is the smaller, global fix — it also protects every future modal.

### M4. Light theme: invisible and low-contrast text on the Portfolio screen

`components/portfolio/PortfolioPage.tsx:272-275`

```tsx
<h1 className="... text-white ...">Portfolio Page</h1>
<p className="text-xs text-slate-400">…</p>
```

`index.css` light `--bg-primary` is `#F8FAFC`. White on `#F8FAFC` ≈ **1.06:1** — the page title is effectively invisible for every light-mode user (the default). `slate-400` on `#F8FAFC` ≈ 2.5:1 (fails AA 4.5:1).

Same class of bug: `components/portfolio/HoldingsTable.tsx:21,24,35` (`text-slate-300`, `text-slate-400` for the empty state and section header), `components/grow/Step3Persona.tsx:127` (`bg-slate-100 text-slate-700` is fine, but the `dark:`-only pairs elsewhere drift), `Header.tsx` menu items rely on `--text-main`.

**Smallest fix:** replace hardcoded `text-white`/`text-slate-3|400` on page-level text with `text-[var(--text-main)]` / `text-[var(--text-muted)]` (PortfolioPage h1/p, HoldingsTable header + empty state). Then add a CI check: `rg "text-(white|slate-[34]00)" src/frontend/components src/frontend/pages` and require an explicit `dark:`-scoped or dark-surface justification.

### M5. Stock cards and learning cards are not keyboard-operable

- `components/explore/StockCard.tsx:78-85`: `<motion.div onClick={() => onSelect(stock)} className="cursor-pointer select-none">` — no `role`, no `tabIndex`, no `onKeyDown`.
- `components/home/LearningHub.tsx:156-159`: same pattern for every concept card.

**User case:** a keyboard-only or switch-access user (common on cheap Android tablets with external keyboards, and the only path for motor-impaired users) can Tab through the header and filters but **can never open a stock profile or a concept**. The two main discovery flows are touch-only.

**Smallest fix:** render a real `<button type="button">` as the outer element (keep `motion.button`), or add `role="button" tabIndex={0} onKeyDown={e => (e.key === "Enter" || e.key === " ") && (e.preventDefault(), onSelect(stock))}`. Prefer the button — it also gets Enter/Space, focus ring, and correct screen-reader role for free. Add an `aria-label` that includes price and change ("RELIANCE, ₹2,980.50, up 1.19%").

### M6. `ModalSheet` has no focus management

`components/ui/ModalSheet.tsx` — has `role="dialog" aria-modal="true"` (`:62-63`), Esc and backdrop close (`:35-43`), scroll lock (`:24-32`). Missing: initial focus, focus trap, focus restore, `aria-labelledby`/`aria-describedby`, `inert` on the background.

**User case:** keyboard user opens Notifications → focus stays on the bell button *behind* the dialog; Tab walks through the page behind the sheet; Esc closes but focus is lost to `<body>`, so the next Tab restarts at the top of the app. Screen readers announce "dialog" with **no name** because `title` is a `ReactNode` and never wired to `aria-labelledby`.

**Smallest fix:** in `ModalSheet`, on open: store `document.activeElement`, focus the sheet container (`tabIndex={-1}`), trap Tab within it, restore focus on close; add `id="modal-title"` to the title node and `aria-labelledby="modal-title"`. ~30 lines, fixes all 9 modals.

### M7. `index.html:5` disables pinch-zoom

`<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">`

**User case:** a 55-year-old first-time investor cannot pinch to read a 9 px range label (`StockCard.tsx:170`, `text-[9px]`) or a dense holdings table. WCAG 1.4.4 failure; iOS Safari also ignores it, so the "benefit" (no accidental zoom) is not even delivered consistently.

**Smallest fix:** drop `maximum-scale` and `user-scalable`. If accidental double-tap zoom is the concern, use `touch-action: manipulation` on interactive elements instead.

### M8. `useAbortableRequest` unregisters the *wrong* controller

`hooks/useAbortableRequest.ts:76` — `finally { abortRegistry.unregister(key); }` with no controller argument. `abortRegistry.unregister(key, controller?)` only deletes when the controller matches (or is omitted). Because it is omitted, a **superseded** request's `finally` deletes the **new** request's controller from the registry.

**User case:** type in Explore search → request A starts; change sector → request B starts (A aborted, B registered); A's `finally` runs and removes B's controller. Now B cannot be aborted by `abortAll()` on navigation — its `setState` lands after unmount / after the user moved on. Compounded by `finally { setIsLoading(false) }`, which clears loading for a still-in-flight B (spinner flicker).

**Smallest fix:** capture `const controller = abortRegistry.register(key)` at the top and call `abortRegistry.unregister(key, controller)` in `finally`; only `setIsLoading(false)` if `abortRegistry.get(key) === controller` (or track a per-call `isCurrent` flag).

### M9. Order sheet reports "Copied!" even when the copy failed

`components/modals/OrderSheetModal.tsx:39-46`

```tsx
navigator.clipboard.writeText(text);
setIsCopied(true);
setTimeout(() => setIsCopied(false), 1800);
```

Not awaited, no `.catch`, no feature check.

**User case (the Capacitor/Android WebView case specifically):** `navigator.clipboard` is `undefined` on a non-secure origin and can reject on permission denial inside a WebView. The user gets a green "Copied!" and pastes nothing into Groww — a failed trade instruction with a success confirmation. Also `setTimeout` is never cleared on unmount (`setState` after unmount).

**Smallest fix:** `try { await navigator.clipboard.writeText(text); setIsCopied(true); } catch { setError("Copy failed — long-press to select"); }`, clear the timeout in a cleanup effect, and fall back to a `document.execCommand('copy')`/selectable `<textarea>`.

### M10. `CreatePortfolioModal` submits twice

`components/portfolio/CreatePortfolioModal.tsx:104-106` — `<PrimaryButton type="submit" onClick={handleSubmit}>` inside a `<form onSubmit={handleSubmit}>`. One tap fires `click` → `handleSubmit`, then native submit → `handleSubmit` again.

**User case:** two `POST`s (once the handler is wired to the API, which is the obvious next step) → duplicate portfolio; today it double-runs the synthetic builder and produces two `port_<Date.now()>` entries within the same millisecond. Also `handleSubmit` has `try/finally` with **no `catch`**, so a rejected `onCreate` leaves the modal open with zero feedback.

**Smallest fix:** remove `onClick` (let the form submit), and add `catch (e) { setError(...) }`.

### M11. Chart.js in the first-paint bundle

`AppShell.tsx` statically imports `PortfolioPage`, which statically imports `CompoundingTrajectoryChart`, which imports `chart.js` + `react-chartjs-2`. `vite.config.ts:256-261` only splits it into a *separate* chunk — and `index.html` `modulepreload`s that chunk, so it is fetched on every first load (61 kB gzip of the 222 kB total).

**User case:** a user on 3G in Jaipur waits for Chart.js before the onboarding splash paints, for a chart they will not see until they own a portfolio.

**Smallest fix:** `const PortfolioPage = lazy(() => import(...))` (or lazy just the chart) inside `AppShell`'s `<Routes>`, wrapped in the existing `Suspense`. Drop `vendor-charts` from the preload list (Vite does this automatically for dynamic-import-only chunks).

### M12. No error boundary — one bad API field blanks the app

`StockProfileModal.tsx:219` calls `profile.day_change_pct.toFixed(2)` unguarded; `:474` calls `reviewsData.summary.average_rating.toFixed(1)` unguarded. Any profile response without `day_change_pct`, or a reviews payload with a null `average_rating`, throws during render.

**User case:** backend returns a partial profile for a newly listed symbol → the whole app unmounts to a white screen (React 18 unmounts the root on an uncaught render error), and the user's unsaved wizard answers are gone.

**Smallest fix:** add one `<ErrorBoundary>` around `<AppShell>` (and one around the modal subtree) with a "Something went wrong — reload" fallback; and change those two call sites to `(profile.day_change_pct ?? 0).toFixed(2)` / `Number(reviewsData.summary?.average_rating ?? 0).toFixed(1)`.

---

## SHOULD-FIX

### S1. `aria-live` does not exist anywhere in the app
`rg "aria-live" src/frontend` → 0 matches. Consequences: NitiBot replies are never announced (`NitiBotModal.tsx` chat log has no `role="log"`), new alerts in `NotificationDrawer` are silent, async errors in `GrowPage.tsx:349-353` appear without announcement, and `AnimatedNumber` price changes are invisible to screen readers (arguably fine) while *error* states are also invisible (not fine).
**Fix:** `role="log" aria-live="polite"` on the chat log; `role="status"` on the Grow error block and the notification list container.

### S2. Unlabeled inputs
- `ExplorePage.tsx:315-321` search input: placeholder only, no `<label>`/`aria-label`; clear button `:323-329` has an icon and no `aria-label`.
- `NitiBotModal.tsx:249-256` chat input: placeholder only.
- `WriteReviewModal.tsx:138,152,164,178` labels have no `htmlFor`; inputs have no `id` (same in `CreatePortfolioModal.tsx:59,75,91`).
**User case:** VoiceOver/TalkBack announces "text field" with no purpose; voice-control users cannot say "tap Your Name".
**Fix:** `aria-label` on the two icon/text-only inputs (2 lines); add `id`/`htmlFor` pairs in the two forms.

### S3. Tab semantics used for non-tabs
- `BottomNav.tsx:46-64`: `role="tablist"` + `role="tab" aria-selected` on navigation buttons, with **no `tabpanel`, no `aria-controls`, no arrow-key roving tabindex**.
- `SegmentedControl.tsx:34-44`: same, plus no `aria-controls`.
**User case:** a screen-reader user is told "tab 1 of 4, selected" and then expects arrow keys to move between tabs; arrow keys do nothing (they scroll the page), and the "tab" navigates to a new route instead of showing a panel — a broken mental model. Also every tab is in the tab order (should be one).
**Fix:** for `BottomNav`, drop `role="tablist"/"tab"` and use `aria-current="page"` on the active `<button>` inside a `<nav aria-label="Primary">`. For `SegmentedControl`, either add `tabIndex={isActive ? 0 : -1}` + ArrowLeft/Right handlers, or switch to `role="radiogroup"`/`radio`.

### S4. `RegimeBadge` is a fake button
`RegimeBadge.tsx:50-57`: `role={onClick ? "button" : "status"}` with `onClick` and `tabIndex={0}` but **no `onKeyDown`** → focusable, announced as a button, and Enter/Space do nothing.
**Fix:** add `onKeyDown` mirroring `StockCard`, or render a `<button>` when `onClick` is provided.

### S5. `ProgressBar` puts buttons inside a `progressbar`
`ProgressBar.tsx:18-57`: container `role="progressbar"` wraps `<button>` segments. ARIA forbids interactive descendants of `progressbar`; AT flattens or mis-announces them. Also `aria-valuenow={currentStep}` with `min=1` is fine, but there is no `aria-valuetext` ("Step 2 of 3, Horizon").
**Fix:** move `role="progressbar"` to an inner `<div>` and keep the buttons outside it; add `aria-valuetext`.

### S6. Header overflow menu has no focus management
`Header.tsx:26-45` closes on Esc and outside click, but does not move focus into the menu on open, does not support ArrowUp/Down, and does not restore focus to the trigger.
**Fix:** focus the first `menuitem` on open, ArrowUp/Down cycle, Esc returns focus to the trigger button.

### S7. No visible keyboard focus on the shared primitives
`focus-visible:ring` exists only in `Header.tsx:56,87,103,116` and `BottomNav.tsx:65`. `PrimaryButton`, `GhostButton`, `ChipButton`, `SegmentedControl`, `ModalSheet` close button, `StockCard`, `LearnChip` all rely on the browser default, which Tailwind's preflight removes (`outline: none` is not set, but `focus:outline-none` appears on many inputs: `ExplorePage.tsx:320`, `LearnPage.tsx:130`, `ProToolsBacktester.tsx:197,216,229`, `WriteReviewModal.tsx:145,159,170,187`).
**Fix:** add `focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-400 focus-visible:ring-offset-2` to the four button primitives once; replace `focus:outline-none` with `focus-visible:outline-none` + ring on inputs.

### S8. Reduced motion is opt-in per component, not global
`prefers-reduced-motion` appears only in `AnimatedNumber.tsx:24`; `useReducedMotion` is used in `AppShell`, `GrowPage`, `OnboardingHero`. **Not** respected by: `ModalSheet` (`slideUpVariants`), `GlassCard` (`fadeInUpVariants` on every mount), `StockCard` (`whileHover/whileTap`), `RegimeRadar` (`:86-124` width animations), `ProgressBar` (`:42-48`), `BottomNav` (`layoutId` pill), `Step1Capital.tsx:45-53` (`key={capital}` re-springs on every slider pixel), `TopRecommendations.tsx:77-81` (staggered `x`), `CompoundingVisualizer` (AnimatedNumber only).
**User case:** a vestibular-sensitive user sets Reduce Motion at OS level; opening any modal still slides a full-height sheet, and dragging the capital slider re-springs the number 200 times.
**Fix:** add one CSS block — `@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; transition-duration: .01ms !important; scroll-behavior: auto !important } }` — and gate `slideUpVariants`/`fadeInUpVariants` on `useReducedMotion()`.

### S9. `no-scrollbar` is a dead class
Used at `ExplorePage.tsx:334`, `LearningHub.tsx:135`, `LearningHub.tsx:149`, `VideoFacades.tsx:112`. Not defined in `index.css`, not a Tailwind plugin, not in `tailwind.config.js`.
**User case:** the sector chip row, the learning carousel, and the video pills all show a visible horizontal scrollbar on Android/Windows, which on a 240 px-tall carousel looks like a rendering bug.
**Fix:** add `.no-scrollbar::-webkit-scrollbar{display:none}` + `scrollbar-width:none` to `index.css` (or a Tailwind `@utility`).

### S10. `marketStream` has no refcount
`services/marketStream.ts`: `connect()` calls `disconnect()` first; `subscribe()` returns an unsubscribe that does **not** close the EventSource. `MarketPulse.tsx:98-103` connects and never disconnects; `PortfolioPage.tsx:112-116` connects and only unsubscribes.
**User case:** navigate Home → Portfolio → Home: two `connect()` calls in quick succession tear down and reopen the EventSource (server-side connection churn, and a visible gap in ticks). If `PortfolioPage` ever called `disconnect()` on unmount it would silently kill Home's feed.
**Fix:** count subscribers — `subscribe` increments, the returned unsubscribe decrements and calls `disconnect()` at 0; `connect()` becomes idempotent.

### S11. Portfolio list fetch is fire-and-forget and can wipe local state
`PortfolioPage.tsx:39-51`: `fetch(apiUrl("/api/v1/portfolios"))` — no `AbortController`, no error surface, `.catch(() => {})`, and `setPortfolios(data)` **replaces** whatever the user created locally in the meantime (a race between "New Goal" and this GET).
**User case:** open Portfolio on a slow connection, create a goal before the GET resolves → the goal disappears when the response lands.
**Fix:** merge by `portfolio_id` (`setPortfolios(prev => mergeById(prev, data))`), abort on unmount, and surface a "couldn't load portfolios — retry" row instead of silence.

### S12. `window.confirm` for destructive delete
`PortfolioPage.tsx:231-234` — native confirm. Blocks the JS thread, is unstyled, is un-dismissible in some WebViews, and cannot be translated/styled; it also drops focus.
**Fix:** use `ModalSheet` with an explicit "Delete" danger button (the app already has the primitive).

### S13. Rebalance is theatre
`PortfolioPage.tsx:243-262`: `await new Promise(r => setTimeout(r, 600))`, then clears `rebalance_alert` locally. No API call. `RebalanceBanner` reports success.
**User case:** user taps "Apply Rebalance", sees a spinner, and believes holdings were rebalanced; nothing changed except the banner disappearing.
**Fix:** either call a real endpoint, or label the button "Dismiss recommendation" and say "Rebalancing is not available in paper mode yet".

### S14. Notification drawer: optimistic push state, no error path
`NotificationDrawer.tsx:104-111` sets `pushEnabled = true` *before* awaiting `subscribeUserToPush()` and ignores a `false` return. On Android where push permission is denied or VAPID key fetch fails, the toggle shows "enabled" and no notification will ever arrive. `:62-93` polls every 45 s but never aborts the in-flight request on close (the component stays mounted; only the interval is cleared), and `mark-all-read` is local-only with no persistence — reopening the drawer resurrects unread dots.
**Fix:** `setPushEnabled(await subscribeUserToPush())`; abort on close via `abortRegistry.abort('fetch-alerts')`; persist read state (or call a `PATCH /alerts/read`).

### S15. Header bell always shows an unread dot
`Header.tsx:92-95` renders the dot unconditionally, not tied to `alerts.length`/unread state, and the dot has no `aria-hidden` (so it may be announced as content) while the button has no unread count in its accessible name.
**Fix:** `{unreadCount > 0 && <span aria-hidden="true" .../>}` and `aria-label={`Notifications${unreadCount ? `, ${unreadCount} unread` : ''}`}`.

### S16. NitiBot leaks an ops detail and loses source links
- `NitiBotModal.tsx:107` error text tells the user to set `GEMINI_API_KEY`. That is an operator secret-shaped string; users cannot act on it, and it advertises the vendor.
- `:44-57` `/api/chat/status` fetch has no abort; closing the modal mid-flight still `setState`s.
- Sources are rendered as `<span>` with an `ExternalLink` icon (`:`) — visually links, not clickable, not focusable.
**Fix:** user-facing copy "Assistant is unavailable right now — try again in a minute" and log the detail; pass the abort signal; render `<a href={source.url} target="_blank" rel="noopener noreferrer">` with a host allow-list.

### S17. `WriteReviewModal` prefills a fabricated claim
`:28` `claimedReturn` defaults to `"+12.4%"` — a number the user never entered, submitted to an "AI fact-checker" that may approve or reject based on it. Also `:74-77` `setTimeout(..., 1400)` calls `onClose` without cleanup (close the modal within 1.4 s and the timeout still fires, calling `onSuccess` on an unmounted tree); the star rating is 5 buttons with no `role="radiogroup"`/`aria-checked` so the selection is not conveyed; the AI badge block `:192-198` claims "SEBI advertisement compliance" that nothing in this code verifies.
**Fix:** default `claimedReturn` to `""`; store the timeout in a ref and clear it in the `isOpen` effect; make the stars a radiogroup; soften the compliance claim.

### S18. `ExplorePage` effect has a stale `allExploreStocks` closure and no loading state
`:209-234` deps `[setAllExploreStocks]` only, but the handler reads `allExploreStocks.length` (`:220`, `:226`) from the first render. If the API returns `[]` after the store was already populated elsewhere (`TopRecommendations` also writes `allExploreStocks`), the code overwrites real data with `DEFAULT_STOCKS`. There is no loading skeleton and no error banner — an offline first load silently shows demo stocks (see M1).
**Fix:** read the store inside the handler (`useAppStore.getState().allExploreStocks`), or add the missing dep and guard with a ref; add `isLoading`/`error` and render a skeleton + retry.

### S19. Two `<h1>`s on Explore; heading order broken
`ExplorePage.tsx:291` `<h1 className="sr-only">Explore Page</h1>` **and** `:301` `<h1>Explore Universe</h1>`. Screen readers announce two top-level headings. `HomePage.tsx:39` uses `sr-only` h1 while every visible card title is `h3` (`MarketPulse.tsx:119`, `RegimeRadar.tsx:65`, `TopRecommendations.tsx:53`, `AdaptiveHomeCard.tsx:36/143`) — no `h2` anywhere, so the document outline is h1 → h3 ×5.
**Fix:** delete the `sr-only` h1 on Explore; in the home cards use `h2` for card titles (they are siblings of the page h1).

### S20. Video "Masterclasses" are search-result links with invented durations
`VideoFacades.tsx:23,38,53,68` — every `watchUrl` is a YouTube **search query**, and `duration` ("14:20") / `keyTakeaways` describe videos that are not those results. The CTA says "Watch Video on YouTube" (`:178`).
`LearningHub.tsx:326` embeds **one hardcoded video id** (`5k3f_eU1j3Q`) for *every* concept's `video` object, and the modal title is the concept's own title → "Play Video" on "Sharpe Ratio" plays whatever that id is.
**Fix:** label the button "Search YouTube for this topic", drop the fake durations, and only show "Play" when `video.video_id` exists (build the embed from it).

### S21. `CompoundingTrajectoryChart` is an inaccessible canvas and refetches per tick
- Canvas has no text alternative: no `role="img"`, no `aria-label`, no adjacent data table. A screen-reader user gets "canvas" and nothing else.
- `isDemo` prop is accepted and ignored (`:36-38`), so a demo trajectory cannot be badged here (unlike `PortfolioHeroCard`).
- Driven by M2: the parent refires the POST on every tick, so the chart's `useMemo` re-runs and Chart.js re-animates continuously during market hours on a phone.
**Fix:** `role="img" aria-label={summarise(trajectory)}` plus a visually-hidden `<table>` of the 10 yearly Q10/Q50/Q90 values; wire `isDemo` to a badge; debounce the fetch (M2).

### S22. PWA/service-worker activation can break the current page
`vite.config.ts` SW: `install` → `skipWaiting()`; `activate` → delete every cache except the new `CACHE_VERSION` + `clients.claim()`.
**User case:** a user has the app open on `index-OLD.js`; a new deploy activates and deletes the old cache; the user then triggers the lazy `PortfolioReportCard` chunk → 404 → unhandled dynamic-import rejection → blank report card (or app, without an error boundary). Also `fetch` caches **any** 200 response, including cross-origin/opaque responses from the YouTube iframe host, and `activate` wipes *all* same-origin caches (any other app on the domain).
**Fix:** keep the previous cache for one generation (delete only `name !== CACHE_VERSION && name !== PREVIOUS`), skip caching `response.type !== 'basic'`, and add a `vite:preloadError` / `unhandledrejection` listener that calls `location.reload()` once.

### S23. Zustand: whole-store subscriptions everywhere
`AppShell.tsx:20`, `ModalRoot.tsx:19-27`, `ExplorePage.tsx:200-201`, `GrowPage.tsx:21-35`, `PortfolioPage.tsx:22-30`, `LearningHub.tsx:12-19`, `RegimeRadar.tsx:13`, `AdaptiveHomeCard.tsx:12`, `TopRecommendations.tsx:14`, `Step5DeepDive.tsx:65` (this one is fine — selector).
**User case:** every SSE tick writes `portfolios`; `AppShell` (which renders the whole route tree) re-renders on *every* store write, including `activeAsyncKeys` add/remove on each request. On a low-end Android device this is the difference between 60 fps and jank while scrolling the Explore list during market hours.
**Fix:** convert the hot ones to selectors (`useAppStore(s => s.x)`) — start with `AppShell` and `ExplorePage`. Also drop `activeAsyncKeys` from the store (it is request bookkeeping, not UI state) or keep it out of any component subscription.

### S24. `setPortfolios` persists synchronously on every call
`store/useAppStore.ts:179-199` — `localStorage.setItem` inside the setter, plus an auto-fix of `activePortfolioId`. With M2 this is a write per tick; it also makes `setPortfolios` non-idempotent under concurrent calls.
**Fix:** subscribe to `portfolios`/`activePortfolioId` once and persist debounced (300-500 ms) in a `subscribe` callback.

### S25. Modal history entries accumulate; Back double-fires
`useAppStore.ts:245-250` pushes a history entry on `openModal`; `closeModal` (`:252-254`) never pops. `ModalRoot.tsx:30-39` listens for `popstate` and closes.
**User case:** open and close 6 modals, then press Android Back once → you are dragged through 6 dead history entries (each one briefly "closes" a modal that is already closed, and `popstate` handlers race). Combined with `HashRouter`, Back may also change route unexpectedly.
**Fix:** in `closeModal`, if the top history state is `{modalOpen:true}`, call `history.back()`; or use `history.replaceState` instead of `pushState` and let Esc/backdrop be the only close paths.

### S26. `NotificationDrawer` polling deps and fake mark-read
`:62-93` effect deps `[isOpen]` with `request` used inside (stable today only because `useAbortableRequest` memoises on stable registry functions — fragile). `mark-all-read` never calls the API, so the bell dot (S15) and the list disagree after reload.
**Fix:** add `request` to deps and implement `PATCH /api/alerts/read-all`, or persist read ids locally.

### S27. `OrderSheetModal` leaks blob URLs and silently no-ops
`:48-57` `URL.createObjectURL(blob)` is never `revokeObjectURL`'d — on a long session with repeated exports this pins memory (each CSV is small, but the pattern is a leak and repeats elsewhere if copied). `:22` `if (!portfolio) return null` means opening the sheet with no active portfolio does **nothing at all** — no message, no disabled state; the button in `PortfolioPage.tsx:296-305` is always enabled.
**Fix:** `const url = URL.createObjectURL(...); ...; setTimeout(() => URL.revokeObjectURL(url), 0)`; disable the Order Sheet button when `!activePortfolio` and add a title explaining why.

### S28. `GrowPage` fallback portfolio on failure is indistinguishable from success
`GrowPage.tsx:98-137`: if activation returns no `portfolio_id` **or throws**, it fabricates `port_${Date.now()}` with `total_pnl: 0` and navigates to Portfolio as if it worked. The user's basket was never activated server-side; the local portfolio will not survive a device change and its P&L will drift from any real data.
**Fix:** on failure, stay on Step 4 and show "Couldn't activate — retry" with the `error` already rendered at `:349-353`; only use the local fallback behind an explicit "Continue in offline paper mode" choice.

### S29. `Step5DeepDive` review filter is bypassed
`:316-349`: when `dynamicReviews.length > 0`, the list renders **all** dynamic reviews and ignores `activeReviewCategory` (the chips only filter `SAMPLE_REVIEWS`). The chips therefore do nothing for real data — a silent dead control.
**Fix:** filter `dynamicReviews` by the selected category (or hide the chips when categories are unavailable).

### S30. `LearnPage` comparison is un-abortable and double-fetches on mount
`:42-78`: raw `fetch` with no `AbortController`; rapid asset switching leaves out-of-order responses (`setComparisonResult` from an older symbol can land last — no guard, unlike `StockProfileModal` which does it right). `:76-78` calls `handleRunStrategyComparison("RELIANCE.NS")` on mount while `selectedSymbol` already defaults to `"RELIANCE.NS"`; the `<select>` `onChange` (`:126-129`) also calls it — fine, but `setIsLoading(false)` in `finally` will clear loading for a newer in-flight request.
**Fix:** use `useAbortableRequest` with key `backtest-compare` (the abort registry already solves this), and delete the mount call in favour of an effect keyed on `selectedSymbol`.

---

## NICE

### N1. Types are `any` end-to-end
`useAppStore.ts` (all `any`), `StockProfileModal` `profile: any`, `ProToolsBacktester` `backtestResult: any`, `LearnPage` `comparisonResult: any`, `reviewsData: any`. There is no runtime validation of API responses either (only `Array.isArray` checks), so a renamed backend field silently becomes `undefined` → then M1's `|| "48.5"` turns it into a confident wrong number.
**Fix:** define `StockProfile`, `BacktestResult`, `ReviewSummary` interfaces and validate at the fetch seam (a 20-line `assertShape` or zod if it is already a dependency); then the `any`s disappear naturally.

### N2. Dead code
- `utils/asyncGuards.ts:15` `createStaleGuard` — never imported (the hand-rolled guard in `StockProfileModal` duplicates it).
- `useAppStore.ts` `theme` + `setTheme` — duplicates `ThemeContext`; nothing reads them.
- `CompoundingTrajectoryChart` `isDemo` prop unused.
- `Header.tsx:73-80` regime pill has a `title` but no role/label; the value is not exposed.
- `AppShell` imports `IOSInstallBanner` eagerly for a component that renders `null` on Android (99% of the target audience) — 3 kB of lucide icons + a framer component in the critical path.
**Fix:** delete `createStaleGuard` (or use it), delete store `theme`, wire or drop `isDemo`, lazy the iOS banner.

### N3. Icon-only controls under 44 px
`ModalSheet` close `p-1.5` ≈ 28×28 (`:close button`), `Header` theme toggle `p-2` ≈ 36 px, `OrderSheetModal`/`PortfolioPage` action buttons `p-2` ≈ 32-36 px, `WriteReviewModal` star `p-1` + 24 px icon ≈ 32 px. WCAG 2.5.8 (AA, 24 px) passes; the practical Android target is 48 dp (`BottomNav` gets this right with `min-h-[48px]`).
**Fix:** `min-h-11 min-w-11` (44 px) on icon buttons, or `after:absolute after:inset-[-8px]` hit-area expansion.

### N4. Safe areas are partially applied
`index.css:58-86` defines `.pt-safe/.pb-safe/.bottom-nav-safe/.content-bottom-safe`, but `IOSInstallBanner.tsx:36` uses `bottom-20` (not `env(safe-area-inset-bottom)`) and `ModalRoot`'s FAB is `bottom-24 right-4` (`ModalRoot.tsx:98-109`), which can sit under the iOS home indicator and overlaps the last card on short screens. `tailwind.config.js` has no safe-area spacing tokens, so new code cannot use `pb-safe` idiomatically.
**Fix:** add `spacing: { safe: 'env(safe-area-inset-bottom)' }` and use `bottom-[calc(5rem+env(safe-area-inset-bottom))]` for the FAB/banner.

### N5. `AnimatedNumber` announces nothing and re-animates on every keystroke
It renders a plain `<span>` (no `aria-live`, which is correct for prices) but has no `aria-hidden` escape hatch either, so a screen reader reading the card gets a mid-animation value if it samples during the 500 ms tween. `Step1Capital.tsx:45-53` remounts it (`key={capital}`) on every slider step, restarting a spring per pixel.
**Fix:** render the final value in a visually-hidden `<span>` and mark the animated one `aria-hidden`; drop `key={capital}` in favour of the number animation only.

### N6. `formatCompactRupees` and `numberToIndianWords` edge cases
`formatters.ts:14-24` — `formatCompactRupees(999999)` → "₹10.0L" (rounds up past the unit boundary); `numberToIndianWords(100000)` → "One Lakh Only" (correct), but `numberToIndianWords(10000000)` → "One Crore Only" and `numberToIndianWords(100000000)` → "Ten Crores" — fine; `twoDigits(100)` is never called, but `crore` ≥ 100 (₹100 crore) produces `twoDigits(100)` → `""` → " Crore Only". Slider max is ₹10L so not reachable today; it is reachable from a basket capital.
**Fix:** guard `n >= 100` for crore/lakh groups by falling back to `threeDigits`.

### N7. `formatRupees` silently turns `null` into "₹0"
`formatters.ts:4-8` — `isNaN(null)` is `false`, `Number(null)` is 0, so `formatRupees(null as any)` → "₹0". Combined with M1 this hides missing data. `isNaN(undefined)` → true → "₹0" too.
**Fix:** `if (amount == null || !Number.isFinite(amount)) return "—";`

### N8. Tailwind: colour tokens bypassed
`tailwind.config.js` defines `accent/profit/loss`, but components hardcode `emerald-*`/`rose-*` (30+ sites) and the light/dark pairs are inconsistent (`text-emerald-500` in `AdaptiveHomeCard.tsx:75` has no `dark:` variant, `StockCard.tsx:123` does). The profit/loss tokens are effectively dead.
**Fix:** use `text-profit`/`text-loss` in the ~6 shared badge/metric components so a future palette change is one edit.

### N9. `SegmentedControl` default `layoutId` includes React's `:r0:` id
`SegmentedControl.tsx:26-27` — `useId()` returns `«r0»`/`:r0:`; using it inside a `layoutId` string is fine for Framer but produces odd DOM attributes and can collide across two instances that share an explicit `layoutId` prop. `ProToolsBacktester` passes none, so every instance is unique — OK today.
**Fix:** generate with `useId().replace(/[^a-zA-Z0-9]/g, "")`.

### N10. `NotificationDrawer` category chips lack `aria-pressed`
`:category chips` are toggle buttons with only a colour change. Add `aria-pressed={active === cat}`.

### N11. `ExplorePage` sector mapping is a 12-branch `if` chain
`:246-260` — a 10-entry sector list maps to substring heuristics that disagree with the `SECTORS` labels ("Consumer Goods" vs backend `"FMCG"`, "Metals" vs `"Metal"`). A stock in `"Consumer Discretionary"` will not match "Consumer Goods". This is shallow logic in a page component; it belongs in a pure `matchesSector(stock, sector)` helper with a table, and it is testable.
**Fix:** extract to `utils/sectors.ts` with a `Record<sector, string[]>` alias table + unit test.

### N12. `ExplorePage` renders `ProToolsBacktester` at the bottom of a filtered list
`:376` — the backtester is inside the Explore page *after* the results, so it is only reachable by scrolling past 10 cards, and it disappears from the DOM only when the list is empty (it is outside the conditional, so it stays — good). Minor IA: a "Pro Tools" entry point in the header would be discoverable.
**Fix:** move behind a header chip that scrolls/expands, or into Learn where the strategy lab already lives.

---

## 7. Test quality

**What is good:** the suite runs fast (19 tests in 5.75 s), `ExplorePage`'s stale-response test (`tests/frontend/unit/pages/ExplorePage.test.tsx:433-491`) is a genuine behaviour test that resolves promises out of order and asserts the *right* symbol wins — keep it as the template. `useAbortableRequest.test.tsx` exercises the hook contract rather than internals.

**What is wrong:**

1. **Tests lock in fabricated data.** `tests/frontend/modals/NotificationDrawer.test.tsx:19-20` asserts that "Market Regime Active: Bull Market" and "Asset Allocation Drift Notice" render. Fixing M1 will (correctly) break this test — expect it, and rewrite it as "shows an offline banner and *no* alerts when the API fails".
2. **Implementation-detail assertions.** `NotificationDrawer.test.tsx:33-43` asserts `setInterval` was called with `45000`; that is a refactor tripwire with no user-facing meaning. Assert instead that a second poll happens after timers advance (`vi.advanceTimersByTime(45000)`) and that the list updates.
3. **No network mocking in `PortfolioPage.test.tsx`.** It lets the real `fetch` fail and relies on `.catch(() => {})` swallowing it — which is exactly the production bug in S11. That produces the 4 reproduced `act(...)` warnings (state updates from the real fetch resolving after the test body). Mock `fetch`/`EventSource` per test, and add cases for: SSE tick merging, the compounding refetch storm, delete-confirm, and abort-on-unmount.
4. **Framer-motion is mocked by hand** (`ExplorePage.test.tsx:8-31`) and forwards `layoutId` to a `div`, producing the reproduced React warning. Use `framer-motion`'s official `__mocks__`/`MotionConfig reducedMotion="always"` or strip unknown props in the mock — otherwise every run is noisy and real animation bugs (M3) are invisible.
5. **Zero a11y assertions.** No test queries by role/label (`getByRole`, `getByLabelText`); everything is `getByTestId`/`getByText`. That is why M5/M6/S2 all pass CI. Add `@testing-library/jest-dom` role queries plus 3 smoke tests: "stock card is a button and Enter opens the profile", "modal traps focus and restores it", "search input has an accessible name".
6. **Coverage gaps for the riskiest code:** no tests for `marketStream` reconnection/backoff, `abortRegistry` (superseded-controller case — M8), `pwaService.subscribeUserToPush` failure paths, or the `useAppStore` persistence/migration. Those are the four places where a regression is silent.
7. **Flakiness risk (not yet flaky):** `PortfolioPage.test.tsx` and any test that mounts a component calling `marketStream.connect()` leaves a real `EventSource` open against `jsdom`; if a future test asserts on `connect` call counts, order-dependence will appear. Add a global `afterEach(() => marketStream.disconnect())` in `tests/setup`.

---

## Top 5

1. **Fabricated financial data presented as live** — `MarketPulse.tsx:38-41`, `PortfolioPage.tsx:171-221` (fake +0.8% P&L + "LIVE STREAM" badge), `ProToolsBacktester.tsx:63-125,368-405` (fake metrics *and* a hardcoded equity curve), `Step5DeepDive.tsx:24-55` (fake testimonials), `StockProfileModal.tsx:102-169`. Smallest fix: kill the fallbacks, render a `StaleBadge`, and replace `x?.toFixed(n) || "48.5"` with `x == null ? "—" : …`.
2. **`PortfolioPage` SSE handler uses a stale `portfolios` closure** (`:69-117`) → newly created goals are silently deleted from state and `localStorage`; plus a compounding `POST` per tick (`:162`). Fix: functional `setPortfolios`, debounced persistence, effect keyed on `portfolio_id`.
3. **Modals inside `GlassCard` are clipped** (`LearningHub.tsx:203,316` + `GlassCard.tsx:26` `backdrop-blur-md overflow-hidden` + `ModalSheet.tsx:48` `fixed inset-0`) — the concept/video sheets render inside the card on Chrome/Android WebView. Fix: `createPortal` in `ModalSheet`.
4. **Keyboard users cannot open a stock or a concept** (`StockCard.tsx:78-85`, `LearningHub.tsx:156-159` are `div onClick`), and **dialogs have no focus trap/restore/label** (`ModalSheet.tsx`). Fix: real `<button>` + 30-line focus management in `ModalSheet`.
5. **Light-theme contrast failure on the Portfolio screen** — `PortfolioPage.tsx:272` `text-white` on `#F8FAFC` (≈1.06:1, invisible heading) and `HoldingsTable.tsx:21-24` `slate-300/400` empty state; plus `index.html:5` blocks pinch-zoom so users cannot work around small text. Fix: theme tokens + drop `user-scalable=no`.

---

*Method: read every file under `src/frontend/{components,pages,store,hooks,services,context,utils}` plus `App.tsx`, `main.tsx`, `index.html`, `vite.config.ts`, `tailwind.config.js`, `index.css`; executed `npm run build` and four targeted vitest files; verified claims against the generated `sw.js`, built `index.html`, and backend `app.py` service-worker route. Read-only — no source files were modified.*

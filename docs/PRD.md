# Spec: QuantNiti Core Platform

**Status:** completed

## Problem Statement

Retail investors and evaluators without a quantitative finance background struggle to make informed, data-backed stock market decisions. Existing retail investment platforms (Groww, INDmoney) provide passive portfolio tracking without predictive intelligence or downside risk modeling, while quantitative tools (TradingView, Zerodha Streak) require technical indicator scripting that retail users cannot parse. When seeking guidance, retail investors are pushed toward high-commission bank wealth managers (charging 1.5%–2.5% AUM fees with hidden conflicts of interest) or low-yielding fixed deposits.

Retail investors need a transparent, mobile-first decision support system that directly answers:
1. *Where should I invest my money?*
2. *How much is it probabilistically projected to grow over 1, 3, 6, and 12 months?*
3. *What is my downside risk in market crashes?*
4. *Why should I trust this algorithmic recommendation over a human bank advisor?*

Simultaneously, active traders and academic evaluators need to inspect underlying market regime dynamics and backtest technical trading strategies on Indian equity markets.

Beyond pure financial returns, investors increasingly want visibility into the ethical and social impact of their investments — but no Indian retail platform surfaces ESG (Environmental, Social, Governance) data at the portfolio recommendation level. India's financial literacy rate remains at 27% (NCFE-FLIS), and existing platforms provide recommendations without educating users on the concepts behind them.

---

## Solution

QuantNiti is an AI-driven regime-adaptive equity intelligence and portfolio recommendation platform for the Indian equity market (NIFTY 50 universe). It provides:

1. **Home Dashboard (`Home` Tab):** Real-time Market Pulse ticker, Unsupervised Market Regime Radar (Gaussian Mixture Model clustering for Bull, Bear, and Sideways states), 4-category Financial Learning Hub (*Basics*, *Regimes*, *Risk*, *Quant*), Playable 16:9 Video Explainer Hub, In-App Competitor Benchmark Drawer, and Notification Center.
2. **Stock Intelligence Profiles & Pro Tools (`Explore` Tab):** 360° asset intelligence for individual NIFTY 50 tickers featuring multi-horizon growth forecast gauges, regime suitability scores, ESG Conscience Scores, benchmark alpha comparisons, and the **Quant Lab Backtesting Studio** accessible via a collapsible Pro Tools accordion.
3. **5-Step Investor Growth Journey (`Grow` Tab):** A 5-step capital-to-basket recommendation wizard (Capital with word-form display -> Horizon -> Persona -> Results Donut -> Deep Dive with 4-Pillar Trust Card & ESG Conscience) that produces curated equity baskets with 3-tier probabilistic ₹ growth projections ($Q_{10}, Q_{50}, Q_{90}$).
4. **Explainable AI Trust Card:** A transparent 4-pillar credibility card explaining current market regime context, 5-year backtested directional accuracy, worst-case drawdown bounds, and estimated fee savings by eliminating middleman advisory commissions.
5. **Dual-State Virtual Paper Portfolio & Rebalancing Engine (`Portfolio` Tab):** Instant pre-populated **Demo Portfolio** for first-time visitors that transitions into a live **Virtual Paper Portfolio** with real-time mark-to-market P&L, 6-trigger smart alert notifications, interactive regime-shift rebalance diffs, and 1-click broker order sheets with discrete whole-share quantities.
6. **NitiBot — RAG-Powered Portfolio Intelligence Assistant:** A context-aware conversational AI assistant grounded in QuantNiti's own regime, portfolio, and backtest data via Retrieval-Augmented Generation (RAG) using Google Gemini, enabling natural-language inquiries from any screen via a floating action button.
7. **ESG Conscience Score Layer:** An Environmental, Social, and Governance scoring dimension applied to every stock in the NIFTY 50 universe and aggregated at the portfolio level, enabling socially responsible investment decisions and an "ESG-Conscious" risk persona option.
8. **Financial Literacy Microlearning Cards & Video Explainer Hub:** Contextual, bite-sized educational cards and playable 16:9 embedded YouTube videos surfaced alongside recommendations to bridge India's financial literacy gap.
9. **Sharable Portfolio Report Card:** One-click generation of a branded, professional portfolio intelligence report (PDF/image) that users can download or share via social media.
10. **Cross-Platform PWA & Native Android Container:** Dual distribution architecture featuring 1-click standalone PWA installation on Android/iOS/Desktop, alongside a native Android container app (`com.quantniti.app`) compiled via automated GitHub Actions CI/CD workflows using AndroidX `WebViewAssetLoader`.

---

## User Stories

1. As a first-time retail investor, I want to input my investment capital (e.g. ₹50,000) and time horizon (e.g. 6 months), so that I get a personalized portfolio basket recommendation suited to my timeframe.
2. As a first-time retail investor, I want to take a 3-question scenario quiz, so that my risk persona (Conservative, Balanced, Aggressive, or ESG-Conscious) is calibrated without financial jargon.
3. As a retail investor, I want to see projected future portfolio values in rupees across three scenarios (Pessimistic, Base, Optimistic), so that I understand realistic outcome boundaries rather than misleading single-point promises.
4. As a retail investor, I want to view an Explainable AI Trust Card on every recommendation, so that I understand why these stocks were selected and why I can trust the algorithm over a bank relationship manager.
5. As a retail investor, I want to see a side-by-side comparison of projected portfolio returns against a 7% Bank Fixed Deposit and the NIFTY 50 index, so that I can evaluate the risk-adjusted premium of equity investing.
6. As a retail investor, I want to see the exact percentage and rupee allocation across recommended stocks in a clean visual donut breakdown, so that I understand where my capital is distributed.
7. As a self-directed investor, I want to search and filter NIFTY 50 stocks by sector (IT, Banking, Energy, Auto, FMCG, Metals), so that I can explore individual companies I am interested in.
8. As a self-directed investor, I want to view a Stock Intelligence Profile for any ticker, so that I can see its multi-horizon growth forecast (1M, 3M, 6M, 12M), regime sensitivity, ESG score, and historical performance.
9. As a self-directed investor, I want to see a Regime Suitability badge on individual stocks, so that I know whether a stock aligns with current market conditions.
10. As a retail investor, I want to see a pre-populated Demo Portfolio on my first visit, so that I understand how portfolio tracking works before creating my own.
11. As a virtual portfolio user, I want to see my portfolio's live mark-to-market value, total return percentage, and day change, so that I can monitor simulated progress over time.
12. As a virtual portfolio user, I want to receive a Regime-Shift Rebalance Alert when the macro market transitions, so that I am notified to adjust my portfolio before severe downturns.
13. As a virtual portfolio user, I want to view an interactive before/after asset allocation diff when a rebalance is recommended, so that I understand exactly which stocks are trimmed or added.
14. As a virtual portfolio user, I want to click "Apply Rebalance", so that my virtual portfolio weights update to the new regime-optimized distribution.
15. As a retail investor ready to invest real funds, I want to generate a 1-Click Order Sheet showing exact whole-share counts, current prices, and remaining unallocated cash, so that I can copy executable orders to Zerodha or Groww without fractional shares.
16. As an active quant trader, I want to open the Quant Lab Pro Tools to view real-time Market Regime probabilities (Bull / Bear / Sideways), so that I can understand prevailing macroeconomic volatility and drift.
17. As an academic evaluator, I want to inspect historical market regime segmentation on the NIFTY 50 index chart, so that I can verify the unsupervised machine learning clustering model.
18. As an active trader, I want to backtest technical trading strategies (Buy & Hold, MA Crossover, RSI, Bollinger Bands, Dual Momentum) across custom date ranges, so that I can evaluate systematic rule profitability.
19. As an active trader, I want to view comprehensive backtest performance metrics (CAGR, Sharpe Ratio, Sortino Ratio, Volatility, Max Drawdown, Win Rate), so that I can evaluate risk-adjusted strategy alpha.
20. As an active trader, I want to view interactive equity curves and drawdown charts comparing my backtested strategy against the NIFTY 50 benchmark, so that I can visually verify historical performance under various market regimes.
21. As a retail investor confused by a recommendation, I want to ask NitiBot a natural-language question like "Why did the AI pick Infosys for my portfolio?" and receive a data-grounded explanation referencing the stock's regime suitability, growth projections, and HRP weight rationale.
22. As a retail investor worried about a market downturn, I want to ask NitiBot "What happens to my portfolio if the market crashes?" and receive a stress-scenario answer citing the Trust Card's max drawdown bounds and backtest performance data.
23. As a first-time investor unfamiliar with financial jargon, I want to ask NitiBot "What does HRP optimization mean?" and receive a plain-language educational explanation grounded in QuantNiti's own domain glossary.
24. As a socially conscious investor, I want to see an ESG Conscience Score (0–100) on every stock's Intelligence Profile, so that I can evaluate whether my investments align with my environmental, social, and governance values.
25. As a socially conscious investor, I want to select the "ESG-Conscious" risk persona, so that the AI tilts portfolio weights toward high-ESG-scoring companies while maintaining return expectations.
26. As a socially conscious investor, I want to see a portfolio-level weighted ESG score on my basket results, so that I understand the aggregate ethical footprint of my entire investment.
27. As a new investor seeing quantitative terms for the first time, I want to watch embedded 16:9 Video Explainers with takeaways in the Learning Hub, so that I can learn while investing.
28. As a user who has generated a portfolio basket, I want to click "Download Report" and receive a branded PDF report card containing my portfolio donut, growth projections, Trust Card summary, ESG score, and current regime badge, so that I can save or print it.
29. As a user who wants to share their AI-generated portfolio analysis, I want to click a "Share" button that generates a shareable image with a WhatsApp-ready pre-formatted message, so that I can share my QuantNiti results socially.
30. As a mobile user on Android, I want to install QuantNiti to my home screen as a standalone fullscreen app or run the native Android container APK (`com.quantniti.app`), so that it feels native without visiting the browser.
31. As a desktop user on a laptop, I want to install QuantNiti from Chrome/Edge as a desktop application with a responsive layout, so that I can use the platform in a wider viewport.
32. As an iOS user, I want to see an in-app guided banner explaining how to "Add to Home Screen" via Safari's Share menu, so that I can install the PWA on my iPhone.

---

## Implementation Decisions

1. **4-Tab Mobile-First Architecture with Responsive Layout:**
   The client interface is structured into four primary tabs: `Home` (Market Pulse, Regime Radar, Learning Hub & Video Explainers), `Explore` (Stock Intelligence Profiles & collapsible Quant Lab Pro Tools accordion), `Grow` (5-Step Guided Basket Wizard), and `Portfolio` (Dual-state Demo & Virtual Investment Tracker with Order Sheet).

2. **Data Ingestion & Universe:**
   The platform operates on an expanded multi-asset universe: NIFTY 50 large-cap equities, commodity ETFs (Gold & Silver via `GOLDBEES` / `SILVERBEES`), and high-momentum sectoral leaders (Defense & Metals), ingesting daily historical and live-adjusted OHLCV price series, India VIX, and benchmark index data with local caching.

3. **Unsupervised Market Regime Classification Engine:**
   Market regime is classified into three macro states (Low-Volatility Bull, High-Volatility Bear, Sideways Consolidation) using Gaussian Mixture Models (GMM) trained on rolling returns, realized volatility, and India VIX metrics.

4. **Multi-Horizon Probabilistic Growth Forecasting Engine:**
   Stock-level expected returns and distribution intervals (10th, 50th, 90th percentiles) across 1-month, 3-month, 6-month, and 12-month horizons are generated using a multi-factor ranking and quantile regression pipeline, providing bounded forecast cones with isotonic monotonicity guarantees ($Q_{10} \le Q_{50} \le Q_{90}$).

5. **Regime-Conditioned Portfolio Optimization with ESG Tilting:**
   Portfolio baskets are constructed using Hierarchical Risk Parity (HRP) with Ledoit-Wolf covariance shrinkage, combining ML return expectations with risk persona constraints (Conservative, Balanced, Aggressive, ESG-Conscious). The ESG-Conscious persona applies an additive weight bias toward high-ESG-scoring stocks before HRP bisection.

6. **Discrete Integer Share Allocation:**
   Continuous theoretical weights are converted to exact whole-share quantities via greedy integer sizing ($n_i = \lfloor (w_i \cdot C) / P_i \rfloor$), tracking the remaining unallocated cash buffer for 100% executable broker order sheets.

7. **Explainable AI Trust Card Generation:**
   Every basket and stock recommendation automatically synthesizes four trust pillars: (1) Active regime context, (2) Historical backtested hit rate, (3) Max stress drawdown guardrail, and (4) Estimated commission savings vs traditional wealth management.

8. **Vectorized Strategy Backtesting Engine:**
   The Quant Lab features an in-memory vectorized backtesting engine that simulates technical trading rules (Moving Average Crossovers, RSI Mean Reversion, Bollinger Band Breakouts, Dual Momentum) on historical OHLCV data with slippage and transaction cost modeling.

9. **Virtual Paper Portfolio Simulator & Regime Rebalancer:**
   Virtual holdings are persisted in local SQLite/session state, computing daily mark-to-market valuations, evaluating 6-trigger smart alerts, and triggering rebalance diff alerts upon regime transition events.

10. **NitiBot RAG Architecture:**
    A FastAPI chat endpoint receives a user message, constructs a RAG context payload by aggregating the user's active basket, current regime state, relevant growth projections, Trust Card data, and backtest results from existing services, then forwards the augmented prompt to the Google Gemini API (gemini-2.5-flash) with SEBI-compliant educational disclaimers.

11. **ESG Conscience Score Data Model:**
    A curated dataset provides per-stock ESG scores (0–100 composite, plus Environment, Social, Governance sub-scores) sourced from publicly available BRSR disclosures and CRISIL ESG ratings.

12. **Financial Literacy Microlearning & Video Explainer Hub:**
    Structured educational content spanning 4 categories (*Basics*, *Regimes*, *Risk*, *Quant*) paired with responsive 16:9 embedded YouTube video breakdowns (`youtube-nocookie.com`) featuring quantitative takeaways and difficulty tiers.

13. **Client-Side PDF/Image Report Generation:**
    Portfolio report cards are generated on the client using `html2canvas` + `jspdf` including the portfolio donut, growth projection chart, Trust Card summary, ESG score, and SEBI disclaimer footer.

14. **Dual Distribution (PWA + Native Android Container):**
    Progressive Web App configuration (`manifest.json`, `sw.js` offline caching, Web Push) paired with a native Android container app (`com.quantniti.app`) compiled via automated GitHub Actions CI/CD workflows using AndroidX `WebViewAssetLoader`.

---

## Testing Decisions

1. **Testing Philosophy:**
   Tests focus strictly on external behavior, API/service boundaries, and component seams under strict TDD principles.

2. **Primary Seam for Testing:**
   - Basket recommendation generation: Verifying valid weight distribution ($\sum w_i = 1.0$), quantile monotonicity ($Q_{10} \le Q_{50} \le Q_{90}$), persona risk constraints, and ESG persona weight tilting.
   - Stock profile intelligence: Verifying correct multi-horizon projections, regime ratings, and ESG score inclusion.
   - Market regime classification: Verifying valid 3-state probability distributions summing to 1.0.
   - Backtest engine: Verifying mathematical integrity of CAGR, Sharpe ratio, drawdown curves, and trade log calculations.
   - Virtual portfolio simulation: Verifying accurate P&L calculation, regime-shift rebalance diff generation, and discrete integer share quantities with non-negative cash buffers.
   - Chat endpoint: Verifying RAG context construction, system prompt injection, and graceful degradation when API key is absent.
   - Frontend component tests: 132 tests in Vitest covering all tabs, modals, wizards, and theme contexts.
   - Backend pytest suite: 272 tests covering ML, API, and stream with 99% line coverage.

---

## Out of Scope

- Automated live broker order routing or auto-trading execution (educational and simulated decision support only).
- Penny stocks or illiquid small-cap tickers outside the NIFTY 50 and expanded ETF universe.
- Intraday high-frequency tick-by-tick streaming or futures/options derivatives pricing.
- User financial advisory licensing under SEBI RIA regulations (standard analytical disclaimer provided).
- Real-time ESG data scraping or paid ESG API integration (curated static dataset).
- Multi-turn agentic workflows where NitiBot autonomously executes trades or modifies portfolios on the user's behalf.
- Official Google Play Store or Apple App Store paid developer account publishing (native Android container APK and PWA distribution are fully implemented and automated via CI/CD).
- Vernacular/multilingual chatbot interface (English-only for this version; noted as future work).

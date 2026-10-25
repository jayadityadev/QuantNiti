# QuantNiti: Domain Glossary

An AI-driven portfolio intelligence and financial education platform for Indian retail investors, providing regime-adaptive portfolio recommendations, transparent growth projections, explainable risk guardrails, and contextual financial literacy — powered by unsupervised market regime classification, multi-factor quantile forecasting, and hierarchical risk parity optimization.

## Language

### Core Product Concepts

**Portfolio Basket**:
A curated, algorithmically weighted collection of Indian equity and commodity ETF assets generated dynamically according to market regime and risk persona. Draws from the Investment Universe.
_Avoid_: Watchlist, Trading bundle, Stock bucket

**Investment Universe**:
The full set of investable assets available to the recommendation engine: NIFTY 50 large-cap equities, select sectoral equities (Defense, Metals), and commodity ETFs (Gold, Silver). Expandable without retraining the regime classifier.
_Avoid_: Stock list, Ticker database, Asset pool

**Market Regime**:
The macro-structural state of the Indian equity market (Low-Volatility Bull, High-Volatility Bear, Sideways Consolidation) classified via unsupervised ML.
_Avoid_: Market trend, Sentiment, Mood

**Growth Projection**:
A probabilistic estimated return percentage and future capital trajectory for a stock or basket over defined horizons (1M, 3M, 6M, 12M) bounded by 10th (Pessimistic), 50th (Base), and 90th (Optimistic) percentiles.
_Avoid_: Price target, Tip, Deterministic forecast

**Compounding Projection**:
A long-horizon (1–10 year) portfolio-level wealth trajectory calculated from backtested CAGR and compounding mathematics (Lump Sum, SIP, Step-Up SIP), not from ML prediction. Visualized as an uncertainty-banded growth cone.
_Avoid_: Long-term forecast, 10-year prediction

**Trust Card**:
An explainability card accompanying every recommendation that details regime suitability, backtested directional hit rate, stress drawdown limits, and fee savings over traditional wealth managers.
_Avoid_: Stock disclaimer, Notes sheet

**Risk Persona**:
The calibrated risk profile of an investor (Conservative, Balanced, Aggressive, ESG-Conscious) that dictates asset allocation bounds and maximum tolerable drawdown.
_Avoid_: Trader tier, Experience level

**Stock Intelligence Profile**:
A comprehensive 360-degree assessment of a single equity or ETF asset encompassing projected growth ranges, regime sensitivity, downside risk, and benchmark comparison.
_Avoid_: Ticker chart, Quote page

**Smart Alert / Multi-Condition Alert Engine**:
A proactive notification triggered by quantitative conditions across 6 automated evaluators: (1) Macro Regime Transition, (2) Persona Trailing Stop-Loss breach, (3) Profit Target reached, (4) Target Weights Drift >5%, (5) Volatility Breakout (Bollinger band penetration), and (6) ESG Conscience Downgrade. Delivered via in-app notification center and browser Web Push. Always framed as an objective quantitative signal with Trust Card context, never as a speculative tip.
_Avoid_: Buy signal, Sell signal, Hot tip, Trading alert

**Recommendation Score**:
A regime-conditioned composite ranking of assets across four quantitative factor pillars (Quality, Value, Momentum, Low Volatility) with regime-adaptive factor weights, used to surface top picks for the current market conditions.
_Avoid_: Stock tip, Buy list, Hot pick

**Virtual Paper Portfolio**:
A simulated investment tracker that calculates live mark-to-market performance, tracks benchmark alpha, surfaces regime-shift rebalance recommendations, and supports multiple named portfolios per user.
_Avoid_: Demo wallet, Mock account

**Demo Portfolio**:
A read-only, pre-populated showcase portfolio demonstrating portfolio tracking features to first-time users who have not yet created their own Virtual Paper Portfolio. Contains synthetic holdings with realistic regime-tagged data. Not editable, not deletable, and displayed with a persistent "This is a demo — build your own!" banner. Replaced by the user's first real Virtual Paper Portfolio.
_Avoid_: Sample account, Test portfolio, Sandbox

**Regime-Shift Rebalance**:
A proactive portfolio re-allocation alert triggered when the market transitions across regimes, offering an interactive before/after diff to protect capital.
_Avoid_: Reset, Auto-trade

**NitiBot**:
A RAG-powered conversational AI assistant grounded in QuantNiti's own regime, portfolio, and backtest data, answering natural-language questions about algorithmic recommendations. Uses Retrieval-Augmented Generation to prevent hallucination.
_Avoid_: Generic chatbot, AI advisor, Financial planner

**ESG Conscience Score**:
A composite Environmental, Social, and Governance rating (0–100) assigned to each stock and aggregated at the portfolio level, enabling socially responsible investment decisions.
_Avoid_: Ethics rating, Green score, Sustainability label

**Financial Literacy Microlearning Card**:
A bite-sized, contextual educational card explaining a financial concept in plain language with a relatable analogy, surfaced inline alongside the relevant UI element and in the Learning Hub across 4 structured tracks (Basics, Regimes, Risk, Quant).
_Avoid_: Tutorial, Help tooltip, Wiki

**Video Explainer**:
A responsive 16:9 embedded video guide hosted on YouTube (via `youtube-nocookie.com`) paired with plain-language quantitative takeaways and difficulty tiers, surfaced within the Learning Hub to explain complex concepts (such as market regimes, diversification, and Sharpe ratio).
_Avoid_: Promotional video, Marketing reel, Webinar

**Learning Hub**:
A dedicated educational section on the Home tab offering structured financial literacy content, video explainers, and concept cards for users with no prior finance knowledge.
_Avoid_: Course, Academy, Varsity clone

**Portfolio Report Card**:
A branded, downloadable PDF/image document summarizing a user's portfolio allocation, growth projections, Trust Card, ESG score, and market regime context for offline reference or social sharing.
_Avoid_: Statement, Receipt, Export dump

**Review**:
User-submitted feedback on an individual stock, AI Portfolio Basket, or investment strategy, audited by an autonomous 3-tier AI Fact-Checking Agent. Reviews with performance claims are verified against ground-truth mathematical market returns (within a +/- 3% tolerance window) to award verified badges, while unsubstantiated claims, deceptive tips, and contact solicitations are rejected to enforce SEBI advertisement compliance.
_Avoid_: Unverified testimonial, Stock tip, Speculative boast, P&L bragging

**Native Android Container**:
A lightweight native Android application shell (`com.quantniti.app`) utilizing AndroidX `WebViewAssetLoader`, custom JavaScript bridge, hardware back button gesture handling, and native splash screens to wrap the precompiled React PWA for mobile environments.
_Avoid_: Web view wrapper, Hybrid port, PhoneGap app

**Continuous Cloud Deployment**:
An automated pipeline orchestrated via GitHub Actions that runs tests, builds the multi-stage Docker container, securely deploys to an AWS Lightsail instance (`13.207.117.167` in `ap-south-1` Mumbai), and manages automated TLS/SSL certificate renewal via Caddy v2 reverse proxy at `https://quantniti.jayadityadev.tech/`.
_Avoid_: Manual FTP, Local tunnel, Staging box

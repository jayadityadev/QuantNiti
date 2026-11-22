# QuantNiti Feature Verification Map

This directory is the maintained source for verifying user-facing behavior in QuantNiti. Read this index before driving the app, then use the matching feature file as the execution recipe.

## Baseline Preconditions

- Launch QuantNiti server at `http://127.0.0.1:8000` (or `8008` during concurrent test runs).
- Ensure Vite client is built in `src/app/static/dist/` (`npm run build`).
- Ensure `.venv` has all dependencies installed (`fastapi`, `uvicorn`, `playwright`, `scikit-learn`, `numpy`).
- Run doctor check `.\.venv\Scripts\python.exe .agents/skills/verify/scripts/verify_driver.py doctor --port 8000` and confirm healthy.
- Never drive an instance not started by or known to this verification run.

## Driving Conventions

- Start every recipe from the baseline state described in its preconditions.
- Prefer stable accessible names and ARIA handles (`button:has-text('Grow')`, `button:has-text('Portfolio')`) over arbitrary CSS coordinates.
- Run automated feature journeys via `verify_driver.py drive <feature>`.
- Store evidence artifacts in `.audit/verify/`. Do not delete them during cleanup.

## Feature Map

- [01. Onboarding Quiz](./01-onboarding-quiz.md) covers risk persona profiling, interactive question selection, and onboarding state persistence.
- [02. Market Regime Radar](./02-market-regime-radar.md) covers macro-structural unsupervised regime classification, regime probabilities, and home tab pulse visualizers.
- [03. Grow AI Basket Recommendation](./03-grow-ai-basket.md) covers capital and horizon selection, HRP portfolio optimization, growth cones, and Trust Cards.
- [04. Algorithmic Backtesting Lab](./04-backtesting-lab.md) covers single and multi-strategy backtesting (MA Crossover, RSI, MACD), Sharpe ratios, and drawdowns.
- [05. Virtual Paper Portfolio](./05-virtual-paper-portfolio.md) covers simulated portfolio tracking, live mark-to-market performance, benchmark alpha, and rebalancing alerts.

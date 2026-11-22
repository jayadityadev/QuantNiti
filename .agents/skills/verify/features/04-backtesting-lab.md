# Algorithmic Backtesting Lab

The Backtesting Lab allows users to evaluate historical algorithmic trading strategies (e.g., Moving Average Crossover, RSI Oscillator, MACD Momentum) on Indian equities, comparing total returns, Sharpe ratios, and max drawdowns against benchmark buy-and-hold returns.

## Sub-features

- `single-strategy-backtest`: Runs parameterizable algorithmic backtests on single symbols (`/api/backtest/run`).
- `multi-strategy-comparator`: Simultaneously tests and ranks 5 distinct strategies for an asset (`/api/backtest/compare`).
- `performance-metrics`: Computes CAGR, Sharpe Ratio, Max Drawdown, and final portfolio equity.

## How to get to it (user POV)

- Open `http://127.0.0.1:8000/`.
- Access the Backtesting Lab via the Quant Lab navigation or individual Stock Intelligence profile pages.
- Or trigger directly via the REST endpoints `/api/backtest/run` and `/api/backtest/compare`.

## Driving it with verify_driver

Preconditions:
- QuantNiti instance is healthy on `http://127.0.0.1:8000`.

Driving steps:
- **Execute Strategy Run:** Send `POST /api/backtest/run` with `symbol: "RELIANCE"`, `strategy: "MA_CROSSOVER"`, `initial_capital: 100000`.
- **Assert Status & Metrics:** Verify response status 200, positive final equity, and non-null Sharpe ratio.
- **Proof:**
  - JSON artifact `.audit/verify/backtest_ma_crossover.json` saved with full trade list and backtest metrics.

Run automated recipe:
```powershell
.\.venv\Scripts\python.exe .agents/skills/verify/scripts/verify_driver.py drive backtesting-lab --port 8000 --output-dir .audit/verify
```

## Gotchas

- Some tickers require historical caching; always test against established large-cap equities (e.g. `RELIANCE`, `TCS`, `INFY`) for deterministic verification.

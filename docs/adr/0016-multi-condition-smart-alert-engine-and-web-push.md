# Multi-Condition Quantitative Smart Alert Engine with Web Push

**Status:** accepted

## Context
Passive portfolio trackers notify users only of price changes, missing macro structural breaks and portfolio drift. Retail investors often fail to rebalance during regime transitions or suffer unmitigated drawdowns when stop-loss limits are breached.

## Decision
We implemented an automated rules-and-regime event detection engine evaluating **6 deterministic quantitative triggers**:
1. Macro Regime Shift (GMM state transition).
2. Persona-Calibrated Trailing Stop-Loss breach (3% Cons, 7% Bal, 12% Aggr).
3. Horizon-Conditioned Profit Target reached.
4. Target Allocation Weight Drift (> 5%).
5. Volatility Breakout (2x baseline volatility or Bollinger band penetration).
6. ESG Conscience Downgrade (governance penalty).

Alerts are dispatched to an in-app notification center and broadcast via browser Web Push notifications.

## Consequences
- Proactively protects user capital against macro market downturns.
- Adheres strictly to SEBI educational disclaimers by framing alerts as objective signals rather than speculative tips.

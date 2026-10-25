# Prioritizing Portfolio Intelligence Over Pure Strategy Testing

**Status:** accepted

## Context
Initial prototypes placed equal emphasis on indicator-based strategy backtesting and multi-asset portfolio optimization. User testing revealed that retail investors are overwhelmed by individual indicator parameters (e.g. RSI periods, MACD fast/slow) and prefer holistic, multi-asset portfolio solutions.

## Decision
We elevated multi-asset portfolio intelligence (HRP allocation, multi-horizon growth cones, Trust Cards) as the primary product experience, while retaining technical strategy backtesting as a specialized evaluator capability within the Pro Tools drawer.

## Consequences
- Drastically simplifies the primary user journey from landing to portfolio generation.
- Positions QuantNiti as a comprehensive wealth intelligence platform rather than a niche trading bot.

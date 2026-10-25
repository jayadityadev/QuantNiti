# Virtual Paper Portfolio with Regime-Shift Rebalance Alerts

**Status:** accepted

## Context
Indian retail equity investing is subject to strict SEBI Registered Investment Advisor (RIA) regulations and broker licensing requirements. Directly executing broker orders via automated APIs would introduce severe regulatory, capital, and liability barriers for an academic project, while purely static backtesting fails to demonstrate live portfolio management.

## Decision
We implemented an in-app **Virtual Paper Portfolio Simulator** with real-time mark-to-market (MTM) tracking, dual-state Demo Portfolio onboarding, and 1-click broker order sheet exports (Zerodha CSV / Groww text). When the unsupervised ML engine detects a macro regime shift (e.g., Low-Vol Bull to High-Vol Bear), the system generates an interactive before/after allocation diff alert allowing users to simulated-rebalance with one click.

## Consequences
- Completely eliminates regulatory SEBI RIA licensing barriers while preserving real-world utility.
- Allows investors to safely evaluate algorithmic portfolio recommendations out-of-sample in simulated time.
- Generates 100% executable whole-share orders without requiring live broker API credentials.

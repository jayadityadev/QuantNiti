# Progressive Disclosure UX: 4-Tab Architecture and Embedded Quant Lab Pro Tools

**Status:** accepted

## Context
Retail investors need a distraction-free, approachable interface that does not intimidate them with institutional trading charts. Conversely, academic evaluators, faculty guides, and quantitative traders need full visibility into backtesting equity curves, drawdown attribution, and regime classification statistics.

## Decision
We organized the interface into a 4-tab mobile-first application shell (`Home`, `Explore`, `Grow`, `Portfolio`) with progressive disclosure:
1. `Home`: Executive Market Pulse, Unsupervised Regime Radar, and Financial Learning Hub.
2. `Explore`: Streamlined 360° Stock Intelligence Profiles, with the advanced **Quant Lab Backtesting Studio** tucked cleanly behind a collapsible "Pro Tools" accordion.
3. `Grow`: 5-Step Guided Investment Wizard.
4. `Portfolio`: Real-time mark-to-market simulated tracker with Demo Portfolio showcase.

## Consequences
- Non-finance retail beginners are never overwhelmed by quantitative charts unless they deliberately expand Pro Tools.
- Academic evaluators retain 100% access to vectorized backtesting, Sharpe/Sortino ratios, and regime attribution.
- Unified single-page application lifecycle with clean tab switching and state management.

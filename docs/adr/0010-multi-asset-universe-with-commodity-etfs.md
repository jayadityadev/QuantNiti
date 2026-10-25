# Multi-Asset Universe Expansion with Defensive Commodity ETFs

**Status:** accepted

## Context
A purely equity-focused investment universe suffers severe systemic drawdowns during macroeconomic risk-off regimes (High-Volatility Bear markets). Retail investors holding 100% equities during market crashes experience panic selling and capital destruction.

## Decision
We expanded the investment universe beyond NIFTY 50 equities to include defensive commodity ETFs:
1. **GOLDBEES (Nippon India ETF Gold BeES)**: Negative or near-zero correlation to equities during liquidity shocks.
2. **SILVERBEES (Nippon India ETF Silver BeES)**: Precious and industrial metal hedge.
3. Select high-momentum sectoral leaders (Defense and Metals).

## Consequences
- Provides the HRP optimizer with uncorrelated assets to allocate defensive weights during Bear regimes.
- Reduces simulated portfolio drawdown during market stress events.

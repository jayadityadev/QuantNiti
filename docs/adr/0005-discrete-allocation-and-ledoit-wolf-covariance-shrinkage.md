# Discrete Integer Allocation and Ledoit-Wolf Covariance Shrinkage

**Status:** accepted

## Context
Theoretical portfolio weights produced by Hierarchical Risk Parity (HRP) are continuous real numbers $\sum w_i = 1.0$. However, Indian equity brokers (Zerodha, Groww) do not support fractional shares. Furthermore, empirical sample covariance matrices on rolling financial returns suffer from estimation noise and singularity.

## Decision
We incorporated two critical quantitative techniques:
1. **Ledoit-Wolf Covariance Matrix Regularization**: Replaces noisy empirical sample covariance with an optimal shrinkage combination against a constant correlation target, guaranteeing well-conditioned, positive-definite matrices across all market regimes.
2. **Greedy Integer Share Allocation**: Converts continuous weights into discrete whole-share quantities ($n_i = \lfloor (w_i \cdot C) / P_i floor$) while strictly accounting for remaining residual cash buffers.

## Consequences
- Eliminates matrix inversion errors and singular matrix exceptions during optimization.
- Delivers 100% executable whole-share order sheets ready for instant broker import.

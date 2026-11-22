"""Markov Regime Transition and State Persistence Engine.

Computes:
1. Empirical / Smoothed 3x3 Transition Probability Matrix P_{ij} = P(S_{t+1} = j | S_t = i).
2. Expected Regime Duration / Persistence E[D_i] = 1 / (1 - P_{ii}) in trading days.
3. Long-run stationary distribution pi where pi * P = pi.
4. Next-step forward regime distribution projection p_{t+1} = p_t * P.
5. Market memory categorization using the Hurst Exponent.
"""

from typing import Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd

from app.core.models import MarketRegimeType, RegimeProbabilities
from app.ml.regime.features import calculate_hurst_exponent


REGIME_ORDER: List[MarketRegimeType] = [
    MarketRegimeType.LOW_VOLATILITY_BULL,
    MarketRegimeType.HIGH_VOLATILITY_BEAR,
    MarketRegimeType.SIDEWAYS_CONSOLIDATION,
]


class MarkovRegimeModel:
    """Estimates transition dynamics, persistence, and stationary equilibria for market regimes."""

    def __init__(self, laplace_smoothing: float = 1.0):
        self.laplace_smoothing = laplace_smoothing
        self.transition_matrix: np.ndarray = np.ones((3, 3)) / 3.0
        self.stationary_distribution: np.ndarray = np.ones(3) / 3.0
        self.expected_durations: Dict[str, float] = {
            r.value: 10.0 for r in REGIME_ORDER
        }
        self.is_fitted: bool = False

    def fit_from_sequence(self, regime_sequence: List[Union[MarketRegimeType, str]]) -> "MarkovRegimeModel":
        """Estimate transition probabilities from an observed sequence of regime states."""
        if len(regime_sequence) < 2:
            # Fallback to realistic default market persistence priors if insufficient data
            # Bull regimes have ~94% daily persistence, Bear ~90%, Sideways ~88%
            self.transition_matrix = np.array([
                [0.94, 0.02, 0.04],  # Bull -> [Bull, Bear, Sideways]
                [0.05, 0.88, 0.07],  # Bear -> [Bull, Bear, Sideways]
                [0.06, 0.04, 0.90],  # Sideways -> [Bull, Bear, Sideways]
            ])
            self._compute_derived_metrics()
            self.is_fitted = True
            return self

        # Map to integer indices: 0: Bull, 1: Bear, 2: Sideways
        str_to_idx = {
            MarketRegimeType.LOW_VOLATILITY_BULL.value: 0,
            MarketRegimeType.HIGH_VOLATILITY_BEAR.value: 1,
            MarketRegimeType.SIDEWAYS_CONSOLIDATION.value: 2,
        }

        indices: List[int] = []
        for r in regime_sequence:
            val = r.value if hasattr(r, "value") else str(r)
            if val in str_to_idx:
                indices.append(str_to_idx[val])
            elif "Bull" in val:
                indices.append(0)
            elif "Bear" in val:
                indices.append(1)
            else:
                indices.append(2)

        # Count state transitions with Laplace smoothing
        counts = np.full((3, 3), fill_value=self.laplace_smoothing, dtype=np.float64)
        for t in range(len(indices) - 1):
            i = indices[t]
            j = indices[t + 1]
            counts[i, j] += 1.0

        # Normalize row-stochastic transition matrix (each row sums strictly to 1.0)
        row_sums = counts.sum(axis=1, keepdims=True)
        self.transition_matrix = counts / np.maximum(row_sums, 1e-12)
        self.transition_matrix = self.transition_matrix / self.transition_matrix.sum(axis=1, keepdims=True)

        self._compute_derived_metrics()
        self.is_fitted = True
        return self

    def _compute_derived_metrics(self) -> None:
        """Compute expected durations and stationary distribution from transition matrix."""
        # 1. Expected duration E[D_i] = 1 / (1 - P_{ii})
        self.expected_durations = {}
        for idx, regime in enumerate(REGIME_ORDER):
            p_ii = float(self.transition_matrix[idx, idx])
            # Bound p_ii to [0.0, 0.999] to prevent zero-division while accurately reflecting high persistence
            p_ii = min(max(p_ii, 0.0), 0.999)
            duration = round(1.0 / (1.0 - p_ii), 1)
            self.expected_durations[regime.value] = max(duration, 1.0)

        # 2. Stationary distribution via exact null-space linear solve: pi * P = pi with sum(pi) = 1
        try:
            A = np.copy(self.transition_matrix.T) - np.eye(3)
            A[-1, :] = 1.0
            b = np.array([0.0, 0.0, 1.0])
            pi = np.linalg.solve(A, b)
            if np.all(np.isfinite(pi)) and np.all(pi >= -1e-6):
                pi = np.maximum(pi, 0.0)
                pi = pi / np.sum(pi)
                self.stationary_distribution = pi
            else:
                raise ValueError("Degenerate linear solution for stationary distribution")
        except Exception:
            # High-precision power iteration fallback: pi_{k+1} = pi_k * P
            pi = np.array([1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0], dtype=np.float64)
            for _ in range(300):
                next_pi = pi @ self.transition_matrix
                next_pi = next_pi / np.sum(next_pi)
                if np.max(np.abs(next_pi - pi)) < 1e-12:
                    break
                pi = next_pi
            self.stationary_distribution = pi

    def predict_next_step(self, current_probabilities: RegimeProbabilities) -> Dict[str, float]:
        """Compute one-step-ahead forecasted regime probability distribution."""
        current_vector = np.array([
            max(0.0, current_probabilities.bull),
            max(0.0, current_probabilities.bear),
            max(0.0, current_probabilities.sideways),
        ], dtype=np.float64)

        c_sum = np.sum(current_vector)
        if c_sum > 0:
            current_vector = current_vector / c_sum
        else:
            current_vector = np.ones(3, dtype=np.float64) / 3.0

        next_vector = current_vector @ self.transition_matrix
        next_vector = next_vector / np.sum(next_vector)

        # Enforce sum to 1.0
        p_bull = round(float(next_vector[0]), 4)
        p_bear = round(float(next_vector[1]), 4)
        p_side = round(1.0 - (p_bull + p_bear), 4)
        if p_side < 0:
            p_side = 0.0
            norm = p_bull + p_bear
            p_bull = round(p_bull / norm, 4)
            p_bear = round(1.0 - p_bull, 4)

        return {
            "bull": p_bull,
            "bear": p_bear,
            "sideways": p_side,
        }

    def get_transition_dict(self) -> Dict[str, Dict[str, float]]:
        """Return transition probabilities as a nested dictionary."""
        res: Dict[str, Dict[str, float]] = {}
        keys = ["bull", "bear", "sideways"]
        for i, source in enumerate(REGIME_ORDER):
            res[source.value] = {
                keys[j]: round(float(self.transition_matrix[i, j]), 4)
                for j in range(3)
            }
        return res

    def get_stationary_dict(self) -> Dict[str, float]:
        """Return stationary distribution as dictionary."""
        return {
            "bull": round(float(self.stationary_distribution[0]), 4),
            "bear": round(float(self.stationary_distribution[1]), 4),
            "sideways": round(float(self.stationary_distribution[2]), 4),
        }

    def analyze_market_memory(self, price_series: pd.Series) -> Tuple[float, str]:
        """Compute Hurst exponent and translate to qualitative market memory regime."""
        h = calculate_hurst_exponent(price_series)
        if h < 0.45:
            memory = "Mean-Reverting"
        elif h > 0.55:
            memory = "Persistent Trend"
        else:
            memory = "Random Walk"
        return round(h, 3), memory

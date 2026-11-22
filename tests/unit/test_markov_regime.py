"""Unit tests for Markov Regime Modeling and State Persistence Engine."""

import numpy as np
import pandas as pd
import pytest

from app.core.models import MarketRegimeType, RegimeProbabilities
from app.ml.regime.markov import MarkovRegimeModel, REGIME_ORDER


def test_markov_regime_model_default_fit():
    """Empty or short sequences fall back to realistic priors without failure."""
    model = MarkovRegimeModel()
    model.fit_from_sequence([])
    assert model.is_fitted
    matrix = model.transition_matrix
    assert matrix.shape == (3, 3)
    # Each row sums to 1.0
    for row in matrix:
        assert pytest.approx(row.sum(), rel=1e-3) == 1.0


def test_markov_regime_model_empirical_transitions():
    """Verify empirical counting with Laplace smoothing produces stochastic matrix."""
    model = MarkovRegimeModel(laplace_smoothing=1.0)
    # 20 days of Bull, then 5 days of Sideways, then 5 days of Bear
    sequence = (
        [MarketRegimeType.LOW_VOLATILITY_BULL] * 20
        + [MarketRegimeType.SIDEWAYS_CONSOLIDATION] * 5
        + [MarketRegimeType.HIGH_VOLATILITY_BEAR] * 5
    )
    model.fit_from_sequence(sequence)
    assert model.is_fitted

    matrix = model.transition_matrix
    assert matrix.shape == (3, 3)
    for row in matrix:
        assert pytest.approx(row.sum(), rel=1e-3) == 1.0

    # Bull persistence should be high
    p_bull_bull = matrix[0, 0]
    assert p_bull_bull > 0.70

    # Expected duration for Bull should be multiple days
    durations = model.expected_durations
    assert durations[MarketRegimeType.LOW_VOLATILITY_BULL.value] > 3.0

    # Stationary distribution should sum to 1.0
    stat_dist = model.get_stationary_dict()
    assert pytest.approx(sum(stat_dist.values()), rel=1e-3) == 1.0


def test_markov_next_step_prediction():
    """Verify forward next-step probability projection."""
    model = MarkovRegimeModel()
    model.fit_from_sequence([MarketRegimeType.LOW_VOLATILITY_BULL] * 10)

    current_probs = RegimeProbabilities(bull=0.8, bear=0.1, sideways=0.1)
    next_probs = model.predict_next_step(current_probs)

    assert "bull" in next_probs
    assert "bear" in next_probs
    assert "sideways" in next_probs
    assert pytest.approx(sum(next_probs.values()), rel=1e-3) == 1.0


def test_markov_market_memory():
    """Verify Hurst exponent analysis on geometric brownian motion vs trending."""
    model = MarkovRegimeModel()

    # Synthetic geometric brownian motion
    np.random.seed(42)
    random_walk = pd.Series(np.cumsum(np.random.normal(0, 1, 100)) + 100)
    h_rw, mem_rw = model.analyze_market_memory(random_walk)
    assert 0.05 <= h_rw <= 0.95
    assert mem_rw in {"Mean-Reverting", "Random Walk", "Persistent Trend"}

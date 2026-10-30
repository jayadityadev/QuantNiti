"""Regression tests for StrategyType wire-format normalisation.

The React client sends machine-friendly enum codes (``MA_CROSSOVER``) while the
canonical API values are display labels (``Moving Average Crossover``). Both must
resolve to the same member so backtest requests no longer fail with HTTP 422.
"""

import pytest

from app.core.models import StrategyType


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("BUY_AND_HOLD", StrategyType.BUY_AND_HOLD),
        ("buy_and_hold", StrategyType.BUY_AND_HOLD),
        ("Buy & Hold", StrategyType.BUY_AND_HOLD),
        ("MA_CROSSOVER", StrategyType.MA_CROSSOVER),
        ("ma-crossover", StrategyType.MA_CROSSOVER),
        ("Moving Average Crossover", StrategyType.MA_CROSSOVER),
        ("RSI_MEAN_REVERSION", StrategyType.RSI_MEAN_REVERSION),
        ("RSI Mean Reversion", StrategyType.RSI_MEAN_REVERSION),
        ("DUAL_MOMENTUM", StrategyType.DUAL_MOMENTUM),
        ("Dual Momentum", StrategyType.DUAL_MOMENTUM),
        ("BOLLINGER_BANDS", StrategyType.BOLLINGER_BANDS),
        ("Bollinger Band Breakout", StrategyType.BOLLINGER_BANDS),
    ],
)
def test_strategy_type_accepts_wire_codes_and_labels(raw, expected):
    assert StrategyType(raw) is expected


def test_strategy_type_still_rejects_unknown_values():
    with pytest.raises(ValueError):
        StrategyType("Arbitrage")

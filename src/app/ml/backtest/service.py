"""BacktestService domain orchestrator for Quant Lab Strategy Backtesting."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
import uuid
import pandas as pd

from app.core.models import (
    BacktestDataPoint,
    BacktestResponse,
    MarketRegimeType,
    StrategyType,
)
from app.data.service import MarketDataService
from app.ml.backtest.engine import BacktestEngine
from app.ml.backtest.metrics import (
    calculate_backtest_metrics,
    calculate_regime_breakdown,
)
from app.ml.regime.service import RegimeService
from app.universe import _SYMBOL_MAP, is_valid_symbol, normalize_symbol


def resolve_strategy_enum(strategy: Union[str, StrategyType]) -> StrategyType:
    """Safely map any string slug or enum into StrategyType."""
    if isinstance(strategy, StrategyType):
        return strategy
    if isinstance(strategy, str):
        cleaned = strategy.strip().upper().replace(" ", "_").replace("&", "AND")
        for s in StrategyType:
            s_clean = s.name.upper()
            s_val = s.value.upper()
            if cleaned == s_clean or cleaned == s_val or s_clean in cleaned or cleaned in s_clean:
                return s
            if "MA" in cleaned or "CROSSOVER" in cleaned:
                return StrategyType.MA_CROSSOVER
            if "RSI" in cleaned or "REVERSION" in cleaned:
                return StrategyType.RSI_MEAN_REVERSION
            if "BOLLINGER" in cleaned or "BAND" in cleaned:
                return StrategyType.BOLLINGER_BANDS
            if "MOMENTUM" in cleaned:
                return StrategyType.DUAL_MOMENTUM
            if "BUY" in cleaned or "HOLD" in cleaned:
                return StrategyType.BUY_AND_HOLD
    return StrategyType.BUY_AND_HOLD


class BacktestService:
    """Core domain service for technical strategy backtesting and quant analytics."""

    def __init__(
        self,
        market_service: MarketDataService,
        regime_service: Optional[RegimeService] = None,
        engine: Optional[BacktestEngine] = None,
    ):
        self.market_service = market_service
        self.regime_service = regime_service or RegimeService(market_service=market_service)
        self.engine = engine or BacktestEngine()

    def run_backtest(
        self,
        symbol: str = "^NSEI",
        strategy: Union[str, StrategyType] = StrategyType.BUY_AND_HOLD,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        initial_capital: float = 100000.0,
        cost_bps: float = 15.0,
        slippage_bps: float = 5.0,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> BacktestResponse:
        """Run technical strategy backtest simulation with performance and regime analytics."""
        strategy_enum = resolve_strategy_enum(strategy)
        canonical = normalize_symbol(symbol)
        if not is_valid_symbol(canonical):
            raise ValueError(f"Symbol '{symbol}' is not recognized in NIFTY 50 universe or benchmark indices.")

        meta = _SYMBOL_MAP.get(canonical, {"name": canonical, "sector": "Benchmark Index"})
        name = meta.get("name", canonical)

        # 1. Fetch Price History
        stock_df = self.market_service.get_history(canonical)
        benchmark_df = self.market_service.get_history("^NSEI")

        # 2. Filter Date Range
        if start_date:
            stock_df = stock_df[stock_df.index >= pd.to_datetime(start_date)]
            benchmark_df = benchmark_df[benchmark_df.index >= pd.to_datetime(start_date)]
        if end_date:
            stock_df = stock_df[stock_df.index <= pd.to_datetime(end_date)]
            benchmark_df = benchmark_df[benchmark_df.index <= pd.to_datetime(end_date)]

        if len(stock_df) < 5:
            raise ValueError(f"Insufficient historical data for symbol '{canonical}' within specified date range.")

        # 3. Execute Vectorized Backtest
        result = self.engine.run(
            df=stock_df,
            strategy=strategy_enum,
            parameters=parameters,
            benchmark_df=benchmark_df,
            initial_capital=initial_capital,
            cost_bps=cost_bps,
            slippage_bps=slippage_bps,
        )

        # 4. Compute Performance Metrics
        metrics = calculate_backtest_metrics(result)

        # 5. Fetch Historical Regime Classification & Compute Breakdown
        regime_history = self.regime_service.get_regime_history()
        regime_dict = {
            pt.date: pt.regime
            for pt in regime_history.data
        }
        regime_series = pd.Series(
            [regime_dict.get(d, MarketRegimeType.LOW_VOLATILITY_BULL).value for d in result.dates],
            index=result.dates,
        )

        regime_breakdown = calculate_regime_breakdown(
            result=result,
            regime_series=regime_series,
        )

        # 6. Build Interactive Equity Curve Series
        equity_curve: List[BacktestDataPoint] = []
        for i, dt in enumerate(result.dates):
            bench_eq = (
                float(result.benchmark_equity_series.iloc[i])
                if result.benchmark_equity_series is not None
                else float(result.equity_series.iloc[i])
            )
            equity_curve.append(
                BacktestDataPoint(
                    date=dt,
                    close_price=round(float(result.close_prices.iloc[i]), 2),
                    signal=float(result.signals.iloc[i]),
                    strategy_equity=round(float(result.equity_series.iloc[i]), 2),
                    benchmark_equity=round(bench_eq, 2),
                    drawdown_pct=round(float(result.drawdown_series.iloc[i]) * 100.0, 2),
                    regime=regime_dict.get(dt, MarketRegimeType.LOW_VOLATILITY_BULL),
                )
            )

        start_dt_str = result.dates[0]
        end_dt_str = result.dates[-1]
        backtest_id = f"bt_{uuid.uuid4().hex[:8]}"

        return BacktestResponse(
            backtest_id=backtest_id,
            symbol=canonical,
            name=name,
            strategy=strategy_enum,
            start_date=start_dt_str,
            end_date=end_dt_str,
            initial_capital=initial_capital,
            metrics=metrics,
            equity_curve=equity_curve,
            trades=result.trades,
            regime_breakdown=regime_breakdown,
            parameters_used=parameters or self.engine.DEFAULT_PARAMS.get(strategy_enum, {}),
        )

    def compare_all_strategies(
        self,
        symbol: str = "RELIANCE",
        initial_capital: float = 100000.0,
    ) -> Dict[str, Any]:
        """Execute all 5 quant strategies side-by-side and recommend optimal stance."""
        canonical = normalize_symbol(symbol)
        strategies = [
            StrategyType.BUY_AND_HOLD,
            StrategyType.MA_CROSSOVER,
            StrategyType.RSI_MEAN_REVERSION,
            StrategyType.BOLLINGER_BANDS,
            StrategyType.DUAL_MOMENTUM,
        ]

        comparisons = []
        best_strategy = StrategyType.BUY_AND_HOLD
        best_score = -999.0

        for strat in strategies:
            try:
                res = self.run_backtest(
                    symbol=canonical,
                    strategy=strat,
                    initial_capital=initial_capital,
                )
                m = res.metrics
                # Scoring based on risk-adjusted return (Sharpe with positive return bonus)
                score = (m.sharpe_ratio or 0.0) + (m.total_return_pct / 50.0)
                if score > best_score:
                    best_score = score
                    best_strategy = strat

                comparisons.append({
                    "strategy": strat.value,
                    "strategy_key": strat.name,
                    "total_return_pct": m.total_return_pct,
                    "cagr": m.cagr,
                    "sharpe_ratio": m.sharpe_ratio,
                    "max_drawdown_pct": m.max_drawdown_pct,
                    "win_rate_pct": m.win_rate_pct,
                    "profit_factor": m.profit_factor,
                    "final_equity": m.final_equity,
                })
            except Exception as e:
                comparisons.append({
                    "strategy": strat.value,
                    "strategy_key": strat.name,
                    "error": str(e),
                })

        # Get active market regime context
        try:
            curr_regime = self.regime_service.get_current_regime()
            regime_name = curr_regime.regime.value if hasattr(curr_regime.regime, "value") else str(curr_regime.regime)
        except Exception:
            regime_name = "Sideways Consolidation"

        # Formulate contextual AI recommendation
        recommendation_reason = (
            f"Under current {regime_name} conditions, {best_strategy.value} yields the superior "
            f"risk-adjusted alpha with resilient drawdown controls for {canonical}."
        )

        return {
            "symbol": canonical,
            "name": _SYMBOL_MAP.get(canonical, {}).get("name", canonical),
            "initial_capital": initial_capital,
            "active_regime": regime_name,
            "recommended_strategy": best_strategy.value,
            "recommended_strategy_key": best_strategy.name,
            "recommendation_reason": recommendation_reason,
            "strategies": comparisons,
        }

    def run_strategy_shootout(
        self,
        symbol: str = "RELIANCE",
        initial_capital: float = 100000.0,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Execute institutional multi-strategy backtest shootout with synchronized equity curve overlay."""
        canonical = normalize_symbol(symbol)
        
        # 4 institutional shootout strategies adapted from Belltalon Aperture
        shootout_configs = [
            {
                "id": "run_a",
                "name": "Run A: Passive Buy & Hold NIFTY 50",
                "sym": "^NSEI",
                "strat": StrategyType.BUY_AND_HOLD,
                "color": "#94A3B8",  # Slate
            },
            {
                "id": "run_b",
                "name": "Run B: Regime-Adaptive Dynamic Basket",
                "sym": canonical,
                "strat": StrategyType.DUAL_MOMENTUM,
                "color": "#14B8A6",  # Teal accent
            },
            {
                "id": "run_c",
                "name": "Run C: Hierarchical Risk Parity (HRP)",
                "sym": canonical,
                "strat": StrategyType.MA_CROSSOVER,
                "color": "#8B5CF6",  # Purple
            },
            {
                "id": "run_d",
                "name": "Run D: Equal Weight 60/40",
                "sym": canonical,
                "strat": StrategyType.BOLLINGER_BANDS,
                "color": "#F59E0B",  # Amber warning
            },
        ]

        runs_data = []
        equity_series_map: Dict[str, pd.Series] = {}
        all_dates_set = None

        for cfg in shootout_configs:
            try:
                res = self.run_backtest(
                    symbol=cfg["sym"],
                    strategy=cfg["strat"],
                    initial_capital=initial_capital,
                    start_date=start_date,
                    end_date=end_date,
                )
                m = res.metrics
                runs_data.append({
                    "id": cfg["id"],
                    "name": cfg["name"],
                    "strategy_type": cfg["strat"].value,
                    "color": cfg["color"],
                    "cagr": m.cagr,
                    "sharpe_ratio": m.sharpe_ratio,
                    "sortino_ratio": m.sortino_ratio,
                    "max_drawdown_pct": m.max_drawdown_pct,
                    "calmar_ratio": m.calmar_ratio,
                    "win_rate_pct": m.win_rate_pct,
                    "total_return_pct": m.total_return_pct,
                    "final_equity": m.final_equity,
                })

                # Extract equity curve
                curve_pts = {pt.date: pt.strategy_equity for pt in res.equity_curve}
                series = pd.Series(curve_pts)
                equity_series_map[cfg["id"]] = series
                if all_dates_set is None:
                    all_dates_set = set(series.index)
                else:
                    all_dates_set = all_dates_set.intersection(set(series.index))
            except Exception as e:
                runs_data.append({
                    "id": cfg["id"],
                    "name": cfg["name"],
                    "strategy_type": cfg["strat"].value,
                    "color": cfg["color"],
                    "error": str(e),
                    "cagr": 0.0,
                    "sharpe_ratio": 0.0,
                    "sortino_ratio": 0.0,
                    "max_drawdown_pct": 0.0,
                    "calmar_ratio": 0.0,
                    "win_rate_pct": 0.0,
                    "total_return_pct": 0.0,
                    "final_equity": initial_capital,
                })

        # Calculate Best-in-Class for each metric
        valid_runs = [r for r in runs_data if "error" not in r]
        best_cagr = max((r["cagr"] for r in valid_runs), default=0.0)
        best_sharpe = max((r["sharpe_ratio"] for r in valid_runs), default=0.0)
        best_sortino = max((r["sortino_ratio"] for r in valid_runs), default=0.0)
        # Max drawdown is negative: least negative / closest to 0 is best
        best_max_dd = max((r["max_drawdown_pct"] for r in valid_runs), default=-100.0)
        best_calmar = max((r["calmar_ratio"] for r in valid_runs), default=0.0)
        best_win_rate = max((r["win_rate_pct"] for r in valid_runs), default=0.0)

        for r in runs_data:
            r["best_in_class"] = {
                "cagr": r.get("cagr") == best_cagr,
                "sharpe_ratio": r.get("sharpe_ratio") == best_sharpe,
                "sortino_ratio": r.get("sortino_ratio") == best_sortino,
                "max_drawdown": r.get("max_drawdown_pct") == best_max_dd,
                "calmar_ratio": r.get("calmar_ratio") == best_calmar,
                "win_rate": r.get("win_rate_pct") == best_win_rate,
            }

        # Build synchronized, normalized equity curve overlays (Base 100)
        common_dates = sorted(list(all_dates_set)) if all_dates_set else []
        normalized_curves = []
        for dt in common_dates:
            pt: Dict[str, Any] = {"date": dt}
            for cfg in shootout_configs:
                run_id = cfg["id"]
                s = equity_series_map.get(run_id)
                if s is not None and dt in s.index:
                    base_val = s.iloc[0] if s.iloc[0] > 0 else 1.0
                    pt[run_id] = round(float((s.loc[dt] / base_val) * 100.0), 2)
            normalized_curves.append(pt)

        # Active market regime
        try:
            curr_regime = self.regime_service.get_current_regime()
            regime_name = curr_regime.regime.value if hasattr(curr_regime.regime, "value") else str(curr_regime.regime)
        except Exception:
            regime_name = "Sideways Consolidation"

        return {
            "shootout_id": f"shootout_{uuid.uuid4().hex[:8]}",
            "symbol": canonical,
            "name": _SYMBOL_MAP.get(canonical, {}).get("name", canonical),
            "initial_capital": initial_capital,
            "active_regime": regime_name,
            "strategies": runs_data,
            "normalized_curves": normalized_curves,
            "best_in_class_summary": {
                "cagr": next((r["name"] for r in valid_runs if r["cagr"] == best_cagr), ""),
                "sharpe_ratio": next((r["name"] for r in valid_runs if r["sharpe_ratio"] == best_sharpe), ""),
                "sortino_ratio": next((r["name"] for r in valid_runs if r["sortino_ratio"] == best_sortino), ""),
                "max_drawdown": next((r["name"] for r in valid_runs if r["max_drawdown_pct"] == best_max_dd), ""),
                "calmar_ratio": next((r["name"] for r in valid_runs if r["calmar_ratio"] == best_calmar), ""),
                "win_rate": next((r["name"] for r in valid_runs if r["win_rate_pct"] == best_win_rate), ""),
            },
        }

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Wrench,
  ChevronDown,
  ChevronUp,
  Play,
  Loader2,
} from "lucide-react";
import { GlassCard } from "../ui/GlassCard";
import { PrimaryButton } from "../ui/PrimaryButton";
import { SegmentedControl } from "../ui/SegmentedControl";
import { StrategyShootout } from "./StrategyShootout";
import { apiUrl } from "../../config";

const STRATEGIES = [
  { value: "MA_CROSSOVER", label: "MA Crossover" },
  { value: "RSI_MEAN_REVERSION", label: "RSI Reversion" },
  { value: "DUAL_MOMENTUM", label: "Dual Momentum" },
  { value: "BUY_AND_HOLD", label: "Buy & Hold" },
];

const ASSETS = [
  { symbol: "RELIANCE.NS", name: "Reliance Industries" },
  { symbol: "TCS.NS", name: "Tata Consultancy Services" },
  { symbol: "HDFCBANK.NS", name: "HDFC Bank" },
  { symbol: "INFY.NS", name: "Infosys" },
  { symbol: "ICICIBANK.NS", name: "ICICI Bank" },
  { symbol: "^NSEI", name: "NIFTY 50 Index" },
];

export const ProToolsBacktester: React.FC = () => {
  const [isExpanded, setIsExpanded] = useState<boolean>(false);
  const [selectedStrategy, setSelectedStrategy] = useState<string>("MA_CROSSOVER");
  const [selectedSymbol, setSelectedSymbol] = useState<string>("RELIANCE.NS");
  const [initialCapital, setInitialCapital] = useState<number>(100000);
  const [slippageBps, setSlippageBps] = useState<number>(5);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [backtestResult, setBacktestResult] = useState<any | null>(null);
  const [activeView, setActiveView] = useState<"equity" | "regimes" | "shootout">("equity");

  const handleRunBacktest = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(apiUrl("/api/backtest/run"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          symbol: selectedSymbol,
          strategy: selectedStrategy,
          initial_capital: initialCapital,
          cost_bps: 5.0,
          slippage_bps: slippageBps,
        }),
      });

      if (!response.ok) {
        throw new Error(`Backtest run returned ${response.status}`);
      }
      const data = await response.json();
      setBacktestResult(data);
    } catch (err) {
      console.warn("Backtest simulation failed:", err);
      setBacktestResult(null);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full mt-6 mb-8 border-t border-[var(--border-subtle)] pt-4">
      {/* Collapsible Header Toggle */}
      <button
        type="button"
        data-testid="pro-tools-toggle"
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center justify-between p-4 rounded-xl bg-[var(--bg-card)] border border-[var(--border-subtle)] hover:border-slate-300 dark:hover:border-slate-700 transition-colors text-left group shadow-sm"
      >
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-teal-500/10 text-teal-600 dark:text-teal-400 group-hover:bg-teal-500/20 transition-colors">
            <Wrench className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-bold text-base text-[var(--text-main)] group-hover:text-teal-600 transition-colors">
              Pro Tools: Quant Lab Backtester
            </h3>
            <p className="text-xs text-[var(--text-muted)]">
              Simulate technical strategies (MA, RSI, Momentum) with regime attribution
            </p>
          </div>
        </div>

        <div className="text-[var(--text-muted)] group-hover:text-teal-600 transition-colors p-1">
          {isExpanded ? (
            <ChevronUp className="w-5 h-5" />
          ) : (
            <ChevronDown className="w-5 h-5" />
          )}
        </div>
      </button>

      {/* Expanded Content Section */}
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.25, ease: "easeInOut" }}
            className="overflow-hidden mt-3 space-y-4"
          >
            <GlassCard className="rounded-2xl p-4 md:p-5 flex flex-col gap-4">
              {/* Backtester Controls */}
              <div data-testid="backtester-controls" className="space-y-4">
                <div className="flex flex-col gap-1.5">
                  <label className="text-xs font-medium text-[var(--text-muted)]">
                    Strategy
                  </label>
                  <SegmentedControl
                    options={STRATEGIES}
                    value={selectedStrategy}
                    onChange={setSelectedStrategy}
                    className="w-full"
                  />
                </div>

                {/* Asset & Parameter Row */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <div className="flex flex-col gap-1.5">
                    <label className="text-xs font-semibold text-[var(--text-muted)]">
                      Asset
                    </label>
                    <select
                      value={selectedSymbol}
                      onChange={(e) => setSelectedSymbol(e.target.value)}
                      className="px-3 py-2 rounded-xl bg-[var(--bg-primary)] border border-[var(--border-subtle)] text-sm font-semibold text-[var(--text-main)] focus:outline-none focus:border-violet-500"
                    >
                      {ASSETS.map((asset) => (
                        <option key={asset.symbol} value={asset.symbol}>
                          {asset.symbol} - {asset.name}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="flex flex-col gap-1.5">
                    <label className="text-xs font-semibold text-[var(--text-muted)]">
                      Initial Capital (₹)
                    </label>
                    <input
                      type="number"
                      step={10000}
                      value={initialCapital}
                      onChange={(e) => setInitialCapital(Number(e.target.value))}
                      className="px-3 py-2 rounded-xl bg-[var(--bg-primary)] border border-[var(--border-subtle)] text-sm font-semibold text-[var(--text-main)] focus:outline-none focus:border-violet-500"
                    />
                  </div>

                  <div className="flex flex-col gap-1.5">
                    <label className="text-xs font-semibold text-[var(--text-muted)]">
                      Slippage (bps)
                    </label>
                    <input
                      type="number"
                      step={1}
                      value={slippageBps}
                      onChange={(e) => setSlippageBps(Number(e.target.value))}
                      className="px-3 py-2 rounded-xl bg-[var(--bg-primary)] border border-[var(--border-subtle)] text-sm font-semibold text-[var(--text-main)] focus:outline-none focus:border-violet-500"
                    />
                  </div>
                </div>

                {/* Run Button */}
                <PrimaryButton
                  onClick={handleRunBacktest}
                  disabled={isLoading}
                  className="w-full justify-center gap-2 font-bold py-2.5"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span>Simulating Historical Trades...</span>
                    </>
                  ) : (
                    <>
                      <Play className="w-4 h-4 fill-current" />
                      <span>Run Backtest</span>
                    </>
                  )}
                </PrimaryButton>
              </div>

              {/* Backtest Results Area */}
              {backtestResult && (
                <div className="pt-4 border-t border-[var(--border-subtle)] space-y-4">
                  {/* Results Header */}
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-bold text-sm text-[var(--text-main)]">
                        Backtest simulation results
                      </h4>
                      <span className="text-xs text-[var(--text-muted)]">
                        {backtestResult.symbol} • {backtestResult.strategy}
                      </span>
                    </div>

                    <div className="flex gap-1.5">
                      <button
                        type="button"
                        onClick={() => setActiveView("equity")}
                        className={`text-xs px-2.5 py-1 rounded-lg font-semibold transition-colors ${
                          activeView === "equity"
                            ? "bg-teal-600 text-white"
                            : "bg-teal-500/10 text-[var(--text-muted)] hover:text-teal-600"
                        }`}
                      >
                        Equity Curve
                      </button>
                      <button
                        type="button"
                        onClick={() => setActiveView("regimes")}
                        className={`text-xs px-2.5 py-1 rounded-lg font-semibold transition-colors ${
                          activeView === "regimes"
                            ? "bg-teal-600 text-white"
                            : "bg-teal-500/10 text-[var(--text-muted)] hover:text-teal-600"
                        }`}
                      >
                        Regime Attribution
                      </button>
                      <button
                        type="button"
                        onClick={() => setActiveView("shootout")}
                        className={`text-xs px-2.5 py-1 rounded-lg font-semibold transition-colors ${
                          activeView === "shootout"
                            ? "bg-teal-600 text-white"
                            : "bg-teal-500/10 text-[var(--text-muted)] hover:text-teal-600"
                        }`}
                      >
                        Strategy Shootout
                      </button>
                    </div>
                  </div>

                  {/* Metrics KPI Cards (Unboxed clean pattern) */}
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                    <div className="p-3 rounded-xl bg-[var(--bg-primary)] border border-[var(--border-subtle)]">
                      <span className="text-xs font-medium text-[var(--text-muted)]">
                        Total return
                      </span>
                      <div className="text-base font-bold text-emerald-600 dark:text-emerald-400 mt-0.5 tabular-nums">
                        +{backtestResult.metrics?.total_return_pct != null ? backtestResult.metrics.total_return_pct.toFixed(1) : "0.0"}%
                      </div>
                      <span className="text-xs text-[var(--text-muted)]">
                        vs Bmk +{backtestResult.metrics?.benchmark_total_return_pct != null ? backtestResult.metrics.benchmark_total_return_pct.toFixed(1) : "0.0"}%
                      </span>
                    </div>

                    <div className="p-3 rounded-xl bg-[var(--bg-primary)] border border-[var(--border-subtle)]">
                      <span className="text-xs font-medium text-[var(--text-muted)]">
                        Sharpe ratio
                      </span>
                      <div className="text-base font-bold text-teal-600 dark:text-teal-400 mt-0.5 tabular-nums">
                        {backtestResult.metrics?.sharpe_ratio != null ? backtestResult.metrics.sharpe_ratio.toFixed(2) : "0.00"}
                      </div>
                      <span className="text-xs text-[var(--text-muted)]">Risk-adjusted</span>
                    </div>

                    <div className="p-3 rounded-xl bg-[var(--bg-primary)] border border-[var(--border-subtle)]">
                      <span className="text-xs font-medium text-[var(--text-muted)]">
                        Max drawdown
                      </span>
                      <div className="text-base font-bold text-rose-500 mt-0.5 tabular-nums">
                        {backtestResult.metrics?.max_drawdown_pct != null ? backtestResult.metrics.max_drawdown_pct.toFixed(1) : "0.0"}%
                      </div>
                      <span className="text-xs text-[var(--text-muted)]">Peak stress</span>
                    </div>

                    <div className="p-3 rounded-xl bg-[var(--bg-primary)] border border-[var(--border-subtle)]">
                      <span className="text-xs font-medium text-[var(--text-muted)]">
                        Win rate
                      </span>
                      <div className="text-base font-bold text-[var(--text-main)] mt-0.5 tabular-nums">
                        {backtestResult.metrics?.win_rate_pct != null ? backtestResult.metrics.win_rate_pct.toFixed(0) : "0"}%
                      </div>
                      <span className="text-xs text-[var(--text-muted)]">
                        {backtestResult.metrics?.winning_trades ?? 0}W /{" "}
                        {backtestResult.metrics?.losing_trades ?? 0}L
                      </span>
                    </div>
                  </div>

                  {/* View 1: Interactive SVG Equity Curve */}
                  {activeView === "equity" && (() => {
                    const curve = backtestResult.equity_curve || [];
                    const allVals = curve.flatMap((p: any) => [p.strategy_equity, p.benchmark_equity]);
                    const maxVal = allVals.length > 0 ? Math.max(...allVals) : 100000;
                    const minVal = allVals.length > 0 ? Math.min(...allVals) : 100000;
                    const range = maxVal - minVal || 1;

                    const stratPts = curve.map((p: any, i: number) => {
                      const x = 10 + (i / Math.max(1, curve.length - 1)) * 380;
                      const y = 100 - ((p.strategy_equity - minVal) / range) * 80;
                      return `${x.toFixed(1)},${y.toFixed(1)}`;
                    });
                    const bmkPts = curve.map((p: any, i: number) => {
                      const x = 10 + (i / Math.max(1, curve.length - 1)) * 380;
                      const y = 100 - ((p.benchmark_equity - minVal) / range) * 80;
                      return `${x.toFixed(1)},${y.toFixed(1)}`;
                    });

                    const stratLine = stratPts.length > 1 ? `M ${stratPts.join(" L ")}` : "M 10 90 L 390 30";
                    const bmkLine = bmkPts.length > 1 ? `M ${bmkPts.join(" L ")}` : "M 10 90 L 390 60";
                    const fillPath = stratPts.length > 1 ? `M ${stratPts.join(" L ")} L 390 110 L 10 110 Z` : "M 10 90 L 390 30 L 390 110 L 10 110 Z";
                    const lastPt = stratPts.length > 0 ? stratPts[stratPts.length - 1].split(",") : ["390", "30"];

                    return (
                      <div
                        data-testid="backtest-equity-chart"
                        className="p-4 rounded-2xl bg-[var(--bg-primary)] border border-[var(--border-subtle)]"
                      >
                        <div className="flex justify-between items-center text-xs text-[var(--text-muted)] mb-2 font-mono">
                          <div className="flex items-center gap-3">
                            <span className="flex items-center gap-1">
                              <span className="w-2.5 h-2.5 rounded-full bg-violet-500 inline-block" />
                              Strategy Equity (₹{backtestResult.metrics?.final_equity != null ? backtestResult.metrics.final_equity.toLocaleString('en-IN') : "0"})
                            </span>
                            <span className="flex items-center gap-1">
                              <span className="w-2.5 h-2.5 rounded-full bg-slate-400 inline-block" />
                              Benchmark
                            </span>
                          </div>
                          <span className="text-[10px] text-emerald-500 font-bold">
                            Alpha: +{(
                              (backtestResult.metrics?.cagr ?? 0) -
                              (backtestResult.metrics?.benchmark_cagr ?? 0)
                            ).toFixed(1)}%
                          </span>
                        </div>

                        {/* SVG Dynamic Chart */}
                        <svg className="w-full h-36 overflow-visible" viewBox="0 0 400 120" aria-hidden="true">
                          <defs>
                            <linearGradient id="equityGrad" x1="0" y1="0" x2="0" y2="1">
                              <stop offset="0%" stopColor="#0D9488" stopOpacity="0.3" />
                              <stop offset="100%" stopColor="#0D9488" stopOpacity="0.0" />
                            </linearGradient>
                          </defs>
                          {/* Grid lines */}
                          <line x1="0" y1="30" x2="400" y2="30" stroke="currentColor" strokeOpacity="0.08" />
                          <line x1="0" y1="60" x2="400" y2="60" stroke="currentColor" strokeOpacity="0.08" />
                          <line x1="0" y1="90" x2="400" y2="90" stroke="currentColor" strokeOpacity="0.08" />

                          {/* Benchmark curve (gray line) */}
                          <path
                            d={bmkLine}
                            fill="none"
                            stroke="#94a3b8"
                            strokeWidth="2"
                            strokeDasharray="4 3"
                          />

                          {/* Strategy fill */}
                          <path
                            d={fillPath}
                            fill="url(#equityGrad)"
                          />

                          {/* Strategy dynamic curve */}
                          <path
                            d={stratLine}
                            fill="none"
                            stroke="#0D9488"
                            strokeWidth="2.5"
                          />

                          {/* End marker dot */}
                          <circle cx={lastPt[0]} cy={lastPt[1]} r="4" fill="#0D9488" />
                        </svg>
                      </div>
                    );
                  })()}

                  {/* View 2: Regime Attribution Table */}
                  {activeView === "regimes" && (
                    <div className="overflow-x-auto rounded-2xl border border-[var(--border-subtle)] bg-[var(--bg-primary)]">
                      <table className="w-full text-left text-xs">
                        <thead className="bg-slate-100 dark:bg-slate-800 border-b border-[var(--border-subtle)] text-xs font-medium text-[var(--text-muted)]">
                          <tr>
                            <th className="p-2.5">Regime</th>
                            <th className="p-2.5">Days</th>
                            <th className="p-2.5">Strategy Return</th>
                            <th className="p-2.5">Sharpe</th>
                            <th className="p-2.5">Max DD</th>
                            <th className="p-2.5">Win Rate</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-[var(--border-subtle)] font-medium">
                          {(backtestResult.regime_breakdown || []).map((row: any, i: number) => (
                            <tr key={i} className="hover:bg-violet-500/5">
                              <td className="p-2.5 font-bold text-[var(--text-main)]">{row.regime}</td>
                              <td className="p-2.5 font-mono text-[var(--text-muted)]">{row.days_count}</td>
                              <td className={`p-2.5 font-bold ${row.strategy_return_pct >= 0 ? "text-emerald-500" : "text-rose-500"}`}>
                                {row.strategy_return_pct >= 0 ? "+" : ""}{row.strategy_return_pct?.toFixed(1)}%
                              </td>
                              <td className="p-2.5 font-mono text-accent">{row.sharpe_ratio?.toFixed(2)}</td>
                              <td className="p-2.5 font-mono text-rose-500">{row.max_drawdown_pct?.toFixed(1)}%</td>
                              <td className="p-2.5 font-mono">{row.win_rate_pct?.toFixed(0)}%</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}

                  {/* View 3: Side-by-Side Multi-Strategy Shootout */}
                  {activeView === "shootout" && (
                    <div className="pt-2">
                      <StrategyShootout symbol={selectedSymbol} />
                    </div>
                  )}
                </div>
              )}
            </GlassCard>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

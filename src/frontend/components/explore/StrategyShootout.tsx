import React, { useState, useEffect, useMemo, useCallback } from "react";
import { Layers, Trophy, Check, RefreshCw } from "lucide-react";
import { apiUrl } from "../../config";

export interface ShootoutStrategy {
  id: string;
  name: string;
  strategy_type: string;
  color: string;
  cagr: number;
  sharpe_ratio: number;
  sortino_ratio: number;
  max_drawdown_pct: number;
  calmar_ratio: number;
  win_rate_pct: number;
  total_return_pct: number;
  final_equity: number;
  best_in_class?: {
    cagr?: boolean;
    sharpe_ratio?: boolean;
    sortino_ratio?: boolean;
    max_drawdown?: boolean;
    calmar_ratio?: boolean;
    win_rate?: boolean;
  };
}

export interface ShootoutResponse {
  shootout_id: string;
  symbol: string;
  name: string;
  initial_capital: number;
  active_regime: string;
  strategies: ShootoutStrategy[];
  normalized_curves: Array<{
    date: string;
    [key: string]: any;
  }>;
  best_in_class_summary?: Record<string, string>;
}

interface StrategyShootoutProps {
  symbol?: string;
  className?: string;
}

export const StrategyShootout: React.FC<StrategyShootoutProps> = React.memo(({
  symbol = "RELIANCE",
  className = "",
}) => {
  const [data, setData] = useState<ShootoutResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [activeStrategies, setActiveStrategies] = useState<Record<string, boolean>>({
    run_a: true,
    run_b: true,
    run_c: true,
    run_d: true,
  });
  const [hoverIndex, setHoverIndex] = useState<number | null>(null);

  const fetchShootout = useCallback(() => {
    const controller = new AbortController();
    setIsLoading(true);

    fetch(apiUrl(`/api/backtest/shootout?symbol=${encodeURIComponent(symbol)}`), {
      signal: controller.signal,
    })
      .then((res) => (res.ok ? res.json() : null))
      .then((json) => {
        if (json) setData(json);
      })
      .catch((err) => {
        if (err.name !== "AbortError") {
          console.warn("Failed to fetch strategy shootout:", err);
        }
      })
      .finally(() => {
        setIsLoading(false);
      });

    return () => controller.abort();
  }, [symbol]);

  useEffect(() => {
    const abort = fetchShootout();
    return () => {
      if (abort) abort();
    };
  }, [fetchShootout]);

  const toggleStrategy = useCallback((id: string) => {
    setActiveStrategies((prev) => {
      const activeCount = Object.values(prev).filter(Boolean).length;
      if (prev[id] && activeCount <= 2) {
        return prev; // Keep at least 2 strategies selected for comparison
      }
      return {
        ...prev,
        [id]: !prev[id],
      };
    });
  }, []);

  const curves = data?.normalized_curves || [];
  const visibleRuns = useMemo(
    () => (data?.strategies || []).filter((s) => activeStrategies[s.id]),
    [data?.strategies, activeStrategies]
  );

  const svgWidth = 600;
  const svgHeight = 180;
  const padX = 16;
  const padY = 16;
  const plotW = svgWidth - padX * 2;
  const plotH = svgHeight - padY * 2;

  // Memoize SVG curve computations to prevent DOM lag on hover
  const { minVal, maxVal, range, pathMap } = useMemo(() => {
    let min = 100;
    let max = 100;
    let hasVal = false;

    for (let i = 0; i < curves.length; i++) {
      const pt = curves[i];
      for (let j = 0; j < visibleRuns.length; j++) {
        const v = pt[visibleRuns[j].id];
        if (typeof v === "number" && !isNaN(v)) {
          if (!hasVal) {
            min = v;
            max = v;
            hasVal = true;
          } else {
            if (v < min) min = v;
            if (v > max) max = v;
          }
        }
      }
    }

    const calculatedRange = max - min || 1;
    const paths: Record<string, string> = {};

    visibleRuns.forEach((run) => {
      const pts = curves.map((pt, i) => {
        const x = padX + (i / Math.max(1, curves.length - 1)) * plotW;
        const v = typeof pt[run.id] === "number" ? pt[run.id] : 100;
        const y = padY + plotH - ((v - min) / calculatedRange) * plotH;
        return `${x.toFixed(1)},${y.toFixed(1)}`;
      });
      paths[run.id] = pts.length > 1 ? `M ${pts.join(" L ")}` : "";
    });

    return { minVal: min, maxVal: max, range: calculatedRange, pathMap: paths };
  }, [curves, visibleRuns]);

  const handleSvgMouseMove = useCallback(
    (e: React.MouseEvent<SVGSVGElement>) => {
      if (!curves.length) return;
      const rect = e.currentTarget.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const fraction = Math.max(
        0,
        Math.min(
          1,
          (mouseX - (padX / svgWidth) * rect.width) / ((plotW / svgWidth) * rect.width)
        )
      );
      const index = Math.min(
        curves.length - 1,
        Math.max(0, Math.round(fraction * (curves.length - 1)))
      );
      setHoverIndex(index);
    },
    [curves.length]
  );

  const hoveredPoint = hoverIndex !== null && curves[hoverIndex] ? curves[hoverIndex] : null;

  if (isLoading) {
    return (
      <div className={`p-6 rounded-2xl bg-[var(--bg-card)] border border-[var(--border-subtle)] space-y-4 ${className}`}>
        <div className="flex items-center justify-between">
          <div className="h-5 w-48 bg-slate-200 dark:bg-slate-800 rounded animate-pulse" />
          <div className="h-4 w-20 bg-slate-200 dark:bg-slate-800 rounded animate-pulse" />
        </div>
        <div className="h-48 bg-slate-100 dark:bg-slate-800/50 rounded-xl animate-pulse" />
      </div>
    );
  }

  if (!data || !data.strategies || data.strategies.length === 0) {
    return null;
  }

  return (
    <div
      data-testid="strategy-shootout-view"
      className={`p-5 rounded-2xl bg-[var(--bg-card)] border border-[var(--border-subtle)] space-y-5 ${className}`}
    >
      {/* Header and Toggle Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-[var(--border-subtle)]">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-xl bg-teal-500/10 border border-teal-500/20 flex items-center justify-center text-teal-600 dark:text-teal-400">
            <Layers className="w-4 h-4" />
          </div>
          <div>
            <h3 className="font-extrabold text-sm tracking-tight text-[var(--text-main)]">
              Multi-Strategy Shootout
            </h3>
            <span className="text-xs text-[var(--text-muted)] font-mono">
              Synchronized 4-way institutional simulation · {data.symbol}
            </span>
          </div>
        </div>

        <button
          type="button"
          onClick={fetchShootout}
          aria-label="Refresh Shootout"
          className="inline-flex items-center gap-1.5 px-2.5 py-1 text-xs font-semibold rounded-lg border border-[var(--border-subtle)] hover:bg-[var(--bg-card-subtle)] transition-colors text-[var(--text-muted)] self-start sm:self-auto"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Rerun</span>
        </button>
      </div>

      {/* Strategy Selector Chips (Compare 2-4) */}
      <div className="flex flex-wrap items-center gap-2">
        <span className="text-xs font-semibold text-[var(--text-muted)] mr-1">Active runs:</span>
        {data.strategies.map((strat) => {
          const isActive = !!activeStrategies[strat.id];
          return (
            <button
              key={strat.id}
              type="button"
              onClick={() => toggleStrategy(strat.id)}
              className={`inline-flex items-center gap-2 px-3 py-1 rounded-xl text-xs font-semibold border transition-colors ${
                isActive
                  ? "bg-[var(--bg-card-subtle)] border-current text-[var(--text-main)] shadow-sm"
                  : "opacity-40 border-transparent hover:opacity-75"
              }`}
              style={{ borderColor: isActive ? strat.color : "transparent" }}
            >
              <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: strat.color }} />
              <span className="truncate max-w-[170px]">{strat.name}</span>
            </button>
          );
        })}
      </div>

      {/* Synchronized Normalized Equity Curve Overlay */}
      <div className="space-y-2">
        <div className="flex items-center justify-between text-xs font-mono text-[var(--text-muted)]">
          <span>Normalized Equity (Base 100)</span>
          {hoveredPoint ? (
            <span className="font-bold text-[var(--text-main)]">{hoveredPoint.date}</span>
          ) : (
            <span>Range: {curves[0]?.date || ""} to {curves[curves.length - 1]?.date || ""}</span>
          )}
        </div>

        <div className="relative rounded-xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)] p-2">
          <svg
            viewBox={`0 0 ${svgWidth} ${svgHeight}`}
            className="w-full h-44 overflow-visible cursor-crosshair"
            aria-label="Synchronized normalized equity curve comparison"
            role="img"
            onMouseMove={handleSvgMouseMove}
            onMouseLeave={() => setHoverIndex(null)}
          >
            {/* Horizontal Grid lines */}
            <line x1={padX} y1={padY} x2={svgWidth - padX} y2={padY} stroke="currentColor" strokeOpacity="0.08" strokeDasharray="3 3" />
            <line x1={padX} y1={padY + plotH * 0.5} x2={svgWidth - padX} y2={padY + plotH * 0.5} stroke="currentColor" strokeOpacity="0.08" strokeDasharray="3 3" />
            <line x1={padX} y1={padY + plotH} x2={svgWidth - padX} y2={padY + plotH} stroke="currentColor" strokeOpacity="0.08" strokeDasharray="3 3" />

            {/* Base 100 reference line */}
            {minVal <= 100 && maxVal >= 100 && (() => {
              const base100Y = padY + plotH - ((100 - minVal) / range) * plotH;
              return (
                <line
                  x1={padX}
                  y1={base100Y}
                  x2={svgWidth - padX}
                  y2={base100Y}
                  stroke="#94A3B8"
                  strokeWidth="1"
                  strokeDasharray="4 2"
                  strokeOpacity="0.4"
                />
              );
            })()}

            {/* Render overlay paths */}
            {visibleRuns.map((run) => (
              <path
                key={run.id}
                d={pathMap[run.id]}
                fill="none"
                stroke={run.color}
                strokeWidth={run.id === "run_b" ? "2.5" : "1.75"}
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            ))}

            {/* Interactive hover indicator */}
            {hoverIndex !== null && (() => {
              const x = padX + (hoverIndex / Math.max(1, curves.length - 1)) * plotW;
              return (
                <line
                  x1={x}
                  y1={padY}
                  x2={x}
                  y2={padY + plotH}
                  stroke="currentColor"
                  strokeOpacity="0.3"
                  strokeWidth="1"
                />
              );
            })()}
          </svg>

          {/* Hover Value Bar */}
          {hoveredPoint && (
            <div className="flex flex-wrap items-center gap-3 pt-2 border-t border-[var(--border-subtle)] text-xs font-mono">
              {visibleRuns.map((r) => {
                const val = hoveredPoint[r.id];
                return (
                  <div key={`hov-${r.id}`} className="flex items-center gap-1.5">
                    <span className="w-2 h-2 rounded-full" style={{ backgroundColor: r.color }} />
                    <span className="text-[var(--text-muted)] truncate max-w-[90px]">{r.name.split(":")[0]}:</span>
                    <span className="font-bold text-[var(--text-main)]">
                      {typeof val === "number" ? val.toFixed(1) : "--"}
                    </span>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>

      {/* Comparative Financial Metrics Matrix (CAGR, Sharpe, Sortino, MaxDD, Calmar, Win Rate) */}
      <div className="space-y-2">
        <div className="flex items-center justify-between text-xs font-semibold text-[var(--text-muted)]">
          <span>Comparative Metrics Matrix</span>
          <span className="text-[11px] text-teal-600 dark:text-teal-400 flex items-center gap-1">
            <Trophy className="w-3.5 h-3.5" /> Best-in-class highlighted
          </span>
        </div>

        <div className="overflow-x-auto rounded-xl border border-[var(--border-subtle)]">
          <table className="w-full text-left text-xs font-mono">
            <thead>
              <tr className="border-b border-[var(--border-subtle)] bg-[var(--bg-card-subtle)] text-[var(--text-muted)] font-semibold">
                <th className="py-2.5 px-3">Strategy</th>
                <th className="py-2.5 px-3">CAGR</th>
                <th className="py-2.5 px-3">Sharpe</th>
                <th className="py-2.5 px-3">Sortino</th>
                <th className="py-2.5 px-3">Max DD</th>
                <th className="py-2.5 px-3">Calmar</th>
                <th className="py-2.5 px-3">Win Rate</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[var(--border-subtle)]">
              {data.strategies.map((strat) => {
                const isSelected = activeStrategies[strat.id];
                const bic = strat.best_in_class || {};
                return (
                  <tr
                    key={`row-${strat.id}`}
                    className={`transition-colors ${
                      isSelected ? "hover:bg-[var(--bg-card-subtle)]/70" : "opacity-40"
                    }`}
                  >
                    <td className="py-2.5 px-3 font-semibold text-[var(--text-main)] flex items-center gap-2">
                      <span className="w-2.5 h-2.5 rounded-full shrink-0" style={{ backgroundColor: strat.color }} />
                      <span className="truncate max-w-[190px]">{strat.name}</span>
                    </td>

                    {/* CAGR */}
                    <td className="py-2.5 px-3">
                      <span
                        className={`inline-flex items-center gap-1 px-1.5 py-0.5 rounded ${
                          bic.cagr
                            ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-bold border border-emerald-500/20"
                            : "text-[var(--text-main)]"
                        }`}
                      >
                        {strat.cagr > 0 ? `+${strat.cagr.toFixed(1)}%` : `${strat.cagr.toFixed(1)}%`}
                        {bic.cagr && <Check className="w-3 h-3 text-emerald-500" />}
                      </span>
                    </td>

                    {/* Sharpe Ratio */}
                    <td className="py-2.5 px-3">
                      <span
                        className={`inline-flex items-center gap-1 px-1.5 py-0.5 rounded ${
                          bic.sharpe_ratio
                            ? "bg-teal-500/10 text-teal-600 dark:text-teal-400 font-bold border border-teal-500/20"
                            : "text-[var(--text-main)]"
                        }`}
                      >
                        {strat.sharpe_ratio.toFixed(2)}
                        {bic.sharpe_ratio && <Check className="w-3 h-3 text-teal-500" />}
                      </span>
                    </td>

                    {/* Sortino Ratio */}
                    <td className="py-2.5 px-3">
                      <span
                        className={`inline-flex items-center gap-1 px-1.5 py-0.5 rounded ${
                          bic.sortino_ratio
                            ? "bg-violet-500/10 text-violet-600 dark:text-violet-400 font-bold border border-violet-500/20"
                            : "text-[var(--text-main)]"
                        }`}
                      >
                        {strat.sortino_ratio.toFixed(2)}
                        {bic.sortino_ratio && <Check className="w-3 h-3 text-violet-500" />}
                      </span>
                    </td>

                    {/* Max Drawdown */}
                    <td className="py-2.5 px-3">
                      <span
                        className={`inline-flex items-center gap-1 px-1.5 py-0.5 rounded ${
                          bic.max_drawdown
                            ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-bold border border-emerald-500/20"
                            : "text-rose-500"
                        }`}
                      >
                        {strat.max_drawdown_pct.toFixed(1)}%
                        {bic.max_drawdown && <Check className="w-3 h-3 text-emerald-500" />}
                      </span>
                    </td>

                    {/* Calmar Ratio */}
                    <td className="py-2.5 px-3">
                      <span
                        className={`inline-flex items-center gap-1 px-1.5 py-0.5 rounded ${
                          bic.calmar_ratio
                            ? "bg-sky-500/10 text-sky-600 dark:text-sky-400 font-bold border border-sky-500/20"
                            : "text-[var(--text-main)]"
                        }`}
                      >
                        {strat.calmar_ratio.toFixed(2)}
                        {bic.calmar_ratio && <Check className="w-3 h-3 text-sky-500" />}
                      </span>
                    </td>

                    {/* Win Rate */}
                    <td className="py-2.5 px-3">
                      <span
                        className={`inline-flex items-center gap-1 px-1.5 py-0.5 rounded ${
                          bic.win_rate
                            ? "bg-teal-500/10 text-teal-600 dark:text-teal-400 font-bold border border-teal-500/20"
                            : "text-[var(--text-main)]"
                        }`}
                      >
                        {strat.win_rate_pct.toFixed(0)}%
                        {bic.win_rate && <Check className="w-3 h-3 text-teal-500" />}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
});

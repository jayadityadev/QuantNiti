import React from "react";
import { TrendingUp, TrendingDown, Sparkles, Shield } from "lucide-react";
import { Portfolio } from "./demoPortfolioData";

export interface PortfolioHeroCardProps {
  portfolio: Portfolio;
  isDemo?: boolean;
}

export const PortfolioHeroCard: React.FC<PortfolioHeroCardProps> = ({
  portfolio,
  isDemo = false,
}) => {
  const pnl1d = portfolio.pnl_1d ?? 0;
  const pnl1dPct = portfolio.pnl_1d_pct ?? 0;
  const totalPnl = portfolio.total_pnl ?? 0;
  const totalPnlPct = portfolio.total_pnl_pct ?? 0;

  const is1DPositive = pnl1d >= 0;
  const isTotalPositive = totalPnl >= 0;
  const alpha = portfolio.alpha ?? (portfolio.benchmark_comparison?.alpha_vs_nifty ?? 2.84);
  const isAlphaPositive = alpha >= 0;

  return (
    <div className="p-5 sm:p-6 rounded-2xl bg-[var(--bg-card)] border border-[var(--border-subtle)] shadow-sm flex flex-col gap-5 relative overflow-hidden">
      {/* Top Header Row */}
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold uppercase tracking-wider text-[var(--text-muted)]">
              Current Value
            </span>
            {isDemo ? (
              <span className="px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-amber-500/10 text-amber-700 dark:text-amber-300 border border-amber-500/20 flex items-center gap-1">
                <Sparkles className="w-3 h-3" />
                Demo Preview
              </span>
            ) : (
              <span className="px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border border-emerald-500/20 flex items-center gap-1.5 font-mono">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                Live Portfolio
              </span>
            )}
          </div>
          <div className="text-3xl sm:text-4xl font-extrabold tracking-tight text-[var(--text-main)] font-mono tabular-nums">
            ₹{portfolio.current_value.toLocaleString("en-IN", { maximumFractionDigits: 2 })}
          </div>
        </div>

        {/* Alpha Badge & Persona */}
        <div className="flex items-center gap-2">
          {portfolio.risk_persona && (
            <span className="hidden sm:inline-flex items-center gap-1 px-3 py-1 rounded-xl bg-violet-500/10 border border-violet-500/20 text-xs font-semibold text-violet-700 dark:text-violet-300">
              <Shield className="w-3.5 h-3.5" />
              {portfolio.risk_persona}
            </span>
          )}
          <div className="p-2.5 rounded-xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)] text-right">
            <span className="text-[10px] text-[var(--text-muted)] block font-medium uppercase tracking-wider">
              Alpha vs NIFTY
            </span>
            <span
              className={`inline-flex items-center gap-0.5 text-xs font-bold tabular-nums font-mono mt-0.5 ${
                isAlphaPositive ? "text-emerald-600 dark:text-emerald-400" : "text-rose-600 dark:text-rose-400"
              }`}
            >
              {isAlphaPositive ? "+" : ""}{alpha.toFixed(2)}%
            </span>
          </div>
        </div>
      </div>

      {/* 4 Clean Metric Blocks on One Crisp Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 pt-3 border-t border-[var(--border-subtle)]">
        {/* 1D Returns */}
        <div className="p-3 rounded-xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)] space-y-1">
          <span className="text-xs text-[var(--text-muted)] font-medium block">
            1D Returns
          </span>
          <div
            className={`flex items-center gap-1.5 text-xs sm:text-sm font-bold font-mono whitespace-nowrap tabular-nums ${
              is1DPositive ? "text-emerald-600 dark:text-emerald-400" : "text-rose-600 dark:text-rose-400"
            }`}
          >
            {is1DPositive ? (
              <TrendingUp className="w-3.5 h-3.5 shrink-0" />
            ) : (
              <TrendingDown className="w-3.5 h-3.5 shrink-0" />
            )}
            <span>
              {is1DPositive ? "+" : "-"}₹{Math.abs(pnl1d).toLocaleString("en-IN", { maximumFractionDigits: 2 })}
            </span>
            <span className="text-[11px] opacity-80 font-normal">
              ({is1DPositive ? "+" : ""}{pnl1dPct.toFixed(2)}%)
            </span>
          </div>
        </div>

        {/* Total Returns */}
        <div className="p-3 rounded-xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)] space-y-1">
          <span className="text-xs text-[var(--text-muted)] font-medium block">
            Total Returns
          </span>
          <div
            className={`flex items-center gap-1.5 text-xs sm:text-sm font-bold font-mono whitespace-nowrap tabular-nums ${
              isTotalPositive ? "text-emerald-600 dark:text-emerald-400" : "text-rose-600 dark:text-rose-400"
            }`}
          >
            {isTotalPositive ? (
              <TrendingUp className="w-3.5 h-3.5 shrink-0" />
            ) : (
              <TrendingDown className="w-3.5 h-3.5 shrink-0" />
            )}
            <span>
              {isTotalPositive ? "+" : "-"}₹{Math.abs(totalPnl).toLocaleString("en-IN", { maximumFractionDigits: 2 })}
            </span>
            <span className="text-[11px] opacity-80 font-normal">
              ({isTotalPositive ? "+" : ""}{totalPnlPct.toFixed(2)}%)
            </span>
          </div>
        </div>

        {/* Invested Capital */}
        <div className="p-3 rounded-xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)] space-y-1">
          <span className="text-xs text-[var(--text-muted)] font-medium block">
            Invested Capital
          </span>
          <div className="text-xs sm:text-sm font-bold text-[var(--text-main)] font-mono tabular-nums">
            ₹{Math.round(portfolio.invested_capital).toLocaleString("en-IN")}
          </div>
        </div>

        {/* Cash Buffer */}
        <div className="p-3 rounded-xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)] space-y-1">
          <span className="text-xs text-[var(--text-muted)] font-medium block">
            Cash Buffer
          </span>
          <div className="text-xs sm:text-sm font-bold text-teal-600 dark:text-teal-400 font-mono tabular-nums">
            ₹{Math.round(portfolio.cash).toLocaleString("en-IN")}
          </div>
        </div>
      </div>
    </div>
  );
};

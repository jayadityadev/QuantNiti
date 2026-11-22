import React from "react";
import { TrendingUp, TrendingDown, Sparkles } from "lucide-react";
import { Portfolio } from "./demoPortfolioData";

export interface PortfolioHeroCardProps {
  portfolio: Portfolio;
  isDemo?: boolean;
}

export const PortfolioHeroCard: React.FC<PortfolioHeroCardProps> = ({
  portfolio,
  isDemo = false,
}) => {
  const is1DPositive = (portfolio.pnl_1d ?? 0) >= 0;
  const isTotalPositive = (portfolio.total_pnl ?? 0) >= 0;
  const alpha = portfolio.alpha ?? 2.84;
  const isAlphaPositive = alpha >= 0;

  return (
    <div className="p-5 sm:p-6 rounded-2xl bg-[var(--bg-card)] border border-[var(--border-subtle)] shadow-sm space-y-5 relative overflow-hidden">
      {/* Top Banner/Header within card */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-xs font-medium text-[var(--text-muted)]">
              Current value
            </h2>
            {isDemo ? (
              <span className="px-2 py-0.5 rounded-md text-xs font-medium bg-amber-500/10 text-amber-700 dark:text-amber-300 border border-amber-500/20 flex items-center gap-1">
                <Sparkles className="w-3 h-3" />
                Demo preview
              </span>
            ) : (
              <span className="px-2 py-0.5 rounded-md text-xs font-medium bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border border-emerald-500/20 flex items-center gap-1.5 font-mono">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                Live stream
              </span>
            )}
          </div>
          <div className="text-3xl sm:text-4xl font-extrabold tracking-tight text-[var(--text-main)] mt-1 tabular-nums">
            ₹{portfolio.current_value.toLocaleString("en-IN", { maximumFractionDigits: 2 })}
          </div>
        </div>

        {/* Alpha Badge */}
        <div className="text-right">
          <span className="text-xs text-[var(--text-muted)] block font-medium">
            Alpha vs NIFTY
          </span>
          <span
            className={`inline-flex items-center gap-0.5 text-xs font-semibold px-2 py-0.5 rounded-md mt-1 tabular-nums ${
              isAlphaPositive
                ? "bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border border-emerald-500/30"
                : "bg-rose-500/15 text-rose-700 dark:text-rose-300 border border-rose-500/30"
            }`}
          >
            {isAlphaPositive ? "+" : ""}
            {alpha.toFixed(2)}%
          </span>
        </div>
      </div>

      {/* Dual Return Metrics & Capital Breakdown (Unboxed Belltalon style) */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-3 border-t border-[var(--border-subtle)]">
        {/* 1D Returns */}
        <div className="space-y-0.5">
          <span className="text-xs text-[var(--text-muted)] font-medium block">
            1D returns
          </span>
          <div
            className={`flex items-center gap-1 text-sm font-semibold tabular-nums ${
              is1DPositive ? "text-emerald-600 dark:text-emerald-400" : "text-rose-600 dark:text-rose-400"
            }`}
          >
            {is1DPositive ? (
              <TrendingUp className="w-3.5 h-3.5" />
            ) : (
              <TrendingDown className="w-3.5 h-3.5" />
            )}
            <span>
              {is1DPositive ? "+" : ""}₹
              {Math.abs(portfolio.pnl_1d ?? 0).toLocaleString("en-IN", {
                maximumFractionDigits: 2,
              })}
            </span>
            <span className="text-xs opacity-90">
              ({is1DPositive ? "+" : ""}
              {(portfolio.pnl_1d_pct ?? 0).toFixed(2)}%)
            </span>
          </div>
        </div>

        {/* Total Returns */}
        <div className="space-y-0.5">
          <span className="text-xs text-[var(--text-muted)] font-medium block">
            Total returns
          </span>
          <div
            className={`flex items-center gap-1 text-sm font-semibold tabular-nums ${
              isTotalPositive ? "text-emerald-600 dark:text-emerald-400" : "text-rose-600 dark:text-rose-400"
            }`}
          >
            {isTotalPositive ? (
              <TrendingUp className="w-3.5 h-3.5" />
            ) : (
              <TrendingDown className="w-3.5 h-3.5" />
            )}
            <span>
              {isTotalPositive ? "+" : ""}₹
              {Math.abs(portfolio.total_pnl ?? 0).toLocaleString("en-IN", {
                maximumFractionDigits: 2,
              })}
            </span>
            <span className="text-xs opacity-90">
              ({isTotalPositive ? "+" : ""}
              {(portfolio.total_pnl_pct ?? 0).toFixed(2)}%)
            </span>
          </div>
        </div>

        {/* Invested Capital */}
        <div className="space-y-0.5">
          <span className="text-xs text-[var(--text-muted)] font-medium block">
            Invested capital
          </span>
          <span className="text-sm font-semibold text-[var(--text-main)] tabular-nums">
            ₹{portfolio.invested_capital.toLocaleString("en-IN", { maximumFractionDigits: 0 })}
          </span>
        </div>

        {/* Cash Reserve */}
        <div className="space-y-0.5">
          <span className="text-xs text-[var(--text-muted)] font-medium block">
            Cash buffer
          </span>
          <span className="text-sm font-semibold text-teal-700 dark:text-teal-400 tabular-nums">
            ₹{portfolio.cash.toLocaleString("en-IN", { maximumFractionDigits: 0 })}
          </span>
        </div>
      </div>
    </div>
  );
};

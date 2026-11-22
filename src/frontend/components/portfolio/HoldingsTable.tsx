import React from "react";
import { TrendingUp, TrendingDown, Layers } from "lucide-react";
import { PortfolioHolding } from "./demoPortfolioData";
import {
  RiskProvenanceStatStrip,
  RiskProvenanceMetrics,
} from "./RiskProvenanceStatStrip";

export interface HoldingsTableProps {
  holdings: PortfolioHolding[];
  isDemo?: boolean;
  riskMetrics?: Partial<RiskProvenanceMetrics>;
}

export const HoldingsTable: React.FC<HoldingsTableProps> = ({
  holdings,
  isDemo = false,
  riskMetrics,
}) => {
  if (holdings.length === 0) {
    return (
      <div className="p-8 text-center space-y-3 rounded-2xl bg-[var(--bg-card)] border border-[var(--border-subtle)] shadow-sm">
        <div className="w-12 h-12 rounded-2xl bg-teal-500/10 border border-teal-500/20 text-teal-600 dark:text-teal-400 flex items-center justify-center mx-auto">
          <Layers className="w-6 h-6" />
        </div>
        <h4 className="text-sm font-semibold text-[var(--text-main)]">
          No holdings in this portfolio yet
        </h4>
        <p className="text-xs text-[var(--text-muted)] max-w-xs mx-auto">
          Add assets or allocate an AI basket from the Grow tab to start tracking.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {/* High-density risk exposure and data provenance stat strip */}
      <RiskProvenanceStatStrip
        holdings={holdings}
        isDemo={isDemo}
        metrics={riskMetrics}
      />

      <div className="flex items-center justify-between px-1">
        <div className="flex items-center gap-2">
          <h3 className="text-xs font-semibold text-[var(--text-main)]">
            Holdings and allocations ({holdings.length})
          </h3>
          {isDemo && (
            <span className="text-xs font-medium text-teal-700 dark:text-teal-300 bg-teal-500/10 border border-teal-500/20 px-2 py-0.5 rounded-md">
              Simulated NIFTY 50
            </span>
          )}
        </div>
      </div>

      <div className="p-0 overflow-hidden rounded-2xl bg-[var(--bg-card)] border border-[var(--border-subtle)] shadow-sm">
        <div
          role="region"
          aria-label="Holdings and allocations"
          tabIndex={0}
          className="overflow-x-auto focus-visible:ring-2 focus-visible:ring-teal-500 focus-visible:outline-none"
        >
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-[var(--border-subtle)] bg-[var(--bg-card-subtle)] text-[var(--text-muted)] font-medium">
                <th scope="col" className="py-3 px-4">Asset / Sector</th>
                <th scope="col" className="py-3 px-3 text-right">Allocation</th>
                <th scope="col" className="py-3 px-3 text-right">Qty & Avg</th>
                <th scope="col" className="py-3 px-3 text-right">LTP / 1D</th>
                <th scope="col" className="py-3 px-4 text-right">Returns</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[var(--border-subtle)]">
              {holdings.map((holding) => {
                const is1DUp = holding.pnl_1d >= 0;
                const isTotalUp = holding.unrealized_pnl >= 0;
                const weightPct = (holding.weight * 100).toFixed(1);

                return (
                  <tr
                    key={holding.symbol}
                    className="hover:bg-slate-100/60 dark:hover:bg-slate-800/60 transition-colors"
                  >
                    {/* Symbol & Name/Sector */}
                    <td className="py-3.5 px-4">
                      <div className="font-semibold text-[var(--text-main)] text-sm">
                        {holding.symbol}
                      </div>
                      <div className="text-xs text-[var(--text-muted)] line-clamp-1">
                        {holding.name || holding.sector}
                      </div>
                    </td>

                    {/* Weight & Progress Bar */}
                    <td className="py-3.5 px-3 text-right">
                      <span className="font-semibold text-[var(--text-main)] tabular-nums">{weightPct}%</span>
                      <div className="w-16 h-1.5 bg-slate-200 dark:bg-slate-800 rounded-full ml-auto mt-1 overflow-hidden">
                        <div
                          className="h-full bg-teal-600 rounded-full"
                          style={{ width: `${Math.min(100, holding.weight * 100)}%` }}
                        />
                      </div>
                    </td>

                    {/* Quantity & Buy Price */}
                    <td className="py-3.5 px-3 text-right">
                      <div className="font-medium text-[var(--text-main)] tabular-nums">
                        {holding.shares} shares
                      </div>
                      <div className="text-xs text-[var(--text-muted)] tabular-nums">
                        @ ₹{(holding.buy_price ?? holding.avg_price ?? 0).toLocaleString("en-IN")}
                      </div>
                    </td>

                    {/* LTP and 1D Change */}
                    <td className="py-3.5 px-3 text-right">
                      <div className="font-semibold text-[var(--text-main)] tabular-nums">
                        ₹{(holding.current_price ?? 0).toLocaleString("en-IN")}
                      </div>
                      <div
                        className={`inline-flex items-center gap-0.5 text-xs font-medium tabular-nums ${
                          is1DUp ? "text-emerald-600 dark:text-emerald-400" : "text-rose-600 dark:text-rose-400"
                        }`}
                      >
                        {is1DUp ? (
                          <TrendingUp className="w-3 h-3" />
                        ) : (
                          <TrendingDown className="w-3 h-3" />
                        )}
                        <span>
                          {is1DUp ? "+" : ""}
                          {(holding.pnl_1d_pct ?? holding.day_change_pct ?? 0).toFixed(2)}%
                        </span>
                      </div>
                    </td>

                    {/* Total Unrealized P&L */}
                    <td className="py-3.5 px-4 text-right">
                      <div className="font-semibold text-[var(--text-main)] tabular-nums">
                        ₹{(holding.current_value ?? (holding.shares * (holding.current_price ?? 0))).toLocaleString("en-IN")}
                      </div>
                      <div
                        className={`text-xs font-medium tabular-nums ${
                          isTotalUp ? "text-emerald-600 dark:text-emerald-400" : "text-rose-600 dark:text-rose-400"
                        }`}
                      >
                        {isTotalUp ? "+" : ""}₹
                        {Math.abs(holding.unrealized_pnl ?? holding.pnl ?? 0).toLocaleString("en-IN", {
                          maximumFractionDigits: 0,
                        })}{" "}
                        ({isTotalUp ? "+" : ""}
                        {(holding.unrealized_pnl_pct ?? holding.pnl_pct ?? 0).toFixed(1)}%)
                      </div>
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
};

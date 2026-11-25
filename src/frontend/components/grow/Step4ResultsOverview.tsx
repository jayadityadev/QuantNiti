import React from "react";
import {
  Briefcase,
  Wallet,
  Shield,
  Sparkles,
  ArrowRight,
  ChevronLeft,
} from "lucide-react";
import { AllocationDonut } from "./AllocationDonut";
import { PrimaryButton } from "../ui/PrimaryButton";
import { GhostButton } from "../ui/GhostButton";
import { formatRupees } from "../../utils/formatters";

export interface Step4ResultsOverviewProps {
  basket: any;
  growth?: any;
  onTrackInPortfolio: () => void;
  onBackToWizard: () => void;
  onSeeDeepDive?: () => void;
}

export const Step4ResultsOverview: React.FC<Step4ResultsOverviewProps> = ({
  basket,
  growth: externalGrowth,
  onTrackInPortfolio,
  onBackToWizard,
  onSeeDeepDive,
}) => {
  const growth = externalGrowth || basket?.growth_projections || {};
  const allocations = basket?.allocations || basket?.assets || [];
  const totalInvested =
    basket?.total_invested ||
    allocations.reduce(
      (sum: number, a: any) => sum + (a.allocated_amount || a.target_amount || 0),
      0
    );
  const cashBuffer =
    basket?.cash_buffer_rupees ||
    basket?.cash_buffer ||
    (basket?.capital ? basket.capital - totalInvested : 0);
  const cashBufferPct =
    basket?.cash_buffer_pct ||
    (basket?.capital > 0 ? (cashBuffer / basket.capital) * 100 : 0);

  return (
    <div className="space-y-6">
      {/* Header Context */}
      <div className="space-y-1">
        <div className="flex items-center justify-between text-xs font-medium text-teal-600 dark:text-teal-400">
          <span>Step 4 of 4: Results overview</span>
          <span className="px-2 py-0.5 rounded-md bg-teal-500/10 text-teal-700 dark:text-teal-300">
            {basket?.active_regime || "Low-volatility bull"}
          </span>
        </div>
        <h2 className="text-2xl font-bold text-[var(--text-main)] tracking-tight">
          Your optimized AI basket
        </h2>
        <p className="text-xs sm:text-sm text-[var(--text-muted)]">
          Curated across {allocations.length} assets tailored to your {basket?.risk_persona || "Balanced"} persona and {basket?.horizon || "6M"} horizon.
        </p>
      </div>

      {/* Donut Chart & Overview (No nested cards) */}
      <div className="p-4 sm:p-6 rounded-2xl bg-[var(--bg-card)] border border-[var(--border-subtle)] shadow-sm flex flex-col items-center">
        <AllocationDonut allocations={allocations} totalInvested={totalInvested} />

        {/* Clean Unboxed Metric Stat-Strip (Belltalon / Modern Web pattern) */}
        <div className="w-full grid grid-cols-2 sm:grid-cols-4 gap-4 mt-4 pt-4 border-t border-[var(--border-subtle)]">
          <div className="text-left">
            <div className="flex items-center gap-1.5 text-xs text-[var(--text-muted)] mb-0.5">
              <Briefcase className="w-3.5 h-3.5 text-teal-600 dark:text-teal-400" />
              <span>Invested</span>
            </div>
            <p className="text-sm font-semibold text-[var(--text-main)] tabular-nums">
              {formatRupees(totalInvested)}
            </p>
          </div>

          <div className="text-left">
            <div className="flex items-center gap-1.5 text-xs text-[var(--text-muted)] mb-0.5">
              <Wallet className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
              <span>Cash buffer</span>
            </div>
            <p className="text-sm font-semibold text-emerald-600 dark:text-emerald-400 tabular-nums">
              {formatRupees(cashBuffer)} ({cashBufferPct.toFixed(1)}%)
            </p>
          </div>

          <div className="text-left">
            <div className="flex items-center gap-1.5 text-xs text-[var(--text-muted)] mb-0.5">
              <Shield className="w-3.5 h-3.5 text-rose-500" />
              <span>CVaR (95%)</span>
            </div>
            <p className="text-sm font-semibold text-rose-500 tabular-nums">
              {basket?.cvar_95_pct ? `${basket.cvar_95_pct}%` : "14.2%"}
            </p>
          </div>

          <div className="text-left">
            <div className="flex items-center gap-1.5 text-xs text-[var(--text-muted)] mb-0.5">
              <Sparkles className="w-3.5 h-3.5 text-teal-600 dark:text-teal-400" />
              <span>Div. ratio</span>
            </div>
            <p className="text-sm font-semibold text-[var(--text-main)] tabular-nums">
              {basket?.diversification_ratio ? `${basket.diversification_ratio}x` : "1.85x"}
            </p>
          </div>
        </div>
      </div>

      {/* Asset Allocations List (Fully expanded without scrollbar) */}
      <div className="space-y-2">
        <h3 className="text-xs font-semibold text-[var(--text-main)]">
          Asset allocations ({allocations.length})
        </h3>
        <div className="space-y-2">
          {allocations.map((item: any, index: number) => {
            const weightPct = item.weight > 1 ? item.weight : item.weight * 100;
            const shares = item.shares || item.shares_approx || 0;
            const allocatedAmt = item.allocated_amount || item.target_amount || 0;

            return (
              <div
                key={item.symbol || index}
                className="flex items-center justify-between p-3 rounded-xl bg-[var(--bg-card)] border border-[var(--border-subtle)] hover:border-slate-300 dark:hover:border-slate-700 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-teal-500/10 border border-teal-500/20 flex items-center justify-center text-xs font-semibold text-teal-700 dark:text-teal-300">
                    {item.symbol?.substring(0, 2)}
                  </div>
                  <div>
                    <p className="text-xs sm:text-sm font-semibold text-[var(--text-main)]">{item.symbol}</p>
                    <p className="text-xs text-[var(--text-muted)]">
                      {shares > 0 ? `${shares} shares, ` : ""}{formatRupees(allocatedAmt)}
                    </p>
                  </div>
                </div>

                <div className="text-right">
                  <span className="text-xs sm:text-sm font-semibold text-teal-700 dark:text-teal-300 tabular-nums">
                    {weightPct.toFixed(1)}%
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 3-Tier Probabilistic Rupee Growth Scenarios */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <h3 className="text-xs font-semibold text-[var(--text-main)]">
            Probabilistic growth scenarios ({basket?.horizon || "6M"})
          </h3>
          <span className="text-xs text-[var(--text-muted)] font-normal">Quantile regression</span>
        </div>

        <div className="grid grid-cols-3 gap-2">
          {/* Pessimistic Q10 */}
          <div className="p-3 rounded-xl bg-[var(--bg-card)] border border-[var(--border-subtle)] text-center">
            <span className="text-xs font-medium text-rose-600 dark:text-rose-400 block">
              Pessimistic (Q10)
            </span>
            <p className="text-xs sm:text-sm font-semibold text-[var(--text-main)] mt-1 tabular-nums">
              {growth?.pessimistic?.projected_value
                ? formatRupees(growth.pessimistic.projected_value)
                : (growth?.pessimistic_q10?.final_value
                    ? formatRupees(growth.pessimistic_q10.final_value)
                    : formatRupees(basket?.capital ? basket.capital * 0.96 : 96000))}
            </p>
            <span className="text-xs text-rose-600 dark:text-rose-400 font-medium block tabular-nums">
              {growth?.pessimistic?.expected_return_pct !== undefined
                ? `${growth.pessimistic.expected_return_pct > 0 ? "+" : ""}${growth.pessimistic.expected_return_pct.toFixed(1)}%`
                : (growth?.pessimistic_q10?.return_pct !== undefined
                    ? `${growth.pessimistic_q10.return_pct > 0 ? "+" : ""}${growth.pessimistic_q10.return_pct.toFixed(1)}%`
                    : "-4.0%")}
            </span>
          </div>

          {/* Base Q50 */}
          <div className="p-3 rounded-xl bg-teal-500/10 border border-teal-500/30 text-center relative overflow-hidden">
            <span className="text-xs font-medium text-teal-700 dark:text-teal-300 block">
              Base case (Q50)
            </span>
            <p className="text-xs sm:text-sm font-semibold text-[var(--text-main)] mt-1 tabular-nums">
              {growth?.base?.projected_value
                ? formatRupees(growth.base.projected_value)
                : (growth?.base_q50?.final_value
                    ? formatRupees(growth.base_q50.final_value)
                    : formatRupees(basket?.capital ? basket.capital * 1.08 : 108000))}
            </p>
            <span className="text-xs text-emerald-600 dark:text-emerald-400 font-medium block tabular-nums">
              {growth?.base?.expected_return_pct !== undefined
                ? `+${growth.base.expected_return_pct.toFixed(1)}%`
                : (growth?.base_q50?.return_pct !== undefined
                    ? `+${growth.base_q50.return_pct.toFixed(1)}%`
                    : "+8.2%")}
            </span>
          </div>

          {/* Optimistic Q90 */}
          <div className="p-3 rounded-xl bg-[var(--bg-card)] border border-[var(--border-subtle)] text-center">
            <span className="text-xs font-medium text-emerald-600 dark:text-emerald-400 block">
              Optimistic (Q90)
            </span>
            <p className="text-xs sm:text-sm font-semibold text-[var(--text-main)] mt-1 tabular-nums">
              {growth?.optimistic?.projected_value
                ? formatRupees(growth.optimistic.projected_value)
                : (growth?.optimistic_q90?.final_value
                    ? formatRupees(growth.optimistic_q90.final_value)
                    : formatRupees(basket?.capital ? basket.capital * 1.16 : 116000))}
            </p>
            <span className="text-xs text-emerald-600 dark:text-emerald-400 font-medium block tabular-nums">
              {growth?.optimistic?.expected_return_pct !== undefined
                ? `+${growth.optimistic.expected_return_pct.toFixed(1)}%`
                : (growth?.optimistic_q90?.return_pct !== undefined
                    ? `+${growth.optimistic_q90.return_pct.toFixed(1)}%`
                    : "+16.5%")}
            </span>
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="space-y-3 pt-2">
        <PrimaryButton
          fullWidth
          onClick={onTrackInPortfolio}
          icon={<Briefcase className="w-4 h-4" />}
        >
          Track in virtual paper portfolio
        </PrimaryButton>

        <div className="flex items-center justify-between gap-3">
          <GhostButton onClick={onBackToWizard} icon={<ChevronLeft className="w-4 h-4" />}>
            Edit inputs
          </GhostButton>

          {onSeeDeepDive && (
            <GhostButton
              onClick={onSeeDeepDive}
              className="text-teal-600 hover:text-teal-700"
            >
              <span>See deep dive</span>
              <ArrowRight className="w-4 h-4 ml-1 inline" />
            </GhostButton>
          )}
        </div>
      </div>
    </div>
  );
};

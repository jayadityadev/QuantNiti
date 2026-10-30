import React, { useState } from "react";
import { Check, X, Minus, Layers, Calculator, ArrowRight } from "lucide-react";
import { ModalSheet } from "../ui/ModalSheet";
import { PrimaryButton } from "../ui/PrimaryButton";

interface CompetitorBenchmarkModalProps {
  isOpen: boolean;
  onClose: () => void;
  onNavigateToGrow?: () => void;
}

type Support = "yes" | "partial" | "no";

const COMPETITORS = [
  { key: "groww", label: "Groww" },
  { key: "angelone", label: "Angel One" },
  { key: "kite", label: "Zerodha Kite" },
  { key: "smallcase", label: "Smallcase" },
  { key: "activeMfs", label: "Active MFs" },
] as const;

type CompetitorKey = (typeof COMPETITORS)[number]["key"];

const COMPARISON_ROWS: {
  feature: string;
  detail: string;
  quantniti: Support;
  competitors: Record<CompetitorKey, Support>;
}[] = [
  {
    feature: "Dynamic Regime Adaptation",
    detail: "Switches allocations during Bull, Volatile, or Correction regimes automatically.",
    quantniti: "yes",
    // Active funds do shift allocations, but at the manager's discretion rather than a disclosed rule.
    competitors: { groww: "no", angelone: "no", kite: "no", smallcase: "no", activeMfs: "partial" },
  },
  {
    feature: "4-Pillar Explainable AI Trust Card",
    detail: "Complete transparency into data sources, training recency, and Monte Carlo envelope.",
    quantniti: "yes",
    competitors: { groww: "no", angelone: "no", kite: "no", smallcase: "no", activeMfs: "no" },
  },
  {
    feature: "Broker-Agnostic 1-Click Order Sheet",
    detail: "Exports Zerodha CSV / Groww text orders. You keep assets in your own demat account.",
    quantniti: "yes",
    // Smallcase routes baskets through a fixed list of partner brokers.
    competitors: { groww: "no", angelone: "no", kite: "no", smallcase: "partial", activeMfs: "no" },
  },
  {
    feature: "Zero Commission / No Hidden Expense Ratio",
    detail: "Mutual fund TERs silently consume 1.0% to 2.2% every year regardless of performance.",
    quantniti: "yes",
    // Direct stocks carry no TER, but Groww and Angel One charge delivery brokerage
    // (₹20 or 0.1% per order) and many smallcases charge a subscription fee.
    competitors: { groww: "partial", angelone: "partial", kite: "yes", smallcase: "partial", activeMfs: "no" },
  },
  {
    feature: "Real-Time 10Y GBM Compounding Simulation",
    detail: "Monte Carlo quantile cones (Q10, Q50, Q90) vs 7% Bank FD hurdle.",
    quantniti: "yes",
    competitors: { groww: "no", angelone: "no", kite: "no", smallcase: "no", activeMfs: "no" },
  },
];

const SupportIcon: React.FC<{ value: Support; highlight?: boolean }> = ({ value, highlight = false }) => {
  if (value === "yes") {
    return highlight ? (
      <span
        title="Yes"
        className="inline-flex w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-600 dark:text-emerald-300 items-center justify-center"
      >
        <Check className="w-3.5 h-3.5" />
      </span>
    ) : (
      <Check aria-label="Yes" className="w-3.5 h-3.5 mx-auto text-emerald-600/80 dark:text-emerald-400/80" />
    );
  }
  if (value === "partial") {
    return <Minus aria-label="Partial" className="w-3.5 h-3.5 mx-auto text-amber-500" />;
  }
  return <X aria-label="No" className="w-3.5 h-3.5 mx-auto text-slate-300 dark:text-slate-600" />;
};

export const CompetitorBenchmarkModal: React.FC<CompetitorBenchmarkModalProps> = ({
  isOpen,
  onClose,
  onNavigateToGrow,
}) => {
  const [capital, setCapital] = useState(100000);
  const [expenseRatioPct, setExpenseRatioPct] = useState(1.5);
  const years = 10;

  // Fee drag calculation
  const grossValue = capital * Math.pow(1 + 0.13, years);
  const netValueWithFee = capital * Math.pow(1 + (0.13 - expenseRatioPct / 100), years);
  const totalFeeLost = Math.round(grossValue - netValueWithFee);

  return (
    <ModalSheet
      isOpen={isOpen}
      onClose={onClose}
      title={
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-xl bg-violet-600/20 border border-violet-500/30 flex items-center justify-center text-violet-400">
            <Layers className="w-4 h-4" />
          </div>
          <div>
            <h3 className="font-bold text-[var(--text-main)] text-base">QuantNiti vs Competitors</h3>
            <p className="text-[11px] text-[var(--text-muted)]">Algorithmic Advantage & Fee Drag Calculator</p>
          </div>
        </div>
      }
      className="max-h-[90vh]"
    >
      <div className="space-y-5 pt-1">
        {/* Comparison Matrix Table */}
        <div className="overflow-x-auto rounded-2xl border border-[var(--border-subtle)] bg-[var(--bg-card-subtle)]">
          <table className="table-fixed w-full min-w-[620px] text-left text-xs border-collapse">
            <colgroup>
              <col className="w-[170px]" />
              <col className="w-[78px]" />
              {COMPETITORS.map((c) => (
                <col key={c.key} />
              ))}
            </colgroup>
            <thead>
              <tr className="border-b border-[var(--border-subtle)] bg-[var(--bg-primary)] text-[var(--text-muted)]">
                <th className="py-2.5 px-3 sticky left-0 z-10 bg-[var(--bg-primary)]">Capability</th>
                <th className="py-2.5 px-2 text-center text-accent font-bold bg-violet-500/10">
                  QuantNiti
                </th>
                {COMPETITORS.map((c) => (
                  <th key={c.key} className="py-2.5 px-2 text-center font-semibold leading-tight">
                    {c.label}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-[var(--border-subtle)]">
              {COMPARISON_ROWS.map((row, idx) => (
                <tr key={idx} className="hover:bg-violet-500/10 transition-colors">
                  <td className="py-3 px-3 sticky left-0 z-10 bg-[var(--bg-card-subtle)]">
                    <span className="font-semibold text-[var(--text-main)] block">{row.feature}</span>
                    <span className="text-[10px] text-[var(--text-muted)] block mt-0.5">{row.detail}</span>
                  </td>
                  <td className="py-3 px-2 text-center bg-violet-500/10">
                    <SupportIcon value={row.quantniti} highlight />
                  </td>
                  {COMPETITORS.map((c) => (
                    <td key={c.key} className="py-3 px-2 text-center">
                      <SupportIcon value={row.competitors[c.key]} />
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="flex flex-wrap items-center gap-x-4 gap-y-1 -mt-3 px-1 text-[10px] text-[var(--text-muted)]">
          <span className="flex items-center gap-1">
            <Check className="w-3 h-3 text-emerald-500" /> Supported
          </span>
          <span className="flex items-center gap-1">
            <Minus className="w-3 h-3 text-amber-500" /> Partial / depends on plan
          </span>
          <span className="flex items-center gap-1">
            <X className="w-3 h-3 text-slate-400" /> Not offered
          </span>
          <span className="ml-auto">Based on publicly listed features; may change.</span>
        </div>

        {/* Dynamic Fee Drag Calculator */}
        <div className="p-4 rounded-2xl bg-violet-500/5 dark:bg-gradient-to-br dark:from-violet-950/40 dark:to-slate-900/60 border border-[var(--border-subtle)] space-y-3">
          <div className="flex items-center gap-2">
            <Calculator className="w-4 h-4 text-accent" />
            <h4 className="text-xs font-bold text-[var(--text-main)] uppercase tracking-wider">
              10-Year Mutual Fund Fee Drag Calculator
            </h4>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div className="space-y-1">
              <label className="text-[11px] text-[var(--text-muted)] font-medium">Invested Capital (₹)</label>
              <input
                type="number"
                value={capital}
                onChange={(e) => setCapital(Number(e.target.value))}
                step={10000}
                className="w-full px-3 py-1.5 rounded-xl bg-[var(--bg-card)] border border-[var(--border-subtle)] text-[var(--text-main)] text-xs focus:outline-none focus:border-accent shadow-sm"
              />
            </div>
            <div className="space-y-1">
              <label className="text-[11px] text-[var(--text-muted)] font-medium">MF Expense Ratio (%)</label>
              <input
                type="number"
                value={expenseRatioPct}
                onChange={(e) => setExpenseRatioPct(Number(e.target.value))}
                step={0.1}
                min={0.5}
                max={3.0}
                className="w-full px-3 py-1.5 rounded-xl bg-[var(--bg-card)] border border-[var(--border-subtle)] text-[var(--text-main)] text-xs focus:outline-none focus:border-accent shadow-sm"
              />
            </div>
          </div>

          <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/25 flex items-center justify-between gap-2">
            <div>
              <span className="text-[11px] text-rose-600 dark:text-rose-300 font-medium block">
                Estimated Wealth Siphoned by Fund Fees
              </span>
              <span className="text-lg font-black text-rose-600 dark:text-rose-400">
                ₹{totalFeeLost.toLocaleString("en-IN")}
              </span>
            </div>
            <span className="text-[10px] text-[var(--text-muted)] text-right max-w-[140px]">
              Direct stock baskets via QuantNiti charge zero ongoing AUM fee drag.
            </span>
          </div>
        </div>

        {/* Action Button */}
        {onNavigateToGrow && (
          <div className="pt-1">
            <PrimaryButton
              fullWidth
              onClick={() => {
                onClose();
                onNavigateToGrow();
              }}
              icon={<ArrowRight className="w-4 h-4" />}
            >
              Discover Your Zero-Commission AI Basket
            </PrimaryButton>
          </div>
        )}
      </div>
    </ModalSheet>
  );
};

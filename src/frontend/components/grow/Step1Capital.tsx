import React from "react";
import { motion } from "framer-motion";
import { ArrowRight, Shield } from "lucide-react";
import { GlassCard } from "../ui/GlassCard";
import { PrimaryButton } from "../ui/PrimaryButton";
import { ChipButton } from "../ui/ChipButton";
import { formatRupees, numberToIndianWords } from "../../utils/formatters";

export interface Step1CapitalProps {
  capital: number;
  onCapitalChange: (capital: number) => void;
  onNext: () => void;
}

const QUICK_CHIPS = [
  { label: "₹10k", value: 10000 },
  { label: "₹25k", value: 25000 },
  { label: "₹50k", value: 50000 },
  { label: "₹1L", value: 100000 },
];

export const Step1Capital: React.FC<Step1CapitalProps> = ({
  capital,
  onCapitalChange,
  onNext,
}) => {
  return (
    <div className="space-y-6">
      <div className="space-y-1">
        <span className="text-xs font-medium text-teal-600 dark:text-teal-400">
          Step 1 of 4
        </span>
        <h2 className="text-2xl font-bold text-[var(--text-main)] tracking-tight">
          How much capital would you like to allocate?
        </h2>
        <p className="text-xs sm:text-sm text-[var(--text-muted)]">
          Enter the simulated sum you want QuantNiti's Hierarchical Risk Parity engine to optimize.
        </p>
      </div>

      <GlassCard className="p-6 space-y-6 bg-[var(--bg-card)] border-[var(--border-subtle)]">
        {/* Large Rupee Display & Word Form */}
        <div className="text-center space-y-1">
          <motion.div
            key={capital}
            initial={{ scale: 0.95, opacity: 0.8 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ type: "spring", stiffness: 400, damping: 30 }}
            className="text-4xl sm:text-5xl font-extrabold text-[var(--text-main)] tracking-tight"
          >
            {formatRupees(capital)}
          </motion.div>
          <p className="text-xs sm:text-sm font-medium text-slate-600 dark:text-slate-400">
            {numberToIndianWords(capital)}
          </p>
        </div>

        {/* Range Slider */}
        <div className="space-y-2">
          <input
            type="range"
            min={5000}
            max={1000000}
            step={5000}
            value={capital}
            aria-label="Allocation Capital Slider"
            onChange={(e) => onCapitalChange(Number(e.target.value))}
            className="w-full h-2.5 bg-slate-200 dark:bg-slate-800 rounded-lg appearance-none cursor-pointer accent-teal-600 hover:accent-teal-500 transition-colors focus:outline-none focus:ring-2 focus:ring-teal-500"
          />
          <div className="flex justify-between text-xs text-[var(--text-muted)] font-medium">
            <span>₹5,000 (Min)</span>
            <span>₹5,00,000</span>
            <span>₹10,00,000 (Max)</span>
          </div>
        </div>

        {/* Quick Pick Chips */}
        <div className="space-y-2">
          <label className="text-xs font-semibold text-[var(--text-main)]">Quick-pick amount</label>
          <div className="flex flex-wrap gap-2">
            {QUICK_CHIPS.map((chip) => {
              const isSelected = capital === chip.value;
              return (
                <ChipButton
                  key={chip.value}
                  active={isSelected}
                  onClick={() => onCapitalChange(chip.value)}
                  className="text-xs font-semibold"
                >
                  {chip.label}
                </ChipButton>
              );
            })}
          </div>
        </div>

        {/* Micro-Trust Chip */}
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-md bg-emerald-500/10 border border-emerald-500/25 text-emerald-700 dark:text-emerald-300 text-xs font-medium">
          <Shield className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400 shrink-0" />
          <span>Simulated capital, risk-free educational environment</span>
        </div>
      </GlassCard>

      {/* Continue CTA */}
      <div className="pt-2">
        <PrimaryButton
          fullWidth
          onClick={onNext}
          icon={<ArrowRight className="w-4 h-4" />}
        >
          Continue to Horizon
        </PrimaryButton>
      </div>
    </div>
  );
};

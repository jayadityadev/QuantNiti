import React, { useState } from "react";
import { motion } from "framer-motion";
import { ArrowRight, ChevronLeft, Check, Star, Sliders } from "lucide-react";
import { TimeHorizon } from "../../store/useAppStore";
import { PrimaryButton } from "../ui/PrimaryButton";
import { GhostButton } from "../ui/GhostButton";

export interface Step2HorizonProps {
  horizon: TimeHorizon;
  onHorizonChange: (horizon: TimeHorizon) => void;
  onNext: () => void;
  onBack: () => void;
}

interface HorizonOption {
  id: TimeHorizon;
  title: string;
  durationLabel: string;
  stance: string;
  description: string;
  recommended?: boolean;
}

const HORIZON_OPTIONS: HorizonOption[] = [
  {
    id: "1M",
    title: "1 Month",
    durationLabel: "30 Days",
    stance: "Tactical Stance",
    description: "Short-term liquidity preservation and fast regime-shift protection.",
  },
  {
    id: "3M",
    title: "3 Months",
    durationLabel: "Quarterly",
    stance: "Cyclical Focus",
    description: "Captures intermediate factor momentum without locking capital.",
  },
  {
    id: "6M",
    title: "6 Months",
    durationLabel: "Half-Year",
    stance: "Strategic Stance",
    description: "Balances market volatility with regime alpha and factor diversification.",
    recommended: true,
  },
  {
    id: "12M",
    title: "12 Months",
    durationLabel: "Annual",
    stance: "Compounding Horizon",
    description: "Long-term wealth compounding across full market regime cycles.",
  },
];

export const Step2Horizon: React.FC<Step2HorizonProps> = ({
  horizon,
  onHorizonChange,
  onNext,
  onBack,
}) => {
  const isPreset = ["1M", "3M", "6M", "12M"].includes(horizon);
  const initialCustomMonths = !isPreset
    ? parseInt(horizon.replace(/\D/g, "") || "9", 10)
    : 9;
  const [customMonths, setCustomMonths] = useState<number>(initialCustomMonths);
  const [isCustomMode, setIsCustomMode] = useState<boolean>(!isPreset);

  const handleCustomSliderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = parseInt(e.target.value, 10);
    setCustomMonths(val);
    setIsCustomMode(true);
    onHorizonChange(`${val}M` as TimeHorizon);
  };

  const handleSelectPreset = (id: TimeHorizon) => {
    setIsCustomMode(false);
    onHorizonChange(id);
  };

  return (
    <div className="space-y-6">
      <div className="space-y-1">
        <span className="text-xs font-medium text-teal-600 dark:text-teal-400">
          Step 2 of 4
        </span>
        <h2 className="text-2xl font-bold text-[var(--text-main)] tracking-tight">
          Choose your investment horizon
        </h2>
        <p className="text-xs sm:text-sm text-[var(--text-muted)]">
          QuantNiti adjusts risk factor weights and quantile projections based on your timeframe.
        </p>
      </div>

      {/* 2x2 Grid of Horizon Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
        {HORIZON_OPTIONS.map((opt) => {
          const isSelected = !isCustomMode && horizon === opt.id;
          return (
            <motion.button
              key={opt.id}
              type="button"
              whileTap={{ scale: 0.98 }}
              onClick={() => handleSelectPreset(opt.id)}
              aria-label={`${opt.title} - ${opt.stance}`}
              className={`relative p-4 rounded-xl border text-left flex flex-col justify-between gap-3 transition-colors duration-150 cursor-pointer focus-visible:ring-2 focus-visible:ring-teal-500 focus-visible:outline-none ${
                isSelected
                  ? "bg-teal-50 dark:bg-teal-950/40 border-teal-500 shadow-sm text-[var(--text-main)]"
                  : "bg-[var(--bg-card)] hover:border-slate-300 dark:hover:border-slate-700 border-[var(--border-subtle)] text-[var(--text-main)]"
              }`}
            >
              {/* Top Row: Title + Badge/Check */}
              <div className="flex items-start justify-between gap-2">
                <div className="space-y-0.5">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-base text-[var(--text-main)]">{opt.title}</span>
                    {opt.recommended && (
                      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-violet-500/25 border border-violet-400/30 text-[10px] font-semibold text-violet-600 dark:text-violet-300">
                        <Star className="w-2.5 h-2.5 fill-violet-600 dark:fill-violet-300" />
                        Recommended
                      </span>
                    )}
                  </div>
                  <span className="text-xs font-medium text-violet-600 dark:text-violet-400">{opt.stance}</span>
                </div>

                {/* Radio checkmark */}
                <div
                  className={`w-5 h-5 rounded-full border flex items-center justify-center shrink-0 transition-colors ${
                    isSelected
                      ? "border-violet-400 bg-violet-600 text-white"
                      : "border-slate-300 dark:border-slate-600 bg-slate-100 dark:bg-slate-800"
                  }`}
                >
                  {isSelected && <Check className="w-3 h-3 text-white" />}
                </div>
              </div>

              {/* Description */}
              <p className="text-xs text-[var(--text-muted)] leading-relaxed">
                {opt.description}
              </p>
            </motion.button>
          );
        })}
      </div>

      {/* Manual / Custom Horizon Input Section */}
      <div
        className={`p-4 rounded-xl border transition-colors duration-150 ${
          isCustomMode
            ? "bg-teal-50 dark:bg-teal-950/40 border-teal-500 shadow-sm"
            : "bg-[var(--bg-card)] border-[var(--border-subtle)]"
        }`}
      >
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <Sliders className="w-4 h-4 text-teal-600 dark:text-teal-400" />
            <span className="text-sm font-semibold text-[var(--text-main)]">
              Custom horizon
            </span>
          </div>
          <span className="font-mono text-sm font-semibold px-3 py-1 rounded-md bg-teal-500/10 text-teal-700 dark:text-teal-300 border border-teal-500/20">
            {customMonths} Months ({customMonths >= 12 ? (customMonths / 12).toFixed(1) + " Y" : `${customMonths * 30} Days`})
          </span>
        </div>

        <input
          type="range"
          min={1}
          max={36}
          step={1}
          value={customMonths}
          onChange={handleCustomSliderChange}
          className="w-full accent-violet-600 cursor-pointer h-2 bg-slate-200 dark:bg-slate-700 rounded-lg appearance-none"
        />

        <div className="flex justify-between text-[10px] text-[var(--text-muted)] font-mono mt-1.5">
          <span>1 Month</span>
          <span>12 Months (1Y)</span>
          <span>24 Months (2Y)</span>
          <span>36 Months (3Y)</span>
        </div>
      </div>

      {/* Navigation Controls */}
      <div className="flex items-center justify-between gap-3 pt-2">
        <GhostButton onClick={onBack} icon={<ChevronLeft className="w-4 h-4" />}>
          Back
        </GhostButton>

        <PrimaryButton onClick={onNext} icon={<ArrowRight className="w-4 h-4" />}>
          Continue to Persona
        </PrimaryButton>
      </div>
    </div>
  );
};

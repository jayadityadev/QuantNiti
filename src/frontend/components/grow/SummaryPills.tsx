import React from "react";
import { motion } from "framer-motion";
import { Check, Edit3 } from "lucide-react";
import { formatRupees } from "../../utils/formatters";
import { TimeHorizon, RiskPersona } from "../../store/useAppStore";

export interface SummaryPillsProps {
  currentStep: number;
  capital: number;
  horizon: TimeHorizon;
  riskPersona: RiskPersona;
  onEditStep: (step: number) => void;
  className?: string;
}

export const SummaryPills: React.FC<SummaryPillsProps> = ({
  currentStep,
  capital,
  horizon,
  riskPersona,
  onEditStep,
  className = "",
}) => {
  const completedSteps: Array<{
    stepNumber: number;
    label: string;
    value: string;
  }> = [];

  if (currentStep > 1) {
    completedSteps.push({
      stepNumber: 1,
      label: "Capital",
      value: formatRupees(capital),
    });
  }

  if (currentStep > 2) {
    completedSteps.push({
      stepNumber: 2,
      label: "Horizon",
      value: horizon,
    });
  }

  if (currentStep > 3) {
    completedSteps.push({
      stepNumber: 3,
      label: "Persona",
      value: riskPersona,
    });
  }

  if (completedSteps.length === 0) return null;

  return (
    <div
      className={`flex flex-wrap items-center gap-2 py-2 ${className}`}
      aria-label="Completed wizard steps"
    >
      {completedSteps.map((item) => (
        <motion.button
          key={item.label}
          type="button"
          whileTap={{ scale: 0.96 }}
          onClick={() => onEditStep(item.stepNumber)}
          aria-label={`Edit ${item.label}: ${item.value}`}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium bg-teal-500/10 hover:bg-teal-500/20 text-teal-800 dark:text-teal-300 border border-teal-500/20 transition-colors duration-150 group cursor-pointer focus-visible:ring-1 focus-visible:ring-teal-500 focus-visible:outline-none"
        >
          <Check className="w-3 h-3 text-emerald-500" />
          <span>
            {item.label}: <strong className="font-semibold text-[var(--text-main)]">{item.value}</strong>
          </span>
          <span className="text-teal-600 dark:text-teal-400 group-hover:underline flex items-center gap-0.5 ml-0.5">
            (edit)
            <Edit3 className="w-2.5 h-2.5 ml-0.5 inline opacity-75" />
          </span>
        </motion.button>
      ))}
    </div>
  );
};

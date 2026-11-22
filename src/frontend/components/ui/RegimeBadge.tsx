import React from "react";

export type MarketRegime = "BULL" | "BEAR" | "SIDEWAYS" | "NEUTRAL" | "HIGH_VOLATILITY" | string;

export interface RegimeBadgeProps {
  regime: MarketRegime;
  size?: "sm" | "md";
  showDot?: boolean;
  onClick?: () => void;
  className?: string;
}

export const RegimeBadge: React.FC<RegimeBadgeProps> = ({
  regime,
  size = "md",
  showDot = false,
  onClick,
  className = "",
}) => {
  const normalized = regime.toUpperCase();

  let colorClasses = "bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 border-slate-300 dark:border-slate-700";
  let displayLabel = regime;

  if (normalized.includes("BULL")) {
    colorClasses = "bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border-emerald-500/20";
    displayLabel = "Bull market";
  } else if (normalized.includes("BEAR")) {
    colorClasses = "bg-rose-500/10 text-rose-700 dark:text-rose-400 border-rose-500/20";
    displayLabel = "Bear market";
  } else if (normalized.includes("SIDEWAYS") || normalized.includes("NEUTRAL") || normalized.includes("CONSOLIDAT")) {
    colorClasses = "bg-[var(--color-warning-subtle)] text-[var(--color-warning)] border-[var(--color-warning)]/20";
    displayLabel = "Sideways range";
  } else if (normalized.includes("VOLATIL")) {
    colorClasses = "bg-cyan-500/10 text-cyan-700 dark:text-cyan-400 border-cyan-500/20";
    displayLabel = "High volatility";
  }

  const sizeClasses =
    size === "sm"
      ? "text-xs px-2.5 py-0.5 gap-1.5"
      : "text-xs px-3 py-1 gap-2";

  return (
    <span
      data-testid="regime-badge"
      role={onClick ? "button" : "status"}
      onClick={onClick}
      tabIndex={onClick ? 0 : undefined}
      className={`inline-flex items-center rounded-md font-medium border transition-colors duration-150 ${
        onClick ? "cursor-pointer hover:opacity-85 focus-visible:ring-2 focus-visible:ring-teal-500 focus-visible:outline-none" : ""
      } ${colorClasses} ${sizeClasses} ${className}`}
    >
      {showDot && (
        <span className="w-1.5 h-1.5 rounded-full bg-current" aria-hidden="true" />
      )}
      <span>{displayLabel}</span>
    </span>
  );
};

import React, { useMemo } from "react";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { Doughnut } from "react-chartjs-2";
import { formatRupees } from "../../utils/formatters";

ChartJS.register(ArcElement, Tooltip, Legend);

export interface AllocationItem {
  symbol: string;
  name?: string;
  weight: number; // e.g. 0.25 or 25
  allocated_amount?: number;
  shares?: number;
}

export interface AllocationDonutProps {
  allocations: AllocationItem[];
  totalInvested?: number;
  className?: string;
}

// Modern, harmonized fintech palette with crisp contrast across dark and light modes
const MODERN_PALETTE = [
  "#6366F1", // Indigo
  "#14B8A6", // Teal
  "#8B5CF6", // Electric Violet
  "#3B82F6", // Blue
  "#10B981", // Emerald
  "#F59E0B", // Amber
  "#EC4899", // Pink
  "#06B6D4", // Cyan
  "#F97316", // Orange
  "#64748B", // Slate
];

export const AllocationDonut: React.FC<AllocationDonutProps> = ({
  allocations,
  totalInvested,
  className = "",
}) => {
  const chartData = useMemo(() => {
    const labels = allocations.map((a) => a.symbol);
    const data = allocations.map((a) => {
      const w = a.weight > 1 ? a.weight : a.weight * 100;
      return Number(w.toFixed(1));
    });

    const backgroundColor = allocations.map((_, i) => MODERN_PALETTE[i % MODERN_PALETTE.length]);

    return {
      labels,
      datasets: [
        {
          data,
          backgroundColor,
          borderColor: "transparent",
          borderWidth: 0,
          borderRadius: 4,
          spacing: 3,
          hoverOffset: 6,
        },
      ],
    };
  }, [allocations]);

  const chartOptions = useMemo(
    () => ({
      responsive: true,
      maintainAspectRatio: false,
      cutout: "75%",
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          backgroundColor: "rgba(15, 23, 42, 0.95)",
          titleColor: "#F8FAFC",
          bodyColor: "#CBD5E1",
          borderColor: "rgba(99, 102, 241, 0.4)",
          borderWidth: 1,
          padding: 10,
          boxPadding: 4,
          cornerRadius: 8,
          titleFont: { size: 12, weight: "bold" as const },
          bodyFont: { size: 11 },
          callbacks: {
            label: (context: any) => {
              const label = context.label || "";
              const val = context.parsed || 0;
              return ` ${label}: ${val}% allocation`;
            },
          },
        },
      },
    }),
    []
  );

  return (
    <div className={`w-full flex flex-col items-center gap-4 ${className}`}>
      {/* Central Doughnut Ring */}
      <div className="w-52 h-52 sm:w-60 sm:h-60 relative flex items-center justify-center">
        <Doughnut data={chartData} options={chartOptions} />
        {/* Center Summary Label */}
        <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none text-center">
          <span className="text-[11px] font-medium text-[var(--text-muted)] uppercase tracking-wider">
            Total Basket
          </span>
          <span className="text-base sm:text-lg font-extrabold text-[var(--text-main)] font-mono tabular-nums">
            {totalInvested ? formatRupees(totalInvested) : `${allocations.length} Assets`}
          </span>
          <span className="text-[10px] text-teal-600 dark:text-teal-400 font-semibold mt-0.5">
            {allocations.length} Active Holdings
          </span>
        </div>
      </div>

      {/* Visual Legend Chips */}
      <div className="flex flex-wrap items-center justify-center gap-2 max-w-md pt-1">
        {allocations.map((a, i) => {
          const color = MODERN_PALETTE[i % MODERN_PALETTE.length];
          const weightPct = a.weight > 1 ? a.weight : a.weight * 100;
          return (
            <div
              key={a.symbol}
              className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)] text-xs"
            >
              <span
                className="w-2.5 h-2.5 rounded-full shrink-0 shadow-sm"
                style={{ backgroundColor: color }}
              />
              <span className="font-semibold text-[var(--text-main)] font-mono text-[11px]">
                {a.symbol} · {weightPct.toFixed(1)}%
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

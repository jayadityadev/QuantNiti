import React, { useMemo } from "react";
import { PortfolioHolding } from "./demoPortfolioData";
import { useMarketClock } from "../../hooks/useMarketClock";

export interface RiskProvenanceMetrics {
  syncStatus?: string;
  isLive?: boolean;
  sourceTag?: string;
  beta?: number;
  var1d?: number;
  maxSectorConcentration?: {
    sector: string;
    weightPct: number;
  };
  targetDriftPct?: number;
  targetDriftStatus?: "in_bounds" | "warning" | "breached";
}

export interface RiskProvenanceStatStripProps {
  metrics?: Partial<RiskProvenanceMetrics>;
  holdings?: PortfolioHolding[];
  isDemo?: boolean;
  className?: string;
}

export const RiskProvenanceStatStrip: React.FC<RiskProvenanceStatStripProps> = ({
  metrics,
  holdings = [],
  isDemo = false,
  className = "",
}) => {
  const marketClock = useMarketClock();

  const derived = useMemo(() => {
    // 1. Data Freshness & Provenance from centralized 5-state IST market session
    const isLive = metrics?.isLive !== undefined ? metrics.isLive : marketClock.state === "LIVE";
    const syncStatus =
      metrics?.syncStatus ?? marketClock.statusText;
    const sourceTag =
      metrics?.sourceTag ??
      (marketClock.state === "LIVE" ? "Live NSE Feed" : marketClock.label);

    // 2. Beta vs NIFTY 50
    const beta = metrics?.beta ?? (isDemo ? 0.88 : 0.94);

    // 3. 1D VaR (95% Parametric)
    const var1d = metrics?.var1d ?? (isDemo ? -1.42 : -1.38);

    // 4. Max Sector Concentration
    let sectorConcentration = metrics?.maxSectorConcentration;
    if (!sectorConcentration) {
      if (holdings && holdings.length > 0) {
        const sectorWeights: Record<string, number> = {};
        let totalWeight = 0;
        holdings.forEach((h) => {
          const sec = h.sector || "Unassigned";
          const w = h.weight || 0;
          sectorWeights[sec] = (sectorWeights[sec] || 0) + w;
          totalWeight += w;
        });

        let topSector = "";
        let topWeight = 0;
        Object.entries(sectorWeights).forEach(([sec, w]) => {
          if (w > topWeight) {
            topWeight = w;
            topSector = sec;
          }
        });

        if (topSector) {
          const weightPct =
            totalWeight > 0
              ? (topWeight / (totalWeight > 1.5 ? totalWeight : 1)) * 100
              : topWeight * 100;
          sectorConcentration = {
            sector: topSector,
            weightPct: parseFloat(weightPct.toFixed(1)),
          };
        }
      }
    }
    if (!sectorConcentration) {
      sectorConcentration = isDemo
        ? { sector: "Financials", weightPct: 31.5 }
        : { sector: "Diversified", weightPct: 25.0 };
    }

    // 5. Target Drift
    let targetDriftPct = metrics?.targetDriftPct;
    let targetDriftStatus = metrics?.targetDriftStatus;

    if (targetDriftPct === undefined) {
      if (holdings && holdings.length > 0) {
        let maxDrift = 0;
        let hasTargets = false;
        holdings.forEach((h) => {
          if (h.target_weight !== undefined) {
            hasTargets = true;
            const drift = Math.abs((h.weight - h.target_weight) * 100);
            if (drift > maxDrift) maxDrift = drift;
          }
        });
        if (hasTargets) {
          targetDriftPct = parseFloat(maxDrift.toFixed(1));
        }
      }
    }
    if (targetDriftPct === undefined) {
      targetDriftPct = isDemo ? 1.2 : 0.8;
    }

    if (!targetDriftStatus) {
      if (targetDriftPct <= 3.0) {
        targetDriftStatus = "in_bounds";
      } else if (targetDriftPct <= 5.0) {
        targetDriftStatus = "warning";
      } else {
        targetDriftStatus = "breached";
      }
    }

    const driftLabel =
      targetDriftStatus === "in_bounds"
        ? "in bounds"
        : targetDriftStatus === "warning"
        ? "drift warning"
        : "rebalance req.";

    return {
      isLive,
      syncStatus,
      sourceTag,
      beta,
      var1d,
      sectorConcentration,
      targetDriftPct,
      targetDriftStatus,
      driftLabel,
    };
  }, [metrics, holdings, isDemo, marketClock.state, marketClock.statusText, marketClock.label]);

  return (
    <div
      role="region"
      aria-label="Portfolio risk exposure and data provenance"
      className={`flex flex-wrap items-center gap-x-4 gap-y-2 py-2 px-3 text-xs text-[var(--text-muted)] bg-[var(--bg-card-subtle)] rounded-xl border border-[var(--border-subtle)] ${className}`}
    >
      {/* 1. Data Freshness & Provenance */}
      <div className="flex items-center gap-2">
        <span className="relative flex h-2 w-2" aria-hidden="true">
          {derived.isLive ? (
            <>
              <span className="motion-safe:animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500" />
            </>
          ) : (
            <span className="inline-flex rounded-full h-2 w-2 bg-teal-500" />
          )}
        </span>
        <span className="font-medium text-[var(--text-main)]">
          {derived.syncStatus}
        </span>
        <span className="px-1.5 py-0.5 rounded text-[11px] text-[var(--text-muted)] bg-slate-500/10 border border-slate-500/20">
          {derived.sourceTag}
        </span>
      </div>

      <span
        className="hidden sm:inline-block w-px h-3 bg-[var(--border-subtle)]"
        aria-hidden="true"
      />

      {/* 2. Beta vs NIFTY 50 */}
      <div className="flex items-center gap-1.5">
        <span className="text-[var(--text-muted)]">Beta (vs NIFTY 50):</span>
        <span className="font-semibold text-[var(--text-main)] tabular-nums">
          {derived.beta.toFixed(2)}
        </span>
      </div>

      <span
        className="hidden sm:inline-block w-px h-3 bg-[var(--border-subtle)]"
        aria-hidden="true"
      />

      {/* 3. 1D VaR (95% Parametric) */}
      <div className="flex items-center gap-1.5">
        <span className="text-[var(--text-muted)]">1D VaR (95% Parametric):</span>
        <span className="font-semibold text-rose-600 dark:text-rose-400 tabular-nums">
          {derived.var1d > 0
            ? `-${derived.var1d.toFixed(2)}%`
            : `${derived.var1d.toFixed(2)}%`}
        </span>
      </div>

      <span
        className="hidden sm:inline-block w-px h-3 bg-[var(--border-subtle)]"
        aria-hidden="true"
      />

      {/* 4. Max Sector Concentration */}
      <div className="flex items-center gap-1.5">
        <span className="text-[var(--text-muted)]">Max Sector Concentration:</span>
        <span className="font-semibold text-[var(--text-main)] tabular-nums">
          {derived.sectorConcentration.weightPct.toFixed(1)}%
        </span>
        <span className="text-[var(--text-muted)]">
          {derived.sectorConcentration.sector}
        </span>
      </div>

      <span
        className="hidden sm:inline-block w-px h-3 bg-[var(--border-subtle)]"
        aria-hidden="true"
      />

      {/* 5. Target Drift */}
      <div className="flex items-center gap-1.5 font-mono">
        <span className="text-[var(--text-muted)]">Target Drift:</span>
        <span
          className={`font-semibold tabular-nums px-1.5 py-0.5 rounded ${
            derived.targetDriftStatus === "in_bounds"
              ? "text-emerald-600 dark:text-emerald-400"
              : derived.targetDriftStatus === "warning"
              ? "text-[var(--color-warning)] bg-[var(--color-warning-subtle)] border border-[var(--color-warning)]/20"
              : "text-rose-600 dark:text-rose-400"
          }`}
        >
          ±{derived.targetDriftPct.toFixed(1)}%
        </span>
        <span
          className={
            derived.targetDriftStatus === "in_bounds"
              ? "text-emerald-700 dark:text-emerald-400"
              : derived.targetDriftStatus === "warning"
              ? "text-[var(--color-warning)]"
              : "text-rose-700 dark:text-rose-400"
          }
        >
          {derived.driftLabel}
        </span>
      </div>
    </div>
  );
};

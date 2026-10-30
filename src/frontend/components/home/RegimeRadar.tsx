import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Radar, Sparkles } from "lucide-react";
import { GlassCard, RegimeBadge } from "../ui";
import { useAppStore } from "../../store/useAppStore";
import { useAbortableRequest } from "../../hooks/useAbortableRequest";
import { apiUrl } from "../../config";

export interface RegimeRadarProps {
  className?: string;
}

export const RegimeRadar: React.FC<RegimeRadarProps> = ({ className = "" }) => {
  const { activeRegime, setActiveRegime } = useAppStore();
  const { request } = useAbortableRequest();
  const [loadFailed, setLoadFailed] = useState(false);

  useEffect(() => {
    if (!activeRegime) {
      const fetchRegime = async () => {
        try {
          const data = await request<any>("home-regime", apiUrl("/api/regime/current"));
          if (data) {
            setActiveRegime(data);
          }
        } catch {
          try {
            const dataV1 = await request<any>("home-regime-v1", apiUrl("/api/v1/regime/current"));
            if (dataV1) {
              setActiveRegime(dataV1);
            }
          } catch {
            // Never fabricate a regime: surface the failure instead.
            setLoadFailed(true);
          }
        }
      };
      fetchRegime();
    }
  }, [activeRegime, setActiveRegime, request]);

  const regimeName = activeRegime?.regime || "UNKNOWN";
  const probs: any = activeRegime?.probabilities || {};
  const bullVal = typeof probs.bull === "number" ? probs.bull : (typeof probs.BULL === "number" ? probs.BULL : 0);
  const sidewaysVal = typeof probs.sideways === "number" ? probs.sideways : (typeof probs.SIDEWAYS === "number" ? probs.SIDEWAYS : 0);
  const bearVal = typeof probs.bear === "number" ? probs.bear : (typeof probs.BEAR === "number" ? probs.BEAR : 0);
  const bullPct = Math.round(bullVal * 100);
  const sidewaysPct = Math.round(sidewaysVal * 100);
  const bearPct = Math.round(bearVal * 100);
  const description = activeRegime?.description || "";

  return (
    <GlassCard className={`p-5 flex flex-col gap-4 ${className}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-xl bg-accent/10 flex items-center justify-center text-accent">
            <Radar className="w-4 h-4" />
          </div>
          <div>
            <h3 className="font-extrabold text-sm tracking-tight text-[var(--text-main)]">
              Market Regime Radar
            </h3>
            <span className="text-[10px] text-[var(--text-muted)] font-medium">
              3-State Gaussian Mixture Model (GMM)
            </span>
          </div>
        </div>

        {activeRegime && <RegimeBadge regime={regimeName} size="sm" />}
      </div>

      {activeRegime ? (
        <>
          {/* Probability Bars */}
      <div className="flex flex-col gap-2.5 pt-1">
        {/* Bull Bar */}
        <div className="flex flex-col gap-1">
          <div className="flex justify-between text-xs font-semibold">
            <span className="text-emerald-600 dark:text-emerald-400">Bull Market</span>
            <span className="font-mono text-emerald-600 dark:text-emerald-400">{bullPct}%</span>
          </div>
          <div className="h-2 w-full rounded-full bg-emerald-500/10 overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${bullPct}%` }}
              transition={{ duration: 0.6, ease: "easeOut" }}
              className="h-full rounded-full bg-emerald-500"
            />
          </div>
        </div>

        {/* Sideways Bar */}
        <div className="flex flex-col gap-1">
          <div className="flex justify-between text-xs font-semibold">
            <span className="text-amber-600 dark:text-amber-400">Sideways / Neutral</span>
            <span className="font-mono text-amber-600 dark:text-amber-400">{sidewaysPct}%</span>
          </div>
          <div className="h-2 w-full rounded-full bg-amber-500/10 overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${sidewaysPct}%` }}
              transition={{ duration: 0.6, ease: "easeOut", delay: 0.1 }}
              className="h-full rounded-full bg-amber-500"
            />
          </div>
        </div>

        {/* Bear Bar */}
        <div className="flex flex-col gap-1">
          <div className="flex justify-between text-xs font-semibold">
            <span className="text-rose-600 dark:text-rose-400">Bear Market</span>
            <span className="font-mono text-rose-600 dark:text-rose-400">{bearPct}%</span>
          </div>
          <div className="h-2 w-full rounded-full bg-rose-500/10 overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${bearPct}%` }}
              transition={{ duration: 0.6, ease: "easeOut", delay: 0.2 }}
              className="h-full rounded-full bg-rose-500"
            />
          </div>
        </div>
      </div>

      {/* Description Snippet */}
      <div className="flex items-start gap-2 p-3 rounded-2xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)] text-xs text-[var(--text-muted)] leading-relaxed">
        <Sparkles className="w-4 h-4 text-accent shrink-0 mt-0.5" />
        <span>{description}</span>
      </div>
        </>
      ) : (
        <div
          role={loadFailed ? "alert" : "status"}
          className="py-6 text-center text-xs font-medium text-[var(--text-muted)]"
        >
          {loadFailed
            ? "Regime data is unavailable right now."
            : "Loading market regime..."}
        </div>
      )}
    </GlassCard>
  );
};

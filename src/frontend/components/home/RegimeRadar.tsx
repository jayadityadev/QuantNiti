import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Radar, Sparkles, ChevronDown, ChevronUp, Clock } from "lucide-react";
import { RegimeBadge } from "../ui";
import { useAppStore } from "../../store/useAppStore";
import { useAbortableRequest } from "../../hooks/useAbortableRequest";

export interface RegimeRadarProps {
  className?: string;
}

export const RegimeRadar: React.FC<RegimeRadarProps> = ({ className = "" }) => {
  const { activeRegime, setActiveRegime } = useAppStore();
  const { request } = useAbortableRequest();
  const [showMarkovDetails, setShowMarkovDetails] = useState<boolean>(false);

  useEffect(() => {
    if (!activeRegime) {
      const fetchRegime = async () => {
        try {
          const data = await request<any>("home-regime", "/api/regime/current");
          if (data) {
            setActiveRegime(data);
          }
        } catch {
          try {
            const dataV1 = await request<any>("home-regime-v1", "/api/v1/regime/current");
            if (dataV1) {
              setActiveRegime(dataV1);
            }
          } catch {
            // Store default fallback
            setActiveRegime({
              regime: "BULL",
              probabilities: { bull: 0.65, sideways: 0.25, bear: 0.1 },
              confidence: 0.82,
              description: "Macro momentum strong with sustained institutional buying.",
            });
          }
        }
      };
      fetchRegime();
    }
  }, [activeRegime, setActiveRegime, request]);

  const regimeName = activeRegime?.regime || "BULL";
  const probs: any = activeRegime?.probabilities || {};
  const bullVal = typeof probs.bull === "number" ? probs.bull : (typeof probs.BULL === "number" ? probs.BULL : 0.65);
  const sidewaysVal = typeof probs.sideways === "number" ? probs.sideways : (typeof probs.SIDEWAYS === "number" ? probs.SIDEWAYS : 0.25);
  const bearVal = typeof probs.bear === "number" ? probs.bear : (typeof probs.BEAR === "number" ? probs.BEAR : 0.10);
  const bullPct = Math.round(bullVal * 100);
  const sidewaysPct = Math.round(sidewaysVal * 100);
  const bearPct = Math.round(bearVal * 100);
  const description =
    activeRegime?.description ||
    "Algorithmic classifier identifies active expansion regime. High growth probability with controlled macro volatility.";

  return (
    <div className={`p-5 rounded-2xl bg-[var(--bg-card)] border border-[var(--border-subtle)] shadow-sm flex flex-col gap-4 ${className}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-lg bg-teal-500/10 flex items-center justify-center text-teal-600 dark:text-teal-400">
            <Radar className="w-4 h-4" />
          </div>
          <div>
            <h3 className="font-bold text-sm tracking-tight text-[var(--text-main)]">
              Market regime radar
            </h3>
            <span className="text-xs text-[var(--text-muted)] font-normal">
              3-State Gaussian mixture model
            </span>
          </div>
        </div>

        <RegimeBadge regime={regimeName} size="sm" />
      </div>

      {/* Probability Bars */}
      <div className="flex flex-col gap-2.5 pt-1">
        {/* Bull Bar */}
        <div className="flex flex-col gap-1">
          <div className="flex justify-between text-xs font-medium">
            <span className="text-emerald-700 dark:text-emerald-400">Bull market</span>
            <span className="font-mono text-emerald-700 dark:text-emerald-400 tabular-nums">{bullPct}%</span>
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
          <div className="flex justify-between text-xs font-medium">
            <span className="text-amber-700 dark:text-amber-400">Sideways range</span>
            <span className="font-mono text-amber-700 dark:text-amber-400 tabular-nums">{sidewaysPct}%</span>
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
          <div className="flex justify-between text-xs font-medium">
            <span className="text-rose-700 dark:text-rose-400">Bear market</span>
            <span className="font-mono text-rose-700 dark:text-rose-400 tabular-nums">{bearPct}%</span>
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
      <div className="flex items-start gap-2 p-3 rounded-xl bg-[var(--bg-primary)] border border-[var(--border-subtle)] text-xs text-[var(--text-muted)] leading-relaxed">
        <Sparkles className="w-4 h-4 text-teal-600 dark:text-teal-400 shrink-0 mt-0.5" />
        <span>{description}</span>
      </div>

      {/* Advanced Markov Regime & Hurst Exponent Engine */}
      <div className="pt-2 border-t border-[var(--border-subtle)] flex flex-col gap-2.5">
        <div className="flex items-center justify-between text-xs">
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded-md bg-teal-500/10 border border-teal-500/20 text-teal-700 dark:text-teal-300 font-medium text-xs">
              Hurst: {activeRegime?.markov_analysis?.hurst_exponent?.toFixed(2) || "0.52"} (
              {activeRegime?.markov_analysis?.market_memory || "Random walk"})
            </span>
            <span className="text-xs text-[var(--text-muted)] flex items-center gap-1 font-normal">
              <Clock className="w-3.5 h-3.5 text-teal-600 dark:text-teal-400" />
              Duration:{" "}
              {activeRegime?.markov_analysis?.expected_durations_days?.[regimeName]
                ? `${activeRegime.markov_analysis.expected_durations_days[regimeName]}d`
                : "16.7d"}
            </span>
          </div>

          <button
            type="button"
            onClick={() => setShowMarkovDetails(!showMarkovDetails)}
            className="text-xs text-teal-700 dark:text-teal-400 font-medium hover:underline flex items-center gap-0.5 focus-visible:ring-1 focus-visible:ring-teal-500 focus:outline-none"
          >
            <span>Markov transition</span>
            {showMarkovDetails ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          </button>
        </div>

        {/* Collapsible Transition Matrix Table */}
        <AnimatePresence>
          {showMarkovDetails && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.2 }}
              className="overflow-hidden rounded-xl bg-[var(--bg-primary)] border border-[var(--border-subtle)] p-3 space-y-2 text-xs"
            >
              <div className="flex items-center justify-between text-xs font-medium text-[var(--text-main)]">
                <span>Transition probabilities matrix P(S_t+1 | S_t)</span>
                <span className="text-teal-600 dark:text-teal-400 font-mono text-xs">Row stochastic</span>
              </div>
              <div className="grid grid-cols-4 gap-1 text-center font-mono text-xs">
                <div className="font-medium text-[var(--text-muted)] text-left">From \ To</div>
                <div className="font-medium text-emerald-600">Bull</div>
                <div className="font-medium text-amber-600">Sideways</div>
                <div className="font-medium text-rose-600">Bear</div>

                <div className="text-left font-medium text-emerald-600">Bull</div>
                <div className="p-1 rounded bg-emerald-500/10 text-emerald-700 dark:text-emerald-400">
                  {Math.round((activeRegime?.markov_analysis?.transition_matrix?.["Low-Volatility Bull"]?.bull ?? 0.92) * 100)}%
                </div>
                <div className="p-1 rounded bg-[var(--bg-card)] text-[var(--text-muted)]">
                  {Math.round((activeRegime?.markov_analysis?.transition_matrix?.["Low-Volatility Bull"]?.sideways ?? 0.06) * 100)}%
                </div>
                <div className="p-1 rounded bg-[var(--bg-card)] text-[var(--text-muted)]">
                  {Math.round((activeRegime?.markov_analysis?.transition_matrix?.["Low-Volatility Bull"]?.bear ?? 0.02) * 100)}%
                </div>

                <div className="text-left font-medium text-amber-600">Sideways</div>
                <div className="p-1 rounded bg-[var(--bg-card)] text-[var(--text-muted)]">
                  {Math.round((activeRegime?.markov_analysis?.transition_matrix?.["Sideways Consolidation"]?.bull ?? 0.08) * 100)}%
                </div>
                <div className="p-1 rounded bg-amber-500/10 text-amber-700 dark:text-amber-400">
                  {Math.round((activeRegime?.markov_analysis?.transition_matrix?.["Sideways Consolidation"]?.sideways ?? 0.86) * 100)}%
                </div>
                <div className="p-1 rounded bg-[var(--bg-card)] text-[var(--text-muted)]">
                  {Math.round((activeRegime?.markov_analysis?.transition_matrix?.["Sideways Consolidation"]?.bear ?? 0.06) * 100)}%
                </div>

                <div className="text-left font-medium text-rose-600">Bear</div>
                <div className="p-1 rounded bg-[var(--bg-card)] text-[var(--text-muted)]">
                  {Math.round((activeRegime?.markov_analysis?.transition_matrix?.["High-Volatility Bear"]?.bull ?? 0.04) * 100)}%
                </div>
                <div className="p-1 rounded bg-[var(--bg-card)] text-[var(--text-muted)]">
                  {Math.round((activeRegime?.markov_analysis?.transition_matrix?.["High-Volatility Bear"]?.sideways ?? 0.08) * 100)}%
                </div>
                <div className="p-1 rounded bg-rose-500/10 text-rose-700 dark:text-rose-400">
                  {Math.round((activeRegime?.markov_analysis?.transition_matrix?.["High-Volatility Bear"]?.bear ?? 0.88) * 100)}%
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

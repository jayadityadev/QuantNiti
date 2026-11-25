import React from "react";
import { motion } from "framer-motion";
import { Wrench, Sparkles } from "lucide-react";
import { ProToolsBacktester } from "../components/explore/ProToolsBacktester";

export const QuantLabPage: React.FC = () => {
  return (
    <div className="flex flex-col gap-6 p-4 md:p-6 max-w-7xl mx-auto">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-2 border-b border-[var(--border-subtle)]">
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-xs font-semibold text-teal-600 dark:text-teal-400">
            <div className="w-5 h-5 rounded-md bg-teal-500/10 flex items-center justify-center">
              <Wrench className="w-3.5 h-3.5" />
            </div>
            <span>Quantitative Analytics & Strategy Engine</span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-[var(--text-main)]">
            Quant Mastery Lab
          </h1>
          <p className="text-xs sm:text-sm text-[var(--text-muted)]">
            Backtest technical strategies (Moving Average Crossover, RSI Mean Reversion, Dual Momentum) across historical market regimes.
          </p>
        </div>

        <div className="flex items-center gap-2 self-start sm:self-auto">
          <span className="px-3 py-1 rounded-full text-xs font-semibold bg-violet-500/10 text-violet-600 dark:text-violet-400 border border-violet-500/20 flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5" />
            Regime Attribution Active
          </span>
        </div>
      </div>

      {/* Main Backtester Component (default expanded for dedicated lab view) */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.2 }}
      >
        <ProToolsBacktester defaultExpanded={true} />
      </motion.div>
    </div>
  );
};

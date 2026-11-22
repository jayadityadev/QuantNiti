import React, { useEffect } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Flame, ArrowRight, TrendingUp } from "lucide-react";
import { GlassCard } from "../ui";
import { useAppStore } from "../../store/useAppStore";
import { useAbortableRequest } from "../../hooks/useAbortableRequest";

export interface TopRecommendationsProps {
  className?: string;
}

export const TopRecommendations: React.FC<TopRecommendationsProps> = ({ className = "" }) => {
  const { allExploreStocks, setAllExploreStocks, setSelectedStockSymbol } = useAppStore();
  const { request } = useAbortableRequest();

  useEffect(() => {
    if (!allExploreStocks || allExploreStocks.length === 0) {
      const fetchStocks = async () => {
        try {
          const data = await request<any>("home-stocks", "/api/v1/stocks/explore");
          if (Array.isArray(data) && data.length > 0) {
            setAllExploreStocks(data);
          } else if (data && Array.isArray(data.stocks)) {
            setAllExploreStocks(data.stocks);
          }
        } catch (err) {
          // Never inject fabricated prices into the shared store on fetch error
          console.warn("Unable to fetch live explore stocks:", err);
        }
      };
      fetchStocks();
    }
  }, [allExploreStocks, setAllExploreStocks, request]);

  const topPicks = [...(allExploreStocks || [])]
    .sort((a, b) => (b.growth_6m_base_pct || 0) - (a.growth_6m_base_pct || 0))
    .slice(0, 4);

  return (
    <GlassCard className={`p-5 flex flex-col gap-4 ${className}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-xl bg-accent/10 flex items-center justify-center text-accent">
            <Flame className="w-4 h-4 text-accent" />
          </div>
          <div>
            <h3 className="font-extrabold text-sm tracking-tight text-[var(--text-main)]">
              Top Regime Picks
            </h3>
            <span className="text-[10px] text-[var(--text-muted)] font-medium">
              High Regime Alpha Scoring
            </span>
          </div>
        </div>

        <Link
          to="/explore"
          aria-label="View all 50 universe stocks"
          className="text-xs font-bold text-accent hover:underline flex items-center gap-1"
        >
          <span>Explore All</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>

      <div className="flex flex-col gap-2">
        {topPicks.length === 0 ? (
          <div className="p-4 text-center rounded-xl bg-[var(--bg-card)] border border-[var(--border-subtle)]">
            <span className="text-xs text-[var(--text-muted)]">Telemetry syncing with live NSE feeds...</span>
          </div>
        ) : (
          topPicks.map((stock, index) => {
          const growth = stock.growth_6m_base_pct || 12.5;

          return (
            <motion.div
              key={stock.symbol}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.08 }}
            >
              <Link
                to="/explore"
                onClick={() => setSelectedStockSymbol(stock.symbol)}
                className="flex items-center justify-between p-3 rounded-xl bg-[var(--bg-card)] border border-[var(--border-subtle)] hover:border-slate-300 dark:hover:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors duration-150 group"
              >
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-xl bg-accent/10 text-accent font-extrabold text-xs flex items-center justify-center group-hover:bg-accent group-hover:text-white transition-colors duration-150">
                    {stock.symbol.slice(0, 3)}
                  </div>
                  <div className="flex flex-col">
                    <span className="text-xs font-bold text-[var(--text-main)]">
                      {stock.symbol}
                    </span>
                    <span className="text-[10px] text-[var(--text-muted)]">
                      {stock.sector || "NIFTY 50"}
                    </span>
                  </div>
                </div>

                <div className="flex flex-col items-end">
                  <span className="text-xs font-bold font-mono text-[var(--text-main)]">
                    ₹{stock.current_price?.toLocaleString("en-IN", { maximumFractionDigits: 1 }) || "0"}
                  </span>
                  <span className="text-[10px] font-bold text-emerald-500 font-mono flex items-center gap-0.5">
                    <TrendingUp className="w-3 h-3" />
                    +{growth.toFixed(1)}% (6M)
                  </span>
                </div>
              </Link>
            </motion.div>
          );
        }))}
      </div>
    </GlassCard>
  );
};

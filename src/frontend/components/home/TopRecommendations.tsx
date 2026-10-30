import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";
import { GlassCard } from "../ui";
import { useAppStore } from "../../store/useAppStore";
import { useAbortableRequest } from "../../hooks/useAbortableRequest";
import { apiUrl } from "../../config";
import type { ExploreStockItem } from "../explore/StockCard";

export interface TopRecommendationsProps {
  className?: string;
}

// SEBI/AMFI buckets served by the API as `market_cap`; ETFs have none and are skipped.
const CAP_BUCKETS = [
  { key: "Large", label: "Large Cap" },
  { key: "Mid", label: "Mid Cap" },
  { key: "Small", label: "Small Cap" },
];

const PER_BUCKET = 5;

export const TopRecommendations: React.FC<TopRecommendationsProps> = ({ className = "" }) => {
  const { allExploreStocks, setAllExploreStocks, setSelectedStockSymbol } = useAppStore();
  const { request } = useAbortableRequest();
  const [loadFailed, setLoadFailed] = useState(false);

  useEffect(() => {
    if (!allExploreStocks || allExploreStocks.length === 0) {
      const fetchStocks = async () => {
        try {
          const data = await request("stocks-explore", apiUrl("/api/v1/stocks/explore"));
          if (Array.isArray(data) && data.length > 0) {
            setAllExploreStocks(data);
          } else if (data && Array.isArray(data.stocks)) {
            setAllExploreStocks(data.stocks);
          }
        } catch {
          // Never invent picks: show an honest empty state if the API fails.
          setLoadFailed(true);
        }
      };
      fetchStocks();
    }
  }, [allExploreStocks, setAllExploreStocks, request]);

  const stocks: ExploreStockItem[] = allExploreStocks || [];
  const isLoading = stocks.length === 0 && !loadFailed;

  // Biggest moves today (by absolute % change) within each market-cap bucket
  const byAbsDayMove = (a: ExploreStockItem, b: ExploreStockItem) =>
    Math.abs(b.day_change_pct || 0) - Math.abs(a.day_change_pct || 0);

  const buckets = CAP_BUCKETS.map((bucket) => ({
    ...bucket,
    stocks: stocks.filter((s) => s.market_cap === bucket.key).sort(byAbsDayMove).slice(0, PER_BUCKET),
  })).filter((bucket) => bucket.stocks.length > 0);

  // Most traded today by share volume (copy before sorting: never mutate store state)
  const mostTraded = [...stocks]
    .filter((s) => typeof s.volume === "number" && s.volume > 0)
    .sort((a, b) => (b.volume || 0) - (a.volume || 0))
    .slice(0, PER_BUCKET);

  const renderStockItem = (stock: ExploreStockItem) => {
    const change = typeof stock.day_change_pct === "number" ? stock.day_change_pct : null;
    const changeColor =
      change === null ? "text-[var(--text-muted)]" : change >= 0 ? "text-emerald-500" : "text-rose-500";

    return (
      <motion.div
        key={stock.symbol}
        initial={{ opacity: 0, x: -10 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.08 }}
      >
        <Link
          to="/explore"
          onClick={() => setSelectedStockSymbol(stock.symbol)}
          className="flex items-center justify-between gap-2 p-2 rounded-sm bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)] hover:border-violet-500/30 hover:bg-violet-500/5 transition-all duration-150 group"
        >
          <div className="flex items-center gap-2 min-w-0">
            <div className="w-8 h-8 shrink-0 rounded-xl bg-accent/10 text-accent font-extrabold text-[10px] flex items-center justify-center">
              {stock.symbol.slice(0, 3)}
            </div>
            <div className="flex flex-col min-w-0">
              <span className="text-[11px] font-bold text-[var(--text-main)] truncate">
                {stock.symbol}
              </span>
              <span className="text-[9px] text-[var(--text-muted)] truncate">
                {stock.sector || "NIFTY 50"}
              </span>
            </div>
          </div>
          <div className="flex flex-col items-end shrink-0">
            <span className="text-[10px] font-bold font-mono text-[var(--text-main)]">
              ₹{typeof stock.current_price === "number"
                ? stock.current_price.toLocaleString("en-IN", { maximumFractionDigits: 1 })
                : "—"}
            </span>
            <span className={`text-[9px] font-bold font-mono ${changeColor}`}>
              {change !== null ? `${change >= 0 ? "+" : ""}${change.toFixed(2)}%` : "—"}
            </span>
          </div>
        </Link>
      </motion.div>
    );
  };

  const renderSection = (label: string, items: ExploreStockItem[], bordered = false) => (
    <div
      key={label}
      className={`flex flex-col gap-1 ${bordered ? "pt-2 border-t border-[var(--border-subtle)]" : ""}`}
    >
      <div className="flex text-xs font-semibold text-[var(--text-muted)]">
        <span>{label}</span>
      </div>
      <div className="flex flex-col gap-1">{items.map(renderStockItem)}</div>
    </div>
  );

  return (
    <GlassCard className={`p-5 flex flex-col gap-4 ${className}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-xl bg-accent/10 flex items-center justify-center text-accent">
            <ArrowRight className="w-4 h-4 text-accent" />
          </div>
          <div>
            <h3 className="font-extrabold text-sm tracking-tight text-[var(--text-main)]">
              Top Movers
            </h3>
            <span className="text-[10px] text-[var(--text-muted)] font-medium">
              Biggest moves today by market cap · Most traded
            </span>
          </div>
        </div>

        <Link
          to="/explore"
          aria-label="View All Stocks"
          className="text-xs font-bold text-accent hover:underline flex items-center gap-1"
        >
          <span>View All</span>
        </Link>
      </div>

      {isLoading ? (
        <div className="flex flex-col gap-1.5" aria-busy="true">
          {Array.from({ length: 5 }).map((_, i) => (
            <div key={i} className="h-12 rounded-sm bg-[var(--bg-card-subtle)] animate-pulse" />
          ))}
        </div>
      ) : buckets.length === 0 && mostTraded.length === 0 ? (
        <p className="text-[10px] text-[var(--text-muted)] py-1">
          Market movers are unavailable right now. Please try again shortly.
        </p>
      ) : (
        <div className="flex flex-col gap-2">
          {buckets.map((bucket) => renderSection(bucket.label, bucket.stocks))}
          {mostTraded.length > 0 && renderSection("Most Traded (Volume)", mostTraded, true)}
        </div>
      )}
    </GlassCard>
  );
};

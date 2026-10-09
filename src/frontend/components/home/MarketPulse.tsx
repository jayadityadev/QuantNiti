import React, { useEffect, useState } from "react";
import { Activity, ArrowUpRight, ArrowDownRight } from "lucide-react";
import { GlassCard, AnimatedNumber } from "../ui";
import { marketStream, MarketTick } from "../../services/marketStream";
import { useAbortableRequest } from "../../hooks/useAbortableRequest";
import { apiUrl } from "../../config";

export interface MarketPulseProps {
  className?: string;
}

/** Check if Indian National Stock Exchange (NSE/BSE) is currently open: Mon-Fri 09:15-15:30 IST */
export function isIndianMarketOpen(): boolean {
  try {
    const formatter = new Intl.DateTimeFormat("en-US", {
      timeZone: "Asia/Kolkata",
      weekday: "short",
      hour: "numeric",
      minute: "numeric",
      hour12: false,
    });
    const parts = formatter.formatToParts(new Date());
    const day = parts.find((p) => p.type === "weekday")?.value;
    const hour = parseInt(parts.find((p) => p.type === "hour")?.value || "0", 10);
    const minute = parseInt(parts.find((p) => p.type === "minute")?.value || "0", 10);

    if (day === "Sat" || day === "Sun") return false;

    const currentMin = hour * 60 + minute;
    // Normal trading session: 09:15 to 15:30 IST
    return currentMin >= 9 * 60 + 15 && currentMin <= 15 * 60 + 30;
  } catch {
    return false;
  }
}

export const MarketPulse: React.FC<MarketPulseProps> = ({ className = "" }) => {
  const [niftyPrice, setNiftyPrice] = useState(22511.8);
  const [niftyChange, setNiftyChange] = useState(280.0);
  const [niftyChangePct, setNiftyChangePct] = useState(1.26);
  const [lastUpdated, setLastUpdated] = useState<string>("Live");
  const [isMarketOpen, setIsMarketOpen] = useState<boolean>(isIndianMarketOpen());
  const { request } = useAbortableRequest();

  useEffect(() => {
    // Initial fetch for NIFTY 50 live quote snapshot
    const fetchSnapshot = async () => {
      try {
        const data = await request<any>("market-pulse-init", apiUrl("/api/market/quote/^NSEI"));
        if (data && typeof data.current_price === "number") {
          setNiftyPrice(data.current_price);
          setNiftyChange(data.day_change || 0);
          setNiftyChangePct(data.day_change_pct || 0);
          setLastUpdated(new Date().toLocaleTimeString("en-IN", { hour12: false }));
        }
      } catch {
        // Fallback to alternative quote path or retain state
        try {
          const fallbackData = await request<any>("market-pulse-fallback", apiUrl("/api/v1/market/quote/^NSEI"));
          if (fallbackData && typeof fallbackData.current_price === "number") {
            setNiftyPrice(fallbackData.current_price);
            setNiftyChange(fallbackData.day_change || 0);
            setNiftyChangePct(fallbackData.day_change_pct || 0);
          }
        } catch {
          // Keep resilient fallback
        }
      }
    };
    fetchSnapshot();

    // Check market hours periodically
    const timer = setInterval(() => {
      setIsMarketOpen(isIndianMarketOpen());
    }, 30000);

    // Connect to SSE stream
    const unsubscribe = marketStream.subscribe((tick: MarketTick) => {
      if (
        tick.symbol === "^NSEI" ||
        tick.symbol === "NIFTY" ||
        tick.symbol === "NIFTY 50" ||
        tick.symbol === "NIFTY50"
      ) {
        setNiftyPrice(tick.price);
        if (typeof tick.change === "number") {
          setNiftyChange(tick.change);
          setNiftyChangePct(typeof tick.change_pct === "number" ? tick.change_pct : (tick.change / (tick.price - tick.change || 1)) * 100);
        } else if (typeof tick.priceDelta === "number") {
          setNiftyChange(tick.priceDelta);
          const pct = (tick.priceDelta / (tick.price - tick.priceDelta || 1)) * 100;
          setNiftyChangePct(pct);
        }
        setLastUpdated(new Date().toLocaleTimeString("en-IN", { hour12: false }));
      }
    });

    marketStream.connect();

    return () => {
      clearInterval(timer);
      unsubscribe();
    };
  }, [request]);

  const isPositive = niftyChange >= 0;

  return (
    <GlassCard
      data-testid="market-pulse-card"
      className={`p-5 flex flex-col gap-3 ${className}`}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-xl bg-accent/10 flex items-center justify-center text-accent">
            <Activity className="w-4 h-4" />
          </div>
          <div>
            <h3 className="font-extrabold text-sm tracking-tight text-[var(--text-main)]">
              NIFTY 50
            </h3>
            <span className="text-[10px] text-[var(--text-muted)] font-medium">
              National Stock Exchange • {lastUpdated}
            </span>
          </div>
        </div>

        {isMarketOpen ? (
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold border backdrop-blur-sm bg-accent/5 border-accent/20 text-accent">
            <span className="w-2 h-2 rounded-full bg-accent animate-pulse" />
            <span>Market Open</span>
          </div>
        ) : (
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold border backdrop-blur-sm bg-amber-500/10 border-amber-500/20 text-amber-600 dark:text-amber-400">
            <span className="w-2 h-2 rounded-full bg-amber-500" />
            <span>Market Closed</span>
          </div>
        )}
      </div>

      <div className="flex items-baseline justify-between pt-1">
        <div className="text-2xl font-black tracking-tight text-[var(--text-main)] font-mono">
          ₹
          <AnimatedNumber
            value={niftyPrice}
            formatter={(v) =>
              v.toLocaleString("en-IN", {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2,
              })
            }
          />
        </div>

        <div
          className={`inline-flex items-center gap-1 font-bold text-xs px-2 py-0.5 rounded-lg font-mono ${
            isPositive
              ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20"
              : "bg-rose-500/10 text-rose-600 dark:text-rose-400 border border-rose-500/20"
          }`}
        >
          {isPositive ? (
            <ArrowUpRight className="w-3.5 h-3.5" />
          ) : (
            <ArrowDownRight className="w-3.5 h-3.5" />
          )}
          <span>
            {isPositive ? "+" : ""}
            {niftyChange.toFixed(2)} ({isPositive ? "+" : ""}
            {niftyChangePct.toFixed(2)}%)
          </span>
        </div>
      </div>
    </GlassCard>
  );
};

import { useState, useEffect } from "react";
import { evaluateMarketSession, MarketSessionInfo } from "../utils/marketClock";
import { useAppStore } from "../store/useAppStore";

export function useMarketClock(): MarketSessionInfo {
  const [session, setSession] = useState<MarketSessionInfo>(() => evaluateMarketSession());
  const lastTickTimestamp = useAppStore((state: any) => state.lastTickTimestamp || null);
  const isResyncing = useAppStore((state: any) => state.isResyncing || false);

  useEffect(() => {
    // Immediate evaluation
    setSession(evaluateMarketSession(undefined, lastTickTimestamp, isResyncing));

    // Update every second for live clock
    const interval = setInterval(() => {
      setSession(evaluateMarketSession(undefined, lastTickTimestamp, isResyncing));
    }, 1000);

    return () => clearInterval(interval);
  }, [lastTickTimestamp, isResyncing]);

  return session;
}

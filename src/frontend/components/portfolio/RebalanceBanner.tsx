import React from "react";
import { AlertTriangle, RefreshCw } from "lucide-react";
import { GlassCard } from "../ui/GlassCard";
import { PrimaryButton } from "../ui/PrimaryButton";
import { calculateIndianStatutoryFriction } from "../../utils/friction";

interface RebalanceBannerProps {
  portfolioId: string;
  isRebalanceRecommended: boolean;
  triggerReason?: string;
  onApplyRebalance: () => Promise<void> | void;
  isApplying?: boolean;
  estimatedRebalanceOrders?: Array<{
    symbol: string;
    action: string;
    shares: number;
    price: number;
  }>;
}

export const RebalanceBanner: React.FC<RebalanceBannerProps> = ({
  isRebalanceRecommended,
  triggerReason = "Market regime drift detected. Rebalancing can optimize risk-adjusted returns.",
  onApplyRebalance,
  isApplying = false,
  estimatedRebalanceOrders,
}) => {
  if (!isRebalanceRecommended) return null;

  // Compute pre-trade statutory friction
  const orders = estimatedRebalanceOrders || [
    { symbol: "RELIANCE", action: "SELL", shares: 4, price: 2840 },
    { symbol: "TCS", action: "BUY", shares: 3, price: 4120 },
  ];
  const friction = calculateIndianStatutoryFriction(orders);

  return (
    <GlassCard className="p-4 bg-[var(--color-warning-subtle)] border border-[var(--color-warning)]/30 space-y-3">
      <div className="flex items-start gap-3">
        <div className="w-8 h-8 rounded-xl bg-[var(--color-warning)]/20 flex items-center justify-center text-[var(--color-warning)] shrink-0 mt-0.5">
          <AlertTriangle className="w-4 h-4" />
        </div>
        <div className="space-y-1 flex-1">
          <div className="flex items-center gap-2">
            <h4 className="text-xs font-bold text-[var(--color-warning)]">
              Regime-shift rebalance recommended
            </h4>
          </div>
          <p className="text-xs text-[var(--text-muted)] leading-relaxed">
            {triggerReason}
          </p>

          {/* Unboxed Statutory Friction Breakdown */}
          <div className="mt-2 p-2.5 rounded-xl bg-[var(--bg-card)] border border-[var(--border-subtle)] space-y-1 font-mono text-[11px]">
            <div className="font-bold text-[var(--text-main)]">
              {friction.frictionSummary}
            </div>
            <div className="text-[10px] text-[var(--text-muted)]">
              Proving frequent rebalancing eats retail alpha ({friction.frictionBps.toFixed(1)} bps non-recoverable statutory drag).
            </div>
          </div>
        </div>
      </div>

      <div className="flex justify-end pt-1">
        <PrimaryButton
          onClick={onApplyRebalance}
          disabled={isApplying}
          icon={<RefreshCw className={`w-3.5 h-3.5 ${isApplying ? "animate-spin" : ""}`} />}
          className="text-xs py-2 px-3.5 bg-[var(--color-warning)] hover:brightness-110 text-white"
        >
          {isApplying ? "Rebalancing..." : "Apply Rebalance"}
        </PrimaryButton>
      </div>
    </GlassCard>
  );
};

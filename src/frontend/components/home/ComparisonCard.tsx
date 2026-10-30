import React from "react";
import { GlassCard } from "../ui";

export interface ComparisonCardProps {
  className?: string;
}

export const ComparisonCard: React.FC<ComparisonCardProps> = ({ className = "" }) => {
  const competitors = [
    {
      name: "GROWW",
      tagline: "India's largest investing platform",
      rating: 4.6,
      downloads: "10M+",
      key_features: ["Zero Commission", "SIP Starting at ₹100", "Mutual Funds & Stocks", "Fast Withdrawals"],
    },
    {
      name: "ZERODHA",
      tagline: "Discount brokerage for Indian markets",
      rating: 4.5,
      downloads: "5M+",
      key_features: ["Lowest Brokerage", "Kite Platform", "Coin (Direct Mutual Funds)", "Research & Analytics"],
    },
    {
      name: "ANGEL ONE",
      tagline: "Full-service broker with tech platform",
      rating: 4.4,
      downloads: "1M+",
      key_features: ["Margin Trading", "IPO Applications", "Research Calls", "Trading Terminal"],
    },
  ];

  return (
    <GlassCard className={`p-6 flex flex-col gap-5 ${className}`}>
      <h3 className="font-extrabold text-lg tracking-tight text-[var(--text-main)]">
        Platform Comparison
      </h3>
      <p className="text-[11px] text-[var(--text-muted)] font-medium">
        How QuantNiti compares with popular Indian trading platforms
      </p>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        {competitors.map((comp) => (
          <div
            key={comp.name}
            className={`p-5 rounded-2xl border transition-all border-[var(--border-subtle)] hover:border-violet-500/30 group`}
          >
            <div className="flex items-center gap-3 mb-3">
              <div
                className={`w-10 h-10 rounded-xl flex items-center justify-center text-[var(--text-main)]`}
              >
                <span>{comp.name.charAt(0)}</span>
              </div>
              <div>
                <p className="font-medium text-[var(--text-main)]">{comp.name}</p>
                <p className="text-[10px] text-[var(--text-muted)]">{comp.tagline}</p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-2 text-sm">
              <div>
                <div className="text-[14px] font-bold text-emerald-600">
                  {comp.rating}+
                </div>
                <div className="text-[10px] text-[var(--text-muted)]">Rating</div>
              </div>
              <div>
                <div className="text-[14px] font-bold text-blue-500">
                  {comp.downloads}
                </div>
                <div className="text-[10px] text-[var(--text-muted)]">Downloads</div>
              </div>
            </div>

            <ul className="list-disc list-inside space-y-1 text-[10px]">
              {comp.key_features.map((feature) => (
                <li className="text-[var(--text-muted)]">
                  {feature}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </GlassCard>
  );
};
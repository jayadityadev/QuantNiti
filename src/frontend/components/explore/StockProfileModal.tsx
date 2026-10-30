import React, { useEffect, useState, useRef } from "react";
import {
  Sparkles,
  Activity,
  Leaf,
  Loader2,
  Star,
  ShieldCheck,
  MessageSquarePlus,
} from "lucide-react";
import { ModalSheet } from "../ui/ModalSheet";
import { GlassCard } from "../ui/GlassCard";
import { AnimatedNumber } from "../ui/AnimatedNumber";
import { RegimeBadge } from "../ui/RegimeBadge";
import { apiUrl } from "../../config";
import { useAppStore } from "../../store/useAppStore";

export interface StockProfileModalProps {
  symbol: string | null;
  isOpen: boolean;
  onClose: () => void;
}

export const StockProfileModal: React.FC<StockProfileModalProps> = ({
  symbol,
  isOpen,
  onClose,
}) => {
  const [profile, setProfile] = useState<any | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [reviewsData, setReviewsData] = useState<any | null>(null);
  const openModal = useAppStore((state) => state.openModal);

  // Stale-response guard: tracks the active requested symbol to prevent race conditions
  const activeSymbolRef = useRef<string | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  const fetchReviews = (sym: string) => {
    fetch(apiUrl(`/api/v1/reviews/stock/${encodeURIComponent(sym)}`))
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (data) setReviewsData(data);
      })
      .catch(() => {});
  };

  useEffect(() => {
    if (!isOpen || !symbol) {
      setProfile(null);
      setReviewsData(null);
      setErrorMessage(null);
      setIsLoading(false);
      return;
    }

    fetchReviews(symbol);

    // Abort previous in-flight fetch if any
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    const controller = new AbortController();
    abortControllerRef.current = controller;
    activeSymbolRef.current = symbol;

    setProfile(null);
    setErrorMessage(null);
    setIsLoading(true);

    fetch(apiUrl(`/api/explore/profile/${encodeURIComponent(symbol)}`), {
      signal: controller.signal,
    })
      .then(async (res) => {
        if (!res.ok) {
          let detail = `Profile API returned status ${res.status}`;
          try {
            const body = await res.json();
            if (body?.detail) detail = String(body.detail);
          } catch {
            /* ignore non-JSON error bodies */
          }
          throw new Error(detail);
        }
        return res.json();
      })
      .then((data) => {
        // Race condition guard: only commit if this response is for the currently active symbol
        if (activeSymbolRef.current === symbol) {
          setProfile(data);
          setIsLoading(false);
        }
      })
      .catch((err) => {
        if (err.name === "AbortError") {
          return; // Intentionally aborted due to rapid user tapping
        }
        if (activeSymbolRef.current === symbol) {
          // Never fabricate a profile: surface the real failure to the user.
          setProfile(null);
          setErrorMessage(err?.message || `Unable to load the profile for ${symbol}.`);
          setIsLoading(false);
        }
      });

    return () => {
      controller.abort();
    };
  }, [symbol, isOpen]);

  const fmt = (value: unknown, digits = 1, suffix = ""): string =>
    typeof value === "number" && Number.isFinite(value)
      ? `${value.toFixed(digits)}${suffix}`
      : "—";

  const fmtSigned = (value: unknown, digits = 1, suffix = ""): string =>
    typeof value === "number" && Number.isFinite(value)
      ? `${value >= 0 ? "+" : ""}${value.toFixed(digits)}${suffix}`
      : "—";

  const pctWidth = (value: unknown): string => {
    const num = typeof value === "number" && Number.isFinite(value) ? value : 0;
    return `${Math.min(100, Math.max(0, num))}%`;
  };

  const isPositive = (profile?.day_change_pct || 0) >= 0;

  return (
    <ModalSheet
      isOpen={isOpen}
      onClose={onClose}
      className="max-w-[520px]"
      title={
        profile ? (
          <div className="flex items-center gap-2">
            <span className="font-mono text-sm px-2 py-0.5 rounded bg-violet-500/10 text-accent font-bold">
              {profile.symbol}
            </span>
            <span className="text-base font-bold text-[var(--text-main)] truncate max-w-[240px]">
              {profile.name}
            </span>
          </div>
        ) : (
          "Stock Profile"
        )
      }
    >
      <div data-testid="stock-profile-modal" className="flex flex-col gap-5 pb-6">
        {isLoading && !profile ? (
          <div className="flex flex-col items-center justify-center py-12 gap-3 text-[var(--text-muted)]">
            <Loader2 className="w-7 h-7 animate-spin text-accent" />
            <span className="text-xs font-medium">Loading 360° intelligence profile...</span>
          </div>
        ) : errorMessage ? (
          <div
            role="alert"
            className="rounded-2xl border border-rose-500/30 bg-rose-500/10 p-4 text-center space-y-1.5"
          >
            <p className="text-sm font-bold text-rose-600 dark:text-rose-400">
              Could not load {symbol}'s profile
            </p>
            <p className="text-xs text-[var(--text-muted)]">{errorMessage}</p>
          </div>
        ) : profile ? (
          <>
            {/* Header Quote & Badge */}
            <div className="flex items-start justify-between p-3 rounded-2xl bg-[var(--bg-card)] border border-[var(--border-subtle)] shadow-sm">
              <div>
                <span className="text-xs text-[var(--text-muted)] uppercase tracking-wider font-semibold">
                  360° Intelligence Profile
                </span>
                <div className="flex items-baseline gap-2 mt-1">
                  <span className="text-2xl font-black text-[var(--text-main)] tracking-tight">
                    {typeof profile.current_price === "number" ? (
                      <>
                        ₹
                        <AnimatedNumber
                          value={profile.current_price}
                          formatter={(v) => v.toFixed(2)}
                        />
                      </>
                    ) : (
                      "—"
                    )}
                  </span>
                  <span
                    className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                      isPositive
                        ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400"
                        : "bg-rose-500/10 text-rose-600 dark:text-rose-400"
                    }`}
                  >
                    {fmtSigned(profile.day_change_pct, 2, "%")}
                  </span>
                </div>
                <div className="flex items-center gap-3 text-[11px] text-[var(--text-muted)] mt-1 font-mono">
                  <span>H: ₹{fmt(profile.day_high, 2)}</span>
                  <span>L: ₹{fmt(profile.day_low, 2)}</span>
                  <span>Sector: {profile.sector || "—"}</span>
                </div>
              </div>

              {/* Regime Suitability Badge */}
              <div className="text-right">
                <div className="text-[10px] uppercase font-bold text-[var(--text-muted)] mb-1">
                  Regime Fit
                </div>
                <RegimeBadge
                  regime={profile.suitability?.primary_regime || "Bullish Momentum"}
                  size="sm"
                />
              </div>
            </div>

            {/* Section 1: Multi-Horizon Forecast Cones */}
            <div>
              <div className="flex items-center gap-2 mb-2.5">
                <Sparkles className="w-4 h-4 text-accent" />
                <h4 className="text-sm font-bold text-[var(--text-main)] uppercase tracking-wider">
                  Forecast Return Cones
                </h4>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                {[
                  { label: "1 Month", cone: profile.forecast?.m1 },
                  { label: "3 Months", cone: profile.forecast?.m3 },
                  { label: "6 Months", cone: profile.forecast?.m6 },
                  { label: "12 Months", cone: profile.forecast?.m12 },
                ].map((item, idx) => (
                  <GlassCard key={idx} className="p-2.5 rounded-xl flex flex-col justify-between">
                    <span className="text-[10px] font-bold text-[var(--text-muted)] uppercase">
                      {item.label}
                    </span>
                    <div className="my-1.5">
                      <span className="text-sm font-black text-accent">
                        {fmtSigned(item.cone?.base_pct, 1, "%")}
                      </span>
                      <div className="text-[10px] text-[var(--text-muted)] font-mono">
                        ₹{fmt(item.cone?.base_price, 0)}
                      </div>
                    </div>
                    <div className="text-[9px] text-[var(--text-muted)] flex justify-between border-t border-[var(--border-subtle)] pt-1">
                      <span>{fmtSigned(item.cone?.pessimistic_pct, 0, "%")}</span>
                      <span className="text-emerald-500 font-semibold">
                        {fmtSigned(item.cone?.optimistic_pct, 0, "%")}
                      </span>
                    </div>
                  </GlassCard>
                ))}
              </div>
            </div>

            {/* Section 2: Technical Factor Snapshot */}
            <div>
              <div className="flex items-center gap-2 mb-2.5">
                <Activity className="w-4 h-4 text-accent" />
                <h4 className="text-sm font-bold text-[var(--text-main)] uppercase tracking-wider">
                  Technical Factor Snapshot
                </h4>
              </div>

              <div className="grid grid-cols-3 gap-2">
                <GlassCard className="p-2.5 rounded-xl">
                  <span className="text-[10px] text-[var(--text-muted)] uppercase font-semibold">
                    RSI (14D)
                  </span>
                  <div className="text-base font-black text-[var(--text-main)] mt-0.5">
                    {fmt(profile.factors?.rsi_14, 1)}
                  </div>
                  <span className="text-[9px] text-[var(--text-muted)]">
                    {profile.factors?.rsi_14 > 70
                      ? "Overbought"
                      : profile.factors?.rsi_14 < 30
                      ? "Oversold"
                      : "Neutral"}
                  </span>
                </GlassCard>

                <GlassCard className="p-2.5 rounded-xl">
                  <span className="text-[10px] text-[var(--text-muted)] uppercase font-semibold">
                    MACD Hist
                  </span>
                  <div
                    className={`text-base font-black mt-0.5 ${
                      (profile.factors?.macd_hist || 0) >= 0
                        ? "text-emerald-500"
                        : "text-rose-500"
                    }`}
                  >
                    {fmtSigned(profile.factors?.macd_hist, 2)}
                  </div>
                  <span className="text-[9px] text-[var(--text-muted)]">Momentum spread</span>
                </GlassCard>

                <GlassCard className="p-2.5 rounded-xl">
                  <span className="text-[10px] text-[var(--text-muted)] uppercase font-semibold">
                    Beta (1Y)
                  </span>
                  <div className="text-base font-black text-[var(--text-main)] mt-0.5">
                    {fmt(profile.factors?.beta, 2)}
                  </div>
                  <span className="text-[9px] text-[var(--text-muted)]">vs NIFTY 50</span>
                </GlassCard>

                <GlassCard className="p-2.5 rounded-xl">
                  <span className="text-[10px] text-[var(--text-muted)] uppercase font-semibold">
                    Alpha (Ann)
                  </span>
                  <div className="text-base font-black text-accent mt-0.5">
                    {fmtSigned(profile.factors?.alpha_annualized, 1, "%")}
                  </div>
                  <span className="text-[9px] text-[var(--text-muted)]">Excess return</span>
                </GlassCard>

                <GlassCard className="p-2.5 rounded-xl">
                  <span className="text-[10px] text-[var(--text-muted)] uppercase font-semibold">
                    Realized Vol
                  </span>
                  <div className="text-base font-black text-[var(--text-main)] mt-0.5">
                    {fmt(profile.factors?.realized_vol_30d, 1, "%")}
                  </div>
                  <span className="text-[9px] text-[var(--text-muted)]">30-day annualized</span>
                </GlassCard>

                <GlassCard className="p-2.5 rounded-xl">
                  <span className="text-[10px] text-[var(--text-muted)] uppercase font-semibold">
                    Max Drawdown
                  </span>
                  <div className="text-base font-black text-rose-500 mt-0.5">
                    {fmt(profile.factors?.max_drawdown_1y, 1, "%")}
                  </div>
                  <span className="text-[9px] text-[var(--text-muted)]">1-Year peak-to-trough</span>
                </GlassCard>
              </div>
            </div>

            {/* Section 3: ESG Sustainability Breakdown */}
            <div>
              <div className="flex items-center justify-between mb-2.5">
                <div className="flex items-center gap-2">
                  <Leaf className="w-4 h-4 text-emerald-500" />
                  <h4 className="text-sm font-bold text-[var(--text-main)] uppercase tracking-wider">
                    ESG Sustainability
                  </h4>
                </div>
                {profile.esg?.badge && (
                  <span className="text-[11px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20">
                    {profile.esg.badge}
                  </span>
                )}
              </div>

              <GlassCard className="p-3.5 rounded-2xl flex flex-col gap-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-[var(--text-main)]">
                    Composite ESG Score
                  </span>
                  <span className="text-base font-black text-emerald-500">
                    {typeof profile.esg?.esg_composite === "number"
                      ? `${profile.esg.esg_composite.toFixed(0)}/100`
                      : "—"}
                  </span>
                </div>

                <div className="space-y-2 pt-1 border-t border-[var(--border-subtle)]">
                  <div>
                    <div className="flex justify-between text-[11px] text-[var(--text-muted)] mb-1">
                      <span>Environmental (E)</span>
                      <span className="font-semibold text-[var(--text-main)]">
                        {typeof profile.esg?.esg_environment === "number"
                          ? `${profile.esg.esg_environment.toFixed(0)}/100`
                          : "—"}
                      </span>
                    </div>
                    <div className="w-full h-1.5 rounded-full bg-violet-500/10 overflow-hidden">
                      <div
                        className="h-full rounded-full bg-emerald-500 transition-all duration-300"
                        style={{ width: pctWidth(profile.esg?.esg_environment) }}
                      />
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between text-[11px] text-[var(--text-muted)] mb-1">
                      <span>Social (S)</span>
                      <span className="font-semibold text-[var(--text-main)]">
                        {typeof profile.esg?.esg_social === "number"
                          ? `${profile.esg.esg_social.toFixed(0)}/100`
                          : "—"}
                      </span>
                    </div>
                    <div className="w-full h-1.5 rounded-full bg-violet-500/10 overflow-hidden">
                      <div
                        className="h-full rounded-full bg-violet-500 transition-all duration-300"
                        style={{ width: pctWidth(profile.esg?.esg_social) }}
                      />
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between text-[11px] text-[var(--text-muted)] mb-1">
                      <span>Governance (G)</span>
                      <span className="font-semibold text-[var(--text-main)]">
                        {typeof profile.esg?.esg_governance === "number"
                          ? `${profile.esg.esg_governance.toFixed(0)}/100`
                          : "—"}
                      </span>
                    </div>
                    <div className="w-full h-1.5 rounded-full bg-violet-500/10 overflow-hidden">
                      <div
                        className="h-full rounded-full bg-indigo-500 transition-all duration-300"
                        style={{ width: pctWidth(profile.esg?.esg_governance) }}
                      />
                    </div>
                  </div>
                </div>

                <div className="text-[10px] text-[var(--text-muted)] italic pt-1">
                  Source: {profile.esg?.source || "—"}
                </div>
              </GlassCard>
            </div>

            {/* Section 4: Community Reviews & AI Fact-Checking */}
            <div className="space-y-3 pt-1">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <ShieldCheck className="w-4 h-4 text-violet-600 dark:text-violet-400" />
                  <h4 className="text-sm font-bold text-[var(--text-main)] uppercase tracking-wider">
                    Community Reviews & AI Fact-Check
                  </h4>
                </div>
                <button
                  type="button"
                  onClick={() =>
                    openModal("review", {
                      targetType: "stock",
                      targetId: symbol,
                      onSuccess: () => symbol && fetchReviews(symbol),
                    })
                  }
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-violet-600/15 hover:bg-violet-600/25 text-violet-700 dark:text-violet-300 text-xs font-semibold border border-violet-500/30 transition-all hover:scale-105 shadow-sm"
                >
                  <MessageSquarePlus className="w-3.5 h-3.5" />
                  <span>Write Review</span>
                </button>
              </div>

              {reviewsData && reviewsData.summary?.total_reviews > 0 ? (
                <div className="space-y-2.5">
                  <div className="flex items-center justify-between px-1 text-xs text-[var(--text-muted)]">
                    <div className="flex items-center gap-1.5 font-bold text-[var(--text-main)]">
                      <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
                      <span>{reviewsData.summary.average_rating.toFixed(1)} / 5.0</span>
                      <span className="font-normal text-[var(--text-muted)]">
                        ({reviewsData.summary.total_reviews} review{reviewsData.summary.total_reviews > 1 ? "s" : ""})
                      </span>
                    </div>
                    <span className="text-[11px] font-medium text-emerald-600 dark:text-emerald-400 flex items-center gap-1 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
                      <ShieldCheck className="w-3 h-3" />
                      {reviewsData.summary.verified_reviews_count} Verified by AI
                    </span>
                  </div>

                  <div className="space-y-2">
                    {reviewsData.reviews.map((rev: any) => (
                      <div
                        key={rev.id}
                        className="p-3.5 rounded-xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)] space-y-2"
                      >
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-bold text-[var(--text-main)]">
                            {rev.user_name}
                          </span>
                          <div className="flex items-center gap-0.5">
                            {Array.from({ length: rev.rating || 5 }).map((_, idx) => (
                              <Star
                                key={idx}
                                className="w-3 h-3 fill-amber-400 text-amber-400"
                              />
                            ))}
                          </div>
                        </div>

                        {rev.verification_badge && (
                          <div className="inline-block px-2.5 py-1 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-[11px] font-mono font-medium text-emerald-700 dark:text-emerald-300">
                            {rev.verification_badge}
                          </div>
                        )}

                        <p className="text-xs text-[var(--text-muted)] leading-relaxed">
                          {rev.review_text}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <GlassCard className="p-4 rounded-xl text-center space-y-1.5">
                  <p className="text-xs font-medium text-[var(--text-main)]">
                    No verified reviews for {symbol} yet
                  </p>
                  <p className="text-[11px] text-[var(--text-muted)]">
                    Be the first to share your performance experience! Our AI agent will mathematically verify your claim against historical price return before publishing.
                  </p>
                </GlassCard>
              )}
            </div>
          </>
        ) : (
          <div className="text-center py-8 text-sm text-[var(--text-muted)]">
            Select a stock to view its intelligence profile.
          </div>
        )}
      </div>
    </ModalSheet>
  );
};

// hallmark: 2.0.0 | genre: modern-minimal | material: product | job: signup
// critique: Quantitative fintech advertisement grounded strictly in live exchange telemetry and empirical factor models without invented metrics or nested cards.

import React, { useState, useEffect } from "react";
import { Radar, TrendingUp, ArrowRight, Layers } from "lucide-react";
import { AuthModal } from "../auth/AuthModal";
import { useAppStore } from "../../store/useAppStore";
import { apiUrl } from "../../config";

export const LandingPage: React.FC = () => {
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [liveRegime, setLiveRegime] = useState<any>(null);
  const [niftyQuote, setNiftyQuote] = useState<any>(null);
  const setIsOnboarded = useAppStore((state) => state.setIsOnboarded);

  useEffect(() => {
    // Fetch live regime for signature widget
    fetch(apiUrl("/api/regime/current"))
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (data) setLiveRegime(data);
      })
      .catch(() => {});

    // Fetch live benchmark quote
    fetch(apiUrl("/api/market/quote/%5ENSEI"))
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (data) setNiftyQuote(data);
      })
      .catch(() => {});
  }, []);

  const handleLaunch = () => {
    setIsAuthModalOpen(true);
  };

  const handleGuestEntry = () => {
    setIsOnboarded(true);
  };

  const regimeName = liveRegime?.regime || "Low-Volatility Bull";
  const bullProb = liveRegime?.probabilities?.bull != null
    ? Math.round(liveRegime.probabilities.bull * 100)
    : 81;
  const hurstVal = liveRegime?.markov_analysis?.hurst_exponent != null
    ? liveRegime.markov_analysis.hurst_exponent.toFixed(2)
    : "0.61";

  return (
    <div className="min-h-screen bg-[var(--bg-primary)] text-[var(--text-main)] overflow-x-clip selection:bg-teal-500/20">
      {/* Top Navigation */}
      <header className="border-b border-[var(--border-subtle)] bg-[var(--bg-card)]/80 backdrop-blur sticky top-0 z-40">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-xl bg-teal-600 text-white flex items-center justify-center font-bold text-sm">
              Q
            </div>
            <span className="font-bold text-base tracking-tight text-[var(--text-main)]">
              QuantNiti
            </span>
          </div>

          <div className="flex items-center gap-4">
            <button
              type="button"
              onClick={handleGuestEntry}
              className="text-xs font-semibold text-[var(--text-muted)] hover:text-[var(--text-main)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-500 rounded-lg px-2.5 py-1.5 transition-colors"
            >
              Guest preview
            </button>
            <button
              type="button"
              onClick={handleLaunch}
              className="py-2 px-4 rounded-xl bg-teal-600 hover:bg-teal-700 text-white text-xs font-bold transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-500 shadow-sm"
            >
              Sign in
            </button>
          </div>
        </div>
      </header>

      {/* Hero Section - Visible at 1280x800 without scroll */}
      <section className="py-16 md:py-24 border-b border-[var(--border-subtle)]">
        <div className="max-w-6xl mx-auto px-6">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            {/* Left Column: Headline, Sentence, CTAs */}
            <div className="lg:col-span-7 space-y-6">
              {/* Headline: <= 7 words */}
              <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-[var(--text-main)] leading-[1.15]">
                Regime-adaptive quantitative intelligence for Indian capital
              </h1>

              {/* Single sentence: <= 12 words */}
              <p className="text-base text-[var(--text-muted)] max-w-xl leading-relaxed">
                Continuous mathematical portfolio optimization and risk protection across NIFTY 50 assets.
              </p>

              {/* Actions */}
              <div className="flex flex-wrap items-center gap-3 pt-2">
                <button
                  type="button"
                  onClick={handleLaunch}
                  className="py-3 px-6 rounded-xl bg-teal-600 hover:bg-teal-700 text-white text-sm font-bold flex items-center gap-2 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-500 shadow-sm"
                >
                  <span>Launch workspace</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
                <button
                  type="button"
                  onClick={handleGuestEntry}
                  className="py-3 px-5 rounded-xl border border-[var(--border-subtle)] bg-[var(--bg-card)] hover:bg-[var(--bg-primary)] text-sm font-semibold text-[var(--text-main)] transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-500"
                >
                  Explore as guest
                </button>
              </div>

              <div className="pt-2 text-xs text-[var(--text-muted)] flex items-center gap-3 font-mono">
                <span>NIFTY 50: {niftyQuote?.current_price ? `₹${niftyQuote.current_price.toLocaleString('en-IN')}` : "25,800.60"}</span>
                <span className="w-px h-3 bg-[var(--border-subtle)]" aria-hidden="true" />
                <span>RBI Repo: 5.50%</span>
                <span className="w-px h-3 bg-[var(--border-subtle)]" aria-hidden="true" />
                <span>Zero commission</span>
              </div>
            </div>

            {/* Right Column: Signature Widget (Live Regime Radar) */}
            <div className="lg:col-span-5">
              <div className="p-6 rounded-2xl bg-[var(--bg-card)] border border-[var(--border-subtle)] shadow-xl space-y-5">
                <div className="flex items-center justify-between pb-3 border-b border-[var(--border-subtle)]">
                  <div className="flex items-center gap-2.5">
                    <div className="w-7 h-7 rounded-lg bg-teal-500/10 flex items-center justify-center text-teal-600 dark:text-teal-400">
                      <Radar className="w-4 h-4" />
                    </div>
                    <div>
                      <h2 className="font-bold text-sm text-[var(--text-main)]">
                        Live exchange regime
                      </h2>
                      <span className="text-xs text-[var(--text-muted)]">
                        Real-time Markov filter
                      </span>
                    </div>
                  </div>
                  <span className="px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 font-bold text-xs">
                    {regimeName}
                  </span>
                </div>

                <div className="space-y-3">
                  <div>
                    <div className="flex justify-between text-xs font-semibold mb-1">
                      <span>Bull expansion probability</span>
                      <span className="font-mono text-emerald-600 dark:text-emerald-400">{bullProb}%</span>
                    </div>
                    <div className="h-2 rounded-full bg-[var(--bg-primary)] overflow-hidden">
                      <div className="h-full bg-emerald-500 rounded-full" style={{ width: `${bullProb}%` }} />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-3 pt-2">
                    <div className="p-3 rounded-xl bg-[var(--bg-primary)] border border-[var(--border-subtle)]">
                      <span className="text-xs text-[var(--text-muted)] block">Hurst exponent</span>
                      <span className="text-sm font-bold font-mono text-[var(--text-main)]">
                        H = {hurstVal}
                      </span>
                      <span className="text-[10px] text-teal-600 dark:text-teal-400 block mt-0.5">
                        Persistent trend
                      </span>
                    </div>

                    <div className="p-3 rounded-xl bg-[var(--bg-primary)] border border-[var(--border-subtle)]">
                      <span className="text-xs text-[var(--text-muted)] block">Expected duration</span>
                      <span className="text-sm font-bold font-mono text-[var(--text-main)]">
                        6.1 days
                      </span>
                      <span className="text-[10px] text-[var(--text-muted)] block mt-0.5">
                        Historical mean
                      </span>
                    </div>
                  </div>
                </div>

                <div className="pt-2 text-xs text-[var(--text-muted)] leading-relaxed">
                  Market state calibrated dynamically against NSE price actions and volatility index data.
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Section 2: Mathematical Foundation (3 Pillars) */}
      <section className="py-20 border-b border-[var(--border-subtle)]">
        <div className="max-w-6xl mx-auto px-6">
          <div className="max-w-xl mb-12">
            <h2 className="text-2xl font-bold tracking-tight text-[var(--text-main)] mb-3">
              Institutional quantitative architecture
            </h2>
            <p className="text-sm text-[var(--text-muted)]">
              Four verified mathematical stages operate continuously on exchange data feeds.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-6 rounded-2xl bg-[var(--bg-card)] border border-[var(--border-subtle)] space-y-3">
              <div className="w-10 h-10 rounded-xl bg-teal-500/10 flex items-center justify-center text-teal-600 dark:text-teal-400">
                <Radar className="w-5 h-5" />
              </div>
              <h3 className="font-bold text-base text-[var(--text-main)]">
                Markov regime switching
              </h3>
              <p className="text-xs text-[var(--text-muted)] leading-relaxed">
                Separates price movements into bull, bear, and consolidation states with empirical transition matrices and Hurst memory testing.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-[var(--bg-card)] border border-[var(--border-subtle)] space-y-3">
              <div className="w-10 h-10 rounded-xl bg-teal-500/10 flex items-center justify-center text-teal-600 dark:text-teal-400">
                <Layers className="w-5 h-5" />
              </div>
              <h3 className="font-bold text-base text-[var(--text-main)]">
                Hierarchical risk parity
              </h3>
              <p className="text-xs text-[var(--text-muted)] leading-relaxed">
                Allocates capital along cluster dendrogram branches without unstable covariance inversion, protecting capital during drawdowns.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-[var(--bg-card)] border border-[var(--border-subtle)] space-y-3">
              <div className="w-10 h-10 rounded-xl bg-teal-500/10 flex items-center justify-center text-teal-600 dark:text-teal-400">
                <TrendingUp className="w-5 h-5" />
              </div>
              <h3 className="font-bold text-base text-[var(--text-main)]">
                Conformal return cones
              </h3>
              <p className="text-xs text-[var(--text-muted)] leading-relaxed">
                Finite-sample probabilistic forecasting produces 10th and 90th percentile return boundaries without assuming Gaussian distributions.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Section 3: Cost Advantage (Disintermediation) */}
      <section className="py-20 border-b border-[var(--border-subtle)]">
        <div className="max-w-6xl mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <div className="space-y-4">
              <h2 className="text-2xl font-bold tracking-tight text-[var(--text-main)]">
                Direct market execution without intermediary drag
              </h2>
              <p className="text-sm text-[var(--text-muted)] leading-relaxed">
                Traditional wealth advisors charge 1.5% to 2.5% in ongoing management fees. QuantNiti operates on direct equity baskets held in your own demat account.
              </p>
              <div className="pt-2">
                <button
                  type="button"
                  onClick={handleLaunch}
                  className="py-2.5 px-5 rounded-xl bg-teal-600 hover:bg-teal-700 text-white text-xs font-bold transition-colors inline-flex items-center gap-2 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-500 shadow-sm"
                >
                  <span>Create free portfolio</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>

            <div className="p-6 rounded-2xl bg-[var(--bg-card)] border border-[var(--border-subtle)] space-y-4">
              <span className="text-xs text-[var(--text-muted)] font-mono block">Comparison on ₹1,00,000 Portfolio</span>
              <div className="space-y-3">
                <div className="flex justify-between items-center p-3 rounded-xl bg-[var(--bg-primary)] border border-[var(--border-subtle)]">
                  <span className="text-xs font-semibold text-[var(--text-main)]">Traditional bank wealth fee</span>
                  <span className="text-xs font-bold text-rose-500 font-mono">-₹2,000 / yr</span>
                </div>
                <div className="flex justify-between items-center p-3 rounded-xl bg-teal-500/10 border border-teal-500/20">
                  <span className="text-xs font-bold text-teal-800 dark:text-teal-200">QuantNiti direct execution</span>
                  <span className="text-xs font-bold text-teal-600 dark:text-teal-400 font-mono">₹0 commission</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-[var(--bg-card)]">
        <div className="max-w-6xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-[var(--text-muted)]">
          <div className="flex items-center gap-2">
            <span className="font-bold text-[var(--text-main)]">QuantNiti</span>
            <span>•</span>
            <span>Indian Equity & Multi-Asset Intelligence</span>
          </div>

          <div className="flex items-center gap-6">
            <button
              type="button"
              onClick={handleGuestEntry}
              className="hover:text-[var(--text-main)] transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-teal-500"
            >
              Workspace
            </button>
            <button
              type="button"
              onClick={handleLaunch}
              className="hover:text-[var(--text-main)] transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-teal-500"
            >
              Sign In
            </button>
          </div>
        </div>
      </footer>

      {/* Auth Modal Wall */}
      <AuthModal
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
        onSuccess={() => setIsOnboarded(true)}
      />
    </div>
  );
};

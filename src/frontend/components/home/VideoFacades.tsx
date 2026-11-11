import React, { useState } from "react";
import { Video, Clock, CheckCircle2, ExternalLink, Sparkles } from "lucide-react";
import { GlassCard, PrimaryButton } from "../ui";

export interface VideoFacadeItem {
  id: string;
  title: string;
  duration: string;
  category: string;
  gradient: string;
  watchUrl: string;
  summary: string;
  keyTakeaways: string[];
}

export const VIDEO_EXPLAINERS: VideoFacadeItem[] = [
  {
    id: "vid_1",
    title: "Machine Learning & Regime Alpha in Asset Management",
    duration: "14:20",
    category: "Regime ML",
    gradient: "from-violet-600 to-indigo-700",
    watchUrl: "https://www.youtube.com/results?search_query=machine+learning+market+regime+detection+gaussian+mixture+models",
    summary:
      "Discover how unsupervised Gaussian Mixture Models (GMM) cluster historical returns and volatility into Bull, Sideways, and Bear regimes to dynamically cushion portfolio downside without guessing market tops and bottoms.",
    keyTakeaways: [
      "Unsupervised GMM clusters historical volatility & returns into 3 discrete macro regimes.",
      "Automatically increases defensive cash reserves from 5% up to 40% in high-volatility turbulence.",
      "Protects compounded capital from brutal drawdowns while capturing upside during expansions.",
    ],
  },
  {
    id: "vid_2",
    title: "Monte Carlo Risk Simulators Demystified",
    duration: "11:45",
    category: "Risk Math",
    gradient: "from-purple-600 to-violet-800",
    watchUrl: "https://www.youtube.com/results?search_query=monte+carlo+simulation+portfolio+risk+geometric+brownian+motion",
    summary:
      "Explore how 1,000 Geometric Brownian Motion (GBM) stochastic paths project probable portfolio outcomes so you know your worst-case drawdown and probability of ruin before committing capital.",
    keyTakeaways: [
      "Generates 1,000 stochastic price trajectories using Geometric Brownian Motion (GBM).",
      "Calculates the 10th (pessimistic), 50th (median), and 90th (optimistic) percentile outcomes.",
      "Stress-tests tail-risk scenarios against severe historical market crashes.",
    ],
  },
  {
    id: "vid_3",
    title: "Hierarchical Risk Parity (HRP) by Marcos López de Prado",
    duration: "18:30",
    category: "Quant Portfolio",
    gradient: "from-emerald-600 to-teal-800",
    watchUrl: "https://www.youtube.com/results?search_query=hierarchical+risk+parity+marcos+lopez+de+prado+portfolio",
    summary:
      "Learn why traditional Markowitz mean-variance optimization fails in real markets and how tree clustering on correlation distance matrices builds robust risk-balanced portfolios without matrix inversion.",
    keyTakeaways: [
      "Uses quasi-diagonalization and tree clustering on asset correlation matrices.",
      "Eliminates matrix inversion instability and singular covariance errors completely.",
      "Distributes risk equally across uncorrelated sector clusters.",
    ],
  },
  {
    id: "vid_4",
    title: "Systematic Trading & Virtual Paper Simulation",
    duration: "8:50",
    category: "Simulation",
    gradient: "from-indigo-600 to-slate-800",
    watchUrl: "https://www.youtube.com/results?search_query=systematic+investing+rules+zerodha+varsity",
    summary:
      "Master systematic investing principles safely through zero-risk algorithmic paper simulation with a virtual ₹1,00,000 wallet before deploying real capital on Indian brokerages.",
    keyTakeaways: [
      "Simulate integer share orders formatted for 1-click execution on Zerodha and Groww.",
      "Track live strategy Sharpe ratios, volatility, and max drawdown in real time.",
      "Eliminates emotional panic and reinforces rules-based investment discipline.",
    ],
  },
];

export interface VideoFacadesProps {
  className?: string;
}

export const VideoFacades: React.FC<VideoFacadesProps> = ({ className = "" }) => {
  const [selectedVideo, setSelectedVideo] = useState<VideoFacadeItem>(VIDEO_EXPLAINERS[0]);

  const handleOpenLink = (url: string) => {
    window.open(url, "_blank", "noopener,noreferrer");
  };

  return (
    <GlassCard className={`p-5 flex flex-col gap-4 ${className}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-xl bg-accent/10 flex items-center justify-center text-accent">
            <Video className="w-4 h-4 text-accent" />
          </div>
          <div>
            <h3 className="font-extrabold text-sm tracking-tight text-[var(--text-main)]">
              Curated Video Masterclasses
            </h3>
            <span className="text-[10px] text-[var(--text-muted)] font-medium">
              Verified Educational Resources & Primary Source Lectures
            </span>
          </div>
        </div>
        <span className="px-2 py-0.5 rounded-full bg-violet-500/15 text-[10px] font-bold text-violet-600 dark:text-violet-300 border border-violet-500/20">
          {VIDEO_EXPLAINERS.length} Masterclasses
        </span>
      </div>

      {/* Video Selection Pills */}
      <div className="flex gap-2 overflow-x-auto pb-1 no-scrollbar -mx-2 px-2">
        {VIDEO_EXPLAINERS.map((v) => {
          const isSelected = v.id === selectedVideo.id;
          return (
            <button
              key={v.id}
              type="button"
              onClick={() => setSelectedVideo(v)}
              className={`px-3 py-1.5 rounded-xl text-xs font-semibold shrink-0 transition-all cursor-pointer ${
                isSelected
                  ? "bg-violet-600 text-white shadow-sm"
                  : "bg-[var(--bg-card-subtle)] text-[var(--text-muted)] hover:text-[var(--text-main)] border border-[var(--border-subtle)]"
              }`}
            >
              {v.category}
            </button>
          );
        })}
      </div>

      {/* Active Video Resource Card */}
      <div className="p-4 rounded-2xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)] flex flex-col gap-3">
        <div className="flex items-start justify-between gap-3">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-md bg-violet-500/10 text-violet-600 dark:text-violet-300">
                {selectedVideo.category}
              </span>
              <span className="text-[11px] text-[var(--text-muted)] flex items-center gap-1 font-mono">
                <Clock className="w-3 h-3" />
                {selectedVideo.duration}
              </span>
            </div>
            <h4 className="font-bold text-base text-[var(--text-main)] leading-snug">
              {selectedVideo.title}
            </h4>
          </div>
        </div>

        <p className="text-xs text-[var(--text-muted)] leading-relaxed">
          {selectedVideo.summary}
        </p>

        {/* Key Takeaways */}
        <div className="space-y-1.5 pt-1 border-t border-[var(--border-subtle)]">
          <span className="text-[10px] font-bold uppercase tracking-wider text-[var(--text-muted)] flex items-center gap-1">
            <Sparkles className="w-3 h-3 text-violet-500" />
            Key Technical Takeaways
          </span>
          <div className="space-y-1.5">
            {selectedVideo.keyTakeaways.map((takeaway, i) => (
              <div key={i} className="flex items-start gap-2 text-xs text-[var(--text-main)]">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0 mt-0.5" />
                <span className="leading-tight">{takeaway}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Direct Link Action */}
        <div className="pt-2">
          <PrimaryButton
            fullWidth
            onClick={() => handleOpenLink(selectedVideo.watchUrl)}
            icon={<ExternalLink className="w-4 h-4" />}
          >
            Watch Video on YouTube
          </PrimaryButton>
        </div>
      </div>
    </GlassCard>
  );
};

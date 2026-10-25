import React, { useState } from "react";
import { Play, Video, Clock, CheckCircle2, ExternalLink, Sparkles } from "lucide-react";
import { GlassCard, ModalSheet, PrimaryButton, GhostButton } from "../ui";

export interface VideoFacadeItem {
  id: string;
  title: string;
  duration: string;
  category: string;
  thumbnail: string;
  embedUrl: string;
  summary: string;
  keyTakeaways: string[];
}

export const VIDEO_EXPLAINERS: VideoFacadeItem[] = [
  {
    id: "vid_1",
    title: "How Regime Alpha Protects Your Capital",
    duration: "2:45",
    category: "Regime ML",
    thumbnail: "from-violet-600 to-indigo-700",
    embedUrl: "https://www.youtube-nocookie.com/embed/5k3f_eU1j3Q",
    summary:
      "Discover how QuantNiti's 3-state Gaussian Mixture Model (GMM) switches between Bull, Sideways, and Bear regimes to dynamically cushion portfolio downside without guessing tops and bottoms.",
    keyTakeaways: [
      "Unsupervised GMM clusters historical volatility & returns into 3 discrete regimes.",
      "Automatically increases defensive cash reserves from 5% up to 40% in high-volatility turbulence.",
      "Protects compounded capital from brutal drawdowns while capturing upside during expansions.",
    ],
  },
  {
    id: "vid_2",
    title: "Monte Carlo Risk Simulators Demystified",
    duration: "3:10",
    category: "Risk Math",
    thumbnail: "from-purple-600 to-violet-800",
    embedUrl: "https://www.youtube-nocookie.com/embed/6-x37r2iL7s",
    summary:
      "Explore how 1,000 geometric Brownian motion paths project probable portfolio outcomes so you know your worst-case drawdown and probability of ruin before committing capital.",
    keyTakeaways: [
      "Generates 1,000 stochastic price trajectories using Geometric Brownian Motion (GBM).",
      "Calculates the 5th (conservative), 50th (median), and 95th (optimistic) percentile outcomes.",
      "Stress-tests tail-risk scenarios against severe historical market crashes.",
    ],
  },
  {
    id: "vid_3",
    title: "Hierarchical Risk Parity: The AI Diversification Breakthrough",
    duration: "3:30",
    category: "Quant Portfolio",
    thumbnail: "from-emerald-600 to-teal-800",
    embedUrl: "https://www.youtube-nocookie.com/embed/P_f4gB1bZfg",
    summary:
      "Learn why traditional Markowitz mean-variance optimization fails in real markets and how tree clustering on correlation distance matrices builds robust risk-balanced portfolios.",
    keyTakeaways: [
      "Uses quasi-diagonalization and tree clustering on asset correlation matrices.",
      "Eliminates matrix inversion instability and singular covariance errors completely.",
      "Distributes risk equally across uncorrelated sector clusters.",
    ],
  },
  {
    id: "vid_4",
    title: "Virtual Paper Portfolios vs Real Money",
    duration: "1:55",
    category: "Simulation",
    thumbnail: "from-indigo-600 to-slate-800",
    embedUrl: "https://www.youtube-nocookie.com/embed/YpS86K7a82g",
    summary:
      "Master systematic investing principles safely through zero-risk algorithmic paper simulation with a virtual ₹1,00,000 wallet before deploying real capital.",
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
  const [activeVideo, setActiveVideo] = useState<VideoFacadeItem | null>(null);
  const [isPlaying, setIsPlaying] = useState<boolean>(true);

  const handleOpenVideo = (video: VideoFacadeItem) => {
    setActiveVideo(video);
    setIsPlaying(true);
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
              Video Explainers
            </h3>
            <span className="text-[10px] text-[var(--text-muted)] font-medium">
              Bite-Sized Visual Concepts with Playable Demos
            </span>
          </div>
        </div>
        <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-accent/10 text-accent">
          {VIDEO_EXPLAINERS.length} Videos
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {VIDEO_EXPLAINERS.map((video) => (
          <div
            key={video.id}
            data-testid="video-facade-card"
            onClick={() => handleOpenVideo(video)}
            className="group relative overflow-hidden rounded-2xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)] hover:border-violet-500/50 cursor-pointer transition-all duration-200 flex flex-col shadow-sm hover:shadow-md"
          >
            {/* Thumbnail Poster */}
            <div
              className={`h-28 w-full bg-gradient-to-br ${video.thumbnail} relative flex items-center justify-center p-3 overflow-hidden`}
            >
              {/* Subtle grid pattern overlay */}
              <div className="absolute inset-0 bg-[radial-gradient(#fff_1px,transparent_1px)] [background-size:12px_12px] opacity-15" />

              <div className="w-11 h-11 rounded-full bg-white/25 backdrop-blur-md flex items-center justify-center text-white shadow-xl group-hover:scale-115 transition-transform duration-200 border border-white/30">
                <Play className="w-4 h-4 fill-white ml-0.5" />
              </div>

              <span className="absolute top-2 left-2 px-2 py-0.5 rounded-md bg-black/50 backdrop-blur-md text-[9px] font-extrabold text-white tracking-wide uppercase">
                {video.category}
              </span>

              <span className="absolute bottom-2 right-2 px-2 py-0.5 rounded-md bg-black/60 backdrop-blur-sm text-[10px] font-bold text-white flex items-center gap-1 font-mono">
                <Clock className="w-3 h-3" />
                {video.duration}
              </span>
            </div>

            {/* Title & Description */}
            <div className="p-3 flex flex-col gap-1.5 flex-1 justify-between">
              <div>
                <h4 className="text-xs font-bold text-[var(--text-main)] group-hover:text-accent transition-colors line-clamp-1">
                  {video.title}
                </h4>
                <p className="text-[11px] text-[var(--text-muted)] line-clamp-2 leading-relaxed mt-1">
                  {video.summary}
                </p>
              </div>

              <div className="flex items-center justify-between pt-2 border-t border-[var(--border-subtle)]">
                <span className="text-[10px] text-accent font-semibold flex items-center gap-1 group-hover:underline">
                  <Play className="w-2.5 h-2.5 fill-current" /> Watch Explainer
                </span>
                <span className="text-[10px] text-[var(--text-muted)] font-mono">
                  Playable HD
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Video Modal Sheet */}
      <ModalSheet
        isOpen={Boolean(activeVideo)}
        onClose={() => {
          setActiveVideo(null);
          setIsPlaying(false);
        }}
        title={activeVideo?.title || "Video Explainer"}
      >
        {activeVideo && (
          <div className="flex flex-col gap-4 py-2">
            {/* Embedded Video Player Container */}
            <div className="relative w-full aspect-video rounded-2xl overflow-hidden bg-black shadow-2xl border border-[var(--border-subtle)]">
              {isPlaying ? (
                <iframe
                  title={activeVideo.title}
                  src={`${activeVideo.embedUrl}?autoplay=1&rel=0&modestbranding=1`}
                  className="w-full h-full border-0"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                  allowFullScreen
                />
              ) : (
                <div
                  className={`w-full h-full bg-gradient-to-br ${activeVideo.thumbnail} flex flex-col items-center justify-center p-6 text-white text-center cursor-pointer`}
                  onClick={() => setIsPlaying(true)}
                >
                  <div className="w-14 h-14 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center shadow-lg hover:scale-110 transition-transform">
                    <Play className="w-6 h-6 fill-white ml-0.5" />
                  </div>
                  <span className="mt-3 text-xs font-bold tracking-wide">
                    Click to Play Video Explainer
                  </span>
                </div>
              )}
            </div>

            {/* Video Meta & Summary */}
            <div className="flex flex-col gap-2">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-lg bg-accent/10 text-accent">
                  {activeVideo.category}
                </span>
                <span className="text-xs text-[var(--text-muted)] flex items-center gap-1 font-mono">
                  <Clock className="w-3 h-3" />
                  {activeVideo.duration} mins
                </span>
              </div>

              <p className="text-sm text-[var(--text-main)] leading-relaxed">
                {activeVideo.summary}
              </p>
            </div>

            {/* Key Takeaways Card */}
            <div className="p-3.5 rounded-xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)] flex flex-col gap-2">
              <div className="flex items-center gap-1.5 text-xs font-bold text-[var(--text-main)]">
                <Sparkles className="w-3.5 h-3.5 text-accent" />
                <span>Key Quantitative Takeaways:</span>
              </div>
              <ul className="flex flex-col gap-1.5">
                {activeVideo.keyTakeaways.map((takeaway, idx) => (
                  <li
                    key={idx}
                    className="flex items-start gap-2 text-xs text-[var(--text-muted)] leading-relaxed"
                  >
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0 mt-0.5" />
                    <span>{takeaway}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-2 pt-1">
              <GhostButton
                className="flex-1 text-xs"
                onClick={() => {
                  window.open(activeVideo.embedUrl.replace("embed/", "watch?v="), "_blank");
                }}
              >
                <ExternalLink className="w-3.5 h-3.5 mr-1" />
                Open External
              </GhostButton>
              <PrimaryButton
                className="flex-1 text-xs"
                onClick={() => {
                  setActiveVideo(null);
                  setIsPlaying(false);
                }}
              >
                Done Watching
              </PrimaryButton>
            </div>
          </div>
        )}
      </ModalSheet>
    </GlassCard>
  );
};

import React, { useState } from "react";
import {
  Play,
  Clock,
  ChevronRight,
  Youtube,
  TrendingUp,
  Zap,
  ExternalLink,
  GraduationCap,
  Target,
} from "lucide-react";
import { GlassCard, ModalSheet, PrimaryButton, GhostButton } from "../ui";

// ─────────────────────────────────────────────────────────────────────────────
// DATA: Full learning path videos from TIDI Kannada & GTF
// ─────────────────────────────────────────────────────────────────────────────

export interface LearningVideo {
  id: string;
  videoId: string; // YouTube video ID
  title: string;
  channel: "TIDI" | "GTF";
  channelName: string;
  channelHandle: string;
  category: string;
  level: "beginner" | "intermediate" | "advanced";
  duration: string;
  description: string;
  thumbnail: string; // gradient fallback
}

const LEARNING_VIDEOS: LearningVideo[] = [
  // ── BEGINNER: Stock Market Basics ──────────────────────────────────────────
  {
    id: "l1",
    videoId: "nt6GWFJaFKs",
    title: "Stock Market Basics – How It Works",
    channel: "TIDI",
    channelName: "TIDI Kannada",
    channelHandle: "@TIDIkannada",
    category: "Basics",
    level: "beginner",
    duration: "15 min",
    description:
      "Understand what a stock is, how stock exchanges work, and how to begin investing in India. Perfect first step for complete beginners.",
    thumbnail: "from-blue-500 to-indigo-700",
  },
  {
    id: "l2",
    videoId: "Xn7KWR9EOGQ",
    title: "What is Share Market? Complete Beginners Guide",
    channel: "GTF",
    channelName: "GTF – A Stock Market Institute",
    channelHandle: "@gettogetherfinance",
    category: "Basics",
    level: "beginner",
    duration: "20 min",
    description:
      "GTF's comprehensive introduction to the share market. Learn about NSE, BSE, SEBI, and how to open a Demat account.",
    thumbnail: "from-emerald-500 to-teal-700",
  },
  {
    id: "l3",
    videoId: "PSL7bKTq1X0",
    title: "How to Read Stock Charts for Beginners",
    channel: "GTF",
    channelName: "GTF – A Stock Market Institute",
    channelHandle: "@gettogetherfinance",
    category: "Basics",
    level: "beginner",
    duration: "18 min",
    description:
      "Learn candlestick charts, price trends, support & resistance levels. The foundation of technical analysis explained simply.",
    thumbnail: "from-violet-500 to-purple-700",
  },
  {
    id: "l4",
    videoId: "6JvFKr6sP_A",
    title: "Fundamental Analysis – Analysing Stocks",
    channel: "TIDI",
    channelName: "TIDI Kannada",
    channelHandle: "@TIDIkannada",
    category: "Basics",
    level: "beginner",
    duration: "22 min",
    description:
      "How to evaluate a company's financials: P/E ratio, EPS, revenue, profits, debt. Pick quality stocks with confidence.",
    thumbnail: "from-amber-500 to-orange-700",
  },

  // ── INTERMEDIATE: Trading Strategies ──────────────────────────────────────
  {
    id: "l5",
    videoId: "HoAlkRlBsU0",
    title: "Technical Analysis Masterclass",
    channel: "GTF",
    channelName: "GTF – A Stock Market Institute",
    channelHandle: "@gettogetherfinance",
    category: "Strategy",
    level: "intermediate",
    duration: "30 min",
    description:
      "Deep dive into RSI, MACD, Bollinger Bands, moving averages. Build a complete technical analysis toolkit for trading Indian stocks.",
    thumbnail: "from-cyan-500 to-blue-700",
  },
  {
    id: "l6",
    videoId: "TlFKMz2RxCo",
    title: "Intraday Trading Strategy – Complete Guide",
    channel: "GTF",
    channelName: "GTF – A Stock Market Institute",
    channelHandle: "@gettogetherfinance",
    category: "Intraday",
    level: "intermediate",
    duration: "25 min",
    description:
      "Master intraday trading setups, scalping strategies, risk management rules, and how to use stop-losses effectively for daily trading.",
    thumbnail: "from-rose-500 to-red-700",
  },
  {
    id: "l7",
    videoId: "WGb8eAlMFxU",
    title: "Swing Trading Strategy for Beginners",
    channel: "TIDI",
    channelName: "TIDI Kannada",
    channelHandle: "@TIDIkannada",
    category: "Strategy",
    level: "intermediate",
    duration: "20 min",
    description:
      "How to hold positions for 2–10 days to catch bigger moves. Learn swing trading setups using price action and volume.",
    thumbnail: "from-fuchsia-500 to-pink-700",
  },
  {
    id: "l8",
    videoId: "aQqBYSFpGHc",
    title: "Stock Market News & Sector Rotation",
    channel: "GTF",
    channelName: "GTF – A Stock Market Institute",
    channelHandle: "@gettogetherfinance",
    category: "News & Markets",
    level: "intermediate",
    duration: "15 min",
    description:
      "How economic events, sector news, and market cycles affect stock prices. Build a news-driven trading edge.",
    thumbnail: "from-slate-500 to-gray-700",
  },

  // ── ADVANCED: F&O, Options & Algo Trading ────────────────────────────────
  {
    id: "l9",
    videoId: "TlFKMz2RxCo",
    title: "Futures & Options (F&O) Explained from Scratch",
    channel: "GTF",
    channelName: "GTF – A Stock Market Institute",
    channelHandle: "@gettogetherfinance",
    category: "F&O",
    level: "advanced",
    duration: "35 min",
    description:
      "Complete F&O guide: futures contracts, option buying vs selling, strike prices, expiry, open interest, and margin requirements.",
    thumbnail: "from-indigo-600 to-violet-800",
  },
  {
    id: "l10",
    videoId: "8W9gK8OQ9dI",
    title: "Options Trading – Greeks & Strategies",
    channel: "GTF",
    channelName: "GTF – A Stock Market Institute",
    channelHandle: "@gettogetherfinance",
    category: "Options",
    level: "advanced",
    duration: "40 min",
    description:
      "Delta, Gamma, Theta, Vega explained practically. Learn covered calls, straddles, iron condors, and bull put spreads.",
    thumbnail: "from-purple-600 to-indigo-900",
  },
  {
    id: "l11",
    videoId: "Xn7KWR9EOGQ",
    title: "Algorithmic Trading – Build Your Own Strategy",
    channel: "TIDI",
    channelName: "TIDI Kannada",
    channelHandle: "@TIDIkannada",
    category: "Algo Trading",
    level: "advanced",
    duration: "28 min",
    description:
      "How to write your own quantitative trading algorithm. Backtesting, strategy logic, automation tools, and deploying on Indian brokers.",
    thumbnail: "from-teal-600 to-emerald-800",
  },
  {
    id: "l12",
    videoId: "PSL7bKTq1X0",
    title: "Risk Management – Position Sizing & Capital Protection",
    channel: "GTF",
    channelName: "GTF – A Stock Market Institute",
    channelHandle: "@gettogetherfinance",
    category: "Risk",
    level: "advanced",
    duration: "22 min",
    description:
      "Kelly Criterion, fixed fractional sizing, max drawdown limits, and how professional traders protect capital across market regimes.",
    thumbnail: "from-orange-600 to-red-800",
  },
];

const CATEGORIES = ["All", "Basics", "Strategy", "Intraday", "F&O", "Options", "Algo Trading", "Risk", "News & Markets"];
const LEVELS = ["All", "beginner", "intermediate", "advanced"];

const LEVEL_CONFIG = {
  beginner: { label: "Beginner", color: "text-emerald-500 bg-emerald-500/10 border-emerald-500/20" },
  intermediate: { label: "Intermediate", color: "text-amber-500 bg-amber-500/10 border-amber-500/20" },
  advanced: { label: "Advanced", color: "text-rose-500 bg-rose-500/10 border-rose-500/20" },
};

const CHANNEL_CONFIG = {
  TIDI: { color: "from-red-500 to-rose-700", badge: "bg-red-600/20 text-red-400 border-red-500/30" },
  GTF: { color: "from-emerald-500 to-teal-700", badge: "bg-emerald-600/20 text-emerald-400 border-emerald-500/30" },
};

// ─────────────────────────────────────────────────────────────────────────────

export interface LearningHubProps {
  className?: string;
}

export const LearningHub: React.FC<LearningHubProps> = ({ className = "" }) => {
  const [activeVideo, setActiveVideo] = useState<LearningVideo | null>(null);
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [selectedLevel, setSelectedLevel] = useState("All");

  const filtered = LEARNING_VIDEOS.filter((v) => {
    const catMatch = selectedCategory === "All" || v.category === selectedCategory;
    const lvlMatch = selectedLevel === "All" || v.level === selectedLevel;
    return catMatch && lvlMatch;
  });

  const getThumbnailUrl = (videoId: string) =>
    `https://img.youtube.com/vi/${videoId}/mqdefault.jpg`;

  const getEmbedUrl = (videoId: string) =>
    `https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1&rel=0&modestbranding=1`;

  const openYouTube = (videoId: string) =>
    window.open(`https://www.youtube.com/watch?v=${videoId}`, "_blank", "noopener,noreferrer");

  return (
    <GlassCard className={`p-5 flex flex-col gap-4 ${className}`}>
      {/* ── Header ── */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-xl bg-accent/10 flex items-center justify-center">
            <GraduationCap className="w-4 h-4 text-accent" />
          </div>
          <div>
            <h3 className="font-extrabold text-sm tracking-tight text-[var(--text-main)]">
              Stock Market Learning Hub
            </h3>
            <span className="text-[10px] text-[var(--text-muted)] font-medium">
              Beginner → Pro · TIDI Kannada & GTF
            </span>
          </div>
        </div>
        <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-red-500/15 text-red-400 border border-red-500/20 flex items-center gap-1">
          <Youtube className="w-3 h-3" />
          {LEARNING_VIDEOS.length} Videos
        </span>
      </div>

      {/* ── Channel Badges ── */}
      <div className="flex items-center gap-2">
        <a
          href="https://www.youtube.com/@TIDIkannada"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg border border-red-500/30 bg-red-600/10 text-red-400 text-[10px] font-bold hover:bg-red-600/20 transition-colors"
        >
          <Youtube className="w-3 h-3" />
          TIDI Kannada
          <ExternalLink className="w-2.5 h-2.5 opacity-70" />
        </a>
        <a
          href="https://www.youtube.com/@gettogetherfinance"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg border border-emerald-500/30 bg-emerald-600/10 text-emerald-400 text-[10px] font-bold hover:bg-emerald-600/20 transition-colors"
        >
          <Youtube className="w-3 h-3" />
          GTF Finance
          <ExternalLink className="w-2.5 h-2.5 opacity-70" />
        </a>
      </div>

      {/* ── Level Filter Pills ── */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-0.5 no-scrollbar">
        {LEVELS.map((lvl) => (
          <button
            key={lvl}
            onClick={() => setSelectedLevel(lvl)}
            className={`shrink-0 px-2.5 py-1 rounded-lg text-[10px] font-bold capitalize border transition-all duration-150 ${
              selectedLevel === lvl
                ? "bg-accent text-white border-accent"
                : "bg-[var(--bg-card-subtle)] text-[var(--text-muted)] border-[var(--border-subtle)] hover:border-accent/50"
            }`}
          >
            {lvl === "All" ? "All Levels" : lvl.charAt(0).toUpperCase() + lvl.slice(1)}
          </button>
        ))}
      </div>

      {/* ── Category Filter Pills ── */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-1 no-scrollbar">
        {CATEGORIES.map((cat) => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            className={`shrink-0 px-2.5 py-1 rounded-lg text-[10px] font-semibold border transition-all duration-150 whitespace-nowrap ${
              selectedCategory === cat
                ? "bg-violet-600/20 text-violet-400 border-violet-500/40"
                : "bg-[var(--bg-card-subtle)] text-[var(--text-muted)] border-[var(--border-subtle)] hover:border-violet-500/30"
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* ── Video Grid ── */}
      <div className="flex flex-col gap-3">
        {filtered.length === 0 && (
          <div className="text-center py-8 text-[var(--text-muted)] text-xs">
            No videos match this filter. Try "All" to see everything.
          </div>
        )}
        {filtered.map((video) => {
          const levelCfg = LEVEL_CONFIG[video.level];
          const channelCfg = CHANNEL_CONFIG[video.channel];
          return (
            <div
              key={video.id}
              onClick={() => setActiveVideo(video)}
              className="group flex gap-3 p-3 rounded-2xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)] hover:border-violet-500/40 cursor-pointer transition-all duration-150 shadow-sm hover:shadow-md"
            >
              {/* Thumbnail */}
              <div className="relative shrink-0 w-28 h-[62px] rounded-xl overflow-hidden bg-black">
                <img
                  src={getThumbnailUrl(video.videoId)}
                  alt={video.title}
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    // Fallback to gradient if thumbnail fails
                    e.currentTarget.style.display = "none";
                    e.currentTarget.parentElement!.classList.add(
                      "bg-gradient-to-br",
                      ...video.thumbnail.split(" ")
                    );
                  }}
                />
                {/* Play overlay */}
                <div className="absolute inset-0 bg-black/30 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-150">
                  <div className="w-8 h-8 rounded-full bg-white/90 flex items-center justify-center shadow-lg">
                    <Play className="w-3.5 h-3.5 fill-gray-900 text-gray-900 ml-0.5" />
                  </div>
                </div>
                {/* Duration badge */}
                <span className="absolute bottom-1 right-1 px-1.5 py-0.5 rounded text-[9px] font-bold bg-black/80 text-white font-mono">
                  {video.duration}
                </span>
              </div>

              {/* Content */}
              <div className="flex flex-col gap-1 flex-1 min-w-0">
                {/* Badges row */}
                <div className="flex items-center gap-1.5 flex-wrap">
                  <span
                    className={`text-[9px] font-bold px-1.5 py-0.5 rounded border ${levelCfg.color}`}
                  >
                    {levelCfg.label}
                  </span>
                  <span
                    className={`text-[9px] font-bold px-1.5 py-0.5 rounded border ${channelCfg.badge}`}
                  >
                    {video.channelHandle}
                  </span>
                  <span className="text-[9px] font-semibold px-1.5 py-0.5 rounded bg-accent/10 text-accent border border-accent/20">
                    {video.category}
                  </span>
                </div>

                {/* Title */}
                <h4 className="text-xs font-bold text-[var(--text-main)] line-clamp-2 leading-snug group-hover:text-accent transition-colors">
                  {video.title}
                </h4>

                {/* Channel name */}
                <span className="text-[10px] text-[var(--text-muted)] flex items-center gap-1">
                  <Youtube className="w-3 h-3 text-red-500" />
                  {video.channelName}
                </span>
              </div>

              {/* Arrow */}
              <div className="flex items-center self-center shrink-0">
                <ChevronRight className="w-4 h-4 text-[var(--text-muted)] group-hover:text-accent transition-colors" />
              </div>
            </div>
          );
        })}
      </div>

      {/* ── Pathway Legend ── */}
      <div className="flex items-center gap-3 pt-1 border-t border-[var(--border-subtle)]">
        <div className="flex items-center gap-1 text-[9px] font-semibold text-emerald-500">
          <Target className="w-3 h-3" /> Beginner
        </div>
        <div className="flex items-center gap-1 text-[9px] font-semibold text-amber-500">
          <TrendingUp className="w-3 h-3" /> Intermediate
        </div>
        <div className="flex items-center gap-1 text-[9px] font-semibold text-rose-500">
          <Zap className="w-3 h-3" /> Advanced
        </div>
        <div className="ml-auto text-[9px] text-[var(--text-muted)]">
          {filtered.length}/{LEARNING_VIDEOS.length} videos
        </div>
      </div>

      {/* ── Video Player Modal ── */}
      <ModalSheet
        isOpen={Boolean(activeVideo)}
        onClose={() => setActiveVideo(null)}
        title={activeVideo?.title || "Video"}
      >
        {activeVideo && (
          <div className="flex flex-col gap-4 py-2">
            {/* Embedded Player */}
            <div className="relative w-full aspect-video rounded-2xl overflow-hidden bg-black shadow-2xl border border-[var(--border-subtle)]">
              <iframe
                key={activeVideo.id}
                title={activeVideo.title}
                src={getEmbedUrl(activeVideo.videoId)}
                className="w-full h-full border-0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                allowFullScreen
              />
            </div>

            {/* Meta */}
            <div className="flex flex-wrap items-center gap-2">
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${LEVEL_CONFIG[activeVideo.level].color}`}>
                {LEVEL_CONFIG[activeVideo.level].label}
              </span>
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${CHANNEL_CONFIG[activeVideo.channel].badge}`}>
                {activeVideo.channelHandle}
              </span>
              <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-accent/10 text-accent border border-accent/20">
                {activeVideo.category}
              </span>
              <span className="ml-auto text-[10px] text-[var(--text-muted)] font-mono flex items-center gap-1">
                <Clock className="w-3 h-3" />
                {activeVideo.duration}
              </span>
            </div>

            {/* Description */}
            <div className="p-3.5 rounded-xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)]">
              <div className="flex items-center gap-1.5 text-xs font-bold text-[var(--text-main)] mb-1.5">
                <Youtube className="w-3.5 h-3.5 text-red-500" />
                {activeVideo.channelName}
              </div>
              <p className="text-xs text-[var(--text-muted)] leading-relaxed">
                {activeVideo.description}
              </p>
            </div>

            {/* Action buttons */}
            <div className="flex gap-2 pt-1">
              <GhostButton
                className="flex-1 text-xs"
                onClick={() => openYouTube(activeVideo.videoId)}
              >
                <ExternalLink className="w-3.5 h-3.5 mr-1" />
                Open in YouTube
              </GhostButton>
              <PrimaryButton
                className="flex-1 text-xs"
                onClick={() => setActiveVideo(null)}
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

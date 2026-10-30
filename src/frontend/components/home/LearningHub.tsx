import React, { useState } from "react";
import {
  Clock,
  ChevronRight,
  Youtube,
  TrendingUp,
  Zap,
  ExternalLink,
  GraduationCap,
  Target,
  Search,
} from "lucide-react";
import { GlassCard, ModalSheet, PrimaryButton, GhostButton } from "../ui";

// ─────────────────────────────────────────────────────────────────────────────
// Learning Hub — curated topics with YouTube search links (always work)
// ─────────────────────────────────────────────────────────────────────────────

export interface LearningTopic {
  id: string;
  title: string;
  channel: "TIDI" | "GTF" | "BOTH";
  channelName: string;
  channelHandle: string;
  channelUrl: string;
  searchQuery: string; // used to build YouTube search URL
  category: string;
  level: "beginner" | "intermediate" | "advanced";
  duration: string;
  description: string;
}

// YouTube channel search URL: always returns live, available videos
const buildChannelSearchUrl = (channelHandle: string, query: string) =>
  `https://www.youtube.com/${channelHandle}/search?query=${encodeURIComponent(query)}`;

const LEARNING_TOPICS: LearningTopic[] = [
  // ── BEGINNER ───────────────────────────────────────────────────────────────
  {
    id: "l1",
    title: "Share Market Basics – How It Works",
    channel: "GTF",
    channelName: "GTF – A Stock Market Institute",
    channelHandle: "@gettogetherfinance",
    channelUrl: "https://www.youtube.com/@gettogetherfinance",
    searchQuery: "share market basics beginners",
    category: "Basics",
    level: "beginner",
    duration: "15–25 min",
    description:
      "What is a stock, how NSE & BSE work, what is SEBI, and how to open a Demat account. The complete starting point for any beginner investor.",
  },
  {
    id: "l2",
    title: "Stock Market Basics in Kannada",
    channel: "TIDI",
    channelName: "TIDI Kannada",
    channelHandle: "@TIDIkannada",
    channelUrl: "https://www.youtube.com/@TIDIkannada",
    searchQuery: "share market basics",
    category: "Basics",
    level: "beginner",
    duration: "10–20 min",
    description:
      "TIDI Kannada explains the stock market from scratch in Kannada — perfect for Kannada speakers who want to learn investing in their native language.",
  },
  {
    id: "l3",
    title: "How to Read Candlestick Charts",
    channel: "GTF",
    channelName: "GTF – A Stock Market Institute",
    channelHandle: "@gettogetherfinance",
    channelUrl: "https://www.youtube.com/@gettogetherfinance",
    searchQuery: "candlestick charts reading beginners",
    category: "Basics",
    level: "beginner",
    duration: "15–30 min",
    description:
      "Learn candlestick patterns, support & resistance, and price action. The core skill every trader must master before anything else.",
  },
  {
    id: "l4",
    title: "Fundamental Analysis – Picking Quality Stocks",
    channel: "GTF",
    channelName: "GTF – A Stock Market Institute",
    channelHandle: "@gettogetherfinance",
    channelUrl: "https://www.youtube.com/@gettogetherfinance",
    searchQuery: "fundamental analysis stocks PE ratio",
    category: "Basics",
    level: "beginner",
    duration: "20–30 min",
    description:
      "How to evaluate a company: P/E ratio, EPS, revenue growth, debt levels, and ROE. Learn to distinguish quality businesses from overpriced hype.",
  },

  // ── INTERMEDIATE ───────────────────────────────────────────────────────────
  {
    id: "l5",
    title: "Technical Analysis – RSI, MACD & Indicators",
    channel: "GTF",
    channelName: "GTF – A Stock Market Institute",
    channelHandle: "@gettogetherfinance",
    channelUrl: "https://www.youtube.com/@gettogetherfinance",
    searchQuery: "technical analysis RSI MACD indicators",
    category: "Strategy",
    level: "intermediate",
    duration: "25–40 min",
    description:
      "Master RSI, MACD, Bollinger Bands, and moving averages. Learn how to read momentum, divergence, and trend signals for entry and exit timing.",
  },
  {
    id: "l6",
    title: "Intraday Trading Strategy",
    channel: "GTF",
    channelName: "GTF – A Stock Market Institute",
    channelHandle: "@gettogetherfinance",
    channelUrl: "https://www.youtube.com/@gettogetherfinance",
    searchQuery: "intraday trading strategy stop loss",
    category: "Intraday",
    level: "intermediate",
    duration: "20–35 min",
    description:
      "Intraday setups, scalping strategies, stop-loss placement, and position sizing for same-day trading in Indian markets.",
  },
  {
    id: "l7",
    title: "Swing Trading Strategy",
    channel: "TIDI",
    channelName: "TIDI Kannada",
    channelHandle: "@TIDIkannada",
    channelUrl: "https://www.youtube.com/@TIDIkannada",
    searchQuery: "swing trading strategy",
    category: "Strategy",
    level: "intermediate",
    duration: "15–25 min",
    description:
      "Hold positions for 2–10 days to capture mid-term moves. Learn swing setups using price action, volume confirmation, and sector rotation.",
  },
  {
    id: "l8",
    title: "Stock Market News & Sector Analysis",
    channel: "GTF",
    channelName: "GTF – A Stock Market Institute",
    channelHandle: "@gettogetherfinance",
    channelUrl: "https://www.youtube.com/@gettogetherfinance",
    searchQuery: "stock market news sector rotation analysis",
    category: "News & Markets",
    level: "intermediate",
    duration: "10–20 min",
    description:
      "How RBI policy, inflation data, and global events move the market. Build a news-driven edge by understanding macro and sectoral cycles.",
  },

  // ── ADVANCED ───────────────────────────────────────────────────────────────
  {
    id: "l9",
    title: "Futures & Options (F&O) from Scratch",
    channel: "GTF",
    channelName: "GTF – A Stock Market Institute",
    channelHandle: "@gettogetherfinance",
    channelUrl: "https://www.youtube.com/@gettogetherfinance",
    searchQuery: "futures options F&O explained beginners",
    category: "F&O",
    level: "advanced",
    duration: "30–45 min",
    description:
      "Futures contracts, option buying vs selling, strike prices, expiry dates, open interest, and margin mechanics for Indian F&O markets.",
  },
  {
    id: "l10",
    title: "Options Greeks – Delta, Theta, Vega & Strategies",
    channel: "GTF",
    channelName: "GTF – A Stock Market Institute",
    channelHandle: "@gettogetherfinance",
    channelUrl: "https://www.youtube.com/@gettogetherfinance",
    searchQuery: "options greeks delta theta strategies",
    category: "Options",
    level: "advanced",
    duration: "35–50 min",
    description:
      "Delta, Gamma, Theta, and Vega explained practically. Learn covered calls, straddles, iron condors, and how to manage option positions like a pro.",
  },
  {
    id: "l11",
    title: "Algorithmic Trading – Build Your Own Strategy",
    channel: "TIDI",
    channelName: "TIDI Kannada",
    channelHandle: "@TIDIkannada",
    channelUrl: "https://www.youtube.com/@TIDIkannada",
    searchQuery: "algorithmic trading strategy python",
    category: "Algo Trading",
    level: "advanced",
    duration: "25–40 min",
    description:
      "Write and backtest your own quantitative algorithm. Automate trading signals and deploy on Indian brokers like Zerodha using APIs.",
  },
  {
    id: "l12",
    title: "Risk Management & Position Sizing",
    channel: "GTF",
    channelName: "GTF – A Stock Market Institute",
    channelHandle: "@gettogetherfinance",
    channelUrl: "https://www.youtube.com/@gettogetherfinance",
    searchQuery: "risk management position sizing trading",
    category: "Risk",
    level: "advanced",
    duration: "20–30 min",
    description:
      "Kelly Criterion, fixed fractional sizing, max drawdown limits, and capital protection rules. How professional traders survive the long run.",
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
  TIDI: { badge: "bg-red-600/20 text-red-400 border-red-500/30" },
  GTF: { badge: "bg-emerald-600/20 text-emerald-400 border-emerald-500/30" },
  BOTH: { badge: "bg-violet-600/20 text-violet-400 border-violet-500/30" },
};

// ─────────────────────────────────────────────────────────────────────────────

export interface LearningHubProps {
  className?: string;
}

export const LearningHub: React.FC<LearningHubProps> = ({ className = "" }) => {
  const [activeTopic, setActiveTopic] = useState<LearningTopic | null>(null);
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [selectedLevel, setSelectedLevel] = useState("All");

  const filtered = LEARNING_TOPICS.filter((v) => {
    const catMatch = selectedCategory === "All" || v.category === selectedCategory;
    const lvlMatch = selectedLevel === "All" || v.level === selectedLevel;
    return catMatch && lvlMatch;
  });

  const openSearch = (topic: LearningTopic) => {
    const url = buildChannelSearchUrl(topic.channelHandle, topic.searchQuery);
    window.open(url, "_blank", "noopener,noreferrer");
  };

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
          {LEARNING_TOPICS.length} Topics
        </span>
      </div>

      {/* ── Channel Links ── */}
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

      {/* ── Level Filter ── */}
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

      {/* ── Category Filter ── */}
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

      {/* ── Topic List ── */}
      <div className="flex flex-col gap-2.5">
        {filtered.length === 0 && (
          <div className="text-center py-8 text-[var(--text-muted)] text-xs">
            No topics match this filter.
          </div>
        )}
        {filtered.map((topic) => {
          const levelCfg = LEVEL_CONFIG[topic.level];
          const channelCfg = CHANNEL_CONFIG[topic.channel];
          return (
            <div
              key={topic.id}
              onClick={() => setActiveTopic(topic)}
              className="group flex gap-3 p-3 rounded-2xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)] hover:border-violet-500/40 cursor-pointer transition-all duration-150 shadow-sm hover:shadow-md"
            >
              {/* Channel color strip + icon */}
              <div className={`shrink-0 w-10 h-10 rounded-xl flex items-center justify-center ${
                topic.channel === "TIDI" ? "bg-red-600/15" : "bg-emerald-600/15"
              }`}>
                <Youtube className={`w-5 h-5 ${topic.channel === "TIDI" ? "text-red-500" : "text-emerald-500"}`} />
              </div>

              {/* Content */}
              <div className="flex flex-col gap-1 flex-1 min-w-0">
                {/* Badges */}
                <div className="flex items-center gap-1.5 flex-wrap">
                  <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded border ${levelCfg.color}`}>
                    {levelCfg.label}
                  </span>
                  <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded border ${channelCfg.badge}`}>
                    {topic.channelHandle}
                  </span>
                  <span className="text-[9px] font-semibold px-1.5 py-0.5 rounded bg-accent/10 text-accent border border-accent/20">
                    {topic.category}
                  </span>
                </div>

                {/* Title */}
                <h4 className="text-xs font-bold text-[var(--text-main)] line-clamp-2 leading-snug group-hover:text-accent transition-colors">
                  {topic.title}
                </h4>

                {/* Duration */}
                <span className="text-[10px] text-[var(--text-muted)] flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  {topic.duration}
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

      {/* ── Footer Legend ── */}
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
          {filtered.length}/{LEARNING_TOPICS.length} topics
        </div>
      </div>

      {/* ── Topic Detail Modal ── */}
      <ModalSheet
        isOpen={Boolean(activeTopic)}
        onClose={() => setActiveTopic(null)}
        title={activeTopic?.title || "Topic"}
      >
        {activeTopic && (
          <div className="flex flex-col gap-4 py-2">
            {/* Badges */}
            <div className="flex flex-wrap items-center gap-2">
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${LEVEL_CONFIG[activeTopic.level].color}`}>
                {LEVEL_CONFIG[activeTopic.level].label}
              </span>
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded border flex items-center gap-1 ${CHANNEL_CONFIG[activeTopic.channel].badge}`}>
                <Youtube className="w-3 h-3" />
                {activeTopic.channelHandle}
              </span>
              <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-accent/10 text-accent border border-accent/20">
                {activeTopic.category}
              </span>
              <span className="ml-auto text-[10px] text-[var(--text-muted)] font-mono flex items-center gap-1">
                <Clock className="w-3 h-3" />
                {activeTopic.duration}
              </span>
            </div>

            {/* Description */}
            <div className="p-3.5 rounded-xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)]">
              <p className="text-sm text-[var(--text-main)] leading-relaxed">
                {activeTopic.description}
              </p>
            </div>

            {/* Info note */}
            <div className="flex items-start gap-2 p-3 rounded-xl bg-amber-500/10 border border-amber-500/20">
              <Search className="w-3.5 h-3.5 text-amber-500 shrink-0 mt-0.5" />
              <p className="text-[11px] text-amber-700 dark:text-amber-300 leading-relaxed">
                Clicking "Find Videos" searches{" "}
                <strong>{activeTopic.channelName}</strong>'s YouTube channel for
                the best videos on this topic — always fresh and available.
              </p>
            </div>

            {/* Action buttons */}
            <div className="flex gap-2 pt-1">
              <GhostButton
                className="flex-1 text-xs"
                onClick={() => window.open(activeTopic.channelUrl, "_blank", "noopener,noreferrer")}
              >
                <Youtube className="w-3.5 h-3.5 mr-1" />
                Visit Channel
              </GhostButton>
              <PrimaryButton
                className="flex-1 text-xs"
                onClick={() => openSearch(activeTopic)}
              >
                <Search className="w-3.5 h-3.5 mr-1" />
                Find Videos
              </PrimaryButton>
            </div>
          </div>
        )}
      </ModalSheet>
    </GlassCard>
  );
};

import React, { useState } from "react";
import { Play, Clock, ExternalLink, Youtube, BookOpen, TrendingUp, Shield, Cpu, Search } from "lucide-react";
import { GlassCard, ModalSheet, PrimaryButton, GhostButton } from "../ui";

// ─────────────────────────────────────────────────────────────────────────────
// Featured video topics — search-based (always available, never 404)
// ─────────────────────────────────────────────────────────────────────────────

export interface VideoFacadeItem {
  id: string;
  title: string;
  duration: string;
  category: string;
  channel: "TIDI" | "GTF";
  channelName: string;
  channelHandle: string;
  channelUrl: string;
  searchQuery: string;
  summary: string;
  gradient: string;
  icon: React.ReactNode;
}

export const VIDEO_EXPLAINERS: VideoFacadeItem[] = [
  {
    id: "vid_1",
    title: "Share Market Basics – Complete Beginners Guide",
    duration: "15–25 min",
    category: "Basics",
    channel: "GTF",
    channelName: "GTF – A Stock Market Institute",
    channelHandle: "@gettogetherfinance",
    channelUrl: "https://www.youtube.com/@gettogetherfinance",
    searchQuery: "share market basics beginners",
    summary:
      "What is a stock? How do NSE & BSE work? What does SEBI do? GTF breaks down the foundations of stock markets for absolute beginners in India.",
    gradient: "from-blue-600 to-indigo-800",
    icon: <BookOpen className="w-5 h-5" />,
  },
  {
    id: "vid_2",
    title: "Technical Analysis – RSI, MACD & Chart Patterns",
    duration: "25–40 min",
    category: "Technical Analysis",
    channel: "GTF",
    channelName: "GTF – A Stock Market Institute",
    channelHandle: "@gettogetherfinance",
    channelUrl: "https://www.youtube.com/@gettogetherfinance",
    searchQuery: "technical analysis RSI MACD chart patterns",
    summary:
      "Master RSI, MACD, Bollinger Bands, and moving averages. GTF explains how to read momentum and trend signals for entry and exit decisions.",
    gradient: "from-emerald-600 to-teal-800",
    icon: <TrendingUp className="w-5 h-5" />,
  },
  {
    id: "vid_3",
    title: "Futures & Options (F&O) – Explained from Scratch",
    duration: "30–45 min",
    category: "F&O",
    channel: "GTF",
    channelName: "GTF – A Stock Market Institute",
    channelHandle: "@gettogetherfinance",
    channelUrl: "https://www.youtube.com/@gettogetherfinance",
    searchQuery: "futures options F&O explained beginners",
    summary:
      "Complete F&O guide covering futures contracts, option buying vs selling, strike prices, expiry, open interest, and margin for Indian markets.",
    gradient: "from-violet-600 to-purple-800",
    icon: <Shield className="w-5 h-5" />,
  },
  {
    id: "vid_4",
    title: "Algorithmic Trading in Kannada – Build Your Strategy",
    duration: "20–35 min",
    category: "Algo Trading",
    channel: "TIDI",
    channelName: "TIDI Kannada",
    channelHandle: "@TIDIkannada",
    channelUrl: "https://www.youtube.com/@TIDIkannada",
    searchQuery: "algorithmic trading strategy automation",
    summary:
      "TIDI Kannada explains how to write and backtest your own trading algorithm and automate strategies on Indian brokers like Zerodha.",
    gradient: "from-orange-600 to-red-800",
    icon: <Cpu className="w-5 h-5" />,
  },
];

// ─────────────────────────────────────────────────────────────────────────────

export interface VideoFacadesProps {
  className?: string;
}

const CHANNEL_BADGE = {
  TIDI: "bg-red-600/20 text-red-400 border border-red-500/30",
  GTF: "bg-emerald-600/20 text-emerald-400 border border-emerald-500/30",
};

const buildChannelSearchUrl = (handle: string, query: string) =>
  `https://www.youtube.com/${handle}/search?query=${encodeURIComponent(query)}`;

export const VideoFacades: React.FC<VideoFacadesProps> = ({ className = "" }) => {
  const [activeVideo, setActiveVideo] = useState<VideoFacadeItem | null>(null);

  const openSearch = (video: VideoFacadeItem) =>
    window.open(buildChannelSearchUrl(video.channelHandle, video.searchQuery), "_blank", "noopener,noreferrer");

  return (
    <GlassCard className={`p-5 flex flex-col gap-4 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-xl bg-red-500/15 flex items-center justify-center">
            <Youtube className="w-4 h-4 text-red-500" />
          </div>
          <div>
            <h3 className="font-extrabold text-sm tracking-tight text-[var(--text-main)]">
              Featured Video Lessons
            </h3>
            <span className="text-[10px] text-[var(--text-muted)] font-medium">
              Hand-picked topics from TIDI Kannada & GTF
            </span>
          </div>
        </div>
        <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-red-500/10 text-red-400 border border-red-500/20 flex items-center gap-1">
          <Play className="w-2.5 h-2.5 fill-current" />
          {VIDEO_EXPLAINERS.length} Topics
        </span>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {VIDEO_EXPLAINERS.map((video) => (
          <div
            key={video.id}
            data-testid="video-facade-card"
            onClick={() => setActiveVideo(video)}
            className="group relative overflow-hidden rounded-2xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)] hover:border-violet-500/50 cursor-pointer transition-all duration-200 flex flex-col shadow-sm hover:shadow-lg"
          >
            {/* Gradient poster (no image to 404) */}
            <div
              className={`h-28 w-full bg-gradient-to-br ${video.gradient} relative flex items-center justify-center p-3 overflow-hidden`}
            >
              {/* Subtle dot grid */}
              <div className="absolute inset-0 bg-[radial-gradient(#fff_1px,transparent_1px)] [background-size:14px_14px] opacity-10" />

              {/* Icon */}
              <div className="w-12 h-12 rounded-2xl bg-white/20 backdrop-blur-md flex items-center justify-center text-white shadow-xl border border-white/25 group-hover:scale-110 transition-transform duration-200">
                {video.icon}
              </div>

              {/* Category */}
              <span className="absolute top-2 left-2 px-2 py-0.5 rounded-md bg-black/50 backdrop-blur-md text-[9px] font-extrabold text-white tracking-wide uppercase">
                {video.category}
              </span>

              {/* Duration */}
              <span className="absolute bottom-2 right-2 px-2 py-0.5 rounded-md bg-black/60 backdrop-blur-sm text-[10px] font-bold text-white flex items-center gap-1 font-mono">
                <Clock className="w-3 h-3" />
                {video.duration}
              </span>

              {/* Channel badge */}
              <span className={`absolute top-2 right-2 px-1.5 py-0.5 rounded text-[9px] font-bold flex items-center gap-0.5 ${CHANNEL_BADGE[video.channel]} backdrop-blur-md`}>
                <Youtube className="w-2.5 h-2.5" />
                {video.channel}
              </span>
            </div>

            {/* Content */}
            <div className="p-3 flex flex-col gap-1.5 flex-1">
              <h4 className="text-xs font-bold text-[var(--text-main)] group-hover:text-accent transition-colors line-clamp-2 leading-snug">
                {video.title}
              </h4>
              <p className="text-[11px] text-[var(--text-muted)] line-clamp-2 leading-relaxed">
                {video.summary}
              </p>
              <div className="flex items-center justify-between pt-1.5 border-t border-[var(--border-subtle)] mt-auto">
                <span className="text-[10px] text-[var(--text-muted)] flex items-center gap-1">
                  <Youtube className="w-3 h-3 text-red-500" />
                  {video.channelName}
                </span>
                <span className="text-[10px] text-accent font-semibold flex items-center gap-0.5 group-hover:underline">
                  <Search className="w-2.5 h-2.5" />
                  Find Videos
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Modal */}
      <ModalSheet
        isOpen={Boolean(activeVideo)}
        onClose={() => setActiveVideo(null)}
        title={activeVideo?.title || "Video Topic"}
      >
        {activeVideo && (
          <div className="flex flex-col gap-4 py-2">
            {/* Gradient banner */}
            <div
              className={`w-full h-28 rounded-2xl bg-gradient-to-br ${activeVideo.gradient} flex items-center justify-center relative overflow-hidden`}
            >
              <div className="absolute inset-0 bg-[radial-gradient(#fff_1px,transparent_1px)] [background-size:14px_14px] opacity-10" />
              <div className="w-14 h-14 rounded-2xl bg-white/20 backdrop-blur-md flex items-center justify-center text-white shadow-xl border border-white/25">
                {activeVideo.icon}
              </div>
            </div>

            {/* Badges */}
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-[10px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-lg bg-accent/10 text-accent border border-accent/20">
                {activeVideo.category}
              </span>
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded flex items-center gap-1 ${CHANNEL_BADGE[activeVideo.channel]}`}>
                <Youtube className="w-3 h-3" />
                {activeVideo.channelHandle}
              </span>
              <span className="ml-auto text-xs text-[var(--text-muted)] flex items-center gap-1 font-mono">
                <Clock className="w-3 h-3" />
                {activeVideo.duration}
              </span>
            </div>

            {/* Summary */}
            <div className="p-3.5 rounded-xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)]">
              <div className="flex items-center gap-1.5 text-xs font-bold text-[var(--text-main)] mb-1.5">
                <Youtube className="w-3.5 h-3.5 text-red-500" />
                {activeVideo.channelName}
              </div>
              <p className="text-sm text-[var(--text-muted)] leading-relaxed">
                {activeVideo.summary}
              </p>
            </div>

            {/* Info */}
            <div className="flex items-start gap-2 p-3 rounded-xl bg-amber-500/10 border border-amber-500/20">
              <Search className="w-3.5 h-3.5 text-amber-500 shrink-0 mt-0.5" />
              <p className="text-[11px] text-amber-700 dark:text-amber-300 leading-relaxed">
                "Find Videos" searches <strong>{activeVideo.channelName}</strong>'s
                YouTube channel for the best videos on this topic — always fresh content.
              </p>
            </div>

            {/* Actions */}
            <div className="flex gap-2 pt-1">
              <GhostButton
                className="flex-1 text-xs"
                onClick={() => window.open(activeVideo.channelUrl, "_blank", "noopener,noreferrer")}
              >
                <ExternalLink className="w-3.5 h-3.5 mr-1" />
                Visit Channel
              </GhostButton>
              <PrimaryButton
                className="flex-1 text-xs"
                onClick={() => openSearch(activeVideo)}
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

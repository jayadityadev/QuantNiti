import React, { useState } from "react";
import { Play, Clock, ExternalLink, Youtube, BookOpen, TrendingUp, Shield, Cpu } from "lucide-react";
import { GlassCard, ModalSheet, PrimaryButton, GhostButton } from "../ui";

// ─────────────────────────────────────────────────────────────────────────────
// Real YouTube videos from TIDI Kannada & GTF curated for QuantNiti users
// ─────────────────────────────────────────────────────────────────────────────

export interface VideoFacadeItem {
  id: string;
  videoId: string;
  title: string;
  duration: string;
  category: string;
  channel: "TIDI" | "GTF";
  channelName: string;
  channelHandle: string;
  summary: string;
  icon: React.ReactNode;
  gradient: string;
}

const ICON_MAP = {
  BookOpen: <BookOpen className="w-5 h-5" />,
  TrendingUp: <TrendingUp className="w-5 h-5" />,
  Shield: <Shield className="w-5 h-5" />,
  Cpu: <Cpu className="w-5 h-5" />,
};

export const VIDEO_EXPLAINERS: VideoFacadeItem[] = [
  {
    id: "vid_1",
    videoId: "nt6GWFJaFKs",
    title: "Stock Market Basics – Beginners Guide",
    duration: "15:00",
    category: "Basics",
    channel: "TIDI",
    channelName: "TIDI Kannada",
    channelHandle: "@TIDIkannada",
    summary:
      "Understand how stock markets work, the role of NSE & BSE, and how to start your investing journey from zero with this TIDI Kannada crash course.",
    icon: ICON_MAP.BookOpen,
    gradient: "from-blue-600 to-indigo-800",
  },
  {
    id: "vid_2",
    videoId: "HoAlkRlBsU0",
    title: "Technical Analysis – RSI, MACD & More",
    duration: "30:00",
    category: "Technical Analysis",
    channel: "GTF",
    channelName: "GTF – A Stock Market Institute",
    channelHandle: "@gettogetherfinance",
    summary:
      "Master key technical indicators: RSI, MACD, Bollinger Bands, and moving averages. GTF breaks down chart reading into actionable trading signals.",
    icon: ICON_MAP.TrendingUp,
    gradient: "from-emerald-600 to-teal-800",
  },
  {
    id: "vid_3",
    videoId: "TlFKMz2RxCo",
    title: "Futures & Options – F&O from Scratch",
    duration: "35:00",
    category: "F&O",
    channel: "GTF",
    channelName: "GTF – A Stock Market Institute",
    channelHandle: "@gettogetherfinance",
    summary:
      "GTF's complete F&O guide covering futures contracts, option buying vs selling, strike prices, expiry, and margin management for Indian markets.",
    icon: ICON_MAP.Shield,
    gradient: "from-violet-600 to-purple-800",
  },
  {
    id: "vid_4",
    videoId: "Xn7KWR9EOGQ",
    title: "Algorithmic Trading – Build Your Strategy",
    duration: "28:00",
    category: "Algo Trading",
    channel: "TIDI",
    channelName: "TIDI Kannada",
    channelHandle: "@TIDIkannada",
    summary:
      "TIDI Kannada explains how to write your own quantitative strategy, backtest it, and automate trading on Indian brokers like Zerodha.",
    icon: ICON_MAP.Cpu,
    gradient: "from-orange-600 to-red-800",
  },
];

export interface VideoFacadesProps {
  className?: string;
}

const CHANNEL_BADGE = {
  TIDI: "bg-red-600/20 text-red-400 border border-red-500/30",
  GTF: "bg-emerald-600/20 text-emerald-400 border border-emerald-500/30",
};

export const VideoFacades: React.FC<VideoFacadesProps> = ({ className = "" }) => {
  const [activeVideo, setActiveVideo] = useState<VideoFacadeItem | null>(null);

  const getThumbnailUrl = (videoId: string) =>
    `https://img.youtube.com/vi/${videoId}/mqdefault.jpg`;

  const getEmbedUrl = (videoId: string) =>
    `https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1&rel=0&modestbranding=1`;

  const openYouTube = (videoId: string) =>
    window.open(`https://www.youtube.com/watch?v=${videoId}`, "_blank", "noopener,noreferrer");

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
              Hand-picked from TIDI Kannada & GTF
            </span>
          </div>
        </div>
        <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-red-500/10 text-red-400 border border-red-500/20 flex items-center gap-1">
          <Play className="w-2.5 h-2.5 fill-current" />
          {VIDEO_EXPLAINERS.length} Featured
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
            {/* Thumbnail */}
            <div className="relative h-32 w-full overflow-hidden bg-black">
              <img
                src={getThumbnailUrl(video.videoId)}
                alt={video.title}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                onError={(e) => {
                  e.currentTarget.style.display = "none";
                  e.currentTarget.parentElement!.classList.add(
                    "bg-gradient-to-br",
                    ...video.gradient.split(" ")
                  );
                }}
              />
              {/* Dark overlay */}
              <div className="absolute inset-0 bg-black/25 group-hover:bg-black/40 transition-colors" />

              {/* Play button */}
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="w-12 h-12 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center text-white shadow-xl border border-white/30 group-hover:scale-110 transition-transform duration-200">
                  <Play className="w-5 h-5 fill-white ml-0.5" />
                </div>
              </div>

              {/* Category badge */}
              <span className="absolute top-2 left-2 px-2 py-0.5 rounded-md bg-black/60 backdrop-blur-md text-[9px] font-extrabold text-white tracking-wide uppercase">
                {video.category}
              </span>

              {/* Duration */}
              <span className="absolute bottom-2 right-2 px-2 py-0.5 rounded-md bg-black/70 backdrop-blur-sm text-[10px] font-bold text-white flex items-center gap-1 font-mono">
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
                  <Play className="w-2.5 h-2.5 fill-current" />
                  Watch
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Video Player Modal */}
      <ModalSheet
        isOpen={Boolean(activeVideo)}
        onClose={() => setActiveVideo(null)}
        title={activeVideo?.title || "Video Lesson"}
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

            {/* Actions */}
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

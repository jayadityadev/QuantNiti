import React, { useState } from "react";
import { Play, Clock, Youtube } from "lucide-react";
import { GlassCard } from "../ui";
import { LessonSheet } from "./LessonSheet";
import { CHANNELS, LESSONS, Lesson, formatDuration, thumbnailUrl } from "./learningLessons";

// ─────────────────────────────────────────────────────────────────────────────
// Featured lessons — a hand-picked path through the Learning Hub catalogue
// ─────────────────────────────────────────────────────────────────────────────

const FEATURED_IDS = ["l18", "l6", "l13", "l15"];

export const FEATURED_LESSONS: Lesson[] = FEATURED_IDS.map((id) => LESSONS.find((l) => l.id === id)).filter(
  (l): l is Lesson => Boolean(l)
);

export interface VideoFacadesProps {
  className?: string;
}

export const VideoFacades: React.FC<VideoFacadesProps> = ({ className = "" }) => {
  const [activeLesson, setActiveLesson] = useState<Lesson | null>(null);

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
              Hand-picked from TIDI ಕನ್ನಡ & GTF
            </span>
          </div>
        </div>
        <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-red-500/10 text-red-400 border border-red-500/20 flex items-center gap-1">
          <Play className="w-2.5 h-2.5 fill-current" />
          {FEATURED_LESSONS.length} Videos
        </span>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {FEATURED_LESSONS.map((lesson) => {
          const channel = CHANNELS[lesson.channel];
          return (
            <button
              type="button"
              key={lesson.id}
              data-testid="video-facade-card"
              onClick={() => setActiveLesson(lesson)}
              className="group text-left relative overflow-hidden rounded-2xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)] hover:border-violet-500/50 transition-all duration-200 flex flex-col shadow-sm hover:shadow-lg"
            >
              {/* Thumbnail */}
              <div className="relative w-full aspect-video bg-black overflow-hidden">
                <img
                  src={thumbnailUrl(lesson.videoId)}
                  alt=""
                  loading="lazy"
                  className="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                />
                <span className="absolute inset-0 flex items-center justify-center bg-black/15">
                  <span className="w-12 h-8 rounded-xl bg-red-600 group-hover:bg-red-500 flex items-center justify-center shadow-xl transition-colors">
                    <Play className="w-4 h-4 text-white fill-current" />
                  </span>
                </span>
                <span className="absolute top-2 left-2 px-2 py-0.5 rounded-md bg-black/60 backdrop-blur-md text-[9px] font-extrabold text-white tracking-wide uppercase">
                  {lesson.category}
                </span>
                <span className="absolute bottom-2 right-2 px-2 py-0.5 rounded-md bg-black/70 text-[10px] font-bold text-white flex items-center gap-1 font-mono">
                  <Clock className="w-3 h-3" />
                  {formatDuration(lesson.durationSeconds)}
                </span>
              </div>

              {/* Content */}
              <div className="p-3 flex flex-col gap-1.5 flex-1">
                <h4 className="text-xs font-bold text-[var(--text-main)] group-hover:text-accent transition-colors line-clamp-2 leading-snug">
                  {lesson.title}
                </h4>
                <p className="text-[11px] text-[var(--text-muted)] line-clamp-2 leading-relaxed">
                  {lesson.description}
                </p>
                <div className="flex items-center justify-between pt-1.5 border-t border-[var(--border-subtle)] mt-auto">
                  <span className="text-[10px] text-[var(--text-muted)] flex items-center gap-1 truncate">
                    <Youtube className={`w-3 h-3 shrink-0 ${channel.iconText}`} />
                    {channel.name} · {channel.language}
                  </span>
                  <span className="text-[10px] text-accent font-semibold flex items-center gap-0.5 shrink-0">
                    <Play className="w-2.5 h-2.5 fill-current" />
                    Play
                  </span>
                </div>
              </div>
            </button>
          );
        })}
      </div>

      <LessonSheet lesson={activeLesson} onClose={() => setActiveLesson(null)} />
    </GlassCard>
  );
};

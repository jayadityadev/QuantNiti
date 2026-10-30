import React, { useState } from "react";
import {
  ChevronRight,
  Youtube,
  TrendingUp,
  Zap,
  ExternalLink,
  GraduationCap,
  Target,
  Play,
} from "lucide-react";
import { GlassCard } from "../ui";
import { LessonSheet, LEVEL_CONFIG } from "./LessonSheet";
import {
  CHANNELS,
  LESSONS,
  LESSON_CATEGORIES,
  Lesson,
  formatDuration,
  thumbnailUrl,
} from "./learningLessons";

// ─────────────────────────────────────────────────────────────────────────────
// Learning Hub — curated lessons that play inline
// ─────────────────────────────────────────────────────────────────────────────

const LEVELS = ["All", "beginner", "intermediate", "advanced"];

export interface LearningHubProps {
  className?: string;
}

export const LearningHub: React.FC<LearningHubProps> = ({ className = "" }) => {
  const [activeLesson, setActiveLesson] = useState<Lesson | null>(null);
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [selectedLevel, setSelectedLevel] = useState("All");

  const filtered = LESSONS.filter((lesson) => {
    const catMatch = selectedCategory === "All" || lesson.category === selectedCategory;
    const lvlMatch = selectedLevel === "All" || lesson.level === selectedLevel;
    return catMatch && lvlMatch;
  });

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
              Beginner → Pro · Kannada & Hindi lessons
            </span>
          </div>
        </div>
        <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-red-500/15 text-red-400 border border-red-500/20 flex items-center gap-1">
          <Youtube className="w-3 h-3" />
          {LESSONS.length} Lessons
        </span>
      </div>

      {/* ── Channel Links ── */}
      <div className="flex items-center gap-2 flex-wrap">
        {Object.values(CHANNELS).map((channel) => (
          <a
            key={channel.handle}
            href={channel.url}
            target="_blank"
            rel="noopener noreferrer"
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg border text-[10px] font-bold hover:opacity-80 transition-opacity ${channel.badge}`}
          >
            <Youtube className="w-3 h-3" />
            {channel.name}
            <span className="font-medium opacity-70">· {channel.language}</span>
            <ExternalLink className="w-2.5 h-2.5 opacity-70" />
          </a>
        ))}
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
        {LESSON_CATEGORIES.map((cat) => (
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

      {/* ── Lesson List ── */}
      <div className="flex flex-col gap-2.5">
        {filtered.length === 0 && (
          <div className="text-center py-8 text-[var(--text-muted)] text-xs">
            No lessons match this filter.
          </div>
        )}
        {filtered.map((lesson) => {
          const levelCfg = LEVEL_CONFIG[lesson.level];
          const channel = CHANNELS[lesson.channel];
          return (
            <button
              type="button"
              key={lesson.id}
              onClick={() => setActiveLesson(lesson)}
              className="group text-left flex gap-3 p-2.5 rounded-2xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)] hover:border-violet-500/40 transition-all duration-150 shadow-sm hover:shadow-md"
            >
              {/* Thumbnail */}
              <div className="relative shrink-0 w-28 aspect-video rounded-xl overflow-hidden bg-black">
                <img
                  src={thumbnailUrl(lesson.videoId)}
                  alt=""
                  loading="lazy"
                  className="absolute inset-0 w-full h-full object-cover"
                />
                <span className="absolute inset-0 flex items-center justify-center bg-black/20 group-hover:bg-black/10 transition-colors">
                  <span className="w-7 h-5 rounded-md bg-red-600 flex items-center justify-center">
                    <Play className="w-3 h-3 text-white fill-current" />
                  </span>
                </span>
                <span className="absolute bottom-1 right-1 px-1 rounded bg-black/75 text-[9px] font-mono font-bold text-white">
                  {formatDuration(lesson.durationSeconds)}
                </span>
              </div>

              {/* Content */}
              <div className="flex flex-col gap-1 flex-1 min-w-0">
                <div className="flex items-center gap-1.5 flex-wrap">
                  <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded border ${levelCfg.color}`}>
                    {levelCfg.label}
                  </span>
                  <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded border ${channel.badge}`}>
                    {lesson.channel} · {channel.language}
                  </span>
                </div>
                <h4 className="text-xs font-bold text-[var(--text-main)] line-clamp-2 leading-snug group-hover:text-accent transition-colors">
                  {lesson.title}
                </h4>
                <span className="text-[10px] text-[var(--text-muted)]">{lesson.category}</span>
              </div>

              <div className="flex items-center self-center shrink-0">
                <ChevronRight className="w-4 h-4 text-[var(--text-muted)] group-hover:text-accent transition-colors" />
              </div>
            </button>
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
          {filtered.length}/{LESSONS.length} lessons
        </div>
      </div>

      <LessonSheet lesson={activeLesson} onClose={() => setActiveLesson(null)} />
    </GlassCard>
  );
};

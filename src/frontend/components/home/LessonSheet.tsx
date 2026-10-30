import React from "react";
import { Clock, ExternalLink, Youtube } from "lucide-react";
import { ModalSheet } from "../ui";
import { VideoPlayer } from "./VideoPlayer";
import { CHANNELS, Lesson, formatDuration, watchUrl } from "./learningLessons";

export const LEVEL_CONFIG = {
  beginner: { label: "Beginner", color: "text-emerald-500 bg-emerald-500/10 border-emerald-500/20" },
  intermediate: { label: "Intermediate", color: "text-amber-500 bg-amber-500/10 border-amber-500/20" },
  advanced: { label: "Advanced", color: "text-rose-500 bg-rose-500/10 border-rose-500/20" },
};

interface LessonSheetProps {
  lesson: Lesson | null;
  onClose: () => void;
}

/** Bottom sheet that plays a lesson inline, with links out to YouTube. */
export const LessonSheet: React.FC<LessonSheetProps> = ({ lesson, onClose }) => {
  const channel = lesson ? CHANNELS[lesson.channel] : null;

  return (
    <ModalSheet isOpen={Boolean(lesson)} onClose={onClose} title={lesson?.title || "Lesson"}>
      {lesson && channel && (
        <div className="flex flex-col gap-4 py-2">
          <div className="flex flex-wrap items-center gap-2">
            <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${LEVEL_CONFIG[lesson.level].color}`}>
              {LEVEL_CONFIG[lesson.level].label}
            </span>
            <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-accent/10 text-accent border border-accent/20">
              {lesson.category}
            </span>
            <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-[var(--bg-card-subtle)] text-[var(--text-muted)] border border-[var(--border-subtle)]">
              {channel.language}
            </span>
            <span className="ml-auto text-[10px] text-[var(--text-muted)] font-mono flex items-center gap-1">
              <Clock className="w-3 h-3" />
              {formatDuration(lesson.durationSeconds)}
            </span>
          </div>

          {/* key: restart from the thumbnail when switching lessons */}
          <VideoPlayer key={lesson.videoId} videoId={lesson.videoId} title={lesson.title} />

          <div className="p-3.5 rounded-xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)]">
            <div className="flex items-center gap-1.5 text-xs font-bold text-[var(--text-main)] mb-1.5">
              <Youtube className={`w-3.5 h-3.5 ${channel.iconText}`} />
              {channel.name}
            </div>
            <p className="text-sm text-[var(--text-muted)] leading-relaxed">{lesson.description}</p>
          </div>

          <div className="flex gap-2">
            <a
              href={channel.url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 flex items-center justify-center gap-1.5 px-3 py-2.5 rounded-xl border border-[var(--border-subtle)] text-xs font-bold text-[var(--text-muted)] hover:text-accent hover:border-accent/40 transition-colors"
            >
              <Youtube className="w-3.5 h-3.5" />
              More from {lesson.channel}
            </a>
            <a
              href={watchUrl(lesson.videoId)}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 flex items-center justify-center gap-1.5 px-3 py-2.5 rounded-xl bg-accent/10 border border-accent/30 text-xs font-bold text-accent hover:bg-accent/20 transition-colors"
            >
              <ExternalLink className="w-3.5 h-3.5" />
              Open in YouTube
            </a>
          </div>
        </div>
      )}
    </ModalSheet>
  );
};

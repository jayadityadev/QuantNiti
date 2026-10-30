import React, { useState } from "react";
import { Play } from "lucide-react";
import { thumbnailUrl } from "./learningLessons";

// ──────────────────────────────────────────────────────────────────────
// Lightweight YouTube player: shows the real thumbnail until tapped, then
// swaps in the privacy-enhanced (youtube-nocookie) embed and autoplays.
// No IFrame API script, no global element ids — safe to render many.
// ──────────────────────────────────────────────────────────────────────

interface VideoPlayerProps {
  /** 11-character YouTube video ID */
  videoId: string;
  /** Used for the iframe title and thumbnail alt text */
  title: string;
  className?: string;
}

export const VideoPlayer: React.FC<VideoPlayerProps> = ({ videoId, title, className = "" }) => {
  const [isPlaying, setIsPlaying] = useState(false);

  return (
    <div
      className={`relative w-full aspect-video rounded-xl overflow-hidden bg-black border border-[var(--border-subtle)] ${className}`}
    >
      {isPlaying ? (
        <iframe
          className="absolute inset-0 w-full h-full"
          src={`https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1&rel=0&modestbranding=1&playsinline=1`}
          title={title}
          // YouTube rejects embeds that arrive without a referrer (player error 153)
          referrerPolicy="strict-origin-when-cross-origin"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          allowFullScreen
        />
      ) : (
        <button
          type="button"
          onClick={() => setIsPlaying(true)}
          aria-label={`Play video: ${title}`}
          className="group absolute inset-0 w-full h-full"
        >
          <img
            src={thumbnailUrl(videoId)}
            alt=""
            loading="lazy"
            className="absolute inset-0 w-full h-full object-cover opacity-90 group-hover:opacity-100 transition-opacity"
          />
          <span className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent" />
          <span className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-16 h-11 rounded-2xl bg-red-600 group-hover:bg-red-500 flex items-center justify-center shadow-xl transition-colors">
            <Play className="w-6 h-6 text-white fill-current" />
          </span>
        </button>
      )}
    </div>
  );
};

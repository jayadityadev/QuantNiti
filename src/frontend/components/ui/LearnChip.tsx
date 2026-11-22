import React from "react";
import { HelpCircle } from "lucide-react";

export interface LearnChipProps {
  concept?: string;
  children?: React.ReactNode;
  onClick?: () => void;
  className?: string;
}

export const LearnChip: React.FC<LearnChipProps> = ({
  concept,
  children,
  onClick,
  className = "",
}) => {
  const content = children || concept || "Learn";

  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={`Learn more about ${concept || "concept"}`}
      className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium text-teal-700 dark:text-teal-400 bg-teal-500/10 hover:bg-teal-500/15 border border-teal-500/20 active:scale-95 transition-colors transition-transform duration-150 focus-visible:ring-1 focus-visible:ring-teal-500 focus-visible:outline-none ${className}`}
    >
      <HelpCircle className="w-3 h-3 text-teal-600 dark:text-teal-400" />
      <span>{content}</span>
    </button>
  );
};

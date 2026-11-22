import React from "react";
import { motion, HTMLMotionProps } from "framer-motion";

export interface ChipButtonProps extends Omit<HTMLMotionProps<"button">, "children"> {
  children: React.ReactNode;
  selected?: boolean;
  active?: boolean;
  icon?: React.ReactNode;
  disabled?: boolean;
  className?: string;
}

export const ChipButton: React.FC<ChipButtonProps> = ({
  children,
  selected = false,
  active = false,
  icon,
  disabled = false,
  className = "",
  type = "button",
  ...props
}) => {
  const isSelected = selected || active;

  return (
    <motion.button
      whileTap={disabled ? undefined : { scale: 0.97 }}
      disabled={disabled}
      type={type}
      className={`inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-xs font-medium transition-colors transition-transform duration-150 border disabled:opacity-50 disabled:pointer-events-none focus-visible:ring-2 focus-visible:ring-teal-500 focus-visible:outline-none ${
        isSelected
          ? "bg-slate-900 text-white border-slate-900 dark:bg-teal-600 dark:border-teal-500 shadow-sm"
          : "bg-[var(--bg-card-subtle)] text-[var(--text-main)] border-[var(--border-subtle)] hover:border-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800"
      } ${className}`}
      {...props}
    >
      {icon}
      <span>{children}</span>
    </motion.button>
  );
};

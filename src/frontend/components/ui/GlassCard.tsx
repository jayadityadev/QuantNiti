import React from "react";
import { motion, HTMLMotionProps } from "framer-motion";
import { fadeInUpVariants } from "./transitions";

export interface GlassCardProps extends HTMLMotionProps<"div"> {
  children: React.ReactNode;
  className?: string;
  delay?: number;
  highlight?: boolean;
}

export const GlassCard: React.FC<GlassCardProps> = ({
  children,
  className = "",
  delay = 0,
  highlight = true,
  ...props
}) => {
  return (
    <motion.div
      variants={fadeInUpVariants}
      initial="initial"
      animate="animate"
      exit="exit"
      transition={{ delay }}
      className={`relative overflow-hidden rounded-3xl bg-[var(--bg-card)] border border-[var(--border-subtle)] shadow-sm transition-colors duration-200 ${
        highlight
          ? "before:pointer-events-none before:absolute before:inset-x-0 before:top-0 before:h-[1px] before:bg-[var(--border-subtle)]"
          : ""
      } ${className}`}
      {...props}
    >
      {children}
    </motion.div>
  );
};

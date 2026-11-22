import React from "react";
import { motion, HTMLMotionProps } from "framer-motion";
import { Loader2 } from "lucide-react";

export interface PrimaryButtonProps extends Omit<HTMLMotionProps<"button">, "children"> {
  children: React.ReactNode;
  loading?: boolean;
  disabled?: boolean;
  icon?: React.ReactNode;
  fullWidth?: boolean;
  className?: string;
}

export const PrimaryButton: React.FC<PrimaryButtonProps> = ({
  children,
  loading = false,
  disabled = false,
  icon,
  fullWidth = false,
  className = "",
  type = "button",
  ...props
}) => {
  const isDisabled = disabled || loading;

  return (
    <motion.button
      whileTap={isDisabled ? undefined : { scale: 0.98 }}
      disabled={isDisabled}
      type={type}
      className={`relative inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl font-medium text-sm text-white bg-slate-900 hover:bg-slate-800 dark:bg-teal-600 dark:hover:bg-teal-500 active:scale-[0.98] shadow-sm disabled:opacity-50 disabled:pointer-events-none focus-visible:ring-2 focus-visible:ring-teal-500 focus-visible:outline-none transition-colors transition-transform duration-150 ${
        fullWidth ? "w-full" : ""
      } ${className}`}
      {...props}
    >
      {loading ? (
        <Loader2 className="w-4 h-4 animate-spin text-white" aria-hidden="true" />
      ) : (
        icon
      )}
      <span>{children}</span>
    </motion.button>
  );
};

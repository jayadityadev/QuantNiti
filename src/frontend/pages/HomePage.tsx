import React from "react";
import { motion } from "framer-motion";
import { GraduationCap, ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";
import { MarketPulse } from "../components/home/MarketPulse";
import { RegimeRadar } from "../components/home/RegimeRadar";
import { AdaptiveHomeCard } from "../components/home/AdaptiveHomeCard";
import { TopRecommendations } from "../components/home/TopRecommendations";
import { CompoundingVisualizer } from "../components/home/CompoundingVisualizer";
import { GlassCard } from "../components/ui/GlassCard";

const containerVariants = {
  initial: { opacity: 0 },
  animate: {
    opacity: 1,
    transition: {
      staggerChildren: 0.08,
    },
  },
};

const itemVariants = {
  initial: { opacity: 0, y: 15 },
  animate: {
    opacity: 1,
    y: 0,
    transition: { type: "spring", stiffness: 320, damping: 26 },
  },
};

export const HomePage: React.FC = () => {
  return (
    <motion.div
      variants={containerVariants}
      initial="initial"
      animate="animate"
      className="flex flex-col gap-5 p-4"
    >
      <h1 className="sr-only">Home Page</h1>

      {/* 1. Live Market Pulse */}
      <motion.div variants={itemVariants}>
        <MarketPulse />
      </motion.div>

      {/* 2. Market Regime Radar */}
      <motion.div variants={itemVariants}>
        <RegimeRadar />
      </motion.div>

      {/* 3. Adaptive Card (Onboarding CTA vs Portfolio Snapshot) */}
      <motion.div variants={itemVariants}>
        <AdaptiveHomeCard />
      </motion.div>

      {/* 4. Top Curated Recommendations */}
      <motion.div variants={itemVariants}>
        <TopRecommendations />
      </motion.div>

      {/* 5. Systematic Compounding Visualizer */}
      <motion.div variants={itemVariants}>
        <CompoundingVisualizer />
      </motion.div>

      {/* 6. Quick Gateway to Quant Mastery Lab & Learn Tab */}
      <motion.div variants={itemVariants}>
        <Link to="/learn" className="block group">
          <GlassCard className="p-4 flex items-center justify-between border-violet-500/20 group-hover:border-violet-500/50 transition-colors">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-violet-600/15 flex items-center justify-center text-violet-600 dark:text-violet-400 group-hover:scale-105 transition-transform">
                <GraduationCap className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-[var(--text-main)] group-hover:text-accent transition-colors">
                  Quant Mastery Lab
                </h3>
                <p className="text-[11px] text-[var(--text-muted)]">
                  Compare 5 algorithmic trading strategies & watch masterclasses.
                </p>
              </div>
            </div>
            <ArrowRight className="w-4 h-4 text-violet-400 group-hover:translate-x-1 transition-transform" />
          </GlassCard>
        </Link>
      </motion.div>
    </motion.div>
  );
};

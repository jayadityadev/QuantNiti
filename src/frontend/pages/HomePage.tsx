import React from "react";
import { motion } from "framer-motion";
import { MarketPulse } from "../components/home/MarketPulse";
import { RegimeRadar } from "../components/home/RegimeRadar";
import { AdaptiveHomeCard } from "../components/home/AdaptiveHomeCard";
import { TopRecommendations } from "../components/home/TopRecommendations";
import { CompoundingVisualizer } from "../components/home/CompoundingVisualizer";

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
      className="flex flex-col gap-6 p-4 md:p-6 max-w-7xl mx-auto"
    >
      <h1 className="sr-only">Home Page • QuantNiti Market Overview</h1>

      {/* Top Grid: Market Pulse & Regime Radar */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 items-stretch">
        <motion.div variants={itemVariants} className="flex">
          <MarketPulse className="w-full" />
        </motion.div>
        <motion.div variants={itemVariants} className="flex">
          <RegimeRadar className="w-full" />
        </motion.div>
      </div>

      {/* Middle Grid: Adaptive Snapshot & Compounding Visualizer */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 items-stretch">
        <motion.div variants={itemVariants} className="flex">
          <AdaptiveHomeCard className="w-full" />
        </motion.div>
        <motion.div variants={itemVariants} className="flex">
          <CompoundingVisualizer className="w-full" />
        </motion.div>
      </div>

      {/* 3. Top Curated Recommendations */}
      <motion.div variants={itemVariants}>
        <TopRecommendations />
      </motion.div>
    </motion.div>
  );
};

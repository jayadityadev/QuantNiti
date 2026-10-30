import { useEffect } from "react";
import { useLocation, Routes, Route, Navigate } from "react-router-dom";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import { Header } from "./Header";
import { BottomNav } from "./BottomNav";
import { useAppStore, NavTab } from "../../store/useAppStore";
import { abortRegistry } from "../../services/abortRegistry";
import { OnboardingHero } from "../onboarding/OnboardingHero";
import { GrowPage } from "../grow/GrowPage";
import { HomePage } from "../../pages/HomePage";
import { ExplorePage } from "../../pages/ExplorePage";
import { PortfolioPage } from "../portfolio/PortfolioPage";
import { ModalRoot } from "../modals/ModalRoot";
import { IOSInstallBanner } from "../pwa/IOSInstallBanner";

export function AppShell() {
  const location = useLocation();
  const shouldReduceMotion = useReducedMotion();
  const { activeTab, setActiveTab, clearActiveAsyncKeys, isOnboarded, isExpandedViewport, toggleViewport } = useAppStore();

  // Keep route pathname in sync with activeTab in Zustand store and abort in-flight requests from prior tab
  useEffect(() => {
    const rawPath = location.pathname.replace(/^\//, "").toLowerCase();
    const validTabs: NavTab[] = ["home", "explore", "grow", "portfolio"];
    if (validTabs.includes(rawPath as NavTab)) {
      setActiveTab(rawPath as NavTab);
    }

    // Abort the outgoing tab's requests in cleanup. Aborting in the effect body would
    // also kill the incoming page's fetches, because child effects run before this one.
    return () => {
      abortRegistry.abortAll("tab-switch");
      clearActiveAsyncKeys?.();
    };
  }, [location.pathname, setActiveTab, clearActiveAsyncKeys]);

  // Motion variants respecting reduced motion preferences
  const pageVariants = {
    initial: shouldReduceMotion
      ? { opacity: 0 }
      : { opacity: 0, y: 20 },
    animate: shouldReduceMotion
      ? { opacity: 1 }
      : { opacity: 1, y: 0 },
    exit: shouldReduceMotion
      ? { opacity: 0 }
      : { opacity: 0, y: -10 },
  };

  const pageTransition = shouldReduceMotion
    ? { duration: 0.1 }
    : { type: "spring", stiffness: 300, damping: 25 };

  return (
    <div className="min-h-screen bg-[var(--bg-primary)] text-[var(--text-main)] flex justify-center transition-colors duration-200">
      {/* Full-screen Onboarding Overlay */}
      <AnimatePresence>
        {!isOnboarded && (
          <motion.div
            key="onboarding-overlay"
            initial={{ opacity: 1 }}
            exit={shouldReduceMotion ? { opacity: 0 } : { opacity: 0, scale: 0.98 }}
            transition={{ duration: 0.35, ease: "easeInOut" }}
            className="fixed inset-0 z-50 overflow-hidden"
          >
            <OnboardingHero />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Container constrained to max-w-[520px] on desktop with centered shadow, or expanded max-w-6xl when toggled */}
      <div className={`w-full ${isExpandedViewport ? "max-w-6xl" : "max-w-[520px]"} min-h-screen flex flex-col bg-[var(--bg-primary)] shadow-2xl shadow-violet-950/5 relative border-x border-[var(--border-subtle)] transition-all duration-300`}>
        {/* Sticky Header - visible when onboarded */}
        {isOnboarded && <Header onViewportToggle={toggleViewport} />}

        {/* Scrollable Content Area with bottom nav clearance */}
        <main className="flex-1 overflow-y-auto content-bottom-safe relative">
          <AnimatePresence mode="wait">
            <motion.div
              key={location.pathname}
              variants={pageVariants}
              initial="initial"
              animate="animate"
              exit="exit"
              transition={pageTransition}
              className="w-full h-full"
            >
              <Routes location={location}>
                <Route path="/home" element={<HomePage />} />
                <Route path="/explore" element={<ExplorePage />} />
                <Route path="/grow" element={<GrowPage />} />
                <Route path="/portfolio" element={<PortfolioPage />} />
                <Route path="*" element={<Navigate to="/home" replace />} />
              </Routes>
            </motion.div>
          </AnimatePresence>
        </main>

        {/* Fixed Bottom Navigation - visible when onboarded */}
        {isOnboarded && <BottomNav activeTab={activeTab} onTabChange={setActiveTab} />}

        {/* Global Modals & Overlays Root */}
        {isOnboarded && <ModalRoot />}

        {/* iOS Safari Installation Guidance Banner */}
        {isOnboarded && <IOSInstallBanner />}
      </div>
    </div>
  );
}

import { useEffect } from "react";
import { useLocation, Routes, Route, Navigate } from "react-router-dom";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import { Header } from "./Header";
import { BottomNav } from "./BottomNav";
import { DesktopSidebar } from "./DesktopSidebar";
import { useAppStore, NavTab } from "../../store/useAppStore";
import { abortRegistry } from "../../services/abortRegistry";
import { OnboardingHero } from "../onboarding/OnboardingHero";
import { GrowPage } from "../grow/GrowPage";
import { HomePage } from "../../pages/HomePage";
import { LearnPage } from "../../pages/LearnPage";
import { ExplorePage } from "../../pages/ExplorePage";
import { PortfolioPage } from "../portfolio/PortfolioPage";
import { ModalRoot } from "../modals/ModalRoot";
import { IOSInstallBanner } from "../pwa/IOSInstallBanner";
import { ErrorBoundary } from "../ui/ErrorBoundary";

export function AppShell() {
  const location = useLocation();
  const shouldReduceMotion = useReducedMotion();
  const { activeTab, setActiveTab, clearActiveAsyncKeys, isOnboarded } = useAppStore();

  // Keep route pathname in sync with activeTab in Zustand store and abort in-flight requests from prior tab
  useEffect(() => {
    // Abort all active controllers on tab switch
    abortRegistry.abortAll("tab-switch");
    clearActiveAsyncKeys?.();

    const rawPath = location.pathname.replace(/^\//, "").toLowerCase();
    const validTabs: NavTab[] = ["home", "learn", "explore", "grow", "portfolio"];
    if (validTabs.includes(rawPath as NavTab)) {
      setActiveTab(rawPath as NavTab);
    }
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
    <div className="min-h-screen bg-[var(--bg-primary)] text-[var(--text-main)] flex w-full transition-colors duration-200">
      {/* Full-screen Onboarding Overlay */}
      <AnimatePresence>
        {!isOnboarded && (
          <motion.div
            key="onboarding-overlay"
            initial={{ opacity: 1 }}
            exit={shouldReduceMotion ? { opacity: 0 } : { opacity: 0, scale: 0.98 }}
            transition={{ duration: 0.35, ease: "easeInOut" }}
            className="fixed inset-0 z-50 overflow-hidden bg-[var(--bg-primary)]"
          >
            <OnboardingHero />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Desktop Sidebar (visible on md: and up) */}
      {isOnboarded && <DesktopSidebar />}

      {/* Main Column: Header + Content + Mobile Bottom Nav */}
      <div className="flex-1 flex flex-col min-h-screen w-full min-w-0 relative">
        {/* Sticky Header - visible when onboarded */}
        {isOnboarded && <Header />}

        {/* Scrollable Content Area with responsive max-w */}
        <main
          className={`flex-1 overflow-y-auto content-bottom-safe md:pb-6 relative w-full ${
            !isOnboarded ? "invisible pointer-events-none" : ""
          }`}
          aria-hidden={!isOnboarded}
        >
          {/* Inner container: max-w-[520px] on mobile, expanding to max-w-7xl on desktop */}
          <div className="w-full max-w-[520px] md:max-w-7xl mx-auto min-h-full">
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
                <ErrorBoundary>
                  <Routes location={location}>
                    <Route path="/home" element={<HomePage />} />
                    <Route path="/learn" element={<LearnPage />} />
                    <Route path="/explore" element={<ExplorePage />} />
                    <Route path="/grow" element={<GrowPage />} />
                    <Route path="/portfolio" element={<PortfolioPage />} />
                    <Route path="*" element={<Navigate to="/home" replace />} />
                  </Routes>
                </ErrorBoundary>
              </motion.div>
            </AnimatePresence>
          </div>
        </main>

        {/* Fixed Bottom Navigation (mobile only: md:hidden) */}
        {isOnboarded && (
          <div className="md:hidden">
            <BottomNav activeTab={activeTab} onTabChange={setActiveTab} />
          </div>
        )}

        {/* Global Modals & Overlays Root */}
        {isOnboarded && <ModalRoot />}

        {/* iOS Safari Installation Guidance Banner */}
        {isOnboarded && <IOSInstallBanner />}
      </div>
    </div>
  );
}

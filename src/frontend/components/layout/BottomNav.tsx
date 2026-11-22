import type { ComponentType } from "react";
import { useNavigate } from "react-router-dom";
import { Home, Compass, GraduationCap, TrendingUp, PieChart } from "lucide-react";
import { motion } from "framer-motion";
import { NavTab } from "../../store/useAppStore";

interface BottomNavProps {
  activeTab: string;
  onTabChange?: (tab: NavTab) => void;
}

interface NavItem {
  id: NavTab;
  label: string;
  path: string;
  icon: ComponentType<{ className?: string }>;
}

const NAV_ITEMS: NavItem[] = [
  { id: "home", label: "Home", path: "/home", icon: Home },
  { id: "explore", label: "Explore", path: "/explore", icon: Compass },
  { id: "grow", label: "Grow", path: "/grow", icon: TrendingUp },
  { id: "portfolio", label: "Portfolio", path: "/portfolio", icon: PieChart },
  { id: "learn", label: "Learn", path: "/learn", icon: GraduationCap },
];

function triggerHaptic() {
  try {
    if (typeof navigator !== "undefined" && typeof navigator.vibrate === "function") {
      navigator.vibrate(12);
    }
  } catch {
    // Graceful no-op on non-supporting devices
  }
}

export function BottomNav({ activeTab, onTabChange }: BottomNavProps) {
  const navigate = useNavigate();

  const handleTabClick = (item: NavItem) => {
    triggerHaptic();
    onTabChange?.(item.id);
    navigate(item.path);
  };

  return (
    <nav
      role="tablist"
      aria-label="Main Navigation"
      className="fixed bottom-0 left-0 right-0 z-40 flex justify-center pointer-events-none"
    >
      <div className="w-full max-w-[520px] px-3 bottom-nav-safe pointer-events-auto">
        <div className="flex items-center justify-around py-1 px-1.5 rounded-2xl bg-[var(--bg-card)]/90 backdrop-blur-lg border border-[var(--border-subtle)] shadow-md transition-colors duration-200">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;

            return (
              <button
                key={item.id}
                role="tab"
                type="button"
                aria-selected={isActive}
                aria-label={item.label}
                onClick={() => handleTabClick(item)}
                className={`relative flex-1 flex flex-col items-center justify-center py-2 px-1 min-h-[48px] rounded-xl transition-colors duration-150 select-none group focus:outline-none focus-visible:ring-2 focus-visible:ring-teal-500 ${
                  isActive
                    ? "text-teal-700 dark:text-teal-400 font-semibold"
                    : "text-[var(--text-muted)] hover:text-[var(--text-main)]"
                }`}
              >
                {/* Active Sliding Pill Indicator via Framer Motion layoutId */}
                {isActive && (
                  <motion.div
                    layoutId="active-tab-indicator"
                    data-testid="active-tab-indicator"
                    className="absolute inset-0 bg-teal-500/10 border border-teal-500/20 rounded-xl -z-10 shadow-sm"
                    transition={{
                      type: "spring",
                      stiffness: 400,
                      damping: 30,
                    }}
                  />
                )}

                <Icon
                  className={`w-5 h-5 transition-transform duration-150 ${
                    isActive ? "scale-110" : "group-hover:scale-105"
                  }`}
                />
                <span className="text-xs tracking-normal mt-1 leading-none font-medium">
                  {item.label}
                </span>
              </button>
            );
          })}
        </div>
      </div>
    </nav>
  );
}

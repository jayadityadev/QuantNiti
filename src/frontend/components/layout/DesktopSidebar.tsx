import React from "react";
import { Link, useLocation } from "react-router-dom";
import {
  Compass,
  Briefcase,
  PieChart,
  Sparkles,
  Bell,
  Sun,
  Moon,
  Shield,
  Activity,
} from "lucide-react";
import { useAppStore, NavTab } from "../../store/useAppStore";
import { useTheme } from "../../context/ThemeContext";

interface DesktopSidebarProps {
  currentPath?: string;
}

interface NavItem {
  id: NavTab;
  label: string;
  path: string;
  icon: React.ComponentType<{ className?: string }>;
  description: string;
}

const DESKTOP_NAV_ITEMS: NavItem[] = [
  {
    id: "home",
    label: "Market Overview",
    path: "/home",
    icon: Compass,
    description: "Macro indicators and active regime",
  },
  {
    id: "explore",
    label: "Asset Universe",
    path: "/explore",
    icon: PieChart,
    description: "Multi-factor screens and analysis",
  },
  {
    id: "grow",
    label: "Grow Wizard",
    path: "/grow",
    icon: Sparkles,
    description: "HRP-driven target asset allocations",
  },
  {
    id: "portfolio",
    label: "Live Holdings",
    path: "/portfolio",
    icon: Briefcase,
    description: "Real-time tracking and rebalancing",
  },
];

export const DesktopSidebar: React.FC<DesktopSidebarProps> = ({
  currentPath = "",
}) => {
  const location = useLocation();
  const { theme, toggleTheme } = useTheme();
  const { openModal, activeTab, setActiveTab, activeRegime, riskPersona } = useAppStore();

  const regimeName = activeRegime?.current_regime || "Sideways / Range";

  return (
    <aside
      aria-label="Desktop Navigation"
      className="hidden md:flex flex-col w-64 lg:w-72 shrink-0 h-screen sticky top-0 bg-[var(--bg-card)]/80 backdrop-blur-xl border-r border-[var(--border-subtle)] select-none transition-colors duration-200"
    >
      {/* Brand Header */}
      <div className="h-16 shrink-0 flex items-center justify-between px-5 border-b border-[var(--border-subtle)]">
        <Link
          to="/home"
          onClick={() => setActiveTab("home")}
          className="flex items-center gap-3 group focus:outline-none focus-visible:ring-2 focus-visible:ring-teal-500 rounded-xl"
          aria-label="Terminal Home"
        >
          <div className="w-9 h-9 rounded-xl bg-slate-900 dark:bg-teal-700 p-1 shadow-sm group-hover:scale-105 transition-transform duration-200 flex items-center justify-center">
            <img src="/icon.svg" alt="Logo" className="w-full h-full rounded-[8px] object-cover" />
          </div>
          <div className="flex flex-col">
            <span className="font-bold text-base tracking-tight leading-none text-[var(--text-main)] group-hover:text-teal-600 transition-colors">
              QuantNiti
            </span>
            <span className="text-xs font-medium text-teal-600 dark:text-teal-400 mt-0.5">
              Portfolio intelligence
            </span>
          </div>
        </Link>
      </div>

      {/* Main Navigation Links */}
      <div className="flex-1 overflow-y-auto px-3.5 py-4 space-y-6">
        <nav aria-label="Primary" className="space-y-1">
          <div className="px-3 pb-1.5 text-xs font-medium text-[var(--text-muted)]">
            Intelligence suite
          </div>
          {DESKTOP_NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path || currentPath.includes(item.id) || activeTab === item.id;

            return (
              <Link
                key={item.id}
                to={item.path}
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-colors duration-150 group relative focus-visible:ring-2 focus-visible:ring-teal-500 focus-visible:outline-none ${
                  isActive
                    ? "bg-slate-900 text-white dark:bg-teal-600 dark:text-white shadow-sm font-semibold"
                    : "text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--bg-card-subtle)] border border-transparent"
                }`}
              >
                <div
                  className={`w-7 h-7 rounded-lg flex items-center justify-center transition-colors ${
                    isActive
                      ? "bg-white/20 text-white"
                      : "bg-[var(--bg-card-subtle)] text-[var(--text-muted)] group-hover:text-teal-600 group-hover:bg-teal-500/10"
                  }`}
                >
                  <Icon className="w-4 h-4" />
                </div>
                <div className="flex flex-col flex-1 min-w-0">
                  <span className="truncate leading-tight">{item.label}</span>
                  <span
                    className={`text-[10px] truncate transition-colors ${
                      isActive ? "text-slate-300 dark:text-teal-100" : "text-[var(--text-muted)] group-hover:text-[var(--text-main)]"
                    }`}
                  >
                    {item.description}
                  </span>
                </div>
              </Link>
            );
          })}
        </nav>

        {/* Live Market & Persona Context Card */}
        <div className="p-3.5 rounded-2xl bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)] space-y-2.5">
          <div className="flex items-center justify-between text-xs">
            <span className="font-medium text-[var(--text-muted)] flex items-center gap-1.5">
              <Activity className="w-3.5 h-3.5 text-teal-600" />
              Market regime
            </span>
            <span className="px-2 py-0.5 rounded-md bg-emerald-500/10 border border-emerald-500/20 text-emerald-700 dark:text-emerald-400 font-medium text-xs flex items-center gap-1">
              Live
            </span>
          </div>
          <div className="font-semibold text-xs text-[var(--text-main)]">
            {regimeName}
          </div>

          <div className="pt-1.5 border-t border-[var(--border-subtle)] flex items-center justify-between text-xs">
            <span className="font-medium text-[var(--text-muted)] flex items-center gap-1.5">
              <Shield className="w-3.5 h-3.5 text-slate-500" />
              Risk persona
            </span>
            <span className="font-semibold text-teal-700 dark:text-teal-400 text-xs">
              {riskPersona || "Balanced"}
            </span>
          </div>
        </div>

        {/* Quick AI & Alerts Launchers */}
        <div className="space-y-1.5">
          <button
            type="button"
            onClick={() => openModal("nitibot")}
            className="w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-medium text-[var(--text-main)] bg-teal-500/10 hover:bg-teal-500/15 border border-teal-500/20 transition-colors text-left group focus-visible:ring-2 focus-visible:ring-teal-500 focus-visible:outline-none"
          >
            <div className="w-6 h-6 rounded-lg bg-teal-600 text-white flex items-center justify-center shadow-sm">
              <Sparkles className="w-3.5 h-3.5" />
            </div>
            <div className="flex-1">
              <div className="font-semibold leading-none text-teal-800 dark:text-teal-200">Ask NitiBot</div>
              <div className="text-[10px] text-[var(--text-muted)] mt-0.5">RAG quant assistant</div>
            </div>
          </button>

          <button
            type="button"
            onClick={() => openModal("notifications")}
            className="w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-medium text-[var(--text-main)] hover:bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)] transition-colors text-left focus-visible:ring-2 focus-visible:ring-teal-500 focus-visible:outline-none"
          >
            <Bell className="w-4 h-4 text-teal-600" />
            <span className="flex-1">Notification center</span>
          </button>
        </div>
      </div>

      {/* Sidebar Footer: Theme Toggle & Info */}
      <div className="p-3.5 border-t border-[var(--border-subtle)] flex items-center justify-between">
        <button
          type="button"
          onClick={toggleTheme}
          aria-label={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
          className="flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-medium text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--bg-card-subtle)] border border-[var(--border-subtle)] transition-colors focus-visible:ring-2 focus-visible:ring-teal-500 focus-visible:outline-none"
        >
          {theme === "dark" ? (
            <>
              <Sun className="w-3.5 h-3.5 text-amber-400" />
              <span>Light Mode</span>
            </>
          ) : (
            <>
              <Moon className="w-3.5 h-3.5 text-slate-600" />
              <span>Dark Mode</span>
            </>
          )}
        </button>

        <span className="text-xs text-[var(--text-muted)] font-mono">
          v0.2.0
        </span>
      </div>
    </aside>
  );
};

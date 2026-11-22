import { useState, useRef, useEffect } from "react";
import { Link } from "react-router-dom";
import { Sun, Moon, Bell, MoreVertical, Layers, Download, Maximize2 } from "lucide-react";
import { useTheme } from "../../context/ThemeContext";
import { useAppStore } from "../../store/useAppStore";
import { AnimatePresence, motion } from "framer-motion";
import { promptPWAInstall } from "../../services/pwaService";

interface HeaderProps {
  onCompareClick?: () => void;
  onInstallClick?: () => void;
  onViewportToggle?: () => void;
}

export function Header({
  onCompareClick,
  onInstallClick,
  onViewportToggle,
}: HeaderProps) {
  const { theme, toggleTheme } = useTheme();
  const { activeRegime, openModal } = useAppStore();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  // Close overflow menu on outside click or Esc key
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsMenuOpen(false);
      }
    }
    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") {
        setIsMenuOpen(false);
      }
    }
    if (isMenuOpen) {
      document.addEventListener("mousedown", handleClickOutside);
      document.addEventListener("keydown", handleKeyDown);
    }
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [isMenuOpen]);

  // Regime display determination
  const regimeLabel = activeRegime?.regime || activeRegime?.name || "Bull market";

  return (
    <header className="sticky top-0 z-40 w-full bg-[var(--bg-primary)]/80 backdrop-blur-md border-b border-[var(--border-subtle)] px-4 py-2.5 transition-colors duration-200">
      <div className="flex items-center justify-between gap-2">
        {/* Brand Badge (Clickable -> Home) */}
        <Link
          to="/home"
          className="flex items-center gap-2.5 group focus:outline-none focus-visible:ring-2 focus-visible:ring-teal-500 rounded-xl"
          aria-label="QuantNiti Home"
        >
          <img src="/icon.svg" alt="QuantNiti Logo" className="w-8 h-8 rounded-xl shadow-sm group-hover:scale-105 transition-transform duration-150 object-cover" />
          <div className="flex flex-col">
            <span className="font-bold text-sm tracking-tight leading-none text-[var(--text-main)] group-hover:text-teal-600 transition-colors">
              QuantNiti
            </span>
            <span className="text-xs text-teal-600 dark:text-teal-400 font-medium mt-0.5">
              Intelligence
            </span>
          </div>
        </Link>

        {/* Center/Right Actions */}
        <div className="flex items-center gap-1.5 sm:gap-2">
          {/* Market Regime Pill */}
          <div
            data-testid="regime-pill-badge"
            className="flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-emerald-500/10 border border-emerald-500/20 text-emerald-700 dark:text-emerald-400 text-xs font-medium tracking-tight shadow-sm"
            title={`Active Market Regime: ${regimeLabel}`}
          >
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
            <span className="truncate max-w-[90px] sm:max-w-[120px]">{regimeLabel}</span>
          </div>

          {/* Notification Bell */}
          <button
            data-testid="notification-bell-btn"
            type="button"
            onClick={() => openModal("notifications")}
            className="relative p-2 rounded-xl text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--bg-card)] focus:outline-none focus-visible:ring-2 focus-visible:ring-teal-500 transition-colors duration-150"
            aria-label="Notifications"
            title="Notifications"
          >
            <Bell className="w-4 h-4" />
            <span
              data-testid="notification-unread-dot"
              className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-teal-600 ring-2 ring-[var(--bg-primary)]"
            />
          </button>

          {/* Theme Toggle */}
          <button
            data-testid="theme-toggle-btn"
            type="button"
            onClick={toggleTheme}
            className="p-2 rounded-xl text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--bg-card)] focus:outline-none focus-visible:ring-2 focus-visible:ring-teal-500 transition-colors duration-150"
            aria-label="Toggle Theme"
            title={theme === "light" ? "Switch to Dark Mode" : "Switch to Light Mode"}
          >
            {theme === "light" ? <Moon className="w-4 h-4" /> : <Sun className="w-4 h-4 text-amber-400" />}
          </button>

          {/* Overflow Menu Anchor */}
          <div className="relative" ref={menuRef}>
            <button
              data-testid="overflow-menu-btn"
              type="button"
              onClick={() => setIsMenuOpen((prev) => !prev)}
              className="p-2 rounded-xl text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--bg-card)] focus:outline-none focus-visible:ring-2 focus-visible:ring-teal-500 transition-colors duration-150"
              aria-label="More options"
              aria-haspopup="menu"
              aria-expanded={isMenuOpen}
              title="More Options"
            >
              <MoreVertical className="w-4 h-4" />
            </button>

            {/* Overflow Dropdown Menu */}
            <AnimatePresence>
              {isMenuOpen && (
                <motion.div
                  role="menu"
                  aria-orientation="vertical"
                  initial={{ opacity: 0, scale: 0.95, y: -4 }}
                  animate={{ opacity: 1, scale: 1, y: 0 }}
                  exit={{ opacity: 0, scale: 0.95, y: -4 }}
                  transition={{ duration: 0.15 }}
                  className="absolute right-0 mt-2 w-52 rounded-xl bg-[var(--bg-card)] border border-[var(--border-subtle)] shadow-xl py-1.5 z-50 text-xs font-medium"
                >
                  <button
                    type="button"
                    role="menuitem"
                    onClick={() => {
                      setIsMenuOpen(false);
                      if (onCompareClick) onCompareClick();
                      else openModal("competitors");
                    }}
                    className="w-full flex items-center gap-2.5 px-3.5 py-2.5 text-left text-[var(--text-main)] hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                  >
                    <Layers className="w-4 h-4 text-teal-600" />
                    <span>Compare vs competitors</span>
                  </button>

                  <button
                    data-testid="pwa-install-btn"
                    id="pwaInstallBtn"
                    type="button"
                    role="menuitem"
                    onClick={() => {
                      setIsMenuOpen(false);
                      if (onInstallClick) {
                        onInstallClick();
                      } else {
                        promptPWAInstall();
                      }
                    }}
                    className="w-full flex items-center gap-2.5 px-3.5 py-2.5 text-left text-[var(--text-main)] hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                  >
                    <Download className="w-4 h-4 text-teal-600" />
                    <span>Install PWA</span>
                  </button>

                  <button
                    type="button"
                    role="menuitem"
                    onClick={() => {
                      setIsMenuOpen(false);
                      onViewportToggle?.();
                    }}
                    className="w-full flex items-center gap-2.5 px-3.5 py-2.5 text-left text-[var(--text-main)] hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                  >
                    <Maximize2 className="w-4 h-4 text-teal-600" />
                    <span>Toggle viewport</span>
                  </button>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </header>
  );
}

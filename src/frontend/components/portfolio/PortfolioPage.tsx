import React, { useState, useEffect } from "react";
import { Plus, Trash2, Check } from "lucide-react";
import { useAppStore } from "../../store/useAppStore";
import { useAbortableRequest } from "../../hooks/useAbortableRequest";
import { DemoPortfolio } from "./DemoPortfolio";
import { PortfolioHeroCard } from "./PortfolioHeroCard";
import { HoldingsTable } from "./HoldingsTable";
import { RebalanceBanner } from "./RebalanceBanner";
import { CompoundingTrajectoryChart } from "./CompoundingTrajectoryChart";
import { CreatePortfolioModal } from "./CreatePortfolioModal";
import { PrimaryButton } from "../ui/PrimaryButton";
import { apiUrl } from "../../config";
import {
  PortfolioData,
  CompoundingTrajectoryData,
  getDemoCompoundingTrajectory,
} from "./demoPortfolioData";

export const PortfolioPage: React.FC = () => {
  const {
    portfolios,
    activePortfolioId,
    setActivePortfolioId,
    setPortfolios,
    setActiveTab,
    riskPersona,
  } = useAppStore();

  const { request } = useAbortableRequest();

  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isRebalancing, setIsRebalancing] = useState(false);
  const [trajectoryData, setTrajectoryData] = useState<CompoundingTrajectoryData | null>(null);

  // Load existing real portfolios from backend if empty in memory
  useEffect(() => {
    fetch(apiUrl("/api/v1/portfolios"))
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) {
          setPortfolios(data);
          if (!activePortfolioId) {
            setActivePortfolioId(data[0].portfolio_id);
          }
        }
      })
      .catch(() => {});
  }, []);

  // Determine active portfolio
  const activePortfolio =
    portfolios.find((p) => p.portfolio_id === activePortfolioId) ||
    portfolios[0] ||
    null;

  // Fetch compounding projection when active portfolio changes
  useEffect(() => {
    if (!activePortfolio) {
      setTrajectoryData(null);
      return;
    }

    let isMounted = true;

    async function loadTrajectory() {
      try {
        const response = await request(
          "portfolio-compounding",
          apiUrl("/api/portfolio/compounding"),
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              portfolio_id: activePortfolio.portfolio_id,
              initial_lump_sum: activePortfolio.current_value,
              tenure_years: 10,
            }),
          }
        );

        if (isMounted && response?.yearly_trajectories) {
          setTrajectoryData(response);
          return;
        }
      } catch {
        // Fallback gracefully to local calculation if API is unavailable
      }

      if (isMounted) {
        setTrajectoryData(getDemoCompoundingTrajectory(activePortfolio.current_value));
      }
    }

    loadTrajectory();

    return () => {
      isMounted = false;
    };
  }, [activePortfolio?.portfolio_id, activePortfolio?.current_value]);

  // Handle portfolio creation (persisted to the backend so it survives reloads)
  const handleCreatePortfolio = async (data: {
    name: string;
    capital: number;
    riskPersona: any;
  }) => {
    try {
      const created = await request<PortfolioData>(
        "create-portfolio",
        apiUrl("/api/v1/portfolios"),
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            name: data.name,
            capital: data.capital,
            horizon: "6M",
            risk_persona: data.riskPersona || riskPersona,
          }),
        }
      );

      if (!created?.portfolio_id) {
        throw new Error("The server did not return a valid portfolio.");
      }

      setPortfolios([
        created,
        ...portfolios.filter((p) => p.portfolio_id !== created.portfolio_id),
      ]);
      setActivePortfolioId(created.portfolio_id);
    } catch (err: any) {
      window.alert(err?.message || "Failed to create portfolio. Please try again.");
    }
  };

  // Handle portfolio deletion (persisted to the backend)
  const handleDeleteActivePortfolio = async () => {
    if (!activePortfolio) return;
    const confirmDelete = window.confirm(
      `Are you sure you want to delete "${activePortfolio.name}"? This action cannot be undone.`
    );
    if (!confirmDelete) return;

    try {
      await request(
        "delete-portfolio",
        apiUrl(`/api/v1/portfolios/${encodeURIComponent(activePortfolio.portfolio_id)}`),
        { method: "DELETE" }
      );

      const remaining = portfolios.filter(
        (p) => p.portfolio_id !== activePortfolio.portfolio_id
      );
      setPortfolios(remaining);
      setActivePortfolioId(remaining.length > 0 ? remaining[0].portfolio_id : null);
    } catch (err: any) {
      window.alert(err?.message || "Failed to delete portfolio. Please try again.");
    }
  };

  // Handle regime-shift rebalance (applies server-side and refreshes holdings)
  const handleApplyRebalance = async () => {
    if (!activePortfolio) return;
    setIsRebalancing(true);
    try {
      const updated = await request<PortfolioData>(
        "apply-rebalance",
        apiUrl(
          `/api/v1/portfolio/${encodeURIComponent(activePortfolio.portfolio_id)}/rebalance/apply`
        ),
        { method: "POST" }
      );

      if (updated?.portfolio_id) {
        setPortfolios(
          portfolios.map((p) =>
            p.portfolio_id === updated.portfolio_id ? updated : p
          )
        );
      }
    } catch (err: any) {
      window.alert(err?.message || "Failed to apply rebalance. Please try again.");
    } finally {
      setIsRebalancing(false);
    }
  };

  // If no portfolios exist in state, render Demo state
  const hasRealPortfolios = portfolios && portfolios.length > 0;

  return (
    <div className="flex flex-col min-h-full pb-20 p-4 space-y-4">
      {/* Top Header bar */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl sm:text-2xl font-black text-[var(--text-main)] tracking-tight">
            Portfolio Page
          </h1>
          <p className="text-xs text-[var(--text-muted)]">
            {hasRealPortfolios
              ? "Live Mark-To-Market and Compounding Engine"
              : "Explore simulated paper portfolios & compounding"}
          </p>
        </div>

        {/* Action buttons */}
        <div className="flex items-center gap-2">
          {hasRealPortfolios && (
            <button
              type="button"
              onClick={handleDeleteActivePortfolio}
              className="p-2 rounded-xl text-rose-400 hover:bg-rose-500/10 transition-colors border border-rose-500/20 text-xs flex items-center gap-1"
              title="Delete Portfolio"
              aria-label="Delete Portfolio"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          )}

          <PrimaryButton
            onClick={() => setIsCreateModalOpen(true)}
            icon={<Plus className="w-3.5 h-3.5" />}
            className="text-xs py-2 px-3"
          >
            New Goal
          </PrimaryButton>
        </div>
      </div>

      {/* Multi-Portfolio Dropdown / Selector (Real State only) */}
      {hasRealPortfolios && (
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1">
          {portfolios.map((p) => {
            const isSelected = p.portfolio_id === activePortfolio?.portfolio_id;
            return (
              <button
                key={p.portfolio_id}
                type="button"
                onClick={() => setActivePortfolioId(p.portfolio_id)}
                className={`px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-colors flex items-center gap-1.5 ${
                  isSelected
                    ? "bg-violet-600 text-white shadow-md shadow-violet-950/30"
                    : "bg-[var(--bg-card-subtle)] text-[var(--text-muted)] hover:text-[var(--text-main)] border border-[var(--border-subtle)]"
                }`}
              >
                {isSelected && <Check className="w-3 h-3 text-white" />}
                <span>{p.name}</span>
              </button>
            );
          })}
        </div>
      )}

      {/* Main Content Area */}
      {!hasRealPortfolios ? (
        <DemoPortfolio onNavigateToGrow={() => setActiveTab("grow")} />
      ) : (
        <div className="space-y-4">
          {/* Rebalance Banner if triggered */}
          {activePortfolio?.rebalance_alert?.is_rebalance_recommended && (
            <RebalanceBanner
              portfolioId={activePortfolio.portfolio_id}
              isRebalanceRecommended={true}
              triggerReason={activePortfolio.rebalance_alert.trigger_reason}
              onApplyRebalance={handleApplyRebalance}
              isApplying={isRebalancing}
            />
          )}

          {/* Hero Metric Card */}
          <PortfolioHeroCard portfolio={activePortfolio} isDemo={false} />

          {/* Holdings Table */}
          <HoldingsTable holdings={activePortfolio.holdings} isDemo={false} />

          {/* 10-Year Compounding Wealth Trajectory */}
          {trajectoryData && (
            <CompoundingTrajectoryChart trajectory={trajectoryData} isDemo={false} />
          )}
        </div>
      )}

      {/* Goal / Virtual Portfolio Creation Modal */}
      <CreatePortfolioModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        onCreate={handleCreatePortfolio}
        onOpenGrowWizard={() => setActiveTab("grow")}
      />
    </div>
  );
};

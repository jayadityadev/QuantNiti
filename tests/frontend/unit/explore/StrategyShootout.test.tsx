import React from "react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { StrategyShootout } from "../../../../src/frontend/components/explore/StrategyShootout";

describe("StrategyShootout Component Seam", () => {
  const mockShootoutData = {
    shootout_id: "shootout_test_1",
    symbol: "RELIANCE",
    name: "Reliance Industries",
    initial_capital: 100000,
    active_regime: "Low-Volatility Bull",
    strategies: [
      {
        id: "run_a",
        name: "Run A: Passive Buy & Hold NIFTY 50",
        strategy_type: "BUY_AND_HOLD",
        color: "#94A3B8",
        cagr: 14.2,
        sharpe_ratio: 1.15,
        sortino_ratio: 1.62,
        max_drawdown_pct: -18.4,
        calmar_ratio: 0.77,
        win_rate_pct: 54,
        total_return_pct: 32.5,
        final_equity: 132500,
        best_in_class: { cagr: false, sharpe_ratio: false, sortino_ratio: false, max_drawdown: false, calmar_ratio: false, win_rate: false },
      },
      {
        id: "run_b",
        name: "Run B: Regime-Adaptive Dynamic Basket",
        strategy_type: "DUAL_MOMENTUM",
        color: "#14B8A6",
        cagr: 22.8,
        sharpe_ratio: 1.84,
        sortino_ratio: 2.45,
        max_drawdown_pct: -9.2,
        calmar_ratio: 2.48,
        win_rate_pct: 71,
        total_return_pct: 54.2,
        final_equity: 154200,
        best_in_class: { cagr: true, sharpe_ratio: true, sortino_ratio: true, max_drawdown: false, calmar_ratio: true, win_rate: true },
      },
      {
        id: "run_c",
        name: "Run C: Hierarchical Risk Parity (HRP)",
        strategy_type: "MA_CROSSOVER",
        color: "#8B5CF6",
        cagr: 17.5,
        sharpe_ratio: 1.55,
        sortino_ratio: 2.1,
        max_drawdown_pct: -7.8,
        calmar_ratio: 2.24,
        win_rate_pct: 64,
        total_return_pct: 40.1,
        final_equity: 140100,
        best_in_class: { cagr: false, sharpe_ratio: false, sortino_ratio: false, max_drawdown: true, calmar_ratio: false, win_rate: false },
      },
      {
        id: "run_d",
        name: "Run D: Equal Weight 60/40",
        strategy_type: "BOLLINGER_BANDS",
        color: "#F59E0B",
        cagr: 12.1,
        sharpe_ratio: 1.1,
        sortino_ratio: 1.45,
        max_drawdown_pct: -8.1,
        calmar_ratio: 1.49,
        win_rate_pct: 58,
        total_return_pct: 26.8,
        final_equity: 126800,
        best_in_class: { cagr: false, sharpe_ratio: false, sortino_ratio: false, max_drawdown: false, calmar_ratio: false, win_rate: false },
      },
    ],
    normalized_curves: [
      { date: "2025-01-01", run_a: 100.0, run_b: 100.0, run_c: 100.0, run_d: 100.0 },
      { date: "2025-01-15", run_a: 102.1, run_b: 104.5, run_c: 103.2, run_d: 101.4 },
      { date: "2025-02-01", run_a: 105.4, run_b: 110.2, run_c: 107.1, run_d: 103.8 },
    ],
  };

  beforeEach(() => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => mockShootoutData,
      })
    );
  });

  it("renders multi-strategy comparison header and active runs selector", async () => {
    render(<StrategyShootout symbol="RELIANCE" />);

    expect(await screen.findByText(/Multi-Strategy Shootout/i)).toBeInTheDocument();
    expect(screen.getAllByText(/Run A: Passive Buy & Hold NIFTY 50/i).length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText(/Run B: Regime-Adaptive Dynamic Basket/i).length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText(/Run C: Hierarchical Risk Parity \(HRP\)/i).length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText(/Run D: Equal Weight 60\/40/i).length).toBeGreaterThanOrEqual(1);
  });

  it("renders comparative financial metrics matrix with best-in-class highlights", async () => {
    render(<StrategyShootout symbol="RELIANCE" />);

    expect(await screen.findByText(/Comparative Metrics Matrix/i)).toBeInTheDocument();
    expect(screen.getByText("CAGR")).toBeInTheDocument();
    expect(screen.getByText("Sharpe")).toBeInTheDocument();
    expect(screen.getByText("Sortino")).toBeInTheDocument();
    expect(screen.getByText("Max DD")).toBeInTheDocument();
    expect(screen.getByText("Calmar")).toBeInTheDocument();
    expect(screen.getByText("Win Rate")).toBeInTheDocument();

    // Check Run B top CAGR +22.8%
    expect(screen.getByText("+22.8%")).toBeInTheDocument();
  });

  it("toggles runs and prevents disabling below 2 strategies", async () => {
    const user = userEvent.setup();
    render(<StrategyShootout symbol="RELIANCE" />);

    const runAButton = await screen.findByRole("button", { name: /Run A: Passive/i });
    const runBButton = screen.getByRole("button", { name: /Run B: Regime/i });

    // Turn off run_a (3 remain active)
    await user.click(runAButton);
    expect(runAButton).toHaveClass("opacity-40");

    // Turn off run_b (2 remain active)
    await user.click(runBButton);
    expect(runBButton).toHaveClass("opacity-40");

    // Attempting to turn off third run should be rejected (keeps min 2)
    const runCButton = screen.getByRole("button", { name: /Run C: Hierarchical/i });
    await user.click(runCButton);
    expect(runCButton).not.toHaveClass("opacity-40");
  });
});

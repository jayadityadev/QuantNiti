import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import {
  RiskProvenanceStatStrip,
  RiskProvenanceMetrics,
} from "../../../src/frontend/components/portfolio/RiskProvenanceStatStrip";
import { DEMO_HOLDINGS } from "../../../src/frontend/components/portfolio/demoPortfolioData";
import { HoldingsTable } from "../../../src/frontend/components/portfolio/HoldingsTable";

describe("RiskProvenanceStatStrip", () => {
  it("renders demo mode metrics with Belltalon high-density stats", () => {
    const demoMetrics: Partial<RiskProvenanceMetrics> = {
      syncStatus: "Synced 15:30 IST",
      isLive: false,
      sourceTag: "NSE/BSE EOD + Tick Engine",
      beta: 0.88,
      var1d: -1.42,
      maxSectorConcentration: {
        sector: "Financials",
        weightPct: 31.5,
      },
      targetDriftPct: 1.2,
      targetDriftStatus: "in_bounds",
    };

    render(
      <RiskProvenanceStatStrip
        metrics={demoMetrics}
        holdings={DEMO_HOLDINGS}
        isDemo={true}
      />
    );

    // Provenance
    expect(screen.getByText("Synced 15:30 IST")).toBeInTheDocument();
    expect(screen.getByText("NSE/BSE EOD + Tick Engine")).toBeInTheDocument();

    // Risk exposure metrics
    expect(screen.getByText(/Beta \(vs NIFTY 50\):/i)).toBeInTheDocument();
    expect(screen.getByText("0.88")).toBeInTheDocument();

    expect(screen.getByText(/1D VaR \(95% Parametric\):/i)).toBeInTheDocument();
    expect(screen.getByText("-1.42%")).toBeInTheDocument();

    expect(screen.getByText(/Max Sector Concentration:/i)).toBeInTheDocument();
    expect(screen.getByText("31.5%")).toBeInTheDocument();
    expect(screen.getByText("Financials")).toBeInTheDocument();

    expect(screen.getByText(/Target Drift:/i)).toBeInTheDocument();
    expect(screen.getByText("±1.2%")).toBeInTheDocument();
    expect(screen.getByText("in bounds")).toBeInTheDocument();
  });

  it("renders live feed pulse indicator and actual metrics when live", () => {
    render(<RiskProvenanceStatStrip isDemo={false} holdings={DEMO_HOLDINGS} />);

    expect(screen.getByText("Live NSE Feed")).toBeInTheDocument();
    expect(screen.getByText("NSE/BSE EOD + Tick Engine")).toBeInTheDocument();
    expect(screen.getByText(/Beta \(vs NIFTY 50\):/i)).toBeInTheDocument();
    expect(screen.getByText(/1D VaR \(95% Parametric\):/i)).toBeInTheDocument();
    expect(screen.getByText(/Max Sector Concentration:/i)).toBeInTheDocument();
    expect(screen.getByText(/Target Drift:/i)).toBeInTheDocument();
  });

  it("dynamically calculates top sector concentration from holdings if metrics are omitted", () => {
    // In DEMO_HOLDINGS: IT has TCS (0.23) + INFY (0.12) = 35.0%
    render(<RiskProvenanceStatStrip holdings={DEMO_HOLDINGS} isDemo={false} />);

    expect(screen.getByText("35.0%")).toBeInTheDocument();
    expect(screen.getByText("Information Technology")).toBeInTheDocument();
  });

  it("reflects warning and breach drift states accurately", () => {
    const { rerender } = render(
      <RiskProvenanceStatStrip
        metrics={{ targetDriftPct: 4.1 }}
        isDemo={false}
      />
    );
    expect(screen.getByText("±4.1%")).toBeInTheDocument();
    expect(screen.getByText("drift warning")).toBeInTheDocument();

    rerender(
      <RiskProvenanceStatStrip
        metrics={{ targetDriftPct: 6.5 }}
        isDemo={false}
      />
    );
    expect(screen.getByText("±6.5%")).toBeInTheDocument();
    expect(screen.getByText("rebalance req.")).toBeInTheDocument();
  });

  it("provides proper accessibility attributes", () => {
    render(<RiskProvenanceStatStrip isDemo={true} />);

    const region = screen.getByRole("region", {
      name: /portfolio risk exposure and data provenance/i,
    });
    expect(region).toBeInTheDocument();
  });

  it("integrates seamlessly into HoldingsTable above holdings rows", () => {
    render(<HoldingsTable holdings={DEMO_HOLDINGS} isDemo={true} />);

    // Stat strip is present inside HoldingsTable
    const region = screen.getByRole("region", {
      name: /portfolio risk exposure and data provenance/i,
    });
    expect(region).toBeInTheDocument();
    expect(screen.getByText(/Beta \(vs NIFTY 50\):/i)).toBeInTheDocument();
  });
});

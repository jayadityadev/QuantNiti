import { describe, it, expect } from "vitest";
import {
  calculateIndianStatutoryFriction,
  getSlippageBpsForTier,
} from "../../../../src/frontend/utils/friction";

describe("Indian Statutory Friction Engine", () => {
  it("resolves correct slippage BPS per asset liquidity tier", () => {
    expect(getSlippageBpsForTier("large")).toBe(5.0);
    expect(getSlippageBpsForTier("nifty50")).toBe(5.0);
    expect(getSlippageBpsForTier("mid")).toBe(7.5);
    expect(getSlippageBpsForTier("small")).toBe(10.0);
  });

  it("calculates exact statutory friction for a BUY order", () => {
    // BUY 100 shares @ Rs 2500 = Turnover Rs 250,000
    const res = calculateIndianStatutoryFriction([
      { symbol: "RELIANCE", action: "BUY", shares: 100, price: 2500, liquidityTier: "large" },
    ]);

    expect(res.totalTurnover).toBe(250000);
    expect(res.buyTurnover).toBe(250000);
    expect(res.sellTurnover).toBe(0);

    // STT: 0.1% = 250
    expect(res.stt).toBe(250);

    // Exchange charges: 0.00325% = 8.13
    expect(res.exchangeCharges).toBe(8.13);

    // SEBI fee: Rs 10 per crore = 0.25
    expect(res.sebiFee).toBe(0.25);

    // Stamp duty: 0.015% = 37.5
    expect(res.stampDuty).toBe(37.5);

    // GST: 18% of (8.125 + 0.25) = 1.51
    expect(res.gst).toBe(1.51);

    // Slippage: 5 bps = 125
    expect(res.slippage).toBe(125);

    // Total friction sum ~ 422.39
    expect(res.totalFriction).toBeCloseTo(422.39, 1);
    expect(res.frictionSummary).toContain("Est. Friction: ₹422");
    expect(res.frictionSummary).toContain("STT: ₹250");
    expect(res.frictionSummary).toContain("Stamp Duty: ₹38");
    expect(res.frictionSummary).toContain("GST: ₹2");
    expect(res.frictionSummary).toContain("Slippage: ₹125");
  });

  it("handles SELL orders with zero stamp duty", () => {
    const res = calculateIndianStatutoryFriction([
      { symbol: "TCS", action: "SELL", shares: 10, price: 4000, liquidityTier: "large" },
    ]);

    expect(res.stampDuty).toBe(0);
    expect(res.stt).toBe(40);
  });
});

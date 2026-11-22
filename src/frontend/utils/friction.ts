/**
 * Pre-Trade Indian Statutory Friction and Transaction Cost Engine.
 *
 * Statutory Indian Market Rates (NSE Equity Delivery):
 * - Securities Transaction Tax (STT): 0.1% on delivery buy/sell turnover (0.0010)
 * - NSE Exchange Turnover Charges: 0.00325% on turnover (0.0000325)
 * - SEBI Turnover Fee: ₹10 per crore = 0.0001% (0.000001 fraction)
 * - Stamp Duty: 0.015% (0.00015) on BUY transactions only
 * - GST: 18% on exchange charges + SEBI fee + brokerage
 * - Estimated Impact / Slippage: 5-10 bps based on asset liquidity tier
 */

export interface OrderInput {
  symbol: string;
  action: "BUY" | "SELL" | string;
  shares: number;
  price: number;
  liquidityTier?: "large" | "mid" | "small" | string;
  slippageBps?: number;
}

export interface StatutoryFrictionBreakdown {
  totalTurnover: number;
  buyTurnover: number;
  sellTurnover: number;
  stt: number;
  exchangeCharges: number;
  sebiFee: number;
  stampDuty: number;
  gst: number;
  slippage: number;
  brokerage: number;
  totalFriction: number;
  frictionBps: number;
  frictionSummary: string;
}

export function getSlippageBpsForTier(tier?: string): number {
  const t = (tier || "large").toLowerCase();
  if (t === "large" || t === "largecap" || t === "nifty50" || t === "index") {
    return 5.0; // 5 bps
  } else if (t === "mid" || t === "midcap") {
    return 7.5; // 7.5 bps
  } else if (t === "small" || t === "smallcap" || t === "micro") {
    return 10.0; // 10 bps
  }
  return 5.0;
}

export function calculateIndianStatutoryFriction(
  orders: OrderInput[],
  brokeragePerOrder = 0.0,
  defaultSlippageBps = 5.0
): StatutoryFrictionBreakdown {
  let buyTurnover = 0;
  let sellTurnover = 0;
  let totalSlippage = 0;

  for (const o of orders) {
    const qty = Math.abs(o.shares || 0);
    const px = Math.max(0, o.price || 0);
    const val = qty * px;
    const act = (o.action || "BUY").toUpperCase();

    if (act === "BUY") {
      buyTurnover += val;
    } else {
      sellTurnover += val;
    }

    const bps =
      o.slippageBps !== undefined
        ? o.slippageBps
        : getSlippageBpsForTier(o.liquidityTier || "large");
    const effectiveBps = bps !== undefined ? bps : defaultSlippageBps;
    totalSlippage += val * (effectiveBps / 10000.0);
  }

  const totalTurnover = buyTurnover + sellTurnover;

  if (totalTurnover <= 0) {
    return {
      totalTurnover: 0,
      buyTurnover: 0,
      sellTurnover: 0,
      stt: 0,
      exchangeCharges: 0,
      sebiFee: 0,
      stampDuty: 0,
      gst: 0,
      slippage: 0,
      brokerage: 0,
      totalFriction: 0,
      frictionBps: 0,
      frictionSummary: "Est. Friction: ₹0 — STT: ₹0, Stamp Duty: ₹0, GST: ₹0, Slippage: ₹0",
    };
  }

  // 1. STT: 0.1% on delivery buy and sell
  const stt = totalTurnover * 0.001;

  // 2. NSE Exchange Turnover Charges: 0.00325%
  const exchangeCharges = totalTurnover * 0.0000325;

  // 3. SEBI Turnover Fee: ₹10 per crore = 0.0001% = 0.000001 fraction
  const sebiFee = totalTurnover * 0.000001;

  // 4. Stamp Duty: 0.015% on BUY orders only
  const stampDuty = buyTurnover * 0.00015;

  // 5. Brokerage
  const totalBrokerage = orders.length * brokeragePerOrder;

  // 6. GST: 18% on exchange charges + SEBI fee + brokerage
  const taxableServices = exchangeCharges + sebiFee + totalBrokerage;
  const gst = taxableServices * 0.18;

  // Total friction
  const totalFriction =
    stt + exchangeCharges + sebiFee + stampDuty + gst + totalSlippage + totalBrokerage;
  const frictionBps = totalTurnover > 0 ? (totalFriction / totalTurnover) * 10000.0 : 0;

  // Format: Est. Friction: ₹48 — STT: ₹25, Stamp Duty: ₹8, GST: ₹7, Slippage: ₹8
  const summary = `Est. Friction: ₹${Math.round(totalFriction).toLocaleString("en-IN")} — STT: ₹${Math.round(
    stt
  ).toLocaleString("en-IN")}, Stamp Duty: ₹${Math.round(stampDuty).toLocaleString("en-IN")}, GST: ₹${Math.round(
    gst
  ).toLocaleString("en-IN")}, Slippage: ₹${Math.round(totalSlippage).toLocaleString("en-IN")}`;

  return {
    totalTurnover: Number(totalTurnover.toFixed(2)),
    buyTurnover: Number(buyTurnover.toFixed(2)),
    sellTurnover: Number(sellTurnover.toFixed(2)),
    stt: Number(stt.toFixed(2)),
    exchangeCharges: Number(exchangeCharges.toFixed(2)),
    sebiFee: Number(sebiFee.toFixed(2)),
    stampDuty: Number(stampDuty.toFixed(2)),
    gst: Number(gst.toFixed(2)),
    slippage: Number(totalSlippage.toFixed(2)),
    brokerage: Number(totalBrokerage.toFixed(2)),
    totalFriction: Number(totalFriction.toFixed(2)),
    frictionBps: Number(frictionBps.toFixed(2)),
    frictionSummary: summary,
  };
}

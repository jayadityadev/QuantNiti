export interface PortfolioHoldingItem {
  symbol: string;
  name: string;
  sector: string;
  shares: number;
  buy_price: number;
  avg_price?: number;
  current_price: number;
  invested_amount: number;
  current_value: number;
  unrealized_pnl: number;
  unrealized_pnl_pct: number;
  pnl?: number;
  pnl_pct?: number;
  weight: number;
  target_weight?: number;
  prev_close_price?: number;
  pnl_1d: number;
  pnl_1d_pct: number;
  day_change_pct?: number;
  regime_suitability?: string;
}

export interface BenchmarkComparison {
  portfolio_return_pct: number;
  nifty_return_pct: number;
  bank_fd_return_pct: number;
  alpha_vs_nifty: number;
  alpha_vs_fd: number;
}

export interface PortfolioData {
  portfolio_id: string;
  name: string;
  initial_capital: number;
  cash: number;
  invested_capital: number;
  current_value: number;
  total_pnl: number;
  total_pnl_pct: number;
  pnl_1d: number;
  pnl_1d_pct: number;
  max_drawdown_pct: number;
  holdings: PortfolioHoldingItem[];
  benchmark_comparison: BenchmarkComparison;
  initial_regime: string;
  current_regime: string;
  risk_persona: string;
  horizon: string;
  created_at: string;
  as_of_date: string;
  is_demo?: boolean;
  alpha?: number;
  beta?: number;
  var_1d_pct?: number;
  target_drift_pct?: number;
  risk_metrics?: {
    syncStatus?: string;
    isLive?: boolean;
    sourceTag?: string;
    beta?: number;
    var1d?: number;
    maxSectorConcentration?: {
      sector: string;
      weightPct: number;
    };
    targetDriftPct?: number;
    targetDriftStatus?: "in_bounds" | "warning" | "breached";
  };
}

export type PortfolioHolding = PortfolioHoldingItem;
export type Portfolio = PortfolioData;

export interface CompoundingYearlyPoint {
  year: number;
  invested_lump_sum: number;
  value_lump_sum: number;
  invested_sip: number;
  value_sip: number;
  invested_step_up: number;
  value_step_up: number;
  bank_fd_value: number;
  gbm_pessimistic_10th: number;
  gbm_base_50th: number;
  gbm_optimistic_90th: number;
}

export interface CompoundingTrajectoryData {
  initial_lump_sum: number;
  monthly_sip: number;
  tenure_years: number;
  expected_return_pct: number;
  step_up_pct: number;
  annual_volatility_pct: number;
  yearly_trajectories: CompoundingYearlyPoint[];
  bank_fd_hurdle_value: number;
  alpha_vs_bank_fd: number;
}

export const DEMO_HOLDINGS: PortfolioHoldingItem[] = [
  {
    symbol: "RELIANCE",
    name: "Reliance Industries Ltd",
    sector: "Energy / Conglomerate",
    shares: 20,
    buy_price: 1320.0,
    current_price: 1377.5,
    invested_amount: 26400.0,
    current_value: 27550.0,
    unrealized_pnl: 1150.0,
    unrealized_pnl_pct: 4.36,
    weight: 0.27,
    pnl_1d: 180.0,
    pnl_1d_pct: 0.66,
    prev_close_price: 1368.5,
  },
  {
    symbol: "TCS",
    name: "Tata Consultancy Services Ltd",
    sector: "Information Technology",
    shares: 10,
    buy_price: 2280.0,
    current_price: 2376.2,
    invested_amount: 22800.0,
    current_value: 23762.0,
    unrealized_pnl: 962.0,
    unrealized_pnl_pct: 4.22,
    weight: 0.23,
    pnl_1d: 120.0,
    pnl_1d_pct: 0.51,
    prev_close_price: 2364.2,
  },
  {
    symbol: "HDFCBANK",
    name: "HDFC Bank Ltd",
    sector: "Banking & Financials",
    shares: 26,
    buy_price: 810.0,
    current_price: 846.0,
    invested_amount: 21060.0,
    current_value: 21996.0,
    unrealized_pnl: 936.0,
    unrealized_pnl_pct: 4.44,
    weight: 0.22,
    pnl_1d: 140.0,
    pnl_1d_pct: 0.64,
    prev_close_price: 840.6,
  },
  {
    symbol: "INFY",
    name: "Infosys Ltd",
    sector: "Information Technology",
    shares: 8,
    buy_price: 1460.0,
    current_price: 1520.0,
    invested_amount: 11680.0,
    current_value: 12160.0,
    unrealized_pnl: 480.0,
    unrealized_pnl_pct: 4.11,
    weight: 0.12,
    pnl_1d: -45.0,
    pnl_1d_pct: -0.37,
    prev_close_price: 1525.6,
  },
  {
    symbol: "ICICIBANK",
    name: "ICICI Bank Ltd",
    sector: "Banking & Financials",
    shares: 7,
    buy_price: 1210.0,
    current_price: 1260.0,
    invested_amount: 8470.0,
    current_value: 8820.0,
    unrealized_pnl: 350.0,
    unrealized_pnl_pct: 4.13,
    weight: 0.09,
    pnl_1d: 65.0,
    pnl_1d_pct: 0.74,
    prev_close_price: 1250.7,
  },
  {
    symbol: "LT",
    name: "Larsen & Toubro Ltd",
    sector: "Capital Goods & Infra",
    shares: 2,
    buy_price: 3520.0,
    current_price: 3680.0,
    invested_amount: 7040.0,
    current_value: 7360.0,
    unrealized_pnl: 320.0,
    unrealized_pnl_pct: 4.55,
    weight: 0.07,
    pnl_1d: 50.0,
    pnl_1d_pct: 0.68,
    prev_close_price: 3655.0,
  },
];

export function getDemoPortfolio(): PortfolioData {
  const invested_capital = DEMO_HOLDINGS.reduce(
    (acc, h) => acc + h.invested_amount,
    0
  );
  const holdings_current_value = DEMO_HOLDINGS.reduce(
    (acc, h) => acc + h.current_value,
    0
  );
  const cash = 3680.0;
  const current_value = holdings_current_value + cash;
  const initial_capital = invested_capital + cash;
  const total_pnl = current_value - initial_capital;
  const total_pnl_pct = (total_pnl / initial_capital) * 100;

  const pnl_1d = DEMO_HOLDINGS.reduce((acc, h) => acc + h.pnl_1d, 0);
  const prev_total_value = current_value - pnl_1d;
  const pnl_1d_pct = prev_total_value > 0 ? (pnl_1d / prev_total_value) * 100 : 0;

  return {
    portfolio_id: "demo-portfolio-nifty50",
    name: "Demo NIFTY 50 Balanced Basket",
    initial_capital,
    cash,
    invested_capital,
    current_value,
    total_pnl,
    total_pnl_pct,
    pnl_1d,
    pnl_1d_pct,
    max_drawdown_pct: 3.2,
    holdings: DEMO_HOLDINGS,
    benchmark_comparison: {
      portfolio_return_pct: total_pnl_pct,
      nifty_return_pct: 3.42,
      bank_fd_return_pct: 1.15,
      alpha_vs_nifty: total_pnl_pct - 3.42,
      alpha_vs_fd: total_pnl_pct - 1.15,
    },
    initial_regime: "BULL_TRENDING",
    current_regime: "BULL_TRENDING",
    risk_persona: "Balanced",
    horizon: "6M",
    created_at: new Date().toISOString(),
    as_of_date: new Date().toISOString().split("T")[0],
    is_demo: true,
    beta: 0.88,
    var_1d_pct: -1.42,
    target_drift_pct: 1.2,
    risk_metrics: {
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
    },
  };
}

export function getDemoCompoundingTrajectory(
  initialLumpSum = 100000
): CompoundingTrajectoryData {
  const yearly_trajectories: CompoundingYearlyPoint[] = [];
  const expectedReturn = 0.13;
  const fdRate = 0.07;
  const vol = 0.15;

  for (let year = 1; year <= 10; year++) {
    const fdVal = initialLumpSum * Math.pow(1 + fdRate, year);
    const medianVal = initialLumpSum * Math.pow(1 + expectedReturn, year);
    // Quantile cones using standard lognormal approximation
    const sigmaSqrtT = vol * Math.sqrt(year);
    const q10Val = medianVal * Math.exp(-1.28155 * sigmaSqrtT);
    const q90Val = medianVal * Math.exp(1.28155 * sigmaSqrtT);

    yearly_trajectories.push({
      year,
      invested_lump_sum: initialLumpSum,
      value_lump_sum: Math.round(medianVal),
      invested_sip: 0,
      value_sip: 0,
      invested_step_up: 0,
      value_step_up: 0,
      bank_fd_value: Math.round(fdVal),
      gbm_pessimistic_10th: Math.round(q10Val),
      gbm_base_50th: Math.round(medianVal),
      gbm_optimistic_90th: Math.round(q90Val),
    });
  }

  const finalYear = yearly_trajectories[yearly_trajectories.length - 1];
  const finalMedian = finalYear.gbm_base_50th;
  const finalFd = finalYear.bank_fd_value;

  return {
    initial_lump_sum: initialLumpSum,
    monthly_sip: 0,
    tenure_years: 10,
    expected_return_pct: 13.0,
    step_up_pct: 0,
    annual_volatility_pct: 15.0,
    yearly_trajectories,
    bank_fd_hurdle_value: finalFd,
    alpha_vs_bank_fd: Math.round(finalMedian - finalFd),
  };
}

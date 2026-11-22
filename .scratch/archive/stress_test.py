from decimal import Decimal
from app.ml.simulation.charges import calculate_delivery_charges
from app.ml.portfolio.compounding_engine import calculate_monthly_sip, calculate_lump_sum
from app.ml.portfolio.rebalancer import evaluate_rebalance
from app.ml.portfolio.belltalon_exporter import export_portfolio_to_belltalon
from app.core.models import PortfolioState, PortfolioHolding, BenchmarkComparisonLive

print("--- STRESS TEST 1: INDIAN STATUTORY CHARGES BOUNDARY CONDITIONS ---")
# Edge cases: 0 turnover, 1 rupee, 100 Crore
zero_buy = calculate_delivery_charges(turnover=0, side="BUY")
assert zero_buy.total == Decimal("0.00")
print("  ✓ Zero turnover: Total charges = ₹0.00")

small_buy = calculate_delivery_charges(turnover=10, side="BUY")
print(f"  ✓ ₹10 Delivery Buy: STT=₹{small_buy.stt}, Stamp Duty=₹{small_buy.stamp_duty}, Total=₹{small_buy.total}")

# High turnover: ₹100 Crore
turnover_100cr = Decimal("1000000000")
big_buy = calculate_delivery_charges(turnover=turnover_100cr, side="BUY")
big_sell = calculate_delivery_charges(turnover=turnover_100cr, side="SELL")
print(f"  ✓ ₹100 Cr Delivery Buy: STT=₹{big_buy.stt:,.2f}, GST=₹{big_buy.gst:,.2f}, Total=₹{big_buy.total:,.2f}")
print(f"  ✓ ₹100 Cr Delivery Sell: STT=₹{big_sell.stt:,.2f}, StampDuty=₹{big_sell.stamp_duty:,.2f} (Stamp duty 0 on sell), Total=₹{big_sell.total:,.2f}")
assert big_sell.stamp_duty == Decimal("0.00")
assert big_buy.stamp_duty > Decimal("0.00")

print("\n--- STRESS TEST 2: COMPOUNDING NET WEALTH WITH CHARGES DRAG ---")
# 30-Year SIP of ₹25,000/month at 15% CAGR
sip_gross = calculate_monthly_sip(monthly_amount=25000, annual_return_pct=15.0, tenure_years=30, include_charges=False)
sip_net = calculate_monthly_sip(monthly_amount=25000, annual_return_pct=15.0, tenure_years=30, include_charges=True)

print(f"  ✓ 30Y SIP Invested: ₹{sip_gross.total_invested:,.2f}")
print(f"  ✓ 30Y SIP Gross Wealth: ₹{sip_gross.future_value:,.2f}")
print(f"  ✓ 30Y SIP Net Wealth:   ₹{sip_net.future_value:,.2f}")
print(f"  ✓ Total Statutory Charges Drag: ₹{sip_net.total_charges:,.2f}")
assert sip_net.future_value < sip_gross.future_value
assert sip_net.total_charges > 0

# 30-Year Lump Sum of ₹10,00,000 at 14% CAGR
lump_gross = calculate_lump_sum(principal=1000000, annual_return_pct=14.0, tenure_years=30, include_charges=False)
lump_net = calculate_lump_sum(principal=1000000, annual_return_pct=14.0, tenure_years=30, include_charges=True)
print(f"  ✓ 30Y Lump Sum Gross Wealth: ₹{lump_gross.future_value:,.2f}")
print(f"  ✓ 30Y Lump Sum Net Wealth:   ₹{lump_net.future_value:,.2f}")
print(f"  ✓ Total Statutory Charges Drag: ₹{lump_net.total_charges:,.2f}")
assert lump_net.future_value < lump_gross.future_value

print("\n--- STRESS TEST 3: REBALANCER UNDER DRIFT & EXTREME VOLATILITY ---")
# 50 holdings under random target vs actual drift
current_holdings = {f"STOCK_{i}": 10 for i in range(50)}
target_weights = {f"STOCK_{i}": 0.02 for i in range(50)}
current_prices = {f"STOCK_{i}": 100.0 + (i * 15.0) for i in range(50)}

eval_sheet = evaluate_rebalance(
    current_holdings=current_holdings,
    target_weights=target_weights,
    current_prices=current_prices,
    available_cash=50000.0,
    portfolio_id="stress_rebalance",
    portfolio_name="Stress Rebalance 50 Holdings"
)
print(f"  ✓ Total Generated Orders: {eval_sheet.total_orders}")
print(f"  ✓ Total Rebalance Amount: ₹{eval_sheet.total_estimated_amount:,.2f}")
print(f"  ✓ Total Invested: ₹{eval_sheet.total_invested:,.2f}")
print(f"  ✓ Unallocated Cash Buffer: ₹{eval_sheet.unallocated_cash:,.2f}")
print(f"  ✓ Estimated Statutory Charges: ₹{eval_sheet.estimated_statutory_charges:,.2f}")
print(f"  ✓ Drift Reduction: {eval_sheet.drift_reduction_pct:.2f}%")
assert eval_sheet.total_orders > 0
assert eval_sheet.estimated_statutory_charges > 0
assert eval_sheet.drift_reduction_pct > 0

print("\n--- STRESS TEST 4: BELLTALON EXPORT ROBUSTNESS ---")
# Export portfolio with 50 holdings
dummy_holdings = [
    PortfolioHolding(
        symbol=f"SYM{i}",
        name=f"Company {i}",
        sector="Technology",
        shares=10,
        buy_price=100.0,
        current_price=110.0,
        invested_amount=1000.0,
        current_value=1100.0,
        unrealized_pnl=100.0,
        unrealized_pnl_pct=10.0,
        weight=0.02,
        target_weight=0.02
    )
    for i in range(50)
]
dummy_portfolio = PortfolioState(
    portfolio_id="stress_test_port",
    name="Stress Test Mega Portfolio",
    initial_capital=50000.0,
    cash=1000.0,
    invested_capital=50000.0,
    current_value=55000.0,
    total_pnl=5000.0,
    total_pnl_pct=10.0,
    pnl_1d=200.0,
    pnl_1d_pct=0.4,
    max_drawdown_pct=2.1,
    holdings=dummy_holdings,
    benchmark_comparison=BenchmarkComparisonLive(
        portfolio_return_pct=10.0,
        nifty_return_pct=5.0,
        bank_fd_return_pct=2.5,
        alpha_vs_nifty=5.0,
        alpha_vs_fd=7.5
    ),
    initial_regime="Low-Volatility Bull",
    current_regime="Sideways Consolidation",
    risk_persona="Aggressive",
    horizon="12M",
    created_at="2026-11-13",
    as_of_date="2026-11-13"
)
belltalon_strat = export_portfolio_to_belltalon(dummy_portfolio)
print(f"  ✓ Belltalon Strategy Name: {belltalon_strat['name']}")
print(f"  ✓ Exported Universe Symbols Count: {len(belltalon_strat['universe']['symbols'])}")
print(f"  ✓ Exported Schema Version: {belltalon_strat['schemaVersion']}")
assert len(belltalon_strat["universe"]["symbols"]) == 50
assert belltalon_strat["schemaVersion"] == 1

print("\n=======================================================")
print("ALL BACKEND STRESS TESTS COMPLETED SUCCESSFULLY WITH 0 FAILURES!")
print("=======================================================")

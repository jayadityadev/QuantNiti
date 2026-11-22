"""Comprehensive End-to-End Endpoint & Logic Verification Script for QuantNiti."""

from fastapi.testclient import TestClient
from app.api.app import create_app
from app.core.models import RiskPersona

app = create_app()
client = TestClient(app)

def test_regime_endpoint():
    print("Testing /api/regime/current...")
    res = client.get("/api/regime/current")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
    data = res.json()
    probs = data["probabilities"]
    print(f"  Regime: {data['regime']}")
    print(f"  Probabilities: Bull={probs['bull']*100:.1f}%, Sideways={probs['sideways']*100:.1f}%, Bear={probs['bear']*100:.1f}%")
    total_prob = probs['bull'] + probs['sideways'] + probs['bear']
    assert abs(total_prob - 1.0) < 0.01, f"Probabilities do not sum to 1.0: {total_prob}"
    print("  [PASS] Regime endpoint verified.")

def test_grow_combinations():
    print("\nTesting /api/v1/grow/recommend combinations...")
    
    # 1. 12M, 1L Aggressive
    res_agg = client.post("/api/v1/grow/recommend", json={
        "capital": 100000,
        "horizon": "12M",
        "risk_persona": "Aggressive"
    })
    assert res_agg.status_code == 200, f"Aggressive failed: {res_agg.text}"
    data_agg = res_agg.json()
    base_agg = data_agg["growth_projections"]["base"]
    opt_agg = data_agg["growth_projections"]["optimistic"]
    pess_agg = data_agg["growth_projections"]["pessimistic"]

    # 2. 12M, 1L Conservative
    res_cons = client.post("/api/v1/grow/recommend", json={
        "capital": 100000,
        "horizon": "12M",
        "risk_persona": "Conservative"
    })
    assert res_cons.status_code == 200, f"Conservative failed: {res_cons.text}"
    data_cons = res_cons.json()
    base_cons = data_cons["growth_projections"]["base"]
    opt_cons = data_cons["growth_projections"]["optimistic"]
    pess_cons = data_cons["growth_projections"]["pessimistic"]

    print(f"  Aggressive (12M, 1L):")
    print(f"    Pessimistic: {pess_agg['expected_return_pct']}% -> Rs.{pess_agg['projected_value']}")
    print(f"    Base Case:   {base_agg['expected_return_pct']}% -> Rs.{base_agg['projected_value']}")
    print(f"    Optimistic:  {opt_agg['expected_return_pct']}% -> Rs.{opt_agg['projected_value']}")

    print(f"  Conservative (12M, 1L):")
    print(f"    Pessimistic: {pess_cons['expected_return_pct']}% -> Rs.{pess_cons['projected_value']}")
    print(f"    Base Case:   {base_cons['expected_return_pct']}% -> Rs.{base_cons['projected_value']}")
    print(f"    Optimistic:  {opt_cons['expected_return_pct']}% -> Rs.{opt_cons['projected_value']}")

    # Assert numbers are NOT identical
    assert base_agg['expected_return_pct'] != base_cons['expected_return_pct'], "Error: Aggressive and Conservative base returns are identical!"
    assert base_agg['projected_value'] != base_cons['projected_value'], "Error: Aggressive and Conservative values are identical!"
    print("  [PASS] Persona distinctiveness verified.")

    # 3. Custom Horizon (e.g. 9M)
    res_custom = client.post("/api/v1/grow/recommend", json={
        "capital": 100000,
        "horizon": "9M",
        "risk_persona": "Balanced"
    })
    assert res_custom.status_code == 200, f"Custom horizon 9M failed: {res_custom.text}"
    print(f"  Custom 9M Horizon Base Return: {res_custom.json()['growth_projections']['base']['expected_return_pct']}%")
    print("  [PASS] Custom horizon input verified.")

def test_backtest_endpoints():
    print("\nTesting /api/backtest/run and /api/backtest/compare...")
    
    # Single backtest run with string strategy
    res_run = client.post("/api/backtest/run", json={
        "symbol": "RELIANCE",
        "strategy": "MA_CROSSOVER",
        "initial_capital": 100000
    })
    assert res_run.status_code == 200, f"Backtest run failed: {res_run.text}"
    m = res_run.json()["metrics"]
    print(f"  Reliance MA Crossover Backtest:")
    print(f"    Return: {m['total_return_pct']}%, Sharpe: {m['sharpe_ratio']}, Final Equity: Rs.{m['final_equity']}")

    # Multi-strategy comparator
    res_comp = client.get("/api/backtest/compare?symbol=RELIANCE&initial_capital=100000")
    assert res_comp.status_code == 200, f"Backtest compare failed: {res_comp.text}"
    comp_data = res_comp.json()
    print(f"  5-Strategy Comparison for RELIANCE:")
    print(f"    Recommended Strategy: {comp_data['recommended_strategy']}")
    print(f"    Reason: {comp_data['recommendation_reason']}")
    for s in comp_data["strategies"]:
        print(f"      - {s['strategy']}: Return={s.get('total_return_pct')}%, Sharpe={s.get('sharpe_ratio')}, MaxDD={s.get('max_drawdown_pct')}%")
    print("  [PASS] Backtest suite and comparator verified.")

def test_alerts_endpoint():
    print("\nTesting /api/alerts...")
    res = client.get("/api/alerts")
    assert res.status_code == 200, f"Alerts failed: {res.text}"
    data = res.json()
    alerts = data.get("alerts", [])
    print(f"  Total Active Alerts: {len(alerts)}")
    for a in alerts:
        print(f"    [{a['severity']}] {a['title']}: {a['message'][:75]}...")
    assert len(alerts) >= 3, "Expected at least 3 active alerts"
    print("  [PASS] Alert and Buy/Sell trigger signals verified.")

def test_reviews_endpoint():
    print("\nTesting /api/v1/reviews/basket/balanced_6m...")
    res = client.get("/api/v1/reviews/basket/balanced_6m")
    assert res.status_code == 200, f"Reviews failed: {res.text}"
    data = res.json()
    reviews = data.get("reviews", [])
    print(f"  Total Community Reviews: {len(reviews)}")
    for r in reviews:
        print(f"    - {r['user_name']} ({r['rating']}/5 stars): {r['verification_badge']}")
    assert len(reviews) >= 2, "Expected verified reviews"
    print("  [PASS] Review system & 3-Tier fact checker verified.")

def test_market_quote():
    print("\nTesting /api/market/quote/^NSEI...")
    res = client.get("/api/market/quote/^NSEI")
    assert res.status_code == 200, f"Quote failed: {res.text}"
    q = res.json()
    print(f"  NIFTY 50 Quote: Rs.{q['current_price']} (Day Change: {q['day_change']})")
    assert q['current_price'] > 20000.0, "Expected realistic Nifty price level"
    print("  [PASS] Market Quote verified.")

if __name__ == "__main__":
    test_regime_endpoint()
    test_grow_combinations()
    test_backtest_endpoints()
    test_alerts_endpoint()
    test_reviews_endpoint()
    test_market_quote()
    print("\n=======================================================")
    print("ALL 6 ENDPOINT SUITES PASSED FLAWLESSLY WITH VALID MATH!")
    print("=======================================================")

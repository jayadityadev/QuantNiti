#!/usr/bin/env python3
"""QuantNiti Verification Driver Script.

Drives the QuantNiti application end-to-end to verify UI journeys,
FastAPI REST contracts, and mathematical quant outputs.
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
import urllib.request
import urllib.error

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
SRC_DIR = REPO_ROOT / "src"
VENV_PYTHON = REPO_ROOT / ".venv" / "Scripts" / "python.exe"
if not VENV_PYTHON.exists():
    VENV_PYTHON = REPO_ROOT / ".venv" / "bin" / "python"
if not VENV_PYTHON.exists():
    VENV_PYTHON = Path(sys.executable)


def http_get(url: str, timeout: float = 15.0) -> tuple[int, dict]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "QuantNiti-Verifier/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
            return response.status, data
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            return e.code, json.loads(body)
        except Exception:
            return e.code, {"error": body}
    except Exception as e:
        return 0, {"error": str(e)}


def http_post(url: str, payload: dict, timeout: float = 10.0) -> tuple[int, dict]:
    try:
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data_bytes,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "QuantNiti-Verifier/1.0",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
            return response.status, data
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            return e.code, json.loads(body)
        except Exception:
            return e.code, {"error": body}
    except Exception as e:
        return 0, {"error": str(e)}


def doctor(port: int) -> int:
    """Check whether the target instance is healthy and ready to drive."""
    health_url = f"http://127.0.0.1:{port}/api/v1/health"
    regime_url = f"http://127.0.0.1:{port}/api/regime/current"

    print(f"[*] Running Doctor Check on http://127.0.0.1:{port}...")
    status, health = http_get(health_url)
    if status != 200 or health.get("status") != "healthy":
        print(f"[FAIL] Health check failed on {health_url}: Status {status}, Body: {health}")
        return 1
    print(f"  ✓ Service Health: {health.get('status')} ({health.get('service')})")

    status, regime = http_get(regime_url)
    if status != 200 or "regime" not in regime:
        print(f"[FAIL] Regime endpoint failed on {regime_url}: Status {status}, Body: {regime}")
        return 1
    print(f"  ✓ Market Regime Engine: Active ('{regime.get('regime')}', confidence: {regime.get('confidence', 0)*100:.1f}%)")
    print("[PASS] QuantNiti instance is healthy and ready to drive.")
    return 0


def drive_feature(feature: str, port: int, output_dir: Path) -> int:
    """Drive a specific user feature and capture verifiable evidence."""
    output_dir.mkdir(parents=True, exist_ok=True)
    base_url = f"http://127.0.0.1:{port}"

    from playwright.sync_api import sync_playwright

    print(f"[*] Driving feature '{feature}' against {base_url}...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 393, "height": 852},
            device_scale_factor=2,
            is_mobile=True,
            has_touch=True,
        )
        page = context.new_page()

        if feature == "market-regime-radar":
            page.goto(base_url)
            page.wait_for_load_state("networkidle")
            time.sleep(1)
            # Set onboarded so we see the Home tab with Regime Radar
            page.evaluate("""() => {
                localStorage.setItem('quantniti_onboarded', 'true');
                localStorage.setItem('quantniti_risk_persona', 'Balanced');
                window.location.reload();
            }""")
            page.wait_for_load_state("networkidle")
            time.sleep(2)

            snap_path = output_dir / "regime_radar_ui.png"
            page.screenshot(path=str(snap_path))
            print(f"  ✓ Captured UI Screenshot: {snap_path}")

            # Verify and save API contract state
            status, regime_json = http_get(f"{base_url}/api/regime/current")
            assert status == 200, f"Regime API failed with status {status}"
            json_path = output_dir / "regime_radar_api.json"
            json_path.write_text(json.dumps(regime_json, indent=2), encoding="utf-8")
            print(f"  ✓ Saved API Evidence: {json_path}")
            print(f"  ✓ Verified Regime: {regime_json.get('regime')} ({regime_json.get('probabilities')})")

        elif feature == "onboarding-quiz":
            page.goto(base_url)
            page.wait_for_load_state("networkidle")
            # Clear storage to ensure quiz is visible
            page.evaluate("() => localStorage.clear()")
            page.reload()
            page.wait_for_load_state("networkidle")
            time.sleep(1.5)

            snap_path = output_dir / "onboarding_quiz_ui.png"
            page.screenshot(path=str(snap_path))
            print(f"  ✓ Captured Onboarding UI Screenshot: {snap_path}")

        elif feature == "grow-ai-basket":
            page.goto(base_url)
            page.wait_for_load_state("networkidle")
            page.evaluate("""() => {
                localStorage.setItem('quantniti_onboarded', 'true');
                localStorage.setItem('quantniti_risk_persona', 'Balanced');
                window.location.reload();
            }""")
            page.wait_for_load_state("networkidle")
            time.sleep(1)

            # Navigate to Grow tab
            page.locator("button:has-text('Grow')").click()
            time.sleep(1.5)

            # Step 1 -> Step 2
            page.locator("button:has-text('Continue to Horizon')").click()
            time.sleep(1)

            # Step 2 -> Step 3
            page.locator("button:has-text('Continue to Persona')").click()
            time.sleep(1)

            # Step 3 -> Generate Results
            page.locator("button:has-text('Review & Generate')").click()
            time.sleep(4)

            snap_path = output_dir / "grow_ai_basket_results.png"
            page.screenshot(path=str(snap_path))
            print(f"  ✓ Captured Grow AI Basket Screenshot: {snap_path}")

            # API proof
            payload = {"capital": 100000, "horizon": "12M", "risk_persona": "Balanced"}
            status, basket = http_post(f"{base_url}/api/v1/grow/recommend", payload)
            assert status == 200, f"Grow recommend API failed: {status}"
            json_path = output_dir / "grow_ai_basket_api.json"
            json_path.write_text(json.dumps(basket, indent=2), encoding="utf-8")
            print(f"  ✓ Saved Basket API Evidence: {json_path}")
            print(f"  ✓ Basket ID: {basket.get('basket_id')}, Allocations: {len(basket.get('allocations', []))} assets")

        elif feature == "backtesting-lab":
            payload = {
                "symbol": "RELIANCE",
                "strategy": "MA_CROSSOVER",
                "initial_capital": 100000,
            }
            status, res = http_post(f"{base_url}/api/backtest/run", payload)
            assert status == 200, f"Backtest run failed: {status}"
            json_path = output_dir / "backtest_ma_crossover.json"
            json_path.write_text(json.dumps(res, indent=2), encoding="utf-8")
            print(f"  ✓ Saved Backtest Evidence: {json_path}")
            print(f"  ✓ Metrics: Return={res['metrics']['total_return_pct']}%, Sharpe={res['metrics']['sharpe_ratio']}")

        elif feature == "virtual-paper-portfolio":
            page.goto(base_url)
            page.wait_for_load_state("networkidle")
            page.evaluate("""() => {
                localStorage.setItem('quantniti_onboarded', 'true');
                localStorage.setItem('quantniti_risk_persona', 'Balanced');
                window.location.reload();
            }""")
            page.wait_for_load_state("networkidle")
            time.sleep(1)

            page.locator("button[role='tab'][aria-label='Portfolio']").click()
            time.sleep(2)
            snap_path = output_dir / "portfolio_tracker_ui.png"
            page.screenshot(path=str(snap_path))
            print(f"  ✓ Captured Portfolio Screenshot: {snap_path}")

        else:
            print(f"[FAIL] Unknown feature '{feature}'. Supported: market-regime-radar, onboarding-quiz, grow-ai-basket, backtesting-lab, virtual-paper-portfolio")
            browser.close()
            return 1

        browser.close()

    print(f"[PASS] Successfully verified feature '{feature}'.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="QuantNiti Verification Driver")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doc_parser = subparsers.add_parser("doctor", help="Run health & readiness check")
    doc_parser.add_argument("--port", type=int, default=8000, help="Port to probe")

    drive_parser = subparsers.add_parser("drive", help="Drive a user-facing feature")
    drive_parser.add_argument("feature", help="Feature name (market-regime-radar, onboarding-quiz, grow-ai-basket, backtesting-lab, virtual-paper-portfolio)")
    drive_parser.add_argument("--port", type=int, default=8000, help="Port to target")
    drive_parser.add_argument("--output-dir", type=str, default=".audit/verify", help="Directory for evidence")

    args = parser.parse_args()

    if args.command == "doctor":
        sys.exit(doctor(args.port))
    elif args.command == "drive":
        out = Path(args.output_dir)
        sys.exit(drive_feature(args.feature, args.port, out))


if __name__ == "__main__":
    main()

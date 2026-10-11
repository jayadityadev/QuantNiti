import os
import time
from playwright.sync_api import sync_playwright

snap_dir = os.path.abspath(r"D:\Codebase\QuantNiti\docs\review\ours\snapshots")
os.makedirs(snap_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    # iPhone 14 Pro mobile viewport (393 x 852 @ 2x DPR)
    context = browser.new_context(
        viewport={"width": 393, "height": 852},
        device_scale_factor=2,
        is_mobile=True,
        has_touch=True
    )
    page = context.new_page()

    # 1. Capture Onboarding Screen (Initial Visit)
    print("Capturing 01_onboarding.png...")
    page.goto("http://localhost:8000")
    page.wait_for_load_state("networkidle")
    time.sleep(1.5)
    page.screenshot(path=os.path.join(snap_dir, "01_onboarding.png"))

    # Set Dark Theme & Onboarded State
    page.evaluate("""() => {
        localStorage.setItem('quantniti_onboarded', 'true');
        localStorage.setItem('quantniti_risk_persona', 'Balanced');
        localStorage.setItem('quantniti_theme', 'dark');
        document.documentElement.setAttribute('data-theme', 'dark');
    }""")
    page.goto("http://localhost:8000")
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # Ensure dark theme is applied
    page.evaluate("document.documentElement.setAttribute('data-theme', 'dark')")

    # 2. Home Tab: Market Pulse & Regime Radar
    print("Capturing 02_home_market_pulse.png...")
    time.sleep(1)
    page.screenshot(path=os.path.join(snap_dir, "02_home_market_pulse.png"))

    # Scroll down to capture Compounding Visualizer & Learning Hub
    print("Capturing 03_home_compounding_hub.png...")
    page.mouse.wheel(0, 420)
    time.sleep(1)
    page.screenshot(path=os.path.join(snap_dir, "03_home_compounding_hub.png"))

    # Scroll back to top
    page.mouse.wheel(0, -500)
    time.sleep(0.5)

    # 3. Grow Tab: Step 1 (Capital)
    print("Capturing 04_grow_step1_capital.png...")
    page.locator("button:has-text('Grow')").click()
    time.sleep(1.5)
    page.screenshot(path=os.path.join(snap_dir, "04_grow_step1_capital.png"))

    # Step 2: Horizon
    print("Capturing 05_grow_step2_horizon.png...")
    page.locator("button:has-text('Continue to Horizon')").click()
    time.sleep(1)
    page.screenshot(path=os.path.join(snap_dir, "05_grow_step2_horizon.png"))

    # Step 3: Persona
    print("Capturing 06_grow_step3_persona.png...")
    page.locator("button:has-text('Continue to Persona')").click()
    time.sleep(1)
    page.screenshot(path=os.path.join(snap_dir, "06_grow_step3_persona.png"))

    # Generate AI Basket (Wait for scikit-learn & HRP calculation ~15s)
    print("Generating AI Basket & waiting for HRP completion...")
    page.locator("button:has-text('Review & Generate')").click()
    page.wait_for_selector("text=Your Optimized AI Basket", timeout=35000)
    time.sleep(2)
    print("Capturing 07_grow_step4_results_donut.png...")
    page.screenshot(path=os.path.join(snap_dir, "07_grow_step4_results_donut.png"))

    # Scroll to Rupee Scenarios & Allocations
    print("Capturing 08_grow_step4_scenarios_and_shares.png...")
    page.mouse.wheel(0, 450)
    time.sleep(1)
    page.screenshot(path=os.path.join(snap_dir, "08_grow_step4_scenarios_and_shares.png"))

    # Step 5: Trust Card (Deep Dive)
    print("Navigating to Step 5: Deep Dive...")
    deep_btn = page.locator("button:has-text('See Deep Dive')")
    if deep_btn.count() > 0:
        deep_btn.click()
        time.sleep(1.5)
        print("Capturing 09_grow_step5_trust_card.png...")
        page.screenshot(path=os.path.join(snap_dir, "09_grow_step5_trust_card.png"))

    # 4. Explore Tab: 360 Stock Intelligence
    print("Capturing 10_explore_stocks.png...")
    page.locator("button:has-text('Explore')").click()
    time.sleep(2)
    page.screenshot(path=os.path.join(snap_dir, "10_explore_stocks.png"))

    # 5. Portfolio Tab: Real-Time Tracker & Regime Alerts
    print("Capturing 11_portfolio_tracker.png...")
    page.locator("button:has-text('Portfolio')").click()
    time.sleep(2)
    page.screenshot(path=os.path.join(snap_dir, "11_portfolio_tracker.png"))

    # 6. Open NitiBot Copilot Modal
    print("Opening NitiBot Copilot...")
    page.evaluate("""() => {
        if (window.__openModal) {
            window.__openModal('nitibot');
        }
    }""")
    time.sleep(1.5)
    # Check if modal opened, otherwise click bot FAB
    if page.locator("text=NitiBot").count() == 0:
        fab = page.locator("button.fixed, button[class*='fixed']").last
        if fab.count() > 0:
            fab.click()
            time.sleep(1.5)
    print("Capturing 12_nitibot_copilot.png...")
    page.screenshot(path=os.path.join(snap_dir, "12_nitibot_copilot.png"))

    browser.close()

print("ALL SNAPSHOTS READY!")

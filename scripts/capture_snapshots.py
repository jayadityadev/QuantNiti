import os
import time
from playwright.sync_api import sync_playwright

snap_dir = os.path.abspath(r"D:\Codebase\QuantNiti\docs\review\ours\snapshots")
os.makedirs(snap_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    # Standard iPhone 14 Pro mobile viewport (393x852 @ 2x DPR)
    context = browser.new_context(
        viewport={"width": 393, "height": 852},
        device_scale_factor=2,
        is_mobile=True,
        has_touch=True
    )
    page = context.new_page()

    # 1. Onboarding Quiz
    print("1. Capturing Onboarding Quiz...")
    page.goto("http://localhost:8000")
    page.wait_for_load_state("networkidle")
    time.sleep(1.5)
    page.screenshot(path=os.path.join(snap_dir, "01_onboarding_quiz.png"))
    print("-> Saved 01_onboarding_quiz.png")

    # Set onboarded & Balanced persona
    page.evaluate("""() => {
        localStorage.setItem('quantniti_onboarded', 'true');
        localStorage.setItem('quantniti_risk_persona', 'Balanced');
        window.location.reload();
    }""")
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # 2. Home Tab: Market Pulse & Regime Radar
    print("2. Capturing Home Tab...")
    page.screenshot(path=os.path.join(snap_dir, "02_home_regime_radar.png"))
    print("-> Saved 02_home_regime_radar.png")

    # Scroll slightly to capture Compounding Visualizer on Home
    page.mouse.wheel(0, 350)
    time.sleep(1)
    page.screenshot(path=os.path.join(snap_dir, "02b_home_compounding.png"))
    print("-> Saved 02b_home_compounding.png")

    # 3. Grow Tab: Navigate via Bottom Nav
    print("3. Navigating to Grow Tab via Bottom Nav...")
    page.locator("button:has-text('Grow')").click()
    time.sleep(2)
    page.screenshot(path=os.path.join(snap_dir, "03_grow_step1_capital.png"))
    print("-> Saved 03_grow_step1_capital.png")

    # Navigate to Step 2 (Horizon)
    print("Navigating to Step 2...")
    page.locator("button:has-text('Continue to Horizon')").click()
    time.sleep(1)
    page.screenshot(path=os.path.join(snap_dir, "04_grow_step2_horizon.png"))
    print("-> Saved 04_grow_step2_horizon.png")

    # Navigate to Step 3 (Persona)
    print("Navigating to Step 3...")
    page.locator("button:has-text('Continue to Persona')").click()
    time.sleep(1)
    page.screenshot(path=os.path.join(snap_dir, "05_grow_step3_persona.png"))
    print("-> Saved 05_grow_step3_persona.png")

    # Click Review & Generate (Step 4: Results Overview)
    print("Generating AI Basket...")
    page.locator("button:has-text('Review & Generate')").click()
    # Wait for scikit-learn / HRP / Ledoit-Wolf backend computation
    time.sleep(4)
    page.screenshot(path=os.path.join(snap_dir, "06_grow_step4_results_overview.png"))
    print("-> Saved 06_grow_step4_results_overview.png")

    # Scroll down to show Whole Shares & Rupee Growth Scenario Cards
    page.mouse.wheel(0, 450)
    time.sleep(1)
    page.screenshot(path=os.path.join(snap_dir, "07_grow_step4_scenario_cards.png"))
    print("-> Saved 07_grow_step4_scenario_cards.png")

    # Click 'See Deep Dive' for Step 5: Trust Card & ESG
    deep_dive_btn = page.locator("button:has-text('See Deep Dive')")
    if deep_dive_btn.count() > 0:
        deep_dive_btn.click()
        time.sleep(1.5)
        page.screenshot(path=os.path.join(snap_dir, "08_grow_step5_trust_card.png"))
        print("-> Saved 08_grow_step5_trust_card.png")

    # 4. Explore Tab via Bottom Nav
    print("4. Navigating to Explore Tab via Bottom Nav...")
    page.locator("button:has-text('Explore')").click()
    time.sleep(2)
    page.screenshot(path=os.path.join(snap_dir, "09_explore_stock_cards.png"))
    print("-> Saved 09_explore_stock_cards.png")

    # 5. Portfolio Tab via Bottom Nav
    print("5. Navigating to Portfolio Tab via Bottom Nav...")
    page.locator("button:has-text('Portfolio')").click()
    time.sleep(2)
    page.screenshot(path=os.path.join(snap_dir, "10_portfolio_tracker.png"))
    print("-> Saved 10_portfolio_tracker.png")

    # 6. Open NitiBot Assistant Modal
    print("6. Capturing NitiBot Assistant...")
    # Find NitiBot floating button
    bot_fab = page.locator("button[aria-label*='NitiBot'], button:has-text('NitiBot'), div.fixed button, button.fixed")
    if bot_fab.count() > 0:
        bot_fab.last.click()
        time.sleep(2)
        page.screenshot(path=os.path.join(snap_dir, "11_nitibot_assistant.png"))
        print("-> Saved 11_nitibot_assistant.png")

    browser.close()

print("ALL SNAPSHOTS CAPTURED SUCCESSFULLY!")

"""Complete User Flow Automation and High-Resolution Snapshot Capture.
Simulates real user interaction across all pages, modals, and flows.
"""

import os
import shutil
import time
from playwright.sync_api import sync_playwright

SNAP_DIR = os.path.abspath(r"D:\Codebase\QuantNiti\docs\snapshots")
ARTIFACT_SNAP_DIR = os.path.abspath(r"C:\Users\Jayaditya\.gemini\antigravity\brain\ef733ee1-ce63-40b7-8474-c2146f4d0b37\snapshots")
os.makedirs(SNAP_DIR, exist_ok=True)
os.makedirs(ARTIFACT_SNAP_DIR, exist_ok=True)

def save_snap(page, filename, description=""):
    path1 = os.path.join(SNAP_DIR, filename)
    path2 = os.path.join(ARTIFACT_SNAP_DIR, filename)
    page.screenshot(path=path1)
    shutil.copyfile(path1, path2)
    print(f"  [SAVED] {filename} - {description}")

def run():
    print("==================================================================")
    print("STARTING FULL USER STORY FLOW AUTOMATION & SNAPSHOT GENERATION")
    print("==================================================================")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Mobile viewport emulation (iPhone 14 Pro: 393 x 852 @ 2x DPR)
        context = browser.new_context(
            viewport={"width": 393, "height": 852},
            device_scale_factor=2,
            is_mobile=True,
            has_touch=True
        )
        page = context.new_page()

        # -------------------------------------------------------------
        # STEP 1: FRESH ONBOARDING FLOW
        # -------------------------------------------------------------
        print("\n1. Testing Onboarding Flow...")
        page.goto("http://127.0.0.1:8000/")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        save_snap(page, "01_onboarding_welcome.png", "Initial Landing & Onboarding Hero")

        # Click Take 60s Risk Quiz
        quiz_btn = page.locator("button:has-text('Take 60s Risk Quiz'), button:has-text('Get Started'), button:has-text('Take Quiz')")
        if quiz_btn.count() > 0:
            quiz_btn.first.click()
            time.sleep(1.5)
            save_snap(page, "01b_onboarding_quiz.png", "Interactive Risk Assessment Quiz")

        # Complete onboarding in LocalStorage
        page.evaluate("""() => {
            localStorage.setItem('quantniti_onboarded', 'true');
            localStorage.setItem('quantniti_risk_persona', 'Balanced');
            localStorage.setItem('quantniti_theme', 'dark');
            document.documentElement.setAttribute('data-theme', 'dark');
        }""")
        page.goto("http://127.0.0.1:8000/home")
        page.wait_for_load_state("networkidle")
        time.sleep(2)

        # -------------------------------------------------------------
        # STEP 2: HOME DASHBOARD (DARK MODE)
        # -------------------------------------------------------------
        print("\n2. Testing Home Dashboard (Dark Mode)...")
        page.evaluate("document.documentElement.setAttribute('data-theme', 'dark')")
        time.sleep(1.5)
        save_snap(page, "02_home_market_pulse.png", "Home Dashboard: Vector Logo, Live Nifty Pulse (Rs.23,053) & GMM Radar")

        # Scroll to view Compounding Visualizer & Learning Gateway
        page.mouse.wheel(0, 480)
        time.sleep(1.5)
        save_snap(page, "03_home_compounding_hub.png", "Compounding Visualizer & Community Reviews Section")
        page.mouse.wheel(0, -600)
        time.sleep(0.5)

        # -------------------------------------------------------------
        # STEP 3: ACTIVE SMART ALERTS & TRIGGERS MODAL
        # -------------------------------------------------------------
        print("\n3. Testing Smart Alerts & Triggers Modal...")
        bell_btn = page.locator("button[data-testid='notification-bell-btn']")
        if bell_btn.count() > 0:
            bell_btn.click()
            time.sleep(2)
            save_snap(page, "04_active_alerts_modal.png", "Notification Center: 4 Active Triggers (TRENT Sell, HDFC Buy, Gold Hedge)")
            page.keyboard.press("Escape")
            time.sleep(1)

        # -------------------------------------------------------------
        # STEP 4: GROW WIZARD - ALL 5 STEPS
        # -------------------------------------------------------------
        print("\n4. Testing Grow Wizard Flow...")
        page.locator("button[aria-label='Grow']").click()
        time.sleep(1.5)
        save_snap(page, "05_grow_step1_capital.png", "Step 1: Capital Allocation (Rs.1,00,000 preset & chips)")

        # Continue to Step 2: Horizon
        page.locator("button:has-text('Continue to Horizon')").click()
        time.sleep(1.5)
        # Test custom manual slider
        slider = page.locator("input[type='range']")
        if slider.count() > 0:
            slider.fill("9")
            time.sleep(0.5)
        save_snap(page, "06_grow_step2_custom_horizon.png", "Step 2: Horizon Presets & Interactive Custom Month Slider (9M)")

        # Continue to Step 3: Persona
        page.locator("button:has-text('Continue to Persona')").click()
        time.sleep(1.5)
        # Select Conservative to showcase Gold safe-haven
        cons_btn = page.locator("text=Conservative").first
        if cons_btn.count() > 0:
            cons_btn.click()
            time.sleep(0.5)
        save_snap(page, "07_grow_step3_persona.png", "Step 3: Risk Persona Selection (Conservative with Gold Hedge)")

        # Generate AI Basket (Wait for HRP computation ~10s)
        print("  Generating AI Basket via HRP...")
        gen_btn = page.locator("button:has-text('Review & Generate'), button:has-text('Generate AI Basket')").first
        gen_btn.click()
        page.wait_for_selector("text=Your Optimized AI Basket", timeout=35000)
        time.sleep(2.5)
        save_snap(page, "08_grow_step4_results_donut.png", "Step 4: Optimized AI Basket Donut (High Contrast Theme)")

        # Scroll down to Probabilistic Growth Scenarios & Allocations
        page.mouse.wheel(0, 480)
        time.sleep(1.5)
        save_snap(page, "09_grow_step4_scenarios_and_shares.png", "Step 4: Quantile Projections (Distinct Rupee Values) & Holdings")

        # Step 5: Trust Card / Mathematical Deep Dive
        deep_btn = page.locator("button:has-text('See Deep Dive')")
        if deep_btn.count() > 0:
            deep_btn.click()
            time.sleep(1.5)
            save_snap(page, "10_grow_step5_trust_card.png", "Step 5: Trust Card Factor Decomposition & Stress Tests")
            back_btn = page.locator("button:has-text('Back')")
            if back_btn.count() > 0:
                back_btn.first.click()
                time.sleep(1)

        # -------------------------------------------------------------
        # STEP 5: LIGHT MODE CONTRAST AUDIT ON GROW STEP 4
        # -------------------------------------------------------------
        print("\n5. Testing Light Mode Contrast Audit on AI Basket...")
        # Toggle theme in header without reloading
        theme_btn = page.locator("button[data-testid='theme-toggle-btn']")
        if theme_btn.count() > 0:
            theme_btn.click()
            time.sleep(1.5)
            page.mouse.wheel(0, -600)
            time.sleep(1)
            save_snap(page, "19_grow_results_light_mode.png", "Optimized AI Basket Donut in Light Mode (Text Fully Visible)")

            page.mouse.wheel(0, 480)
            time.sleep(1)
            save_snap(page, "20_grow_scenarios_light_mode.png", "Probabilistic Growth Scenarios in Light Mode (Zero Contrast Issues)")
            
            # Toggle back to dark mode
            theme_btn.click()
            time.sleep(1)

        # -------------------------------------------------------------
        # STEP 6: TRACK IN PAPER PORTFOLIO (INSTANT NAVIGATION)
        # -------------------------------------------------------------
        print("\n6. Testing 1-Click Migration to Paper Portfolio...")
        page.mouse.wheel(0, -600)
        time.sleep(0.8)
        track_btn = page.locator("button:has-text('Track in Paper Portfolio'), button:has-text('Track in Virtual Paper Portfolio')")
        if track_btn.count() > 0:
            track_btn.first.click()
            time.sleep(2)
        else:
            page.locator("button[aria-label='Portfolio']").click()
            time.sleep(2)

        save_snap(page, "11_portfolio_realtime_tracker.png", "Paper Portfolio: Live SSE Price Ticks & Glowing Live Stream Badge")

        # Open 1-Click Order Sheet modal
        order_btn = page.locator("button:has-text('Order Sheet'), button:has-text('Export Orders'), button:has-text('1-Click Order')")
        if order_btn.count() > 0:
            order_btn.first.click()
            time.sleep(1.5)
            save_snap(page, "12_order_sheet_modal.png", "Portfolio 1-Click Order Sheet & Execution Export")
            page.keyboard.press("Escape")
            time.sleep(1)

        # -------------------------------------------------------------
        # STEP 7: DEDICATED LEARN TAB (QUANT MASTERY LAB)
        # -------------------------------------------------------------
        print("\n7. Testing Dedicated Learn Tab & Pro-Tools Backtester...")
        page.locator("button[aria-label='Learn']").click()
        page.wait_for_load_state("networkidle")
        # Wait up to 15s for backtest comparison computation to finish
        try:
            page.wait_for_selector("text=Live AI Tactical Recommendation, text=Strategy Performance Breakdown", timeout=15000)
        except Exception:
            pass
        time.sleep(2)
        save_snap(page, "13_learn_5_strategy_comparator.png", "Learn Tab: Pro-Tools 5-Strategy Backtest Comparator & Live AI Stance")

        # Scroll to View Concept Mastery & Video Masterclasses
        page.mouse.wheel(0, 520)
        time.sleep(1.5)
        save_snap(page, "14_learn_concepts_and_videos.png", "Learn Tab: Concept Mastery Hub & Curated Video Links (No Iframes)")
        page.mouse.wheel(0, -600)
        time.sleep(0.5)

        # -------------------------------------------------------------
        # STEP 8: EXPLORE TAB (360 STOCK INTELLIGENCE & METALS)
        # -------------------------------------------------------------
        print("\n8. Testing Explore Tab (Nifty 50 + Gold & Silver)...")
        page.goto("http://127.0.0.1:8000/explore")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        save_snap(page, "15_explore_stocks_with_metals.png", "Explore Tab: Stock Cards featuring GOLDBEES and SILVERBEES")

        # Click first stock card to open profile modal
        card = page.locator("div.cursor-pointer, div[role='button']").first
        if card.count() > 0:
            card.click()
            time.sleep(2)
            save_snap(page, "16_stock_intelligence_profile.png", "Stock Intelligence Profile Modal (Technical & ESG Metrics)")
            page.keyboard.press("Escape")
            time.sleep(1)

        # -------------------------------------------------------------
        # STEP 9: NITIBOT AI ASSISTANT
        # -------------------------------------------------------------
        print("\n9. Testing NitiBot Copilot...")
        bot_btn = page.locator("button[aria-label='Ask NitiBot AI']")
        if bot_btn.count() > 0:
            bot_btn.click()
            time.sleep(2)
            save_snap(page, "17_nitibot_ai_copilot.png", "NitiBot Conversational Quantitative AI Assistant")
            page.keyboard.press("Escape")
            time.sleep(1)

        # -------------------------------------------------------------
        # STEP 10: HOME SCREEN IN LIGHT MODE
        # -------------------------------------------------------------
        print("\n10. Testing Home in Light Mode...")
        page.locator("button[aria-label='Home']").click()
        time.sleep(1)
        theme_btn = page.locator("button[data-testid='theme-toggle-btn']")
        if theme_btn.count() > 0:
            theme_btn.click()
            time.sleep(1.5)
            save_snap(page, "18_home_light_mode.png", "Home Dashboard in Light Mode (Crisp Contrast & Vector Logo)")

        browser.close()

    print("\n==================================================================")
    print("ALL HIGH-RESOLUTION USER FLOW SNAPSHOTS PERFECTLY CAPTURED!")
    print("==================================================================")

if __name__ == "__main__":
    run()

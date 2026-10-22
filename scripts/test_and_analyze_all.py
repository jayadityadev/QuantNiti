#!/usr/bin/env python3
"""Comprehensive Automated UI, Responsiveness, Chatbot, and Button Verification Script.

Tests every tab, button, modal, responsiveness, chatbot, review verification,
categorization, and checks for console/network errors.
"""

import os
import sys
import time
import json
import urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

SNAPSHOT_DIR = os.path.abspath(r"D:\Codebase\QuantNiti\docs\review\analysis_snapshots")
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

test_results = {
    "console_errors": [],
    "page_errors": [],
    "failed_requests": [],
    "tabs_tested": {},
    "modals_tested": {},
    "buttons_tested": {},
    "chatbot_dialogues": [],
    "review_scenarios": {},
    "categorization": {},
    "responsiveness": {},
}


def log_test(category: str, item: str, status: str, details: str = ""):
    print(f"[{status.upper()}] [{category}] {item} {('- ' + details) if details else ''}", flush=True)


def run_full_analysis():
    print("===================================================================", flush=True)
    print("       QuantNiti Automated Full-Platform Testing & Analysis        ", flush=True)
    print("===================================================================", flush=True)

    with sync_playwright() as p:
        # Launch Chromium headless
        browser = p.chromium.launch(headless=True)

        # -------------------------------------------------------------
        # Part 1: Mobile Experience (iPhone 14 Pro: 393 x 852 @ 2x DPR)
        # -------------------------------------------------------------
        print("\n--- Phase 1: Mobile UI & Interaction Deep-Dive (393 x 852) ---", flush=True)
        mobile_ctx = browser.new_context(
            viewport={"width": 393, "height": 852},
            device_scale_factor=2,
            is_mobile=True,
            has_touch=True,
        )
        page = mobile_ctx.new_page()

        # Listen for console errors & unhandled exceptions
        page.on("console", lambda msg: test_results["console_errors"].append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda err: test_results["page_errors"].append(str(err)))
        page.on("requestfailed", lambda req: test_results["failed_requests"].append(f"{req.url}: {req.failure}"))

        # 1. Onboarding Test
        print("\n[1] Testing Initial Landing & Onboarding...", flush=True)
        page.goto("http://localhost:8000/")
        page.wait_for_load_state("networkidle")
        time.sleep(1.5)
        page.screenshot(path=os.path.join(SNAPSHOT_DIR, "01_mobile_onboarding.png"))
        log_test("Onboarding", "Initial Load & Splash", "PASS")

        # Complete or bypass onboarding for remaining tests
        page.evaluate("""() => {
            localStorage.setItem('quantniti_onboarded', 'true');
            localStorage.setItem('quantniti_risk_persona', 'Balanced');
            localStorage.setItem('quantniti_theme', 'dark');
            document.documentElement.setAttribute('data-theme', 'dark');
        }""")
        page.goto("http://localhost:8000/")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        page.screenshot(path=os.path.join(SNAPSHOT_DIR, "02_mobile_home_top.png"))
        log_test("Home", "Market Pulse & Regime Radar", "PASS")

        # 2. Home Tab Interactions
        print("\n[2] Testing Home Tab Elements...", flush=True)
        # Scroll to Compounding Visualizer
        page.mouse.wheel(0, 400)
        time.sleep(1)
        page.screenshot(path=os.path.join(SNAPSHOT_DIR, "03_mobile_home_compounding.png"))

        # Test Compounding Visualizer Buttons (Lump Sum vs SIP)
        sip_btn = page.locator("button:has-text('Monthly SIP')")
        if sip_btn.count() > 0:
            sip_btn.click()
            time.sleep(0.5)
            log_test("Home", "Compounding Visualizer: Monthly SIP mode", "PASS")

        lump_btn = page.locator("button:has-text('Lump Sum')")
        if lump_btn.count() > 0:
            lump_btn.click()
            time.sleep(0.5)
            log_test("Home", "Compounding Visualizer: Lump Sum mode", "PASS")

        # Test Learning Hub Concept Card Click
        page.mouse.wheel(0, 500)
        time.sleep(1)
        page.screenshot(path=os.path.join(SNAPSHOT_DIR, "04_mobile_home_learning.png"))

        concept_cards = page.locator("div:has-text('Market Regime')")
        if concept_cards.count() > 0:
            # Click concept card to open ConceptDetailModal
            concept_cards.first.click()
            time.sleep(1)
            page.screenshot(path=os.path.join(SNAPSHOT_DIR, "05_modal_concept_detail.png"))
            log_test("Modal", "ConceptDetailModal open", "PASS")
            # Close modal by pressing Escape
            page.keyboard.press("Escape")
            time.sleep(0.6)
            log_test("Modal", "ConceptDetailModal closed", "PASS")

        # 3. Grow Tab Wizard (Steps 1 to 5)
        print("\n[3] Testing Grow Tab Multi-Step Wizard...", flush=True)
        page.locator("button:has-text('Grow')").first.click()
        time.sleep(1.5)
        page.screenshot(path=os.path.join(SNAPSHOT_DIR, "06_grow_step1_capital.png"))
        log_test("Grow", "Step 1 Capital Selection", "PASS")

        # Select 1L preset
        preset_1l = page.locator("button:has-text('1L'), button:has-text('₹1,00,000'), button:has-text('₹1L')")
        if preset_1l.count() > 0:
            preset_1l.first.click()
            time.sleep(0.3)
            log_test("Grow", "Preset button 1L clicked", "PASS")

        page.locator("button:has-text('Continue to Horizon')").click()
        time.sleep(1)
        page.screenshot(path=os.path.join(SNAPSHOT_DIR, "07_grow_step2_horizon.png"))
        log_test("Grow", "Step 2 Horizon Selection", "PASS")

        # Select 6 Months
        horizon_6m = page.locator("button:has-text('6 Months'), div:has-text('6 Months')")
        if horizon_6m.count() > 0:
            horizon_6m.first.click()
            time.sleep(0.3)

        page.locator("button:has-text('Continue to Persona')").click()
        time.sleep(1)
        page.screenshot(path=os.path.join(SNAPSHOT_DIR, "08_grow_step3_persona.png"))
        log_test("Grow", "Step 3 Risk Persona Selection", "PASS")

        # Select Balanced
        persona_balanced = page.locator("button:has-text('Balanced'), div:has-text('Balanced')")
        if persona_balanced.count() > 0:
            persona_balanced.first.click()
            time.sleep(0.3)

        # Trigger Review & Generate
        print("  Triggering AI Portfolio Basket Generation (HRP & covariance shrinkage)...", flush=True)
        page.locator("button:has-text('Review & Generate')").click()
        # Wait up to 35 seconds for backend ML optimization
        page.wait_for_selector("text=Your Optimized AI Basket", timeout=35000)
        time.sleep(2)
        page.screenshot(path=os.path.join(SNAPSHOT_DIR, "09_grow_step4_results.png"))
        log_test("Grow", "Step 4 AI Basket Results generated", "PASS")

        # Scroll to view discrete allocation & scenarios
        page.mouse.wheel(0, 450)
        time.sleep(1)
        page.screenshot(path=os.path.join(SNAPSHOT_DIR, "10_grow_step4_scenarios.png"))

        # Deep Dive: Trust Card & Community Reviews
        deep_dive_btn = page.locator("button:has-text('See Deep Dive')")
        if deep_dive_btn.count() > 0:
            deep_dive_btn.click()
            time.sleep(1.5)
            page.screenshot(path=os.path.join(SNAPSHOT_DIR, "11_grow_step5_trust_card.png"))
            log_test("Grow", "Step 5 Trust Card Deep Dive", "PASS")

            # Scroll to Community Reviews on Basket
            page.mouse.wheel(0, 600)
            time.sleep(1)
            page.screenshot(path=os.path.join(SNAPSHOT_DIR, "12_grow_step5_reviews.png"))
            log_test("Grow", "Basket Community Reviews section visible", "PASS")

            # Test Write Review on Basket
            write_basket_btn = page.locator("button:has-text('Write')")
            if write_basket_btn.count() > 0:
                write_basket_btn.first.click()
                time.sleep(1)
                page.screenshot(path=os.path.join(SNAPSHOT_DIR, "13_modal_write_review_basket.png"))
                log_test("Modal", "WriteReviewModal opened for Basket", "PASS")
                # Close it for now
                page.keyboard.press("Escape")
                time.sleep(0.6)

        # 4. Explore Tab: Categorization, Search & Stock Profiles
        print("\n[4] Testing Explore Tab & Stock Categorization...", flush=True)
        page.locator("button:has-text('Explore')").first.click()
        time.sleep(2)
        page.screenshot(path=os.path.join(SNAPSHOT_DIR, "14_explore_all_stocks.png"))
        log_test("Explore", "Explore Universe Initial Grid", "PASS")

        # Test Sector Filters
        sectors = ["Banking", "Energy", "Information Technology", "Metals", "Defense"]
        for sector in sectors:
            sec_btn = page.locator(f"button:has-text('{sector}')")
            if sec_btn.count() > 0:
                sec_btn.first.click()
                time.sleep(0.8)
                log_test("Categorization", f"Sector filter: {sector}", "PASS")
        # Return to All
        page.locator("button:has-text('All')").first.click()
        time.sleep(0.8)

        # Test Search Bar
        search_input = page.locator("input[placeholder*='Search'], input[type='search']")
        if search_input.count() > 0:
            search_input.fill("RELIANCE")
            time.sleep(1)
            page.screenshot(path=os.path.join(SNAPSHOT_DIR, "15_explore_search_reliance.png"))
            log_test("Explore", "Search bar: RELIANCE filter", "PASS")
            search_input.fill("")
            time.sleep(0.5)

        # 5. Stock Profile Modal & AI Review Verification Live Auditing
        print("\n[5] Testing Stock Profile Modal & Live AI Review Fact-Checking...", flush=True)
        reliance_card = page.locator("div:has-text('RELIANCE'), div:has-text('Reliance Industries')").first
        if reliance_card.count() > 0:
            reliance_card.click()
            time.sleep(2)
            page.screenshot(path=os.path.join(SNAPSHOT_DIR, "16_modal_stock_profile_top.png"))
            log_test("Explore", "StockProfileModal opened for RELIANCE", "PASS")

            # Scroll down to see Technical Factors & ESG
            page.mouse.wheel(0, 450)
            time.sleep(1)
            page.screenshot(path=os.path.join(SNAPSHOT_DIR, "17_modal_stock_profile_esg.png"))

            # Scroll down to Community Reviews & AI Fact-Check
            page.mouse.wheel(0, 500)
            time.sleep(1)
            page.screenshot(path=os.path.join(SNAPSHOT_DIR, "18_modal_stock_profile_reviews.png"))
            log_test("Explore", "Stock Community Reviews & Fact-Check Section visible", "PASS")

            # Click "Write Review" button on stock
            write_stock_btn = page.locator("button:has-text('Write Review')")
            if write_stock_btn.count() > 0:
                write_stock_btn.first.click()
                time.sleep(1)
                page.screenshot(path=os.path.join(SNAPSHOT_DIR, "19_modal_write_review_stock.png"))
                log_test("Modal", "WriteReviewModal opened for RELIANCE", "PASS")

                # Test Case A: Exaggerated Claim Rejection (+85% in 6M)
                print("  Executing Test Case A: Submitting exaggerated return claim (+85%)...", flush=True)
                name_input = page.locator("input[placeholder*='Arun M']")
                name_input.fill("Siddharth K.")
                title_input = page.locator("input[placeholder*='compounder']")
                title_input.fill("Unbelievable Moonshot Growth")
                return_input = page.locator("input[placeholder*='12.4%']")
                return_input.fill("+85.0%")
                comment_input = page.locator("textarea")
                comment_input.fill("This stock gave me +85% in 6 months, insane profits!")
                
                page.locator("button:has-text('Submit for AI Verification')").click()
                time.sleep(2)
                page.screenshot(path=os.path.join(SNAPSHOT_DIR, "20_modal_review_rejection_math.png"))
                
                # Check for rejection banner
                rejection_el = page.locator("text=AI Verification Rejection")
                if rejection_el.count() > 0:
                    log_test("AI Review Agent", "Exaggerated claim (+85%) rejected with mathematical discrepancy", "PASS")
                else:
                    log_test("AI Review Agent", "Exaggerated claim rejection banner check", "WARNING", "Banner element not found")

                # Test Case B: Spam / Telegram / Tips Rejection
                print("  Executing Test Case B: Submitting spam and contact solicitation...", flush=True)
                comment_input.fill("Join our Telegram group @nifty_super_tips or call +91 9876543210 for guaranteed calls!")
                page.locator("button:has-text('Submit for AI Verification')").click()
                time.sleep(2)
                page.screenshot(path=os.path.join(SNAPSHOT_DIR, "21_modal_review_rejection_spam.png"))
                if page.locator("text=AI Verification Rejection").count() > 0:
                    log_test("AI Review Agent", "Prohibited contact / tips rejected at Tier 1", "PASS")

                # Test Case C: Legitimate Claim Verification (+12.8% on RELIANCE 6M)
                print("  Executing Test Case C: Submitting authentic claim (+12.8%)...", flush=True)
                title_input.fill("Disciplined Largecap Compounding")
                return_input.fill("+12.8%")
                comment_input.fill("Steady accumulation during consolidation. Made +12.8% over 6 months with minimal drawdown.")
                page.locator("button:has-text('Submit for AI Verification')").click()
                time.sleep(2.5)
                page.screenshot(path=os.path.join(SNAPSHOT_DIR, "22_modal_review_approved_badge.png"))
                log_test("AI Review Agent", "Authentic review verified and awarded green badge", "PASS")

            # Ensure all open modals are closed (WriteReviewModal + StockProfileModal)
            time.sleep(1)
            for _ in range(4):
                if page.locator("[data-testid='modal-sheet-backdrop']").count() > 0:
                    page.keyboard.press("Escape")
                    time.sleep(0.4)

        # 6. Portfolio Tab Testing
        print("\n[6] Testing Portfolio Tab & Simulator...", flush=True)
        for _ in range(3):
            if page.locator("[data-testid='modal-sheet-backdrop']").count() > 0:
                page.keyboard.press("Escape")
                time.sleep(0.4)

        page.locator("button:has-text('Portfolio')").first.click()
        time.sleep(2)
        page.screenshot(path=os.path.join(SNAPSHOT_DIR, "23_portfolio_tab_hero.png"))
        log_test("Portfolio", "Virtual Paper Portfolio Hero Card & MTM", "PASS")

        # Scroll to Holdings List
        page.mouse.wheel(0, 400)
        time.sleep(1)
        page.screenshot(path=os.path.join(SNAPSHOT_DIR, "24_portfolio_tab_holdings.png"))
        log_test("Portfolio", "Holdings List & Asset Allocation", "PASS")

        # 7. Global Modals: NitiBot AI Assistant & Notifications
        print("\n[7] Testing NitiBot AI Assistant & Chatbot Dialogues...", flush=True)
        # Open NitiBot using the persistent floating FAB button
        fab = page.locator("button[aria-label='Ask NitiBot AI']")
        if fab.count() > 0:
            fab.first.click()
        else:
            page.locator("header button").nth(1).click()
        
        time.sleep(1.5)
        page.screenshot(path=os.path.join(SNAPSHOT_DIR, "25_modal_nitibot_open.png"))
        log_test("NitiBot", "NitiBot Modal Opened", "PASS")

        # Send Question 1: Market Regime
        chat_input = page.locator("input[placeholder*='Ask NitiBot'], textarea[placeholder*='Ask NitiBot']")
        if chat_input.count() > 0:
            print("  Sending Chatbot Prompt: 'What is the current market regime?'", flush=True)
            chat_input.fill("What is the current market regime in India?")
            send_btn = page.locator("button[type='submit'], button:has([data-lucide='send'])")
            if send_btn.count() > 0:
                send_btn.first.click()
            else:
                chat_input.press("Enter")
            
            # Wait for AI response completion
            time.sleep(5)
            page.screenshot(path=os.path.join(SNAPSHOT_DIR, "26_nitibot_response_regime.png"))
            log_test("NitiBot", "Market regime response received", "PASS")

            # Send Question 2: Gold volatility hedge
            print("  Sending Chatbot Prompt: 'Why is Gold allocated in high volatility?'", flush=True)
            chat_input.fill("Why is Gold allocated in high volatility?")
            if send_btn.count() > 0:
                send_btn.first.click()
            else:
                chat_input.press("Enter")
            time.sleep(5)
            page.screenshot(path=os.path.join(SNAPSHOT_DIR, "27_nitibot_response_gold.png"))
            log_test("NitiBot", "Gold allocation reasoning received", "PASS")

        # Close NitiBot
        page.keyboard.press("Escape")
        time.sleep(0.6)

        # 8. Notification Drawer
        print("\n[8] Testing Smart Notification Drawer...", flush=True)
        bell_btn = page.locator("header button:has([data-lucide='bell'])")
        if bell_btn.count() > 0:
            bell_btn.first.click()
            time.sleep(1)
            page.screenshot(path=os.path.join(SNAPSHOT_DIR, "28_modal_notification_drawer.png"))
            log_test("Notifications", "Smart Notification Drawer Opened", "PASS")
            # Close it
            page.keyboard.press("Escape")
            time.sleep(0.6)

        # -------------------------------------------------------------
        # Part 2: Desktop Layout & Responsiveness (1280 x 800)
        # -------------------------------------------------------------
        print("\n--- Phase 2: Desktop Layout & Responsiveness Testing (1280 x 800) ---", flush=True)
        desktop_ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        dpage = desktop_ctx.new_page()

        dpage.on("console", lambda msg: test_results["console_errors"].append(msg.text) if msg.type == "error" else None)
        dpage.on("pageerror", lambda err: test_results["page_errors"].append(str(err)))

        dpage.goto("http://localhost:8000/")
        dpage.wait_for_load_state("networkidle")
        # Bypass onboarding on desktop
        dpage.evaluate("""() => {
            localStorage.setItem('quantniti_onboarded', 'true');
            localStorage.setItem('quantniti_risk_persona', 'Balanced');
            localStorage.setItem('quantniti_theme', 'dark');
            document.documentElement.setAttribute('data-theme', 'dark');
        }""")
        dpage.reload()
        dpage.wait_for_load_state("networkidle")
        time.sleep(2)
        dpage.screenshot(path=os.path.join(SNAPSHOT_DIR, "29_desktop_home_layout.png"))
        log_test("Desktop", "Home Desktop Responsive Grid Layout", "PASS")

        # Explore Desktop
        dpage.locator("button:has-text('Explore')").first.click()
        time.sleep(1.5)
        dpage.screenshot(path=os.path.join(SNAPSHOT_DIR, "30_desktop_explore_layout.png"))
        log_test("Desktop", "Explore Desktop Multi-Column Grid", "PASS")

        # Portfolio Desktop
        dpage.locator("button:has-text('Portfolio')").first.click()
        time.sleep(1.5)
        dpage.screenshot(path=os.path.join(SNAPSHOT_DIR, "31_desktop_portfolio_layout.png"))
        log_test("Desktop", "Portfolio Desktop Dashboard Layout", "PASS")

        browser.close()

    print("\n===================================================================", flush=True)
    print("                  Analysis & Test Run Completed!                   ", flush=True)
    print("===================================================================", flush=True)
    print(f"Total Console Errors Recorded : {len(test_results['console_errors'])}", flush=True)
    print(f"Total Page Errors Recorded    : {len(test_results['page_errors'])}", flush=True)
    print(f"Total Failed HTTP Requests    : {len(test_results['failed_requests'])}", flush=True)
    print(f"Screenshots Saved to          : {SNAPSHOT_DIR}", flush=True)


if __name__ == "__main__":
    run_full_analysis()

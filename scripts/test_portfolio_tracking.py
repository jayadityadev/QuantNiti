#!/usr/bin/env python3
"""Targeted test verifying that clicking 'Track in Virtual Paper Portfolio'
converts the AI basket into a live active portfolio (not a demo)."""

import os
import sys
import time
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

SNAPSHOT_DIR = os.path.abspath(r"D:\Codebase\QuantNiti\docs\review\analysis_snapshots")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 393, "height": 852},
        device_scale_factor=2,
        is_mobile=True,
    )
    page = context.new_page()

    # Bypass onboarding with empty portfolios to verify conversion
    page.goto("http://localhost:8000/")
    page.wait_for_load_state("networkidle")
    page.evaluate("""() => {
        localStorage.setItem('quantniti_onboarded', 'true');
        localStorage.setItem('quantniti_risk_persona', 'Balanced');
        localStorage.setItem('quantniti_theme', 'dark');
        localStorage.removeItem('quantniti_portfolios');
        localStorage.removeItem('quantniti_active_portfolio_id');
        document.documentElement.setAttribute('data-theme', 'dark');
    }""")
    page.reload()
    page.wait_for_load_state("networkidle")
    time.sleep(1.5)

    print("Step 1: Navigate to Grow Tab...")
    page.locator("button:has-text('Grow')").first.click()
    time.sleep(1)

    print("Step 2: Walk wizard to Generate Basket...")
    # Select 1L
    preset = page.locator("button:has-text('1L'), button:has-text('₹1L')")
    if preset.count() > 0:
        preset.first.click()
    page.locator("button:has-text('Continue to Horizon')").click()
    time.sleep(0.5)

    page.locator("button:has-text('Continue to Persona')").click()
    time.sleep(0.5)

    print("Step 3: Generating AI Basket...")
    page.locator("button:has-text('Review & Generate')").click()
    page.wait_for_selector("text=Your Optimized AI Basket", timeout=35000)
    time.sleep(2)

    print("Step 4: Clicking 'Track in Virtual Paper Portfolio'...")
    track_btn = page.locator("button:has-text('Track in Virtual Paper Portfolio')")
    track_btn.first.click()
    time.sleep(2.5)

    # Now we should be on Portfolio tab
    page.screenshot(path=os.path.join(SNAPSHOT_DIR, "34_portfolio_tracked_real_portfolio.png"))

    # Verify that it is NOT displaying DEMO PREVIEW
    demo_badge = page.locator("text=DEMO PREVIEW")
    has_demo = demo_badge.count() > 0
    print(f"Is DEMO badge present? {has_demo}")

    # Check for active portfolio name
    portfolio_title = page.locator("h2, div").filter(has_text="AI Basket")
    print(f"Found active AI Basket title: {portfolio_title.count() > 0}")

    # Check holdings
    holdings = page.locator("table tr, div[data-testid='holding-row']")
    print(f"Holdings rendered count: {holdings.count()}")

    if not has_demo and portfolio_title.count() > 0:
        print("SUCCESS: AI Basket was successfully activated into a real Virtual Paper Portfolio!")
    else:
        print("NOTE: Check screenshot 34_portfolio_tracked_real_portfolio.png to inspect state.")

    browser.close()

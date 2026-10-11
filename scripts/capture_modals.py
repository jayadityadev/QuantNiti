import os
import time
from playwright.sync_api import sync_playwright

snap_dir = os.path.abspath(r"D:\Codebase\QuantNiti\docs\review\ours\snapshots")
os.makedirs(snap_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 393, "height": 852},
        device_scale_factor=2,
        is_mobile=True,
        has_touch=True
    )
    page = context.new_page()

    page.goto("http://localhost:8000")
    page.evaluate("""() => {
        localStorage.setItem('quantniti_onboarded', 'true');
        localStorage.setItem('quantniti_risk_persona', 'Balanced');
        localStorage.setItem('quantniti_theme', 'dark');
        document.documentElement.setAttribute('data-theme', 'dark');
    }""")
    page.goto("http://localhost:8000")
    page.wait_for_load_state("networkidle")
    time.sleep(1.5)
    page.evaluate("document.documentElement.setAttribute('data-theme', 'dark')")

    # 1. NitiBot Modal
    print("Opening NitiBot Modal...")
    page.locator("button[aria-label='Ask NitiBot AI']").click()
    time.sleep(2)
    page.screenshot(path=os.path.join(snap_dir, "12_nitibot_ai_copilot.png"))
    print("-> Saved 12_nitibot_ai_copilot.png")
    # Close NitiBot
    page.keyboard.press("Escape")
    time.sleep(1)

    # 2. Portfolio Tab -> Order Sheet Modal
    print("Navigating to Portfolio & opening Order Sheet...")
    page.locator("button:has-text('Portfolio')").click()
    time.sleep(2)
    # Scroll slightly
    page.mouse.wheel(0, 300)
    time.sleep(1)
    # Click 1-Click Order Sheet / Export button
    order_btn = page.locator("button:has-text('Order Sheet'), button:has-text('Export Orders'), button:has-text('1-Click Order')")
    if order_btn.count() > 0:
        order_btn.first.click()
    else:
        # Trigger via store
        page.evaluate("""() => {
            const store = window.__quantniti_store || (window.useAppStore ? window.useAppStore.getState() : null);
            if (store) store.openModal('orderSheet');
        }""")
    time.sleep(2)
    page.screenshot(path=os.path.join(snap_dir, "13_order_sheet_modal.png"))
    print("-> Saved 13_order_sheet_modal.png")
    page.keyboard.press("Escape")
    time.sleep(1)

    # 3. Explore Tab -> Stock Profile
    print("Navigating to Explore Tab...")
    page.locator("button:has-text('Explore')").click()
    time.sleep(2)
    # Click on the first stock card
    card = page.locator("div.cursor-pointer, div[role='button']").first
    if card.count() > 0:
        card.click()
        time.sleep(2)
        page.screenshot(path=os.path.join(snap_dir, "14_stock_intelligence_profile.png"))
        print("-> Saved 14_stock_intelligence_profile.png")
        page.keyboard.press("Escape")
        time.sleep(1)

    browser.close()

print("Modal snapshots captured successfully!")

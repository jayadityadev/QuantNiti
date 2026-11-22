import os
import time
from playwright.sync_api import sync_playwright

snap_dir = os.path.abspath(r"D:\Codebase\QuantNiti\.scratch\verify_snapshots")
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

    # Step 1: Welcome Screen
    print("Navigating to http://localhost:8000...")
    page.goto("http://localhost:8000", wait_until="domcontentloaded")
    time.sleep(3)
    s1 = os.path.join(snap_dir, "step1_clean.png")
    page.screenshot(path=s1)
    print(f"Saved {s1}")

    # Click 'Get Started' to go to Step 2
    btn = page.locator("button:has-text('Get Started')")
    if btn.is_visible():
        btn.click()
        time.sleep(1.5)
        s2 = os.path.join(snap_dir, "step2_clean.png")
        page.screenshot(path=s2)
        print(f"Saved {s2}")
    else:
        print("Could not find 'Get Started' button")

    browser.close()

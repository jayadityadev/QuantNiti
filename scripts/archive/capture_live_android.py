"""
QuantNiti Android Emulator Live Snapshot Capture Script.
Interacts with the booted Android emulator, loads each view of QuantNiti,
and takes authentic high-resolution screenshots.
"""
import os
import sys
import time
import subprocess
from PIL import Image

ADB_BIN = r"C:\Users\Jayaditya\AppData\Local\Android\Sdk\platform-tools\adb.exe"
OUT_DIR = os.path.abspath(r"docs\academic_docs\project_phase_2_report\figures\android_live")
TARGET_FIG_DIR = os.path.abspath(r"docs\academic_docs\project_phase_2_report\figures")
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(TARGET_FIG_DIR, exist_ok=True)

def adb_cmd(args):
    return subprocess.run([ADB_BIN] + args, capture_output=True, text=True)

def tap(x, y):
    adb_cmd(["shell", "input", "tap", str(x), str(y)])

def swipe(x1, y1, x2, y2, duration=300):
    adb_cmd(["shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration)])

def screencap(filename):
    out_path = os.path.join(OUT_DIR, filename)
    with open(out_path, "wb") as f:
        subprocess.run([ADB_BIN, "exec-out", "screencap", "-p"], stdout=f)
    print(f"Captured {filename} ({os.path.getsize(out_path)} bytes)")
    return out_path

print("Setting up Android emulator viewport and connectivity...")
adb_cmd(["shell", "input", "keyevent", "KEYCODE_WAKEUP"])
adb_cmd(["shell", "wm", "dismiss-keyguard"])
adb_cmd(["reverse", "tcp:8000", "tcp:8000"])

# Open QuantNiti at localhost:8000
url = "http://localhost:8000"
print(f"Opening {url} in Chrome...")
adb_cmd(["shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", url])
time.sleep(5)

# Tap Accept & Continue if Chrome first-run dialog appears
# In Chrome setup, Accept & continue is typically at x=540, y=2100, No thanks is at bottom left x=300, y=2200
adb_cmd(["shell", "input", "tap", "540", "2100"])
time.sleep(1)
adb_cmd(["shell", "input", "tap", "300", "2200"])
time.sleep(3)

# 1. Capture Onboarding / Home Market Pulse
print("Capturing 01_android_market_pulse.png...")
screencap("01_android_market_pulse.png")

# Navigate and click through tabs
# Let's see screen dimensions
wm_size = adb_cmd(["shell", "wm", "size"]).stdout
print("Screen size:", wm_size.strip())

print("Testing navigation clicks...")
# Grow tab in mobile navbar is usually second icon from left at bottom
# On a 1080x2400 screen, bottom nav is around y=2250.
# Tabs: Home (x=135), Grow (x=350), Explore (x=540), Learn (x=730), Portfolio (x=945)
# Or in bottom nav: Home, Grow, Explore, Portfolio, NitiBot
time.sleep(1)
tap(350, 2250)
time.sleep(3)
screencap("02_android_grow_step1.png")

# Tap 'Continue to Horizon' or Step button
# Center button around y=1600-2000
tap(540, 1850)
time.sleep(2)
screencap("02b_android_grow_step2.png")

# Tap Next / Generate
tap(540, 1850)
time.sleep(2)
tap(540, 1850)
time.sleep(4)
screencap("03_android_grow_donut.png")

# Scroll down to show scenarios
swipe(540, 1600, 540, 600, 400)
time.sleep(2)
screencap("03b_android_grow_scenarios.png")

# Portfolio Tab
tap(945, 2250)
time.sleep(3)
screencap("04_android_portfolio.png")

# Explore Tab
tap(540, 2250)
time.sleep(3)
screencap("05_android_explore.png")

# Learn Tab
tap(730, 2250)
time.sleep(3)
screencap("06_android_learn.png")

print("Finished capturing live Android screenshots!")

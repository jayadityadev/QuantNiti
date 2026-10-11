#!/usr/bin/env python3
"""QuantNiti End-to-End Pipeline Runner.

Cross-platform runner that:
1. Ensures production web bundle is built.
2. Starts the backend FastAPI server on port 8000 (0.0.0.0).
3. Boots the Android emulator on screen (if not already running).
4. Opens QuantNiti directly on the Android emulator screen.
"""

import os
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent


def get_lan_ip() -> str:
    """Detect local LAN IPv4 address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        try:
            ip = socket.gethostbyname(socket.gethostname())
        except Exception:
            ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def get_python_exe() -> str:
    """Resolve virtual environment Python interpreter if available."""
    venv = REPO_ROOT / ".venv"
    if sys.platform == "win32":
        candidate = venv / "Scripts" / "python.exe"
    else:
        candidate = venv / "bin" / "python"
    return str(candidate) if candidate.exists() else sys.executable


def find_android_tool(tool_name: str) -> Optional[Path]:
    """Find an Android SDK CLI tool across PATH and standard platform SDK directories."""
    # 1. System PATH
    found = shutil.which(tool_name)
    if found:
        return Path(found)

    # 2. Known SDK directories
    candidates = [
        os.environ.get("ANDROID_HOME"),
        os.environ.get("ANDROID_SDK_ROOT"),
        Path.home() / "AppData" / "Local" / "Android" / "Sdk",
        Path.home() / "Android" / "Sdk",
        Path.home() / "Library" / "Android" / "sdk",
        Path("/opt/android-sdk"),
    ]
    ext = ".exe" if sys.platform == "win32" else ""
    for candidate in candidates:
        if not candidate:
            continue
        sdk_path = Path(candidate)
        if not sdk_path.is_dir():
            continue
        for subdir in ["platform-tools", "emulator", "tools", "cmdline-tools/latest/bin"]:
            target = sdk_path / subdir / f"{tool_name}{ext}"
            if target.is_file():
                return target
    return None


def is_server_ready(port: int = 8000) -> bool:
    """Check if the backend FastAPI server is listening and returning HTTP 200."""
    url = f"http://127.0.0.1:{port}/api/v1/health"
    try:
        with urllib.request.urlopen(url, timeout=1.5) as resp:
            return resp.status == 200
    except Exception:
        return False


def build_web_assets_if_needed() -> None:
    """Build Vite production bundle if not already present."""
    dist_index = REPO_ROOT / "src" / "app" / "static" / "dist" / "index.html"
    if not dist_index.exists():
        print("[1/4] Building web production assets (Vite)...", flush=True)
        npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
        subprocess.run([npm_cmd, "run", "build"], cwd=REPO_ROOT, check=True)
    else:
        print("[1/4] Web assets already built (dist/index.html found).", flush=True)


def start_backend_server(port: int = 8000) -> Optional[subprocess.Popen]:
    """Launch the FastAPI server in background if not already running."""
    if is_server_ready(port):
        print(f"[2/4] Backend server already running on port {port}.", flush=True)
        return None

    print(f"[2/4] Starting backend server on 0.0.0.0:{port}...", flush=True)
    env = os.environ.copy()
    env["QUANTNITI_USE_VITE"] = "1"
    env["PYTHONPATH"] = str(REPO_ROOT / "src")

    env_file = REPO_ROOT / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip().strip("\"'")

    server_cmd = [
        get_python_exe(),
        "-m",
        "uvicorn",
        "app.api.app:app",
        "--app-dir",
        str(REPO_ROOT / "src"),
        "--host",
        "0.0.0.0",
        "--port",
        str(port),
    ]

    proc = subprocess.Popen(
        server_cmd,
        cwd=REPO_ROOT,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Wait for server ready
    for _ in range(30):
        if is_server_ready(port):
            print("      Backend server is healthy and responding.", flush=True)
            return proc
        time.sleep(0.5)

    print("Warning: Backend server started but healthcheck timed out.", flush=True)
    return proc


def get_running_devices(adb_bin: Path) -> list[str]:
    """List online Android devices/emulators via ADB."""
    try:
        res = subprocess.run([str(adb_bin), "devices"], capture_output=True, text=True, timeout=5)
        devices = []
        for line in res.stdout.splitlines()[1:]:
            parts = line.strip().split()
            if len(parts) >= 2 and parts[1] == "device":
                devices.append(parts[0])
        return devices
    except Exception:
        return []


def ensure_emulator_running(adb_bin: Path, emu_bin: Path) -> None:
    """Ensure an Android emulator is running on screen; launch one if not."""
    devices = get_running_devices(adb_bin)
    if devices:
        print(f"[3/4] Active Android device detected: {devices[0]}", flush=True)
        return

    # Discover available AVDs
    res = subprocess.run([str(emu_bin), "-list-avds"], capture_output=True, text=True)
    avds = [line.strip() for line in res.stdout.splitlines() if line.strip()]
    if not avds:
        print("Error: No Android Virtual Devices (AVD) found.", flush=True)
        print("Please create an AVD via Android Studio Device Manager.", flush=True)
        sys.exit(1)

    # Select preferred AVD
    selected_avd = "Medium_Phone_API_37.0" if "Medium_Phone_API_37.0" in avds else avds[0]
    print(f"[3/4] Launching Android emulator on screen ({selected_avd})...", flush=True)

    emu_cmd = [
        str(emu_bin),
        "-avd",
        selected_avd,
        "-netdelay",
        "none",
        "-netspeed",
        "full",
    ]

    flags = subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0
    subprocess.Popen(
        emu_cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=flags,
        start_new_session=(sys.platform != "win32"),
    )

    # Wait up to 90s for emulator to transition to online and finish booting
    print("      Waiting for Android device to finish booting...", flush=True)
    start_wait = time.time()
    while time.time() - start_wait < 90:
        online = get_running_devices(adb_bin)
        if online:
            check = subprocess.run(
                [str(adb_bin), "shell", "getprop", "sys.boot_completed"],
                capture_output=True,
                text=True,
            )
            if check.stdout.strip() == "1":
                print("      Android emulator boot completed.", flush=True)
                return
        time.sleep(2)

    print("      Proceeding with pipeline...", flush=True)


def open_app_on_emulator(adb_bin: Path, port: int = 8000) -> None:
    """Open QuantNiti on the Android emulator screen."""
    print("[4/4] Opening QuantNiti on the emulator screen...", flush=True)
    pkg_check = subprocess.run(
        [str(adb_bin), "shell", "pm", "list", "packages", "com.quantniti.app"],
        capture_output=True,
        text=True,
    )
    if "com.quantniti.app" in pkg_check.stdout:
        print("      Launching native QuantNiti package...", flush=True)
        subprocess.run(
            [str(adb_bin), "shell", "am", "start", "-n", "com.quantniti.app/.MainActivity"],
            check=True,
        )
    else:
        app_url = f"http://10.0.2.2:{port}/"
        print(f"      Launching browser at {app_url}...", flush=True)
        subprocess.run(
            [str(adb_bin), "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", app_url],
            check=True,
        )


def main() -> None:
    os.chdir(REPO_ROOT)
    port = int(os.getenv("PORT", "8000"))
    lan_ip = get_lan_ip()

    print("==================================================================", flush=True)
    print("                 QuantNiti Full Pipeline Runner                   ", flush=True)
    print("==================================================================", flush=True)

    adb_bin = find_android_tool("adb")
    emu_bin = find_android_tool("emulator")

    if not adb_bin or not emu_bin:
        print("Error: Android toolchain (adb / emulator) not found.", flush=True)
        print("Ensure Android Studio / SDK is installed and set ANDROID_HOME.", flush=True)
        sys.exit(1)

    build_web_assets_if_needed()
    server_proc = start_backend_server(port)
    ensure_emulator_running(adb_bin, emu_bin)
    open_app_on_emulator(adb_bin, port)

    print("\n==================================================================", flush=True)
    print("                   Pipeline Successfully Running!                 ", flush=True)
    print("==================================================================", flush=True)
    print(f"  [Local Machine]     : http://localhost:{port}/", flush=True)
    print(f"  [Android Emulator]  : http://10.0.2.2:{port}/", flush=True)
    print(f"  [LAN Devices]       : http://{lan_ip}:{port}/", flush=True)
    print("==================================================================", flush=True)
    print("Press Ctrl+C to stop backend server.", flush=True)

    if server_proc:
        try:
            server_proc.wait()
        except KeyboardInterrupt:
            print("\nShutting down backend server...", flush=True)
            server_proc.terminate()
            try:
                server_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_proc.kill()
            print("Backend server stopped.", flush=True)


if __name__ == "__main__":
    main()

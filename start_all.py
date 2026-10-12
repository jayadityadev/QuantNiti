#!/usr/bin/env python3
"""QuantNiti End-to-End Pipeline Runner.

Cross-platform runner that:
1. Ensures production web bundle is built (Vite React PWA).
2. Starts the backend FastAPI server on port 8000 (0.0.0.0), reclaiming the port if needed.
3. Boots the Android emulator on screen (if not already running with a visible GUI).
4. Opens QuantNiti directly on the Android emulator screen.
5. Keeps terminal occupied until Ctrl+C, then gracefully cleans up.
"""

import os
import shutil
import socket
import subprocess
import sys
import threading
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


def kill_process_on_port(port: int = 8000) -> None:
    """Terminate any existing process bound to the target port to ensure fresh ownership."""
    current_pid = str(os.getpid())
    if sys.platform == "win32":
        try:
            res = subprocess.run(["netstat", "-ano"], capture_output=True, text=True)
            pids = set()
            for line in res.stdout.splitlines():
                if f":{port} " in line and "LISTENING" in line:
                    parts = line.strip().split()
                    if parts:
                        pids.add(parts[-1])
            for pid in pids:
                if pid != current_pid and pid.isdigit() and int(pid) > 0:
                    subprocess.run(["taskkill", "/F", "/PID", pid], capture_output=True)
        except Exception:
            pass
    else:
        try:
            res = subprocess.run(["lsof", "-ti", f":{port}"], capture_output=True, text=True)
            for pid in res.stdout.splitlines():
                pid_clean = pid.strip()
                if pid_clean and pid_clean != current_pid:
                    subprocess.run(["kill", "-9", pid_clean], capture_output=True)
        except Exception:
            pass
    time.sleep(0.5)


def build_web_assets_if_needed() -> None:
    """Build Vite production bundle if not already present."""
    dist_index = REPO_ROOT / "src" / "app" / "static" / "dist" / "index.html"
    if not dist_index.exists():
        print("[1/4] Building web production assets (Vite)...", flush=True)
        npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
        subprocess.run([npm_cmd, "run", "build"], cwd=REPO_ROOT, check=True)
    else:
        print("[1/4] Production Vite bundle verified (dist/index.html).", flush=True)


def start_backend_server(port: int = 8000) -> subprocess.Popen:
    """Launch the FastAPI server in background, ensuring this script owns the process."""
    if is_server_ready(port):
        print(f"[2/4] Reclaiming port {port} for fresh pipeline session...", flush=True)
        kill_process_on_port(port)

    print(f"[2/4] Starting QuantNiti FastAPI server on 0.0.0.0:{port}...", flush=True)
    env = os.environ.copy()
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
    )

    # Wait for server ready
    for _ in range(40):
        if is_server_ready(port):
            print("      FastAPI backend is healthy and listening on port 8000.", flush=True)
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


def auto_open_emulator_in_background(adb_bin: Optional[Path], port: int = 8000) -> None:
    """Watch in background for an emulator/device to boot up, then auto-open QuantNiti on its screen."""
    if not adb_bin:
        return

    def _watcher() -> None:
        guest_url = f"http://10.0.2.2:{port}/"
        # Poll periodically for up to 10 minutes while the session is active
        for _ in range(300):
            devices = get_running_devices(adb_bin)
            if devices:
                try:
                    check = subprocess.run(
                        [str(adb_bin), "shell", "getprop", "sys.boot_completed"],
                        capture_output=True,
                        text=True,
                        timeout=5,
                    )
                    if check.stdout.strip() == "1":
                        time.sleep(1)
                        pkg_check = subprocess.run(
                            [str(adb_bin), "shell", "pm", "list", "packages", "com.quantniti.app"],
                            capture_output=True,
                            text=True,
                            timeout=5,
                        )
                        if "com.quantniti.app" in pkg_check.stdout:
                            subprocess.run(
                                [str(adb_bin), "shell", "am", "start", "-n", "com.quantniti.app/.MainActivity"],
                                capture_output=True,
                                timeout=5,
                            )
                        else:
                            subprocess.run(
                                [str(adb_bin), "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", guest_url],
                                capture_output=True,
                                timeout=5,
                            )
                        print(f"\n[Android Emulator] Connected ({devices[0]}) — opened {guest_url} on emulator screen!\n", flush=True)
                        return
                except Exception:
                    pass
            time.sleep(2)

    thread = threading.Thread(target=_watcher, daemon=True)
    thread.start()


def main() -> None:
    os.chdir(REPO_ROOT)
    port = int(os.getenv("PORT", "8000"))
    lan_ip = get_lan_ip()

    print("==================================================================", flush=True)
    print("                 QuantNiti Full Pipeline Runner                   ", flush=True)
    print("==================================================================", flush=True)

    adb_bin = find_android_tool("adb")

    build_web_assets_if_needed()
    server_proc = start_backend_server(port)

    # Listen in background so whenever you click Play in Android Studio, QuantNiti opens automatically
    auto_open_emulator_in_background(adb_bin, port)

    print("\n==================================================================", flush=True)
    print("                   Pipeline Successfully Running!                 ", flush=True)
    print("==================================================================", flush=True)
    print(f"  [Host PC Browser]   : http://localhost:{port}/", flush=True)
    print("                        (Open this URL in Chrome / Edge on your PC)", flush=True)
    print(f"  [Mobile on LAN]     : http://{lan_ip}:{port}/", flush=True)
    print("                        (Open on any phone connected to the same Wi-Fi)", flush=True)
    print("  [Android Emulator]  : Launch your device from Android Studio Device Manager", flush=True)
    print(f"                        (QuantNiti will auto-open at http://10.0.2.2:{port}/)", flush=True)
    print("==================================================================", flush=True)
    print("Press Ctrl+C at any time to stop the backend server.\n", flush=True)

    try:
        server_proc.wait()
    except KeyboardInterrupt:
        print("\nShutting down QuantNiti backend server...", flush=True)
        server_proc.terminate()
        try:
            server_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_proc.kill()
        print("Backend server stopped. Port 8000 released.", flush=True)


if __name__ == "__main__":
    main()

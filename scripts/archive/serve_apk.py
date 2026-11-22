#!/usr/bin/env python3
"""QuantNiti Android APK Download Server & QR Code Generator.

Generates a scannable QR code (both ASCII in terminal and saved PNG image)
pointing directly to the Android APK download endpoint on the local Wi-Fi network.
Starts a standalone HTTP server delivering the APK instantly to connected mobile devices.
"""

import os
import sys
import socket
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

def get_lan_ip() -> str:
    """Detect local LAN IPv4 address using UDP probe."""
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


def generate_qr_image(url: str, output_path: Path):
    """Generate high-resolution PNG and SVG QR codes."""
    try:
        import qrcode
        import qrcode.image.svg
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=3,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(str(output_path))

        # Also save SVG
        svg_path = output_path.with_suffix(".svg")
        svg_factory = qrcode.image.svg.SvgPathImage
        svg_img = qrcode.make(url, image_factory=svg_factory)
        svg_img.save(str(svg_path))
        return True
    except Exception as e:
        print(f"[Warning] Could not save QR image: {e}")
        return False


def print_ascii_qr(url: str):
    """Print terminal scannable ASCII QR code."""
    try:
        if hasattr(sys.stdout, "reconfigure"):
            try:
                sys.stdout.reconfigure(encoding="utf-8")
            except Exception:
                pass
        import qrcode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=2,
        )
        qr.add_data(url)
        qr.make(fit=True)
        print("\n" + "=" * 50)
        print("   SCAN THIS QR CODE WITH YOUR PHONE CAMERA")
        print("   TO DOWNLOAD QUANTNITI ANDROID APK")
        print("=" * 50 + "\n")
        qr.print_ascii(invert=True)
        print("\n" + "=" * 50 + "\n")
    except Exception as e:
        print(f"Could not print ASCII QR: {e}")


def create_apk_handler(apk_file: Path, download_url: str):
    class APKRequestHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            clean_path = parsed.path.strip("/")

            # Direct APK download routes
            if clean_path in ("", "download", "download/apk", "apk", apk_file.name):
                if not apk_file.exists():
                    self.send_error(404, "APK File Not Found")
                    return

                self.send_response(200)
                self.send_header("Content-Type", "application/vnd.android.package-archive")
                self.send_header("Content-Disposition", f'attachment; filename="{apk_file.name}"')
                self.send_header("Content-Length", str(apk_file.stat().st_size))
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()

                with open(apk_file, "rb") as f:
                    self.copyfile(f, self.wfile)
                return

            # Web landing page with instructions
            if clean_path == "guide":
                html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Download QuantNiti Android App</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background: #0b0f19;
      color: #f3f4f6;
      margin: 0;
      padding: 24px;
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 100vh;
      box-sizing: border-box;
    }}
    .card {{
      background: #111827;
      border: 1px solid #1f2937;
      border-radius: 16px;
      max-width: 440px;
      width: 100%;
      padding: 24px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.5);
      text-align: center;
    }}
    h1 {{
      font-size: 22px;
      color: #38bdf8;
      margin-top: 0;
    }}
    p {{
      font-size: 14px;
      color: #9ca3af;
      line-height: 1.5;
    }}
    .btn {{
      display: block;
      background: linear-gradient(135deg, #0284c7, #2563eb);
      color: #ffffff;
      padding: 14px 20px;
      border-radius: 10px;
      text-decoration: none;
      font-weight: 600;
      font-size: 16px;
      margin: 20px 0;
      box-shadow: 0 4px 14px rgba(2, 132, 199, 0.4);
    }}
    .steps {{
      text-align: left;
      background: #1f2937;
      border-radius: 10px;
      padding: 14px 18px;
      font-size: 13px;
      color: #e5e7eb;
    }}
    .steps ol {{
      margin: 0;
      padding-left: 20px;
    }}
    .steps li {{
      margin-bottom: 8px;
    }}
  </style>
</head>
<body>
  <div class="card">
    <h1>🚀 QuantNiti APK Download</h1>
    <p>AI-Driven Regime-Adaptive Portfolio & Stock Growth Intelligence Platform</p>
    <a href="/QuantNiti-debug.apk" class="btn">⬇️ Download QuantNiti-debug.apk</a>
    <div class="steps">
      <strong>Installation Steps:</strong>
      <ol>
        <li>Tap <strong>Download</strong> and wait for the file to save.</li>
        <li>Open the downloaded APK from your browser or notifications.</li>
        <li>If prompted with <em>"Install unknown apps"</em>, toggle <strong>Allow from this source</strong>.</li>
        <li>Tap <strong>Install</strong>, then tap <strong>Open</strong> to launch QuantNiti!</li>
      </ol>
    </div>
  </div>
</body>
</html>"""
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html.encode("utf-8"))
                return

            super().do_GET()

    return APKRequestHandler


def main():
    repo_root = Path(__file__).resolve().parent.parent
    os.chdir(repo_root)

    # Locate APK
    apk_candidates = [
        repo_root / "build" / "apk" / "QuantNiti-debug.apk",
        repo_root / "build" / "apk" / "QuantNiti-Android-APK" / "QuantNiti-debug.apk",
        repo_root / "src" / "app" / "static" / "QuantNiti-debug.apk",
    ]
    apk_file = None
    for c in apk_candidates:
        if c.exists():
            apk_file = c
            break

    if not apk_file:
        print("[Error] APK file not found. Run python scripts/build_apk.py first.")
        sys.exit(1)

    lan_ip = get_lan_ip()
    port = int(os.getenv("APK_PORT", "8080"))
    download_url = f"http://{lan_ip}:{port}/QuantNiti-debug.apk"
    guide_url = f"http://{lan_ip}:{port}/guide"

    # Save PNG QR image
    png_path = repo_root / "build" / "apk" / "apk_download_qr.png"
    if generate_qr_image(download_url, png_path):
        print(f"[OK] High-resolution QR code saved to:\n     {png_path}")

    # Print ASCII QR in terminal
    print_ascii_qr(download_url)

    print("==================================================================")
    print("             QuantNiti APK Mobile Distribution Server             ")
    print("==================================================================")
    print(f"  * APK File         : {apk_file} ({apk_file.stat().st_size / (1024*1024):.2f} MB)")
    print(f"  * Direct APK URL   : {download_url}")
    print(f"  * Web Guide URL    : {guide_url}")
    print(f"  * Local Test URL   : http://localhost:{port}/QuantNiti-debug.apk")
    print(f"  * High-Res QR PNG  : {png_path}")
    print("==================================================================")
    print("  Instructions:")
    print("  1. Connect your Android smartphone to the SAME Wi-Fi network.")
    print("  2. Point your phone camera or Google Lens at the QR code above.")
    print("  3. Tap the link to immediately download and install QuantNiti APK!")
    print("==================================================================")
    print(f"Serving HTTP on 0.0.0.0 port {port} (Press Ctrl+C to stop)...\n")

    handler = create_apk_handler(apk_file, download_url)
    server = HTTPServer(("0.0.0.0", port), handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping APK Distribution Server. Goodbye!")


if __name__ == "__main__":
    main()

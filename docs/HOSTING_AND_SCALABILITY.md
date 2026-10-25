# QuantNiti: Production Hosting, Cloud Architecture & Scalability Guide

> **Production URL:** [https://quantniti.jayadityadev.tech/](https://quantniti.jayadityadev.tech/)  
> **Infrastructure Target:** AWS Lightsail VPS (`ap-south-1` Mumbai) with Caddy v2 Reverse Proxy & Automated SSL  
> **Status:** Live in Production

---

## 1. Production Architecture Overview

QuantNiti operates on a centralized, containerized cloud architecture engineered for low-latency market access in India (`ap-south-1` Mumbai):

```
                        +---------------------------------------------+
                        |            AWS Lightsail VPS                |
                        |      (Ubuntu 24.04 LTS, ap-south-1)         |
                        |            IP: 13.207.117.167               |
                        |                                             |
                        |   +-------------------------------------+   |
                        |   |          Caddy v2 Reverse Proxy     |   |
                        |   |    Port 80/443 (Let's Encrypt SSL)  |   |
                        |   +------------------+------------------+   |
                        |                      | Reverse Proxy        |
                        |                      v (Port 8000)          |
                        |   +-------------------------------------+   |
                        |   |      QuantNiti Docker Container     |   |
                        |   |   - FastAPI ASGI Server (Python 3.12)|  |
                        |   |   - Precompiled React Vite SPA      |   |
                        |   |   - SQLite Database (WAL Mode)      |   |
                        |   +-------------------------------------+   |
                        +----------------------^----------------------+
                                               |
                          HTTPS (TLS 1.3)      |
                                               |
                  +----------------------------+----------------------------+
                  |                                                         |
         +--------+---------+                                      +--------+---------+
         |  Mobile Browser  |                                      |  Native Android  |
         |  PWA / Desktop   |                                      |   Container APK  |
         | (Chrome/Safari)  |                                      | (com.quantniti)  |
         +------------------+                                      +------------------+
```

### Key Architectural Tenets:
1. **Single Autonomous Multi-Stage Container:** Packs both the high-performance Vite frontend SPA and the Python 3.12 FastAPI quantitative intelligence engine into a unified Docker image.
2. **Reverse Proxy with Zero-Touch SSL:** Caddy v2 manages automated Let's Encrypt TLS/SSL certificates, HTTP-to-HTTPS redirects, and proxies inbound requests to container port 8000.
3. **Custom Domain Routing:** Configured under `quantniti.jayadityadev.tech` via DNS A Record, preserving root `jayadityadev.tech` portfolio routing without conflict.
4. **Unified Origin:** FastAPI serves the pre-rendered Vite production SPA from `/` and `/app`, while simultaneously handling all REST APIs (`/api/v1/...`) on the same origin, eliminating CORS overhead.
5. **Decoupled Client Access:** External client distributions (such as the standalone Android APK or standalone PWAs) connect seamlessly via `https://quantniti.jayadityadev.tech/`.

---

## 2. Production AWS Lightsail Deployment Setup

### 2.1. Host Configuration
* **Instance Type:** AWS Lightsail Linux/Ubuntu 24.04 LTS
* **Region:** Asia Pacific (Mumbai) `ap-south-1`
* **Static Public IP:** `13.207.117.167`
* **Firewall Rules:**
  - Port 22 (SSH)
  - Port 80 (HTTP — redirected by Caddy)
  - Port 443 (HTTPS — SSL terminated by Caddy)

### 2.2. Caddy Reverse Proxy Configuration (`/etc/caddy/Caddyfile`)
```caddy
quantniti.jayadityadev.tech {
    reverse_proxy localhost:8000
    encode gzip zstd
}
```
Reloading Caddy:
```bash
sudo systemctl reload caddy
```

### 2.3. Docker Container Execution
The container is built and run using Docker:
```bash
# Clone the repository
git clone https://github.com/jayadityadev/QuantNiti.git
cd QuantNiti

# Build Docker image
docker build -t quantniti:latest .

# Run container in background binding to port 8000
docker run -d \
  --name quantniti-server \
  --restart always \
  -p 8000:8000 \
  -e QUANTNITI_USE_VITE=1 \
  -e GEMINI_API_KEY="your-gemini-api-key" \
  quantniti:latest
```

### 2.4. Production Healthcheck Verification
```bash
curl -I https://quantniti.jayadityadev.tech/api/v1/health
# HTTP/2 200
# {"status":"healthy","service":"QuantNiti Core API","version":"0.1.0"}
```

---

## 3. Automated Continuous Deployment (GitHub Actions)

QuantNiti includes an automated CI/CD pipeline in [`.github/workflows/deploy.yml`](../.github/workflows/deploy.yml).

### Deployment Pipeline Workflow:
1. **Trigger:** Push to `main` branch.
2. **Quality Gates:** Runs Vitest unit & integration tests (`npm test`) and Pytest quant tests (`uv run pytest tests/`).
3. **SSH Remote Execution:** Securely connects to the AWS Lightsail host (`13.207.117.167`) via configured repository secrets (`LIGHTSAIL_SSH_KEY`, `LIGHTSAIL_HOST`, `LIGHTSAIL_USER`).
4. **Rolling Update:** Pulls the latest commits, rebuilds the container, updates environment variables, and executes healthcheck verification.

---

## 4. Native Android Container Compilation & Distribution

QuantNiti features an Android Studio native container project in `android/`:

### 4.1. Automated GitHub Actions APK Build
The workflow [`.github/workflows/android-apk.yml`](../.github/workflows/android-apk.yml) automatically compiles debug and release APKs on push or workflow dispatch:
1. Sets up Java 17 and Android SDK 35 tools on headless Ubuntu runners.
2. Executes `./gradlew assembleDebug`.
3. Attaches `app-debug.apk` directly to the workflow run artifacts for one-click download.

### 4.2. Local Manual Compilation
```bash
cd android
./gradlew assembleDebug
# Generated APK: android/app/build/outputs/apk/debug/app-debug.apk
adb install app/build/outputs/apk/debug/app-debug.apk
```

---

## 5. Alternative Cloud Deployment Blueprints

For developers wishing to run secondary instances on other cloud platforms:

### Option A: Render
The repository includes [`render.yaml`](../render.yaml):
1. Link your GitHub account at [render.com](https://render.com).
2. Select repository `jayadityadev/QuantNiti`.
3. Create Blueprint instance using `render.yaml`.
4. Render builds the Dockerfile and provisions the service.

### Option B: Railway
The repository includes [`railway.toml`](../railway.toml) and [`Procfile`](../Procfile):
1. Connect repository in [railway.app](https://railway.app).
2. Add environment variable `GEMINI_API_KEY`.
3. Railway automatically builds the container and maps the `$PORT`.

### Option C: Fly.io
The repository includes [`fly.toml`](../fly.toml):
```bash
fly launch
fly deploy
```

### Option D: Google Cloud Run
```bash
gcloud builds submit --tag gcr.io/[PROJECT-ID]/quantniti:latest
gcloud run deploy quantniti \
  --image gcr.io/[PROJECT-ID]/quantniti:latest \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated \
  --port 8000
```

# QuantNiti: Production Hosting, Cloud Architecture & Scalability Guide

> **Production URL:** [https://quantniti.jayadityadev.tech/](https://quantniti.jayadityadev.tech/)  
> **Infrastructure Target:** AWS Lightsail VPS (`ap-south-1` Mumbai) with Caddy v2 Reverse Proxy & Automated SSL  
> **Standardized Production Targets:**
> 1. **AWS Lightsail Docker Compose:** Centralized cloud engine + Vite SPA (`docker-compose.yml`, `Dockerfile`, `.github/workflows/deploy.yml`).
> 2. **Android Capacitor APK:** Direct native mobile container build (`scripts/build_apk.py`, `.github/workflows/build-apk.yml`).
> 3. **Progressive Web App (PWA):** Service worker offline caching & installability (`public/manifest.json`, `src/app/static/sw.js`).

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

### 2.2. Docker Compose & Caddy Reverse Proxy (`docker-compose.yml`, `Caddyfile`)
QuantNiti standardizes on `docker-compose.yml` orchestrating both the Caddy reverse proxy and the QuantNiti FastAPI/Vite application container:

```yaml
services:
  caddy:
    image: caddy:2-alpine
    container_name: quantniti-proxy
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy_data:/data
      - caddy_config:/config
    depends_on:
      - quantniti

  quantniti:
    build:
      context: .
      dockerfile: Dockerfile
    image: quantniti:latest
    container_name: quantniti-server
    restart: unless-stopped
    ports:
      - "${PORT:-8000}:8000"
    environment:
      - PORT=8000
      - QUANTNITI_USE_VITE=1
      - GEMINI_API_KEY=${GEMINI_API_KEY:-}
      - WEB_CONCURRENCY=${WEB_CONCURRENCY:-1}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 15s

volumes:
  caddy_data:
  caddy_config:
```

The Caddy configuration (`Caddyfile`):
```caddy
quantniti.jayadityadev.tech {
    reverse_proxy quantniti:8000

    encode zstd gzip

    header {
        Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
        X-Content-Type-Options "nosniff"
        X-Frame-Options "DENY"
        Referrer-Policy "strict-origin-when-cross-origin"
    }
}

:80 {
    respond "QuantNiti Server Live" 200
}
```

### 2.3. Starting and Updating Services
```bash
# Clone the repository
git clone https://github.com/jayadityadev/QuantNiti.git
cd QuantNiti

# Create production environment configuration (.env)
cat << 'EOF' > .env
PORT=8000
HOST=0.0.0.0
QUANTNITI_USE_VITE=1
WEB_CONCURRENCY=1
GEMINI_API_KEY="your-gemini-api-key"
EOF

# Launch Docker Compose stack
docker compose down
docker compose up -d --build --remove-orphans
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
1. **Trigger:** Push to `main` branch or manual `workflow_dispatch`.
2. **SSH Remote Execution:** Securely connects to the AWS Lightsail host (`13.207.117.167`) via configured repository secrets (`SERVER_SSH_KEY`, `SERVER_HOST`, `SERVER_USER`).
3. **Rolling Update:** Pulls the latest commits from `origin/main`, provisions `.env`, rebuilds the containers via `docker compose up -d --build --remove-orphans`, and executes healthcheck verification.

---

## 4. Native Android Container Compilation & Distribution

QuantNiti features native mobile distribution through direct Android APK compilation:

### 4.1. Automated GitHub Actions APK Build
The workflow [`.github/workflows/build-apk.yml`](../.github/workflows/build-apk.yml) compiles APKs automatically:
1. Triggers on changes to frontend source, Android assets, or dependencies.
2. Injects production API configuration: `VITE_API_URL=https://quantniti.jayadityadev.tech`.
3. Runs `scripts/build_apk.py` which builds the Vite SPA bundle and synchronizes it into `android/app/src/main/assets/dist/`.
4. Executes Gradle 8.4 with JDK 17 to compile `app-debug.apk`.
5. Uploads the resulting APK as a downloadable release artifact directly on GitHub Actions.

### 4.2. Local Packaging via `scripts/build_apk.py`
```bash
# Packaging script handles Vite build, asset synchronization, and Gradle build
python scripts/build_apk.py

# Install to connected device or emulator
adb install build/apk/quantniti-debug.apk
```

---

## 5. Progressive Web App (PWA) & Offline Resilience

QuantNiti is a fully compliant Progressive Web App (PWA) providing native-like desktop and mobile browser experiences:

### 5.1. Web App Manifest (`public/manifest.json`)
* **Display Mode:** `standalone` with system-native status bar integration.
* **Theme & Styling:** Adaptive theme colors (`#7C3AED` primary, `#F8FAFC` background).
* **Shortcuts:** One-click launcher shortcuts for AI Portfolio Basket (`#grow`) and Market Intelligence.
* **Icons:** Complete suite of standard and maskable icons (192px, 512px, SVG vector).

### 5.2. Service Worker Offline Caching (`src/app/static/sw.js`)
* **Precached App Shell:** Core HTML shells (`/`, `/app`, `/client`, `/vite`), manifest, icons, and precompiled Vite JS/CSS vendor bundles.
* **Cache Strategy:** Stale-While-Revalidate with Cache-First fallback for static assets and offline shell resilience.
* **Safe API Bypass:** REST API requests (`/api/v1/*`) bypass the cache to guarantee real-time market data integrity.

---

## 6. Standardized Production Targets Summary

| Target | Core Files / Workflows | Protocol / Transport | Canonical Endpoint |
|---|---|---|---|
| **AWS Lightsail VPS** | `docker-compose.yml`, `Dockerfile`, `Caddyfile`, `.github/workflows/deploy.yml` | HTTPS (TLS 1.3 / Let's Encrypt), HTTP/2, WebSockets | `https://quantniti.jayadityadev.tech/` |
| **Android APK** | `scripts/build_apk.py`, `android/`, `.github/workflows/build-apk.yml` | Native Android Container (SDK 35, Gradle 8.4) | `com.quantniti` app package |
| **PWA Web App** | `public/manifest.json`, `src/app/static/sw.js`, `index.html` | Service Worker Precache + Standalone Web App | Native installable prompt across browsers |

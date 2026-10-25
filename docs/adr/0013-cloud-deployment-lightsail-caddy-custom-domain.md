# Cloud Deployment via AWS Lightsail, Caddy SSL & Custom Domain

**Status:** accepted

## Context
Academic evaluators, project teammates, and mobile beta testers require reliable 24/7 access to the live platform over HTTPS without executing local terminal commands. PWA service workers and Web Push notifications strictly require valid TLS/SSL certificates.

## Decision
We deployed the unified application container to an **AWS Lightsail VPS** in the Mumbai region (`ap-south-1`, IP `13.207.117.167`):
1. **Edge Proxy**: Caddy v2 web server managing automated Let's Encrypt TLS/SSL certificates, HTTP-to-HTTPS redirects, and reverse-proxying port 8000.
2. **Custom Domain Routing**: Configured DNS A Record for `quantniti.jayadityadev.tech` pointing to `13.207.117.167`, while preserving existing root portfolio routing on `jayadityadev.tech`.
3. **Continuous Deployment**: Automated GitHub Actions workflow (`deploy.yml`) testing, building, and deploying container updates on push to `main`.

## Consequences
- Provides a public, production-grade HTTPS endpoint (`https://quantniti.jayadityadev.tech/`).
- Satisfies all PWA installability and Web Push security requirements.
- Zero-cost automated SSL certificate provisioning and renewal.

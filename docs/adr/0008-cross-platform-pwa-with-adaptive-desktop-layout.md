# Cross-Platform Progressive Web App (PWA) with Responsive Layout

**Status:** accepted

## Context
Retail users access applications across smartphones, tablets, and desktop workstations. Developing and maintaining separate native iOS, Android, and web codebases creates severe development overhead and synchronization drag for a fast-moving quantitative project.

## Decision
We architected the client as an installable Progressive Web Application (PWA) using React 18, Vite, and Tailwind CSS:
1. Web App Manifest and Service Worker caching for instant standalone launching and offline resilience.
2. Responsive layout adapting smoothly from mobile squircle cards to expanded viewports.
3. Web Push notification support for proactive market alerts.

## Consequences
- Zero-friction installation directly from the browser on Android, iOS, Windows, and macOS.
- Unified codebase serving mobile and desktop users simultaneously.

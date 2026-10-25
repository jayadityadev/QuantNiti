# Native Android Container via WebViewAssetLoader & Automated APK CI/CD

**Status:** accepted

## Context
Over 80% of Indian retail investors access financial services exclusively through native Android smartphone applications. While Progressive Web Apps (PWAs) provide web installability, many retail users expect a standalone `.apk` distribution that integrates with Android hardware navigation and offline asset storage.

## Decision
We developed a native Android container project in `android/` (`com.quantniti.app`):
1. **Asset Streaming**: Employs AndroidX `WebViewAssetLoader` to stream precompiled web assets locally with zero latency, with graceful fallback to `https://quantniti.jayadityadev.tech/`.
2. **Hardware Gestures**: Intercepts native back button presses in `MainActivity.java` to dismiss React modal sheets and handle navigation history before exiting.
3. **Automated CI/CD**: A dedicated GitHub Actions workflow (`android-apk.yml`) compiles debug and release APKs on push using headless Android SDK tools and attaches the APK artifacts directly to the build run.

## Consequences
- Delivers a true native app experience on Android devices alongside web PWA support.
- Automates APK generation without requiring local Android Studio installation on every developer machine.

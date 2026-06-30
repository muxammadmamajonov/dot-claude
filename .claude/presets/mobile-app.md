# Mobile Application Preset

## Project type
Application distributed through Apple App Store and/or Google Play Store. Variants: native iOS (Swift/SwiftUI), native Android (Kotlin/Jetpack Compose), cross-platform (React Native, Flutter, Expo), or hybrid (Capacitor/Ionic). Includes consumer apps, enterprise/internal apps, and companion apps for hardware devices.

## Typical use cases
- Consumer product apps (social, fitness, finance, travel, food delivery)
- Enterprise field tools (inspection, logistics, field service, sales)
- Health and wellness apps (HealthKit/Health Connect integration)
- IoT companion apps (BLE pairing, device control, firmware OTA)
- Payments and fintech apps (tap-to-pay, wallet, KYC onboarding)
- Content and media consumption (streaming, reading, podcasts)

## Required discovery questions
1. Which platforms must ship at launch — iOS only, Android only, or both simultaneously? Are there tablet form factors required?
2. What is the minimum OS version target (iOS 16+? Android 9+)? Any specific device hardware features required (NFC, BLE, ARKit, camera AI)?
3. Will the app function offline or in degraded-connectivity environments? What data must be available without a network connection?
4. Is a backend required exclusively for this app, or does it integrate with an existing API? Who owns and operates that API?
5. What authentication method is required — Apple/Google Sign-In, biometric (Face ID / fingerprint), username/password, enterprise SSO?
6. Are push notifications required? What categories (transactional, marketing, real-time events)?
7. Does the app handle payments, subscriptions, or in-app purchases (IAP)? StoreKit / Play Billing compliance required?
8. What privacy-sensitive data is collected — location, health, contacts, microphone, camera? Any HIPAA, COPPA, or GDPR obligations?
9. Does the app need deep linking or Universal Links/App Links for marketing campaigns or third-party integrations?
10. What are the App Store / Play Store review constraints — is the app in a restricted category (finance, health, gambling, VPN)?

## Recommended agents

### Core
- `.claude/agents/core/orchestrator.md` — phase sequencing, store submission coordination
- `.claude/agents/core/solution-architect.md` — offline-first data model, sync strategy
- `.claude/agents/core/project-manager.md` — sprint planning around release cadence

### Engineering
- `.claude/agents/engineering/mobile-engineer.md` — UI components, navigation, state management
- `.claude/agents/engineering/backend-engineer.md` — mobile API (REST/GraphQL), push gateway
- `.claude/agents/engineering/backend-engineer.md` — biometric, OAuth, token storage in Keychain/Keystore

### Quality
- `.claude/agents/quality/qa-engineer.md` — device matrix, OS version matrix, real-device testing
- `.claude/agents/quality/performance-engineer.md` — ANR/crash rate, cold start time, memory profiling
- `.claude/agents/quality/security-auditor.md` — certificate pinning, data-at-rest encryption, reverse-engineering hardening

### Design
- `.claude/agents/design/ui-ux-designer.md` — HIG and Material Design 3 compliance, gesture models
- `.claude/agents/design/accessibility-designer.md` — VoiceOver / TalkBack, Dynamic Type, colour contrast

### Domain
- `.claude/agents/engineering/release-engineer.md` — App Store Connect / Play Console metadata, ASO, review compliance
- `.claude/agents/engineering/mobile-engineer.md` — APNs / FCM configuration, notification categories

## Recommended skills
- `.claude/skills/mobile/SKILL.md` — platform idioms, navigation patterns, state management
- `.claude/skills/mobile/SKILL.md` — local DB (SQLite / Room / Core Data), conflict resolution
- `.claude/skills/security/SKILL.md` — Keychain/Keystore secure storage, biometric flows
- `.claude/skills/security/SKILL.md` — certificate pinning, obfuscation, root/jailbreak detection
- `.claude/skills/testing/SKILL.md` — unit, snapshot, E2E (Detox / XCTest / Espresso)
- `.claude/skills/ui-ux-design/SKILL.md` — VoiceOver, TalkBack, focusability, announcements
- `.claude/skills/performance/SKILL.md` — render performance, memory management, startup time

## Recommended stack options

| Stack | Rationale |
|---|---|
| **React Native (Expo) + TypeScript** | Fastest cross-platform path; large ecosystem; OTA updates via Expo EAS; strong CI toolchain. See `.claude/stack-matrix/mobile.md` |
| **Flutter + Dart** | Single codebase with pixel-perfect custom UI; excellent for design-heavy consumer apps; strong on embedded/desktop too |
| **Swift (SwiftUI) + Kotlin (Compose)** | Maximum native performance and platform integration; choose when deep OS API access or premium feel is non-negotiable |
| **Capacitor + Web App** | When the web team owns the product and mobile is a wrapper; shares web codebase; limited native feel |

Reference `.claude/stack-matrix/mobile.md`, `.claude/stack-matrix/backend.md` for detailed tradeoffs.

## Required checklists
- `.claude/checklists/security.md` — secrets in binary, certificate pinning, data encryption
- `.claude/checklists/performance.md` — cold start ≤2 s, 60 fps scroll, memory budget
- `.claude/checklists/accessibility.md` — VoiceOver/TalkBack labels, Dynamic Type, tap target ≥44pt
- `.claude/checklists/launch.md` — store screenshots, privacy manifests, age rating, rollback (staged rollout)
- `.claude/checklists/mobile.md` — App Store Review Guidelines §2–5, Play Policy compliance

## MVP scope pattern

**In MVP**
- Onboarding + authentication (social sign-in or email)
- Core user flow (the one screen sequence that delivers the value proposition)
- Basic offline capability for the primary read path
- Push notification opt-in
- Crash reporting (Crashlytics or Sentry)
- App Store + Play Store listings ready

**Deferred to v2**
- Widgets (iOS WidgetKit / Android AppWidgets)
- Wear OS / watchOS companion
- Advanced biometric step-up auth
- In-app purchases / subscription management
- Deep-link attribution (Adjust, AppsFlyer)
- Background sync / background fetch
- Apple/Google Wallet integration

## Production risks

| Risk | Severity | Mitigation |
|---|---|---|
| Credentials or API keys embedded in binary | P0 | Use `.env` excluded from SCM; obfuscate keys; use backend proxy for sensitive calls |
| Insecure local storage (plain SQLite, AsyncStorage) | P0 | Encrypt SQLite (SQLCipher); use Keychain/Keystore for tokens |
| Missing certificate pinning | P0 | Pin leaf or intermediate cert; implement pin rotation strategy |
| App Review rejection before launch | P0 | Read review guidelines for the app category before coding login/payments |
| ANR or crash on low-end Android devices | P1 | Test on real low-RAM devices; target API 28+ minimum; profile with Android Profiler |
| Cold start time > 3 s | P1 | Lazy-load non-critical modules; defer analytics init; use Hermes / R8 |
| Push token not refreshed after iOS permission change | P1 | Handle `didFailToRegisterForRemoteNotificationsWithError` and re-register |
| Background data sync draining battery | P1 | Use `BackgroundFetch` / `WorkManager` with appropriate intervals; respect low-power mode |
| Missing privacy nutrition label accuracy | P1 | Audit all SDKs for data collection; update App Privacy Report before every submission |
| Insecure deep-link handling (URL scheme hijacking) | P2 | Use Universal Links / App Links (HTTPS) instead of custom URL schemes |

## Launch requirements
- Crash-free rate ≥ 99.5 % on both platforms in TestFlight / Internal Testing
- All P0 checklist items in `.claude/checklists/security.md` signed off
- App Store and Play Store listings complete: screenshots, description, age rating, privacy policy URL
- Privacy manifest (iOS) and Data Safety form (Android) accurately reflect all SDKs
- Staged rollout configured (5 % → 20 % → 100 %) with rollback trigger thresholds defined
- Error monitoring alerts wired for crash-rate spike and ANR rate
- Backend API versioning strategy confirmed so app v1 still works when v2 ships
- OTA update or force-upgrade mechanism in place for critical patches

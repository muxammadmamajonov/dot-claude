---
name: mobile
description: >
  Activate when building, extending, or shipping a mobile application — native
  iOS (Swift/SwiftUI), native Android (Kotlin/Jetpack Compose), or cross-platform
  (React Native, Expo, Flutter). Covers navigation architecture, offline data,
  push notifications, device permissions, app store submission, and OTA updates.
  Do NOT activate for mobile-responsive web (use .claude/skills/web/SKILL.md).
---

# Mobile Application Skill

## When to use

- Starting a new iOS, Android, or cross-platform mobile project
- Adding navigation flows, offline sync, push notifications, biometric auth
- Diagnosing crashes, ANRs, memory pressure, or battery drain
- Preparing for App Store (Apple) or Google Play submission
- Integrating device capabilities: camera, location, BLE, NFC, sensors

---

## Bundled tooling

- **Release scaffold (script):** `scripts/scaffold_mobile_release.py` generates a correct starter for
  CI/store release — `python3 .claude/skills/mobile/scripts/scaffold_mobile_release.py --platform <expo|rn|flutter|ios|android> <dir>`.
  It writes Fastlane (`Fastfile`/`Appfile`) and/or EAS (`eas.json`), a `.env.example` of signing/credential
  var **names** (never values), and a `RELEASE.md` runbook. Idempotent (won't overwrite without `--force`),
  stdlib-only, no network, no secrets. Used by `.claude/agents/engineering/mobile-release-engineer.md`.
- **Per-store submission references:** `references/app-store-submission.md` (Apple) and
  `references/google-play-submission.md` (Google) — read the relevant one during `app-store-readiness` /
  `/store-readiness`; they cover signing, build/upload (Fastlane + EAS), required disclosures, and the top
  rejection causes. Verify against the **current** store policies (they change).

## Workflow

1. **Classify the project** — Read `docs/specs/product.md` and `.claude/stack-matrix/` to confirm platform (iOS / Android / both), framework, minimum OS versions, and distribution channel (App Store, Play Store, Enterprise MDM, internal TestFlight/Firebase App Distribution).

2. **Choose cross-platform vs. native trade-offs**
   | Scenario | Recommendation |
   |---|---|
   | Single team, consistent UX, fast iteration | React Native (Expo) or Flutter |
   | Heavy platform-specific UI (e.g. widgets, live activities) | Native per platform |
   | Performance-critical (3D, AR, real-time audio) | Native or thin JS bridge with native modules |

3. **Set up project** — Initialise with official CLI:
   - Expo: `npx create-expo-app` with TypeScript template
   - Flutter: `flutter create --org com.company`
   - Native iOS: Xcode template → Storyboard or SwiftUI
   - Native Android: Android Studio template → Compose Activity
   Configure signing immediately; late-adding signing configs causes build pipeline pain.

4. **Design navigation architecture** — Define the full screen graph before coding:
   - React Native: React Navigation with typed route params
   - Flutter: GoRouter with named routes
   - iOS: NavigationStack (SwiftUI) or Coordinator pattern (UIKit)
   - Android: Jetpack Navigation with safe-args
   Never hardcode back-button behaviour; rely on the navigation library's stack.

5. **Implement offline-first data** — Mobile connectivity is unreliable:
   - Choose a local store: SQLite (via Drizzle/Expo SQLite), Realm, Room (Android), Core Data / SwiftData (iOS)
   - Queue mutations locally; sync when online using background fetch or WorkManager (Android)
   - Expose a clear sync-status indicator to the user

6. **Integrate push notifications** — Configure APNs (iOS) and FCM (Android/iOS fallback). Request permission at a contextually appropriate moment — never on first launch cold-open. Handle deep-link payloads: the app must navigate to the correct screen whether it was killed, backgrounded, or foregrounded.

7. **Handle device permissions** — Declare only permissions you use in `Info.plist` / `AndroidManifest.xml`. Ask at the moment of use with an explanation. Gracefully degrade when denied; never crash.

8. **Implement auth** — Prefer native OS credential storage: iOS Keychain, Android Keystore / EncryptedSharedPreferences. Support biometric auth (Face ID, fingerprint) as a convenience layer over a primary credential. Use short-lived access tokens + refresh-token rotation.

9. **Optimise for battery & memory** — Cancel background tasks when the app is backgrounded. Profile with Instruments (iOS) or Android Profiler: resolve memory leaks, limit background location usage, batch network calls. Reference `.claude/checklists/performance.md`.

10. **Write tests**
    - Unit: business logic, reducers, data mappers
    - Widget/component: interaction tests with `flutter_test`, `@testing-library/react-native`, or XCTest
    - E2E: Detox (React Native), Maestro, or XCUITest/Espresso
    Reference `.claude/checklists/qa.md`.

11. **Prepare store submission**
    - iOS: bump `CFBundleShortVersionString` and `CFBundleVersion`; archive in Xcode; upload via Transporter or `xcrun altool`; complete App Review checklist (privacy labels, encryption export compliance, IDFA)
    - Android: bump `versionName` and `versionCode`; build release AAB; sign with Play App Signing key; complete Data Safety form
    Never submit without testing on a physical device.

12. **Set up OTA updates (cross-platform only)** — Expo Updates or CodePush for JS bundle patches. Gate rollout at 5 % → 20 % → 100 %; monitor crash rates at each step before expanding.

---

## Standards

**Do**
- Target the last two major OS versions unless the spec explicitly requires wider support.
- Use adaptive layouts: respect Dynamic Type (iOS) and font scaling (Android). Test at 200 % text size.
- Sanitize and validate all data received from the network, even from your own API.
- Strip debug logging and test credentials from release builds using build-variant config.
- Use ProGuard / R8 on Android release builds to shrink and obfuscate.
- Pin SSL certificates for high-value endpoints (banking, health data).

**Do not**
- Store secrets (API keys, private keys) in the app bundle — they are extractable.
- Request `ACCESS_FINE_LOCATION` when `COARSE` suffices.
- Block the UI thread with disk I/O or network calls.
- Use deprecated APIs that are removed in the next OS version (check deprecation warnings in build output).
- Hard-code server URLs in source; use environment configs per build flavour.

---

## Common mistakes to avoid

- **Cold-start permission dialogs** — asking for camera/contacts immediately on first launch gets denied 70 %+ of the time; present permissions inline at point of use.
- **Not handling background → foreground state** — data shown may be stale; refetch or validate on `AppState` change / `onResume`.
- **Missing keyboard avoidance** — `KeyboardAvoidingView` (RN) or `adjustResize` / `WindowInsets` (native) must be configured for every form screen.
- **Ignoring safe-area insets** — content hidden behind notch, Dynamic Island, or navigation bar; always apply `SafeAreaView` / `WindowInsets`.
- **Leaking async operations** — unmounted components updating state cause warnings (RN) or crashes; cancel in `useEffect` cleanup or use AbortController.
- **Shipping with `debuggable: true`** on Android release builds — allows ADB shell access.
- **Not testing on low-end devices** — mid-range / entry Android devices expose jank and OOM errors that flagship devices hide.

---

## Output format

A production-ready mobile project should include:

```
/
├── src/ (or lib/ for Flutter)
│   ├── screens/            # Full-page views
│   ├── components/         # Reusable UI atoms
│   ├── navigation/         # Route definitions & navigator setup
│   ├── store/ (or state/)  # State management (Zustand, Redux, Riverpod, etc.)
│   ├── services/           # API clients, push, analytics
│   ├── db/                 # Local database schema & queries
│   └── utils/
├── assets/                 # Icons, images, fonts
├── ios/ or android/        # Platform-specific config
├── tests/
├── .env.example
└── README.md               # How to run on simulator and physical device
```

---

## Related checklists

- `.claude/checklists/security.md`
- `.claude/checklists/accessibility.md`
- `.claude/checklists/performance.md`
- `.claude/checklists/qa.md`
- `.claude/checklists/production.md`

## Related agents

- `.claude/agents/core/orchestrator.md`
- `.claude/agents/engineering/mobile-engineer.md`
- `.claude/agents/quality/security-auditor.md`

# Mobile Checklist

Passing this gate proves the mobile app (iOS, Android, React Native, Flutter, or any other cross-platform target) is safe to submit to the App Store / Google Play, is crash-free under normal and edge-case conditions, meets platform policy requirements, and protects user data. Severity tiers: P0=blocker, P1=important (fix shortly after launch), P2=hardening, P3=post-launch/backlog.

## P0 — Blockers (must pass before store submission)

- [ ] App complies with the target platform's current review guidelines — Apple App Store Review Guidelines and/or Google Play Developer Policy — with zero policy violations; any grey-area feature has been verified against the policy text, not assumed.
- [ ] All declared permissions (camera, microphone, location, contacts, calendar, photos, Bluetooth, NFC, health, notifications, etc.) are accompanied by a purpose string (NSUsageDescription on iOS, `uses-permission` rationale on Android); permissions not used by any current code path are removed from the manifest / Info.plist.
- [ ] Runtime permission requests are triggered contextually — at the moment the user initiates the feature that needs the permission — never at first launch unless the feature is the core value proposition.
- [ ] Crash-free session rate ≥ 99.5 % measured on release builds running on real devices (not simulator) across the two most-used OS versions per platform analytics; validated with Crashlytics or Sentry symbolicated reports.
- [ ] Cold-start time ≤ 3 s on the minimum supported device spec (as declared in the product spec); no ANR (Android Not Responding) dialog triggered under normal use; no iOS watchdog-terminated hangs.
- [ ] All network requests degrade gracefully when offline or under poor connectivity: cached or stale data is surfaced with a staleness indicator; a meaningful error state replaces infinite loading spinners; retry logic uses exponential backoff.
- [ ] Sensitive data (auth tokens, session cookies, PII, payment data) is never written to system logs, crash reports, analytics events, or device analytics; Keychain (iOS) or EncryptedSharedPreferences / Keystore (Android) are used for secret storage.
- [ ] Deep links, universal links (iOS), and App Links (Android) are validated with intent filters and apple-app-site-association / assetlinks.json; the app does not open arbitrary external URLs from deep-link parameters without strict allowlist validation.
- [ ] Release binary contains no hardcoded API keys, credentials, internal hostnames, or environment-specific secrets; obfuscation / minification / ProGuard / R8 / Bitcode stripping is enabled in the release build configuration.
- [ ] Target SDK version meets current store minimums (Google Play targetSdkVersion and iOS minimum deployment target); no APIs flagged as deprecated or removed by the platform linter are used.
- [ ] In-app purchase, subscription, and restore flows tested end-to-end in the sandbox environment (StoreKit testing / Google Play Billing sandbox); receipt validation is performed server-side, never client-side only.
- [ ] Binary has been scanned with `dependency-check`, `osv-scanner`, or equivalent; no CRITICAL or HIGH CVEs in shipping dependencies left unaddressed; a mitigation or accepted-risk record exists for each finding.

## P1 — Important (fix before scaling / shortly after launch)

- [ ] Battery impact profiled with Xcode Energy Organizer / Android Battery Historian; background wake-locks, location polling, and push-keepalive operations fire only as frequently as the user's workflow demands and release their locks promptly.
- [ ] Memory footprint profiled on a low-RAM device (≤ 2 GB RAM) using Instruments (iOS) or Android Profiler for a 10-minute soak test; no memory leaks detected; app does not receive memory-pressure warnings under normal use.
- [ ] App handles OS interruptions correctly and restores state: incoming calls, FaceTime, Siri, multi-window / split-view, orientation rotation, background-to-foreground transitions, low-storage warnings, and low-battery mode.
- [ ] Forced-update mechanism is implemented and tested: the server can return a minimum required version; clients below that version are shown a mandatory upgrade prompt that blocks access to the main application until updated.
- [ ] Crash and ANR reports are routed to a monitoring service with symbolicated stack traces; the on-call process receives an alert within 5 minutes of a crash-rate spike above baseline.
- [ ] Accessibility audit passed: touch targets ≥ 44 × 44 pt (iOS) / 48 × 48 dp (Android), dynamic type / font-scaling respected (UIContentSizeCategory / sp units), VoiceOver and TalkBack labels present and accurate on all interactive controls, no color-only state differentiation.
- [ ] Push notification payloads contain no PII; notification delivery and open rates are tracked; the permission prompt is shown only after the user has experienced enough of the product to understand its value.
- [ ] OTA update / CodePush / EAS Update strategy is documented and compliant with the App Store and Play Store guidelines for the update mechanism chosen; code-push updates do not alter core functionality in ways that bypass store review.
- [ ] Third-party SDKs (analytics, advertising, crash reporting, payments, social login) are inventoried; each SDK's data collection is disclosed in the privacy policy and app store privacy nutrition label; SDKs that are no longer needed are removed.
- [ ] App tested under simulated poor-network conditions (Network Link Conditioner on iOS / Android emulator throttle) at 3G (≤ 1 Mbps, 150 ms RTT); timeouts and retry policies are tuned to avoid user-facing failures on marginal connections.

## P2 — Hardening / nice-to-have

- [ ] Biometric authentication (Face ID, Touch ID, Android BiometricPrompt) is offered for sensitive actions (payment, account changes, viewing private data); a PIN/password fallback exists for devices that do not support biometrics.
- [ ] Download size ≤ 50 MB for the initial App Store listing (iOS) and APK/AAB ≤ 150 MB (Play Store); assets are compressed with WebP/AVIF (images) and Brotli/ZSTD (data); unused resources and locales are stripped.
- [ ] Analytics and telemetry collection respects user consent: GDPR / CCPA / PDPA / LGPD consent dialogs appear before any tracking begins; consent preferences are stored and honored across sessions and app updates.
- [ ] Dark mode and system high-contrast themes render correctly on both platforms; no hard-coded color literals bypass the theme; system-dark-mode is honored automatically via semantic color APIs.
- [ ] Screenshot prevention is applied to sensitive screens (payment entry, identity documents, private messages) via `FLAG_SECURE` (Android) and `UITextField.isSecureTextEntry` / `UITextField.textContentType` / screen-recording notifications (iOS).
- [ ] Jailbreak and root detection has been evaluated; the risk appetite is documented; if detection is implemented it uses a reputable library, fails closed for high-risk features, and cannot be silently bypassed by stripping a flag.
- [ ] App size optimization validated with App Thinning (iOS) / Android App Bundle; per-device download sizes measured in App Store Connect / Play Console; unnecessary architectures and assets excluded from the shipping artifact.

## P3 — Post-launch / backlog (track and revisit after launch; never blocks shipping)

- [ ] App Store / Google Play ratings are monitored weekly; a in-app rating prompt is A/B-tested at a moment of delight (e.g., post task-completion) using the native `SKStoreReviewRequest` / `ReviewManager` APIs to avoid policy violations.
- [ ] Localization coverage is expanded beyond the launch locale set; pseudo-locale testing (`en-XA`, `ar-XB`) is automated in CI to catch truncation and RTL layout regressions before each new language ships.
- [ ] Widget, Live Activity (iOS), and App Shortcut / Quick Action (Android) extensions are designed and implemented for the app's primary high-frequency action, benchmarked for home-screen engagement lift.
- [ ] App clip (iOS) / Instant App (Android) is evaluated and prototyped for the top acquisition entry point (e.g., QR code scan at a physical location) to lower the install-barrier conversion funnel.
- [ ] Carrier/roaming-aware data saver mode is implemented: large media downloads are deferred or require explicit user approval when the OS reports a metered or roaming connection.
- [ ] Long-term retention of OS-minimum support versions is reviewed quarterly against crash-free session share; a sunset plan (in-app notice → forced-upgrade grace period → store minimum bump) is documented and rehearsed.

## How to use

**Stage:** gate 6 (Audit) before each App Store / Play Store submission; gate 8 (Launch readiness) for the initial launch; repeat P0 items for each release candidate in CI.

**Agent:** `.claude/agents/engineering/mobile-engineer.md` leads the build and self-review; `.claude/agents/quality/security-auditor.md` owns binary and permission scanning; `.claude/agents/quality/qa-engineer.md` owns device coverage and interrupt testing; `.claude/agents/quality/accessibility-auditor.md` owns the accessibility subset.

**Skill:** `.claude/skills/mobile/SKILL.md` for platform-specific implementation patterns; `.claude/skills/security/SKILL.md` for permission and data-protection guidance; `.claude/skills/testing/SKILL.md` for device-matrix and soak-test protocols.

**Commands:** `audit-security` and `audit-production` trigger the full pass; `review-feature` should include P0 items before each PR merge. Cross-reference `.claude/checklists/security.md` for auth, session management, and transport-layer items; `.claude/checklists/performance.md` for general throughput and memory targets; `.claude/checklists/accessibility.md` for the full WCAG 2.2 AA matrix.

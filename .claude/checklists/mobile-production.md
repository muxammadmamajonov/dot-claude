# Mobile Production-Readiness Checklist

The mobile gate before shipping a production app (React Native, Expo, Flutter, native iOS/Android, KMP).
Pairs with `.claude/checklists/production.md` (universal) and `.claude/checklists/app-store-readiness.md`
(store submission). Severity: **P0** blocker · **P1** important · **P2** hardening · **P3** backlog.

## P0 — Blockers (must pass before release)

- [ ] **No secrets in the app binary**: no API keys/tokens hardcoded in source or `Info.plist`/`AndroidManifest`/JS bundle; secrets sit behind a backend proxy. (Client binaries are decompilable.)
- [ ] **Tokens stored securely**: auth/refresh tokens in **Keychain** (iOS) / **Keystore / EncryptedSharedPreferences / DataStore** (Android) — never in plain `UserDefaults`/`SharedPreferences`/`AsyncStorage`.
- [ ] **Transport security**: HTTPS only; ATS not globally disabled (iOS); `usesCleartextTraffic=false` (Android); certificate/host validation not bypassed.
- [ ] **AuthN/AuthZ enforced server-side**; deep links validated (no auth bypass / unverified params); WebViews don't expose native bridges to untrusted content.
- [ ] **Permissions**: every requested permission is used and has a purpose string (iOS `NS*UsageDescription`) / rationale; app degrades gracefully when denied; no over-broad permissions.
- [ ] **Crash reporting wired** (Crashlytics/Sentry) with symbol/dSYM/mapping upload; release tagged; a clean launch shows zero crashes on the critical path.
- [ ] **Release build succeeds & runs on a real device** (not just simulator) for both platforms targeted; no debug-only code, no `console.log`/logcat of sensitive data in release.
- [ ] **Versioning correct**: marketing version + build number incremented; signing configured (provisioning profile / keystore) and **keystore/cert backed up**.
- [ ] **Automated tests pass** for critical journeys (launch, auth, core action) — real results, not assumed.
- [ ] **Rollback/halt path**: staged rollout planned; ability to halt rollout and ship a hotfix; OTA (Expo Updates/CodePush) only for JS-safe changes.

## P1 — Important (soon)

- [ ] **Startup performance**: cold start within target (e.g. < 2.5s mid-tier device); no main-thread blocking on launch; splash → interactive measured.
- [ ] **Offline behavior**: app doesn't crash offline; queued writes + retry; clear offline UI; sync conflict strategy defined where local data is editable.
- [ ] **Network resilience**: timeouts, retry with backoff, request cancellation, poor-network handling; user-facing API errors are mapped, not raw.
- [ ] **List/scroll performance**: long lists virtualized (FlatList/LazyColumn/ListView.builder); images sized & cached; no jank on the core scroll.
- [ ] **Accessibility**: screen-reader labels on actionable elements (VoiceOver/TalkBack), dynamic-type/font-scaling honored, AA contrast, ≥44pt/48dp touch targets, focus order sane.
- [ ] **Push notifications** (if used): permission UX, channels/categories, deep-link from tap, background/foreground handling, badge management, delivery tested on device.
- [ ] **State restoration**: app survives process death/backgrounding; no lost user input on rotation/return; deep links cold-start correctly.
- [ ] **App size** reasonable for the audience; release build shrunk (R8/Proguard for Android, bitcode/strip for iOS where applicable); unused assets removed.
- [ ] **Analytics + release health** wired (adoption, crash-free users/sessions) with consent honored.

## P2 — Hardening

- [ ] Image/video compression on upload; resumable/background uploads where large media is core; thumbnails + EXIF stripped where privacy matters.
- [ ] IAP/subscriptions (if any): receipt validation server-side, entitlement restore, sandbox-tested, refund/cancellation handled.
- [ ] Tablet/foldable/large-screen layouts checked; safe areas, notches, and orientation handled; keyboard-avoidance correct on forms.
- [ ] Cert pinning where the threat model warrants; root/jailbreak & app-attestation checks for high-risk apps; obfuscation for sensitive logic.
- [ ] Background tasks/fetch behave within OS limits and don't drain battery; location use minimized and justified.
- [ ] Migration tests for local DB schema changes; app-upgrade path tested from the previous released version.

## P3 — Post-launch / backlog (track; never blocks)

- [ ] Device-farm matrix run (BrowserStack/Firebase Test Lab/Sauce) across key OS versions & screen sizes.
- [ ] Visual-regression (Storybook RN / Widgetbook / snapshot) and a11y checks in CI.
- [ ] ANR/OOM tracking dashboards; battery & network-usage profiling under real workloads.
- [ ] On-device AI/model fallback to online; token/cost controls for any LLM calls (via backend proxy).

## How to use

**When:** before a production release / store submission, and at the readiness review.
**Who:** `production-readiness-auditor` leads; `mobile-security-auditor`, `performance-engineer`,
`accessibility-auditor`, `mobile-release-engineer`, and the platform `stack/mobile/*` engineer own their
sections. **Command:** `/mobile-audit <scope> --mode production-hardening` exercises sections;
`/store-readiness` pairs this with `.claude/checklists/app-store-readiness.md`. P0 blocks release;
P1 → tracked issues; P2–P3 → backlog. Mark passed only with real evidence (a device run, a profiler
trace, a test command + output) — never an assumption.

# Mobile Specification

**What:** Defines platform targets, navigation model, offline behaviour, push notifications, device permissions, and app store metadata for any mobile app.
**Who fills it in:** Mobile lead + product manager, reviewed by backend lead and security.
**When:** After the project brief and UI/UX spec. Before any native code is written.

> Applies to: native iOS, native Android, cross-platform (React Native, Flutter, Expo, Capacitor), and hybrid apps that have a meaningful mobile footprint.

---

## 1. Platform Targets

| Platform | Minimum OS version | Target OS version | Architecture | Notes |
|----------|--------------------|-------------------|--------------|-------|
| iOS | `<iOS 16.0>` | `<iOS 18.x>` | `<arm64>` | `<Xcode 16+, Swift 5.9+>` |
| Android | `<API 26 (Android 8.0)>` | `<API 35 (Android 15)>` | `<arm64-v8a, armeabi-v7a>` | `<minSdk 26, targetSdk 35>` |
| iPadOS | `<iPadOS 16.0 — required / nice-to-have / not supported>` | | | |
| Tablets (Android) | `<Support landscape layout: yes / no>` | | | |

**Framework / toolchain:** `<React Native 0.75 | Flutter 3.x | Expo SDK 51 | Swift + UIKit | Kotlin + Jetpack Compose | Capacitor>`

---

## 2. Navigation Model

> Describe the top-level navigation structure and how users move between sections.

| Layer | Pattern | Notes |
|-------|---------|-------|
| Root nav | `<Tab bar (iOS HIG) | Bottom nav (Material) | Drawer | Stack>` | `<e.g. 4 tabs: Home, Search, Activity, Profile>` |
| Secondary nav | `<Push (stack) | Modal sheet | Full-screen takeover>` | |
| Deep-link support | `<yes / no>` | Scheme: `<myapp://path>`, Universal links: `<https://app.example.com/path>` |
| Back navigation | `<System back gesture (iOS) | Android back button + gesture>` | `<Confirm-on-exit for forms>` |
| Auth guard | `<All screens except Sign In, Forgot Password, Onboarding>` | Redirect to `<SignIn>` screen |

---

## 3. Offline Behaviour

> Define what works without a network and how conflicts are resolved.

### 3.1 Offline-Capable Features

| Feature | Offline behaviour | Sync strategy |
|---------|-------------------|---------------|
| `<Read content>` | `<Served from local cache>` | `<Pull on foreground resume>` |
| `<Create / edit>` | `<Queued locally, synced on reconnect>` | `<Last-write-wins | CRDTs | manual conflict UI>` |
| `<Search>` | `<Local index only>` | `<Full reindex on connection>` |
| `<Authentication>` | `<JWT refresh fails → show offline banner, read-only>` | |

### 3.2 Cache Strategy

- Local storage technology: `<SQLite via Drizzle | Realm | Core Data | SharedPreferences | MMKV>`
- Max local cache size: `<50 MB>` — eviction policy: `<LRU>`
- Cache invalidation: `<TTL: 24 h | ETags | Manual purge on logout>`
- Stale-while-revalidate: `<yes / no>`

### 3.3 Conflict Resolution

- Strategy: `<Server wins | Client wins | Last-write-wins | Manual merge UI>`
- Conflict indicator: `<Badge on item | Notification | Toast on sync>`

---

## 4. Push Notifications

### 4.1 Channels & Categories

> Define every notification type. Over-notifying is a top reason users uninstall.

| Channel / Category | Trigger | Priority | User opt-out | Deep-link target |
|--------------------|---------|----------|--------------|-----------------|
| `<Transactional – Order update>` | `<Order status change>` | High | No (legal) | `<OrderDetail screen>` |
| `<Social – New follower>` | `<User follows>` | Default | Yes | `<Profile screen>` |
| `<Marketing – Promo>` | `<Campaign send>` | Low | Yes | `<OfferDetail screen>` |
| `<Silent / Background sync>` | `<Server push>` | Silent | No | None — background work only |

### 4.2 Infrastructure

- iOS: `<APNs via FCM | direct APNs>`
- Android: `<FCM>`
- Backend push service: `<Firebase Cloud Messaging | OneSignal | AWS SNS | custom>`
- Token storage: `<Server stores device token keyed to user ID>`
- Token refresh: `<On app launch if token changed>`

### 4.3 Permission Request Timing

- iOS permission prompt: `<Shown at first meaningful moment after onboarding step X, not on first launch>`
- Rationale shown before prompt: `<"We'll notify you when your order is ready">`
- If denied: `<Show in-app banner with Settings deep-link when notification would have fired>`

---

## 5. Device Permissions

> List every permission the app requests. Justify each one. Unjustified permissions cause store rejections.

| Permission | Platform | When requested | Rationale (shown to user) | Fallback if denied |
|------------|----------|----------------|--------------------------|-------------------|
| Camera | iOS + Android | `<On first photo upload>` | `"To scan receipts and upload photos"` | `<File picker fallback>` |
| Photo Library / Media | iOS + Android | `<On profile photo select>` | `"To choose a profile picture"` | Camera-only or URL input |
| Location (precise) | iOS + Android | `<On map view open>` | `"To show nearby results"` | `<Manual address entry>` |
| Location (background) | iOS only | `<Never / only if tracking feature>` | — | — |
| Contacts | iOS + Android | `<On "invite friends" feature>` | `"To find friends already using the app"` | Manual email input |
| Push Notifications | iOS | `<After onboarding, step 3>` | `"To alert you about order updates"` | Email fallback |
| Microphone | iOS + Android | `<Voice search feature only>` | `"To record voice search"` | Text search |
| Biometric / Face ID | iOS + Android | `<In Security settings>` | `"For faster, more secure sign-in"` | Password fallback |
| Bluetooth | iOS + Android | `<IoT pairing feature only / never>` | — | — |

---

## 6. Performance Budgets (Mobile-Specific)

> Mobile CPUs and batteries are constrained. Set hard targets.

| Metric | Target | Measurement method |
|--------|--------|--------------------|
| Cold start (time to interactive) | `< 2.0 s` | `<Xcode Instruments / Android profiler>` |
| Warm start | `< 0.5 s` | |
| Frame rate | `60 fps` sustained; `120 fps` on ProMotion if supported | |
| Scroll jank | `0 dropped frames` on standard lists | |
| App binary size (initial install) | `< 50 MB` iOS / `< 30 MB` Android AAB | |
| On-device memory (RSS) | `< 150 MB` typical session | |
| Battery drain per hour (background) | `< 2%` | |
| Network: API cold response | `< 300 ms p95` on 4G | |
| Image decode / render (list cell) | `< 16 ms` (one frame) | Async decode off main thread |

---

## 7. Accessibility (Mobile)

> Mobile accessibility requirements layered on top of `.claude/templates/ui-ux-spec.md`.

| Requirement | iOS | Android |
|-------------|-----|---------|
| Dynamic Type / Font scale | Support up to `XXXL` without layout breaks | Support up to `200%` font scale |
| VoiceOver / TalkBack | All interactive elements have `accessibilityLabel` | `contentDescription` on all views |
| Reduce Motion | Respect `UIAccessibility.isReduceMotionEnabled` | Respect `ANIMATOR_DURATION_SCALE = 0` |
| Colour inversion / High contrast | Test with Smart Invert + Increase Contrast | Test with High Contrast Text |
| Minimum touch target | 44×44 pt | 48×48 dp |
| Haptic feedback | Use for destructive confirmations, successes | Use `HapticFeedback` API |

---

## 8. Security (Mobile-Specific)

> See also `.claude/templates/security-model.md`.

| Control | Requirement |
|---------|-------------|
| Token storage | `<iOS: Keychain | Android: EncryptedSharedPreferences / Keystore>` — never AsyncStorage plain text |
| Certificate pinning | `<Required for sensitive endpoints / Not required>` — update strategy: `<OTA config push>` |
| Root / jailbreak detection | `<Warn user | Block login | Not enforced>` |
| Screenshot prevention | `<FLAG_SECURE (Android) / `.withSecure(true)` (iOS) on sensitive screens: payment, PII>` |
| Biometric auth binding | Keys bound to biometric enrollment; invalidated if new biometric added |
| Obfuscation | `<ProGuard / R8 (Android) | bitcode disabled (iOS)>` |
| API keys in bundle | Zero — all secrets via server-side proxy |

---

## 9. Background Processing

> Define what work runs while the app is not in focus.

| Task | Platform | API used | Frequency | Battery impact |
|------|----------|----------|-----------|----------------|
| `<Sync pending queue>` | iOS + Android | `<BGAppRefreshTask / WorkManager>` | `<System-scheduled, ~15 min min>` | Low |
| `<Download media>` | iOS + Android | `<URLSession background / DownloadManager>` | On demand | Medium |
| `<Location tracking>` | iOS only | `<CLLocationManager significant-change>` | Event-driven | `<High — justify carefully>` |

---

## 10. App Store Metadata

### 10.1 iOS (App Store Connect)

| Field | Value |
|-------|-------|
| App Name | `<30 chars max>` |
| Subtitle | `<30 chars max — primary keyword>` |
| Category | `<Primary: e.g. Productivity | Secondary: Utilities>` |
| Age rating | `<4+ | 9+ | 12+ | 17+>` |
| Keywords (100 chars) | `<keyword1, keyword2, ...>` |
| Support URL | `<https://example.com/support>` |
| Privacy Policy URL | `<https://example.com/privacy>` |
| Short description (100 chars) | `<>` |
| Full description (4000 chars) | `<>` |
| In-App Purchases declared | `<Yes / No>` |
| Privacy nutrition labels | `<Data types collected: email, usage data, device ID>` |

### 10.2 Android (Google Play Console)

| Field | Value |
|-------|-------|
| App Name | `<50 chars max>` |
| Short description | `<80 chars>` |
| Full description | `<4000 chars>` |
| Category | `<e.g. Productivity>` |
| Content rating | `<Everyone | Teen | Mature 17+>` |
| Target audience age | `<18+ | 13–17 | mixed>` |
| Data safety section | `<Data collected, shared, security practices — must match actual behaviour>` |
| App signing | `<Play App Signing (recommended)>` |

---

## 11. Update & Versioning Strategy

| Aspect | Decision |
|--------|----------|
| Version scheme | `<SemVer: MAJOR.MINOR.PATCH>` |
| Forced update mechanism | `<Server flag → in-app modal blocking old versions below min_version>` |
| OTA updates (React Native / Expo) | `<CodePush / Expo Updates — allowed for JS bundle only; native changes require store release>` |
| Feature flags | `<Remote config via Firebase RC / LaunchDarkly / custom>` |
| Beta / TestFlight channel | `<Internal: engineers | External: power users waitlist>` |

---

## 12. Open Questions

| # | Question | Owner | Date needed |
|---|----------|-------|-------------|
| 1 | `<e.g. Is iPad a launch requirement or fast-follow?>` | `<PM>` | `<YYYY-MM-DD>` |
| 2 | `<e.g. Which offline-first library: WatermelonDB vs Realm vs SQLite?>` | `<Mobile lead>` | `<YYYY-MM-DD>` |

---

## 13. Related Documents

- UI/UX spec: `.claude/templates/ui-ux-spec.md`
- Security model: `.claude/templates/security-model.md`
- Performance plan: `.claude/templates/performance-plan.md`
- Testing strategy: `.claude/templates/testing-strategy.md`
- Architecture: `.claude/templates/architecture.md`

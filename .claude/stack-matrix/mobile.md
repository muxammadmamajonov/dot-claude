# Mobile Stack Matrix

The core decision is **cross-platform vs native**. Cross-platform (Flutter, React Native, Expo, KMP, Ionic) cuts development cost but trades some platform fidelity and access to the latest OS APIs. Native (Swift/SwiftUI, Kotlin/Compose) delivers the best performance, deepest OS integration, and first-day API access at the cost of maintaining two codebases. Choose cross-platform when your team is small or the UI is not deeply platform-idiomatic; choose native when platform feel, performance, or hardware integration is a primary product differentiator.

---

## Flutter

- **When to use:** Consumer apps targeting iOS + Android (and optionally web/desktop) with a custom, branded UI that does not need to look like native platform controls; teams who can invest in learning Dart.
- **When NOT to use:** Projects that must use existing React Native or web JS libraries; apps that require very deep platform-specific UI idioms (e.g., deeply integrated iOS share sheets); teams allergic to Dart.
- **Strengths:** Single codebase for iOS, Android, web, macOS, Windows, Linux; own rendering engine (Impeller) means pixel-perfect UI everywhere; excellent hot reload; strong typing with Dart; growing ecosystem; Google-backed.
- **Weaknesses:** Dart is not used elsewhere in most stacks; large binary size vs native; web output quality still lags behind native web frameworks; plugin ecosystem narrower than React Native.
- **Team fit:** Teams willing to learn Dart; design-led products with custom UI; teams that want one codebase across mobile + desktop.
- **Scale fit:** Scales well; used in production by Google Pay, Alibaba, BMW. Performance degrades only in extremely complex scrolling lists without careful `ListView` tuning.
- **Production risks:** App Store / Play Store submission with Flutter plugins sometimes lags OS betas; Dart null-safety migration complexity for older codebases; binary size can be large.

---

## React Native

- **When to use:** Teams with existing React/JavaScript expertise; apps that benefit from the npm ecosystem; projects that want near-native look via platform-native components; brownfield integration into existing native apps.
- **When NOT to use:** Highly performance-sensitive games or apps with custom rendering; teams with no JS background; apps needing APIs unavailable in the RN bridge.
- **Strengths:** Reuse JS/TS expertise; large npm ecosystem; the New Architecture (JSI + Fabric + TurboModules) eliminates the old bridge bottleneck; Meta-backed; Expo layer reduces configuration burden significantly.
- **Weaknesses:** JavaScript bridge (old arch) or JSI (new arch) still adds overhead vs true native; ecosystem fragmentation between old and new architecture libraries; Android styling can require extra effort to match iOS.
- **Team fit:** Web teams expanding to mobile; full-stack JS shops; teams that want to share business logic with a web app.
- **Scale fit:** Good. Used in production by Facebook, Shopify, Microsoft Outlook. Performance ceiling is below native but above what most apps require.
- **Production risks:** New Architecture migration is ongoing and some libraries are not yet compatible; OTA updates (CodePush/EAS Update) introduce deployment complexity; platform divergence creep over time.

---

## Expo

- **When to use:** React Native projects that want to avoid native build toolchain pain; MVPs and prototypes; teams without dedicated mobile DevOps; over-the-air update workflows.
- **When NOT to use:** Apps that require native modules not yet in Expo's ecosystem and where ejecting adds unacceptable complexity; teams that need full control over the native layer from day one.
- **Strengths:** Eliminates Xcode/Android Studio setup for most workflows; EAS Build handles CI; EAS Update for OTA; Expo Router for file-based navigation; tight React Native integration; excellent documentation.
- **Weaknesses:** EAS Build costs money at scale; managed workflow limits custom native code (dev clients help but add complexity); a layer of abstraction that can obscure native problems.
- **Team fit:** Web teams building their first mobile app; startups that cannot afford mobile DevOps; solo developers.
- **Scale fit:** Scales to production; many large apps use Expo. Eject to bare workflow when you outgrow managed.
- **Production risks:** Expo SDK version lock-in; major SDK upgrades can require significant dependency updates; EAS service outages affect CI/CD pipelines.

---

## Native iOS (Swift / SwiftUI)

- **When to use:** iOS-first products where platform feel is a core value proposition; apps with deep OS integration (WidgetKit, Live Activities, ARKit, HealthKit, CarPlay); performance-critical applications.
- **When NOT to use:** Projects targeting Android simultaneously without separate team; startups with a single developer or small team and tight budget.
- **Strengths:** First-day access to new Apple APIs; best possible iOS performance and battery efficiency; full access to all SwiftUI/UIKit patterns; Swift concurrency (async/await, actors) is excellent; App Store reviewers favor polished native apps.
- **Weaknesses:** iOS-only; larger team required for parity with Android; SwiftUI still has gaps in complex list performance and some UIKit features.
- **Team fit:** Dedicated iOS engineers; companies with separate iOS and Android teams; Apple-ecosystem-first companies.
- **Scale fit:** No ceiling — all of Apple's own apps are native. SwiftUI scales to complex apps with proper architecture (TCA, MVVM, etc.).
- **Production risks:** SwiftUI breaking changes between iOS versions; macOS Catalyst builds often require extra work; App Store review delays.

---

## Native Android (Kotlin / Jetpack Compose)

- **When to use:** Android-first or Android-only products; apps needing deep Android OS integration (Foreground Services, WorkManager, custom keyboards, accessibility services); Google Play ecosystem.
- **When NOT to use:** iOS-first products; teams without Kotlin experience and timeline pressure.
- **Strengths:** Full Android API access; Jetpack Compose is a modern, productive UI toolkit on par with SwiftUI; excellent Kotlin coroutines and Flow for async; strong Material Design support; free tooling (Android Studio).
- **Weaknesses:** Android-only; device fragmentation testing is expensive; Play Store policies change frequently; Compose is maturing but some APIs are still experimental.
- **Team fit:** Android-specialist engineers; teams building Android-first B2B/enterprise apps.
- **Scale fit:** No technical ceiling. All major Android apps are Kotlin-native.
- **Production risks:** Device fragmentation (OEM UI skins, Android version spread); Play Store policy changes; Compose API stability still evolving in some areas.

---

## Kotlin Multiplatform (KMP)

- **When to use:** Teams that want to share business logic, networking, and data layers across iOS and Android while keeping native UI on each platform; organizations with separate iOS and Android teams who want to reduce duplication.
- **When NOT to use:** Teams without Kotlin expertise; projects where cross-platform UI is the goal (use Flutter instead); very small teams who cannot staff both iOS and Android UI engineers.
- **Strengths:** Share only what makes sense (data models, network, business rules) while retaining fully native UI; Kotlin is idiomatic on both platforms; JetBrains-backed with strong tooling; Compose Multiplatform adds optional shared UI.
- **Weaknesses:** Requires native iOS and Android engineers for the UI layer; Kotlin/Native compilation is slow; ecosystem for KMP-specific libraries is smaller; Xcode integration has friction.
- **Team fit:** Mid-to-large teams with both iOS and Android engineers; companies rewriting a shared backend SDK for mobile.
- **Scale fit:** Excellent — this is how large apps (Netflix, Philips, VMware) reduce duplication without sacrificing native quality.
- **Production risks:** Swift interop has rough edges; debug experience in Kotlin/Native is weaker than JVM; Compose Multiplatform UI parity with native still incomplete.

---

## Ionic / Capacitor

- **When to use:** Web teams (Angular, React, Vue) who need to ship a mobile app quickly and have no budget for native engineers; enterprise internal tools where near-native feel is acceptable; apps that are primarily web UIs wrapped in a shell.
- **When NOT to use:** Consumer-facing apps competing with polished native experiences; performance-intensive applications; apps needing deep hardware access (AR, real-time audio, BLE intensive use).
- **Strengths:** Reuse existing web codebase almost entirely; Capacitor replaces Cordova with a modern, maintained bridge; access to native APIs via Capacitor plugins; single codebase for web + iOS + Android.
- **Weaknesses:** Performance is noticeably below native and Flutter in scrolling, animations, and CPU-heavy tasks; UI looks like a web app, not a native app, without significant custom styling; web view battery consumption is higher.
- **Team fit:** Web developers who need mobile with no mobile expertise; enterprise IT teams with Angular codebases.
- **Scale fit:** Adequate for internal tools and simple consumer apps; hits a ceiling in performance and UI polish at scale.
- **Production risks:** WebView differences across Android OEMs; App Store rejection risk for apps that are purely web wrappers without sufficient native value-add; Capacitor plugin maintenance varies by author.

---

## Comparison Table

| Framework              | Languages       | Platforms          | UI Rendering     | Performance  | Ecosystem  | Native API Access | Hiring Pool |
|------------------------|-----------------|--------------------|------------------|--------------|------------|-------------------|-------------|
| Flutter                | Dart            | iOS, Android, Web, Desktop | Own (Impeller) | High     | Growing    | Via plugins        | Medium      |
| React Native           | JS / TS         | iOS, Android       | Native widgets   | Medium-High  | Large      | Via JSI/bridge     | Large       |
| Expo                   | JS / TS         | iOS, Android, Web  | Native widgets   | Medium-High  | Large      | Via EAS/plugins    | Large       |
| Native iOS (Swift)     | Swift           | iOS, macOS, tvOS   | Native (UIKit/SwiftUI) | Highest | Largest (Apple) | Full        | Medium      |
| Native Android (Kotlin)| Kotlin          | Android            | Native (Compose) | Highest      | Large      | Full              | Medium      |
| Kotlin Multiplatform   | Kotlin + Swift  | iOS, Android       | Native per platform | Highest  | Medium     | Full              | Small-Med   |
| Ionic / Capacitor      | JS / TS         | iOS, Android, Web  | WebView          | Low-Medium   | Large (web)| Via plugins        | Large       |

---

## Recommended Combinations

| Combination                                   | Why                                                                                          |
|-----------------------------------------------|----------------------------------------------------------------------------------------------|
| Flutter + Dart + Riverpod + Supabase          | Fast cross-platform with consistent UI; Riverpod is the modern state management choice      |
| React Native + Expo + TypeScript + Zustand    | Best developer velocity for JS teams; EAS handles CI/CD; Zustand keeps state simple         |
| Swift/SwiftUI + TCA + Combine                 | Principled iOS architecture; The Composable Architecture enforces testability at scale       |
| Kotlin/Compose + ViewModel + Hilt             | Modern Android stack; coroutines + Flow for async; Hilt for DI; aligns with Google guidance |
| KMP + Swift UI (iOS) + Compose (Android)      | Shared business logic, fully native UI per platform; best quality ceiling for dual-platform  |
| Expo + React Native + tRPC                    | Full TypeScript monorepo sharing API types between mobile and backend                       |

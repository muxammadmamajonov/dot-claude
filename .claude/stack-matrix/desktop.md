# Desktop Stack Matrix

Desktop app choice hinges on three tensions: **native fidelity vs cross-platform reach**, **binary size vs development speed**, and **existing team skills vs ideal tech**. If your team builds web apps and the desktop is a secondary channel, Electron or Tauri are natural bridges. If platform-native UX and OS integration are core to your product's value, choose platform-native (Swift/WinUI/GTK). Qt sits in a unique position for complex, performance-sensitive cross-platform apps in industrial, scientific, or embedded-adjacent domains.

---

## Electron

- **When to use:** Teams with web (HTML/CSS/JS/TS) skills who need a desktop app quickly; apps that are fundamentally web UIs (dashboards, editors, communication tools); projects where cross-platform parity and web ecosystem access matter more than binary size.
- **When NOT to use:** Apps where binary size, RAM consumption, or startup time are product requirements; system utilities that need deep OS integration without heavy abstraction; mobile/embedded targets.
- **Strengths:** Reuse entire web stack and npm ecosystem; Chromium rendering means pixel-perfect cross-platform UI; fastest path from web app to desktop app; huge adoption (VS Code, Slack, Discord, Figma, 1Password); active ecosystem (Electron Forge, electron-builder).
- **Weaknesses:** Ships a full Chromium + Node.js runtime — binaries are 80–200 MB minimum; RAM usage is notoriously high (150–500 MB at idle for simple apps); startup time is slow; security surface is large (context isolation and sandbox must be configured deliberately).
- **Team fit:** Web developers expanding to desktop; product teams where UI consistency across web and desktop is required; teams that cannot afford to learn a new language.
- **Scale fit:** Scales to very complex apps (VS Code is proof). Performance ceiling is Chromium's, not your app's, for most use cases.
- **Production risks:** Auto-updater implementation is non-trivial; code signing for macOS (notarization) and Windows (EV cert) adds release pipeline complexity; sandbox misconfigurations create RCE attack surface; Chromium version lag vs web can cause compatibility issues.

---

## Tauri

- **When to use:** Teams wanting Electron-like DX (web frontend) but needing a much smaller binary and lower memory footprint; security-conscious apps; Rust-capable teams who want native performance in the backend; apps where the OS WebView is acceptable.
- **When NOT to use:** Apps that must render identically on all platforms (OS WebView varies: WebKit on macOS/Linux, WebView2 on Windows); teams with no Rust exposure and no appetite to learn it for backend logic; projects needing Chromium-specific web features not in OS WebViews.
- **Strengths:** Binary sizes of 3–15 MB vs 80–200 MB for Electron; uses OS WebView (no bundled Chromium); Rust backend is memory-safe and fast; better security model by default; growing ecosystem (Tauri v2 supports mobile targets — iOS/Android); IPC between JS and Rust is ergonomic.
- **Weaknesses:** OS WebView inconsistencies mean CSS/JS bugs that only appear on specific OS versions; Rust learning curve for backend logic; smaller plugin ecosystem than Electron; Tauri v2 mobile support is still maturing.
- **Team fit:** Web developers who also have or can add Rust expertise; security-focused product teams; teams building tools where download size matters (developer tools, CLI companions).
- **Scale fit:** Suitable for small utilities to complex apps. Performance ceiling is higher than Electron for CPU-heavy work because Rust backend handles compute.
- **Production risks:** WebView2 on Windows requires end-user installation on older Windows versions (bundled option exists but adds size); WebKit rendering bugs on older macOS; Tauri v2 API surface is still stabilizing.

---

## Qt

- **When to use:** Complex, performance-sensitive cross-platform desktop apps; industrial, scientific, medical, or embedded-adjacent GUIs; apps that must run on Linux (including embedded Linux), Windows, and macOS with native-like performance; teams with C++ or Python (PyQt/PySide) expertise.
- **When NOT to use:** Web-developer teams with no C++ appetite; simple CRUD desktop apps where Electron or Tauri would deliver faster; apps targeting only one OS where native toolkits are simpler.
- **Strengths:** True cross-platform native-feel widgets (or QML for custom UIs); extremely high performance (C++ core); runs on embedded Linux, automotive, medical devices; Qt Quick/QML enables fluid animated UIs; LTS releases with long commercial support; comprehensive tooling (Qt Creator, Qt Design Studio).
- **Weaknesses:** Commercial licensing is expensive for closed-source apps (LGPL is free but has requirements); C++ complexity; Qt's own meta-object system (moc) adds a compilation step; QML learning curve on top of C++; slower to build than scripting-language alternatives.
- **Team fit:** C++ engineers; embedded/systems teams; scientific instrument vendors; automotive UI teams; teams needing decades-long maintainability.
- **Scale fit:** No upper bound — Qt powers mission-critical systems at Bosch, BMW, Siemens, and medical device manufacturers.
- **Production risks:** Commercial license cost surprises at scale; moc/QObject memory management traps for C++ beginners; cross-compilation for embedded targets requires careful toolchain setup; UI code and C++ backend tightly coupled without discipline.

---

## .NET MAUI

- **When to use:** .NET/C# teams who need to target Windows, macOS, iOS, and Android from one codebase; organizations in the Microsoft ecosystem; teams migrating from Xamarin.Forms.
- **When NOT to use:** Teams without .NET experience; projects where iOS/Android is not a target and WPF or WinUI would suffice; performance-critical native apps where each platform's native toolkit is preferred.
- **Strengths:** Single codebase for Windows, macOS, iOS, Android; C# and .NET ecosystem; AOT compilation improves startup and size; integrates with Visual Studio and Azure; good for enterprise line-of-business apps; Blazor Hybrid lets web devs reuse Razor components.
- **Weaknesses:** macOS and iOS experience still lags Windows quality; renderer inconsistencies across platforms; slower evolution than Flutter; smaller community than React Native or Flutter for mobile targets; tooling is primarily Windows-focused (VS for Mac was discontinued).
- **Team fit:** Microsoft-stack developers; teams maintaining Xamarin apps; enterprise .NET shops adding mobile/desktop channels.
- **Scale fit:** Good for enterprise LOB apps. Not the first choice for consumer apps competing with native polish.
- **Production risks:** macOS rendering and platform API gaps; hot reload reliability in complex scenarios; Mac Catalyst support has quirks; Play Store and App Store submission from .NET MAUI requires extra signing configuration.

---

## Flutter Desktop

- **When to use:** Teams already using Flutter for mobile who want to extend to desktop without a new framework; apps needing a consistent, custom-branded UI across mobile and desktop; multi-platform products where a unified codebase is a business requirement.
- **When NOT to use:** Desktop-only apps where adopting Flutter solely for desktop is hard to justify; apps needing deep OS integration (system tray, native menus, OS notification APIs are limited); teams not already invested in Flutter/Dart.
- **Strengths:** True single codebase across iOS, Android, macOS, Windows, Linux, and web; own rendering engine means pixel-perfect consistency; hot reload; growing desktop plugin ecosystem; Impeller renderer delivers smooth animations.
- **Weaknesses:** Desktop support is younger than mobile — some platform APIs (system tray, window management, native menus) require platform channel code or third-party plugins; Dart is not useful outside Flutter; desktop app conventions (right-click menus, window chrome) need manual implementation.
- **Team fit:** Flutter mobile teams adding desktop; teams building cross-platform tools where UI consistency is more important than native OS convention adherence.
- **Scale fit:** Suitable for complex apps. Impeller handles demanding UIs; compute-heavy work should be offloaded via platform channels or isolates.
- **Production risks:** Desktop plugin ecosystem gaps; Windows app signing complexity; macOS notarization; Linux app distribution (Snap, AppImage, Flatpak) adds packaging overhead; flutter_windows, flutter_macos, flutter_linux rendering differences can surface subtle bugs.

---

## Native — Swift/SwiftUI (macOS), WinUI 3 (Windows), GTK (Linux)

- **When to use:** Apps where deep OS integration, platform conventions, and first-class accessibility are product requirements; macOS utilities, menubar apps, Windows LOB tools, Linux desktop environments; apps that must use OS-specific APIs (Core Data, HealthKit, Windows Registry, D-Bus) without abstraction layers.
- **When NOT to use:** Cross-platform products — each native toolkit is OS-specific; small teams that cannot staff platform-specialist engineers; apps where web or cross-platform alternatives would deliver equivalent user value.
- **Strengths:**
  - **Swift/SwiftUI**: First-day macOS API access; best macOS UX fidelity; excellent performance; Swift concurrency; seamless iCloud/Keychain/Handoff integration.
  - **WinUI 3 (Windows App SDK)**: Modern Windows 11 design language; full Windows API access; excellent accessibility (UIA); integrates with MSIX packaging and Windows Update.
  - **GTK (C/Python/Rust bindings)**: Standard Linux desktop toolkit (GNOME); Rust bindings (gtk4-rs) are modern; Flatpak distribution is well-supported.
- **Weaknesses:** Platform-specific — separate codebases for each OS; SwiftUI has gaps in complex list performance; WinUI 3 is still maturing (less complete than WPF for some scenarios); GTK documentation and design guidance lags behind Apple/Microsoft equivalents.
- **Team fit:** Platform specialists; companies building OS-native products (utilities, dev tools, productivity apps) where platform feel is a differentiator.
- **Scale fit:** No technical ceiling — all OS vendors' own apps are native.
- **Production risks:**
  - Swift/SwiftUI: API changes between macOS versions; notarization and Gatekeeper requirements; SwiftUI previews unreliable for complex views.
  - WinUI 3: MSIX packaging learning curve; Windows version targeting complexity; WinRT API surface is large and documentation is dense.
  - GTK: Distribution across distros; theme inconsistency; accessibility testing requires assistive technology setup.

---

## Comparison Table

| Framework          | Languages       | Platforms                    | Binary Size  | RAM Usage | OS Integration | Dev Velocity | Best For                              |
|--------------------|-----------------|------------------------------|--------------|-----------|----------------|--------------|---------------------------------------|
| Electron           | JS / TS         | Win, macOS, Linux            | 80–200 MB    | High      | Via Node APIs  | Highest      | Web-to-desktop, editors, dashboards   |
| Tauri              | JS/TS + Rust    | Win, macOS, Linux (+ mobile) | 3–15 MB      | Low       | Via Rust       | High         | Perf/size-conscious cross-platform    |
| Qt                 | C++ / QML / Py  | Win, macOS, Linux, Embedded  | Medium       | Low       | Deep           | Medium       | Industrial, scientific, embedded GUI  |
| .NET MAUI          | C#              | Win, macOS, iOS, Android     | Medium       | Medium    | Via .NET APIs  | Medium       | Microsoft-stack multi-platform        |
| Flutter Desktop    | Dart            | Win, macOS, Linux (+mobile)  | Medium       | Medium    | Via plugins    | High         | Mobile-extending-to-desktop           |
| Native Swift/WinUI/GTK | Swift/C#/C/Rust | Single OS each           | Small        | Lowest    | Full           | Low-Medium   | OS-first utilities and tools          |

---

## Recommended Combinations

| Combination                                    | Why                                                                                              |
|------------------------------------------------|--------------------------------------------------------------------------------------------------|
| Tauri + React/Vite + TypeScript + Rust backend | Best balance of web DX and small binary; Rust handles any performance-sensitive background work  |
| Electron + React + TypeScript + electron-builder | Fastest web-to-desktop path; huge ecosystem; proven at VS Code scale                           |
| Flutter Desktop + Dart + Riverpod              | Best choice when already shipping Flutter mobile; unified state management across platforms      |
| Qt + QML + C++ + CMake                         | Cross-platform industrial/scientific apps; QML for fluid UI, C++ for performance-critical logic  |
| Swift/SwiftUI + Combine + CloudKit             | macOS-first productivity apps; deep Apple ecosystem integration; clean async model              |
| .NET MAUI + C# + Blazor Hybrid + Azure         | Microsoft-stack teams needing desktop + mobile from one codebase with Azure backend             |

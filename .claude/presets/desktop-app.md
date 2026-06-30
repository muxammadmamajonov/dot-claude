# Desktop Application Preset

## Project type
Application installed and run on end-user computers. Variants: cross-platform (Electron, Tauri, Flutter Desktop, .NET MAUI), macOS-native (SwiftUI/AppKit), Windows-native (WPF, WinUI 3, Win32), Linux-native (GTK, Qt), or packaged CLI with GUI shell. Includes productivity tools, developer tools, creative apps, enterprise desktop clients, and kiosk/embedded desktop applications.

## Typical use cases
- Developer and power-user tools (IDEs, terminals, database GUIs, API clients)
- Creative tools (image editors, video editors, DAWs, CAD)
- Enterprise thick clients (ERP clients, point-of-sale, kiosk)
- Communication apps (chat, video conferencing, mail)
- Local-first productivity (note-taking, task management, document editors)
- Scientific/engineering apps with heavy computation or hardware I/O

## Required discovery questions
1. Which operating systems must be supported at launch — macOS, Windows, Linux, or all three? What are the minimum OS versions?
2. Is this a local-first app (data lives on disk), cloud-synced, or a thin client streaming from a server?
3. Does the app require privileged OS access — filesystem outside sandbox, native hardware (USB/HID/BLE), kernel extensions, or system tray / menu bar?
4. What is the distribution channel — Mac App Store, Microsoft Store, direct download with auto-update, or enterprise MDM push?
5. Does the app handle user-owned files (open/save arbitrary paths)? What file formats — proprietary binary, open standard, or both?
6. Are there licensing or activation requirements — single seat, floating, node-locked, or subscription-gated features?
7. What are the performance expectations — does the app need 60 fps rendering, GPU acceleration, or CPU-intensive background processing?
8. Does the app need to communicate with external hardware (serial/USB/BLE devices, cameras, audio interfaces)?
9. Is offline-only operation required, or does the app have online features (sync, collaboration, marketplace)?
10. Are enterprise deployment requirements needed — MSI/PKG silent install, group policy, SSO/SAML, proxy-aware networking?

## Recommended agents

### Core
- `.claude/agents/core/orchestrator.md` — feature phasing, platform parity tracking
- `.claude/agents/core/solution-architect.md` — process model (main/renderer), IPC design, data layer
- `.claude/agents/core/project-manager.md` — milestone planning across platforms

### Engineering
- `.claude/agents/engineering/desktop-engineer.md` — window management, menus, native OS integration
- `.claude/agents/engineering/backend-engineer.md` — local services, embedded DB, sync engine
- `.claude/agents/engineering/backend-engineer.md` — license activation, SSO, OS keychain integration

### Quality
- `.claude/agents/quality/qa-engineer.md` — multi-OS test matrix, installer regression
- `.claude/agents/quality/performance-engineer.md` — startup time, memory profiling, GPU usage
- `.claude/agents/quality/security-auditor.md` — sandbox entitlements, auto-update signing, local data encryption

### Design
- `.claude/agents/design/ui-ux-designer.md` — HIG (macOS) / Fluent (Windows) conformance, keyboard shortcuts
- `.claude/agents/design/accessibility-designer.md` — platform accessibility APIs (NSAccessibility, UIA)

### Domain
- `.claude/agents/engineering/release-engineer.md` — code signing, notarisation (macOS), MSIX/Inno Setup (Windows)
- `.claude/agents/engineering/release-engineer.md` — Sparkle, Squirrel, or custom auto-update pipeline

## Recommended skills
- `.claude/skills/desktop/SKILL.md` — window lifecycle, IPC, native menus, tray
- `.claude/skills/data-modeling/SKILL.md` — embedded SQLite, file watchers, migration
- `.claude/skills/security/SKILL.md` — OS keychain, license key validation, OAuth PKCE from desktop
- `.claude/skills/security/SKILL.md` — app signing, notarisation, auto-update trust chain
- `.claude/skills/testing/SKILL.md` — unit, integration, UI automation (Playwright, XCTest, WinAppDriver)
- `.claude/skills/performance/SKILL.md` — render loop profiling, main-thread unblocking, memory leaks
- `.claude/skills/devops/SKILL.md` — DMG/PKG, MSIX/EXE, AppImage/Flatpak, CI signing pipelines

## Recommended stack options

| Stack | Rationale |
|---|---|
| **Tauri 2 + Rust backend + React/Svelte frontend** | Smallest bundle size; Rust backend for performance/safety; strong security sandbox; cross-platform. See `.claude/stack-matrix/desktop.md` |
| **Electron + Node.js + React/Vue** | Largest ecosystem; most third-party integrations; proven at scale (VS Code, Slack, Figma); large binary but acceptable for many use cases |
| **Flutter Desktop + Dart** | Pixel-perfect custom UI across all platforms from one codebase; best for design-heavy or creative tools |
| **SwiftUI (macOS) + WinUI 3 (Windows)** | Maximum native integration and performance; two codebases but best OS fidelity; choose when platform depth matters most |

Reference `.claude/stack-matrix/desktop.md`, `.claude/stack-matrix/backend.md` for detailed tradeoffs.

## Required checklists
- `.claude/checklists/security.md` — code signing, sandboxing, IPC validation, auto-update integrity
- `.claude/checklists/performance.md` — cold start ≤ 3 s, main-thread budget, memory baseline
- `.claude/checklists/accessibility.md` — platform accessibility APIs, keyboard-only navigation
- `.claude/checklists/launch.md` — notarisation, installer testing, silent install, rollback
- `.claude/checklists/desktop.md` — DMG/PKG/MSIX build, signing certs, delta updates

## MVP scope pattern

**In MVP**
- Main window with core user flow
- File open/save if applicable (with OS native dialogs)
- Preferences window (minimal: theme, account)
- Auto-updater (mandatory — you must be able to ship fixes without user re-downloading)
- Crash reporting
- Code-signed and notarised installer

**Deferred to v2**
- Multi-window or multi-document support
- Plugin / extension system
- System tray / menu bar agent mode
- Hardware peripheral integration
- Cloud sync engine
- Enterprise SSO/SAML
- Offline license activation

## Production risks

| Risk | Severity | Mitigation |
|---|---|---|
| Auto-update not signed / MITM-able | P0 | Sign update archives with EdDSA (Sparkle) or Azure Code Signing; verify on install |
| Unnotarised macOS binary blocked by Gatekeeper | P0 | Notarise with Apple every release; test on a clean macOS VM before shipping |
| Electron main-process exposed to arbitrary code via IPC | P0 | Validate all IPC messages; `contextIsolation: true`; no `nodeIntegration` in renderer |
| Plain-text credentials in app's local storage / config files | P0 | Store all secrets in OS Keychain / Credential Manager; never write to config files |
| Memory leak in long-running background threads | P1 | Profile with Instruments / Memory Profiler before each release; set memory budget alert |
| App crash on specific OS version or hardware | P1 | CI matrix covering oldest supported OS; automated installer smoke tests |
| Large binary size triggering user uninstall | P1 | Tree-shake, use Tauri or native if bundle size is critical; show size before download |
| Permissions not requested gracefully (camera, microphone) | P1 | Request at first use with explanatory prompt; handle denial gracefully |
| Hardcoded file paths breaking on non-English Windows | P2 | Use OS APIs for paths (`NSSearchPathForDirectoriesInDomains`, `SHGetKnownFolderPath`) |
| Blocking the main thread causing UI freeze | P2 | All I/O and computation off the main thread; test with slow HDD simulation |

## Launch requirements
- App signed and notarised (macOS) / signed with EV certificate (Windows) before any public distribution
- Auto-updater tested end-to-end: old version detects update, downloads, verifies signature, installs cleanly
- Installer tested on clean VMs for each supported OS version
- Crash reports wired and producing alerts before beta
- EULA / license agreement shown and accepted during install
- Uninstaller leaves no orphaned files or registry entries
- Privacy policy linked from app About screen
- Performance baseline documented (startup time, idle memory) so regressions are detectable

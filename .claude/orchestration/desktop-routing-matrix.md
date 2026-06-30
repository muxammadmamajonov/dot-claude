# Desktop Engineering Routing Matrix — the elite desktop team, assembled per task

The orchestrator's desktop routing layer (macOS / Windows / Linux). Detects the framework, activates
the **minimal** specialist set, picks an operating **mode**, and runs the right verification loop.
Complements `.claude/orchestration/routing-matrix.md` (universal). Activate only what the task needs.

## Framework detection (first step)
Run `.claude/agents/core/codebase-mapper.md`; classify the desktop target:

| Signal | Target → primary specialist |
|---|---|
| `package.json` + `electron` / electron-builder / electron-forge | Electron → `engineering/electron-engineer` |
| `src-tauri/` + `tauri.conf.json` / Cargo + `tauri` | Tauri → `engineering/tauri-engineer` |
| `pubspec.yaml` with desktop targets (`windows/`,`macos/`,`linux/`) | Flutter Desktop → `stack/mobile/flutter-engineer` |
| `*.csproj` + WinUI/WPF/WinForms/Avalonia/Uno/MAUI | .NET Desktop → `stack/backend/dotnet-engineer` (desktop caveats below) |
| `*.xcodeproj` + AppKit/SwiftUI (macOS target, not iOS) | Native macOS → `engineering/desktop-engineer` (+ Swift skill) |
| `CMakeLists.txt`/`*.pro` + Qt / GTK / wxWidgets | Native C++/Qt/GTK → `engineering/desktop-engineer` |
| Cargo + `egui`/`iced`/`slint`/`dioxus`/`wails` | Rust/Go GUI → `engineering/desktop-engineer` (+ rust-backend/go-backend skill) |
| **Mixed** (web dashboard + desktop client + backend) | union per surface; keep web/mobile/desktop teams separate |

> Electron and Tauri cover the majority of new cross-platform desktop apps → first-class specialists.
> Native (AppKit/WinUI/WPF/Qt/GTK), Flutter Desktop, and .NET desktop route to `desktop-engineer` /
> the matching stack engineer plus the platform caveats here — kept as routing knowledge, not always loaded.

## Operating modes (orchestrator picks ONE)
audit-only · fix-and-verify · production-hardening · ui-ux-polish · security-review · performance-review ·
release-readiness · **desktop-packaging-readiness** · **auto-update-readiness** · store-readiness · documentation.

## Task → team (desktop)
| Desktop task | Lead | Support | Skills | Checklists |
|---|---|---|---|---|
| Map / classify | `core/codebase-mapper` | — | discovery | — |
| App architecture (IPC, multi-process, plugins, undo/redo) | `core/solution-architect` | `engineering/desktop-engineer` | architecture, desktop | architecture, desktop |
| Electron build | `engineering/electron-engineer` | desktop-security-auditor | desktop | desktop, web |
| Tauri build | `engineering/tauri-engineer` | desktop-security-auditor, rust-backend | desktop | desktop |
| Flutter Desktop | `stack/mobile/flutter-engineer` | desktop-engineer | flutter, desktop | desktop |
| .NET / native / Qt / GTK | `engineering/desktop-engineer` | matched stack engineer | desktop | desktop, accessibility |
| UI/UX (native conventions, menus, tray, shortcuts, multi-window, hi-DPI) | `design/ui-ux-designer` | design-system-architect | ui-ux-design | ui-ux, accessibility |
| Accessibility (VoiceOver/Narrator/Orca, keyboard-only, focus) | `quality/accessibility-auditor` | ui-ux-designer | ui-ux-design | accessibility |
| Local storage / offline / sync (SQLite, Core Data, encrypted store) | `engineering/desktop-engineer` | database-architect | data-modeling, sqlite | database, data-model |
| Networking / backend integration (proxy, offline queue, resumable) | `engineering/desktop-engineer` | api-architect, integration-engineer | api-design, realtime | api, backend |
| Security (secure storage, IPC, signing, supply chain) | `quality/desktop-security-auditor` | security-auditor, auth-permission-reviewer | security | security, dependencies |
| Electron/Tauri shell security | `quality/desktop-security-auditor` | electron/tauri engineer | security | security |
| Permissions / OS integration (FS, tray, autostart, protocol handlers) | `engineering/desktop-engineer` | desktop-security-auditor | desktop | desktop, privacy-compliance |
| Background work (services, daemons, LaunchAgents, systemd) | `engineering/desktop-engineer` | reliability-engineer | observability | incident-response |
| Media / files / devices (FFmpeg, screen capture, printers, USB/HID) | `engineering/desktop-engineer` | — | desktop | desktop |
| Performance (startup, memory, IPC, leaks, long-session) | `quality/performance-engineer` | desktop-engineer | performance | performance |
| QA / tests | `quality/qa-engineer` + `quality/test-automation-engineer` | — | testing | qa |
| E2E (Playwright-for-Electron / WebDriver / FlaUI / Qt Test) | `engineering/playwright-e2e-engineer` (Electron) / `engineering/desktop-engineer` (native) | qa-engineer | testing | qa |
| Build / packaging / signing / notarization / installers | `engineering/desktop-release-engineer` | devops-engineer | devops | desktop-distribution, release-rollback |
| Auto-update (Sparkle/Squirrel/electron-updater/Tauri updater) | `engineering/desktop-release-engineer` | desktop-security-auditor | devops | desktop-distribution |
| CI/CD (mac/win/linux runners, matrix, signed builds) | `engineering/devops-engineer` | desktop-release-engineer | devops | devops, release-rollback |
| Observability (crash: Crashpad/Breakpad/Sentry, diagnostics) | `quality/reliability-engineer` | desktop-engineer | observability | observability, incident-response |
| Privacy / compliance (telemetry consent, data export/delete) | `quality/privacy-compliance-auditor` | desktop-engineer | security | privacy-compliance |
| Local AI (Ollama/llama.cpp/MLX/ONNX/Core ML, offline mode) | `engineering/ai-ml-engineer` | desktop-engineer | ai-ml | ai-ml, security |
| Production readiness | `quality/production-readiness-auditor` | all gate owners | production-readiness | desktop-production, desktop-distribution, production |
| Bug fix / refactor | `engineering/{bug-fix,refactoring}-specialist` | the framework specialist | testing, architecture | qa |

## Platform caveats (always note in output)
- **macOS:** code signing (Developer ID) + **notarization** + Gatekeeper; hardened runtime + entitlements; TCC permissions (screen recording, accessibility, automation) need usage strings + user grant; Sparkle for direct dist, MAS for store; universal binary (arm64+x86_64).
- **Windows:** Authenticode signing (EV cert builds SmartScreen reputation fastest); MSIX (store/modern) vs MSI/NSIS/Inno (direct); per-user vs per-machine install; registry + Credential Manager; x64/ARM64.
- **Linux:** no single signing standard — integrity via repo/Flatpak/Snap; AppImage (portable) vs Flatpak (sandboxed, Flathub) vs Snap vs deb/rpm; desktop entries + icons; X11 vs Wayland; glibc vs musl; multi-distro testing.

## High-value external skills (via /find-skills)
- **`tauri-v2`** (~5.6k installs) — prefer for Tauri idioms if installed. **`frontend-design`** for the renderer UI in Electron/Tauri. Community Electron/signing skills are thin → use our specialists.

## Verification loops (fix-and-verify / hardening / packaging / auto-update / release)
change → prove (build the app on the target OS; run unit + the relevant UI/E2E tests for real; never fabricate)
→ re-audit the changed area with its checklist → risk review (crash / corrupt-update / signing / regression risk; reversible?)
→ final summary with **platform caveats**. `core/code-reviewer` checks diffs.

## Commands
`/desktop-audit <scope> [--mode]`, `/desktop-readiness` (packaging + signing + auto-update gate), plus
universal `/route`, `/audit-security`, `/audit-performance`, `/fix-bugs`, `/refactor-safely`, `/create-tests`,
`/prepare-launch`, `/commit-ready`.

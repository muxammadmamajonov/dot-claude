---
name: desktop
description: >
  Activate when building, extending, or packaging a desktop application —
  Electron, Tauri, .NET WinForms/WPF/MAUI, Qt, JavaFX, or native Swift/AppKit
  / Kotlin/Compose Desktop. Covers windowing, IPC, native OS integration,
  packaging, code signing, and auto-update. Do NOT activate for CLIs
  (use .claude/skills/cli/SKILL.md) or Electron apps whose primary concern is
  web rendering without native integration.
---

# Desktop Application Skill

## When to use

- Starting a new desktop application on Windows, macOS, Linux, or cross-platform
- Adding native OS integration: system tray, file associations, OS notifications, clipboard, auto-launch
- Packaging and signing for distribution (MSI/EXE, DMG/PKG, AppImage/DEB/RPM, MSIX)
- Implementing auto-update with staged rollouts
- Diagnosing memory leaks, main-thread blocking, or IPC latency

---

## Workflow

1. **Classify the project** — Read `docs/specs/product.md` and `.claude/stack-matrix/` to confirm target OS(es), distribution channel (direct download, Microsoft Store, Mac App Store, homebrew cask, Flathub), and the tech stack. Confirm whether web-tech (Electron/Tauri) or native UI is required.

2. **Choose framework**
   | Requirement | Recommended |
   |---|---|
   | Ship fast, existing web team | Tauri (Rust backend, web frontend, ~3 MB binary) or Electron |
   | Maximum bundle size constraint (<5 MB) | Tauri |
   | Deep Windows shell integration | .NET WinForms / WPF / WinUI 3 |
   | Deep macOS integration (SwiftUI, Handoff, Continuity) | Swift + AppKit/SwiftUI |
   | Cross-platform with native look | Qt 6 or .NET MAUI |
   | JVM ecosystem | Compose Desktop / JavaFX |

3. **Design the process model** — For multi-process frameworks (Electron, Tauri):
   - Main / backend process: owns system resources, file I/O, native APIs
   - Renderer / frontend: UI only — no direct filesystem or native calls
   - Define the IPC contract (channel names, payload schemas) before coding. Validate payloads with Zod or equivalent on both sides.

4. **Implement IPC securely** — Electron: use `contextBridge.exposeInMainWorld` to whitelist exactly the functions the renderer needs; never enable `nodeIntegration: true` in renderer. Tauri: declare commands in `tauri.conf.json` allow-list.

5. **Handle window management** — Create a `WindowManager` service that:
   - Persists last window size/position to app prefs and restores on launch
   - Handles multiple windows gracefully (reference by label/ID, not index)
   - Respects OS conventions: cmd+W on macOS hides, does not quit; Alt+F4 on Windows quits

6. **Integrate native OS features as needed**
   - System tray: always provide a quit action; optionally show app status
   - File associations: register in manifest/plist; handle `open-file` events at startup and while running
   - Deep links: register custom URL scheme; handle both cold-start and already-running cases
   - Auto-launch at login: provide an explicit toggle in settings; never enable silently

7. **Persist user data** — Use OS-standard locations:
   - Config: `app.getPath('userData')` (Electron) or platform-standard (`~/Library/Application Support`, `%APPDATA%`, `~/.config`)
   - Documents: only with user's explicit consent via file picker
   - Never write to the application bundle itself (breaks signed apps)

8. **Implement auto-update**
   - Electron: `electron-updater` with a private S3/GCS bucket or GitHub Releases
   - Tauri: built-in updater with signed update manifests
   - Test the update flow on every OS before each release. Provide a manual "Check for updates" menu item.

9. **Package and sign**
   - macOS: codesign with Developer ID + notarise with `xcrun notarytool`; staple the ticket
   - Windows: sign with EV or OV code-signing certificate; avoid SmartScreen warnings
   - Linux: provide AppImage + distro package (DEB/RPM) or Flatpak; AppImage is most universal
   Never ship an unsigned binary for production; users will face security warnings.

10. **Write tests**
    - Unit: pure logic, IPC command handlers, data persistence
    - Integration: Playwright Desktop (Electron), Tauri's WebDriver, or OS-native test frameworks
    Reference `.claude/checklists/qa.md`.

11. **Run production-readiness checklist** — Reference `.claude/checklists/production.md`. Confirm: crash reporter integrated (Sentry, BugSnag, or native), no dev-mode flags in production build, update channel set to stable.

---

## Standards

**Do**
- Validate all data crossing the IPC boundary as if it were an untrusted network call.
- Keep the main/backend process lean; push heavy computation to worker threads or child processes.
- Use OS native dialogs (`dialog.showOpenDialog`, `NSSavePanel`) for file operations — never custom HTML pickers for security-sensitive paths.
- Include `Content-Security-Policy` in the `<meta>` tag of every HTML page loaded in Electron (restrict `default-src`, ban `unsafe-eval`).
- Ship a universal macOS binary (arm64 + x86_64) unless the target hardware is known.

**Do not**
- Enable `nodeIntegration: true` or `contextIsolation: false` in Electron renderer processes.
- Load remote URLs in Electron's main window — disable navigation with `will-navigate` handler.
- Write sensitive data (tokens, keys) to plain text files; use the OS credential store (Keychain, Windows Credential Manager, libsecret).
- Hard-code update server URLs; configure them via environment/build config so channels (stable, beta) can differ.
- Block the UI thread with synchronous disk reads; use async APIs.

---

## Common mistakes to avoid

- **No quit shortcut on macOS** — On macOS the Dock icon click should re-open the window if hidden, not launch a new instance; implement `activate` event handler.
- **Missing `app.requestSingleInstanceLock()`** in Electron — users can launch multiple instances and corrupt shared state.
- **IPC payload injection** — If any part of an IPC payload is constructed from user-supplied strings, sanitise before use; arbitrary `eval` or `shell.openExternal` can be triggered.
- **Forgetting Windows-specific paths** — `path.join` is safe; string concatenation with `/` breaks on Windows.
- **Not handling offline startup** — If the app phones home on startup and the network is down, it should still open gracefully.
- **Bundling dev dependencies** — Electron-builder `files` config must exclude `node_modules` dev deps; bloat adds seconds to install.
- **Skipping code signing during development** — differences between signed and unsigned code can mask permission bugs discovered only at signing time.

---

## Output format

A production-ready desktop project should include:

```
/
├── src/
│   ├── main/           # Main / backend process (IPC handlers, native API)
│   ├── renderer/       # UI (React, Vue, Svelte, or native UI code)
│   ├── shared/         # Types, IPC channel constants shared by both processes
│   └── preload/        # Electron preload scripts (context bridge)
├── resources/          # App icons per OS (icns, ico, png)
├── build/              # Packaging config (electron-builder.yml, tauri.conf.json)
├── tests/
├── .env.example
└── README.md           # Build, sign, and distribute steps per OS
```

---

## Related checklists

- `.claude/checklists/security.md`
- `.claude/checklists/performance.md`
- `.claude/checklists/qa.md`
- `.claude/checklists/production.md`

## Related agents

- `.claude/agents/core/orchestrator.md`
- `.claude/agents/quality/security-auditor.md`

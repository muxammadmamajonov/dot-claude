# Desktop Production-Readiness Checklist

The desktop gate before shipping a production app (Electron, Tauri, Flutter Desktop, Qt/GTK, .NET,
or native macOS/Windows/Linux). Pairs with `.claude/checklists/production.md` (universal) and
`.claude/checklists/desktop-distribution.md` (signing/packaging/auto-update). Severity: **P0** blocker ·
**P1** important · **P2** hardening · **P3** backlog. Note the per-OS caveats inline.

## P0 — Blockers (must pass before release)

- [ ] **Code-signed & (macOS) notarized** release build on every target OS; the installer/bundle launches without OS security warnings. (mac: Developer ID + notarization + hardened runtime; win: Authenticode; linux: integrity via repo/Flatpak/Snap.) — see `desktop-distribution.md`.
- [ ] **Auto-update is signed and integrity-checked**: updates are served over HTTPS and cryptographically verified before apply (Sparkle EdDSA / Squirrel / electron-updater signature / Tauri updater pubkey). An unsigned/unverified update path is a P0 RCE vector.
- [ ] **Secrets not in the bundle**: no API keys/tokens in the app package or repo; sensitive APIs go through a backend proxy. (Desktop bundles are trivially unpacked.)
- [ ] **Secrets stored in the OS secure store**: tokens/credentials in **Keychain** (mac) / **Credential Manager** (win) / **libsecret/KWallet** (linux) — never plaintext files or unencrypted config.
- [ ] **Electron/Tauri shell hardened (if web-shell):** Electron `contextIsolation: true`, `sandbox: true`, `nodeIntegration: false`, validated `preload` IPC, a CSP, no loading of remote/untrusted content into a privileged renderer; Tauri capabilities/allowlist scoped to the minimum, commands validate input. A misconfigured shell = full local compromise.
- [ ] **TLS validation intact** (no disabled cert checks); cert pinning where the threat model warrants.
- [ ] **No data-loss paths**: document/state writes are crash-safe (atomic write + fsync / temp-then-rename); a crash mid-save does not corrupt user data; migrations have a backup/rollback.
- [ ] **Release build runs on each target OS** (not just the dev machine); no debug/devtools left enabled in production; no sensitive data logged.
- [ ] **Automated tests pass** for critical flows (launch, core action, save/load, update check) — real results, not assumed.
- [ ] **Rollback path**: previous version reinstallable; a bad update can be halted and superseded; channels (stable/beta) separated.

## P1 — Important (soon)

- [ ] **Startup performance**: cold start within target; no main/UI-thread blocking on launch; heavy work off the UI thread (workers/threads/async).
- [ ] **Memory & long-session stability**: no unbounded growth over a long session; leaks profiled (Instruments / WPA / Valgrind / heaptrack / DevTools); idle resource use is low.
- [ ] **Offline / local-first behavior**: app works without network where designed to; offline queue + retry; clear sync/conflict handling for local-to-cloud data.
- [ ] **Window & display correctness**: multi-monitor, high-DPI/Retina, display hot-plug, and window-state restore all behave; safe on the smallest supported resolution.
- [ ] **OS integration correct**: tray/menu-bar, global shortcuts, startup-at-login, protocol handlers, file associations, and native notifications work and are removable/uninstall-clean.
- [ ] **Permissions UX**: each OS permission (mac TCC: screen recording/accessibility/automation; camera/mic) is requested with rationale at point of use and degrades gracefully when denied.
- [ ] **Accessibility**: keyboard-only navigation, visible focus, screen-reader labels (VoiceOver/Narrator/Orca), high-contrast and dynamic-text honored on key screens.
- [ ] **Crash reporting + diagnostics** wired (Crashpad/Breakpad/Sentry) with symbol upload and release tagging; a user-exportable diagnostics bundle (logs with rotation, no secrets).
- [ ] **Installer is clean**: per-user vs per-machine intentional; uninstall removes app + agents/services and leaves user data per policy; upgrade-over-install tested from the previous version.

## P2 — Hardening

- [ ] Background services/daemons (Windows Service / LaunchAgent / systemd) are least-privilege, crash-restart-safe, and observable; jobs persist across crashes.
- [ ] Supply-chain: dependency CVE scan clean of high/critical; lockfile committed; native deps pinned; plugin loading is sandboxed/validated.
- [ ] Telemetry is consented and privacy-preserving; PII handling + data retention documented; user data export/delete supported.
- [ ] Delta updates where artifact size warrants; update applies atomically and rolls back on failure.
- [ ] Enterprise: policy/config support (managed prefs / registry / config profiles) and MDM-deployable build where the audience needs it.

## P3 — Post-launch / backlog (track; never blocks)

- [ ] Cross-distro Linux matrix (glibc/musl, X11/Wayland, GNOME/KDE) in CI; installer VM tests per OS.
- [ ] Visual-regression + accessibility checks in CI; long-session soak test.
- [ ] GPU/battery profiling under real workloads; app/installer size budget review.
- [ ] Local-AI fallback (online↔offline) with token/cost controls if AI features exist.

## How to use

**When:** before a production release / installer / store submission, and at the readiness review.
**Who:** `production-readiness-auditor` leads; `desktop-security-auditor`, `performance-engineer`,
`accessibility-auditor`, `desktop-release-engineer`, and the framework engineer (`electron-engineer` /
`tauri-engineer` / `desktop-engineer`) own their sections. **Command:** `/desktop-audit <scope> --mode
production-hardening` exercises sections; `/desktop-readiness` pairs this with
`.claude/checklists/desktop-distribution.md`. P0 blocks release; P1 → tracked issues; P2–P3 → backlog.
Mark passed only with real evidence (a signed build, a `codesign`/`signtool` verify, a profiler trace,
a test command + output) — never an assumption. Always record the per-OS caveats.

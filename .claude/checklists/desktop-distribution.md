# Desktop Distribution Checklist — signing, packaging & auto-update (macOS · Windows · Linux)

The ship gate for getting a desktop app safely onto users' machines and keeping it updated. Covers
**macOS** signing/notarization, **Windows** signing/installers, **Linux** packaging, and **auto-update**
for all three. Pairs with `.claude/checklists/desktop-production.md` (app quality). Severity: **P0**
blocker · **P1** important · **P2** hardening · **P3** backlog. Skip the OS / channel you don't ship.

## macOS — signing, notarization, distribution

### P0
- [ ] App + all nested binaries/helpers signed with a **Developer ID Application** cert; **hardened runtime** enabled; only the entitlements actually used are declared.
- [ ] App **notarized** by Apple and the ticket **stapled** (`xcrun notarytool` + `stapler`); a fresh download opens without a Gatekeeper block. Verify: `spctl -a -vvv App.app` and `codesign -dv --verbose=4`.
- [ ] Usage-description strings present for every sensitive API (camera, mic, screen recording, accessibility, automation, location); the app requests them at point of use.
- [ ] Universal binary (arm64 + x86_64) or a clear per-arch story.
### P1
- [ ] Distribution channel decided: **Sparkle** (direct DMG/PKG, EdDSA-signed appcast) or **Mac App Store** (sandbox + MAS provisioning). DMG/PKG itself signed.
- [ ] Versioning: `CFBundleShortVersionString` + `CFBundleVersion` incremented; LSMinimumSystemVersion set.
### P2
- [ ] Signing identity & notarization run in CI (App Store Connect API key in secret store, never committed); Developer ID private key backed up.

## Windows — signing, installers, distribution

### P0
- [ ] Executables + installer **Authenticode-signed** (timestamped, so signatures survive cert expiry). Verify: `signtool verify /pa /v App.exe`.
- [ ] Installer format chosen and tested: **MSIX** (modern/store) or **MSI / NSIS / Inno** (direct); per-user vs per-machine install is intentional and works without unexpected UAC.
- [ ] No unsigned post-install code download/execute; auto-update binaries are signed (see Auto-update P0).
### P1
- [ ] **SmartScreen** reputation plan: EV cert (instant reputation) or accept ramp-up time on a standard cert; document expected first-run warnings.
- [ ] Clean install / upgrade / uninstall tested (registry + Credential Manager entries removed; user data per policy); x64 and ARM64 as targeted.
### P2
- [ ] Signing in CI with the cert in a secret store / HSM (never committed); store submission (Microsoft Store) or package managers (winget/Chocolatey/Scoop) configured if used.

## Linux — packaging & distribution

### P0
- [ ] At least one first-class format built and launch-tested: **AppImage** (portable), **Flatpak** (sandboxed, Flathub), **Snap**, or **deb/rpm**; integrity comes from the channel (repo signing / Flatpak / Snap), since Linux has no single code-signing standard.
- [ ] Valid `.desktop` entry + icons; app appears and launches from the app menu; runs on the declared minimum distro/glibc.
### P1
- [ ] Wayland **and** X11 behavior verified; tray/StatusNotifier works on target desktops (GNOME/KDE); Flatpak/Snap permission portals requested correctly.
- [ ] Repo publishing (apt/yum) or Flathub/Snap Store metadata complete; package version + changelog set.
### P2
- [ ] Multi-distro CI matrix; glibc vs musl story; reproducible builds where feasible.

## Auto-update (all platforms)

### P0
- [ ] Updates delivered over **HTTPS** and **cryptographically verified** before apply — Sparkle EdDSA / Squirrel / electron-updater code-signature / **Tauri updater pubkey**. An unsigned or unverified update channel is a remote-code-execution hole — treat as P0.
- [ ] Update apply is **atomic** with rollback on failure; a failed/corrupt update never bricks the app.
- [ ] The update **private/signing key is in a secret store**, never in the repo or the app bundle; losing it (or leaking it) is catastrophic — back it up securely.
### P1
- [ ] **Channels** (stable/beta/alpha) separated; **staged rollout** + the ability to **halt** a bad release; users can defer/postpone where appropriate.
- [ ] Update **failure telemetry** (with consent) so a broken update is detected fast; minimum-version / forced-update path for security fixes.
### P2
- [ ] **Delta updates** where artifact size warrants; signed appcast/manifest; update integrity re-checked after download and before swap.

## How to use

**When:** before every installer build / store submission / update push, and at the release review.
**Who:** `desktop-release-engineer` leads; `desktop-security-auditor` owns the signing/auto-update-integrity
items; `production-readiness-auditor` confirms app quality via `.claude/checklists/desktop-production.md`.
**Command:** `/desktop-readiness` runs this checklist and emits a go/no-go; `/desktop-audit packaging`
or `/desktop-audit update` exercises a section. P0 blocks distribution; P1 → fix before/just-after
launch; P2–P3 → backlog. Verify against **current** Apple/Microsoft/Flathub/Snap requirements (they
change) and mark passed only with real evidence (a `codesign`/`spctl`/`signtool` verify, a successful
notarization, a test install on a clean VM) — never an assumption.

# Desktop Checklist
Gate for desktop application projects covering packaging, code signing, auto-update, and OS permissions. Severity tiers: P0=blocker, P1=important (fix shortly after launch), P2=hardening, P3=post-launch/backlog.

## P0 — Blockers (must pass before any public distribution)

- [ ] **Code signing complete**: Binaries and installers are signed with a valid, non-expired certificate from a trusted CA (Apple Developer ID, Microsoft Authenticode, or equivalent); unsigned builds are not distributed to end users.
- [ ] **Installer/package integrity**: The installer (`.exe`, `.msi`, `.dmg`, `.pkg`, `.deb`, `.AppImage`, etc.) can be installed cleanly on a fresh OS image without existing dependencies or developer tooling installed.
- [ ] **Application starts on minimum-spec OS**: App launches without error on the oldest supported OS version for each target platform (e.g., Windows 10 22H2, macOS 13 Ventura, Ubuntu 22.04 LTS).
- [ ] **No hardcoded dev paths**: Build artifacts contain no references to build-machine paths, developer home directories, or `node_modules`/virtualenv paths that will fail on end-user machines.
- [ ] **Dangerous permissions scoped correctly**: The app requests only the OS permissions it actually uses (camera, microphone, location, contacts, accessibility, full-disk access); requesting overly broad permissions will be rejected by notarisation/store review.
- [ ] **Notarisation / store submission passes**: macOS binaries pass `spctl --assess` (Gatekeeper) after notarisation; Windows MSIX passes Store certification; Linux Flatpak/Snap passes submission validation where applicable.
- [ ] **Crash on launch absent**: App does not crash on launch due to missing native dependencies (e.g., VC++ Redistributable, WebView2, .NET runtime) — either they are bundled or the installer detects and installs prerequisites.
- [ ] **Auto-update mechanism present and tested**: At minimum one update path exists (e.g., Squirrel, Sparkle, NSIS updater, built-in updater); update from the previous release version to the current build has been tested end-to-end without data loss.

## P1 — Important (fix before wide distribution or shortly after)

- [ ] **Update signature verification**: Auto-update downloads are verified against a signed manifest or checksum before applying; the app does not silently execute unsigned update payloads.
- [ ] **First-run experience works from installer**: On a clean install the app opens, completes any first-run setup (license agreement, initial config), and reaches a usable state without requiring manual steps not documented to the user.
- [ ] **Uninstaller is clean**: Uninstalling the app removes the application, its data directory (with a user prompt if data will be lost), registry keys, and startup entries; no orphaned files remain in system directories.
- [ ] **Deep-link / URI scheme registered correctly**: If the app registers a custom URI scheme (`myapp://`), it is registered per-user or per-machine as appropriate; conflicts with other apps are documented.
- [ ] **Accessibility (a11y) basics pass**: App UI is navigable via keyboard alone; screen reader (VoiceOver / NVDA / Orca) can read primary interactive elements; colour contrast meets WCAG 2.1 AA.
- [ ] **Per-user data stored in correct OS location**: User config and data are stored in the OS-standard path (`%APPDATA%`, `~/Library/Application Support`, `~/.config`), not beside the application binary.
- [ ] **Log files do not grow unbounded**: Application logs are rotated or capped; default log level in release builds does not write sensitive user data to disk.
- [ ] **Crash reporter active and anonymised**: A crash reporting integration (e.g., Sentry, Crashpad, PLCrashReporter) is active in release builds; PII in crash reports is scrubbed or anonymised per privacy policy.
- [ ] **Multi-instance behaviour defined**: The app either prevents a second instance from launching (and focuses the existing window) or explicitly supports multiple instances; it does not silently corrupt shared state when run twice.

## P2 — Hardening / nice-to-have

- [ ] **Startup time acceptable**: Cold-start time on minimum-spec hardware is under the target threshold (e.g., < 3 s to interactive for a productivity tool); measured on a spinning disk to simulate real-world conditions.
- [ ] **System tray / menu bar integration tested**: If the app lives in the system tray or menu bar, all tray actions work correctly after system reboot and session restore.
- [ ] **High-DPI / Retina rendering correct**: UI renders without blurriness or layout breakage at 125 %, 150 %, 200 %, and 250 % display scaling on Windows; and on Retina (2× HiDPI) on macOS.
- [ ] **Dark mode support**: App respects the OS-level dark/light mode preference and switches without restart; custom colours are not hardcoded to light-mode values.
- [ ] **Delta updates available**: Update patches are smaller than a full re-download; measured and confirmed for the release-to-release patch size.
- [ ] **Portable/offline build option documented**: A portable build (no installer, runs from any directory) is available or documented as unsupported; offline install (bundled runtimes) is provided for enterprise customers.
- [ ] **Dependency vulnerability scan**: Third-party native libraries and bundled runtimes are scanned for known CVEs; findings are tracked in `.claude/checklists/security.md`.
- [ ] **Rollback path tested**: If the auto-update fails partway through, the app rolls back to the previous working version rather than leaving the install in a broken state.

## P3 — Post-launch / backlog (track and revisit after launch; never blocks shipping)

- [ ] **OS-native feature integration reviewed**: Platform-specific capabilities added post-launch (e.g., Windows Jump Lists, macOS Continuity/Handoff, Linux D-Bus notifications) are evaluated against the user-base OS share and prioritized on a roadmap.
- [ ] **Automatic crash-minidump analysis pipeline**: Crashpad/Breakpad minidumps are symbolicated and clustered automatically (e.g., via Sentry or Socorro); the top-5 crash signatures by user-impact are assigned and tracked each release cycle.
- [ ] **Telemetry opt-in usage analytics**: Aggregate, anonymised feature-usage telemetry (screens visited, commands invoked, session duration) is collected with explicit user consent to guide post-launch UX improvements.
- [ ] **Enterprise deployment packaging**: An MSI/MSIX with Group Policy ADMX templates (Windows) or a MDM-deployable PKG with configuration profile support (macOS) is produced and documented for IT-managed fleet deployments.
- [ ] **Accessibility conformance re-audit with assistive technology**: Full keyboard-only and screen-reader (NVDA, VoiceOver, Orca) walkthrough is conducted against the shipped UI after each major feature addition; findings are logged against WCAG 2.2 AA criteria.
- [ ] **Reduced-motion and high-contrast mode support**: All animations respect the OS `prefers-reduced-motion` / `Accessibility > Reduce Motion` setting; a Windows high-contrast theme is tested and passes without broken layouts or invisible interactive elements.

## How to use

**When**: Run this checklist when a release candidate build is produced, before submitting to any app store or distributing a signed installer externally.

**Who**: Build/release engineer owns P0 and signs off the installer. QA lead validates P1 items on at least two target OS versions. Tech lead reviews P2 before GA.

**Command / agent**: Ask the agent `"Run .claude/checklists/desktop.md against build v<version>"` — it will check signing status, inspect installer contents for hardcoded paths, validate the auto-update manifest, and enumerate OS permissions declared in the app manifest. Manual items (crash-reporter test, multi-instance, dark-mode visual) are listed for human sign-off. Cross-reference `.claude/checklists/security.md` for dependency CVE tracking.

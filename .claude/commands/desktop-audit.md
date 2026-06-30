---
description: Mode- and scope-driven desktop audit for macOS/Windows/Linux. Detects the framework (Electron, Tauri, Flutter Desktop, Qt/GTK, .NET desktop, native macOS/Windows/Linux) and routes to the right specialists for a chosen area — returning ranked, evidence-backed findings with platform caveats, never fabricated results. Use for "audit my desktop app", "Electron/Tauri review", "is this signed/notarized/packaged right", security/perf/packaging/auto-update review.
argument-hint: <scope: electron|tauri|security|performance|storage|networking|permissions|background|media|accessibility|packaging|update|full> [--mode audit-only|fix-and-verify|production-hardening|desktop-packaging-readiness|auto-update-readiness]
---

# /desktop-audit

## Purpose
One token-efficient entry point for auditing a desktop app. It detects the framework + target OS(es),
activates only the specialists the chosen **scope** needs (see
`.claude/orchestration/desktop-routing-matrix.md`), runs them against the desktop checklists, and returns
a single ranked report with **platform caveats** — serving read-only review, fix-and-verify, hardening,
packaging-readiness, or auto-update-readiness via the **mode**.

## When to use
- "Audit my desktop app" / "review the Electron / Tauri / Qt / .NET code".
- Targeted: shell security (Electron contextIsolation/Tauri allowlist), secure local storage, IPC,
  permissions/OS integration, background services, performance/leaks, packaging, auto-update.
- Before a release/installer/store submission → use `--mode desktop-packaging-readiness` or `/desktop-readiness`.

## Workflow
1. **Map & detect framework + OS targets.** `.claude/agents/core/codebase-mapper.md` → `docs/state/codebase-map.md`; classify Electron/Tauri/Flutter-desktop/.NET/native via the routing matrix's detection table; note which of macOS/Windows/Linux are targeted.
2. **Resolve scope → specialists** (routing matrix). Examples:
   - `electron` → `engineering/electron-engineer` + `quality/desktop-security-auditor` (contextIsolation, sandbox, nodeIntegration, preload, IPC, CSP, remote content).
   - `tauri` → `engineering/tauri-engineer` + `quality/desktop-security-auditor` (capabilities/allowlist scope, command permission, IPC, WebView).
   - `security` → `quality/desktop-security-auditor` (+ auth-permission-reviewer); secure storage (Keychain/Credential Manager/libsecret), encrypted DB, TLS, signing, supply chain, secure auto-update.
   - `storage` → desktop-engineer + database-architect; SQLite/Core Data, encryption, migrations, backup/restore, app-data dirs, conflict resolution.
   - `networking` → desktop-engineer + api-architect; proxy/corporate network, offline queue, retry/timeout/cancel, resumable up/download, sync.
   - `permissions` → desktop-engineer + desktop-security-auditor; FS/camera/mic/screen-record/accessibility/automation, tray, autostart, protocol handlers, file associations.
   - `background` → desktop-engineer + reliability-engineer; services/daemons (Windows Services / LaunchAgents / systemd), crash-safe job persistence.
   - `media` → desktop-engineer; file import/export, drag-drop, clipboard, FFmpeg, screen/webcam capture, printers, USB/HID.
   - `performance` → performance-engineer + desktop-engineer; startup, memory/CPU/GPU, IPC overhead, leaks, long-session stability.
   - `accessibility` → accessibility-auditor; VoiceOver/Narrator/Orca, keyboard-only, focus order, high-contrast, dynamic text.
   - `packaging`/`update` → `engineering/desktop-release-engineer`; signing/notarization/installers and Sparkle/Squirrel/electron-updater/Tauri updater.
   - `full` → run framework + security + performance + packaging scopes **concurrently**, then dedupe.
3. **Run gates** read-only against the checklist; mark each item pass/fail with `file:line` evidence. Run real commands (build, test, `electron-builder`, `tauri build`, `codesign -dv`, `signtool verify`) or mark "unverified" — never fabricate.
4. **Apply mode.** `audit-only` stops. `fix-and-verify` fixes P0/P1 then rebuilds + reruns tests and re-audits. `production-hardening`/`desktop-packaging-readiness`/`auto-update-readiness` drive `.claude/checklists/desktop-production.md` + `.claude/checklists/desktop-distribution.md`.
5. **Reconcile, rank P0→P3, risk review, summary** (crash / corrupt-update / signing-failure / regression risk; reversibility) — always with **per-OS caveats**.

## Agents used
`core/codebase-mapper`, `core/orchestrator`, and the scope's specialists: `engineering/{electron-engineer,tauri-engineer,desktop-engineer,desktop-release-engineer,playwright-e2e-engineer}`, `quality/{desktop-security-auditor,performance-engineer,accessibility-auditor,qa-engineer,reliability-engineer}`, `design/ui-ux-designer`. `core/code-reviewer` verifies diffs in fix-and-verify.

## Skills used
`.claude/skills/desktop/SKILL.md`, plus scope: `security`, `performance`, `testing`, `data-modeling`, `devops`, `ui-ux-design`. Prefer the installed `tauri-v2` skill for Tauri idioms; `frontend-design` for the renderer UI.

## Expected outputs
| Output | Path |
|---|---|
| Repo map (framework + OS targets) | `docs/state/codebase-map.md` |
| Audit report (ranked P0–P3, per-OS caveats) | `docs/reports/desktop-audit-<scope>-<date>.md` |
| Fixes (fix-and-verify) | code diff + test/build results |
| Risk records | `docs/decisions/` |

## Stop conditions
- No desktop project detected → suggest `/route` (may be web → `/web-audit`).
- Cross-OS build can't run on this host (e.g. no Windows runner for an MSI) → report which, mark unverified, never fake a pass; recommend a CI matrix.
- A P0 (Electron `nodeIntegration:true`+`contextIsolation:false` with remote content, unsigned auto-update, plaintext token storage) → surface immediately.

## Final report format
```
## /desktop-audit — <scope> (<mode>)
Framework: <Electron|Tauri|Flutter|Qt|.NET|native>  |  OS targets: <mac|win|linux>  |  Mode: <…>
### Findings (N): P0 <n> · P1 <n> · P2 <n> · P3 <n>
- [P0] <title> — <file:line> — evidence: <…> — fix: <…>  (platform: <mac/win/linux/all>)
### Fixed & verified (fix-and-verify): <list + how proven (command + result)>
### Risk review: <crash / corrupt-update / signing ; reversibility>
### Per-OS caveats: <mac / win / linux notes>
### Verdict: <ship / fix-first / blocked>  ·  Next: <command, e.g. /desktop-readiness>
```

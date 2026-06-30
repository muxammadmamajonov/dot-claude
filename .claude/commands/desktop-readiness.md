---
description: Desktop ship gate for macOS/Windows/Linux — runs the desktop-production checklist plus the desktop-distribution checklist (signing, notarization, packaging, auto-update) and returns a go/no-go with P0 blockers, per-OS caveats, and evidence, never a cosmetic sweep. Use before building an installer, submitting to a store, or pushing an auto-update, or when asked "is this desktop app ready to ship / signed / notarized / packaged / safe to auto-update".
argument-hint: [--os mac|win|linux|all] [--mode audit-only|production-hardening]  (defaults: all, audit-only)
---

# /desktop-readiness

## Purpose
The single ship gate for a desktop app. It verifies app quality (`.claude/checklists/desktop-production.md`)
and distribution readiness — signing, notarization, installers, and **auto-update integrity**
(`.claude/checklists/desktop-distribution.md`) — then issues **go / fix-first / no-go** with real evidence
and per-OS caveats. It catches the desktop-specific killers: an unsigned/unverified auto-update channel,
plaintext secret storage, and a misconfigured Electron/Tauri shell.

## When to use
- Before building/shipping an installer (DMG/PKG, MSI/MSIX/NSIS, AppImage/Flatpak/Snap/deb/rpm).
- Before a store submission (Mac App Store / Microsoft Store / Flathub / Snap Store).
- Before pushing an **auto-update**.
- When asked "is this desktop app ready to ship / signed / notarized / safe to update?"

## Workflow
1. **Map & detect** framework + OS targets: `.claude/agents/core/codebase-mapper.md`; confirm it's a desktop app and which of `--os` apply.
2. **Run the distribution gate**: walk `.claude/checklists/desktop-distribution.md` for the selected OS(es) + auto-update. Each item marked pass/fail with **evidence** — `codesign -dv` / `spctl -a -vvv` (mac), `signtool verify` (win), a clean-VM install (linux), the update signature config. Never mark passed by assumption.
3. **Run the quality gate**: `.claude/checklists/desktop-production.md` via its owners (`desktop-security-auditor`, `performance-engineer`, `accessibility-auditor`, the framework engineer). Run concurrently.
4. **Reconcile** into one ranked list (P0→P3); dedupe; attach per-OS caveats.
5. **Apply mode**: `audit-only` reports; `production-hardening` fixes P0/P1, rebuilds + re-verifies (re-sign/re-notarize as needed), and records deferred gaps as risks in `docs/decisions/`.
6. **Verdict + risk review**: go / fix-first / no-go, with the top ship risks (unsigned update, signing failure, data-loss path) and the rollback/halt plan called out.

## Agents used
`core/codebase-mapper`, `engineering/desktop-release-engineer` (lead), `quality/production-readiness-auditor`, `quality/desktop-security-auditor`, `quality/{performance-engineer,accessibility-auditor}`, and the framework engineer (`electron-engineer`/`tauri-engineer`/`desktop-engineer`). `core/code-reviewer` checks any hardening diff.

## Skills used
`.claude/skills/production-readiness/SKILL.md`, `.claude/skills/desktop/SKILL.md`, `.claude/skills/security/SKILL.md`, `.claude/skills/devops/SKILL.md`.

## Expected outputs
| Output | Path |
|---|---|
| Readiness report (ranked, per-OS, with evidence) | `docs/reports/desktop-readiness-<date>.md` |
| Go/no-go verdict + top ship risks | top of the report |
| Hardening fixes (hardening mode) | code/config diff + re-verified items |
| Deferred-risk records | `docs/decisions/` |

## Stop conditions
- Not a desktop app → suggest `/web-readiness` or `/store-readiness` (mobile) or `/audit-production`.
- A target OS can't be built/verified on this host (e.g. notarization needs macOS; MSI needs Windows) → mark "unverified" = not passed; recommend a CI matrix; never fabricate.
- A P0 (unsigned/unverified auto-update, unsigned release, plaintext secrets, `nodeIntegration` + remote content) → verdict **no-go**; surface immediately.

## Final report format
```
## /desktop-readiness — <verdict: GO | FIX-FIRST | NO-GO>   OS: <mac|win|linux|all>
Framework: <…>  |  Mode: <…>  |  Date: <…>
### Ship blockers (P0): <list with evidence>  ·  none → ✓
### Important (P1): <list>
### Hardening/backlog (P2–P3): <count, tracked>
### Hardened this run (hardening mode): <fixes + how verified (codesign/signtool/install)>
### Per-OS caveats: <mac / win / linux>
### Update channel: <signed? atomic? rollback? halt plan?>   Residual risk: <…>
### Verdict & next step: <build/submit/push / fix list / blocked>
```

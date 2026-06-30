---
description: App Store + Google Play submission gate. Runs the app-store-readiness checklist plus the mobile-production checklist and returns a go/no-go with P0 rejection-blockers, P1 follow-ups, and evidence — never a cosmetic checkmark sweep. Use before submitting to the App Store or Google Play, or when asked "is this store-ready / will Apple/Google reject this / ready to submit".
argument-hint: [--store apple|google|both] [--mode audit-only|production-hardening]  (defaults: both, audit-only)
---

# /store-readiness

## Purpose
The single submission gate for a mobile app. It verifies store policy + metadata + signing readiness
(`.claude/checklists/app-store-readiness.md`) and underlying app quality
(`.claude/checklists/mobile-production.md`), then issues **go / fix-first / no-go** backed by real
evidence — catching the common rejection causes (permissions, privacy disclosure, account deletion,
payment rails, signing) before Apple/Google do.

## When to use
- Before submitting to the App Store and/or Google Play.
- Before a major release that changes permissions, payments, data collection, or login.
- When asked "is this store-ready / will this get rejected / ready to ship to the stores?"

## Workflow
1. **Map & detect platform/targets**: `.claude/agents/core/codebase-mapper.md`; confirm it's a mobile app and which store(s) (`--store`).
2. **Run the store gate**: walk `.claude/checklists/app-store-readiness.md` for the selected store(s). Each item marked pass/fail with **evidence** — the privacy form, a successful archive/AAB upload, the signing config, the deep-link verification, demo creds. Never mark passed by assumption.
3. **Run the quality gate**: `.claude/checklists/mobile-production.md` via its owners (`mobile-security-auditor`, `performance-engineer`, `accessibility-auditor`, the platform `stack/mobile/*` engineer). Run concurrently.
4. **Reconcile** into one ranked list (P0→P3); dedupe.
5. **Apply mode**: `audit-only` reports; `production-hardening` fixes P0/P1, rebuilds, re-verifies, and records deferred gaps as risks in `docs/decisions/`.
6. **Verdict + risk review**: go / fix-first / no-go, with the top rejection risks and the rollout/halt plan called out.

## Agents used
`core/codebase-mapper`, `engineering/mobile-release-engineer` (lead), `quality/production-readiness-auditor`, `quality/privacy-compliance-auditor`, `quality/mobile-security-auditor`, `quality/{performance-engineer,accessibility-auditor}`, the platform `stack/mobile/*` engineer. `core/code-reviewer` checks any hardening diff.

## Skills used
`.claude/skills/production-readiness/SKILL.md`, `.claude/skills/mobile/SKILL.md`, `.claude/skills/security/SKILL.md`.

## Expected outputs
| Output | Path |
|---|---|
| Store-readiness report (ranked, with evidence) | `docs/reports/store-readiness-<date>.md` |
| Go/no-go verdict + top rejection risks | top of the report |
| Hardening fixes (hardening mode) | code/config diff + re-verified items |
| Deferred-risk records | `docs/decisions/` |

## Stop conditions
- Not a mobile app → suggest `/web-readiness` (PWA) or `/audit-production`.
- A P0 (truthful-disclosure mismatch, missing account deletion, wrong payment rail, broken signing) → verdict **no-go**; surface immediately.
- An item can't be verified (no store account / no build) → mark "unverified" = not passed; never fabricate. Always check the **current** Apple/Google policies (they change).

## Final report format
```
## /store-readiness — <verdict: GO | FIX-FIRST | NO-GO>   Store(s): <apple|google|both>
Platform: <…>  |  Mode: <…>  |  Date: <…>
### Rejection blockers (P0): <list with evidence>  ·  none → ✓
### Important (P1): <list>
### Hardening/backlog (P2–P3): <count, tracked>
### Hardened this run (hardening mode): <fixes + how verified>
### Rollout/halt plan: <staged %, how to halt + hotfix>   Residual risk: <…>
### Verdict & next step: <submit / fix list / blocked>
```

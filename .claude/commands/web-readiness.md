---
description: Web production-readiness gate — runs the web-production checklist plus the baseline security/performance/accessibility/production gates and returns a go/no-go with P0 blockers, P1 follow-ups, and evidence. Use before launching or releasing a web app, or when asked "is this production-ready / safe to ship / launch-ready".
argument-hint: [--mode audit-only|production-hardening]  (default audit-only)
---

# /web-readiness

## Purpose
The single ship-gate for a web app. It verifies the web-specific production checklist and the
universal gates, then issues a clear **go / fix-first / no-go** verdict backed by real evidence —
not a cosmetic checkmark sweep. In `production-hardening` mode it also fixes P0/P1 gaps and re-verifies.

## When to use
- Before a production launch or a significant release.
- At the quarterly production-readiness review.
- When someone asks "is this ready to ship / launch / go live?"

## Workflow
1. **Map & classify** (if not already): `.claude/agents/core/codebase-mapper.md` → `docs/state/codebase-map.md`; confirm it's a web app and note the stack/hosting.
2. **Run the web gate**: walk `.claude/checklists/web-production.md` (P0–P3). Each item is marked pass/fail with **evidence** — a header dump, a Lighthouse/axe run, a test command + output, a config line. Never mark passed by assumption.
3. **Run the baseline gates** via their owners: `.claude/checklists/security.md` (`security-auditor`), `.claude/checklists/performance.md` (`performance-engineer`), `.claude/checklists/accessibility.md` (`accessibility-auditor`), `.claude/checklists/production.md` + `.claude/checklists/release-rollback.md` (`production-readiness-auditor` + `reliability-engineer`). Run concurrently — each reads, writes its own section.
4. **Reconcile** into one ranked list (P0→P3); dedupe overlaps.
5. **Apply mode**: `audit-only` reports. `production-hardening` fixes P0/P1, re-runs the affected checks, and records any deliberately-deferred gap as a risk in `docs/decisions/`.
6. **Verdict + risk review**: go / fix-first / no-go, with blast radius and rollback confirmed.

## Agents used
`.claude/agents/core/codebase-mapper.md`, `.claude/agents/quality/production-readiness-auditor.md` (lead), `.claude/agents/quality/{security-auditor,performance-engineer,accessibility-auditor,reliability-engineer}.md`, `.claude/agents/engineering/devops-engineer.md`. `.claude/agents/core/code-reviewer.md` checks any hardening diff.

## Skills used
`.claude/skills/production-readiness/SKILL.md`, `.claude/skills/security/SKILL.md`, `.claude/skills/performance/SKILL.md`, `.claude/skills/observability/SKILL.md`.

## Expected outputs
| Output | Path |
|---|---|
| Readiness report (ranked, with evidence) | `docs/reports/web-readiness-<date>.md` |
| Go/no-go verdict | top of the report |
| Hardening fixes (hardening mode) | code diff + re-verified checks |
| Deferred-risk records | `docs/decisions/` |

## Stop conditions
- Not a web app → suggest `/route` / `/audit-production` instead.
- A P0 (exposed secret, missing authz, no rollback) is found → verdict is **no-go**; surface immediately.
- A check can't be verified (tool/env missing) → mark "unverified" and treat as not-passed; never fabricate.

## Final report format
```
## /web-readiness — <verdict: GO | FIX-FIRST | NO-GO>
Stack: <…>  |  Mode: <…>  |  Date: <…>
### Blockers (P0): <list with evidence>  ·  none → ✓
### Important (P1): <list>
### Hardening/backlog (P2–P3): <count, tracked>
### Hardened this run (hardening mode): <fixes + how verified>
### Rollback: <confirmed path>   Residual risk: <…>
### Verdict & next step: <ship / fix list / blocked>
```

---
description: Mode- and scope-driven web audit. Routes to the right specialist auditors for a chosen area (frontend, backend, api, database, security, performance, accessibility, responsive, devops, observability, or full) and returns ranked, evidence-backed findings — no fabricated results. Use for "audit my web app", "frontend/backend/api/db/security/perf/a11y review", "is this production-ready", or a deep project audit.
argument-hint: <scope: frontend|backend|api|database|security|performance|accessibility|responsive|devops|observability|full> [--mode audit-only|fix-and-verify|production-hardening]
---

# /web-audit

## Purpose
One token-efficient entry point for auditing a web project. Instead of loading every agent, it
classifies the repo, selects only the specialists the chosen **scope** needs, runs them against the
matching gate checklists, and returns a single ranked report. It honors the operating **mode** so the
same command serves a read-only review, a fix-and-verify pass, or production hardening.

## When to use
- "Audit my web app" / "review the frontend / backend / API / database / security / performance".
- Before a release, to find P0/P1 blockers ("is this production-ready?").
- After inheriting a codebase, to get a prioritized risk map.
- As the first step of `/web-readiness` or `/prepare-launch`.

## Workflow
1. **Map first.** Run `.claude/agents/core/codebase-mapper.md` to produce a compact repo map
   (stack, entry points, routes, data layer, test setup) → `docs/state/codebase-map.md`. Skip if a
   fresh map exists.
2. **Resolve scope → specialists** via `.claude/orchestration/web-routing-matrix.md`:
   - `frontend` → frontend-engineer + ui-ux-designer; checklists `web`, `ui-ux`, `accessibility`.
   - `backend` → backend-engineer + api-architect; checklists `backend`, `api`.
   - `api` → api-architect; checklist `api`.
   - `database` → database-architect; checklists `database`, `data-model`.
   - `security` → security-auditor (+ privacy-compliance-auditor if personal data); checklists `security`, `dependencies`, `privacy-compliance`.
   - `performance` → performance-engineer; checklists `performance`, `cost`.
   - `accessibility` → accessibility-auditor; checklist `accessibility`.
   - `responsive` → mobile-ux-specialist + accessibility-auditor; checklists `accessibility`, `web`.
   - `devops` → devops-engineer + cloud-architect; checklists `devops`, `release-rollback`.
   - `observability` → reliability-engineer; checklists `observability`, `incident-response`.
   - `full` → run every scope above **concurrently** (safe: each reads, writes its own report), then dedupe.
3. **Run the gate(s).** Each specialist works read-only against its checklist; mark every item pass/fail with file:line evidence. Do **not** fabricate test output — run the real command or mark the item "unverified".
4. **Apply mode.** `audit-only` stops here. `fix-and-verify` fixes P0/P1, then re-runs build/lint/tests and re-audits the changed area. `production-hardening` drives `.claude/checklists/web-production.md` to green or records each gap as a risk.
5. **Reconcile & rank.** The orchestrator dedupes overlapping findings and ranks P0→P3.
6. **Risk review + summary.** State blast radius and reversibility for any change; emit the final report.

## Agents used
`.claude/agents/core/codebase-mapper.md`, `.claude/agents/core/orchestrator.md`, and the scope's specialists from the routing matrix (`.claude/agents/quality/*`, `.claude/agents/engineering/*`, `.claude/agents/design/*`). `.claude/agents/core/code-reviewer.md` verifies any diff in fix-and-verify mode.

## Skills used
`.claude/skills/discovery/SKILL.md`, plus the scope's skill(s): `web`, `backend`, `api-design`, `data-modeling`, `security`, `performance`, `testing`, `observability`, `devops`, `ui-ux-design`.

## Expected outputs
| Output | Path |
|---|---|
| Repo map | `docs/state/codebase-map.md` |
| Audit report (ranked P0–P3) | `docs/reports/web-audit-<scope>-<date>.md` |
| Fixes (fix-and-verify mode) | code diff + updated tests |
| Risk records (non-obvious calls) | `docs/decisions/` |

## Stop conditions
- No web stack detected → stop; suggest `/route` to classify first.
- `fix-and-verify` requested but tests can't run (missing deps) → report which, fix or mark unverified, do not fake a pass.
- A P0 security/data-loss issue is found mid-fix → stop, surface it, get confirmation before continuing.

## Final report format
```
## /web-audit — <scope> (<mode>)
Stack: <detected>  |  Scope: <area(s)>  |  Mode: <mode>
### Findings (N): P0 <n> · P1 <n> · P2 <n> · P3 <n>
- [P0] <title> — <file:line> — evidence: <…> — fix: <…>
### Fixed & verified (fix-and-verify): <list + how proven (command + result)>
### Risk review: <blast radius / reversibility>
### Verdict: <ship / fix-first / blocked>  ·  Next: <command>
```

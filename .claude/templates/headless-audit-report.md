# Headless Run Report — `<run-id>`

> **What this is:** the standard, machine-and-human-readable output of one **non-interactive** run of the OS (CI job, cron routine, webhook handler). Because no human watched the run, this report is the entire account of what happened: what was checked, what was found, what — if anything — was changed, what it cost, and whether the gate passed. Produced by the headless runner; gated by `.claude/checklists/headless-ci.md` (and `.claude/checklists/routine-safety.md` for scheduled runs); method in `.claude/docs/HEADLESS_AND_ROUTINES.md` and `.claude/skills/headless-automation/SKILL.md`. Secrets must never appear anywhere in this file (CLAUDE.md §8).

---

## 1. Run metadata

| Field | Value |
|-------|-------|
| Run ID | `<ci-run-12345 / routine-nightly-audit-2026-06-26>` |
| Trigger | `<push | PR #123 | cron @daily 02:00 UTC | manual dispatch | webhook>` |
| Started / finished (UTC) | `<YYYY-MM-DDThh:mm:ssZ>` → `<…>` |
| Runner | `<github-actions ubuntu-24.04 | self-hosted node-7>` |
| Commit (pinned) | `<full SHA — the exact revision audited, not a branch tip>` |
| Branch / ref | `<refs/heads/feature-x>` |
| Mode | `<read-only | write-enabled (--allow-write)>` |
| Identity | `<scoped CI service account — least privilege>` |
| Target environment | `<non-prod | staging — never prod without recorded approval>` |

---

## 2. Scope

> What this run was asked to do, and the boundary it was not allowed to cross.

- **Commands run:** `<` /audit-security, /audit-production `>`
- **Paths / surface in scope:** `<src/**, .claude/** | whole repo>`
- **Explicitly out of scope:** `<production systems, real-user channels, secret rotation>`

---

## 3. Per-gate results

| Gate | Checklist | Result | Blocking findings | Notes |
|------|-----------|--------|-------------------|-------|
| Security | `.claude/checklists/security.md` | `<PASS | FAIL | SKIP>` | `<0 | n>` | `<…>` |
| Dependencies | `.claude/checklists/dependencies.md` | `<PASS | FAIL>` | `<…>` | `<…>` |
| QA | `.claude/checklists/qa.md` | `<PASS | FAIL>` | `<…>` | `<…>` |
| Performance | `.claude/checklists/performance.md` | `<PASS | FAIL | N/A>` | `<…>` | `<…>` |
| Accessibility | `.claude/checklists/accessibility.md` | `<PASS | FAIL | N/A>` | `<…>` | `<…>` |
| MCP safety | `.claude/checklists/mcp-safety.md` | `<PASS | N/A>` | `<…>` | `<…>` |

---

## 4. Findings by severity

> Map each to its checklist item. P0 blocks; P1 important; P2 hardening; P3 backlog.

- **P0 (blockers):** `<none | FIN-001: hardcoded token in config.ts:42 — security.md>`
- **P1 (important):** `<FIN-002: missing rate limit on /api/x>`
- **P2 (hardening):** `<…>`
- **P3 (backlog):** `<…>`

---

## 5. Actions taken

> Exactly what the run changed. A read-only run lists "none". Anything mutating must be itemized.

| Action | Type | Dry-run done? | Reversible via | Approver |
|--------|------|---------------|----------------|----------|
| `<none — read-only run>` | — | — | — | — |
| `<opened PR #130 with lint fixes>` | `<write/non-prod>` | `<yes — diff attached>` | `<close/revert PR>` | `<n/a — non-prod, in-scope>` |

### Destructive operations
> Any delete/overwrite/send/deploy/spend. Each needs a justification + named human approver, or it should not have run (`.claude/checklists/headless-ci.md` P0).

- `<NONE>` *(expected for read-only runs)* — or — `<OP + justification + approver + recorded decision link>`

---

## 6. Budget & time consumed

| Metric | Used | Cap | Within budget? |
|--------|------|-----|----------------|
| Wall-clock | `<6m 12s>` | `<15m>` | `<yes>` |
| Tokens / cost | `<420k / $1.30>` | `<1M / $5>` | `<yes>` |
| Tool/API calls | `<37>` | `<200>` | `<yes>` |

---

## 7. Gate exit status

| Field | Value |
|-------|-------|
| Overall verdict | `<GREEN — all gates pass | RED — blocking findings | ERROR — run failed>` |
| Exit code | `<0 on green only; deterministic non-zero on any red gate, refused forbidden action, or run failure>` |
| Reason for non-zero (if any) | `<P0 finding FIN-001 | budget exceeded | forbidden action blocked closed>` |

---

## 8. Residual risk & next actions

- **Residual risk:** `<what remains unresolved and its severity>`
- **Reversibility:** `<how to undo anything this run did, or "nothing to undo (read-only)">`
- **Recommended next actions:** `<who should do what — e.g. fix FIN-001 before merge; file P1s as issues>`
- **Escalation (if RED):** `<owner/channel notified per .claude/checklists/routine-safety.md>`

---
**Done when:** metadata pins the exact commit and trigger, every gate has a PASS/FAIL/N-A with finding counts, all actions (especially destructive ones) are itemized with reversibility and approver, budget vs. cap is shown, and the exit code is consistent with the verdict (non-zero on any red gate). No secret appears anywhere in this report.

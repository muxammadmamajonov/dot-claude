# Routine Definition — `<routine-name>`

> **What this is:** the definition of **one** scheduled / recurring agent run (a cron job, nightly audit, weekly dependency review, docs-drift check). A routine acts repeatedly with no human starting each run, so its danger is *repetition without supervision*. This document pins down what it does, how often, in which safety mode, who owns it, how to stop it, and why running it twice is safe. Authored with `.claude/skills/routine-authoring/SKILL.md`; gated by `.claude/checklists/routine-safety.md`; runs emit `.claude/templates/headless-audit-report.md`; method in `.claude/docs/HEADLESS_AND_ROUTINES.md`.

---

## 1. Identity & ownership

| Field | Value |
|-------|-------|
| Routine name | `<nightly-dependency-audit>` |
| Owner | `<@person / rotation — accountable for runs and failures, not "the team">` |
| Purpose | `<one sentence: what value this routine delivers>` |
| Created / last reviewed | `<YYYY-MM-DD>` · Next review due `<YYYY-MM-DD>` |
| Status | `<active | paused | retired>` |

---

## 2. Schedule & trigger

| Field | Value |
|-------|-------|
| Schedule | `<cron: 0 2 * * *  (daily 02:00 UTC)>` |
| Trigger type | `<time-based cron | event (e.g. new release) | webhook>` |
| Frequency rationale | `<why this cadence — vs. cost and blast radius>` |
| Change-detection | `<runs only if <X changed> since last run; otherwise no-op / report-only>` |

---

## 3. Scope & runner

- **What it operates on:** `<dependency manifests + lockfiles across the repo>`
- **Explicitly out of scope:** `<no production systems, no real-user channels, no secret rotation>`
- **Target environment:** `<non-prod by default — prod requires per-run human approval (CLAUDE.md §8)>`
- **Runner / identity:** `<github-actions | self-hosted; scoped service account — least privilege>`
- **Reads before acting:** `<preset, docs/state/, relevant specs — so actions match the real project stage>`

---

## 4. Safety mode

> Pick exactly one. Destructive/production actions are **never** `approved-write` on a schedule without a per-run human approver (`.claude/checklists/routine-safety.md` P0).

- [ ] **read-only** — inspects and reports; performs no writes. *(default; safest)*
- [ ] **propose** — produces recommendations / a dry-run diff / a draft PR; a human must approve before anything is applied.
- [ ] **approved-write** — may apply changes **only** within the declared non-destructive, non-prod scope below; each destructive action still requires explicit human confirmation.

**Declared write scope (if not read-only):** `<e.g. may open a PR bumping patch versions on a branch; may NOT merge, delete, deploy, or touch prod>`

---

## 5. Steps

> Ordered, each step's effect, and whether it mutates anything. Reads come before writes.

1. `<Read lockfiles + manifests>` — *read*
2. `<Run SCA scan (.claude/checklists/dependencies.md)>` — *read*
3. `<Detect change vs. last run; no-op if none>` — *read*
4. `<Compose report of findings + recommended bumps>` — *read*
5. `<(propose mode) open draft PR with safe patch bumps for human review>` — *write, non-prod, no auto-merge*

---

## 6. Reporting & escalation

- **Report destination:** `<issue tracker | #ops channel | .claude/templates/headless-audit-report.md artifact>`
- **Every run reports:** what it found, what it recommended, what (if anything) it did.
- **Failure alert:** `<error/timeout/skip pages <owner> via <pager/channel> — silent failure forbidden>`
- **Escalation on serious finding:** `<e.g. P0 CVE → notify @security immediately; routine pauses writes, keeps reporting>`
- **Auto-disable threshold:** `<after <N> consecutive failures, disable and page owner>`

---

## 7. Kill-switch

> A single, fast way to stop this routine without editing code or redeploying.

- **How to disable:** `<set ROUTINE_NIGHTLY_AUDIT_ENABLED=false | pause the schedule in <platform> | toggle <flag>>`
- **Who can disable:** `<owner + on-call>`
- **Verification:** `<how to confirm it is actually stopped — e.g. next scheduled run shows "skipped">`

---

## 8. Idempotency & budget

- **Idempotency strategy:** `<re-running, or re-running after a partial failure, yields the same end state — e.g. PR keyed by content hash so no duplicate PRs; sends keyed by run-date>`
- **Concurrency:** `<lock / single-flight so two runs cannot overlap on shared state>`
- **Per-run caps:** wall-clock `<10m>` · cost `<$2 / 300k tokens>` · tool calls `<150>` — exceeding any cap aborts cleanly and reports.

---
**Done when:** the routine has a named owner, a documented kill-switch, a stated idempotency strategy, a wired failure alert, exactly one safety mode (with declared write scope if it can act), a report destination, and a confirmation that it reads project state before acting. No destructive or production action runs unsupervised — it reports and recommends, and waits for approval.

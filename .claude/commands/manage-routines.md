---
description: Register, list, and inspect scheduled routines (recurring audits, dependency reviews, docs-drift checks, readiness reviews); each is report-first, approval-gated, and recorded in docs/state/routines.md.
argument-hint: <register | list | inspect | disable> [routine-name]
---

# /manage-routines

## Purpose
Maintain the project's set of **scheduled routines** — recurring, mostly-unattended runs of this system's audit/review/readiness commands (e.g. a weekly security audit, a dependency/supply-chain review, a docs-drift check, a monthly production-readiness review). This command registers new routines, lists the existing ones, inspects a single routine's definition and history, or disables one. Every routine is **report-first and approval-gated**: it may produce findings and reports but must never take an unsupervised destructive or production action — those always require a human. Routines are defined from a single template, name an explicit runner (cron, CI schedule, or Claude Code's native `/schedule` plus the scheduled-tasks MCP if available), and record their next-due date so the team can see what will run and when. This command manages routine *definitions*; the actual unattended execution goes through `/headless-run`.

## When to use
- After launch (or once a project is stable), to stand up recurring guardrails so quality gates keep running without manual prompting.
- When adding a new recurring check (e.g. "review dependencies every Monday", "re-run the readiness audit monthly").
- To audit what scheduled automation already exists (`list`), or to inspect one routine's exact definition, runner, and last result (`inspect`).
- To pause a routine that is noisy, redundant, or no longer relevant (`disable`) — without deleting its history.

## Workflow

### Step 0 — Load context and parse the action (read-only)
1. Read `.claude/docs/HEADLESS_AND_ROUTINES.md` for the routine model: report-first, approval-gated, named-runner.
2. Read `.claude/skills/routine-authoring/SKILL.md` for how to define a well-scoped, safe routine.
3. Read `.claude/checklists/routine-safety.md` — the gate every routine definition must pass.
4. Read `.claude/templates/routine-template.md` — the definition shape.
5. Read `docs/state/routines.md` if it exists (the registry of current routines).
6. Parse the action (`register | list | inspect | disable`) and the optional routine name. Default action when none given: `list`.

### Step 1 — Branch by action
- **list** → render the current registry: each routine's name, target command, schedule, runner, next-due date, and enabled/disabled state. Then exit via the report format.
- **inspect** → for the named routine, show its full definition, the last run's report path and verdict (if any), and its next-due date. Then exit.
- **disable** → mark the named routine disabled in `docs/state/routines.md`, preserving its definition and history; note who/when in the entry. Then exit.
- **register** → continue to Step 2.

### Step 2 — Define the routine (register)
Using `.claude/templates/routine-template.md`, draft the routine:
- **Target command** — which audit/review/readiness command runs (it executes via `/headless-run`, inheriting that command's fail-closed envelope).
- **Schedule** — cron expression or human cadence (e.g. weekly Monday 09:00).
- **Runner** — exactly one of: external cron, CI schedule, or Claude Code's native `/schedule` plus the scheduled-tasks MCP. Do **not** assume the scheduled-tasks MCP exists; if it is not configured, fall back to cron/CI and note that in the definition.
- **Mode** — report-first and read/review-only by default. A routine may never be defined with unsupervised write-to-production or destructive scope.
- **Output** — where the routine's reports land (`docs/reports/`), and who is notified.

### Step 3 — Enforce routine safety
Run `.claude/checklists/routine-safety.md` against the draft: report-first confirmed; no unsupervised destructive/production action; runner named and reachable (or a documented fallback); failure/escalation path defined; schedule sane (not so frequent it floods reports). Any P0 failure blocks registration.

**STOP — Present the proposed routine to the user.** State its target command, schedule, runner, mode, and output location, and confirm it takes no destructive action. Ask: "Approve this routine for registration? Reply before I write it to the registry." Wait for acknowledgment — a routine is never registered silently.

### Step 4 — Register and record
1. Append the approved routine to `docs/state/routines.md` with its computed next-due date and enabled state.
2. If the runner is external (cron/CI), emit the schedule snippet for the user to install in their own pipeline — this command does not install it for them.
3. Record the registration as an assumption/decision via `.claude/templates/assumptions-log.md` (and a decision record if the routine governs a production-readiness gate).

## Agents used
- `.claude/agents/core/orchestrator.md` — owns the routine registry and enforces the report-first, approval-gated contract.
- `.claude/agents/core/project-manager.md` — sequences cadence and ownership so routines map to real review responsibilities.

## Skills used
- `.claude/skills/routine-authoring/SKILL.md` — how to scope, schedule, and safety-bound a recurring routine.

## Expected outputs
| Output | Path |
|---|---|
| Routine registry (definitions + next-due) | `docs/state/routines.md` |
| Runner snippet (for external cron/CI) | emitted in report for user to install |
| Assumptions / decision record | `docs/state/assumptions.md`, `docs/decisions/` |

## Stop conditions
- A routine is requested with unsupervised destructive or production write scope → **decline**; routines are report-first only. Offer a report-only variant instead.
- The named runner (e.g. scheduled-tasks MCP) is not configured and no cron/CI fallback is possible → **STOP**; register the definition as `disabled` with a note, and tell the user what to configure.
- `inspect`/`disable` names a routine not present in the registry → report it as not found; do not create a stub.
- A proposed schedule is so frequent it would flood `docs/reports/` or duplicate an existing routine → flag it and ask the user to confirm or widen the cadence before registering.

## Final report format
```
## /manage-routines — <action> — <date>

**Action:** register | list | inspect | disable

### Routine registry
| Name | Target command | Schedule | Runner | Mode | Next due | State |
|---|---|---|---|---|---|---|
| weekly-security | /audit-security | Mon 09:00 | cron | report-only | <date> | enabled |
| dep-review | /audit-security (deps) | Mon 09:00 | CI schedule | report-only | <date> | enabled |
| docs-drift | /review-feature (docs) | nightly | /schedule + MCP | report-only | <date> | enabled |

### This action
<what changed: routine registered / disabled / inspected; or the rendered list>

### Safety
Routine-safety checklist: <PASS | N P0 blockers>. Destructive scope: none (report-first).

### Next step
<install the emitted cron/CI snippet | nothing further | configure the named runner>
Registry: docs/state/routines.md
```

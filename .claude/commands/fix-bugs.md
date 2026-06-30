---
description: Systematic debugging — reproduce, isolate root cause, fix with a regression test, verify
argument-hint: [bug description or issue ID]
---

# /fix-bugs

## Purpose
Fix one or more bugs using a disciplined, evidence-based process: reproduce the bug reliably, isolate the root cause (not just the symptom), apply the minimal safe fix, write a regression test that would have caught it, and verify no regressions were introduced. Never patch symptoms without understanding cause.

## When to use
- When a test suite is failing after `/implement-feature` or `/create-tests`
- When a bug is reported from a review finding (link from `/review-feature`)
- When a production or staging incident needs a fix
- When the argument names a specific bug or issue ID; if omitted, ask for a description or error message
- One bug or tightly related bug cluster per run — do not batch unrelated bugs

## Workflow

**Step 1 — Gather evidence** (orchestrator: `.claude/agents/core/orchestrator.md`)
Collect all available signal before touching any code:
- Exact error message or unexpected behaviour description
- Stack trace (full, not truncated) with file paths and line numbers
- Environment where it occurs: OS, runtime version, browser, device, queue consumer, embedded hardware
- Steps to reproduce (from the reporter or inferred from the error)
- When it first appeared: last known-good commit or deployment
- Frequency: always / intermittent / under specific load

Write a brief bug summary to `.claude/bugs/[issue-id]-investigation.md` and keep it updated throughout.

**Step 2 — Reproduce locally**
- Construct the minimal reproduction: the smallest input or sequence of steps that reliably triggers the bug
- If reproduction requires a specific database state, write a fixture or seed script — do not use production data
- If the bug is intermittent, reproduce it at least 3 times before proceeding; if it cannot be reproduced, document why and ask the user for more signal before continuing
- Record the exact reproduction command or sequence in the investigation file

STOP — if the bug cannot be reproduced reliably, do not guess at a fix. Present findings to the user and ask for additional context (logs, traces, request IDs, environment variables).

**Step 3 — Isolate root cause**
Work from the error backwards, layer by layer:
1. Identify the failing assertion, exception, or incorrect output — the observable symptom
2. Trace the call stack to find where the unexpected state was first introduced — the origin point
3. Identify the condition or input that triggers the bad path — the trigger
4. Determine why the code at the origin point produces bad output — the root cause

Root-cause categories to consider:
- **Logic error**: incorrect conditional, wrong algorithm, bad type assumption
- **State/ordering**: shared mutable state, race condition, initialisation order dependency
- **Boundary**: off-by-one, integer overflow, empty collection, null/undefined input not handled
- **Integration contract**: API response shape changed, schema migration not applied, config key renamed
- **Environment**: missing env var, wrong version of a dependency, OS-specific behaviour
- **Data**: unexpected data shape in production that tests never exercised

Write the identified root cause (one or two sentences) to the investigation file before writing any fix.

STOP — business-critical decision
Present the root cause analysis to the user. Ask:
1. Does this root-cause analysis match the observed behaviour?
2. Are there other locations in the codebase with the same pattern that need the same fix?
3. If the fix requires a data migration or a breaking API change — confirm scope and rollback plan before proceeding.

**Step 4 — Write a failing regression test first**
Before fixing:
- Write a test that reproduces the exact bug scenario and fails on the current code
- Place it in the appropriate test layer (unit if pure logic; integration if I/O; E2E if user-journey)
- Confirm the test is red before writing the fix

This test must be committed alongside the fix so the bug cannot silently reappear.

**Step 5 — Apply the minimal fix**
Rules:
- Fix the root cause, not the symptom — do not add a guard clause on top of broken logic if the logic itself is wrong
- Make the smallest change that fixes the root cause — no opportunistic refactors in the same commit
- No `rm -rf`, no dropping tables or migrations, no force-pushes, no changes to production data without explicit human approval
- If the fix requires a database migration: write a reversible migration; test the down migration; document the rollback procedure in the investigation file
- If the fix affects a public API or interface: note the breaking change and update the API spec

**Step 6 — Verify**
- Run the regression test from Step 4 — it must now be green
- Run the full test suite — all pre-existing tests must remain green
- If the bug was in the UI: manually walk through the reproduction steps to confirm the fix
- If the bug was a race condition or intermittent: run the reproduction 5+ times to confirm it no longer triggers
- Check that the fix does not introduce new lint warnings or type errors

**Step 7 — Search for related instances**
- Search the codebase for the same pattern or condition that caused the bug
- List any other locations where the same root cause could manifest
- For each: either apply the same fix immediately (if safe) or file a follow-up item in `docs/specs/roadmap.md` under tech debt

**Step 8 — Finalise investigation file**
Update `.claude/bugs/[issue-id]-investigation.md` with:
- Confirmed root cause (one paragraph)
- Fix applied (file:line, description of change)
- Regression test location
- Related instances found and their status
- Any follow-up items added to the roadmap

## Agents used
- `.claude/agents/core/orchestrator.md` — coordinates investigation and fix steps
- `.claude/agents/quality/qa-engineer.md` — regression test authoring (if present)
- `.claude/agents/quality/security-auditor.md` — if root cause is security-related (if present)

## Skills used
- `.claude/skills/security/SKILL.md` — if the bug has a security dimension
- `.claude/checklists/security.md` — cross-check fix for new vulnerabilities

## Expected outputs
| Artefact | Status |
|----------|--------|
| `.claude/bugs/[issue-id]-investigation.md` | created |
| Regression test (failing before fix, green after) | created |
| Fix code | modified |
| Full test suite | all green |
| Roadmap updated (related instances deferred) | updated (if applicable) |

## Stop conditions
- Bug cannot be reproduced — halt after Step 2, ask user for more signal; do not guess at a fix
- Root cause requires a destructive action (data migration, breaking API change, schema drop) — halt after Step 3, present impact and rollback plan, require explicit human approval
- Fix causes new test failures that cannot be resolved without larger refactor — document scope, present to user, do not silently expand the change
- Bug is in a third-party dependency — document the version, check for an upstream patch or known CVE, propose a workaround or upgrade path; do not monkey-patch vendor code

## Final report format
```
## Bug fix — [issue ID or short description]

### Root cause
[One paragraph: what was wrong, where, and why]

### Trigger condition
[The specific input / state / sequence that activates the bug]

### Fix applied
- File: [path:line]
- Change: [one-line description]
- Migration: [yes — reversible | no]

### Regression test
- File: [path]
- Layer: unit | integration | E2E
- Status: GREEN

### Full test suite: all green | N regressions (list)

### Related instances
| Location | Status |
|----------|--------|
| [file:line] | fixed in this PR | deferred to roadmap |

### Files modified
- [list with paths]

### Investigation file
- .claude/bugs/[issue-id]-investigation.md

### Next step
Run /review-feature [feature name] if this fix is part of an open feature branch
```

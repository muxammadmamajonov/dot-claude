---
description: Lite-mode fast path for a small, well-understood, low-risk change — skip interview/spec ceremony, verify, report. Auto-escalates to the full flow if the task turns out bigger than expected.
argument-hint: <one-line description of the small change>
---

# /quick-fix

## Purpose
Not every request is a project. A typo, a one-line config change, an obvious bug with an obvious fix
does not need an interview, a spec document, and a formal audit trail — but it still needs to be
understood before it's touched, verified after, and never allowed to quietly skip a real safety rule
just because it looked small at a glance. `/quick-fix` is lite mode's entry point
(`.claude/docs/OPERATING_MODES.md`): full rigor, zero ceremony, for work that actually earns it.

## When to use
- The user explicitly asks for a quick fix, a small change, or says "don't overthink this."
- A single-file or tight-cluster change with an obvious cause and an obvious fix.
- Anything that would otherwise force a disproportionate amount of spec/interview overhead onto a
  trivial diff.

## Workflow

### Step 1 — Confirm lite-mode eligibility (gate, not a formality)
Check every condition in `.claude/docs/OPERATING_MODES.md`'s lite-mode heuristic:
- Single file or a tight cluster of obviously-related files.
- Diff reasonably estimated under ~20–30 lines before starting.
- No new dependency, no schema/migration change, no new public API/interface contract.
- Nothing touching auth, payments, secrets, or infrastructure — and nothing on
  `.claude/CLAUDE.md` §8's forbidden-without-approval list.

**If any condition fails, STOP** — do not force it through. Say so plainly and hand off to
`.claude/commands/implement-feature.md` or `.claude/commands/start-project.md` (full flow) instead.

### Step 2 — State the one-line understanding and plan
One sentence: what's wrong or needed. One sentence: what you're about to change. No spec document, no
architecture note — the point is proportional effort, not zero effort.

### Step 3 — Make the change
Read the touched file(s) first even for a "small" fix — never edit code you haven't actually read.

### Step 4 — Verify (never skipped, regardless of size)
Run the relevant tests, linter, and/or build for the touched area, sourced from the repo's own config
(`package.json` scripts, `Makefile`, CI config) — never assumed. "Quick" describes the ceremony that's
skipped, not the verification.

### Step 5 — Record only if non-obvious
If anything non-obvious was decided (a naming choice with real alternatives, a small trade-off), append
one line to `docs/state/assumptions.md` — no new formal decision record for routine choices. If nothing
non-obvious happened, add nothing; don't manufacture paperwork.

### Step 6 — Auto-escalate on scope creep
If, mid-task, the change turns out to touch more files, need a new dependency, or brushes against a
§8-listed area you didn't see at Step 1, **stop and escalate to full mode** — report what changed your
assessment and continue under `.claude/commands/implement-feature.md` instead of finishing under a
quick-fix label that no longer fits.

## Agents used
- None required by default — that's the point. If the touched area clearly belongs to one specialist
  (e.g. a security-relevant path was flagged at Step 1 and full mode was triggered), hand off to that
  single agent rather than assembling a team.

## Skills used
- `.claude/skills/testing/SKILL.md` — what "verify" means for the repo's stack.
- `.claude/docs/OPERATING_MODES.md` — the eligibility rule this command enforces.

## Expected outputs
| Output | Path |
|---|---|
| The code change itself | (touched files, in place) |
| One-line assumption (only if non-obvious) | `docs/state/assumptions.md` (appended) |

## Stop conditions
- Fails any Step 1 eligibility check → refuse quick-fix mode, route to the full flow.
- Touches anything on `.claude/CLAUDE.md` §8's forbidden list → always full mode, always explicit approval — no exception for "it's a small change."
- Scope grows mid-task past the Step 1 estimate → escalate per Step 6, do not push through.

## Final report format
```
## /quick-fix — <one-line description>

**Eligibility:** confirmed lite-mode (single file/cluster, <~30 lines, no dep/schema/§8 surface)
**Change:** <one-line what changed> — <file paths>
**Verified:** <test/lint/build command(s) run> — <pass/fail>
**Assumption logged:** <one line, or "none — nothing non-obvious">
```

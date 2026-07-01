---
description: Read-only explanation of how existing code, architecture, or a flow currently works. Never edits anything — for when the ask is understanding, not building.
argument-hint: <what to explain — a file, a feature, a flow, "how does X work", "where does Y live">
---

# /explain

## Purpose
A large share of real requests are questions, not build requests — "how does auth work here," "where
does this value come from," "walk me through what happens on checkout." Forcing those through the
9-stage flow is absurd; `.claude/CLAUDE.md` §1 already only mandates the flow for non-trivial *changes*.
`/explain` makes the read-only path an explicit, named command instead of an ambiguous judgment call,
and guarantees it stays read-only — no code, config, or docs are modified by this command, ever.

## When to use
- "Explain X," "how does Y work," "where does Z live," "walk me through this flow."
- Before a change, when the real need is understanding the current behavior first — use this, then
  decide separately whether to follow up with `.claude/commands/quick-fix.md` or the full flow.
- Onboarding-adjacent but narrower than `.claude/commands/onboard.md` — `/explain` answers one question;
  `/onboard` produces a whole-repo brief.

## Workflow

### Step 1 — Confirm this is genuinely read-only
If the real ask has an implicit "...and then fix/change it," say so and stop treating it as `/explain` —
route to `.claude/commands/quick-fix.md` or the full flow instead. Do not let an explanation quietly
turn into an unreviewed change.

### Step 2 — Scope the read proportionally
- If `docs/state/codebase-map.md` exists and is fresh, use it as a starting index.
- If the ask is narrow (one function, one file, one config value), just read that directly — do not
  invoke a full `.claude/agents/core/codebase-mapper.md` pass to answer a one-line question.
- If the ask is broad ("how does the whole auth system work") and no map exists, it's reasonable to run
  the mapper first so the explanation is grounded in a real map rather than a guess.

### Step 3 — Trace the real path
Read the actual files involved and follow the real call/data path — never explain from naming
conventions or assumption alone. If something is genuinely unclear from the code, say so rather than
guessing at what it "probably" does.

### Step 4 — Produce the explanation
State what happens, in what order, where the interesting logic/edge cases/gotchas live, with concrete
`file_path:line_number` references so the reader can jump straight to the source. Offer a short diagram
(sequence/flow) only if a multi-step flow genuinely benefits from one — plain text is enough for most asks.

### Step 5 — No hidden writes
Nothing is written to disk by default — the explanation is the answer, not a file. If the user wants it
saved as a durable doc, offer to write it (e.g. into `docs/architecture.md` or a new note), but only on
request; never write silently, per this pillar's transparency principle (every command states what it
will touch — this one touches nothing unless explicitly asked to).

## Agents used
- `.claude/agents/core/codebase-mapper.md` — only for broad, whole-system explanations where no fresh map exists; skip it for narrow questions.

## Skills used
- `.claude/skills/discovery/SKILL.md` — how to read a codebase efficiently without slurping the whole tree.
- `.claude/skills/documentation/SKILL.md` — if the user asks to save the explanation as a doc.

## Expected outputs
| Output | Path |
|---|---|
| The explanation itself | conversational — no file by default |
| Saved doc (only if requested) | wherever the user directs, or `docs/architecture.md` by convention |

## Stop conditions
- The ask turns out to secretly want a change → stop, say so, and hand off to `/quick-fix` or the full flow rather than editing under the guise of explaining.
- The code path genuinely can't be determined from what's in the repo → say that plainly instead of inventing a plausible-sounding but unverified answer.

## Final report format
```
## /explain — <what was explained>

<the explanation: what happens, in order, with file_path:line_number references>

**Traced from:** <files actually read>
**Diagram offered:** <yes/no — only if it clarified a multi-step flow>
```

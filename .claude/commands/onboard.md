---
description: Produce a fast, accurate "how this repo works" brief for a new engineer or a fresh AI session joining an existing project — stack, structure, current stage, active team, risks, and how to run it.
argument-hint: [package-name — optional, scope onboarding to one package in a monorepo]
---

# /onboard

## Purpose
Joining an unfamiliar or inherited codebase is expensive — a human re-reads the tree for an afternoon, and a fresh AI session either re-discovers everything from scratch or, worse, guesses. `/onboard` runs the mapping and classification steps once and writes a single, durable brief so the next person (or the next session) starts from facts, not archaeology.

## When to use
- A new engineer joins the project and needs to be productive same-day.
- A new AI session starts cold on a repo that already has code and history but no fresh `docs/state/` context.
- Returning to a project after a long gap where prior context has aged out of memory (`.claude/docs/MEMORY_STRATEGY.md`).
- In a monorepo, onboarding onto one specific package rather than the whole repo (pass `package-name`).

## Workflow

### Step 1 — Detect scope
1. Check `.claude/orchestration/monorepo-routing-matrix.md`'s topology signals. If the repo is a monorepo and no `package-name` argument was given, produce a root-level brief plus a one-paragraph summary per package (not a full per-package deep-dive — link to running `/onboard <package-name>` for that). If `package-name` was given, scope every later step to that package's subtree.
2. If `docs/state/codebase-map.md` (or the package-scoped equivalent) already exists and is recent, skip to Step 3 with a note that it was reused rather than regenerated — do not silently re-run expensive discovery when it isn't stale.

### Step 2 — Map and classify
1. Dispatch `.claude/agents/core/codebase-mapper.md` to produce/refresh `docs/state/codebase-map.md` (stack, structure, entry points, routes, data layer, auth, tests/CI, run commands, risk smells).
2. Run `.claude/commands/route.md` if no cached `docs/state/project-type.md` / `docs/state/active-team.md` exists, so the brief can state the project's classification and its currently active team, not just its file layout.
3. Read any existing `docs/state/project.md`, `docs/state/assumptions.md`, and `docs/decisions/*` — an onboarding brief that ignores prior decisions and assumptions will contradict them within a day.

### Step 3 — Synthesize the brief
Write `docs/ONBOARDING.md` with these sections:
1. **What this is** — one paragraph: project type, primary users, current phase in the 9-stage flow (from `docs/state/project.md` if present, else "not yet classified — run `/route`").
2. **How a request flows** — the codebase-mapper's one-paragraph summary, plus links to entry points/routes/data layer/auth.
3. **Stack & run commands** — from the codebase map, verified against the repo's own config (never assumed).
4. **Active team** — a compact version of `docs/state/active-team.md`: which agents/skills/checklists are actually in play for this project, so a new session doesn't activate the whole system.
5. **Known risks / gotchas** — the codebase-mapper's risk-smell pointers, plus any open items in `docs/state/assumptions.md` or unresolved decision records.
6. **Where things live** — a short map of `docs/specs/`, `docs/state/`, `docs/decisions/` so the next reader knows where to look instead of grepping.
7. **Recommended next action** — the single next step per the current stage gate (e.g. "audit gate is red on performance — see `docs/state/project.md`" or "no specs yet — run `/create-specs`").

### Step 4 — STOP and confirm
Present the brief's summary to whoever invoked `/onboard` (human or the calling session) and ask them to flag anything stale or wrong before treating it as ground truth — a wrong onboarding brief is worse than none, because it's trusted by default.

## Agents used
- `.claude/agents/core/codebase-mapper.md` — stack/structure/risk mapping (Step 2).
- `.claude/agents/core/orchestrator.md` — via `.claude/commands/route.md`, for classification and active-team assembly.

## Skills used
- `.claude/skills/discovery/SKILL.md`, `.claude/skills/project-classification/SKILL.md`, `.claude/skills/documentation/SKILL.md`.

## Expected outputs
| Output | Path |
|---|---|
| Codebase map | `docs/state/codebase-map.md` (or per-package under `docs/state/packages/<name>/`) |
| Classification (if not cached) | `docs/state/project-type.md` |
| Active team (if not cached) | `docs/state/active-team.md` |
| Onboarding brief | `docs/ONBOARDING.md` |

## Stop conditions
- Empty repo / no source or specs → do not fabricate a brief; report that and hand off to `/route`'s own stop condition ("what are you building?").
- Codebase map and active team are both fresh (generated this session or very recently) → skip regeneration, synthesize directly from what exists, and say so in the final report.
- Monorepo with no `package-name` given and more than ~8 packages → produce the root-level brief and package summaries, but flag that a full per-package `/onboard` run is opt-in, not automatic, to avoid an unbounded fan-out.

## Final report format
```
## /onboard — Onboarding Brief

**Project:** <name>  |  **Scope:** <whole repo | package: name>
**Reused vs regenerated:** codebase map <reused|regenerated>, classification <reused|regenerated>

### Summary
<2-3 sentences: what this is, current stage, one standout risk>

### Full brief
See `docs/ONBOARDING.md`.

### Recommended next action
<the single next step per the current stage gate>
```

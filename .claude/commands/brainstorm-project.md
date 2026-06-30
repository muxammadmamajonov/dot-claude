---
description: Structured idea-to-scoped-concept dialogue that runs BEFORE classification; diverges directions, pressure-tests the idea, and writes a concept brief that feeds /classify-project.
argument-hint: [one-line idea — optional; if omitted, the command asks for it]
---

# /brainstorm-project

## Purpose
Turn a raw, half-formed idea into a *scoped concept* before any classification, interview, or spec work begins. This is the pre-stage-1 step: it does not pick a project type, a stack, or a preset. It exists to answer four questions — **what real problem is being solved, for whom, under what constraints, and how will we know it worked** — and to make sure the idea is small enough and clear enough to classify. The output is a single concept brief at `docs/context/brainstorm.md` that `/classify-project` reads as its starting input. Universal by default: the idea may become a CLI, a game, an embedded controller, a data platform, or a web app — this command stays type-agnostic and never assumes a screen.

## When to use
- At the very beginning, when the user has an idea but not a defined project ("I want to build something that…").
- Before `/start-project` or `/classify-project`, whenever the concept is still fuzzy.
- When a feature request is large or vague enough that it is really a new sub-project needing its own framing.
- When two stakeholders disagree on what is being built and the concept needs to be pinned down in writing.

## Workflow

### Step 0 — Capture the seed
1. If an idea was passed as the argument, restate it back in one sentence and confirm you understood it.
2. If no argument was given, ask one open question: "In one or two sentences, what do you want to build and why?" Wait for the answer.
3. Read any existing `docs/context/` and the repo root for prior context; do not assume a greenfield.

### Step 1 — Find the real problem
1. Separate the **problem** from the **proposed solution**. The user usually states a solution; extract the underlying need.
2. Ask, briefly, who hurts today without this, what they do instead (the status quo / workaround), and why now.
3. Draft a one-paragraph problem statement. Do not proceed until the problem is stated independently of any particular implementation.

### Step 2 — Diverge: 2–3 directions
1. Generate **two or three genuinely different directions** the concept could take — not cosmetic variants. Vary the form factor, the scope, or the core mechanism (e.g. "a CLI you run locally" vs "a hosted service" vs "a library others embed").
2. For each direction give: the core idea, who it serves best, the main risk, and rough effort (S/M/L).
3. **STOP — present the directions to the user.** Ask: "Which direction fits your intent — or is it a blend? Anything I've framed wrong?" Do not pick for the user; direction is a business-critical fork (CLAUDE.md §6).

### Step 3 — Pressure-test the chosen direction
Challenge the surviving idea honestly. Work through:
- **Riskiest assumption** — what must be true for this to work at all?
- **Why-not** — what kills this (no demand, legal blocker, a cheaper existing tool, a hard technical wall)?
- **Smallest proof** — what is the minimum that would validate the core bet?
Record each as a one-line assumption in the brief. If a fatal flaw surfaces, surface it plainly rather than papering over it.

### Step 4 — Define users, constraints, and success metric
1. **Users:** the primary user and, if any, the secondary user. One sentence each.
2. **Constraints:** the hard ones the user has stated or implied — budget, timeline, platform, regulatory, team size, must-use/avoid technologies. Record only stated constraints; flag unknowns as open questions rather than inventing answers.
3. **Success metric:** one measurable signal that the concept worked (e.g. "10 internal users run it weekly", "checkout completes < 3s", "issue triage time halved"). One metric, not a wishlist.

### Step 5 — Decompose if too large
1. Assess scope. If the concept clearly spans multiple independent subsystems (e.g. "a marketplace + its own payment rail + a mobile app + an analytics platform"), it is too large to classify as one project.
2. Propose a **first slice** — the smallest coherent piece that delivers standalone value and can be classified on its own — and list the rest as a follow-on backlog.
3. **STOP — confirm the slice with the user** before writing the brief, since scope is business-critical.

### Step 6 — Write the concept brief
Write `docs/context/brainstorm.md` with this structure:

```markdown
# Concept Brief — <working title>

**Generated:** <ISO date>  |  **Command:** /brainstorm-project  |  **Status:** ready for /classify-project

## Problem
<one paragraph, solution-independent>

## Chosen direction
<the selected direction + one-line rationale>

## Directions considered
- <direction A> — <who / risk / effort>
- <direction B> — <who / risk / effort>

## Users
- Primary: <…>
- Secondary: <… or none>

## Constraints
- <stated constraints; "unknown — open question" where not yet known>

## Success metric
<single measurable signal>

## Riskiest assumptions
- <assumption + smallest proof>

## Scope decision
First slice: <…>   |   Deferred: <… or none>

## Open questions for classification
- <questions /classify-project should resolve>
```

Append any non-trivial framing decisions to `docs/state/assumptions.md` (from `.claude/templates/assumptions-log.md`).

## Agents used
- `.claude/agents/core/business-analyst.md` — frames the problem, extracts constraints, and surfaces the few founder-only decisions.
- `.claude/agents/core/product-manager.md` — shapes directions, scopes the first slice, and defines the success metric.

## Skills used
- `.claude/skills/discovery/SKILL.md` — the questioning method for separating problem from solution and eliciting users and constraints.

## Expected outputs
| Output | Path |
|---|---|
| Concept brief | `docs/context/brainstorm.md` |
| Framing assumptions | `docs/state/assumptions.md` |

## Stop conditions
- **Idea too vague** to state a problem after Step 1 questioning → **STOP**, ask the user for a concrete example of someone hitting the problem; do not invent one.
- **Concept spans many subsystems** → do not classify the whole thing. **STOP** at Step 5, decompose, and carry only the agreed first slice forward.
- **Fatal flaw found** in Step 3 (no real problem, legal blocker, an existing tool already solves it) → report it honestly and ask whether to pivot the direction or stop.
- **User rejects all directions** in Step 2 → gather what they actually want and regenerate before continuing.

## Final report format
```
## /brainstorm-project — Concept Report

**Working title:** <name>
**Status:** ready to classify | needs decomposition | blocked

### Problem (solution-independent)
<one paragraph>

### Chosen direction
<direction> — <why>

### Users
Primary: <…>  |  Secondary: <…>

### Constraints
<bullet list, with open questions flagged>

### Success metric
<single measurable signal>

### Riskiest assumption
<assumption> — smallest proof: <…>

### Scope
First slice: <…>  |  Deferred: <…>

### Next step
Run `/classify-project` — it will read docs/context/brainstorm.md to detect the
project type, platform, and risk class, then `/route` to assemble the team.
```

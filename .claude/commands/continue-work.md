---
description: Resume an in-progress project: read existing specs/state, summarize, and pick the next safe step.
argument-hint: [feature or workstream name — optional]
---

# /continue-work

## Purpose
Re-orient quickly after any interruption — a new session, a context switch, or a handoff between engineers. Read all persistent project state (specs, ADRs, open tasks, last commit, active branches, in-progress agents), produce a crisp summary of where things stand, and identify the single safest next action. Never re-do completed work. Never skip ahead to a risky step without confirming prerequisites.

## When to use
- Starting a new Claude Code session on an existing project.
- Resuming work after a multi-day break.
- Picking up a task handed off by another engineer or agent.
- After a blocked step is unblocked and work can resume.
- When unsure what was done last and what comes next.

## Workflow

### Step 1 — Read project state (all sources, in order)

**Live run-state** (read first — this is the source of truth for where the project stands)
- `docs/state/project-type.md` — classification (project category, presets, cross-cutting concerns).
- `docs/state/project.md` — live project state and current stage.
- `docs/state/assumptions.md` — recorded assumptions and their validation status.
- `docs/state/active-team.md` — the selected agents/skills/checklists for this project (from `/route`).
- `docs/state/plan.md` — the current plan, if one is in flight.

> Run-state lives in `docs/state/`, never inside `.claude/` (CLAUDE.md §11.2). Do not read run-state from `.claude/`.

**Specs and decisions**
- `docs/specs/` — product spec, discovery, requirements, feature specs, glossary.
- `docs/architecture/` — architecture overview and data model.
- `docs/roadmap/phases.md` — phased roadmap.
- `docs/decisions/` — Architecture Decision Records (ADRs).
- `.claude/stack-matrix/` — confirmed tech stack per layer.
- `docs/reports/` — most recent audit/launch reports (read the latest of each type).
- `docs/runbooks/` — operational procedures (signals deployment maturity).

**Task and progress tracking**
- `docs/state/tasks.md` — task list and per-item status. (Legacy `tasks.md` / `TODO.md` at the repo root may also exist; if so, reconcile into `docs/state/tasks.md`.)
- Open GitHub/GitLab issues if a URL is configured in `docs/state/project.md`.

**Code state**
- `git log --oneline -20` — last 20 commits; identify the most recent feature work.
- `git status` — uncommitted changes; flag anything that looks unfinished.
- `git branch --list` — identify feature branches that suggest in-progress work.
- `git stash list` — any stashed changes.

**If an argument was given**, filter all of the above to that feature or workstream only.

### Step 2 — Build the project map
Synthesise what was read into four lists:

1. **Completed** — features/tasks fully merged and verified.
2. **In progress** — started but not merged/verified; include branch name and last commit.
3. **Blocked** — started but waiting on a dependency, decision, or external factor; include what is blocking.
4. **Not started** — specified but not yet begun, in priority order per specs.

If the lists cannot be determined from existing files, state what is unknown and what information would resolve it.

### Step 3 — Identify the next safe step
Apply this decision tree:

```
Is there uncommitted or stash work?
  → YES: Resume that work first. Commit or discard before starting anything new.

Is there an in-progress branch with no recent commits (>3 days)?
  → YES: Summarise its state. Ask user if it should be resumed, abandoned, or merged as-is.

Is there a blocked item where the block is now resolvable?
  → YES: Propose to unblock it.

Is there a completed feature not yet audited?
  → YES: Propose the relevant audit command (/audit-security, /audit-performance).

Is the next not-started item small enough to complete in one session?
  → YES: Propose it with a brief implementation plan.
  → NO: Propose breaking it down first before starting.

Is the project approaching launch with no /prepare-launch run?
  → YES: Propose running /audit-production then /prepare-launch.
```

**STOP — present the project map and the proposed next step to the user. Confirm before taking any action.** This is the critical decision point: the user may know about context not captured in files (a decision made in a meeting, a scope change, a dependency that just landed).

### Step 4 — Execute the confirmed next step
Once the user confirms the next step:

- **If it is a new feature:** follow the safe build sequence — write/update the spec in `docs/specs/`, write tests first if TDD applies, implement in small commits, verify tests pass.
- **If it is a bug fix:** reproduce the bug in a failing test first, then fix.
- **If it is an audit:** invoke the relevant audit command (`/audit-security`, `/audit-performance`, `/audit-production`).
- **If it is a refactor:** invoke `/refactor-safely`.
- **If it is launch preparation:** invoke `/prepare-launch`.
- **If it is clearing a blocked item:** perform the minimum action to unblock, then re-run this command to re-orient.

Commit progress before ending the session — never leave unstaged work without a WIP commit or stash.

### Step 5 — Update project state
After completing the step (or at the end of the session if interrupted):
1. Update `docs/state/tasks.md` — mark items completed, update in-progress status.
2. If new architectural decisions were made, write an ADR to `docs/decisions/adr-<N>-<slug>.md`.
3. If new risks or assumptions surfaced, append them to `docs/state/assumptions.md`.
4. Commit the state files: `docs(state): update project state after <step>`.

### Step 6 — Report
Produce the Final report (see below).

## Agents used
- `.claude/agents/core/orchestrator.md` — delegates sub-tasks when the next step spans multiple files or services.
- Any domain-specific agent appropriate to the confirmed next step (e.g., `.claude/agents/quality/test-automation-engineer.md` for test work).

## Skills used
- `.claude/skills/requirements-engineering/SKILL.md` — breaks large next steps into safe sub-tasks.
- Any skill appropriate to the confirmed next step (security, performance, refactoring, etc.).

## Expected outputs
| Output | Path |
|---|---|
| Project state summary | printed to session (not written to disk unless user requests) |
| Updated task list | `docs/state/tasks.md` |
| New ADR (if decisions made) | `docs/decisions/adr-<N>-<slug>.md` |
| WIP commit or completed feature commit | git history |

## Stop conditions
- Uncommitted work exists that cannot be safely auto-committed → present diff to user, ask how to handle before proceeding.
- Spec files are missing or empty and no code exists yet → the project may not have started; suggest running `/interview` or `/spec` commands first.
- The next step requires a decision only the user can make (budget, scope, third-party contract) → surface the decision clearly and wait.
- Conflicting signals in state files (task says "done" but branch is unmerged) → flag the conflict, ask user to clarify before proceeding.
- Multiple in-progress branches with no clear priority → list them all, ask user to pick one.

## Final report format
```
## Project State — <date>

**Project:** <name>  |  **Workstream:** <all | specific feature>

### Completed
- ✅ <feature/task> — merged <date>, commit <sha>
- ✅ <feature/task> — ...

### In progress
- 🔄 <feature/task> — branch `<name>`, last commit <sha> (<N> days ago)
  Status: <one sentence on where it stands>

### Blocked
- ⏸ <feature/task> — blocked on: <dependency or decision>
  Unblocked now? <yes/no + reason>

### Not started (prioritised)
1. <task> — <size estimate>
2. <task> — <size estimate>

### Uncommitted / stashed work
- <description or "none">

### Proposed next step
**<Action>** — <one paragraph rationale>

Confirmed by user: ✅ / awaiting confirmation

### Session outcome
- <what was accomplished in this session>
- Next session should start with: <one-line pointer>
```

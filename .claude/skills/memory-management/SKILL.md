---
name: memory-management
description: Use when deciding where information should live across sessions — what belongs in project memory (CLAUDE.md), what belongs in docs-as-long-term-memory (specs, decision records, assumptions, architecture history, known risks), and what belongs in user/global memory. Also covers rehydrating context when resuming work. Triggers on — remember this, where should this go, continue work, /continue-work, lost context, what did we decide, project memory, CLAUDE.md.
---

# Memory Management: What Lives Where, and How to Rehydrate

## When to use
- You learned something durable (a decision, an assumption, a constraint, a risk) and must decide where to record it.
- You are starting a session on an existing project and need to reconstruct prior context.
- `/continue-work` is invoked, or the user asks "where were we / what did we decide".
- Project memory (`CLAUDE.md`) is getting bloated, contradictory, or used as a scratchpad.
- You need to separate project-specific facts from user-wide preferences.

This applies to every project type. The three tiers below are universal; only the contents differ. See `.claude/docs/MEMORY_STRATEGY.md` for the full model.

## Workflow
1. **Classify the information into a tier.**
   - **Project memory** (`.claude/CLAUDE.md` constitution + the repo's own `CLAUDE.md`): durable project *law and conventions* — flow rules, safety constraints, stack conventions, where artifacts live. Short, stable, project-agnostic where possible. Not a log; not a notepad.
   - **Docs as long-term memory** (`docs/`): the project's *evolving record* — specs (`docs/specs/`), architecture (`docs/architecture.md`), decision records (`docs/decisions/`), the assumptions log (`docs/state/assumptions.md`), known risks, and run state (`docs/state/`). This is where the "why" and the history live.
   - **User/global memory** (the user's private global instructions and auto-memory, outside the repo): preferences that span *all* projects — tone, tooling habits, identity. Never put project secrets or project-specific scope here; never copy global preferences into a shared repo.
2. **Write at the moment of decision, not retroactively.** When you pick a database, an auth model, a retention period, or a default — record it immediately. Architectural choices get a decision record from `.claude/templates/decision-record.md`; smaller judgment calls get an entry in `.claude/templates/assumptions-log.md`. Rule of thumb: if a reasonable senior engineer might have chosen differently, log it (`.claude/CLAUDE.md` §7).
3. **Keep each tier clean.** Promote a recurring, stable fact from docs into project memory only once it is truly a convention. Demote stale or one-off notes out of `CLAUDE.md` into a dated doc. Resolve contradictions rather than appending a new contradicting line.
4. **Never store secrets in any memory tier.** Credentials, tokens, and `.env*` contents stay in a secret manager — referenced, never written into `CLAUDE.md`, `docs/`, or global memory (`.claude/CLAUDE.md` §8).
5. **Rehydrate on resume (the continuation workflow).** When `/continue-work` runs, read in order: the project `CLAUDE.md`, then `docs/state/` (run state, active team, assumptions), then the latest specs and decision records, then `git log`/`git status` for what actually changed. Reconstruct *where in the 9-stage flow* the project sits before acting.
6. **Reconcile memory with reality.** If `docs/` claims a feature is done but the code or tests disagree, trust the code, flag the drift, and update the doc. Memory that contradicts the repo is a bug to fix, not a fact to follow.
7. **Surface memory at gates.** Re-present the assumptions log and open decisions at each stage gate so the user can cheaply correct course.

## Standards
- **Do** keep `CLAUDE.md` short, stable, and about rules/conventions; keep history and rationale in `docs/`.
- **Do** record decisions and assumptions immediately, each with alternatives, rationale, blast radius, and reversal.
- **Do** put cross-project preferences in user/global memory and project facts in the repo.
- **Do** write run/continuation state to `docs/state/` so the next session can rehydrate deterministically.
- **Do-not** store secrets, tokens, or `.env` contents in any memory tier.
- **Do-not** use `CLAUDE.md` as a chat log or dumping ground; do-not let it contradict itself.
- **Do-not** copy project-specific scope into global memory, or global preferences into a shared repo.
- **Do-not** trust a doc over the code when they disagree — reconcile and fix the doc.

## Common mistakes to avoid
- Capturing a decision only in chat — if it is not in `docs/` or `CLAUDE.md`, it is lost next session.
- Letting `CLAUDE.md` balloon with transient notes until it is too long to be read fully.
- Recording an assumption with no reversal path, so a wrong call is expensive to undo later.
- Putting an API key or DB URL "temporarily" into a doc or memory file.
- Resuming work from chat scrollback instead of `docs/state/`, and missing a prior decision.
- Treating stale `docs/` as ground truth after the code moved on.

## Output format
A clear placement decision (which tier, which file) and the written artifact: a decision record (`.claude/templates/decision-record.md`) for architectural calls, or an assumptions-log entry (`.claude/templates/assumptions-log.md`) for smaller ones, saved under `docs/`. For continuation, a short "where we are" summary: current flow stage, what changed since last session (from `git` + `docs/state/`), open decisions/assumptions, and the next safe step.

## Related agents
- `.claude/agents/core/orchestrator.md`
- `.claude/agents/core/documentation-writer.md`
- `.claude/agents/core/project-manager.md`

## Related skills/docs/checklists
- `.claude/docs/MEMORY_STRATEGY.md`
- `.claude/skills/documentation/SKILL.md`
- `.claude/templates/decision-record.md`
- `.claude/templates/assumptions-log.md`
- `.claude/commands/continue-work.md`

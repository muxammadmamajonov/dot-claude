# Memory Strategy — what to remember, and where

Claude Code has three memory tiers. Putting information in the wrong tier is the single most
common cause of lost context and contradictory decisions. This document defines the tiers and the
routing rules. Procedure lives in `.claude/skills/memory-management/SKILL.md`.

## The three tiers

| Tier | Lives in | Scope | Lifetime | Examples |
|---|---|---|---|---|
| **Project memory** | `CLAUDE.md` (this `.claude/CLAUDE.md` is the OS constitution; a project may add its own `CLAUDE.md`/`AGENTS.md`) | This repo | As long as the repo | Coding conventions, the 9-stage flow, "always run `/self-test` before committing `.claude/`", stack choices |
| **Docs-as-long-term-memory** | `docs/` in the project | This project, durable & versioned | Forever (git history) | Specs, **decision records**, **assumptions log**, architecture history, known risks, runbooks, audit reports |
| **User / global memory** | `~/.claude/` (user CLAUDE.md, auto-memory) | The person, across all projects | Across projects | The user's role/preferences, "always ask before pushing", cross-project conventions |

## Routing rules — where does this fact go?

- **Is it true for everyone who works in this repo?** → project memory (`CLAUDE.md`).
- **Is it a decision, assumption, risk, or design fact about *this* project?** → `docs/` (a decision
  record, the assumptions log, the architecture doc). This is the durable project brain.
- **Is it about the human (their preferences, their cross-project habits)?** → user/global memory.
- **Is it only relevant to the current task and disposable?** → don't persist it at all.

Rule of thumb: **CLAUDE.md is for *rules*, `docs/` is for *records*, user memory is for *the person*.**
Never write project run-state into the reusable `.claude/` tree — it pollutes the copy-to-next-project
payload (CLAUDE.md §3).

## Docs-as-memory: the canonical artifacts

These are the project's long-term memory. Each has a template:

- **Assumptions log** — `docs/state/assumptions.md` (from `.claude/templates/assumptions-log.md`). Every
  non-trivial decision made on the user's behalf, with alternatives, blast radius, and how to reverse it.
- **Decision records (ADRs)** — `docs/decisions/` (from `.claude/templates/decision-record.md`). The
  architecture-shaping choices and *why*.
- **Architecture history** — `docs/architecture/` evolves; superseded designs stay in git history and are
  referenced by ADRs, so the *why-it-changed* is never lost.
- **Known risks** — tracked in the production-readiness and audit artifacts; P3 backlog items are explicitly
  "tracked, never blocks."
- **Run-state** — `docs/state/project-type.md` (classification), `docs/state/project.md` (live phase/decisions),
  `docs/state/active-team.md` (selected agents), `docs/state/handoffs/` (agent-to-agent handoff notes).

## The continuation workflow

When a session resumes (or context is summarized), the OS rehydrates from `docs/`, not from chat history:

1. `/continue-work` reads `docs/state/project-type.md`, `docs/state/project.md`, `docs/state/assumptions.md`,
   the latest specs, and open decisions/risks.
2. It re-derives the current stage in the 9-stage flow and the active team.
3. It surfaces open assumptions and unresolved business-critical questions before doing new work.

Because the durable memory is on disk, a fresh session — or a teammate, or a headless CI run — can pick up
exactly where the last one stopped. This is why "document the why" (CLAUDE.md §7) is non-negotiable: the
assumptions log and decision records *are* the project's memory.

## Anti-patterns

- **Putting decisions only in chat.** Chat is volatile; summarization can drop detail. Persist to `docs/`.
- **Putting project facts in user/global memory.** They leak into unrelated projects and go stale.
- **Putting volatile run-state in `CLAUDE.md` or `.claude/`.** Breaks portability; pollutes the next project.
- **Re-deriving a past decision.** If it's in `docs/decisions/`, read it — don't re-litigate it.

## Related

- Skill: `.claude/skills/memory-management/SKILL.md`
- Command: `.claude/commands/continue-work.md`
- Templates: `.claude/templates/assumptions-log.md`, `.claude/templates/decision-record.md`, `.claude/templates/runbook.md`
- Constitution: `.claude/CLAUDE.md` §3 (artifacts in `docs/`), §7 (assumptions policy)

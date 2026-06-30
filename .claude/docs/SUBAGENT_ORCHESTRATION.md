# Subagent Orchestration — parallel by default, reconciled by the orchestrator

The orchestrator (`.claude/agents/core/orchestrator.md`) does not do deep work itself; it dispatches
specialists, runs safe work concurrently, and reconciles the results into **one** plan. This document
is the method. It complements the orchestrator's *Concurrency & conflict resolution* section.

## The rule: ownership is singular, timing is parallel

"Exactly one accountable agent per task" governs **ownership** (no dropped handoffs), not **timing**.
Independent tasks should run concurrently to cut wall-clock. The orchestrator's loop:

> **classify → select the minimal active team → dispatch independent work in parallel → collect →
> dedupe → resolve conflicts → emit one plan → advance the gate.**

Never "activate everything." Activate only the active team (`docs/state/active-team.md`, via `/route`).

## What is safe to parallelize

| Stage | Parallel fan-out | Why it's safe |
|---|---|---|
| **Discovery** | `business-analyst` (problem/users) ∥ `solution-architect` (tech-fit spike) ∥ a design agent (UX exploration) | Different `docs/` outputs; no shared write target |
| **Audit (stage 6)** | `security-auditor` ∥ `qa-engineer` ∥ `performance-engineer` ∥ `accessibility-auditor` | Each reads the build, writes its own report |
| **Build** | Two engineering agents on **disjoint** module/file sets | No file overlap (use git worktrees if any risk) |
| **Stack specialists** | Only the ones the preset selected | Scoped to the active team |
| **Audit-style research** | Multiple read-only explorers over different subsystems | Read-only; no mutation |

## What must stay sequential

- The 9-stage flow itself: each gate consumes the prior stage's output.
- Any two tasks that write the **same file** or the **same `docs/` artifact**.
- Anything that mutates shared infrastructure, migrations, or production.
- A verify/review step always runs **after** the thing it reviews.

## Dispatching well

1. **Scope each subagent tightly.** Give it one job, the inputs (paths), and a **structured output format**
   so results are mergeable. Vague prompts produce unmergeable prose.
2. **Hand each the valid-paths context** when they author or edit files, so cross-references resolve and no
   broken links are introduced.
3. **Cap fan-out to the active team and the token budget.** If you drop work for budget, say so — silent
   truncation reads as "covered everything" when it didn't.
4. **Prefer read-only agents for discovery/audit.** They cannot collide and are cheap to run wide.
5. **Isolate parallel writers.** If two agents might edit the same tree, give them separate git worktrees;
   otherwise keep writes sequential.

## Reconciliation — the orchestrator is the sole merge point

When subagents return, the orchestrator (never the user) merges:

1. **Collect** every subagent's structured output.
2. **Dedupe** overlapping findings (same file+line, same issue).
3. **Resolve contradictions by gate ownership** — the accountable agent for that dimension decides
   (a security dispute is settled by `security-auditor`; a perf dispute by `performance-engineer`).
4. **Escalate genuine trade-offs** to a decision record (`.claude/templates/decision-record.md`) and surface
   the business-critical ones to the user.
5. **Emit one reconciled plan.** Never hand the user N conflicting subagent reports — synthesize.

## Adversarial verification (for high-stakes findings)

For audits and security work, verify before trusting. Spawn independent verifiers prompted to **refute** a
finding; keep it only if it survives a majority. Give each verifier a distinct lens (correctness, security,
reproducibility) rather than N identical checks — diversity catches failure modes redundancy can't. This is
how the OS avoids shipping plausible-but-wrong findings.

## Failure handling

- A subagent that dies or returns nothing → its slice is `null`; filter it out, log the gap, and either retry
  or proceed with the gap recorded.
- Rate limits / transient errors → re-dispatch that one slice; do not abandon the whole fan-out.
- Never let one subagent's failure silently shrink the audit scope without a logged note.

## Related

- Orchestrator: `.claude/agents/core/orchestrator.md` (Concurrency & conflict resolution)
- Routing: `.claude/orchestration/routing-matrix.md`, `.claude/commands/route.md`
- Operating model: `.claude/docs/CLAUDE_CODE_OPERATING_MODEL.md`

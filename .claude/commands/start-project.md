---
description: Master entry point — orchestrates the full project lifecycle from idea to launch
argument-hint: [brief idea or project name]
---

# /start-project

## Purpose
Bootstrap the complete project lifecycle for any software type — web app, mobile, desktop, backend API, CLI tool, AI system, IoT firmware, blockchain protocol, SaaS platform, or custom IT solution. Delegates each phase to a specialist command or agent, ensuring nothing is skipped and no destructive actions happen without explicit approval.

## When to use
Run this once at the start of every new project. It is the single entry point that chains all other commands in the correct order. Re-run individual phase commands later to update specific artifacts without redoing everything.

## Workflow

### Phase 0 — Orientation
1. Read `.claude/agents/core/orchestrator.md` to load the orchestration rules.
2. Confirm the working directory is the project root. If no `$PROJECT_ROOT` is set, ask the user to confirm the root path before continuing.
3. Print a one-line summary of each phase so the user knows what to expect.

### Phase 1 — Classify
4. Run `/classify-project` (see `.claude/commands/classify-project.md`).
   - Output: `docs/state/project-type.md` — project category, presets, cross-cutting concerns.
5. **STOP.** Present the classification to the user. Ask: "Does this classification look correct? Any corrections before we continue?" Wait for explicit confirmation.

### Phase 1.5 — Route (Select)
6. Run `/route` (see `.claude/commands/route.md`).
   - Input: `docs/state/project-type.md` (the confirmed classification).
   - Reads the confirmed `docs/state/project-type.md`, then assembles the **minimal active team** (only the agents, skills, and checklists the matched preset + detected cross-cutting concerns require).
   - Output: `docs/state/active-team.md` — the selected agents/skills/checklists for this project. This is CLAUDE.md §2 stage 3 (Select); without it the build phases have no active-team manifest to route against.

### Phase 2 — Discover
7. Run `/interview-founder` (see `.claude/commands/interview-founder.md`).
   - Output: `docs/context/discovery-answers.md` — business goals, users, constraints, metrics, risks.
8. **STOP.** Summarise the discovery answers back to the user. Ask: "Have we captured everything important? Any corrections?" Wait for approval.

### Phase 3 — Specs
9. Run `/create-specs` (see `.claude/commands/create-specs.md`).
   - Output: `docs/specs/product-spec.md`, `docs/specs/feature-specs/`, `docs/specs/business-rules.md`, `docs/specs/roles-permissions.md`.
10. **STOP.** Ask: "Review the specs. Flag anything missing or wrong before we choose the stack."

### Phase 4 — Stack
11. Run `/select-stack` (see `.claude/commands/select-stack.md`).
    - Output: `docs/decisions/stack.md`, one ADR per major choice in `docs/decisions/adr/`.
12. **STOP.** Present the stack decision. Ask: "Any hard constraints (existing vendor lock-in, team expertise, licensing) that should change a choice?"

### Phase 5 — Architecture
13. Run `/design-architecture` (see `.claude/commands/design-architecture.md`).
    - Output: `docs/architecture/overview.md`, component diagrams (Mermaid), integration map, NFR table.

### Phase 6 — Data Model
14. Run `/design-data-model` (see `.claude/commands/design-data-model.md`).
    - Output: `docs/architecture/data-model.md`, ERD (Mermaid), migration strategy, retention policy.
15. **STOP.** Present architecture + data model together. Ask: "Approve to begin roadmap and phased build?"

### Phase 7 — Roadmap
16. Spawn `.claude/agents/core/project-manager.md`. It reads specs, constraints, and the approved stack to produce `docs/roadmap/phases.md` with milestones, dependencies, and risk flags.
17. **STOP.** Ask: "Does the roadmap reflect your budget, team size, and timeline?"

### Phase 8 — Build (iterative)
18. For each roadmap phase, spawn `.claude/agents/core/technical-lead.md`. It works in small, testable increments. Each increment must pass the checklists in `.claude/checklists/qa.md` before the next starts.
19. After each increment: run `.claude/checklists/security.md`, `.claude/checklists/qa.md`, `.claude/checklists/performance.md`, and `.claude/checklists/accessibility.md` (where applicable to project type).
20. **STOP before any database migration or destructive file change.** Show the exact commands and ask for approval.

### Phase 9 — Production Readiness
21. Spawn `.claude/agents/quality/production-readiness-auditor.md`. It verifies environment config, secrets handling, observability, backup strategy, and runbook existence.
22. Output: `docs/ops/production-readiness.md` with a pass/fail per item.
23. **STOP.** All red items must be resolved or explicitly accepted by the user before proceeding.

### Phase 10 — Launch
24. Spawn `.claude/agents/engineering/release-engineer.md`. It coordinates the deployment sequence per the runbook in `docs/ops/runbook.md`.
25. Never run `rm -rf`, force-push, drop databases, or expose secrets. Any such action requires a typed confirmation from the user.

## Agents used
- `.claude/agents/core/orchestrator.md` — session state and phase tracking
- `.claude/agents/core/project-manager.md` — roadmap generation
- `.claude/agents/core/technical-lead.md` — incremental build
- `.claude/agents/quality/production-readiness-auditor.md` — pre-launch audit
- `.claude/agents/engineering/release-engineer.md` — deployment coordination

## Skills used
- `.claude/skills/security/SKILL.md` — applied at every build increment and production readiness
- `.claude/skills/testing/SKILL.md` — test strategy and coverage gates
- `.claude/skills/performance/SKILL.md` — profiling and budget checks
- `.claude/skills/ui-ux-design/SKILL.md` — where the project has a user-facing surface

## Expected outputs
| Path | Description |
|------|-------------|
| `docs/state/project-type.md` | Classification output |
| `docs/state/active-team.md` | Selected agents/skills/checklists (Route output) |
| `docs/context/discovery-answers.md` | Founder interview record |
| `docs/specs/product-spec.md` | Full product spec |
| `docs/specs/business-rules.md` | Business rules |
| `docs/specs/roles-permissions.md` | Role/permission matrix |
| `docs/specs/feature-specs/` | Per-feature spec files |
| `docs/decisions/stack.md` | Stack decision summary |
| `docs/decisions/adr/` | Architecture Decision Records |
| `docs/architecture/overview.md` | Architecture document |
| `docs/architecture/data-model.md` | Data model + ERD |
| `docs/roadmap/phases.md` | Phased roadmap |
| `docs/ops/production-readiness.md` | Readiness checklist results |
| `docs/ops/runbook.md` | Operational runbook |

## Stop conditions
- User has not confirmed the project root.
- Classification is rejected by the user.
- Discovery answers are incomplete (fewer than 5 business questions answered).
- Specs contain unresolved `[DECISION NEEDED]` markers.
- Stack choice violates a hard constraint raised by the user.
- Any roadmap phase has unresolved blocking dependencies.
- Production readiness has red items the user has not explicitly accepted.
- Any command proposes a destructive action (drop, force-push, `rm -rf`, secret exposure).

## Final report format
```
## /start-project — Session Summary

**Project:** <name>
**Type:** <classification from project-type.md>
**Stack:** <one-line summary>
**Phases completed:** <list with ✓/✗>
**Files created:** <count>
**Open decisions:** <any [DECISION NEEDED] markers remaining>
**Next step:** <exact command or manual action required>
```

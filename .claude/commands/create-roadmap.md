---
description: Break scope into small safe phases with milestones, dependencies, and a clear MVP cut
argument-hint: [project or epic name]
---

# /create-roadmap

## Purpose
Convert product specs and design briefs into a phased delivery roadmap: a minimal MVP cut, ordered build phases, explicit dependencies between work items, milestone definitions, and risk flags — so the team always knows what to build next and why.

## When to use
- After `/interview-founder` and at least a draft of `docs/specs/product-spec.md` exist
- Before kicking off `/build-prototype` or the first `/implement-feature`
- When replanning after a major scope change or pivot
- When the argument is omitted, scope to the full product

## Workflow

**Step 1 — Load and validate inputs** (orchestrator: `.claude/agents/core/orchestrator.md`)
- Read `docs/specs/product-spec.md`, `docs/architecture/overview.md`, `docs/specs/ui-ux-brief.md` (if present)
- Extract: feature list, user personas, non-functional requirements (performance, security, compliance), known constraints (deadline, team size, budget, platform)
- If product spec is missing or incomplete, halt and ask the user to run `/interview-founder` first

**Step 2 — Enumerate all work items**
List every discrete deliverable implied by the spec:
| ID | Work item | Type (feature/infra/design/test/ops) | Estimated size (S/M/L/XL) | User-facing? |
- Include: data models, auth, third-party integrations, background jobs, observability, CI/CD pipeline, deployment, documentation
- Do NOT include items with no spec basis — note any gaps

**Step 3 — Identify dependencies**
For each work item from Step 2, list:
- Hard blockers (cannot start until X is done)
- Soft dependencies (easier after X, but parallelisable)
- External dependencies (third-party API keys, design assets, legal approval, infrastructure provisioning)
Build a dependency graph summary (text DAG or table).

**Step 4 — Define MVP cut**

STOP — business-critical decision #1
Present the full work-item list and dependency graph to the user. Ask:
1. Which features are non-negotiable for a first working version?
2. What is the target date or budget constraint for MVP?
3. Are there regulatory, security, or compliance items that must be in MVP regardless of user value?

Wait for explicit answers before proceeding.

**Step 5 — Assign phases**
Using the MVP cut and dependency order, define phases:

- **Phase 0 — Foundation**: repo scaffold, CI/CD, local dev environment, auth skeleton, core data model, observability hooks. No user-facing features. Duration: 1–3 days typical.
- **Phase 1 — MVP Walking Skeleton**: the thinnest end-to-end path that delivers the single highest-value user journey. All integrations stubbed or mocked. Tests for the critical path.
- **Phase 2 — MVP Complete**: remaining MVP features, real integrations replacing stubs, error states, basic security hardening, accessibility pass, performance baseline.
- **Phase 3 — Hardening**: load testing, penetration testing or security audit, accessibility audit, monitoring/alerting in production, runbook, backup/recovery verified.
- **Phase 4+ — Post-MVP iterations**: features deferred from MVP, v2 capabilities, platform expansion. Each phase gets its own milestone definition.

Rules for phase assignment:
- No phase > 2 weeks of estimated work (split if larger)
- Every phase ends with something demonstrably working
- Destructive or irreversible actions (schema drops, key rotations, DNS cutover) always get their own step inside a phase, never bundled

**Step 6 — Define milestones**
For each phase boundary, write a milestone acceptance checklist:
- Specific, binary pass/fail criteria (not "mostly done")
- Who signs off (human role, not agent)
- What regression tests must be green

**Step 7 — Surface risks**
List the top 5–8 delivery risks:
| Risk | Likelihood (H/M/L) | Impact (H/M/L) | Mitigation |
Common risks: unclear requirements, external API instability, team capacity, infrastructure lead time, security review timeline, scope creep.

**Step 8 — Write outputs**
- Write `docs/roadmap/phases.md` with phases, milestones, dependency table, and risk register
- Update `docs/specs/product-spec.md` with MVP scope annotation

STOP — business-critical decision #2
Present the phased roadmap to the user. Ask:
1. Do the phase boundaries and milestone definitions look correct?
2. Are the risk mitigations acceptable?
3. Any re-prioritisation before work begins?

## Agents used
- `.claude/agents/core/orchestrator.md` — coordinates all steps
- `.claude/agents/core/project-manager.md` — phase and dependency analysis (if present)

## Skills used
- `.claude/skills/requirements-engineering/SKILL.md` (if present)
- `.claude/checklists/security.md` — ensures security items land in the right phase
- `.claude/checklists/performance.md` — ensures performance items are scheduled

## Expected outputs
| File | Status |
|------|--------|
| `docs/roadmap/phases.md` | created / updated |
| `docs/specs/product-spec.md` | updated (MVP annotation) |

## Stop conditions
- No product spec exists — halt, ask user to run `/interview-founder`
- MVP cut cannot be determined from spec alone — halt at decision #1, do not guess
- Any phase exceeds 2 weeks of estimated work — split before writing output
- External dependencies (legal, compliance, third-party contracts) are unresolved — flag as blockers, do not schedule around them silently

## Final report format
```
## Roadmap — [project or epic name]

### Work items: N total | N in MVP | N deferred
### Phases: N (Phase 0 through Phase N)
### Estimated MVP: [size range, e.g. 3–5 weeks]
### Dependencies: N hard blockers identified | N external
### Risks: N flagged (H: N, M: N, L: N)

### Phase summary
| Phase | Goal | Items | Milestone gate |
|-------|------|-------|---------------|
| 0     | Foundation | N | CI green, local env reproducible |
| 1     | MVP skeleton | N | Happy path E2E passes |
| 2     | MVP complete | N | All MVP acceptance criteria pass |
| 3     | Hardening | N | Security + load + a11y audits pass |

### Files written
- docs/roadmap/phases.md
- docs/specs/product-spec.md (updated)

### Open decisions
- [any unresolved items]

### Next step
Run /build-prototype to validate the Phase 1 skeleton
```

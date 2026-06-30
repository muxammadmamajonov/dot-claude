---
description: Implement one feature in small safe steps with tests, following the spec and project conventions
argument-hint: [feature name]
---

# /implement-feature

## Purpose
Implement a single specified feature end-to-end in small, independently-reviewable steps. Each step leaves the codebase in a working, tested, and committable state. The feature must match its spec, follow project conventions, pass all tests, and be ready for `/review-feature`.

## When to use
- After the feature has a written spec in `docs/specs/` and appears in `docs/roadmap/phases.md`
- After the walking skeleton from `/build-prototype` exists (or Phase 0 scaffold at minimum)
- One feature at a time — do not batch multiple features in a single run
- The argument must name the feature explicitly; if omitted, list unimplemented roadmap features and ask which to build

## Workflow

**Step 1 — Load and validate context** (orchestrator: `.claude/agents/core/orchestrator.md`)
- Read `docs/specs/product-spec.md`, `docs/roadmap/phases.md`, `docs/architecture/overview.md`, `docs/specs/ui-ux-brief.md`
- Locate the feature spec section (or a dedicated spec file in `docs/specs/feature-specs/[feature-name].md`)
- Confirm the feature is in scope for the current roadmap phase
- List all acceptance criteria from the spec as a checklist — every criterion must be met before the feature is considered done
- Read project conventions: linting config, test framework, folder structure, naming patterns (infer from existing code if no explicit doc)

STOP — if the feature has no written spec or acceptance criteria, halt and ask the user to define them before proceeding.

**Step 2 — Break into implementation steps**
Decompose the feature into ordered, atomic steps. Each step must:
- Be completable in one focused session
- Leave the codebase compiling and tests passing
- Produce a logical git commit unit

Typical step order:
1. Data model changes (schema migration, type definitions, interfaces)
2. Repository / data-access layer
3. Core business logic (pure functions, domain services)
4. Integration points (external API calls, message publishing, file I/O)
5. Application layer (controllers, resolvers, CLI commands, event handlers)
6. UI layer (if applicable: components, screens, views)
7. Tests for each layer (written alongside or immediately after each layer — never deferred)
8. Error states, edge cases, validation
9. Observability (structured log statements, metrics, traces at key points)
10. Documentation updates (inline, README, or API docs)

Present the step breakdown to the user and confirm before writing code.

**Step 3 — Implement each step**

For every step:
- Write the implementation code
- Write tests immediately (unit tests for logic, integration tests for I/O boundaries)
- Run the test suite; all existing tests must stay green
- Check for: hardcoded secrets, unsafe file operations, missing input validation, SQL injection, unhandled promise rejections / panics
- No `rm -rf`, no dropping tables, no force-pushes, no irreversible operations without an explicit human approval comment in the code

Conventions to enforce:
- Follow the naming, folder, and import conventions already present in the codebase
- Use the dependency-injection pattern already established (do not introduce a new DI approach)
- Errors must surface to callers — never silently swallowed
- All public interfaces must have types / signatures (TypeScript, Python type hints, Go interfaces, etc.)

**Step 4 — Integrate and wire up**
- Connect the new layers to the application entry point (route registration, CLI command registration, event subscription, etc.)
- Confirm the feature is reachable end-to-end in the local environment
- Update `.env.example` if new environment variables were introduced

**Step 5 — Run the full test suite**
- Execute all unit, integration, and (if available) E2E tests
- Zero test failures permitted before marking the feature complete
- If a pre-existing test fails due to this feature's changes, fix the test or the code — do not skip or comment out

**Step 6 — Self-review checklist**
Before declaring done, verify:
- [ ] All spec acceptance criteria are met
- [ ] No hardcoded secrets or credentials
- [ ] All new code has test coverage
- [ ] Input validation on all external inputs (HTTP, CLI args, file uploads, messages)
- [ ] Error messages do not leak stack traces or internal paths to end users
- [ ] Observability: at least one structured log per significant state transition
- [ ] UI changes pass a basic accessibility check (keyboard navigable, labels present, contrast)
- [ ] No console.log / print debug statements left in
- [ ] API or interface changes are reflected in relevant docs

**Step 7 — Write implementation notes**
Append to `docs/specs/feature-specs/[feature-name].md` (create if absent):
- Actual implementation decisions that deviated from spec and why
- Known limitations or deferred edge cases (link to roadmap item)
- Any tech debt introduced (label with `# TODO:` and reason)

STOP — business-critical decision
Present the completed feature, test results, and implementation notes. Ask:
1. Does the implementation match the intended behavior?
2. Are there edge cases or user scenarios not covered that need handling before review?

## Agents used
- `.claude/agents/core/orchestrator.md` — coordinates steps, tracks checklist
- `.claude/agents/engineering/fullstack-engineer.md` — code generation per layer (if present)
- `.claude/agents/quality/qa-engineer.md` — test authoring (if present)

## Skills used
- `.claude/skills/security/SKILL.md` — secure defaults, input validation, secret handling
- `.claude/checklists/security.md`
- `.claude/checklists/accessibility.md` (for UI features)
- `.claude/checklists/performance.md` (for data-intensive features)

## Expected outputs
| Artefact | Status |
|----------|--------|
| Feature implementation code (all layers) | created |
| Unit tests | created, green |
| Integration tests | created, green |
| Updated `.env.example` (if new vars) | updated |
| `docs/specs/feature-specs/[feature-name].md` | created / updated |
| All pre-existing tests | still green |

## Stop conditions
- No spec or acceptance criteria exist for the feature — halt before Step 2
- A step cannot be completed without a destructive action (drop migration, key rotation, DNS change) — halt, ask for explicit human approval with description of impact
- The test suite cannot be made green — halt, document the blocker in the feature spec, do not mark complete
- A required external service or credential is unavailable — stub it and document the gap

## Final report format
```
## Feature implemented — [feature name]

### Acceptance criteria: N/N met
### Steps completed: N
### Tests: N unit | N integration | N E2E — all green
### Pre-existing tests: all green | N regressions (details below)

### Layers touched
- [ ] Data model
- [ ] Data access / repository
- [ ] Business logic
- [ ] Integration / external
- [ ] Application layer
- [ ] UI layer
- [ ] Observability

### Deviations from spec
- [bullet per deviation with rationale]

### Tech debt introduced
- [bullet per TODO with file:line reference]

### Files created / modified
- [list with paths]

### Next step
Run /review-feature [feature name]
```

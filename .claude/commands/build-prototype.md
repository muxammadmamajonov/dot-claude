---
description: Stand up a thin vertical slice / walking skeleton that proves the riskiest path end to end
argument-hint: [feature or integration name]
---

# /build-prototype

## Purpose
Build the thinnest possible end-to-end vertical slice — a "walking skeleton" — that exercises every layer of the stack (input → logic → persistence → output) for the single highest-risk user journey. The goal is to prove feasibility and uncover integration surprises before committing to full implementation.

## When to use
- After `docs/specs/roadmap.md` Phase 0 (Foundation) is complete
- When a new integration, algorithm, or architecture pattern is unproven
- Before `/implement-feature` begins Phase 2 work
- When the argument names a specific risky path (e.g. "payment flow", "ML inference pipeline", "real-time sync")
- NOT for polished UI, complete error handling, or production hardening — that belongs in `/implement-feature`

## Workflow

**Step 1 — Identify the riskiest path** (orchestrator: `.claude/agents/core/orchestrator.md`)
- Read `docs/specs/roadmap.md`, `docs/specs/architecture.md`, `docs/specs/product.md`
- List candidates for the walking skeleton: flows that cross the most architectural boundaries, depend on third-party integrations, involve novel algorithms, or have the most unknowns
- Select one path. If the argument names a specific path, use that.

STOP — business-critical decision #1
Present the selected path and the rationale for choosing it. Ask:
1. Is this the correct path to validate first?
2. Are there integration credentials, API keys, or environment variables needed that aren't yet in `.env.example`?
3. Should the prototype be throwaway (spike) or form the foundation of production code?

Do not write any code until the user confirms.

**Step 2 — Scaffold the skeleton**
- If Phase 0 scaffold doesn't exist: create the minimal project structure (entry point, config loader, dependency manifest, `.env.example`, basic CI config) following `.claude/stack-matrix/` for the chosen stack
- Keep scope strictly to the chosen path — do not add features, screens, or endpoints not needed to prove this path
- Create stub/mock implementations for every external dependency (third-party API, database, message queue, hardware) so the path can run locally without real credentials

**Step 3 — Implement the path, layer by layer**
Work in this order to surface integration issues early:
1. Data model / schema for the entities on this path only
2. Core logic (service/domain layer) with no I/O dependencies
3. Persistence layer (real or in-memory stub per decision #1)
4. External integrations (call real API if credentials available, otherwise use recorded fixture)
5. Entry point (HTTP handler, CLI command, message consumer, UI screen — whichever applies to the project type)

Rules:
- Every function that does I/O must be behind an interface/abstraction so it can be swapped
- No secrets in code; read from environment or config
- No `rm -rf`, no irreversible migrations, no production data touches

**Step 4 — Write a smoke test**
- One automated test that exercises the full path end-to-end using stubs/mocks for external dependencies
- Test must be runnable with a single command documented in `README` or `CONTRIBUTING`
- Test must pass before Step 5

**Step 5 — Document findings**
Write `docs/specs/prototype-findings.md`:
- What was built and what was explicitly left out
- Integration surprises, latency observations, schema changes needed
- Assumptions that need validation with real data or real credentials
- Recommended changes to architecture or roadmap before full implementation

**Step 6 — Verify**
- Run the smoke test; confirm it is green
- Manually walk through the path using the stub environment
- Check that no secrets, credentials, or environment-specific values are hardcoded

STOP — business-critical decision #2
Present prototype-findings.md. Ask:
1. Does this prototype confirm the approach, or does the architecture need revision?
2. Should any stubs be replaced with real integrations before `/implement-feature` begins?
3. Any changes to the roadmap based on what was discovered?

## Agents used
- `.claude/agents/core/orchestrator.md` — coordinates all steps
- `.claude/agents/engineering/fullstack-engineer.md` — code generation per layer (if present)
- `.claude/agents/quality/qa-engineer.md` — smoke test authoring (if present)

## Skills used
- `.claude/skills/security/SKILL.md` — no secrets in code, safe defaults
- `.claude/checklists/architecture.md` (if present)

## Expected outputs
| File / artefact | Status |
|-----------------|--------|
| Project scaffold (entry point, config, deps) | created |
| Data model for path entities | created |
| Core logic for path | created |
| External integration stubs | created |
| Smoke test | created, green |
| `docs/specs/prototype-findings.md` | created |
| `.env.example` | created / updated |

## Stop conditions
- Phase 0 scaffold does not exist and stack is undefined — halt, resolve stack first
- Required API credentials unavailable and no fixture strategy agreed — halt at decision #1
- Smoke test cannot be made green in the prototype scope — document the blocker, do not silently skip
- User specifies "throwaway spike" at decision #1 — mark all files with a `# SPIKE — do not promote` header and do not connect to production code paths

## Final report format
```
## Prototype — [path name]

### Path validated: [one-line description of the flow]
### Layers built: [data model | logic | persistence | integration | entry point]
### Stubs: N external dependencies stubbed
### Smoke test: PASS | FAIL (with reason)
### Surprises: N integration issues found

### Key findings
- [bullet per discovery that affects roadmap or architecture]

### Files created
- [list with paths]

### Prototype status: FOUNDATION | THROWAWAY SPIKE

### Next step
Run /implement-feature [feature name] to build Phase 2 on this skeleton
```

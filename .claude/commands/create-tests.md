---
description: Design and write the test strategy and tests (unit/integration/e2e) for a feature or the system
argument-hint: [feature name | "system"]
---

# /create-tests

## Purpose
Design a complete, layered test strategy for a feature or the full system, then write the tests: unit tests for logic, integration tests for I/O boundaries, and end-to-end tests for critical user journeys. Every test must be deterministic, independently runnable, and tied to a specific acceptance criterion or risk.

## When to use
- During or after `/implement-feature` to add missing coverage
- After `/build-prototype` to formalise the smoke test into a proper suite
- When the argument is `"system"`, create or update the full test strategy for the project
- When the argument names a feature, scope to that feature only
- When a `/review-feature` finding cites insufficient test coverage

## Workflow

**Step 1 — Load context** (orchestrator: `.claude/agents/core/orchestrator.md`)
- Read `docs/specs/feature-specs/[feature-name].md` (or `docs/specs/product-spec.md` for system scope) for acceptance criteria
- Read `docs/architecture/overview.md` for layer boundaries and integration points
- Read `docs/roadmap/phases.md` to understand which risks are highest priority to cover
- Identify existing test framework, test runner, and conventions by reading `package.json` / `pyproject.toml` / `go.mod` / equivalent and any existing test files
- List all existing tests and their coverage scope to avoid duplication

**Step 2 — Define test strategy**
Write a test strategy section covering:

| Layer | What to test | Tool/framework | Target coverage |
|-------|-------------|----------------|-----------------|
| Unit | Pure functions, domain logic, validation rules, utilities | [project's unit test tool] | Every branch of business logic |
| Integration | DB queries, external API calls, message publish/consume, file I/O | [project's integration tool] | Every I/O contract at the boundary |
| E2E / contract | Full user journeys from entry point to persistence | [project's E2E tool] | Every acceptance criterion and error path |
| Performance | Throughput and latency of critical operations | benchmark/load tool (if present) | Baseline established; regression gate defined |
| Accessibility | Screen-reader, keyboard, contrast (UI projects only) | axe-core / pa11y / equivalent | WCAG 2.2 AA on every new screen |

Rules:
- No test may depend on another test's state (setup/teardown per test)
- No test may call a live third-party service — use recorded fixtures or mocks
- No test may use a production database or bucket — use a test-scoped instance or in-memory substitute
- Flaky tests (network timeouts, timing-sensitive) are not acceptable; use deterministic waits and mocks

STOP — business-critical decision
Present the test strategy to the user. Ask:
1. Are there user journeys or risk areas not represented in this strategy?
2. Is there an existing coverage threshold or CI gate that must be maintained?
3. Are there any integration environments (staging DB, sandbox API) pre-provisioned for integration tests?

**Step 3 — Write unit tests**
For each business-logic function or module in scope:
- Identify: happy path, all error/exception paths, boundary values, known edge cases from spec
- Write one `describe` / `suite` block per module; one `it` / `test` per scenario
- Assertions must be specific — test the actual returned value, not just that a function ran
- Mock all I/O at the function boundary; unit tests must run with no network or disk access

**Step 4 — Write integration tests**
For each I/O boundary (database, external HTTP, message queue, file system, cache):
- Write tests that call the real implementation against a test-scoped resource (in-memory DB, local container, recorded HTTP fixture via VCR/nock/httpretty/equivalent)
- Cover: successful round-trip, connection failure, timeout, malformed response, transaction rollback
- Teardown must leave the test resource in a clean state after every test

**Step 5 — Write end-to-end / acceptance tests**
For each acceptance criterion in the spec:
- Write one E2E test that exercises the full path from the entry point (HTTP request, CLI invocation, UI interaction, message publish) through to the observable output (response body, exit code, UI state, persisted record)
- Cover the happy path and the two highest-impact failure paths per criterion
- For UI: use the project's E2E browser tool (Playwright, Cypress, WebdriverIO, etc.); for API: use HTTP client assertions; for CLI: subprocess invocation with stdout/stderr assertions

**Step 6 — Write performance baselines** (skip if no performance requirement in spec)
- Identify the 1–3 operations where latency or throughput matters
- Write a benchmark test that records the baseline and fails if it regresses beyond an agreed threshold (e.g. p95 > 500ms)
- Document the threshold in the test file with a comment linking to the spec requirement

**Step 7 — Write accessibility tests** (skip if no UI)
- Add axe-core (or platform equivalent) assertions to each E2E test that renders a new screen
- Assert zero violations at impact level "critical" and "serious"
- Add keyboard-navigation tests for all interactive flows: tab order, enter/space activation, escape to close

**Step 8 — Integrate with CI**
- Confirm tests run with a single command (e.g. `npm test`, `pytest`, `go test ./...`)
- Update CI config (`.github/workflows/`, `.gitlab-ci.yml`, `buildkite.yml`, etc.) to run the full suite on every pull request
- Ensure integration and E2E test jobs use isolated, reproducible environments (containers, seeded test DB)
- Set the coverage threshold gate in CI if the project uses coverage reporting

**Step 9 — Write test documentation**
Append to or create `docs/specs/test-strategy.md`:
- Strategy table from Step 2
- How to run each test layer locally (exact commands)
- How to add new tests (naming conventions, file locations, fixture management)
- Known gaps and the rationale for leaving them (e.g. "E2E for admin panel deferred to Phase 3")

## Agents used
- `.claude/agents/core/orchestrator.md` — coordinates steps and layer sequencing
- `.claude/agents/quality/qa-engineer.md` — test authoring and coverage analysis (if present)

## Skills used
- `.claude/skills/testing/SKILL.md` (if present)
- `.claude/checklists/accessibility.md` — Step 7 assertions
- `.claude/checklists/performance.md` — Step 6 thresholds

## Expected outputs
| Artefact | Status |
|----------|--------|
| Unit test files (per module) | created / updated |
| Integration test files (per boundary) | created / updated |
| E2E / acceptance test files (per criterion) | created / updated |
| Performance benchmark tests (if applicable) | created |
| Accessibility test assertions (if UI) | created |
| CI config updated | updated |
| `docs/specs/test-strategy.md` | created / updated |

## Stop conditions
- No test framework configured and none can be inferred from the project — halt, ask user to choose and install one before proceeding
- A live production service is the only option for integration testing — halt, require a safe alternative (mock, sandbox, test account) before writing tests that call it
- Coverage of an acceptance criterion is impossible without accessing production data — document as a known gap; do not write tests that touch production

## Final report format
```
## Test suite — [feature name | system]

### Tests written
| Layer | New tests | Total in suite |
|-------|-----------|---------------|
| Unit | N | N |
| Integration | N | N |
| E2E / acceptance | N | N |
| Performance | N | N |
| Accessibility | N | N |

### Acceptance criteria covered: N/N
### Known gaps: N (see docs/specs/test-strategy.md)

### All tests: PASS | N failing (list)

### CI updated: yes | no (reason)

### Files created / modified
- [list with paths]

### Next step
Run /review-feature [feature name] if not yet done, or /fix-bugs if any tests are red
```

# QA Checklist
Passing this gate proves the build is tested to an extent that gives confidence to ship — known paths are exercised, regressions are caught automatically, and CI enforces quality on every merge. Severity tiers: P0=blocker, P1=important (fix shortly after launch), P2=hardening, P3=post-launch / backlog (track and revisit; never blocks shipping).

## P0 — Blockers (must pass before merging / releasing)

- [ ] All unit tests pass with zero failures across the full suite (`npm test`, `pytest -x`, `go test ./...`, `cargo test`, `flutter test`, or equivalent for the project's stack) on the current commit in a clean environment.
- [ ] Integration tests covering all critical paths pass in CI: authentication and session management, authorization enforcement (role boundaries, ownership checks), payment or financial transaction flows, data mutation operations (create/update/delete), and all external API calls via contract tests or recorded responses.
- [ ] No known regressions: every test that passed on the last release tag still passes. A failing test that previously passed is a build-blocker until root-caused and fixed — not skipped.
- [ ] End-to-end smoke test exercises the primary user workflow from cold start to value moment without error: sign-up or login, core action, data persistence, and visible confirmation. Must pass against an environment that mirrors production config.
- [ ] All public API contracts have corresponding contract tests or schema-validated stubs (Pact, Dredd, OpenAPI request/response validation, GraphQL schema enforcement). Contracts are versioned and checked against real sandbox responses, not stale recorded responses.
- [ ] Boundary, negative-input, and malformed-input tests exist for every endpoint or function that accepts external data: empty values, null, max-length strings, Unicode edge cases (emoji, RTL characters, zero-width characters), negative numbers where positive is expected, and type coercion attacks (string "0" vs. integer 0).
- [ ] No test is unconditionally skipped (`xit`, `@pytest.mark.skip`, `t.Skip(...)`, `xtest(`, `xit(`) without a linked issue number in the skip annotation explaining the reason and an owner responsible for re-enabling it.
- [ ] CI gate is mechanically enforced: PRs cannot be merged when any test job is red. This is a branch-protection setting, not a convention.
- [ ] Security-sensitive test scenarios pass: authentication bypass attempts, authorization boundary violations (horizontal and vertical privilege escalation), SQL/NoSQL injection in all user-supplied fields, mass-assignment attempts on model fields, and CSRF protection where applicable. Reference `../checklists/security.md` for the full list.
- [ ] All tests are deterministic and environment-independent: tests do not depend on execution order, real-time clocks (use fake timers), random seeds (fixed seed or mocked), external network calls (mocked/stubbed), or shared mutable global state.

## P1 — Important (fix before scaling / shortly after launch)

- [ ] Line coverage meets the project's agreed threshold — recommended ≥ 80% for business-logic modules, ≥ 60% overall — measured on CI and trended over sprints. Coverage below threshold is a P1 debt item with an owner.
- [ ] Branch and condition coverage is measured, not just line coverage. Decision points (if/else, switch, ternary, try/catch) have tests for each branch where the branch represents business logic.
- [ ] Mutation testing score (Stryker, PITest, mutmut, or equivalent) is above 60% for critical modules (auth, billing, data-access layer). A high line-coverage score with a low mutation score means tests exist but don't assert meaningfully.
- [ ] Flaky tests are tracked in a dedicated label or issue tag. No test has been flaky more than twice in any rolling two-week window without a written investigation and resolution plan. Chronically flaky tests are either fixed or removed.
- [ ] Load and stress tests have been executed against a staging environment that matches production specs (same instance size, same DB engine, same cache config): p95 latency under expected peak load is within the SLA, and the system degrades gracefully under 2× and 5× peak load rather than crashing.
- [ ] All third-party API stubs and recorded fixtures are verified against current vendor sandbox responses — not stale recordings from more than 30 days ago. API versioning changes are checked.
- [ ] Total regression suite runtime is ≤ 15 minutes in CI. Suites exceeding this threshold must be parallelized or split into unit/integration/e2e tiers with separate triggers. Slow tests are profiled and optimized.
- [ ] Test data management is clean: factories and fixtures create isolated datasets per test run; tests do not read from or write to shared mutable fixtures; database state is reset between integration test runs (transactions rolled back or DB recreated).
- [ ] Error handling paths are tested explicitly: every `catch` block, every error response path, and every fallback behavior has at least one test that deliberately triggers the failure condition.

## P2 — Hardening / nice-to-have

- [ ] Property-based tests (Hypothesis, fast-check, go-fuzz, proptest, or equivalent) cover core parsing, validation, serialization, and business-rule logic — inputs are generated, not hand-crafted, to find edge cases a human would not invent.
- [ ] Visual regression tests (Chromatic, Percy, Playwright screenshot diffing, or equivalent) are configured for UI components and key screens; failures require human sign-off before merge, not automatic acceptance.
- [ ] Test pyramid is balanced: unit tests outnumber integration tests; integration tests outnumber E2E tests. A test suite that is mostly E2E tests is slow, fragile, and does not provide fast feedback.
- [ ] Snapshot tests are reviewed intentionally when they update: a bulk `--updateSnapshot` or `--update-snapshots` without reading the diff is treated as a failed QA step.
- [ ] Chaos and fault-injection tests verify graceful degradation: upstream timeout, upstream 500-error cascade, message queue unavailability, database read-replica lag, disk full, and memory pressure each have a scenario that verifies the system's defined degraded-mode behavior.
- [ ] Test execution metrics (pass rate, suite runtime, flakiness rate) are tracked in a dashboard or CI artifact over time so regressions in test health are visible before they become merge-blockers.

## P3 — Post-launch / backlog (track and revisit after launch; never blocks shipping)

- [ ] Contract test suite is expanded to cover all downstream consumer services, not just the primary integration; Pact broker or schema registry stores versioned contracts so breaking changes surface before deploy, not in production incidents.
- [ ] Test-coverage trend is charted over the past 90 days; modules whose coverage has declined by ≥ 5 percentage points are flagged in the next sprint retrospective with an assigned owner for remediation.
- [ ] Mutation testing is extended to all business-logic modules (not just auth and billing); mutation score target raised to ≥ 75% for critical modules, and the results are posted as a CI artifact on every release branch.
- [ ] Regression suite runtime is profiled and restructured: tests exceeding 500 ms individually are identified, and the 10 slowest are either optimized or moved to a nightly scheduled run rather than blocking every PR merge.
- [ ] A dedicated test-environment provisioning pipeline (ephemeral per-branch databases, seed data, and service stubs) is in place so integration tests always run against a fresh, isolated state without manual reset between runs.
- [ ] Test-quality retrospective is scheduled quarterly: flakiness rate, mutation score, coverage trend, and CI failure-to-merge ratio are reviewed and targets for the next quarter are set and owned.

## How to use
Run via `../agents/quality/qa-engineer.md` or `../agents/quality/test-automation-engineer.md` at the quality gate phase for every feature branch before merge and for every release candidate before launch. Invoke via `../commands/create-tests.md` (to write tests) or `../commands/review-feature.md` (to verify an existing feature). Cross-reference `../checklists/security.md` for security-specific test items and `../checklists/performance.md` for load-test thresholds. CI invocation examples:

```sh
# JS/TS
npm run test:ci

# Python
pytest --tb=short -q --cov=src --cov-fail-under=80

# Go
go test ./... -race -count=1

# Rust
cargo test -- --test-threads=1
```

Reviewer marks each item `[x]` when satisfied or `[-]` when explicitly waived with a written reason, risk rating, and a linked remediation ticket with an owner.

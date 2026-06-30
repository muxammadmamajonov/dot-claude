---
name: testing
description: Use when defining or building a test strategy, choosing what to test at which layer, raising meaningful coverage, or fixing a flaky/failing suite. Triggers when implementing any feature (write tests with it, not after), when a bug is found (write the failing test first), and during the QA audit phase before launch.
---

# Testing: Layered Strategy with Meaningful Coverage

## When to use
- Implementing a feature or fixing a bug (tests are part of the change, not a follow-up).
- Standing up a test strategy for a new project or component.
- Coverage is low, the suite is flaky, or regressions keep slipping through.
- Running the QA audit phase before production readiness.

Applies to any project type. The layers map differently (a CLI's "e2e" is invoking the binary; an API's is hitting endpoints; a game's may be deterministic simulation) but the pyramid logic holds.

## Workflow
1. **Derive test cases from the spec.** Turn each acceptance criterion into one or more concrete cases. Add the obvious failure/edge cases: empty, max, boundary, invalid, concurrent, unauthorized. Reference `.claude/templates/product-spec.md`. **First, detect the existing runner** with the bundled script `python3 .claude/skills/testing/scripts/detect_test_runner.py <repo>` (add `--json`) so the plan targets the runner the project actually uses (vitest/jest/mocha/playwright/pytest/unittest/go test/cargo test/rspec/minitest/pest/phpunit/dotnet test) and its run command — or, if it reports none, propose one appropriate to the stack via `.claude/stack-matrix/testing.md`. Verifiable behaviour is pinned by `evals/evals.json` beside the script.
2. **Choose the layer per case (test pyramid).** Most logic → fast unit tests. Interactions across modules/services/DB → integration tests. A few critical user journeys → end-to-end. Push tests as low as they can meaningfully live.
3. **Write the failing test first for bugs and TDD-friendly logic.** Confirm it fails for the right reason, then implement until green. For exploratory work, characterize behavior with tests as it stabilizes.
4. **Make tests deterministic and isolated.** Control time, randomness, network, and IDs. Each test sets up and tears down its own state; no ordering dependencies; no shared mutable fixtures.
5. **Cover the non-functional cases that matter.** Authorization-denied paths (with `.claude/skills/security/SKILL.md`), accessibility checks for UI (`.claude/checklists/accessibility.md`), and a thin performance/load smoke for hot paths (`.claude/skills/performance/SKILL.md`).
6. **Measure coverage as a guide, not a goal.** Track line + branch coverage; investigate untested branches in critical code. Prioritize coverage of business-critical and security-critical paths over chasing a global percentage.
7. **Wire into CI.** Tests run on every PR, fast suite as a merge gate, full/e2e suite on main or nightly. Fail the build on new failures and on coverage regressions in critical packages. See `.claude/skills/devops/SKILL.md`.
8. **Maintain.** Quarantine and fix flakes promptly (a flake is a bug). Delete obsolete tests. Keep the suite fast enough that people actually run it.

## Standards
- **Do** test behavior and public contracts, not private implementation details, so tests survive refactors.
- **Do** follow Arrange–Act–Assert; one logical assertion focus per test; descriptive names stating the scenario and expectation.
- **Do** keep unit tests fast (milliseconds) and hermetic — no real network, clock, or filesystem unless that is the unit under test.
- **Do** use real collaborators where cheap; mock only at true boundaries (network, time, third-party, payment, email).
- **Do** add a regression test for every bug fixed, reproducing the bug first.
- **Do** test the unhappy paths: errors, timeouts, retries, permission denials, malformed input.
- **Do** make e2e tests few, stable, and focused on critical journeys; everything else lives lower.
- **Do-not** assert on incidental output (exact log strings, ordering of unordered collections, timestamps) unless that is the contract.
- **Do-not** chase 100% coverage with trivial getter tests while leaving complex branches untested.
- **Do-not** let flaky tests stay green-by-retry; they erode trust in the whole suite.
- **Do-not** couple tests to each other via shared state or required execution order.

## Common mistakes to avoid
- Over-mocking until tests assert that the mocks were called, proving nothing about real behavior.
- An inverted pyramid: many slow brittle e2e tests, few unit tests — slow CI and flaky signal.
- Tests that only cover the happy path; production breaks on the inputs nobody tested.
- Coverage theater: high percentage, low confidence, because critical branches and error handling are skipped.
- Non-deterministic tests from real time/randomness/network that fail intermittently.
- Writing tests after the fact that simply encode whatever the code currently does, bugs included.
- Skipping authorization and input-validation tests, leaving the security-critical paths unverified.

## Output format
A test plan + the tests themselves: a short table mapping acceptance criteria → layer → test name → status, plus the implemented test files. For audits, produce a coverage summary highlighting critical-path gaps and flaky tests with owners. Link the plan from the spec (`.claude/templates/product-spec.md`).

## Related checklists
- `.claude/checklists/qa.md`
- `.claude/checklists/security.md`
- `.claude/checklists/accessibility.md`

## Related agents
- `.claude/agents/quality/qa-engineer.md`
- `.claude/agents/engineering/backend-engineer.md`
- `.claude/agents/core/orchestrator.md`

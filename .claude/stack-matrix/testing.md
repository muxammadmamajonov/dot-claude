# Testing Stack Matrix

Choose your testing tools by layer: unit → integration → end-to-end → load → contract. Each layer has a distinct purpose and cost; do not conflate them. The testing pyramid still applies — many fast unit tests, fewer slow e2e tests, targeted load tests only for critical paths. Pick tools that match your language runtime first, then layer in e2e and load tools regardless of language.

Key decision drivers: language/runtime, platform (web/mobile/API/desktop), CI environment constraints, acceptable test execution time, team familiarity, and whether you need browser automation or pure API testing.

---

## Unit Testing: Jest

- **When to use:** JavaScript and TypeScript projects — Node.js backends, React/Vue/Angular frontends, React Native. The standard for the JS ecosystem.
- **When NOT to use:** Non-JS projects; pure Node.js projects where Vitest is faster (see below); projects where the test setup overhead of Jest (babel transforms, module mocking) outweighs benefit.
- **Strengths:** Snapshot testing, built-in mocking (`jest.mock`, `jest.spyOn`), jsdom for browser API simulation, parallel test runner, code coverage via V8 or Istanbul, `@testing-library` integration.
- **Weaknesses:** Slower than Vitest on large suites; config complexity for ESM projects; module mocking can be brittle; requires Babel or ts-jest for TypeScript transforms.
- **Team fit:** All JS/TS teams. Jest is the most widely known; abundant examples and StackOverflow answers.
- **Scale fit:** Parallelizes across CPU cores. Sharding across CI machines for large suites.
- **Production risks:** Snapshot files becoming stale and auto-accepted; module mocking hiding real integration bugs; test isolation failure via shared module state.

---

## Unit Testing: Vitest

- **When to use:** Vite-based projects (SvelteKit, Nuxt 3, Astro, vanilla Vite), or any JS/TS project wanting faster test execution. Drop-in Jest API compatibility makes migration easy.
- **When NOT to use:** Projects not using Vite where the ecosystem is already Jest (no compelling reason to migrate); teams unfamiliar with ESM-first workflows.
- **Strengths:** Native ESM support (no transpile step), 2–10x faster than Jest on large suites, compatible with Jest API (`describe`, `it`, `expect`), HMR-driven watch mode, built-in coverage via V8, browser mode via Playwright/WebdriverIO.
- **Weaknesses:** Smaller ecosystem than Jest (fewer third-party plugins); browser mode still maturing; less community history means fewer Q&A resources.
- **Team fit:** Modern frontend teams using Vite toolchain. Strong default for new JS/TS projects started today.
- **Scale fit:** Same parallelism as Jest. Faster per-test means the same CI time budget covers more tests.
- **Production risks:** ESM interop edge cases with CommonJS packages; Vitest's browser mode less battle-tested than Playwright.

---

## Unit Testing: PyTest

- **When to use:** All Python projects — FastAPI, Django, Flask, data pipelines, ML code, scripts, CLI tools. The Python testing standard.
- **When NOT to use:** There is no good reason to use `unittest` directly in new Python projects; PyTest supersedes it while remaining fully compatible.
- **Strengths:** Fixture system (setup/teardown composable and injectable), parametrize decorator for data-driven tests, rich plugin ecosystem (pytest-cov, pytest-asyncio, pytest-mock, pytest-django), clear failure output, compatible with `unittest.TestCase`.
- **Weaknesses:** Fixture scope confusion (function/class/module/session) causes subtle test pollution; plugin version conflicts; async test setup has historically required careful configuration.
- **Team fit:** All Python teams. Mandatory default.
- **Scale fit:** `pytest-xdist` for parallel execution across CPUs. `pytest-split` for CI sharding.
- **Production risks:** Fixture scope leaks causing tests to pass individually but fail in suite; missing `@pytest.mark.asyncio` on async tests causing silent skips; coverage gaps from missing edge-case parametrization.

---

## Unit Testing: JUnit

- **When to use:** Java, Kotlin, Scala, and JVM-based projects. JUnit 5 (Jupiter) is the current standard. Works with Spring Boot, Micronaut, Quarkus, Android (via Robolectric).
- **When NOT to use:** Non-JVM projects. Kotlin projects may prefer Kotest for its idiomatic DSL.
- **Strengths:** JUnit 5 extension model is highly composable, parameterized tests with `@ParameterizedTest`, `@ExtendWith` for dependency injection in tests, Mockito integration for mocking, deep IDE support (IntelliJ, Eclipse).
- **Weaknesses:** Verbose compared to pytest/Vitest; XML test reports are dated; JVM startup overhead for large suites; mocking requires Mockito or PowerMock (complex for statics/constructors).
- **Team fit:** All JVM teams. JUnit is the lingua franca of Java testing.
- **Scale fit:** Maven Surefire / Gradle Test Worker parallelize within the JVM. CI sharding via Gradle test distribution.
- **Production risks:** Static mocking via PowerMock introducing classloader issues; `@BeforeAll` shared state causing flaky tests; missing test isolation between parameterized runs.

---

## Unit Testing: Go test

- **When to use:** All Go projects. `go test` is the built-in Go testing tool — no third-party framework needed. Testify adds assertions and mocking if desired.
- **When NOT to use:** There is no alternative; `go test` is the standard. Avoid BDD frameworks (Ginkgo/Gomega) unless the team has a strong BDD preference — they add boilerplate.
- **Strengths:** Built into the toolchain (no install), parallel tests via `t.Parallel()`, table-driven test pattern is idiomatic, `-race` flag for data race detection, `-cover` for coverage, `httptest` package for HTTP handler testing.
- **Weaknesses:** No built-in mocking (use `testify/mock` or `gomock`); assertion messages require `t.Errorf` verbosity without Testify; test binary compilation time adds up in large monorepos.
- **Team fit:** All Go teams. Add `testify` for cleaner assertions; add `gomock` or `mockery` for interface mocking.
- **Scale fit:** `go test ./... -parallel N` for concurrency. Bazel or `gotestsum` for better CI reporting at scale.
- **Production risks:** Shared global state between tests (Go's `init()` functions); `-race` not run in CI (race conditions in production); missing `t.Cleanup` causing resource leaks in tests.

---

## Integration Testing

- **When to use:** Verify that multiple units work together correctly — database queries return expected results, HTTP handlers process requests end-to-end, message queue consumers handle events correctly. Run against real (or containerized) dependencies.
- **When NOT to use:** As a replacement for unit tests; for UI interaction (use e2e tools).
- **Tooling by stack:**
  - **Node.js/TS:** Supertest (HTTP integration), Testcontainers-node (real DBs in Docker)
  - **Python:** pytest + httpx (async HTTP), Testcontainers-python, Django `TestClient`
  - **Java/Kotlin:** Spring Boot Test (`@SpringBootTest`), Testcontainers, RestAssured
  - **Go:** `net/http/httptest`, Testcontainers-go, `database/sql` against real DB in Docker
- **Key pattern:** Use Testcontainers to spin up real PostgreSQL, Redis, Kafka etc. in Docker during CI. Avoid mocking the database in integration tests — that is the point of integration tests.
- **Production risks:** Slow CI if integration tests are too numerous; flakiness from container startup timing; shared test data causing ordering-dependent failures; not cleaning up containers on failure.

---

## E2E Testing: Playwright

- **When to use:** Web application end-to-end testing across Chrome, Firefox, and Safari. The current best-in-class tool, superseding Cypress for most new projects.
- **When NOT to use:** Mobile native apps (use Detox/Espresso/XCTest); pure API testing (use REST client or contract tests); unit/integration testing (wrong tool).
- **Strengths:** True multi-browser (Chromium, Firefox, WebKit), auto-waiting eliminates most flakiness, network interception, component testing mode, trace viewer for debugging failures, parallel test execution, codegen for recording tests, TypeScript-first API.
- **Weaknesses:** Test isolation requires careful page object patterns; visual regression needs additional tooling (Percy, Argos); setup for auth state management has learning curve; slower than unit tests by 100-1000x.
- **Team fit:** All web teams shipping user-facing UIs. Playwright is the default for new projects.
- **Scale fit:** Playwright sharding across CI workers. Playwright Test built-in reporter integrates with GitHub Actions.
- **Production risks:** Flaky tests from timing assumptions despite auto-wait; tests coupling to CSS selectors instead of accessible roles; large test suites blocking CI; screenshot diffs causing false failures.

---

## E2E Testing: Cypress

- **When to use:** Teams with existing Cypress investment; React-heavy projects where Cypress Component Testing provides component-level isolation; teams preferring browser-based interactive test runner for debugging.
- **When NOT to use:** New projects (choose Playwright); Safari testing required (Cypress lacks WebKit support); mobile testing.
- **Strengths:** Excellent DX for debugging (time-travel in browser, live reload), component testing for React/Vue/Angular, cy.intercept for network stubbing, Cypress Cloud for parallelization and test analytics.
- **Weaknesses:** Chromium/Firefox only (no Safari/WebKit); runs inside the browser (cannot test outside-browser behavior); Cypress Cloud required for meaningful parallelization; slower than Playwright on equivalent test suites.
- **Team fit:** Existing Cypress users. React teams using Cypress Component Testing as a Storybook alternative.
- **Scale fit:** Cypress Cloud shards tests across machines.
- **Production risks:** Same flakiness risks as any e2e; Cypress's single-tab limitation for multi-tab flows; cy.wait() anti-patterns causing false stability.

---

## Mobile Testing: XCTest / Espresso / Detox

### XCTest (iOS)
- Built into Xcode. Use for all native Swift/Objective-C unit and UI testing. XCUITest for interaction testing. No alternative for native iOS UI automation.
- Risk: Slow UI test execution; simulator vs. device behavior differences; fragile to layout changes.

### Espresso (Android)
- Google's official Android UI testing framework. Idling resources make it more reliable than Appium for native Android. Use for all native Kotlin/Java Android UI testing.
- Risk: Requires running on emulator/device; JVM startup time; Robolectric for pure unit tests is faster but less faithful.

### Detox (React Native)
- Grey-box e2e testing for React Native apps. Synchronizes with the JS bridge to eliminate flakiness. Supports iOS (XCUITest) and Android (Espresso) under the hood.
- Risk: Complex setup (build config, device provisioning); slower than web e2e; bridge sync can time out on heavy animations.

**Team fit:** XCTest for iOS-native, Espresso for Android-native, Detox for React Native. Appium as cross-platform fallback for teams needing one framework for both platforms (lower fidelity than native tools).

---

## Load Testing: k6

- **When to use:** API performance testing, stress testing, spike testing, soak testing. JavaScript-based scripts, runs from CLI or Grafana Cloud k6. Best balance of ease-of-use and capability.
- **When NOT to use:** Browser-based load testing requiring real browser rendering (k6 Browser extension exists but is limited); teams needing GUI-based test design (JMeter has a GUI).
- **Strengths:** JavaScript scripting (familiar to most devs), declarative VU (virtual user) and ramp configuration, built-in metrics (p95, p99, error rate), Grafana Cloud k6 for managed execution, Prometheus/InfluxDB integration.
- **Weaknesses:** Go runtime (not a real browser); k6 Cloud required for large distributed loads from multiple regions; less GUI than JMeter.
- **Team fit:** Backend API teams, SRE teams. Easiest entry point for developers new to load testing.
- **Scale fit:** Single machine handles thousands of VUs. Grafana Cloud k6 for global distributed load.
- **Production risks:** Load testing production without rate limiting your own infra; not accounting for connection pool exhaustion in tests; synthetic load not matching real traffic patterns.

### Locust (Python)
- Use when the team is Python-first. Locust tasks are plain Python, distributed mode built-in, web UI for real-time monitoring. Slower per VU than k6 (Python GIL) but highly readable.

### JMeter (Java)
- Legacy standard. XML-based test plans (GUI designer). Use only when the team inherits existing JMeter tests or requires specific JMeter plugins. New projects should prefer k6 or Locust.

---

## Contract Testing: Pact

- **When to use:** Microservices where consumer and provider teams deploy independently. Consumer-driven contract tests catch API breaking changes before integration — essential when services are owned by different teams.
- **When NOT to use:** Monoliths or single-team services where integration tests serve the same purpose more simply; teams with a shared integration test environment that runs on every deploy.
- **Strengths:** Consumer defines the contract (what it expects from the provider), provider verifies against it without needing the consumer running, Pact Broker stores contracts and verification results, prevents breaking API changes from reaching production.
- **Weaknesses:** Setup overhead is significant; both teams must buy into the Pact workflow; Pact Broker requires hosting; most valuable with many services and many teams — overkill for small orgs.
- **Team fit:** Platform teams managing internal APIs consumed by multiple independent teams. Particularly valuable in event-driven and REST microservice architectures.
- **Scale fit:** Pact Broker scales with the number of service pairs. PactFlow (managed) for enterprise.
- **Production risks:** Outdated contracts not reflecting real consumer behavior; provider ignoring failed verifications; not running Pact verification in the provider's CI pipeline.

---

## Comparison Table

| Tool | Layer | Language | Platform | Speed | CI Friendliness |
|---|---|---|---|---|---|
| Jest | Unit | JS/TS | Web/Node/RN | Fast | Excellent |
| Vitest | Unit | JS/TS | Web/Node | Very Fast | Excellent |
| PyTest | Unit | Python | Any | Fast | Excellent |
| JUnit 5 | Unit | Java/Kotlin | JVM | Fast | Excellent |
| go test | Unit | Go | Any | Very Fast | Excellent |
| Testcontainers | Integration | Multi | Any | Medium | Good (Docker req.) |
| Playwright | E2E | JS/TS/Python | Web | Slow | Good |
| Cypress | E2E | JS/TS | Web | Slow | Good (Cloud for scale) |
| XCTest | E2E/Unit | Swift/ObjC | iOS native | Slow | Medium (macOS CI) |
| Espresso | E2E/Unit | Kotlin/Java | Android native | Slow | Medium (emulator) |
| Detox | E2E | JS/TS | React Native | Slow | Medium |
| k6 | Load | JS | Any (API) | N/A | Good |
| Locust | Load | Python | Any (API) | N/A | Good |
| JMeter | Load | Java/XML | Any (API) | N/A | Medium |
| Pact | Contract | Multi | API (REST/async) | Fast | Excellent |

---

## Recommended Combinations

- **Vitest + Playwright + k6** — Modern JS/TS web stack: Vitest for unit speed, Playwright for e2e reliability across browsers, k6 for API load testing. All CI-friendly.
- **PyTest + Testcontainers + Locust** — Python backend: PyTest for unit/integration with real Docker dependencies, Locust for load testing. No tool mismatches.
- **JUnit 5 + Testcontainers + RestAssured + Pact + k6** — Java microservices: JUnit for unit, Testcontainers for integration with real DB/Kafka, RestAssured for HTTP assertions, Pact for inter-service contracts, k6 for load.
- **go test + Testcontainers-go + k6** — Go services: idiomatic Go tests + real dependencies in Docker for integration, k6 for load. Minimal external dependencies.
- **Jest + Cypress Component Testing + Playwright (e2e) + k6** — React-heavy web: Jest for logic, Cypress for component isolation, Playwright for full browser e2e, k6 for API load.
- **XCTest + PyTest/JUnit (backend) + Pact** — iOS app + backend API: XCTest for native iOS, backend tests in Python/Java, Pact contracts ensure the iOS client and backend API stay in sync across team deploys.
- **Detox + Vitest + Playwright (web parity) + k6** — React Native app with shared backend: Detox for mobile e2e, Vitest for shared business logic, Playwright for web parity testing, k6 for API stress.
- **PyTest + RAGAS + PromptFoo** — AI/LLM applications: PyTest for standard unit tests, RAGAS for RAG pipeline quality, PromptFoo for prompt regression testing in CI. See also `.claude/stack-matrix/ai-ml.md`.

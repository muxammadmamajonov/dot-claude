# Testing Strategy

**What:** Defines testing levels, tooling choices, coverage targets, environment topology, and CI gate rules for the project.
**Who fills it in:** QA lead + engineering lead, reviewed by product manager and DevOps.
**When:** Before writing production code. Update when the stack, team size, or risk profile changes.

> This document applies to any project type: web, mobile, backend API, CLI, game, IoT, data pipeline, or AI/ML system. Skip levels that don't apply; note the reason.

---

## 1. Testing Philosophy

> State the guiding principles that shape testing decisions. 2–5 sentences.

- **Shift left:** Find bugs at the cheapest level (unit > integration > E2E > production).
- **Risk-based coverage:** Invest most heavily in code that handles money, auth, data integrity, and public APIs.
- **Tests as documentation:** Test names describe behaviour in plain language; tests serve as the living spec.
- **CI is the gate:** No code merges without green CI. Flaky tests are treated as bugs.
- **Production observability complements tests:** `<Metrics/tracing/alerting detect what tests miss.>`

---

## 2. Test Levels & Ownership

> For each level: what it tests, who writes it, target count or coverage, and tool choice.

### 2.1 Static Analysis & Linting

| Concern | Tool | Config file | Blocks CI? |
|---------|------|-------------|------------|
| Code style | `<ESLint / Ruff / golangci-lint / SwiftLint>` | `.eslintrc` / `pyproject.toml` | Yes |
| Type safety | `<TypeScript strict / mypy --strict / Pyright>` | `tsconfig.json` | Yes |
| Secret detection | `<Gitleaks / TruffleHog>` | `.gitleaks.toml` | Yes |
| Dependency CVEs | `<Dependabot / Snyk / OWASP Dependency-Check>` | CI config | Yes (Critical) |
| IaC scanning | `<Checkov / tfsec>` | CI config | Yes (Critical) |

### 2.2 Unit Tests

- **What they test:** Pure functions, business logic, algorithms, data transformations, utility helpers — in isolation from I/O and external services.
- **Who writes them:** Feature developer, alongside the code (TDD preferred).
- **Coverage target:** `<80% line coverage minimum; 90%+ for auth, payment, data-validation modules>`
- **Speed target:** Full suite runs in `< 60 s`.
- **Mocking strategy:** `<Stub I/O at the boundary (repository / adapter layer); do not mock the system under test>`

| Layer | Framework |
|-------|-----------|
| `<Backend (Node.js)>` | `<Vitest | Jest>` |
| `<Backend (Python)>` | `<pytest + pytest-cov>` |
| `<Backend (Go)>` | `<go test + testify>` |
| `<Frontend (React)>` | `<Vitest + React Testing Library>` |
| `<Mobile (Swift)>` | `<XCTest>` |
| `<Mobile (Kotlin)>` | `<JUnit5 + Mockk>` |
| `<Game (Unity)>` | `<Unity Test Framework (EditMode)>` |

### 2.3 Integration Tests

- **What they test:** Interactions between components — service ↔ database, service ↔ cache, service ↔ queue, multiple modules wired together.
- **Who writes them:** Feature developer + QA engineer for complex flows.
- **Coverage target:** All public API endpoints; all database migrations round-trip; all queue producer/consumer pairs.
- **Environment:** `<Runs against real DB in Docker Compose testenv; uses test-specific schema or isolated DB name>`
- **Data strategy:** `<Seed fixtures per test; truncate after each test — no shared mutable state between tests>`

| What | Framework |
|------|-----------|
| HTTP API contracts | `<Supertest | httpx | net/http/httptest>` |
| Database | `<pg-mem / testcontainers / SQLite in-memory / real Docker Postgres>` |
| Message queues | `<testcontainers-kafka | localstack SQS>` |
| Third-party APIs | `<WireMock / Nock / responses (Python) — record once, replay in CI>` |

### 2.4 Contract Tests

- **What they test:** The interface boundary between this service and its consumers / providers — ensures a producer change does not silently break a consumer.
- **Applies when:** `<Microservices architecture | Multiple teams sharing API | Mobile app + backend>`.
- **Tool:** `<Pact (consumer-driven) | OpenAPI schema validation | Specmatic>`
- **CI gate:** Consumer publishes pact → provider verifies in its pipeline before deploy.

### 2.5 End-to-End (E2E) Tests

- **What they test:** Full user flows through a real or near-real environment — from UI input to database state.
- **Who writes them:** QA engineer + feature developer for the critical path.
- **Suite size target:** `<Fewer than 100 tests; only cover the P0 flows listed in §3 below.>` (E2E are slow and brittle by nature.)
- **Parallelism:** `<Run in parallel across N workers; shard by feature area>`
- **Retry policy:** `<1 retry on failure in CI; alert on > 2% flake rate>`

| Platform | Framework | Run target |
|----------|-----------|------------|
| Web | `<Playwright | Cypress>` | `<Chromium + Firefox>` |
| Mobile iOS | `<XCUITest | Detox>` | `<iPhone 15 simulator>` |
| Mobile Android | `<Espresso | Detox>` | `<Pixel 6 API 34 emulator>` |
| API-only | `<Newman (Postman) | Tavern | pytest-httpx>` | `<Staging environment>` |
| Game | `<Unity Test Framework (PlayMode) | custom>` | `<Headless build>` |

### 2.6 Visual Regression Tests

- **What they test:** Unintended UI changes — pixel diffs against approved baseline screenshots.
- **Tool:** `<Chromatic | Percy | Playwright visual comparisons | Storybook + Reg-suit>`
- **Trigger:** Run on PRs that touch UI components or design tokens.
- **Approval workflow:** `<Diff shown in PR; designer approves baseline update>`

### 2.7 Performance Tests

> See `.claude/templates/performance-plan.md` for full budgets. This section defines the *test* side only.

| Type | Tool | When run | Pass criteria |
|------|------|----------|---------------|
| Load test | `<k6 | Locust | Artillery>` | `<Nightly on staging>` | `<p95 < 300 ms; error rate < 0.1%>` |
| Stress test | `<k6>` | `<Pre-release>` | `<Graceful degradation at 2× expected peak>` |
| Spike test | `<k6>` | `<Pre-release>` | `<Recovery within 30 s after spike>` |
| Frontend bundle | `<Bundlewatch | size-limit>` | `<Every PR>` | `<JS < 250 kB gzip; CSS < 30 kB>` |
| Lighthouse CI | `<LHCI>` | `<Every PR>` | `<Performance ≥ 90; Accessibility ≥ 95>` |

### 2.8 Security Tests

> See `.claude/templates/security-model.md` for threat model.

| Type | Tool | Cadence | Owner |
|------|------|---------|-------|
| SAST | `<Semgrep / CodeQL / Bandit>` | Every PR | CI automation |
| Dependency CVE scan | `<Dependabot / Snyk>` | Daily | DevOps |
| DAST (dynamic) | `<OWASP ZAP / Nuclei>` | Weekly on staging | Security lead |
| Penetration test | External firm | `<Annually / pre-major launch>` | CTO |
| Secrets scan | `<Gitleaks>` | Pre-commit + CI | CI automation |

### 2.9 Accessibility Tests

| Type | Tool | Blocks CI? |
|------|------|------------|
| Automated axe scan | `<axe-core via Playwright / jest-axe>` | Yes |
| Color contrast check | `<Storybook a11y addon / axe>` | Yes |
| Manual screen-reader test | VoiceOver, TalkBack, NVDA | No (checklist before release) |

---

## 3. P0 Critical Paths (Must Always Pass)

> These flows must have E2E or integration test coverage. A failing test here blocks all deployments.

1. `<User registers, verifies email, and logs in>`
2. `<User completes primary core action — e.g. places an order, submits a form, publishes a post>`
3. `<Payment flow: initiates checkout → Stripe webhook → order confirmed>`
4. `<Admin creates/modifies/deletes a resource>`
5. `<Password reset flow end-to-end>`

---

## 4. Test Environments

| Environment | Purpose | Data | Deployment trigger | External services |
|-------------|---------|------|--------------------|------------------|
| **Local (dev)** | Developer inner loop | Seeded fixtures | Manual | Mocked / WireMock |
| **CI** | PR gate | Seeded fixtures; isolated DB per run | Every commit/PR | Mocked |
| **Staging** | Integration, E2E, perf, DAST | Anonymised prod snapshot or generated | Merge to `main` | Sandbox/test accounts |
| **Prod** | Smoke test only post-deploy | Real | Post-deploy pipeline | Real (read-only probes) |

**Staging data rules:**
- No real PII in staging — use anonymised snapshots or generated data.
- Stripe: `<test mode keys only>`
- Email: `<Mailtrap / no real sends — catch-all test inbox>`

---

## 5. CI Pipeline Gates

> Define what must pass before each stage. Nothing proceeds if a gate fails.

```
PR opened
  └─► [Lint + Type check]  → fail = block merge
  └─► [Unit tests]         → fail = block merge
  └─► [Integration tests]  → fail = block merge
  └─► [SAST + secrets]     → fail = block merge
  └─► [Visual diff]        → fail = request designer review
  └─► [Bundle size check]  → fail = block merge (if exceeds limit)

Merge to main
  └─► [All above]
  └─► [E2E tests on staging]  → fail = block deploy to prod
  └─► [Performance tests]     → fail = block deploy to prod

Deploy to prod
  └─► [Smoke tests]           → fail = auto-rollback
```

**Parallelism:** `<Unit + lint run in parallel; integration runs after lint passes.>`
**Test result storage:** `<JUnit XML / JSON uploaded as CI artifact; 30-day retention>`
**Flake detection:** `<Test reported flaky if it fails without code changes on 2 consecutive runs — auto-creates issue>`

---

## 6. Coverage Targets

| Module / area | Line coverage target | Branch coverage target | Notes |
|---------------|---------------------|----------------------|-------|
| Auth & session | 90% | 85% | Critical security surface |
| Payment / billing | 90% | 85% | Financial risk |
| Public API endpoints | 85% | 80% | |
| Data access layer | 80% | 75% | Integration tests supplement |
| UI components | 70% | 60% | Visual regression fills the gap |
| Utility / helpers | 80% | 75% | |
| CLI commands | 80% | 75% | |
| **Overall project** | **`<80%>`** | **`<75%>`** | Enforced by CI coverage gate |

> Coverage is a floor, not a goal. 100% coverage with trivial tests provides false confidence. Focus on meaningful assertions.

---

## 7. Test Data Management

| Concern | Approach |
|---------|---------|
| Fixtures | `<Factory functions (factory-bot / fishery / factory_boy) — build objects in code, not YAML files>` |
| Database seeding | `<Seed script idempotent; run via `npm run db:seed` / `make seed`>` |
| Large datasets | `<Generated with Faker; stored in `.claude/fixtures/`; versioned>` |
| PII in tests | `<Forbidden — generate synthetic data; no real emails/phones>` |
| Test isolation | `<Each test runs in a transaction rolled back after; or use per-test DB namespace>` |

---

## 8. Testing for AI/ML Components

> Fill in if the project includes ML models, LLM integrations, or AI agents.

| Concern | Testing approach |
|---------|----------------|
| LLM output quality | `<Eval harness (e.g. PromptFoo / Braintrust) with golden-set assertions>` |
| Regression on model update | `<Snapshot tests on benchmark prompts; alert on >5% quality drop>` |
| Tool/function call correctness | `<Unit tests with stubbed LLM responses; verify tool schemas>` |
| Latency | `<p95 < X ms; measured in load tests with realistic prompt corpus>` |
| Cost per request | `<Token count assertion in integration tests; budget alert in prod>` |
| Hallucination / safety | `<Red-team eval suite; block deploy if safety classifier fail rate > threshold>` |

---

## 9. Defect Management

| Severity | Definition | SLA to fix | Blocks release? |
|----------|-----------|-----------|-----------------|
| **P0 — Critical** | Data loss, auth bypass, payment failure, prod outage | `< 4 h` | Yes |
| **P1 — High** | Core feature broken for all users | `< 24 h` | Yes |
| **P2 — Medium** | Feature broken for subset; workaround exists | `< 1 week` | No (tracked) |
| **P3 — Low** | Minor UI glitch, edge-case | Next sprint | No |

**Bug triage process:** `<New bugs in GitHub Issues / Jira with template including repro steps, environment, logs, expected vs actual.>`

---

## 10. Open Decisions

| # | Question | Owner | Date needed |
|---|----------|-------|-------------|
| 1 | `<e.g. Should E2E run against Docker Compose or a dedicated staging cluster?>` | `<DevOps lead>` | `<YYYY-MM-DD>` |
| 2 | `<e.g. Which contract-testing tool — Pact or Specmatic?>` | `<Arch lead>` | `<YYYY-MM-DD>` |

---

## 11. Related Documents

- Security model: `.claude/templates/security-model.md`
- Performance plan: `.claude/templates/performance-plan.md`
- CI/CD pipeline config: `<.github/workflows/ | .gitlab-ci.yml | Jenkinsfile>`
- QA checklist: `.claude/checklists/qa.md`
- Architecture: `.claude/templates/architecture.md`

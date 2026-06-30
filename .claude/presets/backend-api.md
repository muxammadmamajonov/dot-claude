# Backend API / Service Preset

## Project type
Server-side application exposing a programmatic interface consumed by other software — web frontends, mobile apps, third-party integrations, or other services. Variants: REST API, GraphQL API, gRPC service, WebSocket server, event-driven microservice, background job processor, data pipeline service, or BFF (Backend for Frontend). May be a standalone monolith, a service in a microservices mesh, or a serverless function fleet.

## Typical use cases
- Core product API backing a web/mobile client
- B2B integration APIs (webhooks, partner data exchange, ETL)
- Internal platform services (auth service, notification service, billing service)
- Data ingestion and processing pipelines
- AI/ML inference serving endpoints
- Background job queues (email delivery, report generation, async workflows)

## Required discovery questions
1. What consumers will call this API — first-party clients (web/mobile), external third-party developers, or internal services? Is a public developer portal required?
2. What protocol is required — REST/JSON, GraphQL, gRPC, WebSocket, or a mix? Are there versioning expectations from existing consumers?
3. What is the expected request throughput at launch and at 12-month scale? Are there burst traffic patterns (end-of-month billing, marketing campaigns)?
4. What is the data model — relational, document, graph, time-series, or hybrid? Are there existing legacy databases that must be integrated?
5. What are the idempotency requirements for write operations? Do any operations involve money, inventory, or irreversible state changes?
6. What authentication and authorisation model is required — API keys, JWT/OAuth 2.0, mTLS, IP allowlist, or a combination?
7. Are there rate limiting, quota, or SLA requirements per consumer tier?
8. Does the service need to produce or consume events (Kafka, SQS, SNS, RabbitMQ)? Are there exactly-once or ordering guarantees needed?
9. What are the observability requirements — structured logging, distributed tracing, custom metrics, alerting SLOs?
10. Is this service deployed as a long-running process (container/VM), serverless functions, or at the edge?

## Recommended agents

### Core
- `.claude/agents/core/orchestrator.md` — API surface ownership, versioning governance
- `.claude/agents/core/solution-architect.md` — service boundaries, data model, integration patterns
- `.claude/agents/core/project-manager.md` — endpoint delivery phasing, consumer onboarding plan

### Engineering
- `.claude/agents/engineering/backend-engineer.md` — request handling, business logic, ORM/query layer
- `.claude/agents/engineering/database-architect.md` — schema design, migrations, indexing strategy
- `.claude/agents/engineering/backend-engineer.md` — OAuth 2.0 flows, token introspection, RBAC/ABAC
- `.claude/agents/engineering/backend-engineer.md` — queue workers, event consumers, retry policies

### Quality
- `.claude/agents/quality/qa-engineer.md` — contract testing, integration testing, load testing
- `.claude/agents/quality/performance-engineer.md` — p99 latency, throughput benchmarks, query profiling
- `.claude/agents/quality/security-auditor.md` — injection, auth bypass, mass assignment, secrets audit

### Domain
- `.claude/agents/core/documentation-writer.md` — OpenAPI/AsyncAPI spec, developer portal, changelog
- `.claude/agents/quality/reliability-engineer.md` — structured logs, trace correlation, SLO dashboards

## Recommended skills
- `.claude/skills/api-design/SKILL.md` — RESTful conventions, GraphQL schema design, versioning
- `.claude/skills/data-modeling/SKILL.md` — query optimisation, migrations, connection pooling
- `.claude/skills/security/SKILL.md` — JWT validation, OAuth flows, API key management
- `.claude/skills/security/SKILL.md` — input validation, injection prevention, rate limiting
- `.claude/skills/backend/SKILL.md` — idempotency keys, dead-letter queues, retry with backoff
- `.claude/skills/testing/SKILL.md` — unit, integration, contract, load (k6/Locust)
- `.claude/skills/production-readiness/SKILL.md` — structured logs, OpenTelemetry tracing, SLO alerting

## Recommended stack options

| Stack | Rationale |
|---|---|
| **Node.js (Fastify or Hono) + PostgreSQL + TypeScript** | Fast I/O; type-safe; shared language with frontend teams; excellent ecosystem for REST and WebSockets. See `.claude/stack-matrix/backend.md` |
| **Python (FastAPI) + PostgreSQL / SQLAlchemy** | Best for ML/AI adjacent services; async-native; auto-generated OpenAPI docs; strong data library ecosystem |
| **Go (Gin / Chi / stdlib) + PostgreSQL** | Highest throughput per core; tiny container images; ideal for latency-critical or high-concurrency services |
| **Java / Kotlin (Spring Boot) + PostgreSQL** | Enterprise-grade; mature transaction management; strong when integrating with JVM ecosystem (Kafka, Hadoop, legacy ERP) |

Reference `.claude/stack-matrix/backend.md`, `.claude/stack-matrix/database.md`, `.claude/stack-matrix/cloud-devops.md` for detailed tradeoffs.

## Required checklists
- `.claude/checklists/security.md` — injection, auth bypass, secrets, dependency CVEs
- `.claude/checklists/performance.md` — query plans, connection pool sizing, cache strategy
- `.claude/checklists/launch.md` — health endpoint, graceful shutdown, DB backup, monitoring
- `.claude/checklists/api.md` — versioning, error schema consistency, rate limiting, pagination
- `.claude/checklists/production.md` — structured logs, traces correlated, SLO defined and alerted

## MVP scope pattern

**In MVP**
- Core CRUD endpoints for the primary resource
- Authentication (API key or JWT) and basic authorisation
- Input validation and consistent error response schema
- Health-check endpoint (`/health`, `/ready`)
- Structured JSON logging with request ID
- Database schema and initial migration
- Rate limiting on all public-facing endpoints
- Basic API documentation (OpenAPI spec)

**Deferred to v2**
- GraphQL or gRPC layer (add after REST contract is stable)
- Webhook delivery system
- Per-consumer quota management
- Advanced RBAC / attribute-based access control
- Event sourcing or CQRS pattern
- Async job queue for long-running tasks
- Multi-region failover
- Developer portal and SDK generation

## Production risks

| Risk | Severity | Mitigation |
|---|---|---|
| SQL injection via unsanitised input | P0 | Use parameterised queries / ORM; never string-interpolate SQL |
| Unauthenticated endpoints returning sensitive data | P0 | Auth middleware applied globally; explicit opt-out for public routes; automated route audit |
| Missing idempotency on payment / state-change endpoints | P0 | Accept `Idempotency-Key` header; store and replay safe response for duplicate requests |
| Unhandled promise rejections crashing Node.js process | P0 | Global unhandled rejection handler; process manager (PM2/supervisord) to restart |
| Mass-assignment overwriting protected fields | P0 | Allowlist DTO fields; never pass raw request body to ORM `save()` |
| Secrets committed to repository | P0 | Pre-commit hook (`gitleaks`); secrets manager (Vault, AWS SSM) for all credentials |
| N+1 queries degrading under load | P1 | Enable slow-query log in staging; DataLoader / eager loading; explain-analyse new queries |
| Missing DB connection pool limit causing connection exhaustion | P1 | Set pool max; use pgBouncer in transaction mode for high concurrency |
| No graceful shutdown — in-flight requests dropped on deploy | P1 | Handle `SIGTERM`; drain connections with configurable timeout before exit |
| Unbounded pagination returning millions of rows | P1 | Enforce `limit` cap; cursor-based pagination for large datasets |
| SSRF via user-supplied URLs in outbound requests | P1 | Allowlist outbound domains; reject private-IP ranges; use a proxy for third-party fetches |
| No distributed tracing — blind spots in microservice chains | P2 | Propagate `traceparent` (W3C); emit spans for DB, external HTTP, queue operations |

## Launch requirements
- All P0 checklist items in `.claude/checklists/security.md` signed off
- `/health` returns 200 with dependency status; `/ready` gated on DB connectivity
- Graceful shutdown tested under load: zero dropped requests on SIGTERM
- p99 latency and error-rate SLOs defined, instrumented, and alerted in monitoring
- Database backup automated, restoration tested, RTO/RPO documented
- OpenAPI spec published and versioned; breaking-change policy documented
- Rate limits configured and tested; abuse response plan documented
- Staging environment with production-parity schema and sanitised data in place
- Rollback strategy: DB migration reversibility confirmed or blue/green deploy ready
- On-call runbook drafted in `docs/runbook.md`

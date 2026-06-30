# Backend Checklist
Gate for backend service projects covering idempotency, rate limits, timeouts, migrations, and observability. Severity tiers: P0=blocker, P1=important (fix shortly after launch), P2=hardening, P3=post-launch/backlog.

## P0 — Blockers (must pass before any traffic is served)

- [ ] **No secrets in source**: All credentials, API keys, connection strings, and tokens are loaded from environment variables or a secrets manager; `git log` and `git grep` confirm none are committed; `.env` files are in `.gitignore`.
- [ ] **Database migrations are reversible**: Every migration has a tested `down` script; applying and rolling back leaves the schema in its prior state; verified in a staging environment before production.
- [ ] **Migrations run without table locks on production data sizes**: Schema changes use `ADD COLUMN … DEFAULT NULL`, concurrent index builds, or equivalent lock-free strategies; tested against a clone of production data volume.
- [ ] **Health and readiness endpoints exist**: `/health` (liveness) and `/ready` (readiness — checks DB, cache, external deps) return `200` when healthy and `503` when degraded; used by load balancer and orchestrator.
- [ ] **Authentication is enforced on all non-public routes**: Every endpoint that handles user data requires a valid auth token; no route accidentally left open; verified by a negative test (unauthenticated request returns `401`/`403`).
- [ ] **Input validation rejects malformed payloads**: All user-supplied input is validated (type, length, format, encoding) before reaching business logic; fuzz/boundary tests confirm `400` on invalid input, not `500`.
- [ ] **No unhandled promise rejections / panics reach the client**: Uncaught exceptions return a structured `500` error, not a stack trace; stack traces are never sent to API consumers.
- [ ] **Graceful shutdown implemented**: On `SIGTERM` the service stops accepting new requests, drains in-flight requests (with a configurable timeout), closes DB connections cleanly, and exits with code `0`.

## P1 — Important (fix before scaling or shortly after launch)

- [ ] **Idempotency keys on mutating endpoints**: `POST` endpoints that create resources or trigger side-effects accept an idempotency key; replaying the same key within the TTL window returns the cached result without re-executing.
- [ ] **Rate limiting active**: Per-user and per-IP rate limits are enforced at the API gateway or middleware level; responses include `Retry-After` and `X-RateLimit-*` headers; limits are tuned to actual usage patterns.
- [ ] **Timeouts set on all outbound calls**: Every HTTP client, DB query, cache call, and queue operation has an explicit timeout; defaults from the SDK/driver are not relied upon.
- [ ] **Circuit breaker on critical dependencies**: Downstream calls to payment providers, email services, or third-party APIs are wrapped in a circuit breaker; failure does not cascade to a full service outage.
- [ ] **Structured logging with correlation IDs**: Every log line includes `request_id` (or `trace_id`), `service`, `level`, and `timestamp` in JSON; log level is configurable at runtime without restart.
- [ ] **Distributed tracing instrumented**: At minimum entry/exit spans are emitted for each request, outbound HTTP call, and DB query; traces are visible in the observability stack (e.g., Datadog, Jaeger, OpenTelemetry).
- [ ] **Error budget / SLO defined and tracked**: Availability and latency SLOs (e.g., 99.9 % uptime, p99 < 500 ms) are defined; dashboards and alerts fire before the error budget is exhausted.
- [ ] **Background jobs are observable**: Each scheduled or async job emits start/success/failure events; failed jobs enter a dead-letter queue with alerting; jobs are idempotent and safe to retry.
- [ ] **API versioning strategy in place**: Breaking changes are introduced under a new version prefix (`/v2/`) or via `Accept` header; old versions have a documented deprecation timeline.
- [ ] **Pagination on all list endpoints**: No list endpoint returns an unbounded result set; cursor-based or offset pagination with a maximum `limit` (e.g., 1000) is enforced.

## P2 — Hardening / nice-to-have

- [ ] **Request payload size limits enforced**: The HTTP server rejects request bodies above a configured maximum (e.g., 10 MB for JSON, configurable for file uploads) to prevent memory exhaustion.
- [ ] **SQL query budget**: Slow-query logging is enabled; queries exceeding a threshold (e.g., 1 s) are logged with the full query plan; no unbounded `SELECT *` on large tables in hot paths.
- [ ] **Connection pool tuning documented**: DB and cache connection pool sizes are set explicitly (not library defaults); `max_connections` on the DB side is not exceeded under peak load.
- [ ] **Feature flags decouple deploys from releases**: New behaviour is gated behind a feature flag so a rollback is a flag flip, not a revert + redeploy.
- [ ] **Dependency audit clean**: `npm audit`, `pip-audit`, `govulncheck`, or equivalent reports zero critical/high CVEs in production dependencies; findings are tracked in `.claude/checklists/security.md`.
- [ ] **API contract tests in CI**: Consumer-driven or provider-side contract tests (e.g., Pact, Dredd) run in CI to catch breaking changes before they reach staging.
- [ ] **Load test baseline established**: A baseline load test (e.g., k6, Locust) has been run against staging; throughput and p99 latency at 2× expected peak load are documented.
- [ ] **Runbook for each alert**: Every production alert has a runbook link in the alert body describing diagnosis steps and remediation actions.

## P3 — Post-launch / backlog (track and revisit after launch; never blocks shipping)

- [ ] **GraphQL / gRPC / AsyncAPI schema registry**: All service contracts (REST OpenAPI, gRPC proto, GraphQL SDL, AsyncAPI) are published to a central schema registry with versioning; consumers subscribe to breaking-change notifications automatically.
- [ ] **Chaos engineering baseline**: A fault-injection runbook (kill a pod, inject latency, drop a DB connection) is documented and exercised in staging quarterly; findings feed into resilience improvements tracked in the backlog.
- [ ] **Multi-region active-active or active-passive readiness**: Data residency, conflict resolution, and failover routing are designed and documented even if not yet deployed; the plan is reviewed whenever traffic or compliance requirements change.
- [ ] **Deprecation enforcement pipeline**: Sunset endpoints emit `Deprecation` and `Sunset` HTTP headers; a tooling job tracks consumer call counts against the deprecation date and sends automated warnings to callers still using deprecated routes.
- [ ] **Cost attribution per endpoint**: Per-route CPU/memory/DB-query cost is instrumented (e.g., via OpenTelemetry resource attributes + cloud cost tags); the top-10 most expensive endpoints are reviewed monthly for optimization opportunities.
- [ ] **Event-sourcing or audit-log replay verified**: For services that use event sourcing or append-only audit logs, a replay from log-zero to current state is exercised in a non-production environment to confirm log completeness and idempotency.

## How to use

**When**: Run this checklist before promoting a service to production and again before any significant traffic increase or architectural change.

**Who**: Backend engineer owns P0 items. Engineering lead signs off P1. SRE/platform team reviews P2 during capacity planning.

**Command / agent**: Ask the agent `"Run .claude/checklists/backend.md for service <name>"` — it will scan for hardcoded secrets, verify health endpoint responses, inspect migration files for down scripts, and check timeout configuration in the codebase. Items requiring load testing or manual deployment validation are flagged for human sign-off. Cross-reference `.claude/checklists/security.md` for CVE tracking and `.claude/checklists/database.md` for migration and query-budget details.

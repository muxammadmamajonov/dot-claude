---
name: backend
description: >
  Activate when building, extending, or operating backend services — REST APIs,
  GraphQL APIs, gRPC services, message consumers, background workers, or
  microservices. Covers contract design, data modelling, auth, job queues,
  observability, and deployment. Applies to Node.js, Python, Go, Java/Kotlin,
  Ruby, Rust, PHP, or any server-side stack. Do NOT activate for web frontends
  (use .claude/skills/web/SKILL.md) or infrastructure-only changes (Terraform,
  Kubernetes manifests) — though this skill references infrastructure concerns.
---

# Backend Service Skill

## When to use

- Designing or implementing a new API surface (REST, GraphQL, gRPC, WebSocket)
- Adding database models, migrations, or data-access layers
- Implementing auth (sessions, JWT, OAuth 2.0, API keys)
- Building background jobs, queues, cron tasks, or event consumers
- Integrating third-party services (payment providers, email, storage, AI APIs)
- Preparing a service for production: observability, rate limiting, graceful shutdown

---

## Workflow

1. **Classify the project** — Read `docs/specs/product.md` and `.claude/stack-matrix/backend.md` to confirm language/runtime, API style, database(s), and deployment target (container, serverless, VPS). If these don't exist, interview the founder first (`.claude/agents/core/orchestrator.md`).

2. **Define the API contract first** — Write the contract before any implementation:
   - REST: OpenAPI 3.1 YAML with request/response schemas, error codes, and auth scheme
   - GraphQL: SDL schema with descriptions on every type and field
   - gRPC: `.proto` file with service definition and message types
   Store the contract at `docs/api/` and reference it in `README.md`. Never break a published contract without versioning.

3. **Design the data model** — Write the schema (SQL DDL or ODM schema) before coding:
   - Name tables/collections in singular snake_case (e.g. `user`, `order_item`)
   - Add `created_at`, `updated_at` timestamps to every mutable table
   - Choose primary key type deliberately: UUID v7 (time-sortable) for distributed systems, auto-increment for simple single-DB apps
   - Write migrations with a migration tool (Alembic, Flyway, Prisma Migrate, golang-migrate); never alter production schema manually

4. **Implement the data-access layer** — Centralise all DB queries in a repository or DAO layer:
   - No raw SQL in route handlers or controllers
   - Use parameterised queries / ORM — never string-interpolate user input into SQL
   - Write read replicas logic separately from primary writes if applicable

5. **Implement auth and authorisation**
   - Auth (who are you?): prefer an established library or managed identity provider (Auth0, Supabase Auth, Keycloak) over hand-rolled JWT logic
   - Authorisation (what can you do?): enforce at the service layer, not only the API layer; implement RBAC or ABAC as the spec requires
   - Rotate secrets on a schedule; invalidate tokens on logout (maintain a denylist or use short expiry + refresh)
   Reference `.claude/skills/security/SKILL.md`.

6. **Handle errors consistently** — All error responses must follow a single shape:
   ```json
   { "error": { "code": "MACHINE_READABLE_CODE", "message": "Human message", "details": {} } }
   ```
   Use HTTP status codes correctly: 400 for client errors, 401 unauthenticated, 403 forbidden, 404 not found, 422 validation, 429 rate-limited, 500 server errors.

7. **Add input validation** — Validate and sanitise every inbound payload at the API boundary before it reaches any business logic. Use a schema validator (Zod, Pydantic, `class-validator`, `ozzo-validation`). Reject unknown fields.

8. **Implement background jobs** — Use a dedicated queue (BullMQ, Celery, Sidekiq, Temporal, AWS SQS) rather than spawning goroutines/threads in the request handler:
   - Jobs must be idempotent — safe to retry on failure
   - Store job state and completion receipts; expose a status endpoint
   - Set dead-letter queues for unprocessable messages

9. **Add observability**
   - Structured JSON logging with trace-id, request-id, user-id on every log line
   - Metrics: request count, latency p50/p95/p99, error rate, queue depth — expose as Prometheus endpoint or push to Datadog/Grafana Cloud
   - Distributed tracing: instrument with OpenTelemetry; attach spans to DB queries, outbound HTTP calls, and queue operations
   Reference `.claude/checklists/production.md`.

10. **Implement rate limiting** — Apply at the API gateway or service layer per (user, IP, or API key). Return `Retry-After` header on 429 responses. Separate limits for auth endpoints (stricter) vs. read endpoints.

11. **Write tests**
    - Unit: pure functions, validators, business-logic services (mock the DB)
    - Integration: API routes with a real (test) database using transactions rolled back after each test
    - Contract: Pact or Dredd tests to verify the API matches the published spec
    Reference `.claude/checklists/qa.md`.

12. **Deploy safely** — Use the deploy sequence from `.claude/agents/core/orchestrator.md`:
    - Run migrations before deploying new code (additive-only migrations are safe; destructive ones require a multi-phase deploy)
    - Implement graceful shutdown: stop accepting new requests, drain in-flight requests, close DB pool
    - Use readiness and liveness probes for container orchestrators

---

## Standards

**Do**
- Return pagination metadata (`total`, `page`, `limit`, `next_cursor`) on all list endpoints.
- Cache expensive read queries at the service layer (Redis, Memcached) with explicit TTLs; invalidate on write.
- Use connection pooling for all databases; configure pool size to match server resources, not to unlimited.
- Set timeouts on all outbound HTTP calls (default client timeout is often infinite).
- Prefer async I/O; block threads only when the library forces it and document why.
- Keep environment-specific config in env vars; use a validated config loader at startup so the service fails fast on misconfiguration.

**Do not**
- Log passwords, tokens, PII, or card numbers — use field masking in your log sanitiser.
- Return stack traces in production API responses — log them server-side only.
- Use `SELECT *` in production queries — select explicit columns; `*` breaks when columns are added.
- Perform database migrations inside the application startup path — run migrations as a separate pre-deploy step.
- Hard-code retry counts or timeouts as magic numbers in business code — put them in config.
- Trust `Content-Type` without validating the actual payload.

---

## Common mistakes to avoid

- **N+1 queries** — loading a list then fetching related rows per item in a loop; use eager-loading (`JOIN`, `include`, `prefetch_related`) or batch fetching.
- **Missing database indexes** — any column used in a `WHERE`, `ORDER BY`, or `JOIN ON` clause in a hot query needs an index; run `EXPLAIN ANALYZE` to verify.
- **Unbounded response payloads** — list endpoints without pagination return millions of rows on a mature system; always default to a sensible `limit` (e.g. 25).
- **Silent job failures** — a background job that fails and logs nothing is invisible; always catch exceptions, log with context, and update job status to `failed`.
- **Secrets in environment variables logged at startup** — `console.log(process.env)` or equivalent dumps all secrets; redact them explicitly.
- **CORS misconfiguration** — `Access-Control-Allow-Origin: *` on authenticated endpoints; restrict to known origins.
- **Forgetting idempotency keys on payment/mutation endpoints** — duplicate requests (network retry, user double-click) must not create duplicate charges or records.

---

## Output format

A production-ready backend service should include:

```
/
├── src/ (or app/, cmd/)
│   ├── api/             # Route handlers / controllers
│   ├── services/        # Business logic
│   ├── repositories/    # Data-access layer
│   ├── models/          # Domain models / DB schema types
│   ├── jobs/            # Background job definitions
│   ├── middleware/       # Auth, logging, rate-limit middleware
│   └── config/          # Validated env-var config loader
├── migrations/          # Database migration files (in order)
├── tests/
│   ├── unit/
│   └── integration/
├── docs/
│   └── api/             # OpenAPI / GraphQL SDL / proto files
├── .env.example
├── Dockerfile
└── README.md            # Local dev setup, migration steps, test commands
```

---

## Related checklists

- `.claude/checklists/security.md`
- `.claude/checklists/performance.md`
- `.claude/checklists/qa.md`
- `.claude/checklists/production.md`

## Related skills

- `.claude/skills/api-design/SKILL.md` — owns the API **contract** (resources, versioning, error taxonomy, pagination). Design the contract there first; this skill covers its **implementation**.

## Related agents

- `.claude/agents/core/orchestrator.md`
- `.claude/agents/quality/security-auditor.md`
- `.claude/agents/engineering/database-architect.md`

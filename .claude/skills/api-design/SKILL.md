---
name: api-design
description: Design clean, versioned, secure API contracts (REST, GraphQL, RPC, events, or library/SDK surface) from requirements and the data model. Activate before implementing endpoints or any inter-component/public interface, and when an existing contract needs a breaking change handled safely.
---

# API Design

**Scope: the API CONTRACT (resources, versioning, errors, pagination). Implementation → `.claude/skills/backend/SKILL.md`.**

## When to use
- After requirements (`.claude/skills/requirements-engineering/SKILL.md`) and data modeling (`.claude/skills/data-modeling/SKILL.md`), before endpoint/handler implementation.
- When defining any boundary contract: public/partner API, internal service-to-service, event/message schema, CLI surface, or a library/SDK's public interface.
- When a contract must change in a backward-incompatible way and consumers must be migrated safely.

## Workflow
1. **Pick the interface style** to match consumers and the architecture (`docs/architecture.md`): REST for resource CRUD over HTTP; GraphQL for flexible client-driven reads; gRPC/RPC for low-latency internal calls; async events/messages for decoupled workflows; a typed library/SDK surface for code consumers. Hybrids are normal (e.g. REST + webhooks).
2. **Model resources/operations from the domain**, not from database tables. Name resources as plural nouns (`/orders`, `/orders/{id}/items`); name RPCs/events as verbs (`CreateOrder`, `order.created`). Keep the contract stable even if storage changes.
3. **Define the request/response contract** for each operation: inputs with types and validation rules, output schema, status/result codes, and pagination/filtering/sorting conventions (cursor-based for large/append-only sets). Use a consistent envelope and a consistent error shape (machine-readable `code`, human `message`, and field-level details).
4. **Design authentication and authorization into the contract.** Specify the auth mechanism (OAuth2/OIDC, API keys, mTLS, signed requests), which scopes/roles each operation requires, and tenant isolation for multi-tenant systems. Never expose an operation without an explicit authz rule.
5. **Build in safety controls**: input validation at the boundary, rate limiting/quotas, idempotency keys for unsafe-to-retry writes, request size limits, and output filtering so internal/sensitive fields never leak.
6. **Version from day one.** Choose a versioning strategy (URI `/v1`, header, or GraphQL schema evolution) and an explicit deprecation policy. Additive changes are non-breaking; for breaking changes use expand/contract: ship the new shape alongside the old, migrate consumers, then retire the old version with notice.
7. **Specify the spec artifact.** Write the contract as OpenAPI for REST, an SDL for GraphQL, `.proto` for gRPC, or a schema (e.g. JSON Schema/Avro) for events. The spec is the source of truth and should drive generated clients/server stubs and contract tests.
8. **Define non-functional behavior**: timeouts, retry/backoff guidance for clients, caching headers/TTLs, and observability (correlation/request IDs propagated end to end).
9. **Document examples and errors** for every operation: a sample request, success response, and the common error responses with their codes.
10. **Record** in `.claude/templates/api-spec.md` (`docs/api/`), commit the machine-readable spec, and hand off to implementation and to QA for contract tests.

## Standards
- **Do** keep contracts consistent: uniform naming, casing, pagination, error shape, and date/time format (ISO 8601 / UTC) across every endpoint.
- **Do** validate and sanitize all input at the boundary and return precise, non-leaky error messages.
- **Do** make writes idempotent where retries can occur, and use correct HTTP semantics (GET safe/idempotent, PUT idempotent, POST for non-idempotent creates).
- **Do** version explicitly and document deprecations with timelines.
- **Do** treat the spec (OpenAPI/SDL/proto/schema) as the single source of truth and test against it.
- **Do not** leak internal IDs, stack traces, or sensitive fields in responses or errors.
- **Do not** ship breaking changes onto an existing version; add a new version and migrate.
- **Do not** put auth as an afterthought — every operation states its required scope/role.
- **Do not** overfetch/underfetch by design flaws; give clients the shaping they need (fields/expand/GraphQL selection).

## Common mistakes to avoid
- Exposing the database schema directly as the API, coupling consumers to storage.
- Inconsistent error formats across endpoints, making client handling brittle.
- No pagination on collections that grow unbounded.
- Returning 200 for errors (status codes that don't reflect outcome) or leaking 500s with stack traces.
- Forgetting idempotency, so a retried payment or order creates duplicates.
- No versioning, so the first breaking change strands every consumer.
- Authz checked in some endpoints but silently missing in others (broken object-level authorization).

## Output format
A completed `.claude/templates/api-spec.md` plus a machine-readable spec under `docs/api/` (OpenAPI `openapi.yaml`, GraphQL `schema.graphql`, `.proto`, or event schemas). Each operation documents: purpose, auth/scope, request schema + validation, response schema, status/error codes, pagination, idempotency, rate limits, and an example request/response. Versioning and deprecation policy stated once at the top.

## Related checklists
- `.claude/checklists/security.md`
- `.claude/checklists/qa.md`
- `.claude/checklists/performance.md`

## Related agents
- `.claude/agents/core/solution-architect.md`
- `.claude/agents/engineering/api-architect.md`
- `.claude/agents/quality/security-auditor.md`
- `.claude/agents/quality/qa-engineer.md`

# API Checklist

API design, security, and contract gate — passing this proves the API is consistently versioned, correctly secured, fully specified, and safe for any client or integration partner to build against. Items are severity-tagged P0/P1/P2/P3.

## P0 — Blockers (must pass before any client consumes the API)

- [ ] Every endpoint has an explicit, consistent versioning scheme — URL path prefix (`/v1/`), request header (`API-Version: 2024-01`), or content-type negotiation — and the chosen strategy is documented in the API spec with a stated compatibility guarantee.
- [ ] Authentication is enforced on every non-public endpoint via a single, consistent mechanism (Bearer JWT with RS256/ES256, OAuth 2.0 with PKCE, or HMAC-signed API key); a mix of mechanisms across endpoints is prohibited without documented justification.
- [ ] Authorization is enforced server-side on every authenticated request: the server validates the caller's permissions against the resource owner before returning data; no endpoint relies on the client to filter its own data (IDOR check passes for all endpoints).
- [ ] All request inputs (path params, query params, headers, body fields) are validated before use: type, length, format, allowed values, and presence; unknown fields are rejected by default; validation errors return HTTP 422 with a field-level error envelope.
- [ ] Error responses follow a single, documented envelope schema (e.g., `{ "error": { "code": "string", "message": "string", "details": [...] } }`) and never leak stack traces, internal file paths, database error messages, or system architecture details.
- [ ] HTTP status codes are semantically correct and consistent across all endpoints: 200/201/204 for success, 400 for malformed requests, 401 for missing/invalid credentials, 403 for insufficient permissions, 404 for missing resources, 409 for state conflicts, 422 for semantic validation failures, 429 for rate limit exceeded, 500 for unexpected server faults.
- [ ] Rate limiting is applied to all public and authenticated endpoints with clearly defined limits per plan/tier; response headers (`Retry-After`, `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`) communicate the limit state on every response.
- [ ] A machine-readable schema is published and version-controlled alongside the code: OpenAPI 3.x for REST, AsyncAPI 2.x+ for event-driven, GraphQL SDL for GraphQL, or Protobuf/Thrift for RPC; client SDKs or type bindings are generated from the schema, never hand-written.
- [ ] All endpoints are covered by automated contract tests that run in CI; a PR that breaks a documented contract fails the build before it can be merged.
- [ ] Sensitive data (tokens, secrets, plaintext passwords, full PAN/CVV) is never returned in any response body, URL query parameter, or access log; responses containing PII are flagged in the schema with `x-sensitive: true`.

## P1 — Important (fix before external or third-party consumption)

- [ ] Breaking changes follow a documented deprecation policy: the deprecated version is supported for a defined sunset period (minimum 90 days for external partners), the sunset date is communicated in the `Sunset` and `Deprecation` response headers and the changelog, and clients receive advance notice.
- [ ] Every list endpoint implements pagination using cursor/keyset pagination for large or growing datasets; offset-based pagination is acceptable only with a documented maximum page size; unbounded queries that can return millions of rows are rejected at the API layer.
- [ ] Idempotency keys are supported on every mutating endpoint (POST, PATCH, PUT) that triggers a side effect (payment, email, resource provisioning, webhook delivery) to allow safe client retries; the idempotency key and the cached response are stored with a defined TTL.
- [ ] Webhooks and async callbacks include a request signature header (`X-Signature: HMAC-SHA256=...`) computed from the payload and a shared secret; the documentation provides a code sample for recipients to verify the signature before processing the event.
- [ ] CORS policy is explicitly configured with an origin allowlist — wildcard (`*`) is forbidden for any endpoint that accepts cookies or Authorization headers; preflight responses are cached with an appropriate `Access-Control-Max-Age`.
- [ ] File upload endpoints enforce MIME-type validation (magic-byte check, not only Content-Type header), maximum file-size limit returned as a 413 response, and antivirus/malware scanning before the file is persisted or made available to other users.
- [ ] API response times are measured in staging under representative load; endpoints that exceed the documented SLA (e.g., p95 < 300 ms) are either optimized or offloaded to async jobs with a status-polling or webhook pattern before any client is built against them.
- [ ] A changelog (`CHANGELOG.md` or equivalent in the API repository) records every breaking and non-breaking change per version with date, description, and migration guidance.
- [ ] API keys and OAuth tokens have a defined expiry; short-lived access tokens (≤ 1 h) are paired with refresh tokens; key rotation and revocation are supported via a self-service portal or API management endpoint.

## P2 — Hardening / nice-to-have

- [ ] A sandbox or mock environment with production-equivalent schemas is available for integration partners to develop and test against without using real production data or triggering live side effects.
- [ ] Request and response examples (not just schemas) are included in the OpenAPI/AsyncAPI spec for every operation, covering the happy path and at least one error case, so consumers do not need to guess the payload shape.
- [ ] Consumer-driven contract tests (Pact, or schema-based contract tests) are run in CI to catch breaking changes before they reach staging; providers publish their pacts to a broker, and provider verification is a required CI step.
- [ ] GraphQL schemas (where applicable) enforce query depth limits (`maxDepth`), complexity limits (`maxComplexity`), and field-level authorization (`@auth` directives or equivalent resolver guards) to prevent DoS via deeply nested or expensive queries.
- [ ] API observability is wired: request/response metrics (latency distribution, status code distribution, payload sizes) are tracked per endpoint in the monitoring platform; slow and error-prone endpoints are surfaced automatically in a dashboard.
- [ ] Hypermedia links or a consistent resource URL convention (`rel: "self"`, `rel: "next"`, `rel: "related"`) allow clients to navigate related resources without hard-coding paths, reducing coupling to the URL structure.

## P3 — Post-launch / backlog (track and revisit after launch; never blocks shipping)

- [ ] API observability dashboard is reviewed 4–8 weeks post-launch against real traffic; endpoints with p95 latency above the documented SLA or error rates above 0.1 % are assigned optimisation or async-offload tickets.
- [ ] Consumer-driven contract tests (Pact or schema-based) are introduced for every external integration partner that has gone live, ensuring their verified expectations are pinned in CI before the next breaking-change window opens.
- [ ] Deprecation sunset dates for any versions already marked deprecated at launch are actively monitored; partners still on deprecated versions 30 days before sunset receive direct outreach and migration support.
- [ ] Sandbox / mock environment schema drift relative to production is measured and corrected on a monthly cadence; any field, status code, or error envelope that diverged during the build phase is reconciled.
- [ ] Hypermedia links or consistent resource URL conventions are retrofitted to the highest-traffic endpoints identified post-launch to reduce client coupling ahead of the next major API version.

## How to use

Run after the API design is drafted using `.claude/templates/api-spec.md` and before the first client (web, mobile, third-party) begins integration. The primary agents are `.claude/agents/engineering/api-architect.md` and `.claude/agents/quality/security-auditor.md`. This gate is triggered by `.claude/commands/design-architecture.md` at the design stage and re-run for every new API version or breaking change. Reference `.claude/checklists/security.md` for additional input-validation, injection, and transport security controls. Mark each item `[x]` when verified or `[-]` when waived with a written justification and the approving engineer's name.

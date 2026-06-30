# API Integration Preset

## Project type
Software whose primary purpose is connecting two or more systems by translating, routing, or synchronising data between them — rather than presenting a UI or owning the primary data store. Variants: inbound webhook consumer, outbound webhook publisher, bidirectional data sync service, ETL/ELT pipeline, iPaaS connector, third-party API adapter, event bridge, reverse proxy with transformation, OAuth 2.0 token broker, or integration middleware layer embedded in a larger application.

## Typical use cases
- CRM ↔ marketing platform sync (contacts, deals, events)
- Payment gateway integration (Stripe, Adyen, PayPal — charge, webhook, refund, dispute flows)
- Identity / SSO federation (OAuth 2.0 authorization code flow, SAML assertion consumer)
- ERP ↔ e-commerce order and inventory sync
- Communication platform integrations (Slack bots, email providers, SMS gateways)
- Third-party data enrichment pipelines (append firmographic, location, or identity data)
- Outbound notification systems (email, push, in-app) routing through provider APIs
- IoT device telemetry ingestion from vendor APIs or MQTT brokers
- Webhook fanout — receive one inbound event and dispatch to N downstream systems

## Required discovery questions
1. Which external systems are involved, and which direction does data flow — inbound only, outbound only, or bidirectional with conflict resolution? Who is the system of record for each entity?
2. What authentication mechanisms do the external APIs require (OAuth 2.0, API key, HMAC-signed webhooks, mTLS, Basic Auth)? Who owns and rotates those credentials?
3. What are the reliability and consistency requirements — is eventual consistency acceptable, or must operations be exactly-once and strongly consistent? What is the acceptable data-loss window?
4. What event volumes are expected at launch and at 12-month scale? Are there burst patterns (end-of-day batch, campaign sends, billing cycle)?
5. How should the integration handle external API failures, rate limits, and partial failures — retry with backoff, dead-letter queue, manual intervention queue, or silent skip with alerting?
6. Is this integration business-critical (blocking customer transactions) or best-effort (analytics enrichment)? What is the acceptable downtime / lag SLA?
7. What data transformations are required between source and destination schemas? Is the mapping static or does it need to be configurable per customer / tenant?
8. Are there compliance constraints on the data flowing through the integration — PII that must not be logged, financial data under PCI scope, health data under HIPAA, or data that must not leave a geographic region?
9. Does the integration need observability beyond basic logging — per-event trace IDs, per-provider success/failure metrics, lag monitoring, or a replay/re-process capability?
10. Who owns and monitors this integration in production? Is there a human-readable audit trail requirement (e.g. "show me every record sent to Salesforce this week")?

## Recommended agents

### Core
- `.claude/agents/core/orchestrator.md` — integration scope governance, phased rollout by provider
- `.claude/agents/core/solution-architect.md` — message flow topology, idempotency model, error taxonomy
- `.claude/agents/core/business-analyst.md` — field-level mapping, business-rule clarification with stakeholders
- `.claude/agents/core/requirements-engineer.md` — contract between source and destination, edge-case enumeration

### Engineering
- `.claude/agents/engineering/backend-engineer.md` — request/response handling, retry logic, transformation code
- `.claude/agents/engineering/integration-engineer.md` — provider-specific SDK usage, webhook verification, OAuth flows
- `.claude/agents/engineering/api-architect.md` — inbound API surface design, idempotency key scheme, error schema
- `.claude/agents/engineering/data-engineer.md` — ETL pipelines, schema evolution, large-volume batch processing
- `.claude/agents/engineering/devops-engineer.md` — queue infrastructure, worker deployment, secret rotation automation

### Quality
- `.claude/agents/quality/qa-engineer.md` — contract testing against provider sandbox, retry scenario simulation
- `.claude/agents/quality/reliability-engineer.md` — lag monitoring, dead-letter alerting, replay procedures
- `.claude/agents/quality/security-auditor.md` — webhook signature verification, credential exposure, data-in-transit encryption
- `.claude/agents/quality/privacy-compliance-auditor.md` — PII in logs, data-residency constraints, cross-border transfer rules

### Domain
- `.claude/agents/domain/fintech-domain-expert.md` — payment and financial data integrations
- `.claude/agents/domain/saas-domain-expert.md` — CRM, billing, and SaaS platform integrations
- `.claude/agents/domain/ecommerce-domain-expert.md` — order, inventory, and fulfilment integrations

## Recommended skills
- `.claude/skills/api-design/SKILL.md` — inbound endpoint conventions, idempotency keys, webhook payload schema
- `.claude/skills/backend/SKILL.md` — retry with exponential backoff, dead-letter queues, saga/outbox patterns
- `.claude/skills/security/SKILL.md` — HMAC webhook verification, OAuth token storage, secrets management
- `.claude/skills/data-modeling/SKILL.md` — event schema design, idempotency tables, sync-state tracking
- `.claude/skills/testing/SKILL.md` — provider sandbox testing, contract tests, chaos/failure injection
- `.claude/skills/production-readiness/SKILL.md` — per-event tracing, provider-latency metrics, dead-letter alerting
- `.claude/skills/devops/SKILL.md` — queue worker deployment, secret rotation, environment parity

## Recommended stack options

| Stack | Rationale |
|---|---|
| **Node.js (Fastify/Hono) + BullMQ + PostgreSQL + Redis** | Excellent async I/O for webhook-heavy workloads; BullMQ provides durable queues with retry, delay, and dead-letter; Redis for fast idempotency-key lookups. See `.claude/stack-matrix/backend.md` |
| **Python (FastAPI + Celery) + PostgreSQL + Redis** | Natural fit when the team is Python-primary or integrating ML/data APIs; Celery handles background workers; strong SDK ecosystem for most SaaS providers |
| **Go (stdlib + pgx) + NATS or Kafka** | Best for very high throughput event pipelines; minimal memory footprint per worker; excellent concurrency primitives; favoured for infrastructure-level integrations |
| **Temporal (workflow engine) + any language worker** | Purpose-built for long-running, multi-step integration workflows with built-in retry, activity history, and exactly-once semantics; reduces custom saga logic significantly |

Reference `.claude/stack-matrix/backend.md`, `.claude/stack-matrix/realtime.md`, `.claude/stack-matrix/cloud-devops.md` for queue, messaging, and deployment tradeoffs.

## Required checklists
- `.claude/checklists/security.md` — webhook signature verification, credential storage, PII-in-logs audit, mTLS where required
- `.claude/checklists/api.md` — idempotency on all write operations, consistent error schema, versioning strategy
- `.claude/checklists/backend.md` — retry policy, dead-letter queue, graceful shutdown, connection pool limits
- `.claude/checklists/production.md` — per-provider metrics, lag alerting, dead-letter alerting, replay procedure documented
- `.claude/checklists/launch.md` — sandbox-to-production credential swap verified, rate limits confirmed, rollback plan

## MVP scope pattern

**In MVP**
- Single provider integration end-to-end (happy path + most common error paths)
- Webhook signature verification (if inbound webhooks)
- Idempotency key stored and checked on all write operations
- Durable queue with at least one retry with exponential backoff
- Dead-letter queue with alerting when messages land there
- Structured logging with per-event trace/correlation ID
- Secrets loaded from environment / secrets manager — never hardcoded
- Provider sandbox tested; credential rotation procedure documented

**Deferred to v2**
- Multi-tenant credential management (per-customer API keys)
- Self-service integration configuration UI
- Bidirectional sync with conflict resolution (start with one direction)
- Replay / reprocess UI for dead-letter messages
- Additional providers beyond the first (design for extensibility, build one first)
- Per-customer rate-limit accounting
- Webhook fanout to N downstream targets
- Full audit-trail query UI (logs-based query is sufficient at MVP)

## Production risks

| Risk | Severity | Mitigation |
|---|---|---|
| Webhook signature not verified — spoofed events trigger state changes | P0 | Verify HMAC or RSA signature on every inbound webhook before processing; reject and log all failures; return 400 not 200 on invalid signatures |
| Credentials (API keys, OAuth tokens) committed to source control or emitted in logs | P0 | Secrets manager for all credentials; log scrubbing to redact `Authorization` headers and token fields; gitleaks in pre-commit |
| Duplicate event processed twice — double charges, double sends, phantom records | P0 | Idempotency key (provider event ID or deterministic hash) stored in DB with unique constraint; check before processing; return 200 on duplicate without reprocessing |
| Infinite retry loop filling queue and hitting provider rate limit | P0 | Cap retry count (e.g. max 5); exponential backoff with jitter; route to dead-letter after max retries; alert on dead-letter depth |
| PII flowing through logs or error messages to observability platform | P0 | Structured log fields for IDs only; scrub email, phone, SSN, card fields before any log.info/error call; validate with log-sampling audit |
| Partial failure leaves source and destination out of sync with no reconciliation path | P1 | Transactional outbox pattern or saga with compensating transactions; daily reconciliation job comparing record counts/checksums |
| Provider API breaking change silently corrupting data | P1 | Pin provider SDK versions; test against provider changelog on each SDK upgrade; schema validation on inbound payloads before processing |
| No alerting on queue lag — backlog grows undetected | P1 | Alert when queue depth > threshold or oldest-message age exceeds SLA; separate alert for dead-letter receiving any message |
| OAuth token expiry causing silent integration failures | P1 | Proactive token refresh before expiry; alert on refresh failure; test token-expiry path in CI against provider sandbox |
| Rate limit breach causing 429s that silently drop events | P1 | Honour `Retry-After` headers; implement per-provider rate-limit budget tracking; backpressure to queue rather than discard |
| No rollback path when a bad transformation ships to production | P2 | Feature flag per provider; replay from dead-letter or re-fetch from source API; transformation version stored alongside each processed event record |

## Launch requirements
- Webhook signature verification tested with real provider-signed payloads (not only mocked)
- Idempotency confirmed: sending the same event payload twice produces exactly one state change in the destination
- Dead-letter alerting fires and reaches on-call channel within 5 minutes of a message landing there
- OAuth token refresh cycle tested end-to-end including token expiry simulation
- All secrets loaded from secrets manager in production environment; no plaintext credentials in config files or environment variable files committed to VCS
- Per-event correlation ID visible in logs, traceable from inbound receipt to destination confirmation
- Provider sandbox swapped for production credentials and a real end-to-end transaction confirmed in production (smoke test)
- Rate limits for each provider documented; queue worker concurrency tuned to stay within limits at expected peak volume
- Runbook in `docs/runbook.md` covering: how to replay dead-letter messages, how to rotate provider credentials, how to disable a specific provider without a code deploy
- Data classification confirmed: any PII fields identified, logging exclusions in place, cross-border transfer legality confirmed with compliance owner

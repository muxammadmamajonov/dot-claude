# Automation / Workflow Tool Preset

## Project type

A system that executes sequences of actions in response to triggers, connecting disparate services, APIs, and data sources without manual intervention. Encompasses no-code/low-code workflow builders, integration platforms (iPaaS), robotic-process automation (RPA), event-driven automation, CI/CD pipelines, scheduled job runners, business-process automation, and custom internal tools that wire together SaaS products. The defining characteristic is: **trigger → condition evaluation → action sequence → outcome**, often across third-party service boundaries.

---

## Typical use cases

- Internal workflow automation (approval flows, notifications, data sync between systems)
- iPaaS / integration platform (connect CRM, ERP, email, Slack, payments, storage)
- No-code / low-code workflow builder product (end users define triggers and actions via a UI)
- Scheduled report generation and distribution
- Event-driven microservice orchestration (webhook in → transform → webhook/API out)
- RPA for legacy systems without APIs (browser/desktop automation)
- CI/CD and DevOps automation pipeline
- Data sync / reverse ETL (warehouse → CRM / marketing automation)
- Customer onboarding orchestration (send email → wait → check condition → branch → next action)
- Business-process automation (invoicing, HR workflows, compliance sign-offs)

---

## Required discovery questions

1. **Trigger types** — What initiates a workflow? (Webhook, cron/schedule, database event/CDC, message queue, file drop, API poll, user action, inbound email.) The trigger type drives the ingestion architecture.
2. **Action set** — What does the automation do? (Call APIs, write to a database, send notifications, transform data, spawn sub-workflows, wait for human approval, run code.) Each action type is a separate integration surface.
3. **User type building workflows** — Are workflows defined by developers (code/YAML), technical power users (low-code with a builder UI), or non-technical business users (no-code drag-and-drop)? This determines the entire UX and configuration model.
4. **Volume and throughput** — How many workflow executions per day? What is the peak burst (e.g. thousands of webhooks in a second from a payment processor event)? What is the maximum acceptable latency from trigger to first action?
5. **Error handling and retry policy** — What happens when an action step fails? Retry with backoff, dead-letter queue, alert to a human, or stop the workflow? Are partial completions acceptable, or must workflows be all-or-nothing?
6. **Idempotency requirements** — If a trigger fires twice (webhook replay, at-least-once delivery), does the automation run twice or deduplicate? Duplicate prevention is critical for actions with side effects (charge a card, send an email).
7. **Long-running and async workflows** — Do workflows need to wait for external events (human approval, async API callback) that may take hours or days? Long-running workflows require a durable execution engine (Temporal, Conductor, AWS Step Functions).
8. **Secret and credential management** — Workflows authenticate to external services. How are credentials stored, rotated, and scoped? Per-user credentials (OAuth), per-team, or per-workspace?
9. **Auditability and compliance** — Must every workflow execution be logged with inputs, outputs, timestamps, and actor? Is there a regulated industry context (financial services, healthcare, SOC 2)?
10. **Multi-tenancy** — Is this a product serving multiple customers (each with their own workflows, credentials, and data), or an internal tool for one organisation? Multi-tenancy adds isolation, billing, and permission complexity.

---

## Recommended agents

**Core**
- `.claude/agents/core/orchestrator.md` — drives the 9-stage flow; automation tools are deceptively complex to spec correctly
- `.claude/agents/core/solution-architect.md` — execution engine design, trigger ingestion, action runner, state machine model, retry/DLQ design
- `.claude/agents/core/requirements-engineer.md` — workflow DSL or schema design, trigger contracts, action interface specs

**Engineering**
- `.claude/agents/engineering/backend-engineer.md` — workflow execution engine, API layer, scheduler, job queue
- `.claude/agents/engineering/integration-engineer.md` — third-party API connectors, OAuth flows, webhook ingestion, data transformation
- `.claude/agents/engineering/frontend-engineer.md` — workflow builder UI (if no-code/low-code product), execution log viewer, connector configuration forms
- `.claude/agents/engineering/realtime-engineer.md` — event-driven ingestion at high throughput (Kafka, SQS, EventBridge)
- `.claude/agents/engineering/devops-engineer.md` — job runner infrastructure, worker scaling, secret management, observability

**Quality**
- `.claude/agents/quality/qa-engineer.md` — workflow replay tests, idempotency tests, failure and retry scenario tests
- `.claude/agents/quality/security-auditor.md` — credential storage, SSRF via webhook URLs, action permission scope, tenant isolation

**Domain**
- `.claude/agents/domain/automation-domain-expert.md` — workflow patterns, connector catalogue design, error-handling UX, version management

---

## Recommended skills

- `.claude/skills/node-backend/SKILL.md` — Node.js/TypeScript is the dominant runtime for automation tools (Zapier, Make, n8n are all Node-based)
- `.claude/skills/python-backend/SKILL.md` — Python for data-heavy or AI-augmented automation workflows
- `.claude/skills/go-backend/SKILL.md` — Go for high-throughput, low-latency trigger ingestion workers
- `.claude/skills/redis/SKILL.md` — job queue (BullMQ), idempotency key store, rate limiting per connector, short-term execution state
- `.claude/skills/postgres/SKILL.md` — workflow definitions, execution history, audit log, credential store metadata
- `.claude/skills/security/SKILL.md` — credential encryption at rest, OAuth 2.0 / token refresh, SSRF prevention on user-supplied URLs, tenant isolation
- `.claude/skills/devops/SKILL.md` — worker auto-scaling, queue depth alerting, canary deploy for new connector versions
- `.claude/skills/testing/SKILL.md` — workflow replay harness, connector mock server, idempotency regression tests

---

## Recommended stack options

| Stack | Rationale |
|---|---|
| **Node.js/TypeScript + BullMQ (Redis) + PostgreSQL + n8n (embedded or self-hosted)** | Proven automation-tool stack; BullMQ provides durable job queues with retry; n8n can be embedded or used as a reference; TypeScript gives typed connector interfaces. |
| **Python + Temporal + PostgreSQL + FastAPI** | Temporal provides durable workflow execution with replay, versioning, and long-running activity support; best for complex business-process automation with async waits and human-in-the-loop steps. |
| **Node.js + AWS Step Functions + SQS + Lambda + Secrets Manager** | Fully managed; Step Functions handles state, retries, and branching; SQS provides at-least-once delivery with deduplication; Lambda scales to zero; best for AWS-native teams. |
| **Go + Kafka + Kubernetes + CockroachDB** | Maximum throughput for event-driven automation at scale; Kafka as the durable event log; Go workers for low-latency action execution; CockroachDB for globally distributed execution state. |

---

## Required checklists

- `.claude/checklists/security.md` — credential encryption at rest and in transit, SSRF prevention on webhook/URL inputs, OAuth token scoping, tenant data isolation, audit log completeness
- `.claude/checklists/performance.md` — trigger-to-execution latency p50/p95/p99, queue depth under peak load, worker throughput, database connection pool sizing
- `.claude/checklists/qa.md` — idempotency verified (duplicate trigger → no duplicate side effect), retry tested at every step, dead-letter queue drainable, long-running workflow survives worker restart
- `.claude/checklists/production.md` — queue depth alerting, worker auto-scaling, dead-letter queue monitoring, runbook for stuck workflows, credential rotation procedure

---

## MVP scope pattern

**In the first cut**
- One trigger type (e.g. webhook) and two to three action types (e.g. HTTP request, send email, write to database)
- Linear workflow execution (no branching or conditionals in MVP; add branches in v2)
- Synchronous execution for short workflows (< 30 s); async job queue for anything longer
- Per-step retry with configurable backoff and a dead-letter queue for failed workflows
- Basic execution log: trigger received, each step outcome, final status — queryable by execution ID
- Idempotency key on webhook ingestion: duplicate webhook replays do not re-execute the workflow
- Credential storage: encrypted at rest, referenced by ID in workflow definitions — never stored in workflow config plaintext

**Defer until post-MVP**
- Branching / conditional logic (design the DSL to support it; implement the UI/runtime for branches in v2)
- Long-running async workflows with durable waits (design with Temporal in mind; stub the wait step)
- No-code workflow builder UI (JSON/YAML-defined workflows first; visual builder after execution engine is solid)
- Large connector catalogue (two or three connectors MVP; build a connector SDK so adding more is self-service)
- Per-tenant rate limiting and quota enforcement (build the data model for it from day one; enforce in v2)
- Workflow versioning and rollback (define version field in workflow schema from day one; implement migration in v2)
- Webhook signature validation for all ingested webhooks (implement for MVP connectors; enforce broadly in v2)

---

## Production risks

| Risk | Priority | Mitigation |
|---|---|---|
| Duplicate side effects from at-least-once webhook delivery | P0 | Idempotency key extracted from webhook payload and stored; deduplicate before enqueuing; idempotency window configurable per connector |
| SSRF — user-configures a workflow action that calls internal infrastructure URLs | P0 | Validate and block private/loopback IP ranges and internal DNS names for all user-supplied URLs; use an allowlist for connector target domains |
| Credentials stored or logged in plaintext | P0 | Encrypt all OAuth tokens and API keys with a KMS key at rest; never log credential values; store only the reference ID in workflow configs and execution logs |
| Tenant data isolation failure — one tenant's workflow reads another's data | P0 | Enforce tenant ID on every database query; row-level security at the DB layer; separate credential namespaces per tenant; audit in `.claude/checklists/security.md` |
| Runaway retry loop consuming all queue capacity | P0 | Max retry count per step; exponential backoff with jitter; dead-letter queue after max retries; alert on DLQ depth |
| Worker crash mid-execution leaves workflow in unknown state | P1 | Job queue heartbeat / visibility timeout; worker marks step as "in-progress" before executing; on timeout, re-queue the step for a new worker |
| Long-running workflow lost on deploy restart | P1 | Durable execution engine (Temporal, Step Functions) persists state externally; or: checkpoint step completion to DB before acknowledging queue message |
| Connector API breaking change silently corrupts downstream workflow outputs | P1 | Connector version pinning; integration tests run against connector API on a schedule; alert on unexpected response schema changes |
| OAuth token expiry mid-workflow | P1 | Proactive token refresh before expiry; refresh-on-401 with retry; alert when refresh fails so user can re-authorise |
| No audit trail for compliance — "who triggered this workflow and what did it do?" | P1 | Immutable append-only execution log (actor, trigger payload hash, each step input/output, timestamps); retained per compliance policy |

---

## Launch requirements

- All items in `.claude/checklists/production.md` are green
- Idempotency end-to-end tested: send the same webhook 5 times → exactly one workflow execution and one side effect
- SSRF prevention tested: attempt to configure an action pointing to `169.254.169.254` (AWS metadata), `localhost`, and internal hostname — all blocked
- Credential security verified: credentials not present in execution logs, application logs, or error messages; encryption at rest confirmed
- Retry and dead-letter queue tested: inject step failure at 100% rate → max retries exhausted → job lands in DLQ → DLQ drain procedure confirmed
- Peak load tested: queue and workers handle 2× expected peak trigger rate without lag exceeding SLA
- Tenant isolation verified: tenant A's execution cannot read or affect tenant B's data or credentials
- Audit log complete for all executions in staging: trigger, actor, each step input/output, timestamps, final status
- OAuth token refresh tested: revoke token mid-workflow → refresh fires → workflow continues without user intervention
- Worker restart mid-execution tested: kill worker → workflow resumes correctly from last completed step on new worker
- All P0/P1 bugs resolved; P2 triaged
- Runbooks complete: stuck workflow resolution, DLQ drain, credential rotation, connector version rollback
- Monitoring active: queue depth, DLQ depth, execution latency p95, step error rate, worker CPU — all with alerting thresholds

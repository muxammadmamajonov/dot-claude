# Helpdesk / Support System Preset

## Project type

Customer and internal support platform. Centralises incoming support requests across channels (email, chat, web form, phone, social), routes them to agents, tracks SLAs, and closes the feedback loop with customers. Variants range from a simple shared inbox to an omnichannel enterprise support suite with AI deflection, ITSM workflows, and a knowledge base.

Common variants:
- **External customer support** — B2C or B2B ticket management, SLA tracking, CSAT
- **Internal IT helpdesk (ITSM)** — incident, problem, change, asset management (ITIL-aligned)
- **Shared inbox / team inbox** — lightweight routing without full ticketing ceremony
- **Embedded support widget** — in-product chat/ticket creation integrated into a host SaaS
- **AI-first deflection system** — LLM-powered self-service with escalation to human agents
- **Field service dispatch** — ticket → technician assignment → on-site resolution → sign-off

---

## Typical use cases

- Ticket lifecycle: open → triaged → assigned → in-progress → pending customer → resolved → closed
- Multi-channel ingestion: email-to-ticket parsing, web form, live chat, WhatsApp, social DMs
- SLA enforcement: response-time and resolution-time targets with breach alerts and escalation
- Queue management: routing rules (skill-based, round-robin, load-balanced, priority-based)
- Knowledge base / help centre: article authoring, search, article-attach-to-ticket workflow
- Macro / canned response library for common issues
- CSAT / NPS survey dispatch on ticket close
- Reporting: ticket volume, SLA compliance, first-contact resolution, agent handle time, CSAT score
- ITSM: incident severity tiers, change advisory board (CAB) workflow, CMDB asset linking

---

## Required discovery questions

1. **Who submits tickets — external customers, internal employees, or both?** — determines authentication model (anonymous/email vs. SSO/LDAP), data sensitivity, and compliance scope.
2. **Which inbound channels must be supported at launch?** (email, web form, live chat, WhatsApp, phone transcript, social) — each channel has distinct ingestion complexity.
3. **What SLA commitments exist, and how are they tiered?** (e.g., P1 respond in 1 h / resolve in 4 h; P2 respond in 4 h / resolve in 1 business day) — SLA engine is a core scheduling challenge.
4. **Is a knowledge base / self-service portal required, and does it need AI-powered search or deflection?** — doubles scope if yes.
5. **How are tickets routed — manual triage, rule-based automation, or ML-based?** — determines workflow engine complexity.
6. **What integrations are required on day one?** (CRM for customer context, monitoring/alerting for auto-ticket creation, Slack/Teams for agent notifications, Jira/GitHub for bug escalation) — each adds scope.
7. **What compliance or data-residency obligations apply?** (GDPR right-to-erasure on customer communication history, HIPAA for healthcare support, SOC 2 for internal ITSM) — shapes data retention, encryption, and erasure workflows.
8. **Are there multiple support teams or departments sharing one system?** (IT, finance, HR, customer success) — determines multi-team isolation, separate queues, cross-team visibility rules.
9. **What does "reporting" need to cover?** (real-time queue dashboard for team leads vs. executive weekly digest vs. custom BI) — sizes analytics layer.
10. **Is there an existing ticketing system in use, and does historical ticket data need migrating?** — migration from Zendesk/Freshdesk/Jira Service Management is a distinct work stream.

---

## Recommended agents

### Core
- `.claude/agents/core/orchestrator.md`
- `.claude/agents/core/solution-architect.md`
- `.claude/agents/core/requirements-engineer.md`
- `.claude/agents/core/business-analyst.md`
- `.claude/agents/core/product-manager.md`

### Engineering
- `.claude/agents/engineering/backend-engineer.md`
- `.claude/agents/engineering/frontend-engineer.md`
- `.claude/agents/engineering/realtime-engineer.md`
- `.claude/agents/engineering/api-architect.md`
- `.claude/agents/engineering/integration-engineer.md`
- `.claude/agents/engineering/search-engineer.md`

### Quality
- `.claude/agents/quality/security-auditor.md`
- `.claude/agents/quality/qa-engineer.md`
- `.claude/agents/quality/privacy-compliance-auditor.md`
- `.claude/agents/quality/performance-engineer.md`
- `.claude/agents/quality/reliability-engineer.md`
- `.claude/agents/quality/production-readiness-auditor.md`

### Design
- `.claude/agents/design/ui-ux-designer.md`
- `.claude/agents/design/accessibility-designer.md`

### Domain
- `.claude/agents/domain/helpdesk-domain-expert.md`
- `.claude/agents/domain/saas-domain-expert.md` *(if multi-tenant)*

### Stack
- `.claude/agents/stack/backend/node-nest-fastify-engineer.md` or `.claude/agents/stack/backend/python-fastapi-django-engineer.md`
- `.claude/agents/stack/web/react-next-engineer.md`
- `.claude/agents/stack/database/postgres-engineer.md`

---

## Recommended skills

- `.claude/skills/backend/SKILL.md` — SLA timer logic, queue-drain workers, email parsing
- `.claude/skills/data-modeling/SKILL.md` — ticket, comment, attachment, SLA breach, audit event schema
- `.claude/skills/api-design/SKILL.md` — webhook inbound (email provider, chat platform) and outbound (integrations)
- `.claude/skills/redis/SKILL.md` — real-time queue metrics, presence (agent online status), rate limiting
- `.claude/skills/postgres/SKILL.md` — full-text search on ticket body/title, SLA deadline indexing
- `.claude/skills/security/SKILL.md` — attachment scanning, PII redaction, customer data isolation
- `.claude/skills/testing/SKILL.md` — SLA timer accuracy tests, routing rule determinism tests
- `.claude/skills/performance/SKILL.md` — inbox list query performance, real-time agent dashboard
- `.claude/skills/production-readiness/SKILL.md`
- `.claude/skills/requirements-engineering/SKILL.md`

---

## Recommended stack options

| Stack | Rationale |
|---|---|
| **Node/NestJS + PostgreSQL + Redis + React** | Event-driven architecture suits ticket ingestion; NestJS queues handle email/chat adapters; WebSocket support for live chat; Redis pub/sub for real-time agent dashboard. See `.claude/stack-matrix/backend.md`. |
| **Python/Django + PostgreSQL + Celery + React** | Django's admin is useful for internal ITSM configuration; Celery handles SLA timer jobs and notification dispatch; strong email parsing libraries. See `.claude/stack-matrix/backend.md`. |
| **Ruby on Rails + PostgreSQL + Sidekiq + React** | Proven pattern (Zendesk-style); ActiveJob/Sidekiq for background SLA enforcement; Action Cable for real-time updates; fastest time-to-working for standard ticket workflows. |
| **Go + PostgreSQL + Redis + React** | High-throughput inbound channel processing (email/webhook flood); low memory footprint per goroutine suits concurrent ticket ingestion at scale. See `.claude/stack-matrix/backend.md`. |

---

## Required checklists

- `.claude/checklists/security.md` — emphasize: attachment malware scanning, customer PII isolation, GDPR erasure on ticket history, webhook signature validation for inbound channels
- `.claude/checklists/qa.md` — SLA timer accuracy, routing rule coverage, email-to-ticket parse correctness
- `.claude/checklists/performance.md` — inbox list <150 ms p95; real-time dashboard latency <500 ms; SLA breach alert fires within 60 s of deadline
- `.claude/checklists/accessibility.md` — agent UI used all day; full keyboard nav and screen reader support required
- `.claude/checklists/production.md`
- `.claude/checklists/launch.md`

---

## MVP scope pattern

**In the first cut:**
- Ticket CRUD: create, view, comment, assign, status transitions, close
- Email inbound channel: parse incoming emails into tickets (one mailbox)
- Web form inbound channel
- Manual agent assignment; basic team/queue concept
- Single SLA tier with breach alert to agent and team lead
- Canned responses (macro) library
- Customer notification emails on ticket open, reply, and close
- CSAT survey on close (single-question rating)
- Basic reports: open ticket count by queue, SLA compliance %, average resolution time
- Agent web UI; customer-facing ticket portal (view own tickets, reply)

**Deferred to later iterations:**
- Additional channels (live chat, WhatsApp, social, phone transcript)
- Knowledge base / self-service portal
- AI deflection / suggested articles / auto-response
- Multiple SLA tiers and SLA policies by customer segment
- Skill-based and ML-powered routing
- ITSM modules (change management, CMDB, problem management)
- Jira/GitHub bug escalation integration
- CRM integration for customer context panel
- Slack/Teams notification integration
- Custom report builder
- Mobile app for agents
- Multi-brand / multi-department isolation with separate portals

---

## Production risks

| Risk | Severity | Mitigation |
|---|---|---|
| SLA breach alert fires late or not at all | **P0** | SLA deadline stored in DB; background job runs every minute to check; test with accelerated time in CI; alert if job itself is delayed |
| Email ingestion failure silently drops customer tickets | **P0** | Dead-letter queue for failed parses; daily gap report comparing inbound email count to ticket count; customer auto-acknowledgement confirms receipt |
| Customer data visible to wrong tenant / team | **P0** | `org_id` scoping on every query; multi-tenant integration tests; no cross-org joins possible at ORM layer |
| Malicious attachment reaches agent browser or storage | **P0** | Scan attachments before storage (ClamAV or cloud AV API); serve via signed URL with content-type enforcement; block executable extensions |
| GDPR erasure request cannot be fulfilled because PII lives in email body stored verbatim | **P1** | Store email body as a structured scrubable object; erasure job replaces PII fields with tombstone token; log erasure completion |
| High email volume spike floods ingestion queue | **P1** | Rate-limit inbound processing; horizontal queue workers; circuit breaker; queue depth alert |
| Agent real-time dashboard stale during high load | **P1** | Decouple dashboard metrics from OLTP path; publish to Redis channel; fallback to polling if WebSocket drops |
| Knowledge base articles returned as irrelevant by search | **P2** | Weight recent, high-resolution-rate articles; monitor zero-result search queries; allow agents to flag poor suggestions |
| Notification email lands in spam, customer misses resolution | **P2** | Configure SPF/DKIM/DMARC on sending domain; use reputable transactional email provider; monitor bounce/spam rates |

---

## Launch requirements

- [ ] Email-to-ticket ingestion tested with 1 000 synthetic emails including malformed and attachment-bearing messages
- [ ] SLA timer accuracy verified: breach alert fires within 60 s of deadline in load test
- [ ] Cross-tenant data isolation verified: agent from org A cannot access org B tickets
- [ ] Attachment scanning confirmed active; executable upload rejected
- [ ] GDPR erasure flow tested end-to-end: ticket history scrubbed, erasure logged
- [ ] Customer notification emails delivered with SPF/DKIM passing (check mail-tester.com score)
- [ ] CSAT survey delivery and response recording confirmed
- [ ] Performance baseline: inbox list <150 ms p95 at expected queue depth
- [ ] Agent UI keyboard navigation and screen reader tested
- [ ] Runbook written: on-call escalation, queue drain procedure, email provider failover
- [ ] Database backup and restore verified on staging
- [ ] Security checklist `.claude/checklists/security.md` fully green

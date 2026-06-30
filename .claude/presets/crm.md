# CRM Preset

## Project type

Customer Relationship Management system. Manages contacts, companies, deals/opportunities, activities, pipelines, and communications in one place. Variants range from lightweight contact managers to full-blown sales-force-automation (SFA) platforms with marketing automation, service modules, and AI-assisted scoring.

Common variants:
- **Sales CRM** — pipeline stages, deal tracking, forecasting, quota management
- **Marketing CRM** — campaign tracking, lead scoring, segmentation, nurture workflows
- **Service/Support CRM** — case management linked to contacts (overlaps with helpdesk preset)
- **Operational CRM** — deep workflow automation: sequences, tasks, reminders, integrations
- **Embedded/white-label CRM** — CRM capabilities surfaced inside a host product (SaaS, ERP, marketplace)

---

## Typical use cases

- Sales teams tracking leads → prospects → customers through configurable pipeline stages
- Account management: relationship history, notes, calls, emails, meetings per contact/company
- Revenue forecasting from weighted deal values across pipeline stages
- Marketing attribution: source tracking, campaign ROI, UTM → deal linkage
- Automated follow-up sequences: tasks, emails, reminders triggered by time or stage change
- Reporting: win/loss analysis, rep performance, cycle time, conversion rates by stage
- Integration hub: sync with email (Gmail/Outlook), calendar, telephony, ERP, billing

---

## Required discovery questions

1. **Who are the primary users?** (sales reps, account managers, marketing, customer success, leadership with read-only views) — drives role/permission model complexity.
2. **What is the primary sales motion?** (B2B outbound, B2B inbound, B2C, PLG, channel/partner) — determines pipeline shape, deal object fields, and whether contacts or accounts are the top-level entity.
3. **Does the CRM need to own communication, or integrate with existing tools?** (send email/SMS natively vs. log from Gmail/Outlook/Twilio) — biggest build-vs-integrate decision.
4. **What data will be imported on day one, and from where?** (existing spreadsheets, Salesforce/HubSpot export, ERP) — determines migration complexity and field mapping requirements.
5. **What compliance obligations apply?** (GDPR right-to-erasure on contact data, CCPA opt-outs, CAN-SPAM for email, data residency requirements) — shapes PII storage, consent records, and soft-delete strategy.
6. **How many users, contacts, and companies at launch vs. 12-month target?** — sizes the search/indexing and query performance budget.
7. **Is multi-tenancy required?** (SaaS with multiple customer orgs vs. single-org internal tool) — the highest-impact architectural fork.
8. **What are the must-have pipeline customizations?** (custom fields, multiple pipelines, conditional stage rules) — determines whether the data model is fixed or dynamic/EAV.
9. **What integrations are contractually required at launch?** (email provider, calendar, ERP, billing, phone/VoIP) — each is a distinct scope item.
10. **What does "reporting" mean?** (built-in dashboards only, embed BI tool, export to spreadsheet, real-time board) — drives data warehouse vs. OLTP-only decision.

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
- `.claude/agents/engineering/database-architect.md`
- `.claude/agents/engineering/api-architect.md`
- `.claude/agents/engineering/integration-engineer.md`
- `.claude/agents/engineering/search-engineer.md`
- `.claude/agents/engineering/realtime-engineer.md`

### Quality
- `.claude/agents/quality/security-auditor.md`
- `.claude/agents/quality/qa-engineer.md`
- `.claude/agents/quality/privacy-compliance-auditor.md`
- `.claude/agents/quality/performance-engineer.md`
- `.claude/agents/quality/production-readiness-auditor.md`

### Design
- `.claude/agents/design/ui-ux-designer.md`
- `.claude/agents/design/accessibility-designer.md`

### Domain
- `.claude/agents/domain/crm-domain-expert.md`
- `.claude/agents/domain/saas-domain-expert.md` *(if multi-tenant SaaS)*

### Stack
- `.claude/agents/stack/backend/node-nest-fastify-engineer.md` or `.claude/agents/stack/backend/python-fastapi-django-engineer.md`
- `.claude/agents/stack/web/react-next-engineer.md` or `.claude/agents/stack/web/vue-nuxt-engineer.md`
- `.claude/agents/stack/database/postgres-engineer.md`

---

## Recommended skills

- `.claude/skills/data-modeling/SKILL.md` — entity relationship design (Contact, Company, Deal, Activity, User, Team)
- `.claude/skills/api-design/SKILL.md` — REST + webhook contracts for integrations
- `.claude/skills/security/SKILL.md` — row-level security, PII encryption at rest, GDPR erasure
- `.claude/skills/backend/SKILL.md`
- `.claude/skills/postgres/SKILL.md` — JSONB for custom fields, full-text search, partitioning for activity logs
- `.claude/skills/redis/SKILL.md` — session cache, rate limiting, real-time notification queuing
- `.claude/skills/requirements-engineering/SKILL.md`
- `.claude/skills/testing/SKILL.md`
- `.claude/skills/performance/SKILL.md`
- `.claude/skills/production-readiness/SKILL.md`

---

## Recommended stack options

| Stack | Rationale |
|---|---|
| **Next.js + Node/NestJS + PostgreSQL + Redis** | Full-stack TypeScript end-to-end; NestJS modules map cleanly to CRM domains; Postgres JSONB handles custom fields; strong ecosystem for email/calendar integrations. See `.claude/stack-matrix/backend.md`. |
| **React + Python/FastAPI + PostgreSQL + Celery** | FastAPI is fast to prototype; Celery handles async email/notification pipelines; Python has rich ML libraries for lead scoring. See `.claude/stack-matrix/backend.md`. |
| **Vue/Nuxt + Laravel + PostgreSQL + Queues** | Laravel's Eloquent ORM and built-in queue system accelerate CRUD-heavy CRM work; strong PHP ecosystem for Salesforce/HubSpot connectors. See `.claude/stack-matrix/backend.md`. |
| **React + Ruby on Rails + PostgreSQL** | Rails conventions speed up standard CRM CRUD; ActiveRecord associations mirror the Contact→Company→Deal graph naturally; mature gem ecosystem for integrations. |

---

## Required checklists

- `.claude/checklists/security.md` — emphasize: row-level tenant isolation, PII at-rest encryption, OAuth token storage, webhook signature validation
- `.claude/checklists/qa.md`
- `.claude/checklists/performance.md` — contact list queries with filters must return < 200 ms at 100 k+ records
- `.claude/checklists/accessibility.md` — sales reps use the product all day; keyboard navigation and screen reader support are non-optional
- `.claude/checklists/production.md`
- `.claude/checklists/launch.md`

---

## MVP scope pattern

**In the first cut:**
- Contact + Company entities with standard field set
- Single configurable sales pipeline with deal stages
- Activity log (notes, calls, emails — manual entry)
- Basic user + role model (admin, rep, read-only)
- List/filter view with search
- Simple dashboard: deals by stage, total pipeline value
- CSV import for initial data load
- Email notifications for task due dates

**Deferred to later iterations:**
- Multiple pipelines; custom field builder (EAV)
- Email send/receive integration (Gmail OAuth, Outlook Graph)
- Calendar sync
- Automated sequences and workflows
- Lead scoring / AI assistant
- Revenue forecasting with weighted projections
- Advanced reporting / BI embed
- Mobile apps
- Partner/channel portal
- Public API + webhook outbound delivery
- Multi-tenant SaaS billing layer

---

## Production risks

| Risk | Severity | Mitigation |
|---|---|---|
| Tenant data leakage in multi-tenant SaaS | **P0** | Row-level security on every query; enforce `org_id` filter at ORM/middleware layer; integration test with a second tenant on every endpoint |
| PII breach (contact emails, phone numbers, deal amounts) | **P0** | Encrypt PII columns at rest; audit log on access; GDPR erasure endpoint tested before launch |
| Custom field schema drift (EAV or JSONB) corrupts reports | **P1** | Schema versioning; migration tests; validate field types on write |
| Integration token expiry breaks email/calendar sync silently | **P1** | Background job monitors token validity; alert on failed refresh; graceful degradation with user notification |
| Activity log volume kills query performance at scale | **P1** | Partition `activities` table by `created_at`; index on `(entity_type, entity_id)`; archive older than 24 months |
| Bulk import overwrites existing records unintentionally | **P1** | Dry-run mode with diff preview; deduplication key selection required before import; import is always reversible via snapshot |
| Lack of audit trail makes GDPR erasure unverifiable | **P2** | Append-only audit log separate from main tables; soft-delete with erasure cascade |
| Search relevance poor for large contact lists | **P2** | Full-text search index on name/email/company; consider Meilisearch or Postgres `tsvector` with weights |

---

## Launch requirements

- [ ] All tenant boundaries tested with cross-tenant access attempts returning 403
- [ ] GDPR/CCPA erasure flow demonstrated end-to-end on staging
- [ ] Import tested with production-scale dataset (>10 k records) without timeout or duplicate creation
- [ ] Role-permission matrix verified: admin, rep, read-only cannot exceed their access
- [ ] Email notification delivery confirmed (SPF/DKIM configured if sending own emails)
- [ ] Performance baseline recorded: list endpoint <200 ms p95 at expected record count
- [ ] Database backup and point-in-time restore verified on staging
- [ ] Rollback plan documented and tested (migration down scripts present)
- [ ] Runbook written for: user provisioning, data export, tenant offboarding
- [ ] Security checklist `.claude/checklists/security.md` fully green

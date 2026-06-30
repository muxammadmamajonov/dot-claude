# Internal Tool Preset

## Project type
A software application built for use exclusively by employees, contractors, or partners within an organisation — not exposed to the public internet or end customers. Variants: operations dashboard, data explorer / BI front-end, admin panel, approval workflow tool, support portal, internal API gateway, DevOps control plane, HR self-service portal, reporting tool, or back-office CRUD application.

## Typical use cases
- Operations and monitoring dashboards (order management, fleet tracking, incident response)
- Admin panels for managing users, content, or configuration of a customer-facing product
- Data exploration and reporting tools for analysts without SQL access
- Approval and workflow tools (expense approvals, content review queues, compliance sign-off)
- Support portals giving agents a unified view of customer data across systems
- HR / IT self-service portals (equipment requests, PTO, onboarding checklists)
- Internal developer portals (service catalog, environment provisioning, secrets rotation)

## Required discovery questions
1. Who are the users — specific teams (ops, support, finance, engineering) or all employees? Roughly how many concurrent users at peak?
2. Which existing internal systems (databases, SaaS APIs, ERP, CRM, HRIS) does this tool need to read from or write to? Are any of them classified as sensitive (PII, financial, medical)?
3. What authentication mechanism is in place — corporate SSO/SAML (Okta, Azure AD, Google Workspace), VPN-only access, IP allowlist, or a combination?
4. What data classification applies — is any data displayed or stored PII, PHI, PCI, financially sensitive, or under NDA? What are the data-handling and retention obligations?
5. Are there approval or audit requirements — does every write action need a log entry, manager approval, or four-eyes confirmation?
6. What does the happy-path workflow look like start to finish? Which manual steps does this tool replace, and what is the current workaround?
7. What is the tolerance for downtime — is this a "nice-to-have" productivity tool or does the business grind to a halt if it is unavailable?
8. Are there self-service reporting or data-export requirements (CSV/Excel download, scheduled email reports)?
9. Does the tool need role-based access — e.g. viewers vs. editors vs. admins with different data visibility?
10. What is the build-and-maintain budget? Should this be a thin Retool/Metabase wrapper, a custom-built app, or something in between?

## Recommended agents

### Core
- `.claude/agents/core/orchestrator.md` — scope management, phased delivery
- `.claude/agents/core/solution-architect.md` — system integration topology, auth model, data access layer
- `.claude/agents/core/business-analyst.md` — workflow mapping, stakeholder requirements, edge-case discovery
- `.claude/agents/core/project-manager.md` — stakeholder alignment, sprint pacing

### Engineering
- `.claude/agents/engineering/fullstack-engineer.md` — UI, data tables, forms, API layer
- `.claude/agents/engineering/backend-engineer.md` — integrations with internal systems, business logic
- `.claude/agents/engineering/database-architect.md` — query design, read replicas, caching strategy
- `.claude/agents/engineering/integration-engineer.md` — connectors to ERP, HRIS, CRM, and other internal APIs

### Quality
- `.claude/agents/quality/qa-engineer.md` — user-acceptance testing, role-based access testing
- `.claude/agents/quality/security-auditor.md` — SSO integration security, internal data exposure, audit logging
- `.claude/agents/quality/privacy-compliance-auditor.md` — PII data handling, retention, access logs

### Design
- `.claude/agents/design/ui-ux-designer.md` — dense data layouts, table/form UX, workflow clarity
- `.claude/agents/design/accessibility-designer.md` — keyboard navigation for power users, colour contrast

### Domain
- `.claude/agents/domain/erp-domain-expert.md` — when integrating ERP (SAP, NetSuite, Dynamics)
- `.claude/agents/domain/crm-domain-expert.md` — when integrating CRM (Salesforce, HubSpot)

## Recommended skills
- `.claude/skills/api-design/SKILL.md` — internal service contracts, BFF patterns, pagination for large datasets
- `.claude/skills/security/SKILL.md` — SSO/SAML integration, RBAC, session management, audit logging
- `.claude/skills/data-modeling/SKILL.md` — read-model optimisation, materialized views, caching
- `.claude/skills/backend/SKILL.md` — integration patterns, webhook consumers, data sync strategies
- `.claude/skills/testing/SKILL.md` — role-based access tests, integration tests against real-ish data
- `.claude/skills/production-readiness/SKILL.md` — structured logging, error alerting (even for internal tools)

## Recommended stack options

| Stack | Rationale |
|---|---|
| **Next.js (App Router) + PostgreSQL + NextAuth (SSO)** | Full-stack in one repo; built-in SSO adapter for Okta/Azure AD; type-safe data layer; easy to host on internal infra or Vercel. See `.claude/stack-matrix/web.md` |
| **React + Vite + Node/Fastify API + PostgreSQL** | Best when a separate API team owns the backend; clean frontend/backend contract; easy to wire to multiple data sources |
| **Retool / Appsmith (low-code)** | Fastest time to value for data tables, forms, and CRUD workflows; appropriate when no custom UI logic is needed and engineering capacity is limited |
| **Python (FastAPI) + React + SQLAlchemy** | Ideal when the team is Python-primary or the tool needs heavy data transformation (pandas, polars) before display |

Reference `.claude/stack-matrix/web.md`, `.claude/stack-matrix/backend.md`, `.claude/stack-matrix/database.md` for detailed tradeoffs.

## Required checklists
- `.claude/checklists/security.md` — SSO enforcement, RBAC, audit logging, secrets management, data exposure
- `.claude/checklists/qa.md` — role-based access matrix tested, approval flows validated, edge-case data handled
- `.claude/checklists/performance.md` — large dataset pagination, query plan review, table render performance
- `.claude/checklists/production.md` — structured logs, alerting, backup of tool-owned data, graceful error pages
- `.claude/checklists/launch.md` — SSO tested with real IdP, data classification confirmed, on-call contact defined

## MVP scope pattern

**In MVP**
- SSO authentication enforced (no passwords, no self-registration)
- Core workflow: the single most painful manual process this tool replaces
- Role-based views (at minimum: read-only vs. editor)
- Audit log for every write action (who, what, when, before/after values)
- Pagination and search on any list of > 50 records
- Error states and empty states in all data views
- Basic alerting if the tool itself errors or goes down
- Internal README and deployment instructions for the owning team

**Deferred to v2**
- Bulk actions (bulk approve, bulk export)
- Complex multi-step approval workflows
- Advanced filtering and saved views
- Scheduled report delivery (email digests)
- Self-service admin configuration (adding users, adjusting roles without a deploy)
- Integration with additional internal systems beyond the core use case
- Mobile-responsive layout (internal tools are typically desktop-only at MVP)
- Embedded charts and analytics beyond simple counts

## Production risks

| Risk | Severity | Mitigation |
|---|---|---|
| SSO misconfiguration allowing unauthenticated access | P0 | Auth middleware applied globally; smoke-test unauthenticated requests in CI; VPN or IP restriction as second layer |
| Sensitive internal data (PII, financials) exposed in API responses to wrong roles | P0 | Row-level security or explicit role checks in every query; automated RBAC test suite covering all roles × all endpoints |
| Missing audit log — no record of who changed what | P0 | Write-audit middleware that logs actor, timestamp, resource ID, old and new values before committing change |
| Direct database mutations from UI bypassing business logic | P0 | All writes go through an API layer; no direct DB access from frontend; parameterised queries only |
| Hardcoded service credentials for internal system integrations | P0 | All credentials in secrets manager (Vault, AWS SSM, 1Password Secrets Automation); rotate on schedule |
| Tool unavailability blocking critical operations (if business-critical) | P1 | Health endpoint monitored; on-call channel defined; runbook in `docs/runbook.md`; read-only fallback mode if possible |
| Overly permissive roles — everyone is admin | P1 | Minimum two roles at MVP; document intended permissions matrix in `docs/`; review during onboarding |
| Large queries locking production database | P1 | Internal tools must use read replicas for reporting queries; statement timeout configured |
| No data retention policy for tool-owned tables | P1 | Define retention period for audit logs and cached data; implement automated purge job |
| Browser caching sensitive data after session ends | P2 | Cache-Control: no-store on authenticated responses; clear sensitive state on logout |

## Launch requirements
- SSO login tested with real IdP credentials for every configured role
- RBAC matrix verified: each role can access only its intended views and actions
- Audit log confirmed: every write operation produces a timestamped entry with actor identity
- All data integrations tested with production-like data volumes (not just toy fixtures)
- Runbook written covering: how to restart, how to roll back a deploy, who to page if it breaks
- Data classification confirmed with the owning team and any applicable compliance owner
- At least one non-engineer (the primary user persona) has completed the core workflow end-to-end in staging
- Structured error logging wired and producing test alerts before go-live

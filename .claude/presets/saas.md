# Multi-Tenant SaaS Preset

## Project type

A cloud-hosted software product delivered to multiple organisations (tenants) over the internet, typically on a subscription basis. Common variants:

- **B2B SaaS** — sold to businesses; per-seat or usage-based pricing; SSO, RBAC, and audit logs are expected.
- **B2C SaaS** — sold to individuals; credit-card self-serve; strong onboarding funnel; freemium tier common.
- **PLG (Product-Led Growth)** — free tier acquires users; upsell to paid within the product; virality built into core flows.
- **Vertical SaaS** — deep domain specialisation (legal, medical, construction); compliance requirements tied to the vertical.
- **Horizontal platform / API-first SaaS** — developer product; REST/GraphQL/gRPC API is the primary interface; SDKs and webhooks matter as much as the UI.
- **White-label SaaS** — customers rebrand and resell the product; custom domains and branding per tenant.

## Typical use cases

- Productivity tools (project management, CRM, HRMS, helpdesk, document collaboration).
- Developer tooling (CI/CD, observability, feature flags, API management).
- Analytics and BI platforms.
- Communication and workflow automation.
- Industry-specific platforms (practice management, fleet management, LMS, PMS).

## Required discovery questions

1. Who is the primary buyer and primary user? Are they the same person, or does a business admin buy and employees use?
2. What is the multi-tenancy isolation model? (Shared database with tenant ID column, schema-per-tenant, database-per-tenant, or hybrid.) What are the data residency or sovereignty requirements?
3. What is the pricing and billing model? (Per-seat, usage-based, flat-rate, tiered, or hybrid.) Which payment processor? Will you need invoicing, tax handling, or enterprise contract billing?
4. What identity and SSO requirements exist? (Email/password, Google OAuth, GitHub OAuth, SAML 2.0 / OIDC for enterprise customers, SCIM provisioning.)
5. What permission model is needed at launch? (Simple owner/member/admin, or full RBAC with custom roles and resource-level permissions.)
6. What compliance frameworks apply? (SOC 2 Type II, ISO 27001, GDPR/CCPA, HIPAA, FedRAMP.) Any customer security questionnaire requirements?
7. What does a tenant's data export and account deletion flow need to look like? (GDPR right-to-erasure, data portability.)
8. What integrations are must-haves at launch vs. nice-to-have? (Slack, Zapier/Make, REST webhooks, Salesforce, etc.)
9. What SLA is promised to customers? (Uptime %, RTO/RPO, support response times.) Does this require multi-region or active-active?
10. What metrics define product success in the first 90 days? (Activation rate, MRR, churn, NPS, time-to-value.)

## Recommended agents

**Core**
- `.claude/agents/core/orchestrator.md` — flow control and gate enforcement.
- `.claude/agents/core/product-manager.md` — feature scope, success metrics, pricing model alignment.
- `.claude/agents/core/solution-architect.md` — multi-tenancy strategy, auth architecture, scaling model.
- `.claude/agents/core/requirements-engineer.md` — tenant isolation invariants, billing edge cases.

**Engineering**
- `.claude/agents/engineering/backend-engineer.md` — tenant data model, billing integration, auth, API design.
- `.claude/agents/engineering/frontend-engineer.md` — onboarding funnel, settings/billing UI, tenant switcher.
- `.claude/agents/engineering/devops-engineer.md` — CI/CD, zero-downtime deployments, per-tenant resource limits.

**Quality**
- `.claude/agents/quality/security-auditor.md` — tenant data isolation, auth bypass, secrets, OWASP Top 10.
- `.claude/agents/quality/privacy-compliance-auditor.md` — GDPR/CCPA, data-retention, erasure flows.
- `.claude/agents/quality/qa-engineer.md` — cross-tenant data leakage tests, billing edge cases.
- `.claude/agents/quality/production-readiness-auditor.md` — observability, SLA verification, runbooks.
- `.claude/agents/quality/performance-engineer.md` — per-tenant query isolation, noisy-neighbour prevention.

**Domain**
- `.claude/agents/domain/saas-domain-expert.md` — multi-tenancy patterns, subscription lifecycle, PLG mechanics.

## Recommended skills

- `.claude/skills/backend/SKILL.md` — REST/GraphQL API, auth middleware, subscription webhooks.
- `.claude/skills/security/SKILL.md` — tenant isolation, OWASP, secrets management.
- `.claude/skills/data-modeling/SKILL.md` — tenant-scoped schema design, soft deletes, audit log tables.
- `.claude/skills/devops/SKILL.md` — CI/CD pipelines, environment promotion, feature flags, secrets.
- `.claude/skills/production-readiness/SKILL.md` — uptime SLOs, alerting, on-call runbooks.
- `.claude/skills/performance/SKILL.md` — index strategy, connection pooling, caching, noisy-neighbour limits.
- `.claude/skills/testing/SKILL.md` — cross-tenant isolation test suite, contract tests for billing webhooks.
- `.claude/skills/requirements-engineering/SKILL.md` — translating compliance requirements into acceptance criteria.

## Recommended stack options

| Stack | Rationale |
|-------|-----------|
| **Next.js + tRPC + PostgreSQL (row-level security) + Stripe** | Full-stack TypeScript; Postgres RLS enforces tenant isolation at the database layer; Stripe handles subscription billing, invoicing, and tax. See `.claude/stack-matrix/backend.md`. |
| **Rails + PostgreSQL (acts_as_tenant) + Stripe + Hotwire** | Convention-over-configuration accelerates B2B SaaS; strong multi-tenancy gems; Hotwire for reactive UI without a separate JS framework. |
| **FastAPI + PostgreSQL + React + Stripe** | Python backend suits data-heavy or ML-adjacent SaaS; React for a rich UI; well-understood pairing with good library support. |
| **Node.js (NestJS) + PostgreSQL + React + Paddle** | NestJS's opinionated structure scales well; Paddle handles merchant-of-record billing (tax, VAT, chargebacks) for global B2C SaaS. |

## Required checklists

- `.claude/checklists/security.md` — extend with: tenant ID on every database query enforced at ORM/RLS layer, cross-tenant data leakage tests in CI, auth token scope verified, admin impersonation logged and audited.
- `.claude/checklists/qa.md` — extend with: billing webhook idempotency tested (duplicate events, out-of-order events), subscription state machine edge cases (cancel mid-period, upgrade mid-cycle, failed payment retry).
- `.claude/checklists/production.md` — extend with: per-tenant usage metrics visible, soft-delete and hard-delete (erasure) flows tested, data export tested.
- `.claude/checklists/performance.md` — extend with: slow-query log reviewed per tenant, connection pool sized for tenant count, noisy-neighbour CPU/query limits enforced.

## MVP scope pattern

**In the first cut:**
- Single region, single database with tenant_id row-level isolation.
- Email/password + one OAuth provider (Google). No SAML yet.
- Two subscription tiers (free/starter and paid). Stripe Checkout for card capture; Stripe webhooks for subscription lifecycle.
- Simple RBAC: owner and member roles per workspace.
- Core product feature (the one thing that delivers value). Nothing else.
- Onboarding flow: sign-up → create workspace → invite one colleague → reach "aha moment".
- Basic admin panel: tenant list, subscription status, impersonation (audit-logged).
- Email notifications for key events (invite, payment failure, password reset).

**Deferred to later:**
- SAML / SCIM (add when first enterprise customer demands it).
- Custom roles and resource-level permissions.
- Usage-based billing metering.
- Multi-region / data residency.
- White-labelling and custom domains.
- SOC 2 audit (begin evidence collection from day one; audit after product-market fit).
- Webhooks and Zapier/Make integration.
- API key management for developer access.

## Production risks

| Risk | Priority | Notes |
|------|----------|-------|
| Cross-tenant data leakage | P0 | Every query must be scoped to tenant_id; use Postgres RLS or a middleware layer; add automated leakage tests to CI. |
| Billing webhook not idempotent — double-charging or missed activation | P0 | Store Stripe event ID; skip duplicate events; test all subscription lifecycle events (created, updated, deleted, payment_failed). |
| Account takeover via weak auth or session fixation | P0 | Enforce strong passwords, rate-limit login, invalidate sessions on password change, use httpOnly+Secure cookies or short-lived JWTs. |
| No data erasure path for GDPR right-to-be-forgotten | P1 | Design soft-delete + hard-delete (with cascade) from day one; log erasure events for compliance. |
| Noisy-neighbour tenant degrading shared infrastructure | P1 | Per-tenant query timeout and connection limits; rate-limit API per tenant; monitor per-tenant resource consumption. |
| Secrets or PII leaked in logs | P1 | Structured logging; redact sensitive fields at the logger level; never log passwords, tokens, or card data. |
| Subscription state desync between Stripe and database | P1 | Reconcile subscription state on each webhook event; add a daily reconciliation job that compares Stripe subscriptions with DB state. |
| No rollback for breaking database migrations | P1 | Every migration has a down migration; test rollback in staging before applying to production; use expand-contract pattern. |
| No multi-tenancy in automated tests — bugs only found in production | P2 | Test matrix must include cross-tenant scenarios (User A cannot read Tenant B's data). |
| GDPR/CCPA consent or cookie banner missing at launch | P2 | Add consent management and privacy policy before public launch; consult `.claude/agents/quality/privacy-compliance-auditor.md`. |

## Launch requirements

- Cross-tenant data isolation verified by automated tests that pass in CI.
- Stripe webhook handler tested for all lifecycle events; idempotency confirmed.
- Password reset, email verification, and session invalidation all work end-to-end.
- Data export (download my data) and account deletion flows implemented and tested.
- Privacy policy and terms of service live; cookie/consent banner in place if applicable.
- Error monitoring (Sentry or equivalent) active; alerts fire on error-rate spike.
- Uptime monitoring with on-call alert routing; runbook for common incidents documented.
- Database backup tested with a restore drill; RTO/RPO validated against the SLA promise.
- Staging environment that mirrors production used for final pre-launch smoke test.
- Billing edge cases tested in Stripe test mode: failed payment, card expiry, upgrade, downgrade, cancellation.

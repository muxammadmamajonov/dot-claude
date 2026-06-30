# Project Brief — Fluxboard Analytics (B2B SaaS)

> **One-line idea:** A multi-tenant B2B SaaS platform that turns raw product-event data into customer-health dashboards and automated churn-risk alerts for SaaS companies with 10–500 employees.

---

## 1. Classification Result

| Dimension | Value |
|-----------|-------|
| **Project type** | Web — Multi-tenant B2B SaaS |
| **Preset applied** | `saas` |
| **Primary domain** | Analytics / Business Intelligence |
| **Cross-cutting concerns** | Payments (Stripe subscriptions), Realtime (WebSocket push for live metrics), AI (LLM-powered insight summaries), Compliance (SOC 2 Type II target, GDPR) |
| **Deployment target** | Cloud-native, single-region to start (AWS us-east-1), multi-region in 12 months |
| **Auth model** | SSO-ready (Google OAuth + SAML via WorkOS), per-workspace RBAC |

Resolved via `.claude/agents/core/orchestrator.md` → `classify-project` → matched `saas` preset in `.claude/stack-matrix/backend.md`.

---

## 2. Founder Discovery Answers

**Problem being solved**
Mid-size SaaS companies instrument events in Mixpanel or Segment but have no single place that maps those events to account health. Customer Success Managers spend 4–6 hours per week exporting CSVs and building manual spreadsheets to identify at-risk accounts before a renewal.

**Target users**
- Primary: Customer Success Managers and VPs of CS at B2B SaaS companies ($2M–$50M ARR).
- Secondary: Product managers who need adoption cohorts by account tier.
- Decision-maker / buyer: VP of Customer Success or Chief Revenue Officer.

**Value proposition**
Fluxboard ingests event streams from Segment or a direct SDK, scores each account on a composite health index updated hourly, and surfaces a prioritised at-risk list with one-click email playbooks — reducing churn-identification time from 6 hours/week to under 15 minutes.

**Constraints**
- Solo technical founder; 1 contract front-end engineer available part-time.
- $80k seed budget; need to reach revenue before runway ends (~9 months).
- Must not store raw PII in the analytics layer — hashed user IDs only.
- Enterprise prospects will require SOC 2 Type II report within 18 months.

**Success metrics (6-month targets)**
- 10 paying workspaces at ≥ $499/month (MRR $4,990+).
- P95 dashboard load < 2 s for accounts with up to 500k events/month.
- < 2% false-positive rate on churn-risk alerts (validated by CS team feedback).
- NPS ≥ 40 from pilot customers after 60 days.

**Key risks**
1. Data-pipeline reliability — dropped events erode trust instantly.
2. Long sales cycles — enterprise buyers take 60–90 days; must close SMB first.
3. Segment API rate limits could throttle ingestion at scale.
4. Competing with Gainsight (expensive) and ChurnZero; differentiation is simplicity + price.

**Budget & timeline**
- Budget: $80k total (infra + tooling + contractor).
- Target: closed beta with 3 pilot customers in 10 weeks; paid launch in 16 weeks.

---

## 3. Recommended Stack

See `.claude/stack-matrix/backend.md` and `.claude/stack-matrix/web.md` for full option tables.

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Frontend** | Next.js 14 (App Router) + TypeScript | SSR for fast first paint; RSC for server-side data fetching reduces waterfall |
| **UI library** | shadcn/ui + Tailwind CSS | Unstyled primitives, rapid theming, accessible by default |
| **Charts** | Recharts (simple) → Echarts for complex heatmaps | Recharts for MVP speed; Echarts when drilldowns are needed |
| **Backend API** | Node.js + Fastify | Low overhead, first-class TypeScript, Zod schema validation |
| **Database (OLTP)** | PostgreSQL 16 on RDS | Row-level security for multi-tenancy; pg_partman for event tables |
| **Analytics store** | ClickHouse Cloud (serverless) | Columnar aggregations over 100M+ events in < 500ms; per-query billing |
| **Job queue** | BullMQ + Redis (ElastiCache) | Reliable background ingestion workers; retries + dead-letter queue |
| **Auth** | WorkOS (Google OAuth + SAML, RBAC) | Handles enterprise SSO without building it; SOC 2 compliant vendor |
| **Payments** | Stripe Billing + Stripe Webhooks | Metered usage tiers; webhook events persisted before processing |
| **AI summaries** | Anthropic Claude claude-sonnet-4-6 via API | Streaming insight summaries; prompt caching on static context |
| **Infra** | AWS (ECS Fargate + ALB) | Predictable costs; no cold starts vs Lambda for sustained load |
| **IaC** | AWS CDK (TypeScript) | Type-safe infra, reusable constructs |
| **Observability** | OpenTelemetry → Honeycomb | Distributed traces across ingestion pipeline |
| **CI/CD** | GitHub Actions → ECR → ECS rolling deploy | Blue/green possible at GA |

**Multi-tenancy pattern:** `workspace_id` foreign key on every table + RLS policies. Each workspace gets its own ClickHouse database namespace.

---

## 4. MVP Scope

### In scope (weeks 1–10)
- Workspace creation, invite-by-email, role assignment (Admin / Analyst / Viewer).
- Segment webhook receiver + raw event buffer → ClickHouse loader (BullMQ worker).
- Direct SDK (JS snippet) as fallback ingestion path.
- Account health score engine: 4 signals (DAU/MAU ratio, feature adoption %, support ticket volume, login streak). Score refreshed hourly.
- Dashboard: account list with health score sparkline, filter by segment, sort by risk.
- Account detail page: event timeline, feature usage heatmap, health history chart.
- Churn-risk alert: email digest (daily) when score drops > 15 points in 48 hours.
- Stripe integration: Free trial (14 days) → Starter ($499/mo, 5 seats, 2M events/mo) → Growth ($1,299/mo, 20 seats, 20M events/mo).
- Basic admin: billing portal link, workspace settings, audit log (last 90 days).

### Deferred to post-MVP
- SAML SSO (WorkOS handles foundation; surface in UI at month 4).
- Bi-directional Salesforce / HubSpot sync.
- Playbook automation (auto-trigger email sequences).
- Custom health-score formula builder (drag-and-drop signal weighting).
- Multi-region data residency (EU).
- Mobile app.
- AI chat interface over account data.
- SOC 2 audit (begin prep at month 6).

---

## 5. First 3 Phases

### Phase 1 — Foundation (Weeks 1–3)
**Goal:** Running skeleton with auth, multi-tenant DB, and one ingestion endpoint. No business logic yet.

Deliverables:
- Next.js app bootstrapped; WorkOS Google OAuth login flow end-to-end.
- PostgreSQL schema: `workspaces`, `workspace_members`, `api_keys` tables with RLS enabled.
- Fastify API with Zod validation, JWT middleware, and `/health` endpoint.
- Segment webhook receiver that writes raw payloads to a `raw_events` Postgres table (ClickHouse load in Phase 2).
- BullMQ + Redis wired up; one dummy worker that logs job receipt.
- Stripe customer created on workspace sign-up; free-trial period set.
- ECS Fargate task definitions + CDK stack deploying to staging.
- GitHub Actions pipeline: lint → typecheck → unit tests → Docker build → deploy to staging on merge to `main`.
- Checklist: `.claude/checklists/security.md` items 1–8 verified (HTTPS enforced, secrets in AWS Secrets Manager, no debug endpoints in prod).

**Safe exit criteria:** A new workspace can sign up, invite one member, and the API returns 200 on a POST to `/ingest/segment` with a sample payload stored in the DB.

### Phase 2 — Core Analytics Engine (Weeks 4–7)
**Goal:** Events flow end-to-end; health scores computed; dashboard renders real data.

Deliverables:
- BullMQ worker: batches raw events → inserts into ClickHouse `events` table (partitioned by `workspace_id`, `date`).
- Account entity resolution: maps `userId` hashes to account records via a `user_account_map` table.
- Health score engine: scheduled job (every hour, BullMQ cron) computes 4 signals per account, writes to `account_health_snapshots` Postgres table.
- Dashboard UI: account list with health score badge and 7-day sparkline (Recharts).
- Account detail page: feature usage heatmap (ClickHouse aggregation), event timeline (last 30 days).
- Pagination and search on account list (Postgres full-text on account name).
- Rate-limit middleware on ingestion endpoint (100 req/s per workspace, Redis sliding window).
- Observability: OpenTelemetry spans on ingestion worker and health score job; traces visible in Honeycomb.
- Load test: k6 script simulating 500k events/day ingestion; P95 insert latency < 200ms.

**Safe exit criteria:** Pilot account with 50k historical events loaded; dashboard renders in < 2 s; health scores update within 65 minutes of new events arriving.

### Phase 3 — Alerts, Billing, and Pilot Launch (Weeks 8–10)
**Goal:** Product is sellable; first 3 pilot customers onboarded on free trial.

Deliverables:
- Churn-risk alert: daily digest email (SendGrid) listing accounts whose score dropped > 15 points; opt-in per workspace.
- Stripe webhook handler: provision/deprovision seats on subscription events; metered event-count billing reported daily.
- Usage gauge in UI: events consumed vs. plan limit this month; upgrade CTA at 80%.
- Billing portal page: embedded Stripe Customer Portal link.
- Audit log UI: last 90 days of workspace events (member joins, score threshold changes).
- Onboarding checklist in-app: 5-step guide (connect Segment → verify events → set alert threshold → invite team → review first dashboard).
- Security audit pass: `.claude/checklists/security.md` all items; pen-test on ingestion endpoint.
- QA pass: `.claude/checklists/qa.md` — manual test plan across Chrome/Firefox/Safari, WCAG 2.1 AA on dashboard.
- Production environment promoted; custom domain `app.fluxboard.io` live with TLS.

**Safe exit criteria:** 3 pilot customers have logged in, connected Segment, and received at least one churn-risk alert email. Stripe reports $0 revenue (trial) but subscription objects exist and billing will activate automatically at trial end.

---

## Next Command to Run

```
/create-specs
```

This will expand the Phase 1 deliverables into a full technical specification (API contracts, DB schema, component tree) using `.claude/templates/architecture.md` and `.claude/agents/core/requirements-engineer.md` as inputs.

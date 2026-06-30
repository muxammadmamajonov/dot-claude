# Discovery Answers
**What:** Structured founder/business discovery answers captured during the `/interview-founder` or `/discovery` flow.  
**Who fills it in:** Founder or product owner, guided by the AI. Copy this file to `docs/context/discovery-answers.md` in your project and fill every section before running `/create-specs`.

---

## 1. Problem & Opportunity

> What problem does this product solve? Who has this problem and how do they solve it today? What makes the current solution painful, expensive, or slow?

- Problem: `<e.g., freelance designers spend 3–5 hours per project writing contracts manually>`
- Current solution: `<Word templates, DocuSign from scratch, or nothing at all>`
- Pain: `<Errors, forgotten clauses, client disputes, no audit trail>`
- Opportunity: `<Automated contract generation + e-signature in < 2 minutes>`

---

## 2. Target Users

> Who are the primary users? Secondary users? What is their technical comfort level? What device or environment do they primarily use?

| Persona | Description | Technical Level | Primary Device |
|---------|-------------|-----------------|----------------|
| `<Freelance Designer>` | `<Solo contractor, 2–10 clients/month>` | `<Low-medium>` | `<Mobile + laptop>` |
| `<Studio Admin>` | `<Office manager at 5-person agency>` | `<Medium>` | `<Desktop browser>` |
| `<Client (payer)>` | `<Signs and pays invoices>` | `<Low>` | `<Mobile>` |

---

## 3. Core Use Cases (Top 5)

> List the 5–7 things users must be able to do for the product to be worth using. Rank by frequency × impact.

1. `<Create a contract from a project type template in < 2 minutes>`
2. `<Send contract to client for e-signature via link or email>`
3. `<Track contract status (draft / sent / signed / expired)>`
4. `<Get paid via integrated payment link after signature>`
5. `<Download signed PDF for records>`

---

## 4. Out of Scope (v1)

> What explicitly will NOT be built in the first version? Why?

- `<Custom clause library — too complex for v1, use fixed templates>`
- `<Multi-party contracts — single signer only in v1>`
- `<Native mobile apps — responsive web only>`

---

## 5. Success Metrics

> How will you know the product is working? Include leading indicators (engagement) and lagging indicators (business outcomes).

| Metric | Target | Timeframe |
|--------|--------|-----------|
| `<Contracts created per active user / month>` | `<≥ 4>` | `<60 days post-launch>` |
| `<Time to first sent contract>` | `<< 5 min>` | `<Onboarding session>` |
| `<Paid conversion (free → pro)>` | `<≥ 8 %>` | `<90 days>` |
| `<Contract completion rate (sent → signed)>` | `<≥ 70 %>` | `<Ongoing>` |

---

## 6. Business Model

> How does the product make money? What are the pricing tiers? Any usage-based components?

- Model: `<SaaS subscription + per-seat for teams>`
- Free tier: `<3 contracts/month, watermarked PDF>`
- Pro tier: `<$19/mo — unlimited contracts, custom branding, payment integration>`
- Team tier: `<$49/mo for up to 5 seats>`
- Revenue goal: `<$10 k MRR by month 12>`

---

## 7. Regulatory & Compliance Constraints

> Is the product subject to legal, privacy, financial, medical, or industry-specific regulations? List each and its implication.

| Regulation / Standard | Implication |
|-----------------------|-------------|
| `<GDPR / CCPA>` | `<Data residency choice; right to erasure; consent banners>` |
| `<eIDAS / ESIGN Act>` | `<E-signatures must meet legal validity requirements>` |
| `<PCI DSS (if payments)>` | `<Use Stripe/Paddle — never store raw card data>` |
| `<SOC 2 Type II (roadmap)>` | `<Audit logging, access controls from day one>` |

---

## 8. Integrations Required

> What third-party systems must the product connect to at launch? What is the integration type (API, webhook, file import)?

| System | Purpose | Integration Type | Priority |
|--------|---------|-----------------|----------|
| `<Stripe>` | `<Payments>` | `<REST API + webhooks>` | `<Must-have>` |
| `<SendGrid>` | `<Transactional email>` | `<SMTP / API>` | `<Must-have>` |
| `<Google Drive>` | `<Auto-save signed PDFs>` | `<OAuth + REST>` | `<Nice-to-have>` |
| `<Zapier>` | `<Workflow automation>` | `<Webhook>` | `<Post-launch>` |

---

## 9. Non-Functional Requirements (NFRs)

> What are the performance, availability, scale, and security expectations?

| Dimension | Requirement |
|-----------|-------------|
| Availability | `<99.9 % uptime SLA (≤ 8.7 h/year downtime)>` |
| Latency | `<P95 page load < 2 s; API response < 500 ms>` |
| Scale (launch) | `<500 concurrent users, 10 k contracts/month>` |
| Scale (12 months) | `<5 k concurrent users, 200 k contracts/month>` |
| Data retention | `<Contracts kept 7 years; soft-delete; GDPR erasure within 30 days>` |
| Security | `<Encryption at rest (AES-256) and in transit (TLS 1.3); MFA optional>` |
| Accessibility | `<WCAG 2.1 AA>` |

---

## 10. Competitive Landscape

> Who are the 2–4 closest competitors? What do you do better, worse, or differently?

| Competitor | Their Strength | Our Differentiator |
|------------|---------------|--------------------|
| `<HelloSign>` | `<Brand recognition, deep Dropbox integration>` | `<Lower price, faster setup for freelancers>` |
| `<PandaDoc>` | `<Rich proposal builder>` | `<Simpler UX, built-in payment collection>` |
| `<Bonsai>` | `<All-in-one freelancer tool>` | `<API-first, white-label ready>` |

---

## 11. Tech Preferences & Constraints

> Any preferred languages, frameworks, cloud providers, or hard constraints (existing codebase, team skill set, licensing)?

- Language / runtime: `<TypeScript (Node.js backend + React frontend)>`
- Hosting: `<AWS, EU region preferred>`
- Database: `<PostgreSQL via RDS; Redis for caching>`
- Must reuse: `<existing auth service at auth.company.internal>`
- Avoid: `<MongoDB (team lacks expertise); proprietary PaaS lock-in>`

---

## 12. Timeline & Budget

> When does v1 need to ship? What is the engineering budget/team size?

- v1 hard deadline: `<2026-10-01>`
- Team: `<2 full-stack engineers + 1 part-time designer>`
- Infrastructure budget: `<< $500/month until 1 k paying users>`
- Expected build time for v1: `<10–12 weeks>`

---

## 13. Open Questions

> What is still unknown or unresolved? List decisions that must be made before specs are finalised.

1. `<Legal validity of e-signatures in target markets (US, EU, AU) — need legal sign-off>`
2. `<Whether to build e-signature in-house or use DocuSign API>`
3. `<Pricing model confirmed by finance: need approval on $19/$49 tiers>`

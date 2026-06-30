# Project Brief
**What:** One-page summary of the project idea, type, goals, constraints, and success criteria.
**Who fills it in:** Founder, product owner, or lead engineer — before the first AI session.
**When:** Completed before running `.claude/agents/core/orchestrator.md` so the AI has full context.

---

## 1. Project Identity

> What is the name of this project? What is the single sentence that describes what it does and for whom?

- **Name:** `<ProjectName>`
- **Tagline:** `<"A <type> that helps <audience> <verb> <outcome>">`
- **Current stage:** `<idea | prototype | MVP | growth | scaling>`

---

## 2. Project Type

> Check all that apply. This tells the AI which stack matrix, checklist, and agent patterns apply.

| Type | Applies? |
|------|----------|
| Web app (browser SPA/MPA) | `<yes/no>` |
| Mobile app (iOS / Android / cross-platform) | `<yes/no>` |
| Desktop app (Electron / native) | `<yes/no>` |
| Backend API / microservice | `<yes/no>` |
| CLI tool | `<yes/no>` |
| Browser extension | `<yes/no>` |
| AI agent / LLM-powered system | `<yes/no>` |
| Data platform / analytics | `<yes/no>` |
| IoT / embedded / firmware | `<yes/no>` |
| Blockchain / smart contracts | `<yes/no>` |
| Game | `<yes/no>` |
| SaaS / multi-tenant platform | `<yes/no>` |
| Ecommerce / marketplace | `<yes/no>` |
| Fintech / payments | `<yes/no>` |
| CRM / ERP / helpdesk | `<yes/no>` |
| Other: `<describe>` | `<yes/no>` |

---

## 3. Problem & Solution

> What specific pain does this solve? Why does the current alternative fail?

- **Problem:** `<Users currently struggle with X because Y>`
- **Root cause:** `<The underlying reason existing tools fall short>`
- **Solution:** `<How this project addresses the root cause differently>`

---

## 4. Target Users

> Who are the primary and secondary users? Be concrete — describe one real person.

- **Primary:** `<Job title / role, context, technical skill level, e.g. "Non-technical small-business owner managing 5 employees">`
- **Secondary:** `<e.g. "Accountant who reviews the owner's exports once a month">`
- **Out-of-scope user:** `<Who this is explicitly NOT built for>`

---

## 5. Core Goals (prioritized)

> List 3–5 outcomes the project must achieve to be considered successful. Order by priority.

1. `<e.g. "A new user can complete their first task within 5 minutes of sign-up">`
2. `<e.g. "Process 10 000 records per minute without degradation">`
3. `<e.g. "Pass SOC 2 Type I audit by Q4">`

---

## 6. Key Constraints

> Hard limits that cannot be negotiated. Examples: budget, timeline, compliance, technology mandate, team size.

| Constraint | Value |
|------------|-------|
| Launch deadline | `<YYYY-MM-DD or "no hard date">` |
| Budget ceiling | `<$X total / $X/month opex>` |
| Regulatory requirements | `<GDPR, HIPAA, PCI-DSS, SOC 2, none>` |
| Mandated tech / vendor | `<e.g. "Must use Azure; existing Postgres cluster on RDS">` |
| Team size | `<N engineers, N designers, N QA>` |
| Offline / air-gapped requirement | `<yes/no>` |
| Accessibility standard | `<WCAG 2.1 AA / 2.2 AAA / none>` |

---

## 7. Success Metrics

> How will you know in 90 days that this project succeeded? Metrics must be measurable.

| Metric | Target | Measurement method |
|--------|--------|--------------------|
| `<Daily active users>` | `<500>` | `<Product analytics event>` |
| `<p99 API latency>` | `<< 300 ms>` | `<Datadog SLO>` |
| `<Monthly churn rate>` | `<< 5 %>` | `<Stripe MRR dashboard>` |

---

## 8. Out of Scope (v1)

> Explicitly list what will NOT be built in the first version to prevent scope creep.

- `<e.g. "Native mobile apps — web only for v1">`
- `<e.g. "Self-hosted / on-premise deployment">`
- `<e.g. "Multi-language support beyond English">`

---

## 9. Related Documents

- Discovery answers: `.claude/templates/discovery-answers.md`
- Product spec: `.claude/templates/product-spec.md`
- Architecture: `.claude/templates/architecture.md`
- Data model: `.claude/templates/data-model.md`

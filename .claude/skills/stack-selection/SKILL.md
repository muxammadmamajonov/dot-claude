---
name: stack-selection
description: Choose the technology stack from project type and constraints using the stack-matrix, and record the decisions as durable ADRs. Activate after classification and before architecture/build, or whenever a foundational technology choice (language, framework, database, hosting, queue, auth) must be made or revisited.
---

# Stack Selection

## When to use
- After classification (`.claude/skills/project-classification/SKILL.md`) and requirements (`.claude/skills/requirements-engineering/SKILL.md`) are settled, before architecture and any scaffolding.
- When a mandated or inherited stack must be validated against actual requirements — mandated does not mean unchecked.
- When a single foundational component (database, message queue, auth provider, hosting platform) needs a deliberate, recorded choice rather than a default that nobody questioned.
- When a previous stack choice must be revisited due to a new constraint (cost spike, compliance change, scale ceiling hit, team change, vendor EOL).
- For a major new capability (adding real-time, adding ML inference, adding a second region) that introduces a new technology slot.

Do not activate for minor library choices within an already-decided layer (which HTTP client to use, which icon set) — those are implementation details. Reserve this skill for decisions whose blast radius spans the whole system or a whole layer.

## Workflow

### 1. Gather and lock the inputs
Read `docs/classification.md` and `docs/requirements.md`. Extract the constraint set that will act as hard filters:

**Hard constraints** (any violation disqualifies a candidate immediately):
- Data residency / sovereignty requirements (region, country, sovereign cloud)
- Regulatory approval or certification (FedRAMP, HIPAA BAA, PCI-DSS QSA, ISO 27001, etc.)
- License compatibility (GPL contamination risk, copyleft vs. commercial, SSPL)
- Vendor mandates from the client or procurement (e.g. "must run on Azure", "must use Okta")
- Team hard-stop skills gap (zero experience AND no budget for learning AND hard deadline)
- Total cost of ownership ceiling (budget per month at target scale, not just free-tier cost)
- Runtime environment constraints (no JVM on target embedded hardware, browser-only execution, air-gapped network)

**Soft constraints** (scored, not binary):
- Team familiarity (strong, familiar, heard of, never used)
- Ecosystem maturity and community size
- Hiring pool in your geography
- Vendor lock-in tolerance
- Operational complexity headroom (does the team have ops capacity?)
- Long-term cost trajectory

Write both sets down before evaluating any candidates. Do not let enthusiasm for a technology sneak past a hard constraint.

### 2. List every decision slot to fill
Typical slots — only include what the project actually needs:

| Slot | Examples |
|------|---------|
| Primary language(s) | TypeScript, Python, Go, Rust, Swift, Kotlin, C#, Elixir |
| Frontend framework | React/Next.js, Vue/Nuxt, SvelteKit, Angular, native (iOS/Android) |
| Backend runtime/framework | Node/Express/Fastify, Django, FastAPI, Rails, Spring Boot, Go stdlib, Axum |
| Primary database | Postgres, MySQL, SQLite, MongoDB, DynamoDB, Firestore |
| Secondary / analytical DB | ClickHouse, BigQuery, Redshift, DuckDB |
| Cache | Redis, Valkey, Memcached, in-process (Caffeine) |
| Message queue / streaming | SQS, Kafka, RabbitMQ, NATS, Pub/Sub, EventBridge |
| Auth / identity | Auth0, Clerk, Cognito, Supabase Auth, self-hosted Keycloak, workOS |
| File / object storage | S3, GCS, R2, Azure Blob, Supabase Storage |
| Hosting / compute | Vercel, Railway, Fly.io, ECS, GKE, Lambda, Cloud Run, bare VPS |
| CDN | CloudFront, Cloudflare, Fastly |
| IaC | Terraform, Pulumi, CDK, Bicep, raw CLI |
| CI/CD | GitHub Actions, GitLab CI, CircleCI, Buildkite, Jenkins |
| Observability | Datadog, Grafana/Prometheus/Loki, OpenTelemetry + backend, Sentry |
| Payments | Stripe, Braintree, Adyen, PayPal, regional gateway |
| Search | Postgres FTS, Typesense, Meilisearch, Elasticsearch, Algolia |
| Real-time | WebSockets (ws/Socket.io), SSE, Pusher, Ably, Liveblocks |

Add domain-specific slots: AI inference (OpenAI, Anthropic, Bedrock, local Ollama), email (Resend, SendGrid, Postmark), maps (Mapbox, Google Maps, MapLibre), feature flags (LaunchDarkly, Unleash, Flagsmith), etc.

Remove slots that genuinely do not apply. Every slot on the list will receive a decision.

### 3. Consult the stack-matrix for each slot
For each slot, open the relevant matrix file:
- `.claude/stack-matrix/web.md` — frontend frameworks, SSR strategies, bundlers
- `.claude/stack-matrix/backend.md` — runtimes, frameworks, API styles
- `.claude/stack-matrix/database.md` — relational, document, key-value, time-series, vector
- `.claude/stack-matrix/mobile.md` — native vs. cross-platform, component libraries
- `.claude/stack-matrix/cloud-devops.md` — hosting platforms, IaC, CI/CD
- `.claude/stack-matrix/monitoring.md` — observability stacks, APM, error tracking
- `.claude/stack-matrix/realtime.md` — WebSockets, SSE, long-polling, managed channels
- `.claude/stack-matrix/payments.md` — payment processors, embedded finance, regional coverage
- `.claude/stack-matrix/ai-ml.md` — model hosting, inference APIs, vector databases, fine-tuning
- `.claude/stack-matrix/testing.md` — unit, integration, e2e, contract test frameworks

Each matrix entry lists: when to use it, when not to use it, key trade-offs, typical cost at scale, and recommended pairings. Read the relevant entries before forming an opinion.

### 4. Filter by hard constraints — eliminate, do not score
Apply every hard constraint as a binary filter. An option that violates even one hard constraint is off the table, regardless of how attractive it is on other dimensions. Document each elimination: "Rejected: MongoDB — data residency requires EU sovereign cloud, MongoDB Atlas EU regions do not have ISO 27001 BAA (per constraint C-03)." This prevents the rejected option from being re-litigated later.

**Decision point — constraint conflict:** If hard constraints conflict with each other (e.g. "must use vendor X" AND "must meet compliance Y that vendor X cannot satisfy"), stop and surface to the user. This is a business decision, not a technical one.

### 5. Score the surviving candidates
For each slot with more than one surviving option, score against weighted criteria. Suggested weights (adjust per project):

| Criterion | Weight | Notes |
|-----------|--------|-------|
| Fit for requirements (functional + NFR coverage) | 30% | Does it actually do the job? |
| Team familiarity | 25% | Most underweighted factor on deadline projects |
| Operational cost at target scale | 15% | Free tier is not the target; model actual usage |
| Scalability headroom | 10% | When does it stop working? How hard to escape? |
| Ecosystem maturity & community | 10% | Bus factor, long-term viability, hiring |
| Lock-in risk | 5% | How painful is replacement in 2–3 years? |
| Security posture | 5% | CVE history, security release cadence, audit certifications |

Do not score what you eliminated in step 4. Do not score what has a clear dominant choice — just pick it and note why. Scoring is for genuine trade-off calls.

**Default to boring, proven technology.** The highest-scoring option on excitement is not the highest-scoring option on delivery reliability. For a new project on a deadline, "the team has shipped three projects with it" beats "it benchmarks 20% faster in synthetic tests."

### 6. Apply the cohesion and minimalism test
Before finalizing, ask for each proposed component: "Does a concrete requirement force this to exist?" If the answer is no, remove it.

Also check cross-layer compatibility:
- Frontend auth model ↔ backend session/JWT model — must be consistent, or you get double-issuance bugs.
- ORM/query library ↔ chosen database — not all ORMs support all DB features you need.
- Message queue semantics ↔ consumer idempotency requirement — at-least-once vs. exactly-once matters.
- Hosting platform ↔ compliance requirement — some platforms have no certifications.
- IaC tool ↔ team experience — Terraform state corruption from a first-time user is a launch-blocking incident.

Prefer components that were designed to work together (e.g. Supabase's auth + DB + storage, Vercel's hosting + Next.js + Edge Functions) unless a requirement forces you off the happy path.

### 7. Record an ADR for each significant decision
Use `.claude/templates/decision-record.md` saved under `docs/adr/NNNN-<slug>.md`. A significant decision is one that: (a) affects multiple layers, (b) is hard to reverse, (c) has a non-obvious trade-off, or (d) was actively contested.

Mandatory ADR fields:
- **Context** — what question needed answering and why it matters
- **Options considered** — the 2–4 real candidates that survived hard-constraint filtering
- **Decision** — what was chosen and by whom
- **Rationale** — why this option over the others (reference scores or constraint IDs)
- **Consequences** — what you gain, what you give up, what becomes harder
- **Revisit trigger** — the specific condition that would reopen this decision (e.g. "if monthly DB cost exceeds $X", "if concurrent users exceed Y", "if team grows to Z and hiring needs change")

Record "why not" for the top rejected alternative in every ADR. The next engineer to join the team will want to know why you didn't use the obvious alternative. If you don't write it down, they'll switch to it and undo your decision.

### 8. Summarize the chosen stack
Write `docs/stack.md` as a single glanceable table:

| Slot | Choice | Key alternatives rejected | Primary rationale | Cost/ops note | Revisit trigger |
|------|--------|--------------------------|-------------------|---------------|-----------------|

This is the single source of truth the whole team reads. It must be updated every time an ADR changes a decision. Link each row to the corresponding ADR.

### 9. Escalate business-critical trade-offs
Surface to the user only the decisions that involve:
- A meaningful cost difference (e.g. managed vs. self-hosted with a $X/month delta)
- Vendor lock-in that would be expensive to reverse (e.g. proprietary database, closed-source AI provider)
- A compliance implication they need to sign off on (e.g. "we need a BAA from vendor X before storing PHI there")
- A capability gap where no option fully covers the requirement (e.g. "no payment processor covers all required countries without a second processor")

Document all other choices yourself and record them in the stack summary.

### 10. Hand off
Pass `docs/stack.md` and `docs/adr/` to `.claude/skills/architecture/SKILL.md`. The architecture skill reads the stack to make component and integration decisions — it must not contradict the stack without writing a new ADR.

## Standards

- **Do** record *why not* for the top rejected alternative in each ADR. Future maintainers will re-evaluate; give them the reasoning so they don't repeat the analysis.
- **Do** weight team familiarity heavily for tight deadlines. The most capable technology the team cannot operate safely is the wrong technology for this project right now.
- **Do** model cost at realistic target scale, not at free-tier usage. A system that is cheap at 1 user and ruinous at 10,000 is a hidden time bomb.
- **Do** prefer managed services when ops capacity is thin and budget permits. Prefer self-hosted when cost, data control, or residency demands it — but factor in the full ops burden honestly.
- **Do** check license compatibility and total cost of ownership before selecting any component. SSPL and AGPL have commercial use implications.
- **Do** verify compliance certifications (SOC2, ISO 27001, PCI-DSS, HIPAA BAA) against actual vendor documentation, not marketing copy.
- **Do not** select a technology because it is new, fast-rising on GitHub star charts, or used by FAANG at scale. Each of those is a non-reason for your project.
- **Do not** add a database, queue, cache, or runtime "in case we need it later." Add it when a requirement forces it. Premature components are premature complexity.
- **Do not** leave a foundational choice undocumented. Undocumented choices get silently reversed, re-litigated in PRs, or carried forward as tribal knowledge that leaves with the original engineer.
- **Do not** let frontend and backend choices drift into incompatible auth/session models. Validate the full auth flow end-to-end at decision time, not at implementation time.

## Common mistakes to avoid

- **Picking trendy tech the team has never used before a hard deadline.** The risk premium on an unfamiliar stack is real and large. A team building their first SvelteKit + Prisma + Fly.io + Tigris project will spend a third of their time on framework surprises instead of product value.
- **Over-architecting v1 with microservices, Kafka, and Kubernetes** when a modular monolith on Railway or Fly.io would ship in half the time and cost a tenth as much. Distribution is a solution to a specific scale and team-topology problem; apply it when you have that problem.
- **Ignoring data residency until after hosting is chosen.** Discovering that your chosen cloud region has no compliance certification after scaffolding is already done forces a restart. Check residency in step 1.
- **Choosing a database by popularity rather than by data shape and access patterns.** Postgres is an excellent default, but it is the wrong answer for time-series sensor data (TimescaleDB/InfluxDB), for a document model with deeply nested variable schemas (MongoDB/Firestore), or for a key-value cache (Redis/Valkey). See `.claude/skills/data-modeling/SKILL.md`.
- **Letting frontend and backend auth models diverge.** A React SPA using JWTs from Clerk and a Django backend expecting sessions from a different provider will produce hours of CORS, cookie, and 401 debugging. Validate the auth flow holistically.
- **Treating containerization as free.** "We'll Dockerize it later" ignores that Kubernetes networking, secrets injection, rolling deploys, and resource limits are non-trivial operational problems. If the team is not running containers today, containerization is a project, not a checkbox.
- **Selecting by the free tier.** DynamoDB at 25 GB free becomes expensive fast at scale; Supabase free tier has connection limits; Mongo Atlas free tier has no ops flexibility. Model the cost at the target 12-month scale before deciding.
- **Ignoring the revisit trigger.** Without a written condition that would reopen a decision, teams either never revisit (accumulating technical debt) or constantly relitigate (wasting time). The trigger turns "this is locked forever" into "this is locked until condition X."

## Output format

Per-decision ADRs in `docs/adr/` (one file per significant decision, using `.claude/templates/decision-record.md`) plus a consolidated `docs/stack.md` table:

```
| Slot | Choice | Key alternatives rejected | Primary rationale | Cost/ops note | Revisit trigger |
```

Every row in `docs/stack.md` links to its ADR. Every ADR records context, options, decision, rationale, consequences, and revisit trigger. Every significant choice traces back to a constraint or requirement ID.

## Related checklists
- `.claude/checklists/production.md`
- `.claude/checklists/security.md`
- `.claude/checklists/performance.md`
- `.claude/checklists/devops.md`

## Related agents
- `.claude/agents/core/orchestrator.md`
- `.claude/agents/core/solution-architect.md`
- `.claude/agents/core/technical-lead.md`
- `.claude/agents/quality/security-auditor.md`
- `.claude/agents/quality/production-readiness-auditor.md`

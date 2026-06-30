---
description: Produce a capacity/scaling plan with SLOs, bottleneck analysis, and cost model; output docs/architecture/scaling-plan.md.
argument-hint: [horizon: 3m | 6m | 12m | 24m — optional, default 12m]
---

# /plan-scale

## Purpose
Produce a concrete, evidence-based scaling and capacity plan. Identify the current load profile, project growth, locate architectural bottlenecks, define SLOs, choose a scaling strategy (vertical, horizontal, sharding, caching, async offload, geographic), and estimate the cost envelope. Output a living document the team can reference when provisioning infrastructure and negotiating SLA commitments.

## When to use
- Before launch on any project expecting non-trivial or unpredictable load (APIs, real-time systems, data pipelines, game servers, marketplaces).
- After `/design-architecture` but before finalizing infrastructure choices — scaling constraints should shape the architecture, not be bolted on after.
- When the team sets SLA/SLO commitments with customers or partners.
- When performance audit (`/audit-performance`) uncovers bottlenecks that require structural remediation rather than code-level optimization.
- At recurring intervals (e.g., quarterly on a live system) or after a traffic event (viral spike, large customer onboarding).

## Workflow

### Step 0 — Load context and horizon
1. Read `.claude/agents/quality/performance-engineer.md` and `.claude/agents/quality/reliability-engineer.md` — both roles are active for this command. The performance-engineer owns bottleneck analysis and load modeling; the reliability-engineer owns SLO definition and failure-mode analysis.
2. Read `.claude/skills/performance/SKILL.md` — load profiling patterns, scaling strategies, and benchmarking guidance.
3. Read `.claude/templates/slo-sla.md` and `.claude/templates/cost-model.md` — these are the sub-documents that feed the final plan.
4. Determine the planning horizon from the argument (`3m | 6m | 12m | 24m`). Default: `12m`.
5. Read existing specs: `docs/architecture.md`, `docs/specs/`, `docs/state/project-type.md`, `docs/architecture/scaling-plan.md` (if a prior plan exists — use it as the baseline).
6. Read any observability data present: dashboards, metric exports, APM traces, load test results, profiling reports under `docs/` or referenced in specs.

### Step 1 — Establish the current load profile
If the system is already live, derive actuals. If pre-launch, derive estimates from product spec and comparables.

**For live systems:**
- Read application logs, APM traces, and metric exports if available in the repo (`docs/`, `infra/`, `monitoring/`).
- Identify: peak RPS/QPS per endpoint or service, p50/p95/p99 latency, error rates, peak concurrent connections, data ingestion rate, queue depths, storage growth rate per month.
- Identify traffic patterns: daily/weekly seasonality, known spike events, batch job peaks.

**For pre-launch systems:**
- Read the product spec for DAU/MAU targets, transaction volumes, data retention requirements.
- Model requests-per-user-per-day × DAU → RPS. Add a 3× headroom multiplier for spikes.
- State the model's assumptions explicitly — they go into the assumptions log.

Record in the plan:
```
Current (or projected at launch): <N> RPS peak, <N> RPS average
p95 latency target: <Nms>  |  Error rate target: <N%>
Data ingestion: <N GB/day>  |  Storage growth: <N GB/month>
Concurrency: <N> simultaneous connections/sessions
```

### Step 2 — Project growth over the horizon
1. Define three growth scenarios:
   - **Conservative:** <current × 2 at end of horizon>
   - **Expected:** based on roadmap milestones and sales/marketing plan from `docs/specs/`.
   - **Aggressive:** viral/enterprise event, 10× spike over 48 hours.
2. For each scenario, project: peak RPS, storage volume, egress bandwidth, compute-hours, database connections, queue throughput at 3-month intervals through the horizon.
3. Identify the point at which each scenario exceeds current headroom — this is the **capacity cliff**.

### Step 3 — Identify bottlenecks
Systematically analyze each layer of the stack against the projected load. Read architecture docs and source code as needed.

| Layer | What to check | Common bottleneck signals |
|---|---|---|
| **Compute** | CPU saturation, memory pressure, thread pool exhaustion | p99 latency spike under load; OOM kills |
| **Database** | Connection pool limits, query plans, index coverage, write throughput, replication lag | Slow query log; connection wait time > 5ms |
| **Cache** | Hit rate, eviction rate, hot-key contention, cold-start behavior | Hit rate < 80%; single-key RPS > 10k |
| **Network / CDN** | Bandwidth caps, egress cost, latency to user regions, DNS TTL | Egress bills; p99 TTFB > 200ms from distant regions |
| **Queue / async** | Consumer lag, DLQ growth, poison-pill processing, backpressure | Queue depth growing unbounded under load |
| **Storage** | IOPS limits, throughput caps, object storage API rate limits | Throttling errors; list-operation latency |
| **Third-party APIs** | Rate limits, SLA of uptime dependency, no circuit breaker | Cascading failure when downstream degrades |
| **Application** | Synchronous blocking calls in hot path, N+1 queries, missing pagination, large serialization payloads | CPU-bound at low RPS; heap pressure |
| **Build / deploy** | Deploy time, migration run time, downtime window | Cannot roll out fast enough during an incident |

For each identified bottleneck:
- **BN-ID** (BN-001, BN-002 …)
- **Layer and component**
- **Trigger threshold** — at what load level does this become a problem?
- **Failure mode** — what breaks and how (timeout, OOM, queue overflow, cascading failure)?
- **Mitigation strategy** — concrete fix (add read replica, introduce cache, move to async, increase pool size, shard, add circuit breaker, etc.)
- **Estimated effort** (S / M / L / XL) and whether it is reversible.

### Step 4 — Design scaling strategy
For each bottleneck and growth scenario, select the scaling approach. Document the reasoning.

**Scaling primitives to evaluate (use what fits; reject what doesn't):**

| Primitive | When to choose | When to avoid |
|---|---|---|
| Vertical scale-up | Stateful workloads; fast fix; predictable load | Cost ceiling; single point of failure |
| Horizontal scale-out | Stateless services; variable load | Session affinity required; shared mutable state |
| Read replicas | Read-heavy DB; analytics queries hurting write path | Write-heavy; strong consistency required |
| Caching (in-process, Redis, CDN) | Repeated reads; slow computed results; static assets | Write-heavy; cache invalidation complexity > benefit |
| Async / queue offload | Non-latency-critical writes; fan-out; batch processing | User expects synchronous response; ordering critical |
| Sharding / partitioning | Data volume exceeds single-node; hot partition avoidance | Cross-shard queries; joins; transactions |
| Geographic distribution | Latency to specific regions; data residency compliance | Cost; operational complexity; consistency tradeoffs |
| Rate limiting & back-pressure | Protect against traffic spikes; third-party rate limits | Cannot reject requests (safety-critical path) |
| Connection pooling / PgBouncer | DB connection limit exhaustion | Already pooled; overhead not justified |
| Circuit breaker | Third-party dependency with variable availability | Internal services with low latency SLA |

For each chosen strategy, record:
- The bottleneck it resolves (BN-ID).
- Implementation steps in priority order.
- Infrastructure changes required (new services, new cloud resources, config changes).
- Dependencies and sequencing constraints (e.g., "must add read replica before removing cache to avoid DB overload").

### Step 5 — Define SLOs
Using `.claude/templates/slo-sla.md`, define SLOs for each critical user-facing path.

For each SLO:
- **Service / endpoint:** what is being measured.
- **SLI (indicator):** the metric being tracked (availability %, latency percentile, error rate, throughput).
- **SLO (objective):** the target (e.g., 99.9% availability, p95 < 200ms, error rate < 0.1%).
- **Measurement window:** rolling 30 days (standard) or calendar month.
- **Error budget:** how much downtime/error is acceptable per window (e.g., 99.9% = 43.8 min/month).
- **Alert threshold:** when to page (e.g., error budget burn rate > 5× in 1 hour).
- **Exclusions:** planned maintenance, upstream dependencies, force-majeure.

Minimum SLOs to define (add more for critical paths):
1. API availability (primary traffic path).
2. p95 and p99 response latency (primary traffic path).
3. Error rate (5xx) on authenticated endpoints.
4. Data pipeline freshness lag (if applicable).
5. Background job completion time (if user-visible results depend on it).

**STOP — Present the proposed SLOs to the user.** State each SLO and ask: "Do these SLO targets reflect your commitments to users and any contractual SLAs you have? Reply with adjustments before I finalize the plan."

Wait for user acknowledgment before Step 6.

### Step 6 — Model costs
Using `.claude/templates/cost-model.md`, produce a cost estimate for each growth scenario at the end of the planning horizon.

**Cost categories to cover:**
- Compute (instances / containers / serverless invocations).
- Database (instance + storage + backup + data transfer).
- Cache (instance + memory tier).
- Storage (object storage + egress + API calls).
- CDN (bandwidth + requests).
- Queue / messaging (message volume + retention).
- Observability (log ingestion, metric storage, trace retention).
- Third-party APIs (per-call pricing × projected volume).
- Support / infrastructure tooling.
- **Total monthly and annual cost per scenario.**

Identify **cost cliffs**: points where a pricing tier changes, a resource type must be upgraded, or egress volume jumps a pricing band. Flag these clearly.

For each scenario, also compute:
- Cost per 1000 active users (or equivalent unit).
- Break-even point vs. revenue projection if product spec includes pricing.
- Top 3 cost drivers and whether each is fixed, variable, or step-function.

If cloud pricing data is unavailable, state the assumption (e.g., "estimated using AWS us-east-1 on-demand pricing as of <date>") and note that actual costs should be validated with a cloud cost calculator.

### Step 7 — Write the scaling plan document
Write `docs/architecture/scaling-plan.md` incorporating all steps above, structured as:
1. Executive summary (risk of not scaling + biggest bottleneck + recommended first action).
2. Load profile (current and projected, all three scenarios, with capacity cliffs).
3. Bottleneck register (all BN-NNN entries, layered by stack).
4. Scaling strategy (per bottleneck, with implementation roadmap).
5. SLOs (from Step 5, with error budgets and alert thresholds).
6. Cost model (from Step 6, all three scenarios).
7. Implementation roadmap (ordered by risk and impact, with effort estimates).
8. Assumptions log (all load projections, pricing assumptions, growth rate assumptions).
9. Review cadence (when to revisit: quarterly, or after 2× traffic, or after major feature launch).

### Step 8 — Append assumptions to project log
For every modeled assumption (growth rate, RPS estimate, cost assumption), append to `docs/state/assumptions.md` using `.claude/templates/assumptions-log.md`. Reference the BN-ID or scenario name so each assumption is traceable.

## Agents used
- `.claude/agents/quality/performance-engineer.md` — owns load profile, bottleneck analysis, benchmarking, and scaling strategy selection.
- `.claude/agents/quality/reliability-engineer.md` — owns SLO definition, error budget calculation, failure-mode analysis, and alerting thresholds.

## Skills used
- `.claude/skills/performance/SKILL.md` — profiling patterns, load-testing strategies, caching patterns, async offload patterns, database scaling patterns.

## Expected outputs
| Output | Path |
|---|---|
| Scaling plan (main document) | `docs/architecture/scaling-plan.md` |
| SLO register (embedded in plan, also standalone) | `docs/architecture/slos.md` |
| Cost model (embedded in plan, also standalone) | `docs/architecture/cost-model.md` |
| Assumptions appended | `docs/state/assumptions.md` |

## Stop conditions
- No architecture documentation and no source code to read → cannot identify bottlenecks; **STOP** and request: "Share the system architecture (even a rough description) so I can model the scaling constraints."
- SLO targets in Step 5 conflict with the architecture's realistic capability (e.g., 99.99% SLO on a single-AZ deployment with no redundancy) → **STOP**, flag the gap as a Critical finding, and present the user with the minimum infrastructure changes needed to make the SLO achievable.
- Cost projections for the aggressive scenario exceed what a reasonable project of this type would spend per user, with no clear monetization path → flag as a business risk in the executive summary and surface to the user; do not block the plan.
- Third-party dependency has no published SLA and sits on a critical path → flag as a reliability risk, recommend a fallback/circuit breaker, and note it as an SLO exclusion candidate.

## Final report format
```
## Scaling Plan Report — <date>

**Project:** <name>  |  **Horizon:** <3m|6m|12m|24m>
**Planner roles:** performance-engineer + reliability-engineer

### Executive summary
<3–5 sentences: biggest risk, most critical bottleneck, top recommended action, cost range>

### Load profile
| Scenario | Current | 3m | 6m | 12m | Capacity cliff |
|---|---|---|---|---|---|
| Conservative | N RPS | N | N | N | <month M> |
| Expected | N RPS | N | N | N | <month M> |
| Aggressive | N RPS | N | N | N | <month M> |

### Bottleneck register
| ID | Layer | Trigger load | Failure mode | Mitigation | Effort |
|---|---|---|---|---|---|
| BN-001 | Database | 500 RPS | Connection pool exhaustion | PgBouncer + read replica | M |

### SLOs
| Path | SLI | SLO | Error budget (30d) | Burn-rate alert |
|---|---|---|---|---|
| POST /api/orders | Availability | 99.9% | 43.8 min | >5× in 1h |

### Cost model
| Scenario | Monthly (now) | Monthly (end of horizon) | Annual | $/1k users |
|---|---|---|---|---|
| Conservative | $N | $N | $N | $N |
| Expected | $N | $N | $N | $N |
| Aggressive | $N | $N | $N | $N |

**Top cost drivers:** <driver 1>, <driver 2>, <driver 3>
**Cost cliff:** at <N> RPS / <N> users, tier upgrade adds ~$N/month

### Implementation roadmap
| Priority | Action | Resolves | Effort | Reversible? |
|---|---|---|---|---|
| P0 (before launch) | Add PgBouncer connection pool | BN-001 | S | Yes |
| P1 (month 1–2) | Add Redis cache for session data | BN-003 | M | Yes |
| P2 (month 3–6) | Introduce read replica for analytics | BN-002 | L | Yes |

### Assumptions
<N> assumptions logged to docs/state/assumptions.md.
Key assumptions: <growth rate source>, <pricing basis>, <RPS model formula>

### Next review
Revisit this plan at: <ISO date> — or sooner if traffic exceeds the expected scenario
trajectory or a major architecture change is made.
```

# Architecture Checklist
Passing this gate proves architectural decisions are sound, trade-offs are documented with rationale, and the design is safe to build against — no undocumented "magic," no single points of silent failure, no components that trust each other without explicit justification. Items are severity-tagged P0/P1/P2/P3.

## P0 — Blockers (must pass before implementation begins)

- [ ] A single authoritative architecture document exists at `docs/architecture.md` (from `../templates/architecture.md`), is version-controlled, and has been reviewed and approved by the technical lead.
- [ ] Every major architectural decision (technology choice, communication pattern, data ownership, deployment topology) has an ADR in `docs/decisions/` (from `../templates/decision-record.md`) that records: the decision, alternatives considered, the rationale for choosing this one, and the reversal path if wrong.
- [ ] System boundaries are drawn precisely: what this system owns, what is delegated to external services, and what is explicitly out of scope for the current phase — with no ambiguous overlaps.
- [ ] Communication patterns between every pair of components are explicitly specified: synchronous HTTP/REST/gRPC, asynchronous message queue (broker, topic, at-least-once vs. exactly-once), event stream, webhook push, or scheduled polling. Each choice is justified by the latency and reliability requirements from the requirements checklist.
- [ ] A single authoritative source of truth is identified for every entity that can be mutated; split-brain, cache-coherence, and eventual-consistency lag scenarios are analyzed and mitigated.
- [ ] Authentication and authorization boundaries are explicit in every component diagram: no component implicitly trusts any other; trust is always established through a named mechanism (JWT validation, API key, mutual TLS, service account, OAuth 2.0 scope).
- [ ] The data flow for every sensitive data category (PII, PHI, PCI card data, credentials, financial transactions) is traced end-to-end: ingress → processing → storage → egress. Each segment is labelled with its encryption standard (TLS 1.2+ in transit; AES-256 or equivalent at rest) and access control.
- [ ] No "magic" component exists whose failure would silently corrupt data, cause money loss, or leave the system permanently inconsistent without triggering an operator alert.
- [ ] Every stateful component has a documented persistence strategy: what gets stored, where, with what consistency guarantee (strong / eventual), backup frequency, and maximum tolerable data loss (RPO).
- [ ] The architecture satisfies all non-functional requirements from `../checklists/requirements.md`: latency budgets are allocated per tier, throughput is achievable without re-architecture, and uptime SLA is achievable with the chosen redundancy model.

## P1 — Important (fix before first production deployment)

- [ ] Scalability strategy is documented for each bottleneck: horizontal pod/node auto-scaling (HPA/KEDA/ASG), database sharding or read-replica strategy, CDN for static and edge-cached content, cache layer (Redis/Memcached) placement, and the traffic threshold that triggers each scaling action.
- [ ] Every external dependency has a documented: connection timeout, read timeout, max-retry count with exponential back-off and jitter, circuit-breaker threshold (error rate and window), and graceful-degradation fallback (serve stale cache, return partial response, disable non-critical feature, queue for later processing).
- [ ] Observability is designed in, not bolted on: every service emits structured logs (JSON with trace ID, request ID, user/tenant ID), metrics (latency p50/p95/p99, error rate, queue depth, saturation), and distributed traces (OpenTelemetry or equivalent). Alerting thresholds are defined for each SLO.
- [ ] Deployment topology is matched to the availability target: single-region (acceptable for ≤ 99.9% SLA with fast restore), multi-region active-passive (99.95%), or multi-region active-active (99.99%+). The choice is justified with cost trade-off analysis.
- [ ] Data residency and sovereignty constraints from the requirements are satisfied by the chosen cloud regions, storage services, and CDN configurations (no cross-border transfer of regulated data without documented legal basis).
- [ ] The migration path from the current state (or from zero) to the target architecture is documented step-by-step with: the order of operations, the rollback procedure for each step, the estimated downtime window (or the zero-downtime strategy), and who approves each step.
- [ ] Local development and CI environments mirror production closely enough to catch integration failures before they reach production: same message broker, same database engine and version, same service discovery, same secrets management model.
- [ ] The architecture diagram is maintained as code (`docs/architecture.md` using Mermaid, PlantUML, or Structurizr DSL), not only as a rendered image, so it stays in sync with the codebase via review.

## P2 — Hardening / nice-to-have

- [ ] Cost model is estimated at expected load with cost-per-unit projections (cost per 1000 API calls, cost per active user per month), budget alert thresholds, and a documented cost-reduction lever for each major line item.
- [ ] Chaos engineering scenarios are enumerated and accepted as risks or planned for: primary database node failure, message broker partitioning, external API outage, network latency spike, clock skew, memory exhaustion, and disk-full on a stateful node.
- [ ] Technology choices are validated against team skill set, vendor support windows, open-source community health, and license compatibility with the project's license.
- [ ] Evolutionary architecture seams are identified so the system can absorb likely future changes without full rewrites: anti-corruption layers at domain boundaries, plugin/extension interfaces, tenant isolation boundaries, and feature-flag-gated behaviors.
- [ ] Shared platform services (auth service, notification service, file storage, billing) are clearly separated from application-specific business logic to prevent accidental coupling and allow independent scaling.
- [ ] Database schema versioning and migration strategy is documented: tool (Flyway, Alembic, golang-migrate, Prisma Migrate), naming convention for migrations, backward-compatibility rules for zero-downtime deploys, and the policy on editing vs. deleting existing migrations (editing existing migrations is forbidden by default per `.claude/CLAUDE.md` §8).

## P3 — Post-launch / backlog (track and revisit after launch; never blocks shipping)

- [ ] All ADRs in `docs/decisions/` are reviewed 3–6 months post-launch against real production behaviour; decisions that proved wrong or suboptimal are superseded with a new ADR documenting what changed and why.
- [ ] Chaos engineering scenarios enumerated at P2 are formally executed (game days or automated fault injection) and results are used to update circuit-breaker thresholds, alerting rules, and runbooks.
- [ ] Cost model projections from P2 are compared against actual cloud spend; any line item exceeding the projection by more than 20 % triggers a documented cost-reduction action or a revised budget approval.
- [ ] Evolutionary architecture seams are stress-tested against the next-phase requirements now known from real usage; seams that proved too narrow or placed at the wrong boundary are redesigned before the next major feature build.
- [ ] Technology choices are re-evaluated against updated team skill set, vendor support windows (EOL dates), and open-source community health signals (release cadence, CVE response time) once the system has been in production for 6 months.

## How to use
Run at the end of the design phase, before the first feature implementation sprint begins. Triggered by `../agents/core/orchestrator.md` after `../checklists/requirements.md` passes. The `../agents/core/solution-architect.md` owns this gate, with input from `../agents/engineering/database-architect.md`, `../agents/engineering/cloud-architect.md`, and `../agents/quality/security-auditor.md`. Reference `../templates/architecture.md`, `../templates/decision-record.md`, and `../stack-matrix/` entries matching the project type. Invoke via `../commands/design-architecture.md`. Reviewer marks each item `[x]` when satisfied or `[-]` when explicitly waived with a written rationale and risk classification in a decision record.

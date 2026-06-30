---
description: Production-readiness review: reliability, observability, scaling, backups, runbooks, on-call.
argument-hint: [scope: full | reliability | observability | scaling | backups | runbooks — optional]
---

# /audit-production

## Purpose
Verify the system is ready to carry real production traffic. Covers the five pillars of production readiness: reliability (error handling, retries, circuit breakers), observability (metrics, logs, traces, alerts), scaling (capacity, autoscaling, rate limits), data safety (backups, DR, migration strategy), and operational readiness (runbooks, on-call rotation, deployment process). Produces a gated go/no-go recommendation.

## When to use
- Final gate before running `/prepare-launch`.
- After a major architectural change (new service, new database, migration to cloud).
- Quarterly production health review.
- Before onboarding a new on-call engineer.
- After a post-incident review recommends hardening.

## Workflow

### Step 0 — Scope and context
1. Read `docs/specs/`, `.claude/stack-matrix/`, and any existing runbooks in `docs/runbooks/`.
2. Identify: deployment targets (cloud provider, region, container/VM/serverless), SLO commitments, data classification (PII, financial, health), and expected peak traffic.
3. If scope argument is given, restrict to that pillar; otherwise evaluate all five.

### Step 1 — Reliability review
Check each item; mark PASS / FAIL / N/A:

**Error handling**
- All external calls (HTTP, DB, queue, cache) have timeout values set.
- Transient errors are retried with exponential backoff and jitter.
- Non-retryable errors are distinguished from transient ones.
- Circuit breakers prevent cascade failures to downstream services.
- Graceful degradation: feature flags or fallback paths exist for non-critical dependencies.

**Process resilience**
- Health-check endpoint (`/healthz` or equivalent) returns dependency status, not just HTTP 200.
- Liveness and readiness probes are configured (Kubernetes / ECS / similar).
- Application handles `SIGTERM` gracefully — drains in-flight requests before exit.
- Crash loops produce an alert (not silent restart loops).

**Data integrity**
- Database writes are idempotent or protected by unique constraints where needed.
- Background jobs are idempotent (safe to re-run on failure).
- Dead-letter queues are configured for message queues.
- Long-running transactions have timeouts.

### Step 2 — Observability review

**Metrics**
- RED metrics exported for every service: Request rate, Error rate, Duration (p50/p95/p99).
- USE metrics for every resource: Utilisation, Saturation, Errors (CPU, memory, disk, connections).
- Business KPI metrics (orders/min, signups/hour, revenue events) are instrumented.
- Metrics are stored in a time-series system with at least 13-month retention.

**Logging**
- Structured JSON logs (not free-text) with consistent fields: timestamp, level, trace_id, service, environment.
- No PII, credentials, or payment data in logs.
- Log levels are calibrated — DEBUG not enabled in production by default.
- Logs are shipped to a centralised system with at least 30-day retention.
- Correlation IDs propagate across service boundaries.

**Tracing**
- Distributed traces span all service hops for request flows.
- Database queries appear in traces with sanitised SQL.
- Trace sampling rate is set (100% at low traffic, adaptive at scale).

**Alerting**
- On-call alerts fire for: error rate spike, p95 latency breach, service downtime, queue depth spike, disk/memory saturation.
- Alerts route to on-call rotation (PagerDuty, OpsGenie, or equivalent) — not just email.
- Alert fatigue audit: all current alerts have a defined response action (no "watch only" alerts).
- Runbook link is embedded in each alert.

### Step 3 — Scaling review

**Capacity**
- Peak traffic estimate is documented. Current capacity provides ≥2× headroom.
- Autoscaling (horizontal or vertical) is configured with tested scale-up/scale-down triggers.
- Database connection pool is sized for peak instance count × connections per instance.
- Rate limiting is in place on public-facing endpoints.
- CDN/edge caching is in front of static assets and cacheable API responses.

**Statelessness**
- Application instances are stateless — session state is in a shared store (Redis, DB), not in-process memory.
- Sticky sessions are not required for correctness (or are explicitly documented as a constraint).

**Dependency limits**
- Third-party API rate limits are documented. Back-off and queuing exist for high-volume callers.
- Database max connections vs. instance count is validated.

### Step 4 — Data safety review

**Backups**
- Automated backups run on schedule; backup frequency ≤ RPO target.
- Backup restoration has been tested end-to-end within the last 90 days.
- Backups are stored in a separate account/region from production data.
- Point-in-time recovery (PITR) is enabled for databases holding critical data.

**Disaster recovery**
- RTO and RPO targets are documented in `docs/specs/` or `docs/runbooks/`.
- Failover procedure is written and has been dry-run.
- Multi-region or multi-AZ is in place if RTO < 1 hour.

**Migration safety**
- Database migrations are backwards-compatible (expand-contract pattern) so rollback does not require schema reversal.
- Migration runs are logged and can be verified post-deploy.

### Step 5 — Operational readiness review

**Runbooks** — check `docs/runbooks/` for:
- Service restart / rollback procedure.
- Incident severity classification.
- On-call escalation path.
- Common failure scenarios with diagnosis steps.
- Dependency outage playbook (what to do when Stripe/AWS/Twilio is down).

**Deployment process**
- CI/CD pipeline runs tests, security scans, and smoke tests before promoting to production.
- Deployment is zero-downtime (rolling, blue/green, or canary).
- Feature flags allow toggling new features without redeployment.
- Rollback takes < 10 minutes and is a single documented command/click.

**On-call**
- At least two engineers are in the on-call rotation.
- On-call handbook is up to date.
- Post-incident review (PIR) process is defined.

### Step 6 — Score and gate
Assign each pillar a score: GREEN (all critical items pass), AMBER (non-critical gaps), RED (critical gap blocks launch).

**STOP — present pillar scores to the user. If any pillar is RED, do not proceed to `/prepare-launch` until resolved. Get user sign-off on the go/no-go decision.**

### Step 7 — Fix resolvable gaps
For AMBER gaps that are code or config changes (not infra provisioning):
1. Draft the fix.
2. Get user approval.
3. Apply and commit: `ops(<pillar>): <fix description>`.

### Step 8 — Report
Produce the Final report (see below).

## Agents used
- `.claude/agents/core/documentation-writer.md` — generates missing runbooks from code and architecture.
- `.claude/agents/quality/reliability-engineer.md` — reviews alert definitions for coverage and fatigue.

## Skills used
- `.claude/checklists/production.md` — full itemised checklist.
- `.claude/templates/runbook.md` — standard runbook template.
- `.claude/stack-matrix/cloud-devops.md` — infrastructure patterns for the detected stack.

## Expected outputs
| Output | Path |
|---|---|
| Production-readiness report | `docs/reports/prod-readiness-<date>.md` |
| Generated/updated runbooks | `docs/runbooks/<service>.md` |
| Applied config/code fixes | in-place, committed |

## Stop conditions
- Any pillar scores RED → block `/prepare-launch`; present gaps; wait for user resolution.
- Backup restoration has never been tested → RED for data safety regardless of other items.
- No on-call rotation exists for a user-facing service → RED for operational readiness.
- Observability gap means a production outage could go undetected > 5 minutes → RED.

## Final report format
```
## Production Readiness Report — <date>

**Project:** <name>  |  **Scope:** <scope>
**Deployment target:** <cloud/region>  |  **SLO:** <uptime target>

### Pillar scorecard
| Pillar | Score | Critical gaps |
|---|---|---|
| Reliability | 🟢 GREEN | none |
| Observability | 🟡 AMBER | No business KPI metrics |
| Scaling | 🟢 GREEN | none |
| Data Safety | 🔴 RED | Backup restore untested |
| Ops Readiness | 🟡 AMBER | Only 1 on-call engineer |

### Go / No-Go: ❌ NOT READY (1 RED pillar)

### RED — must resolve before launch
#### [R1] Backup restore untested — Data Safety
- **Risk:** Backup files exist but restoring them has never been validated. Data loss on failure with no recovery path.
- **Action:** Run a full restore drill to a staging environment; document the procedure in `docs/runbooks/backup-restore.md`.
- **Owner:** <assigned>  |  **Due:** before launch

### AMBER — resolve within first sprint post-launch
- [A1] No business KPI metrics — instrument `order.created`, `signup.completed` events.
- [A2] Single on-call engineer — add a second rotation member before go-live.

### Fixes applied this session
| Item | Fix | Commit |
|---|---|---|
| Missing `/healthz` dependency status | Added DB + cache ping to health endpoint | abc1234 |
| No DLQ on orders queue | Configured DLQ with 3-retry policy | def5678 |

### Next steps
1. Resolve [R1] backup restore drill.
2. Resolve [A2] on-call rotation.
3. Re-run `/audit-production` after items resolved.
4. Run `/prepare-launch` once all pillars are GREEN or AMBER.
```

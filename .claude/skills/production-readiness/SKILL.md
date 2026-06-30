---
name: production-readiness
description: Use as the final gate before launch — verify reliability, observability, scaling, and disaster recovery are real, not assumed. Triggers when a release candidate is built and audits (security, QA, performance, accessibility) have passed, and you must confirm the system can run, be watched, scale, and recover in production. Blocks launch on unmet critical criteria.
---

# Production Readiness Review

## When to use
- A release candidate has passed the security, QA, performance, and accessibility audits and is being considered for launch.
- Promoting a service from staging to production for the first time, or after a major architectural change.
- Periodically re-certifying a live system after significant growth or incidents.

Applies to any system that runs after release: hosted apps/APIs, background services, scheduled jobs, agents, mobile/desktop apps with backends, and embedded fleets. The four pillars below are universal even when the mechanisms differ.

## Workflow
1. **Confirm the audits are green.** Production readiness comes *after* security (`.claude/skills/security/SKILL.md`), QA (`.claude/skills/testing/SKILL.md`), performance (`.claude/skills/performance/SKILL.md`), and accessibility. If any are open, stop and route back. This skill verifies operability, not feature correctness.
2. **Reliability.** Verify graceful degradation: timeouts, retries with backoff, circuit breakers, idempotency on writes, and sane handling of dependency failure. Confirm health/readiness checks exist and are wired to the platform.
3. **Observability.** Confirm structured logs (no secrets/PII), metrics for the golden signals (latency, traffic, errors, saturation), distributed tracing on critical paths, and actionable alerts that page on user-impacting conditions — not noise. Verify dashboards exist for the top flows.
4. **Scaling & limits.** Confirm the system meets performance budgets at expected peak load (verified, not assumed), has autoscaling or a capacity plan, enforces rate limits/quotas, and applies back-pressure instead of collapsing. Identify the next bottleneck.
5. **Disaster recovery.** Verify backups exist, are automated, and — critically — have been test-restored. Define and check RPO/RTO. Confirm rollback works, runbooks exist for top failure modes, and there is an on-call/escalation path.
6. **Data & compliance.** Confirm data retention/deletion, encryption at rest/in transit, and any regulatory requirements (privacy, residency, audit logs) are satisfied for the project's domain.
7. **Operational dry run.** Walk a deploy + rollback in staging. Trigger a synthetic failure and confirm alerts fire and runbooks work. Confirm secrets rotation and on-call are real, not theoretical.
8. **Go/no-go.** Score the readiness checklist. Any unmet *critical* criterion is a no-go. Document accepted risks with owners and a remediation date; get explicit human sign-off before launch.

## Standards
- **Do** verify backups by actually restoring one; an untested backup is not a backup.
- **Do** require real, test-fired alerts on user-impacting conditions with an owner and a runbook for each.
- **Do** prove the system meets performance budgets at peak load before launch, with measurements.
- **Do** make every write idempotent or safely retryable, and every external call timeout-bounded.
- **Do** keep a tested rollback and a documented incident/escalation path.
- **Do** strip secrets and PII from logs and traces; confirm during the review.
- **Do** define RPO/RTO and confirm the recovery mechanism meets them.
- **Do-not** launch on assumptions ("it should scale", "backups probably run") — verify each.
- **Do-not** ship noisy or non-actionable alerts; alert fatigue means real pages get ignored.
- **Do-not** override a failed *critical* readiness criterion without explicit, recorded human approval.
- **Do-not** perform destructive recovery drills (restore-over-prod, failover) without approval and a safety net.

## Common mistakes to avoid
- "It works in staging" with no load test, then collapsing at real traffic.
- Backups that run but were never restored, discovered useless during an actual outage.
- Logging that captures secrets/PII, or alerts so noisy the team mutes them.
- No rollback rehearsal; the first real rollback happens during the first real incident.
- Missing idempotency, so a retried payment or webhook double-charges or duplicates data.
- No on-call/escalation defined; an alert fires at 3am to nobody.
- Treating readiness as paperwork instead of dry-running deploy, failure, alert, and recovery.

## Output format
A go/no-go report scored against the four pillars (reliability, observability, scaling, DR) plus data/compliance, each item pass/fail with evidence (load-test numbers, restore proof, fired-alert screenshot/log). Include an accepted-risk register with owners and dates, and a recorded human sign-off line. Use `.claude/checklists/production.md` as the source list and link the report to the release.

## Related checklists
- `.claude/checklists/production.md`
- `.claude/checklists/security.md`
- `.claude/checklists/performance.md`

## Related agents
- `.claude/agents/quality/production-readiness-auditor.md`
- `.claude/agents/engineering/devops-engineer.md`
- `.claude/agents/core/orchestrator.md`

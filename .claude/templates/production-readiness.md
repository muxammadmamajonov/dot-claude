# Production Readiness Review
**What:** A structured checklist and evidence record confirming a system is safe to run in production.  
**Who fills it in:** Engineering lead + reviewers from security, QA, and platform — completed before every initial launch and major release.  
**Cross-references:** `.claude/checklists/security.md`, `.claude/templates/deployment-plan.md`, `.claude/templates/launch-checklist.md`

---

## 1. Review Metadata

> Fill in before the review begins.

| Field | Value |
|-------|-------|
| Service / component | `<auth-service v2.0>` |
| Review date | `<YYYY-MM-DD>` |
| Review lead | `<@engineer-name>` |
| Reviewers | `<@security, @sre, @qa-lead>` |
| Release linked | `<v2.0.0 — link to deployment-plan.md instance>` |
| Overall verdict | `<PASS | CONDITIONAL PASS | FAIL>` |

---

## 2. Functional Correctness

> Is the software doing what it's supposed to do?

| Check | Status | Evidence / Notes |
|-------|--------|-----------------|
| All acceptance criteria met | ☐ | Link to feature spec sign-off |
| No open P0/P1 bugs in scope | ☐ | `<Jira filter link>` |
| Regression tests pass | ☐ | `<CI run link>` |
| Manual QA sign-off | ☐ | `<@qa-lead confirmed YYYY-MM-DD>` |
| Edge cases documented and handled | ☐ | `<link to feature-spec.md>` |

**Open issues (if CONDITIONAL PASS):** `<list any known issues with accepted risk>`

---

## 3. Security

> Has the system been reviewed against the threat model?

| Check | Status | Evidence / Notes |
|-------|--------|-----------------|
| Authentication / authorization verified | ☐ | `<Auth flow tested, OWASP checklist run>` |
| Input validation and output encoding in place | ☐ | |
| Secrets not hardcoded or logged | ☐ | `<grep/semgrep scan clean>` |
| Dependency vulnerabilities scanned | ☐ | `<npm audit / pip-audit / snyk report link>` |
| HTTPS enforced, TLS version ≥ 1.2 | ☐ | |
| CORS, CSP, security headers configured | ☐ | `<link to headers audit>` |
| PII / sensitive data handled per policy | ☐ | |
| Penetration test or security review completed | ☐ | `<optional — link to report>` |

See `.claude/checklists/security.md` for the full security checklist.

---

## 4. Reliability & Resilience

> Will the system stay up and recover gracefully?

| Check | Status | Evidence / Notes |
|-------|--------|-----------------|
| SLA / uptime target defined | ☐ | `<99.9 % monthly>` |
| Health check endpoints return correct status | ☐ | `<GET /health → 200>` |
| Graceful shutdown implemented | ☐ | `<SIGTERM handler drains in-flight requests>` |
| Retry logic with backoff on external calls | ☐ | |
| Circuit breakers / timeouts on dependencies | ☐ | `<timeout: 5 s, circuit opens at 50 % errors>` |
| Chaos / failure injection tested (if applicable) | ☐ | |
| Single points of failure identified and mitigated | ☐ | |

---

## 5. Performance & Scalability

> Will the system handle expected load and scale when needed?

| Check | Status | Evidence / Notes |
|-------|--------|-----------------|
| Load test run at `<2×>` expected peak | ☐ | `<k6 / Locust report link>` |
| P95 latency ≤ target under load | ☐ | `<target: 300 ms>` |
| No memory leaks under sustained load | ☐ | |
| Database queries indexed and explain-plan reviewed | ☐ | |
| Caching strategy in place for hot paths | ☐ | |
| Auto-scaling configured and tested | ☐ | `<HPA min 2, max 10 pods>` |
| Resource limits (CPU, memory, connections) set | ☐ | |

---

## 6. Observability

> Can the team detect, diagnose, and respond to issues in production?

| Check | Status | Evidence / Notes |
|-------|--------|-----------------|
| Structured logs with correlation IDs | ☐ | `<JSON logs shipped to Datadog>` |
| Metrics collected (RED: rate, errors, duration) | ☐ | `<Prometheus / CloudWatch>` |
| Distributed tracing instrumented | ☐ | `<OpenTelemetry spans>` |
| Dashboards created and reviewed | ☐ | `<link to dashboard>` |
| Alerts defined with thresholds and routes | ☐ | `<error rate > 1 % → PagerDuty>` |
| On-call runbook written and linked | ☐ | `<link to runbook>` |
| Log retention policy set | ☐ | `<30 days hot, 1 year cold>` |

---

## 7. Data Integrity & Persistence

> Is data stored, migrated, and backed up safely?

| Check | Status | Evidence / Notes |
|-------|--------|-----------------|
| Database migrations are backward-compatible | ☐ | |
| Backup strategy defined and tested | ☐ | `<daily snapshots, 30-day retention, restore tested>` |
| Data encryption at rest | ☐ | `<AES-256 / KMS>` |
| Data encryption in transit | ☐ | `<TLS 1.3>` |
| GDPR / CCPA / data-residency requirements met | ☐ | |
| Soft-delete or audit log for sensitive records | ☐ | |

---

## 8. Deployment & Rollback

> Can the team deploy safely and undo if needed?

| Check | Status | Evidence / Notes |
|-------|--------|-----------------|
| Deployment plan documented | ☐ | `<link to deployment-plan.md>` |
| Zero-downtime deploy verified | ☐ | `<rolling deploy / blue-green>` |
| Rollback procedure tested in staging | ☐ | |
| RTO target achievable with rollback plan | ☐ | `<target: 15 min>` |
| Feature flags used to decouple deploy from release | ☐ | |
| Previous stable artifact available | ☐ | `<v1.9.2 in registry>` |

---

## 9. Operational Readiness

> Is the team ready to operate this in production?

| Check | Status | Evidence / Notes |
|-------|--------|-----------------|
| On-call rotation includes this service | ☐ | `<PagerDuty schedule link>` |
| Runbook covers top 5 failure scenarios | ☐ | `<link>` |
| Support / CS team briefed on changes | ☐ | |
| SLAs / SLOs documented and agreed | ☐ | `<99.9 % uptime, < 300 ms P95>` |
| Incident response process known to team | ☐ | |
| Cost model reviewed (cloud spend within budget) | ☐ | `<$X/month estimate>` |

---

## 10. Compliance & Legal

> Are there any regulatory, licensing, or contractual obligations?

| Check | Status | Evidence / Notes |
|-------|--------|-----------------|
| Open-source license audit clean | ☐ | `<FOSSA / license-checker>` |
| Data processing agreements in place | ☐ | |
| Audit logging meets compliance requirement | ☐ | `<SOC 2 / ISO 27001 / HIPAA / PCI>` |
| Accessibility requirements met (if user-facing) | ☐ | `<WCAG 2.1 AA>` |
| Export control / geo-restriction rules followed | ☐ | |

---

## 11. Risk Register & Mitigations

> List known risks being accepted with this release and the mitigation for each.

| Risk | Likelihood | Impact | Mitigation | Owner |
|------|-----------|--------|-----------|-------|
| `<Migration takes longer than estimated>` | Medium | High | `<Maintenance window, rollback tested>` | `<@devops>` |
| `<Third-party API unavailable>` | Low | Medium | `<Circuit breaker + cached fallback>` | `<@backend-lead>` |

---

## 12. Sign-Off

> All reviewers must explicitly approve before production deployment proceeds.

| Reviewer | Role | Decision | Date |
|----------|------|----------|------|
| `<@engineer>` | Engineering lead | `<APPROVE / REQUEST CHANGES>` | `<YYYY-MM-DD>` |
| `<@security>` | Security | `<APPROVE / REQUEST CHANGES>` | `<YYYY-MM-DD>` |
| `<@sre>` | Platform / SRE | `<APPROVE / REQUEST CHANGES>` | `<YYYY-MM-DD>` |
| `<@qa-lead>` | QA | `<APPROVE / REQUEST CHANGES>` | `<YYYY-MM-DD>` |

**Conditions attached (if CONDITIONAL PASS):**
- `<Condition 1: fix X before enabling feature flag Y>`
- `<Condition 2: complete penetration test within 30 days post-launch>`

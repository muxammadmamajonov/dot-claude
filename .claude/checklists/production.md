# Production Checklist

Production-readiness gate covering reliability, observability, scaling, backups, runbooks, and graceful degradation — passing this proves the system can sustain failures, alert on problems, and recover within defined RTO/RPO without manual heroics. Severity tiers: P0=blocker, P1=important (fix shortly after launch), P2=hardening, P3=post-launch / backlog (track and revisit; never blocks shipping).

## P0 — Blockers (must pass before proceeding / launch)

- [ ] Structured logging is configured on every service: each log line emits at minimum `timestamp` (RFC 3339), `level` (DEBUG/INFO/WARN/ERROR), `service`, `trace_id`, `request_id`, and a human-readable `message`; logs are shipped in real time to a central, queryable store (Datadog, CloudWatch Logs, Grafana Loki, OpenSearch, or equivalent) with a retention policy of ≥ 30 days for operational logs and ≥ 1 year for audit logs.
- [ ] Health-check endpoints exist and are correctly wired: a liveness probe (`/livez`) returns HTTP 200 only when the process can serve requests; a readiness probe (`/readyz`) returns HTTP 200 only when all dependencies (database, cache, required external services) are reachable; both are registered as load-balancer health checks or orchestrator probes.
- [ ] Alerting rules are defined, tested, and routed for at minimum: (a) service or pod down for > 1 min, (b) error rate > 1% over a 5-minute window, (c) p95 latency > SLA threshold for 5 min, (d) disk utilization > 80%, (e) memory utilization > 85%, (f) any critical CVE disclosure affecting a running dependency. Alerts route to the on-call channel with a direct link to the relevant runbook.
- [ ] On-call rotation is documented with named primary and secondary contacts, an escalation path that reaches someone with production access within 30 minutes 24/7, and runbook links published in the monitoring dashboard.
- [ ] Automated database backups are verified end-to-end: backup runs on schedule (at minimum daily, hourly for OLTP systems), backup files are encrypted at rest, and a restoration test against a non-production environment has been executed within the past 30 days with the restore time and row-count validation recorded.
- [ ] Disaster-recovery runbook is complete and has been executed in staging: it defines RTO, RPO, step-by-step restore procedure, the owner for each step, and the communication template to notify stakeholders during an outage. RTO and RPO targets are approved by the product owner.
- [ ] All outbound dependencies (payment processors, auth providers, email/SMS gateways, object storage, downstream APIs) have timeout, retry (with exponential back-off and jitter), and circuit-breaker logic; a dependency failure causes a graceful degraded response (e.g., cached data, queue, or error page) — not a cascade or a blank screen.
- [ ] Secrets rotation procedure is documented, tested, and automated where possible; expiry alerts fire at least 14 days before any credential, certificate, or API key expires; rotation does not require downtime.
- [ ] SLOs are defined and documented: at minimum availability (e.g., 99.9% over 30 days) and latency (e.g., p95 < 300 ms); an error-budget burn-rate alert fires when the burn rate exceeds 2× the target, and the error-budget policy states what triggers a feature freeze.

## P1 — Important (fix before scaling / shortly after launch)

- [ ] Distributed tracing (OpenTelemetry SDK + a backend: Jaeger, Tempo, AWS X-Ray, Honeycomb, or Datadog APM) propagates `trace_id` and `span_id` across all service and async-job boundaries; slow traces (p95 > SLA) are queryable by trace ID within 30 seconds of completion.
- [ ] The four golden signals are dashboarded per service: **Latency** (p50/p95/p99), **Traffic** (RPS/throughput), **Errors** (rate and 5xx count), **Saturation** (CPU %, memory %, queue depth); the dashboard URL is embedded in the runbook at `.claude/templates/runbook.md`.
- [ ] Auto-scaling policies are configured and tested under synthetic load: horizontal pod autoscaler, EC2 ASG, Cloud Run min/max instances, or equivalent scales out before the saturation threshold is breached; scale-in uses a connection-draining or request-draining period so in-flight requests complete before pods terminate.
- [ ] Resource limits are set on every container, function, or process: CPU and memory requests and limits are defined, tuned to observed 90th-percentile usage with a 30% headroom, so one runaway workload cannot starve the host or sibling services.
- [ ] Graceful shutdown is implemented: on SIGTERM the service stops accepting new connections, drains in-flight requests with a configurable timeout (default 30 s), flushes buffers and closes DB connections cleanly, and then exits with code 0; no in-flight request is silently dropped on a rolling deploy.
- [ ] Rate limiting and request throttling are applied at the API gateway or application layer; abuse or a misconfigured client cannot exhaust DB connection pools, downstream API quotas, or memory.
- [ ] Dependency version pinning and automated security patching are active; critical and high CVEs are patched and deployed within 72 hours of public disclosure; the patch SLA is documented and owned by a named team.
- [ ] Cost anomaly detection is configured: unexpected spend > 20% above the 7-day rolling average triggers an alert to the engineering and finance owners; reserved/committed spend and resource rightsizing are reviewed monthly.

## P2 — Hardening / nice-to-have

- [ ] Chaos engineering baseline: at least one steady-state hypothesis is documented and tested (e.g., kill a pod, inject 200 ms latency on a downstream dependency, fail a database replica); the experiment results, blast radius, and any remediation are recorded in `docs/`.
- [ ] Multi-region or multi-AZ failover is tested: DNS failover or traffic-manager cutover is rehearsed, DNS TTL is set ≤ 60 s for critical hostnames, and the measured failover time is within RTO.
- [ ] Immutable infrastructure: deploys replace instances/containers rather than mutating them in place; configuration drift is structurally impossible because configuration is baked at build time or injected at runtime from a secrets manager.
- [ ] Audit log — who performed what action on which resource and when — is stored in an append-only, tamper-evident store (CloudTrail, GCP Audit Logs, an immutable S3 bucket with Object Lock, or equivalent) and retained per compliance requirements (minimum 90 days; 1 year for regulated systems).
- [ ] Log-based anomaly detection or ML-based alerting (Datadog Watchdog, Cloud Monitoring anomaly detection, or equivalent) is enabled to catch novel error patterns not covered by static threshold alerts.
- [ ] Backup encryption is verified: backup files are encrypted at rest with a customer-managed or platform-managed key; key rotation is tested annually; the ability to decrypt and restore from an encrypted backup is validated in the DR test.
- [ ] Synthetic monitoring (Checkly, Pingdom, CloudWatch Synthetics, or equivalent) runs the critical user journey or API health scenario every 5 minutes from multiple geographic regions; pages on-call immediately on failure.

## P3 — Post-launch / backlog (track and revisit after launch; never blocks shipping)

- [ ] SLO error-budget consumption is reported to stakeholders monthly: burn rate, remaining budget, top contributors to budget spend, and whether a feature freeze was triggered are summarized in a written report linked from the ops runbook.
- [ ] Runbooks are reviewed and rehearsed quarterly: each runbook owner executes a dry run in a non-production environment, confirms command accuracy, and timestamps the review — stale runbooks (> 90 days unreviewed) are flagged in the on-call rotation.
- [ ] Distributed tracing sampling rate is tuned based on production traffic volume: head-based sampling is replaced or augmented with tail-based sampling (Tempo, Honeycomb, or equivalent) so 100% of slow and error traces are retained without excessive storage cost.
- [ ] Cost anomaly detection thresholds are tightened after 60 days of baseline data: the initial 20% threshold is narrowed to 10%, and per-service cost attribution tags are validated so anomalies route to the correct team's alert channel.
- [ ] Chaos engineering scope is expanded beyond a single steady-state hypothesis: a game-day exercise covering at least three simultaneous failure scenarios (network partition, dependency degradation, and traffic spike) is scheduled semi-annually with pre-defined success/failure criteria.
- [ ] Backup restoration drills are automated and scheduled monthly in a CI-adjacent pipeline: row-count validation, referential-integrity checks, and restore duration are recorded as metrics and alerted when they regress versus the previous run.

## How to use

Run `.claude/commands/audit-production.md` and invoke `.claude/agents/quality/production-readiness-auditor.md` against the project before any production launch. Revisit monthly and after any major infrastructure change, dependency upgrade, or architecture decision. The primary agents are `.claude/agents/quality/reliability-engineer.md` and `.claude/agents/engineering/devops-engineer.md`. Cross-reference `.claude/checklists/devops.md` for CI/CD gates, `.claude/checklists/security.md` for hardening, and `.claude/checklists/launch.md` for the final go-live sign-off. Mark each item `[x]` when verified or `[-]` when formally waived with a written justification and a named approver.

# Observability Checklist

Gate for production observability: structured logs, metrics, distributed traces, SLOs, actionable alerts, dashboards, on-call readiness, and cardinality/cost control.

## P0 — Blockers (must pass before launch)

- [ ] Structured logging enabled on every service: JSON format, consistent fields (`timestamp`, `level`, `service`, `trace_id`, `span_id`, `user_id` redacted, `error`); no plain-text log lines in production.
- [ ] All logs shipped to a central sink (CloudWatch Logs, Datadog, Loki, GCP Cloud Logging, etc.) with retention policy set; log loss tested under load — confirmed < 0.1 % drop rate.
- [ ] Golden signals instrumented for every service: Latency (p50/p95/p99), Traffic (RPS), Errors (5xx rate), Saturation (CPU/memory/queue depth) — all queryable in the observability platform.
- [ ] Distributed tracing deployed across the full request path (HTTP, gRPC, async queues): OpenTelemetry SDK instrumented; trace IDs propagated through all hops; sampled at ≥ 1 % (100 % for errors).
- [ ] SLOs defined for every user-facing API and background job: target (e.g. 99.9 % availability, p99 latency < 500 ms), measurement window (28-day rolling), and error budget percentage documented.
- [ ] Burn-rate alerts configured per SLO: fast-burn alert (2 % error budget in 1 h) AND slow-burn alert (5 % in 6 h); alerts route to on-call channel with runbook link in the alert body.
- [ ] On-call rotation documented and active: primary + secondary responder per service, escalation path, PagerDuty/OpsGenie schedule set, and at least one end-to-end on-call drill completed.
- [ ] Service health dashboard published and accessible to all engineers without VPN: shows SLO status, error rate, latency heatmap, and saturation for each service on a single screen.
- [ ] Synthetic / uptime monitors running from ≥ 2 external regions; alert fires within 60 s of an outage; monitor covers the critical user journey (login → core action → success response).

## P1 — Important (address soon after launch)

- [ ] Error tracking platform integrated (Sentry, Bugsnag, Rollbar, or equivalent): every unhandled exception captured with stack trace, user context (anonymised), and environment tag; new error types alert within 5 min.
- [ ] Database slow-query log enabled; queries exceeding 100 ms logged with full query plan; top-10 slow queries reviewed weekly.
- [ ] Queue depth and consumer lag monitored for every async queue/topic (Kafka consumer group lag, SQS `ApproximateNumberOfMessagesNotVisible`, RabbitMQ queue depth); alert when lag > 5-minute processing time.
- [ ] Deployment markers annotated in all dashboards: every deploy, config change, and feature flag toggle appears as a vertical line so regressions are instantly correlated.
- [ ] Alert fatigue audit completed: each alert has a documented runbook, an owner, and has fired and been actioned in the last 30 days OR has been silenced/deleted; no alert fires more than 5 times per week without action.
- [ ] Cost of observability data quantified: estimated monthly spend on logs, metrics, and traces; high-volume noisy logs identified and filtered or sampled; cardinality of custom metrics audited.
- [ ] Feature flag observability: every flag change logged with actor and timestamp; dashboards segment key metrics by flag variant to enable safe rollouts.

## P2 — Hardening

- [ ] Cardinality guard enforced: no custom metric dimension with unbounded cardinality (user IDs, request IDs, full URL paths); metric series count reviewed monthly; hard limit set in the observability platform.
- [ ] Log sampling strategy documented for high-throughput services: DEBUG logs sampled at ≤ 1 % in production; ERROR logs always captured; sampling decision propagated to traces.
- [ ] Capacity planning dashboards built: 30/60/90-day trend projections for storage, compute, and network from observed growth rates; reviewed before each major traffic event.
- [ ] Chaos / fault injection experiments run quarterly to validate that alerts fire correctly when dependencies fail (circuit breakers, timeout, partial outage simulations using Chaos Monkey / Gremlin / LitmusChaos).
- [ ] OpenTelemetry Collector deployed as a sidecar or daemon set to decouple instrumentation from vendor lock-in; tail-based sampling configured for high-traffic services.

## P3 — Post-launch / backlog

- [ ] Continuous profiling enabled (Pyroscope, Datadog Continuous Profiler, or equivalent) on CPU/memory-intensive services to guide optimisation without requiring ad-hoc profiling sessions.
- [ ] Business-level metrics (DAU, conversion rate, revenue per hour) surfaced on the same observability platform as technical metrics to correlate incidents with business impact.
- [ ] Observability-as-code: dashboards, alert rules, and SLO definitions committed to version control (Terraform / Jsonnet / Grafonnet) and applied via CI/CD; manual dashboard edits prohibited in production.
- [ ] AIOps / anomaly detection baseline established: ML-based anomaly detection enabled for top-5 business metrics to catch subtle degradation that threshold alerts miss.

## How to use

Run this checklist via the `audit-production` or `reliability-engineer` commands before any production launch and after significant architecture changes. P0 items block launch sign-off. Link each completed item to the relevant dashboard URL, alert rule, or runbook in `docs/state/observability.md`. Re-run P1 items as a monthly health check.

---
name: observability
description: Use when adding or auditing logging, metrics, distributed tracing, alerting, SLOs, or dashboards. Triggers when a service lacks visibility into its own health, when an incident reveals a blind spot, when setting up a new service or environment, or when reviewing production readiness. Applies to all backend services, APIs, workers, agents, mobile apps, and data pipelines — any running system that can fail silently.
---

# Observability: Logs, Metrics, Traces, Alerts & SLOs

**Scope: system health, metrics, logs, traces, SLOs. Product/business events → `.claude/skills/analytics/SKILL.md`.** This skill is the single owner of metric-cardinality guidance (see Phase 4).

## When to use
- Standing up observability for a new service, environment, or project type (backend API, worker, agent, mobile app, data pipeline).
- Adding structured logging, a metrics layer, or distributed tracing to an existing service.
- Defining SLOs and configuring alerts that fire on user impact, not noise.
- Responding to an incident where the root cause was invisible (blind-spot remediation).
- Running the production-readiness gate: verifying that the system is observable before launch.
- Reviewing dashboards or alert configs for cardinality explosions, missing signals, or alert fatigue.

Applies to every project type: web backends, mobile backends, event-driven workers, AI/agent systems, data pipelines, IoT gateways, CLI tools with usage telemetry.

---

## Workflow

### Phase 1 — Instrument

**1. Adopt OpenTelemetry (OTel) as the instrumentation standard.**
OTel is vendor-neutral; it separates instrumentation from the backend. Use the OTel SDK for your language (Go, Python, Java, Node.js, .NET, Ruby, PHP, Rust). Export to your chosen backend (Grafana/Tempo, Honeycomb, Datadog, Jaeger, Google Cloud Trace, AWS X-Ray) via the OTel Collector. This avoids vendor lock-in in instrumentation code.

Install auto-instrumentation for the framework first (FastAPI, Express, Django, Spring Boot, etc.) — it captures HTTP spans, DB queries, and outgoing HTTP calls with zero custom code. Then add manual spans only for business-critical operations: payment processing, external API calls, queue publish/consume, ML inference.

**2. Structured logging: JSON everywhere, never plaintext.**
Every log entry must be a JSON object. Required fields on every log line:
```json
{
  "timestamp": "ISO-8601 UTC",
  "level": "info|warn|error|debug",
  "service": "auth-service",
  "version": "1.4.2",
  "trace_id": "...",
  "span_id": "...",
  "request_id": "...",
  "user_id": "...",   // redacted/hashed for PII
  "message": "...",
  "...context fields": "..."
}
```
Inject `trace_id` and `span_id` from the active OTel span so logs are correlatable with traces. Use a structured logger: `zerolog` (Go), `structlog` (Python), `pino` (Node.js), `logback` with JSON encoder (Java). Never use `console.log(string)` or `print(string)` in production code.

Log levels: **ERROR** = action required; **WARN** = degraded but handling; **INFO** = significant business event; **DEBUG** = detailed diagnostic (disabled in production unless sampled).

**3. Metrics: RED for services, USE for resources.**
Define metrics in two categories:

*RED (per service/endpoint):*
- **Rate** — requests per second (counter: `http_requests_total{method, route, status}`)
- **Errors** — error rate (derived: `rate(http_requests_total{status=~"5.."}[1m])`)
- **Duration** — latency distribution (histogram: `http_request_duration_seconds{method, route}`, expose p50/p95/p99 percentiles)

*USE (per resource — CPU, memory, DB pool, queue):*
- **Utilization** — % of capacity in use
- **Saturation** — work queue depth / wait time
- **Errors** — resource-level error count

For Prometheus: use the official client library (`prometheus_client` Python, `prom-client` Node.js, `prometheus/client_golang`). Expose a `/metrics` scrape endpoint. For OTEL metrics, use the SDK meter.

Examples shown in JS/Node; the same patterns apply across platforms — equivalents (mobile, Go, Python, etc.) follow the Standards table.

**4. Distributed traces: connect the dots across services.**
Every inbound HTTP/gRPC request receives a trace context (`traceparent` W3C header or `X-B3-TraceId`). Propagate it through: outbound HTTP calls, message queue publish (store in message metadata), async workers (extract from message metadata on consume). This creates an end-to-end trace from the user's browser to the database query.

Add custom span attributes for business context: `order.id`, `user.tier`, `payment.provider`, `model.name`, `experiment.variant`. These make traces searchable and filterable.

Sample: use **head-based sampling** at 10–20% for high-volume routine traffic; use **tail-based sampling** or **100% sampling** for errors and slow requests (> p99 threshold). The OTel Collector supports tail-sampling via the `tailsampling` processor.

**5. Instrument AI/agent systems specifically.**
For LLM-based services: trace each inference call as a span with attributes `llm.model`, `llm.prompt_tokens`, `llm.completion_tokens`, `llm.latency_ms`, `llm.finish_reason`. Track tool calls as child spans. Log full prompt/completion at DEBUG level (redact PII) — these are critical for debugging agent misbehavior. Track token cost as a metric (`llm_cost_usd_total{model, operation}`).

---

### Phase 2 — Define SLOs

**6. Define SLIs and SLOs before writing alerts.**
An SLO without an SLI is a wish. For each user-facing service, define:

- **SLI** (what you measure): e.g., "proportion of API requests completing in < 500ms with HTTP 2xx"
- **SLO** (target): e.g., "99.5% of requests over a 30-day rolling window"
- **Error budget**: 100% − 99.5% = 0.5% → ~3.6 hours of allowable bad minutes/month

For most services, define SLOs for: availability (success rate), latency (p95 or p99), and optionally throughput or data freshness (for pipelines).

Record SLOs in `docs/specs/slo-sla.md` using `.claude/templates/slo-sla.md`. Keep them few (3–5 per service) and meaningful (represent actual user experience, not internal implementation details).

**7. Wire SLO tracking to burn-rate alerts (not threshold alerts).**
Threshold alerts (`error_rate > 1%`) fire too late and generate noise. Burn-rate alerts fire when you are consuming your error budget faster than sustainable.

Multi-window burn-rate alert pattern (Google SRE Book):
```
Alert 1 (page immediately): burn_rate > 14.4× over 1h AND 6h    → consuming 30-day budget in 2 days
Alert 2 (ticket, faster): burn_rate > 6× over 6h AND 3h         → consuming budget in 5 days
Alert 3 (inform): burn_rate > 3× over 24h AND 3h                → budget will exhaust in ~10 days
```
Implement this in Prometheus recording rules + Alertmanager, or directly in Grafana, Datadog SLO monitors, or Google Cloud Monitoring.

---

### Phase 3 — Dashboards & Alerting

**8. Build dashboards for roles, not vanity.**
Three essential dashboards:

- **Service overview (RED)**: one row per service — RPS, error rate, p95 latency, active instances. This is the on-call first screen.
- **Resource health (USE)**: CPU/memory per container/pod, DB connection pool (active/idle/waiting), queue depth, cache hit rate.
- **Business metrics**: DAU, conversions, revenue rate, feature adoption — derived from application events, not infrastructure. Shows business impact of incidents.

Use Grafana with Prometheus/Loki/Tempo datasources for a unified stack. Dashboards as code: store in version control as JSON (`grafana-dashboard-*.json`) or use Grafonnet/Terraform provider. Never configure a dashboard manually only.

**9. Alert routing and on-call hygiene.**
- Route pages (P1, immediate response) to PagerDuty / Opsgenie → on-call rotation.
- Route tickets (P2, next business day) to a Slack channel + issue tracker.
- Suppress noisy alerts during known maintenance windows.
- Every alert must have: a description, a runbook link (`.claude/templates/runbook.md`), and a severity.
- Review alert history weekly during early operation: mute alerts that fired without requiring action (false positives → tune or remove); add alerts for incidents that were missed (gaps).

**10. Centralize logs with Loki or your cloud provider.**
- Ship structured JSON logs to Loki (if self-hosted Grafana stack), CloudWatch Logs (AWS), Google Cloud Logging, or Datadog Logs.
- Add log-based alerts for: `level=error` spike (more than N in 5 min), security events (auth failures, rate limit hits), and business anomalies (zero orders in 10 min during business hours).
- Set retention policies: hot tier 7–30 days (queryable), cold/archive 90–365 days (compliance). Do not retain logs indefinitely; they grow unboundedly and may contain PII.

---

### Phase 4 — Cardinality & Cost Control

**11. Control metric cardinality — it kills your backend.**
High-cardinality labels cause Prometheus TSDB memory explosions and Datadog cost overruns. Rules:
- **Never** use user IDs, order IDs, session IDs, UUIDs, or IP addresses as metric label values. These create millions of unique time series.
- **Safe labels**: HTTP method, route (normalized: `/users/:id` not `/users/12345`), status code, service, version, region, environment.
- If you need per-user or per-entity analytics, use a columnar store (ClickHouse, BigQuery) not a time-series database.
- In Prometheus: set a `scrape_config` with `metric_relabel_configs` to drop or normalize problematic labels before ingestion.

**12. Sample and filter before shipping.**
- Drop DEBUG logs from production unless a feature flag is on for that service instance.
- Use head-based sampling at 5–20% for healthy traces; always sample errors and slow requests.
- Use Prometheus recording rules to pre-aggregate expensive queries (`record: job:http_requests:rate5m`).

---

## Standards

**Do:**
- Instrument before you have an incident. Retro-fitting observability under outage pressure is extremely costly.
- Correlate logs and traces via `trace_id` injected into every log line. This is the single most valuable debugging capability.
- Express SLOs as ratios over a rolling window (28 or 30 days), not a fixed calendar period.
- Use histograms (not summaries or averages) for latency metrics. Averages hide tail latency; summaries can't be aggregated across instances.
- Store dashboards and alert rules as code in version control.
- Include a runbook link in every alert. An alert without a runbook is noise.
- Redact or hash PII before it enters logs (`user_id: hash(email)`, never raw email).
- Test alert conditions in staging before production by injecting synthetic errors.

**Do not:**
- Put user-identifying data (email, phone, full name) in log messages, metric labels, or span attributes without explicit PII-safe handling.
- Alert on CPU > 80% in isolation — this is a resource metric, not a user-impact signal. Alert on error budget burn instead.
- Create a metric label for every attribute. Treat high-cardinality data as events/logs, not metrics.
- Use plaintext logs — they are impossible to query at scale and can't be correlated with traces.
- Set alert thresholds without historical data; calibrate against at least 2 weeks of baseline.
- Log sensitive values: passwords, tokens, API keys, PANs, PII. These end up in log aggregators and violate GDPR/CCPA.
- Disable tracing in production "for performance" — modern auto-instrumentation overhead is < 1% at 10% sampling.

---

## Common mistakes to avoid

- **Alert fatigue from static thresholds**: alerts fire every day because the threshold was set without understanding normal variation. Fix: burn-rate alerts for SLO violations; silence or remove other threshold alerts.
- **Trace context dropped at queue boundary**: spans stop at the producer; the consumer has no parent. Fix: serialize `traceparent` into message metadata; extract on consume.
- **Cardinality explosion from route templating**: `/api/users/12345` as a label creates one series per user ID. Fix: normalize routes to `/api/users/:id` in middleware before labeling.
- **Missing error budget tracking**: SLO defined but not measured. Incidents extend without anyone knowing the budget is burning. Fix: implement recording rules for SLI ratio; wire to burn-rate alert.
- **Log-only debugging model**: errors logged but no traces, so distributed call chains are invisible. Fix: add auto-instrumentation and inject `trace_id` into log context.
- **Dashboards only in Grafana UI**: misconfiguration or team member changes break them. Fix: export and commit dashboard JSON to repo; use Terraform or Grafonnet.
- **Sampling kills error visibility**: sampling rate of 1% means 99% of errors are not traced. Fix: always sample `error=true` spans at 100%.

---

## Output format

Primary deliverables:
- **Observability spec**: `docs/specs/observability.md` — SLI/SLO definitions, instrumentation decisions, alert routing, retention policy, sampling strategy.
- **SLO/SLA document**: `docs/specs/slo-sla.md` using `.claude/templates/slo-sla.md`.
- **Runbook template per service**: `docs/runbooks/<service>.md` using `.claude/templates/runbook.md`.

Supporting artifacts (in project source):
- OTel SDK initialization module and auto-instrumentation config.
- Prometheus recording rules + alerting rules YAML.
- Grafana dashboard JSON (service RED, resource USE, business metrics).
- Structured logging middleware/interceptor for each service.
- Sampling config for OTel Collector.

---

## Related checklists
- `.claude/checklists/observability.md` — full checklist: logs structured, traces correlated, SLOs defined, burn-rate alerts wired, dashboards versioned, runbooks linked.
- `.claude/checklists/production.md` — production readiness gate includes observability as a P0 requirement.
- `.claude/checklists/incident-response.md` — what must be visible during an incident.

## Related agents
- `.claude/agents/quality/reliability-engineer.md` — SLO design, error budget policy, incident response.
- `.claude/agents/quality/performance-engineer.md` — latency SLIs, trace-based profiling, cardinality analysis.
- `.claude/agents/quality/production-readiness-auditor.md` — verifies observability gate before launch.
- `.claude/agents/engineering/devops-engineer.md` — OTel Collector deployment, Prometheus/Grafana stack, log aggregation pipeline.
- `.claude/agents/engineering/cloud-architect.md` — managed observability services (CloudWatch, Google Cloud Observability, Azure Monitor, Datadog).

# Monitoring Stack Matrix

Choose by answering three questions first: (1) Do you need logs, metrics, or traces — or all three? (2) Is self-hosting acceptable, or must the stack be fully managed? (3) What is the on-call / incident-response story? Most production systems need at least two pillars (e.g., metrics + logs), and a separate alerting/paging layer. Pick the fewest tools that cover your gaps rather than adopting an entire suite upfront.

Key decision drivers: operational burden vs. cost, vendor lock-in, data volume/retention needs, existing team familiarity, and whether the project is a single service or a distributed system with many services and teams.

---

## Sentry

- **When to use:** Any project that ships code to end users and needs error tracking, stack traces, release health, and session replay. Excellent first-monitoring-tool for early-stage projects.
- **When NOT to use:** As a replacement for infrastructure metrics or log aggregation. It captures application errors, not host CPU or database query latency.
- **Strengths:** Zero-config SDK integration for 100+ frameworks; automatic grouping of duplicate errors; source-map support; release tracking; performance tracing for web/mobile; generous free tier.
- **Weaknesses:** Not a general-purpose observability platform; no native metrics dashboards; storage costs escalate fast at high error volume; self-hosted version requires significant maintenance.
- **Team fit:** Fits every team size. Particularly valuable for small teams who need error visibility without a dedicated DevOps engineer.
- **Scale fit:** Handles millions of events per day on cloud plan. Above ~50 M events/month, cost modelling is required.
- **Production risks:** Over-relying on Sentry as the only monitoring tool; missing infrastructure failures that don't produce application exceptions. Rate-limiting errors if SDK is misconfigured.

---

## Datadog

- **When to use:** Medium-to-large organizations that need a single pane of glass across infrastructure metrics, APM, logs, synthetics, and security posture. Strong value when running on AWS/GCP/Azure with many managed services.
- **When NOT to use:** Small projects or early-stage startups — costs balloon quickly. Projects with strict data-residency requirements in regions Datadog doesn't support.
- **Strengths:** Best-in-class APM with distributed tracing; 600+ integrations; unified dashboards; ML-powered anomaly detection; log management with live tail; on-call via native integrations (PagerDuty, OpsGenie). 
- **Weaknesses:** Expensive at scale (per-host licensing model); vendor lock-in is high; complex pricing (metrics, APM hosts, log ingestion, retention all billed separately); can take weeks to instrument fully.
- **Team fit:** Teams with a dedicated platform/DevOps function; organizations that already buy SaaS tooling rather than self-host.
- **Scale fit:** Designed for fleets of hundreds to thousands of hosts; handles millions of custom metrics.
- **Production risks:** Bill shock if custom metrics or log volumes spike unexpectedly. Dependency on a single vendor for all observability data.

---

## Grafana / Prometheus

- **When to use:** Teams comfortable with self-hosting or using Grafana Cloud; projects where cost at scale matters; Kubernetes-native environments (Prometheus scrapes are a first-class primitive in K8s).
- **When NOT to use:** Teams without DevOps capacity to operate and tune Prometheus retention, alerting rules, and Grafana dashboards. Projects that need a single managed SaaS with zero ops.
- **Strengths:** Open-source with no per-host cost; Prometheus is the de-facto standard for K8s metrics; Grafana visualizes any data source; rich ecosystem (Alertmanager, Thanos, Cortex for scale-out); Grafana Cloud offers a managed tier with a generous free allowance.
- **Weaknesses:** Metrics only (no native log storage — pair with Loki); Prometheus retention is limited by local disk; requires disciplined label cardinality management to avoid performance issues; alert rule DSL (PromQL) has a learning curve.
- **Team fit:** DevOps/platform engineers; teams that value control and cost efficiency over convenience.
- **Scale fit:** Single Prometheus node handles ~1 M active time series; use Thanos or Cortex for multi-region or long-term retention at scale.
- **Production risks:** Prometheus single point of failure without HA setup (use two Prometheus replicas + Thanos). High-cardinality labels crash Prometheus.

---

## OpenTelemetry

- **When to use:** Any project that wants vendor-neutral instrumentation. Use OTel SDK in your code and route telemetry to any backend (Datadog, Grafana Tempo, Jaeger, Honeycomb, etc.). Essential for microservices and distributed tracing.
- **When NOT to use:** As a standalone monitoring solution — OTel is an instrumentation standard and collection pipeline, not a storage or visualization layer. Do not use if you want a zero-config path; OTel requires deliberate setup.
- **Strengths:** Vendor-neutral (avoids lock-in at the instrumentation layer); unified API for logs, metrics, and traces; backed by CNCF with wide industry adoption; auto-instrumentation available for many runtimes; OTel Collector can fan out to multiple backends simultaneously.
- **Weaknesses:** Maturity varies by language SDK (Java/Go/Python mature; others still stabilizing); collector configuration is complex for non-trivial topologies; adds operational overhead (collector fleet to manage).
- **Team fit:** Platform/infra teams building a standardized internal observability platform. Any team that may switch backends in the future.
- **Scale fit:** Scales horizontally via collector pools; backend determines ultimate scale ceiling.
- **Production risks:** Misconfigured sampling dropping critical traces in production. SDK overhead if not tuned (use tail sampling at the collector, not head sampling in the app).

---

## ELK Stack / Loki

- **When to use:** Log-heavy workloads — security audit trails, compliance logging, full-text search over application logs. ELK (Elasticsearch + Logstash + Kibana) for rich search; Loki (Grafana) for cost-efficient label-indexed log streams.
- **When NOT to use:** As a primary metrics or tracing platform. ELK is expensive and operationally heavy for teams that only need basic log tailing.
- **Strengths:** ELK: full-text search, powerful KQL query language, security/SIEM use cases. Loki: cost-efficient (indexes labels not content), integrates natively with Grafana, same query experience as Prometheus (LogQL).
- **Weaknesses:** ELK: high resource usage (Elasticsearch is memory-hungry), complex cluster management, licensing changes (Elastic moved to SSPL). Loki: full-text search is more limited than Elasticsearch; requires structured log format for efficient queries.
- **Team fit:** ELK fits security, compliance, and large engineering orgs. Loki fits DevOps/cloud-native teams already using Grafana/Prometheus.
- **Scale fit:** ELK scales to petabytes with proper index lifecycle management; Loki scales via object storage (S3/GCS) as the backend.
- **Production risks:** ELK: shard allocation issues, memory pressure on Elasticsearch nodes. Loki: slow queries without proper label cardinality strategy; no full-text indexing by default.

---

## PagerDuty / On-Call

- **When to use:** Any production system with SLA commitments or users who expect high availability. PagerDuty is the standard for enterprise on-call management; alternatives include OpsGenie, VictorOps (now Splunk On-Call), and open-source options like Grafana OnCall.
- **When NOT to use:** Side projects or internal tools with no on-call requirements. Early-stage startups where a Slack alert to the founding team is sufficient.
- **Strengths:** Reliable alert routing with escalation policies; on-call scheduling and rotation management; integration with virtually all monitoring tools; incident timeline and postmortem tooling; mobile app with push + phone call alerts.
- **Weaknesses:** Cost scales with users; learning curve for escalation policy configuration; can produce alert fatigue if alert rules are not tuned before wiring into PagerDuty.
- **Team fit:** Any team that needs structured on-call rotation — typically when team size exceeds ~4 engineers and product is revenue-generating.
- **Scale fit:** Handles any number of alerts per second; enterprise tier adds AI-based noise reduction.
- **Production risks:** Misconfigured escalation leaving an alert unacknowledged. Alert fatigue from noisy monitors causing on-call engineers to mute real incidents.

---

## Comparison Table

| Option | Signals covered | Managed SaaS | Self-host | Cost model | Best for | Vendor lock-in |
|---|---|---|---|---|---|---|
| Sentry | Errors, traces, replays | Yes | Yes (heavy) | Per event/seat | App error tracking | Medium |
| Datadog | Metrics, logs, traces, APM | Yes | No | Per host + ingestion | Full observability, large orgs | High |
| Grafana/Prometheus | Metrics (+ Loki for logs) | Grafana Cloud | Yes (native) | Open-source / volume | K8s, cost-sensitive | Low |
| OpenTelemetry | Logs, metrics, traces (pipeline) | Collector only | Yes | Free (infra cost only) | Vendor-neutral instrumentation | None |
| ELK / Loki | Logs (full-text / label) | Elastic Cloud / Grafana | Yes | Storage + compute | Log search, compliance | Medium |
| PagerDuty | Alerting, incident mgmt | Yes | No | Per user/seat | On-call, escalation | Medium |

---

## Recommended Combinations

- **Early-stage startup:** Sentry + Grafana Cloud free tier — error tracking plus basic infra metrics with no ops burden.
- **K8s / cloud-native (mid-size):** Prometheus + Grafana + Loki + Grafana OnCall — full self-hosted or Grafana Cloud stack; cost-efficient; OTel for instrumentation layer.
- **Enterprise / multi-team:** OpenTelemetry (instrumentation) → Datadog (storage + dashboards) + PagerDuty (on-call) — single pane of glass with structured incident management.
- **Compliance-heavy (fintech, healthcare):** ELK (Elastic Cloud) + Datadog APM + PagerDuty — rich audit log search, full APM, and paged on-call for SLA enforcement.
- **Cost-optimized at scale:** OpenTelemetry Collector → Prometheus (metrics) + Loki (logs) + Grafana Tempo (traces) + Grafana OnCall — the full Grafana LGTM stack, all open-source, S3-backed storage.

Cross-reference: `.claude/checklists/security.md` for log retention requirements, `.claude/agents/core/orchestrator.md` for alerting hooks in the CI/CD pipeline.

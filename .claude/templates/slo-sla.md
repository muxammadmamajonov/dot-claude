# SLO / SLA Document

**What this is:** Defines Service Level Indicators (SLIs), Service Level Objectives (SLOs), error budgets, measurement methodology, alerting thresholds, and the customer-facing Service Level Agreement (SLA) including credit terms. This is the contractual and operational source of truth for service reliability.

**Who fills this:** Reliability engineer + product manager, reviewed by tech lead, legal (for SLA terms), and customer success.

---

## 0. Document Metadata

| Field | Value |
|---|---|
| Service | `<service-name>` |
| Version | `<v1.0>` |
| Effective date | `<YYYY-MM-DD>` |
| Review cadence | `<Quarterly or after any SLO miss>` |
| Owners | `<SRE lead, Product Manager>` |

---

## 1. Service Overview

> Describe what the service does and why reliability matters to users.

- **Service description:** `<API and web application enabling <users> to <core action> — e.g., process payments, stream media, submit orders>`
- **User impact of degradation:** `<Revenue loss at $X/min downtime; regulatory risk; user churn above Y% incident rate>`
- **Criticality tier:** `<Tier 1 — mission-critical; Tier 2 — business-impacting; Tier 3 — internal/best-effort>`

---

## 2. Service Level Indicators (SLIs)

> An SLI is a quantitative measure of a specific aspect of the service. Define what you measure and how.

### 2.1 Availability

> What fraction of requests succeed?

- **Definition:** `(successful HTTP responses) / (total HTTP responses)` — where success = HTTP status < 500
- **Measurement source:** `<Load balancer access logs, synthetic monitoring, APM agent>`
- **Measurement window:** `<Rolling 30-day window>`
- **Exclusions:** `<Planned maintenance windows (max 4 h/quarter) excluded from denominator>`

### 2.2 Latency

> How fast do requests complete?

- **Definition:** `P99 response time of all API requests measured at the load balancer`
- **Measurement source:** `<APM tool — e.g., Datadog, New Relic, Prometheus histogram>`
- **Percentiles tracked:** P50, P95, P99, P999
- **Exclusions:** `<Health-check endpoints, batch export jobs>`

### 2.3 Error Rate

> What fraction of requests return errors visible to users?

- **Definition:** `(5xx responses + client-visible failures) / (total requests)`
- **Measurement source:** `<Application logs + APM>`

### 2.4 Freshness / Staleness (if applicable)

> How up-to-date is data served to users?

- **Definition:** `Age of the most-recently served record (e.g., feed, dashboard)`
- **Measurement source:** `<Timestamp field in response payload compared to wall clock>`

### 2.5 Durability (if applicable)

> What fraction of writes are safely stored and retrievable?

- **Definition:** `(successfully retrieved writes) / (acknowledged writes) measured over 30 days`
- **Measurement source:** `<Database checksums, backup restore tests>`

---

## 3. Service Level Objectives (SLOs)

> An SLO is the target value for an SLI. Be specific about window and threshold.

| SLI | SLO Target | Window | Notes |
|---|---|---|---|
| Availability | `≥ 99.9%` | Rolling 30 days | `Excludes planned maintenance` |
| Latency P99 | `≤ 500 ms` | Rolling 7 days | `All authenticated API endpoints` |
| Latency P50 | `≤ 80 ms` | Rolling 7 days | |
| Error rate | `≤ 0.1%` | Rolling 7 days | |
| Data freshness | `≤ 60 seconds` | Per-request | `For real-time feeds` |
| Durability | `≥ 99.999%` | Rolling 30 days | `For user-submitted data` |

> **Tip:** Start conservative (99.5% availability is still 3.6 h/month downtime) and tighten as reliability improves.

---

## 4. Error Budgets

> Error budget = 1 − SLO target. Consuming the budget signals when to stop feature work and invest in reliability.

| SLI | SLO | Error Budget (30-day) | In concrete time/volume |
|---|---|---|---|
| Availability 99.9% | 99.9% | 0.1% | `≈ 43.8 min downtime / month` |
| Availability 99.5% | 99.5% | 0.5% | `≈ 3.65 h downtime / month` |
| Error rate 0.1% | 0.1% | 0.1% | `1 error per 1,000 requests` |

### 4.1 Error Budget Policy

> What happens when the budget is consumed?

- **>50% consumed in first 2 weeks:** `<Alert SRE on-call; review incident list at next weekly sync>`
- **>75% consumed:** `<Freeze new feature rollouts; SRE/eng sprint on reliability items>`
- **100% consumed (SLO miss):** `<Incident review mandatory; postmortem with action items within 5 business days; escalate to VP Engineering>`
- **Budget reset:** `<Monthly, on the 1st>`

---

## 5. Measurement & Tooling

> Where do numbers come from, and how are they surfaced?

| SLI | Tool | Metric name / query | Dashboard link |
|---|---|---|---|
| Availability | `<Datadog / Prometheus>` | `<sum(rate(http_requests_total{status!~"5.."}[5m])) / sum(rate(http_requests_total[5m]))>` | `<link>` |
| Latency P99 | `<Datadog / Prometheus>` | `<histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))>` | `<link>` |
| Error rate | `<Datadog / APM>` | `<sum(rate(http_requests_total{status=~"5.."}[5m]))>` | `<link>` |
| Freshness | `<Custom app metric>` | `<feed_staleness_seconds>` | `<link>` |

- **Synthetic monitoring:** `<Uptime Robot / Pingdom / Checkly — synthetic health-check every 60 seconds from 3 regions>`
- **Alerting platform:** `<PagerDuty / OpsGenie>`
- **SLO dashboard:** `<link to Grafana / Datadog SLO dashboard>`

---

## 6. Alerting Thresholds

> Alert before the SLO is breached. Use burn-rate alerts to catch fast and slow burns.

| Alert | Condition | Severity | Response |
|---|---|---|---|
| Availability burn-rate fast | `<Error rate > 14.4× budget burn for 5 min>` | P1 / Page | `<Wake on-call immediately>` |
| Availability burn-rate slow | `<Error rate > 6× budget burn for 1 h>` | P2 / Notify | `<Notify SRE; investigate within 30 min>` |
| Latency P99 breach | `<P99 > 500 ms for 5 min>` | P2 | `<Investigate; scale if needed>` |
| Error rate spike | `<Error rate > 1% for 2 min>` | P1 / Page | `<Wake on-call>` |
| Error budget 50% consumed | `<Burn at current rate: budget exhausted < 15 days>` | P3 | `<Email to SRE + PM>` |
| Error budget 75% consumed | `<Burn at current rate: budget exhausted < 7 days>` | P2 | `<Slack #sre + feature freeze discussion>` |

---

## 7. Service Level Agreement (SLA)

> The SLA is the customer-facing commitment, typically weaker than the internal SLO, with defined remedies.

### 7.1 Uptime Commitment

| Tier | Monthly Uptime Commitment | Max Downtime / Month |
|---|---|---|
| `<Standard>` | `99.5%` | `3h 38m` |
| `<Professional>` | `99.9%` | `43m 49s` |
| `<Enterprise>` | `99.95%` | `21m 54s` |

> Internal SLO is tighter than the SLA to create a reliability buffer.

### 7.2 Definitions

- **Downtime:** `<Any period during which the service returns HTTP 5xx on > 10% of requests for > 5 consecutive minutes, excluding scheduled maintenance>`
- **Scheduled maintenance:** `<Communicated ≥ 72 hours in advance via status page; maximum 4 hours/quarter; not counted as downtime>`
- **Exclusions from SLA:** `<Force majeure; customer-caused incidents; third-party service outages beyond our control; free-tier accounts>`

### 7.3 Service Credits

| Monthly Uptime Achieved | Credit (% of monthly fee) |
|---|---|
| `< 99.9% and ≥ 99.0%` | `10%` |
| `< 99.0% and ≥ 95.0%` | `25%` |
| `< 95.0%` | `50%` |

- **Credit request window:** `<Must be submitted within 30 days of incident>`
- **Credit form:** `<support@<domain> with incident date, duration, evidence>`
- **Maximum credit:** `<50% of monthly fee for that service; credits are non-transferable and non-cashable>`

### 7.4 Escalation Path

| Step | Trigger | Contact |
|---|---|---|
| 1 | `<P2+ incident>` | `<Support ticket>` |
| 2 | `<No response in 1 h>` | `<Dedicated CSM>` |
| 3 | `<SLA breach or sustained P1>` | `<VP Customer Success — escalation email>` |

---

## 8. Review & Approval

| Reviewer | Role | Date |
|---|---|---|
| `<Name>` | `<SRE Lead>` | `<YYYY-MM-DD>` |
| `<Name>` | `<Product Manager>` | `<YYYY-MM-DD>` |
| `<Name>` | `<Legal / Commercial>` | `<YYYY-MM-DD>` |
| `<Name>` | `<VP Engineering>` | `<YYYY-MM-DD>` |

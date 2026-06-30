# Incident Postmortem

**What this is:** A blameless postmortem capturing what happened, why it happened, and what will be done to prevent recurrence. Focus is on system and process failures, not individuals. Published internally within 5 business days of incident resolution.

**Who fills this:** Incident commander + on-call responders, reviewed by engineering manager and affected team leads. All participants contribute to the timeline and 5 Whys.

---

## 0. Document Metadata

| Field | Value |
|---|---|
| Incident ID | `<INC-2024-0142>` |
| Severity | `<P1 / P2 / P3 / P4>` |
| Status | `<Draft / In review / Published>` |
| Author(s) | `<Name, role>` |
| Reviewers | `<Name, role>` |
| Published date | `<YYYY-MM-DD>` |
| Incident start | `<YYYY-MM-DD HH:MM UTC>` |
| Incident end (resolved) | `<YYYY-MM-DD HH:MM UTC>` |
| Total duration | `<X hours Y minutes>` |

---

## 1. Executive Summary

> 3–5 sentences. What went wrong, who was affected, for how long, and the headline root cause.

`<On 2024-03-15 at 14:32 UTC, the checkout API became unavailable for approximately 47 minutes due to a database connection pool exhaustion triggered by a slow-query regression introduced in the v3.12 deployment 18 minutes prior. Approximately 2,400 users were unable to complete purchases, resulting in an estimated $18,000 in lost GMV. The root cause was an unindexed query added in a new reporting feature that caused a table-scan on the orders table under production load. The incident was detected via automated alerting at 14:35 UTC and resolved by rolling back the deployment.>`

---

## 2. Impact

> Quantify the blast radius: users affected, revenue, SLO impact, and any downstream effects.

| Dimension | Value |
|---|---|
| Users affected | `<~2,400 unique users attempted checkout during the window>` |
| Requests failed | `<~28,000 5xx errors across checkout and order-status endpoints>` |
| Availability during incident | `<61.3% (well below 99.9% SLO)>` |
| Error budget consumed | `<~14× normal burn rate; ~3× monthly error budget consumed in 47 min>` |
| Revenue impact | `<~$18,000 estimated lost GMV (avg order value $7.50 × ~2,400 failed sessions)>` |
| Downstream services affected | `<Order fulfillment queue backed up; email notification service delayed by 12 min>` |
| Customer-facing status page | `<Updated at 14:38 UTC; resolved notice at 15:21 UTC>` |
| Support tickets opened | `<43 tickets; 11 escalated to customer success>` |

---

## 3. Timeline

> Granular chronological record. Use UTC. Note who detected / acted. Include what was tried even if it didn't work.

| Time (UTC) | Event | Actor |
|---|---|---|
| `<14:14>` | `<v3.12 deployment initiated via CI/CD pipeline>` | `<Automated / release engineer>` |
| `<14:18>` | `<v3.12 deployment completes; traffic shifted to new version>` | `<Automated>` |
| `<14:32>` | `<DB connection pool at 100%; checkout API begins returning 503s>` | `<System>` |
| `<14:35>` | `<PagerDuty alert fires: "Checkout availability < 80% for 3 min">` | `<Alerting system>` |
| `<14:36>` | `<On-call engineer acknowledges alert, begins investigation>` | `<@on-call-eng>` |
| `<14:40>` | `<DB slow query log shows full table scan on orders; correlated to new reporting query>` | `<@on-call-eng>` |
| `<14:42>` | `<Incident declared P1; incident commander engaged; #incident-2024-0142 Slack channel opened>` | `<@incident-commander>` |
| `<14:45>` | `<Attempted to disable reporting feature flag — flag not wired to this query path>` | `<@on-call-eng>` |
| `<14:48>` | `<Decision made to roll back v3.12 to v3.11>` | `<@incident-commander>` |
| `<14:51>` | `<Rollback initiated via pipeline>` | `<@on-call-eng>` |
| `<15:02>` | `<v3.11 live; connection pool begins draining; error rate drops below 5%>` | `<System>` |
| `<15:09>` | `<Error rate < 0.1%; service declared recovered>` | `<@incident-commander>` |
| `<15:21>` | `<Status page updated: "Resolved">` | `<@comms-lead>` |
| `<15:30>` | `<Postmortem kickoff scheduled for 2024-03-16 10:00 UTC>` | `<@incident-commander>` |

---

## 4. Detection

> How was the incident discovered? Was automated alerting sufficient? What could have caught it sooner?

- **Detected by:** `<Automated PagerDuty alert — availability burn-rate alert triggered at 14:35 UTC>`
- **Time to detect (TTD):** `<3 minutes after first 503 errors>`
- **Detection gap:** `<The slow query began degrading DB performance at 14:20 but did not breach alert thresholds until connection pool was full at 14:32 — 12 minutes of degradation before severe impact>`
- **Missed signals:** `<DB CPU alert set at 95% threshold — CPU hit 92% at 14:25 but did not alert; connection pool utilization alert did not exist>`
- **What would have caught it earlier:** `<Connection pool utilization alert at 80%; DB query P99 latency alert; pre-deployment query plan check in CI>`

---

## 5. Root Cause Analysis — 5 Whys

> Drill down from symptom to systemic cause. Stop when you reach a process or system that can be improved.

| Why # | Question | Answer |
|---|---|---|
| 1 | Why did checkout fail? | `<The database connection pool was exhausted, causing all new checkout requests to queue and time out>` |
| 2 | Why was the connection pool exhausted? | `<A query in the new reporting feature performed a full table scan on the 50M-row orders table, holding connections for 30–60 seconds each>` |
| 3 | Why did the full table scan occur? | `<The query filtered on `created_at` which lacks an index; the developer tested on a 10K-row dev database where the scan completed in < 1ms>` |
| 4 | Why was there no index on `created_at`? | `<The column was added 6 months ago for analytics queries; an index was planned but deprioritized and never completed>` |
| 5 | Why wasn't the missing index caught before production? | `<There is no automated EXPLAIN ANALYZE / query plan check in CI/CD; code review did not include a database expert; staging data volume is < 1% of production>` |

**Root cause:** Absence of automated query-plan analysis in CI and insufficient staging data volume allowed a performance regression to reach production undetected.

---

## 6. Contributing Factors

> Secondary factors that made the incident worse or harder to resolve. Not the root cause, but each is actionable.

- **No feature flag on the slow query path:** `<The reporting feature had a feature flag, but the slow query was also called from a background sync job not gated by the flag — disabling the flag had no effect>`
- **Alert threshold misconfigured:** `<DB CPU alert threshold was 95% rather than 80%; connection pool utilization was not monitored at all>`
- **Rollback required manual steps:** `<The pipeline rollback required two manual approvals totalling ~3 minutes; fully automated rollback on SLO breach was not configured>`
- **Status page lag:** `<Status page was updated 6 minutes after alert; process was unclear for who owns comms during P1>`
- **Staging data gap:** `<Staging database has ~50K rows vs. 50M in production — query performance on staging is not representative>`

---

## 7. What Went Well

> Blameless postmortems also capture effective practices to reinforce.

- `<Alerting fired within 3 minutes of impact — well within the P99 TTD target of 5 minutes>`
- `<The on-call engineer correctly correlated the deployment to the incident within 4 minutes using deployment markers in the APM dashboard>`
- `<The incident commander opened a dedicated Slack channel and ran a tight 15-minute decision loop that led to the rollback decision>`
- `<Rollback pipeline completed in under 3 minutes once initiated>`
- `<Customer comms (status page + proactive email to enterprise customers) was completed within 2 hours of resolution>`

---

## 8. Action Items

> Concrete, owned, time-boxed actions to prevent recurrence and reduce blast radius.

| # | Action | Type | Owner | Due | Status |
|---|---|---|---|---|---|
| AI-01 | `<Add EXPLAIN ANALYZE to CI pipeline; fail build if query plan includes Seq Scan on tables > 1M rows>` | Prevention | `<@backend-lead>` | `<2024-03-29>` | `<Open>` |
| AI-02 | `<Add index on orders.created_at; test migration on staging with production-scale dataset>` | Prevention | `<@db-admin>` | `<2024-03-22>` | `<Open>` |
| AI-03 | `<Increase staging database to ≥ 10% of production row count; automate refresh from anonymized prod snapshot weekly>` | Prevention | `<@devops>` | `<2024-04-05>` | `<Open>` |
| AI-04 | `<Add DB connection pool utilization alert at 70% (warn) and 85% (page)>` | Detection | `<@sre>` | `<2024-03-19>` | `<In progress>` |
| AI-05 | `<Lower DB CPU alert threshold from 95% to 80%>` | Detection | `<@sre>` | `<2024-03-19>` | `<In progress>` |
| AI-06 | `<Implement automated rollback triggered when P1 alert fires for > 5 min and deployment is < 30 min old>` | Response | `<@platform-lead>` | `<2024-04-12>` | `<Open>` |
| AI-07 | `<Document P1 comms runbook: who updates status page, when, template language>` | Process | `<@comms-lead>` | `<2024-03-25>` | `<Open>` |
| AI-08 | `<Require database migration review by a DB-experienced engineer in code review checklist>` | Prevention | `<@engineering-manager>` | `<2024-03-22>` | `<Open>` |
| AI-09 | `<Gate all background-job query paths with the same feature flag used for the UI>` | Prevention | `<@backend-lead>` | `<2024-03-29>` | `<Open>` |

---

## 9. Lessons Learned

> Higher-level insights for the engineering organization.

- **Test at production scale:** `<Performance characteristics of queries can be orders of magnitude worse at production data volumes. Staging must be representative.>`
- **Instrument what you deploy:** `<Every deployment should have query plan checks, not just functional tests.>`
- **Blast radius containment:** `<Feature flags must gate all code paths that depend on a feature, including background jobs and cron tasks — not just the UI path.>`
- **Automate response at known failure modes:** `<A recent deployment + an SLO breach is a strong signal for automated rollback; human decision latency added ~10 minutes to MTTR.>`

---

## 10. Sign-off

| Reviewer | Role | Date |
|---|---|---|
| `<Name>` | `<Incident Commander>` | `<YYYY-MM-DD>` |
| `<Name>` | `<Engineering Manager>` | `<YYYY-MM-DD>` |
| `<Name>` | `<On-call Engineer>` | `<YYYY-MM-DD>` |
| `<Name>` | `<SRE Lead>` | `<YYYY-MM-DD>` |

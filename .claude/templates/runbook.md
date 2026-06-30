# Operational Runbook — `<service / component name>`

> **What this is:** the on-call survival guide for one service. Filled in by the **reliability-engineer** + **devops-engineer** agents before launch (stage 7) and kept current as the system changes. If it's 3am and something is on fire, this is the document the responder opens. Verified against the [production checklist](../checklists/production.md).

---

## 1. At a glance
> The 30-second orientation.

- **Owner / on-call:** `<team / rotation>`
- **What it does:** `<one line>`
- **Tier / criticality:** `<P0 user-facing | internal | batch>`
- **Dependencies (upstream):** `<DB, queue, 3rd-party APIs>`
- **Dependents (downstream):** `<who breaks if this breaks>`

## 2. Health & dashboards
> Where to look first.

| Signal | Where | Healthy looks like |
|--------|-------|--------------------|
| Liveness | `<URL / dashboard>` | `<200, p95 < Xms>` |
| Error rate | `<dashboard>` | `<< 0.1%>` |
| Queue depth / lag | `<dashboard>` | `<< N>` |

- **Logs:** `<query / link>` · **Traces:** `<link>` · **Alerts route to:** `<pager/channel>`

## 3. Common alerts → response
> One row per alert. The responder should be able to act from this table alone.

| Alert | Likely cause | First checks | Mitigation |
|-------|--------------|--------------|------------|
| `<HighErrorRate>` | `<bad deploy / dependency down>` | `<recent deploys, dep status>` | `<rollback (see §5) / failover>` |
| `<LatencyP95High>` | `<DB slow / saturation>` | `<DB load, CPU, pool>` | `<scale out / shed load>` |

## 4. Standard operations
> Routine, safe procedures. Note which require approval.

- **Restart:** `<command / console steps>`
- **Scale up/down:** `<how>` (approval: `<who>`)
- **Drain / cordon:** `<how>`
- **Feature flag kill-switch:** `<flag name + where to toggle>`

## 5. Rollback procedure
> The single most important section. Must be tested.

> 1. `<identify last-good version>`  2. `<command to roll back>`  3. `<verify health §2>`  4. `<communicate status>`
> Database migrations: `<down-migration command / forward-fix policy — never delete migrations>`

## 6. Backups & recovery
- **What's backed up:** `<datastores>` · **Frequency:** `<>` · **RPO/RTO:** `<5 min / 1 h>`
- **Restore procedure:** `<step-by-step, with the last time it was tested: <date>>`

## 7. Escalation
> When and to whom.

| Condition | Escalate to | How |
|-----------|-------------|-----|
| `<not resolved in 30 min>` | `<secondary on-call / lead>` | `<page / call>` |
| `<data loss / security>` | `<incident commander + security>` | `<declare incident>` |

## 8. Incident checklist
- [ ] Acknowledge the alert and declare severity.
- [ ] Mitigate first (rollback/flag), diagnose second.
- [ ] Communicate status to stakeholders on a cadence.
- [ ] Capture a timeline for the postmortem.
- [ ] After recovery: open a blameless postmortem and follow-up actions.

---
**Done when:** dashboards/alerts are linked, every routine alert has a response row, the rollback and restore procedures are written **and tested** (with dates), and escalation paths name real people/rotations. Keep this file current — a stale runbook is worse than none.

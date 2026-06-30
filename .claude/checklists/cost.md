# Cloud & Infrastructure Cost Checklist

Gate for cloud and infrastructure cost controls: budget alerts, unit economics, right-sizing, egress, idle resources, reserved/committed use, and cost per request.

## P0 — Blockers (must pass before launch)

- [ ] Cloud budget alert is configured at 50 %, 80 %, and 100 % of monthly forecast; alert fires to on-call Slack channel and triggers an escalation runbook — not just email.
- [ ] Hard spending cap (quota or budget action) set on every cloud account/project to prevent runaway spend; tested by simulating an overage in a staging account.
- [ ] All infrastructure is tagged consistently (project, environment, team, cost-center, service); untagged resources are blocked at deploy time via policy (AWS SCP / GCP OrgPolicy / Azure Policy).
- [ ] Unit economics baseline established pre-launch: cost per active user, cost per API request, cost per GB stored — documented in `docs/cost-model/`.
- [ ] No public-facing storage bucket, queue, or cache with open read/write access that could be exploited for cost amplification (crypto mining, data exfiltration egress).
- [ ] Egress costs estimated and within budget: cross-region, CDN origin pull, and database replication egress accounted for; CDN caching verified to reduce origin hits.
- [ ] Load test run at 2× expected peak; resulting cost projected and within budget; autoscaling upper bound set to cap runaway scaling.
- [ ] Every recurring scheduled job or background worker has an idle-state kill switch or scale-to-zero configuration to avoid 24/7 compute cost during low-traffic periods.

## P1 — Important (address soon after launch)

- [ ] Right-sizing audit completed: every VM, container, or serverless function memory/CPU limit set to the 90th-percentile observed usage + 20 % headroom — no default/oversized instances in production.
- [ ] Reserved Instances, Savings Plans, or Committed Use Discounts purchased for stable baseline workloads (>30 % predictable load) — on-demand pricing only for burst capacity.
- [ ] Data transfer architecture reviewed: data processed as close to storage as possible (avoid cross-AZ or cross-region hops for hot paths); S3 Transfer Acceleration / CDN used only where justified.
- [ ] Database provisioned capacity (RCUs/WCUs, IOPS) reviewed against actual peak metrics; serverless/autoscaling mode enabled where appropriate.
- [ ] Idle and orphaned resources automated cleanup: snapshots older than 90 days reviewed, unattached volumes deleted, stopped instances older than 7 days terminated.
- [ ] Third-party SaaS costs audited: seats, API call tiers, and data retention pricing confirmed against actual usage; overage alerts configured per vendor.
- [ ] Cost anomaly detection enabled (AWS Cost Anomaly Detection / GCP Billing Budget anomaly / Azure Cost Alerts); anomaly threshold set to ±20 % week-over-week.

## P2 — Hardening

- [ ] Multi-account / multi-project cost allocation implemented: each environment (dev/staging/prod) billed separately; chargeback or show-back reports generated monthly.
- [ ] Container image sizes minimised (multi-stage builds, distroless bases) to reduce ECR/GCR storage and network transfer costs.
- [ ] Spot/Preemptible instances or ARM-based instances (Graviton, T2A) evaluated and adopted for fault-tolerant batch and stateless workloads.
- [ ] Cache hit-rate monitored (Redis, CDN, HTTP cache headers): target ≥ 80 % hit rate on hot reads to prevent expensive downstream DB or API calls.
- [ ] Log retention tiered: hot logs (7 days), warm (30 days in cheaper storage tier), cold/archive (90–365 days in Glacier/Coldline); logs older than retention policy deleted automatically.
- [ ] AI/ML inference costs tracked per model, per endpoint, per token; model caching and batching strategies applied; cheaper models used for classification, expensive ones only for generation.

## P3 — Post-launch / backlog

- [ ] FinOps practice established: monthly cost review meeting with engineering and finance; top-5 cost drivers reviewed and actioned.
- [ ] Cost-per-feature tracking added to the CI/CD pipeline: deploy-time cost estimate diff shown in pull request comments (Infracost or equivalent).
- [ ] Green / carbon efficiency reviewed: region selection considers carbon intensity data (Cloud Carbon Footprint); carbon credits or offset programme evaluated.

## How to use

Run this checklist via the `audit-production` command or the `cloud-architect` / `infrastructure-engineer` agents before launch and after any significant infrastructure change. P0 items block launch sign-off. Populate actual cost figures in `docs/cost-model/` and link each P0 item to a screenshot or exported budget report as evidence.

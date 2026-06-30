# Incident Response Checklist

Incident-readiness gate: runbooks verified, on-call rotation active, severity levels defined, communications plan documented, postmortem process established, rollback tested, and status page operational.

## P0 — Blockers (must pass before proceeding/launch)

- [ ] Severity level taxonomy is documented, agreed upon, and published (e.g., SEV-1 = complete outage, SEV-2 = major degradation, SEV-3 = partial impact, SEV-4 = low-impact/cosmetic) with concrete examples for each level.
- [ ] On-call rotation is configured in PagerDuty/OpsGenie/VictorOps (or equivalent) with at least two engineers per shift and an escalation chain that reaches a final human decision-maker within 15 minutes for SEV-1.
- [ ] A primary runbook exists for every critical failure mode identified during architecture review (database outage, auth provider down, payment processor failure, CDN/DNS failure, etc.).
- [ ] Each runbook has been walk-tested (dry-run) by an engineer other than the author; date and tester name are recorded.
- [ ] Rollback procedure for the most recent production deployment has been tested end-to-end in a staging or pre-prod environment and documented with timing (how long rollback takes).
- [ ] A status page (Statuspage.io, Instatus, self-hosted) is live with at minimum one subscriber; URL is publicly reachable.
- [ ] Incident communication channel (Slack `#incidents` or equivalent) and bridge/war-room procedure (video call link) are documented and all on-call engineers have access.
- [ ] Alerting covers the four golden signals: latency P95/P99 breaches SLO, error rate > threshold, saturation (CPU/memory/disk > 85%), and traffic anomalies (drop or spike beyond 3-sigma baseline).
- [ ] All production secrets are rotatable without a full deployment; rotation runbook exists and has been tested.

## P1 — Important (soon after launch)

- [ ] SEV-1 time-to-detect (TTD) target ≤ 5 minutes and time-to-acknowledge (TTA) ≤ 10 minutes are enforced by alert routing; review alert history to confirm targets are met.
- [ ] Postmortem template is adopted and stored (see `.claude/templates/incident-postmortem.md`); at least one practice postmortem has been conducted before launch.
- [ ] Blameless postmortem process is documented: who facilitates, timeline reconstruction method, root-cause analysis technique (5-Whys, Fishbone, or equivalent), and action-item ownership assignment.
- [ ] External dependency incidents are tracked: integrations with third-party APIs (payment, auth, email, cloud provider) subscribe to their status feeds and have documented fallback behaviors.
- [ ] Incident commander role is defined with explicit authority to make deployment, rollback, and customer-communication decisions without additional approval during active SEV-1/2.
- [ ] Customer-facing incident communication templates (email, status page update, social post) are pre-drafted for common failure scenarios to reduce drafting time under pressure.
- [ ] Log aggregation (Datadog, Grafana Loki, CloudWatch, Elastic, or equivalent) retains at minimum 30 days of application and infrastructure logs accessible from a single pane.
- [ ] Runbook index exists (linked from on-call handbook) so any on-call engineer can locate the correct runbook within 2 minutes of an alert firing.

## P2 — Hardening

- [ ] Chaos engineering experiments (Chaos Monkey, LitmusChaos, Gremlin, or equivalent) have validated at least three failure scenarios documented in runbooks; results are recorded.
- [ ] Automated remediation runbooks (auto-restart crashed pods, auto-scale on saturation, auto-failover to read replica) are implemented for the top three most frequent incident types.
- [ ] Incident retrospective metrics are tracked quarterly: mean time to detect (MTTD), mean time to resolve (MTTR), repeat-incident rate; targets are set and reviewed with leadership.
- [ ] On-call handbook covers off-hours procedures: escalation path when primary is unreachable, emergency contact list including vendor support contacts with SLA tier and phone numbers.
- [ ] Database failover (primary → replica promotion) has been tested and timing documented; RPO and RTO objectives are formally stated and validated against test results.
- [ ] Security incident response procedure is separate from operational incidents: covers breach discovery, evidence preservation, legal/compliance notification timelines (e.g., GDPR 72-hour breach notification), and external security contact (CERT, vendor PSIRT).

## P3 — Post-launch / backlog (track, revisit after launch; never blocks)

- [ ] Incident response tabletop exercises conducted semi-annually with cross-functional participants (engineering, customer success, legal, comms).
- [ ] AI-assisted log triage or anomaly detection integrated into incident workflow to surface relevant log lines and reduce MTTD.
- [ ] Incident cost tracking enabled: financial impact of each SEV-1/2 is estimated and reported to leadership to prioritise reliability investment.

## How to use

**When:** Complete P0 items as a pre-launch gate (at least two weeks before launch to allow time for walk-testing). P1 items must be in-progress at launch. Revisit the full checklist after every SEV-1 or SEV-2 incident and after every major architecture change.

**Who:** `reliability-engineer` agent (`.claude/agents/quality/reliability-engineer.md`) and `devops-engineer` (`.claude/agents/engineering/devops-engineer.md`) are primary owners. `technical-lead` signs off on P0 completion.

**Command:** `/audit-production` (`.claude/commands/audit-production.md`) includes this checklist. `/prepare-launch` (`.claude/commands/prepare-launch.md`) requires P0 green before approving launch.

**Tools:** PagerDuty/OpsGenie, Statuspage.io/Instatus, Datadog/Grafana/CloudWatch, LitmusChaos/Gremlin, incident.io or Jira incident management, Confluence/Notion for runbook storage.

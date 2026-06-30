# Launch Checklist

Go-live gate and rollback readiness — passing this proves that every critical system is verified in production, every stakeholder has signed off, and the team can respond to any failure within 30 minutes without data loss. Severity tiers: P0=blocker, P1=important (fix shortly after launch), P2=hardening, P3=post-launch / backlog (track and revisit; never blocks shipping).

## P0 — Blockers (must pass before proceeding / launch)

- [ ] All P0 items in `.claude/checklists/security.md`, `.claude/checklists/performance.md`, `.claude/checklists/devops.md`, `.claude/checklists/production.md`, and `.claude/checklists/qa.md` are individually checked, signed off by a named owner, and the sign-off is recorded in the project's `docs/state/` or a launch sign-off document.
- [ ] Smoke test suite covering the top 5 critical user journeys (or equivalent for non-UI systems: top 5 API contracts or workflows) passes against the live production environment using real infrastructure — not a staging clone or mocked dependencies.
- [ ] Rollback plan is documented with exact commands or pipeline steps, the estimated time to execute (target ≤ 15 min from decision to traffic cutover), the name of the engineer responsible for execution, and evidence it was rehearsed at least once in staging within the past 7 days.
- [ ] Traffic-switching mechanism is in place and verified: feature flag, canary deployment, blue-green cutover, or weighted DNS split can shift traffic from 0% to 100% and back in under 5 minutes; the reversal was tested in staging.
- [ ] DNS propagation confirmed, TLS certificate is valid with ≥ 60 days remaining, HSTS header is set with `max-age ≥ 31536000`, and a full TLS handshake test (e.g., `ssl-labs` or `testssl.sh`) scores A or higher with no mixed-content warnings.
- [ ] Legal and compliance sign-off obtained and documented: privacy policy published, terms of service published, cookie consent banner implemented (if applicable to jurisdiction), and any mandatory regulatory certifications (PCI-DSS SAQ, HIPAA BAA, SOC 2, GDPR DPA) are in place or formally scoped out with a written rationale.
- [ ] Personally identifiable information (PII), financial data, and health data flows are mapped and confirmed to stay within declared jurisdictions; data processing agreements with sub-processors are signed.
- [ ] Data migration (if any) is complete: row counts, referential integrity checks, and spot-checks of critical records confirm correctness; the migration script is idempotent; a full dry run was executed against a production-equivalent dataset within the past 48 hours with zero errors.
- [ ] Support and escalation paths are operational before the first user hits production: helpdesk queue is staffed, public status page is live (Statuspage.io, Instatus, or equivalent), and a customer-facing incident communication template is ready to send within 15 minutes of a P0 incident.
- [ ] On-call rotation is confirmed active with a primary and secondary engineer for the launch window; production monitoring dashboards are open and verified to be receiving live data; a launch war-room channel is created and all responders are present.
- [ ] No production service uses test-mode credentials, sandbox payment keys, or development OAuth client IDs; all third-party integrations have been validated with live production credentials on the production environment.

## P1 — Important (fix before scaling / shortly after launch)

- [ ] Analytics and conversion-event tracking verified firing correctly in production for every primary KPI defined in `docs/specs/` or the product spec template; events appear in the analytics dashboard within the expected latency window.
- [ ] Error-tracking tool (Sentry, Bugsnag, Rollbar, Honeybadger, or equivalent) is receiving events from the production environment, source maps or debug symbols are uploaded, and alert thresholds for error rate and new issue spikes are configured and tested by triggering a sample error.
- [ ] Transactional emails (welcome, password reset, purchase receipt, account notification) are tested end-to-end in production using real addresses; SPF, DKIM, and DMARC records pass validation (MXToolbox or equivalent); emails arrive in under 60 seconds.
- [ ] Rate limits and quota headroom verified for all third-party APIs under 2× expected launch traffic; upgrade plans or API quota increases are confirmed in writing from the vendor where needed.
- [ ] Post-launch monitoring schedule is written and assigned: named engineers will check dashboards and error rates at T+1 h, T+4 h, and T+24 h after go-live; documented thresholds define when a rollback decision is triggered.
- [ ] Launch communications drafted, reviewed, and scheduled: internal announcement, customer email / changelog, and any social or press content are approved and queued for the correct time.
- [ ] Auto-scaling policy is verified to respond correctly under production-equivalent load: scale-out fires before CPU/memory/RPS thresholds are breached, and scale-in does not drop in-flight requests.

## P2 — Hardening / nice-to-have

- [ ] A closed beta or soft-launch cohort (internal users, invited testers, or a waitlist segment) has run the release for ≥ 48 hours with no P0 or P1 issues before full public rollout; feedback is triaged and addressed.
- [ ] Load test at 2× expected peak traffic was run against the production environment or a full production clone within the past 7 days; p95 latency and error rates remained within SLA; results are documented in `docs/`.
- [ ] Automated synthetic monitoring (Checkly, Pingdom, CloudWatch Synthetics, or equivalent) runs the critical user journey every 5 minutes from at least two geographic regions and pages on-call on failure.
- [ ] App-store or marketplace submission (if applicable) is approved by the platform, version numbers and release notes are finalized, and the release is ready to publish with a single click.
- [ ] Launch retrospective is scheduled for 1 week post-launch to capture what went well, what was missed, and how to update this checklist for the next release.

## P3 — Post-launch / backlog (track and revisit after launch; never blocks shipping)

- [ ] Launch retrospective findings are actioned: each item from the 1-week post-launch retrospective is triaged into the backlog with a severity, an owner, and a target sprint; the retrospective document is stored in `docs/decisions/` and linked from the next release's launch checklist.
- [ ] Rollback runbook is refined with real timing data from the launch window: actual execution times replace estimates, any steps that were unclear or missed are corrected, and a second engineer validates the updated procedure in staging.
- [ ] Canary or progressive-rollout pipeline is automated for subsequent releases: traffic shift increments (1% → 10% → 50% → 100%) are driven by automated pass/fail checks on error rate and p95 latency, not manual observation, so future launches require less war-room overhead.
- [ ] On-call rotation and escalation paths are reviewed post-launch: response times during the launch window are measured against the 30-minute SLA; gaps in coverage or knowledge are addressed before the next major release.
- [ ] Third-party quota headroom is re-evaluated 30 days post-launch against actual traffic: any API or service that consumed > 60% of its quota during the first week is flagged for upgrade or rate-limit mitigation before the next traffic growth milestone.

## How to use

This is the final gate before flipping production traffic. Run `.claude/commands/prepare-launch.md` and invoke `.claude/agents/core/orchestrator.md` to coordinate the launch sequence. Assign a named owner to every P0 item; each P0 requires a checkmark and a sign-off comment before launch proceeds. A single unchecked P0 item is a hard stop — do not launch. Reference `.claude/checklists/production.md` for ongoing post-launch monitoring obligations and `.claude/agents/quality/production-readiness-auditor.md` for the readiness audit. Mark each item `[x]` when verified or `[-]` when formally waived with a written justification and the approving stakeholder's name.

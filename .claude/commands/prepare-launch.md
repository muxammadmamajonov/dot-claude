---
description: Walk the launch checklist; verify go-live gates; produce the launch plan and rollback plan.
argument-hint: [launch date — optional, e.g. 2026-07-01]
---

# /prepare-launch

## Purpose
Orchestrate the final go-live sequence. Verify every prerequisite gate is met, produce a time-ordered launch plan with owner slots, and produce a tested rollback plan. This command does not deploy — it produces the plan and validates readiness so the human team executes the actual cutover with confidence.

## When to use
- Immediately before a first public launch or a major version release.
- Before migrating live traffic from a legacy system to the new one.
- Before a planned maintenance window with breaking changes.
- Run only after `/audit-security`, `/audit-performance`, and `/audit-production` have all produced GREEN or AMBER (no RED) results.

## Workflow

### Step 0 — Confirm prerequisites
1. Check that the following reports exist and are dated within the last 14 days:
   - `docs/reports/security-audit-<date>.md` — no P0 open items.
   - `docs/reports/perf-audit-<date>.md` — all budgets met.
   - `docs/reports/prod-readiness-<date>.md` — no RED pillars.
2. If any report is missing or stale, **STOP — tell the user which audit(s) must be run first.** Do not continue.
3. If any report shows open P0 security findings or RED production-readiness items, **STOP — list the blockers and refuse to produce a launch plan until they are resolved.**
4. Read `docs/specs/` for the stated launch scope, target audience, and rollout strategy (big-bang, canary, feature-flag, regional wave).
5. If a launch date was given as argument, record it; otherwise **STOP — ask the user for the target launch date and time (with timezone).** This is a business-critical decision.

### Step 1 — Inventory launch artefacts

**Launch checklist by project type.** The infrastructure and integration items below are written for web/SaaS. Apply only the branch(es) matching the project type; for non-web types, substitute the equivalent go-live gate:
- **Web / SaaS** — the items as written below (DNS TTL, CDN purge, SSL renewal, cookie consent).
- **Mobile (iOS/Android)** — app-store submission and review lead time; phased/staged rollout %; store listing, screenshots, and privacy nutrition labels; minimum-OS and force-update gating.
- **Desktop** — code-signing certificate and notarization (macOS) / Authenticode (Windows); auto-update channel and delta packages; installer signing and SmartScreen/Gatekeeper reputation.
- **Game** — platform store certification (console/Steam/mobile); day-one patch staged; build submitted before cert deadline; rollback build retained.
- **CLI / library** — package-registry publish (npm/PyPI/crates.io/etc.); semver bump and tag; changelog/release notes; deprecation notices for removed APIs; provenance/signing where supported.
- **Embedded / IoT** — firmware OTA rollout in waves; signed firmware images; A/B partition or staged rollback path; device-fleet health gating before fleet-wide push.
- **Blockchain / smart contract** — contract deployment to target network; source verification on the explorer; completed security audit; multisig/timelock and upgrade/pause path confirmed.

Verify each item exists and is current:

**Code and build**
- [ ] All feature branches merged to the release branch.
- [ ] Release tag created (`git tag v<N.N.N>`).
- [ ] CI pipeline is green on the release commit.
- [ ] Docker image / binary / package is built and pushed to the registry with the release tag.
- [ ] Environment variables and secrets are provisioned in the production secret store (no `.env` files on servers).

**Data**
- [ ] Database migrations are written, tested on staging, and confirmed backwards-compatible.
- [ ] Seed data or reference data scripts are ready if required.
- [ ] Pre-launch backup of the production database is scheduled (run immediately before cutover).

**Infrastructure**
- [ ] Production environment is provisioned and matches the staging configuration.
- [ ] Autoscaling/capacity policy is enabled and tested (or fixed-capacity confirmed for non-elastic targets).

**Infrastructure — Web/SaaS** *(skip or substitute the project-type equivalent for non-web types)*
- [ ] SSL/TLS certificates are valid and auto-renewing.
- [ ] DNS records are prepared (TTL lowered to 60 s at least 48 hours before cutover).
- [ ] CDN is configured and cache-purge script is ready.

**External integrations**
- [ ] Third-party API keys are production keys (not sandbox/test keys).
- [ ] Webhooks point to production URLs.
- [ ] Email/SMS sending domain is verified and warmed.
- [ ] Payment provider is in live mode and webhooks are confirmed.

**Legal and compliance**
- [ ] Privacy policy and terms of service are live at their URLs.
- [ ] Cookie consent banner is implemented if required by jurisdiction.
- [ ] GDPR/CCPA data processing agreements are signed with all sub-processors.
- [ ] Accessibility statement is published if required.

**Communication**
- [ ] Status page is set up and linked from the app.
- [ ] Support channel is staffed for the launch window.
- [ ] Internal announcement drafted (team knows the launch time).
- [ ] External announcement / press release is staged (embargoed until cutover).

For each unchecked item note the owner and deadline. **STOP — present the incomplete checklist to the user and confirm they can complete all outstanding items before the launch date.**

### Step 2 — Write the launch plan
Produce a time-ordered runbook for the cutover window:

**T-48h**
- Lower DNS TTL to 60 s.
- Final staging smoke test with production-equivalent data volume.
- Brief on-call rotation; confirm all engineers have production access.

**T-2h**
- Freeze non-critical deploys.
- Take pre-launch production database snapshot; verify it is readable.
- Set status page to "scheduled maintenance" if applicable.

**T-0 Cutover sequence** (exact ordered steps):
1. Run database migrations: `<exact command>`.
2. Deploy new version: `<exact command or pipeline trigger>`.
3. Verify health check endpoint returns 200 with all dependencies healthy.
4. Run smoke test suite: `<exact command>`.
5. Flip DNS / load-balancer / feature flag to route live traffic.
6. Purge CDN cache: `<exact command>`.
7. Monitor error rate and p95 latency for 15 minutes before declaring success.

**T+15m**
- Confirm key business metrics are flowing (first orders/signups/events visible in dashboards).
- Remove "scheduled maintenance" from status page.
- Send internal "we're live" announcement.

**T+1h**
- Review logs for unexpected error patterns.
- Confirm autoscaling has not triggered unexpectedly.
- Send external announcement if embargoed.

**T+24h**
- Post-launch review meeting.
- Archive launch notes to `docs/reports/launch-<date>.md`.

### Step 3 — Write the rollback plan
Produce a step-by-step rollback procedure executable by any on-call engineer in under 10 minutes:

1. **Decision trigger:** who can call a rollback and under what conditions (error rate > X%, p95 > Y ms, data corruption detected).
2. **Traffic rollback:** revert DNS / load-balancer / feature flag to previous version. Exact command.
3. **Application rollback:** redeploy previous image/package. Exact command.
4. **Database rollback:** if migration was backwards-compatible, no action needed. If not, run down-migration: `<exact command>`. If no down-migration exists, restore from pre-launch snapshot: `<exact command>` — note this is destructive and loses writes since cutover.
5. **Verification:** run health check and smoke test on rolled-back version.
6. **Communication:** draft incident update for status page.

**STOP — present the launch plan and rollback plan to the user for review and explicit sign-off. Do not finalise until approved.**

### Step 4 — Dry-run the rollback (recommended)
If the user approves, execute the rollback procedure against the staging environment to confirm all commands are correct and record actual elapsed time.

### Step 5 — Package and store
Write the approved launch plan and rollback plan to `docs/reports/launch-plan-<date>.md`. This document is the single source of truth during the cutover window. Write the rollback steps to `docs/runbooks/rollback.md`.

### Step 6 — Report
Produce the Final report (see below).

## Agents used
- `.claude/agents/engineering/release-engineer.md` — tracks checklist item owners.
- `.claude/agents/quality/qa-engineer.md` — runs the automated smoke test suite against staging and production.

## Skills used
- `.claude/checklists/launch.md` — full itemised launch checklist.
- `.claude/templates/runbook.md` — rollback runbook template.
- `docs/runbooks/rollback.md` — existing rollback procedure (updated by this command).

## Expected outputs
| Output | Path |
|---|---|
| Launch plan + rollback plan | `docs/reports/launch-plan-<date>.md` |
| Updated rollback runbook | `docs/runbooks/rollback.md` |
| Completed launch checklist | `.claude/checklists/launch.md` (checked items) |

## Stop conditions
- Security audit has open P0 items → block entirely.
- Production readiness has any RED pillar → block entirely.
- Any audit report is older than 14 days → require re-audit before continuing.
- Launch date not provided and cannot be inferred → ask user.
- Database migration is not backwards-compatible AND no tested restore procedure exists → block (data safety risk).
- User does not explicitly approve the launch plan → do not finalise.

## Final report format
```
## Launch Preparation Complete — <date>

**Project:** <name>  |  **Target launch:** <date + time + timezone>
**Release:** <git tag>  |  **Strategy:** <big-bang | canary | feature-flag | regional>

### Gate checks
| Gate | Status |
|---|---|
| Security audit (no P0) | ✅ |
| Performance budgets met | ✅ |
| Production readiness (no RED) | ✅ |

### Launch checklist — outstanding items
| Item | Owner | Due |
|---|---|---|
| Production API keys confirmed | @alice | T-48h |
| DNS TTL lowered | @bob | T-48h |

### Launch plan
Saved to: `docs/reports/launch-plan-<date>.md`

### Rollback plan
Estimated rollback time (dry-run): <N> minutes
Saved to: `docs/runbooks/rollback.md`

### Status
✅ Launch plan approved by user — ready for go-live on <date>.

### Immediate next actions
1. Complete <N> outstanding checklist items above by their deadlines.
2. Brief on-call rotation on the rollback procedure.
3. Lower DNS TTL by T-48h.
```

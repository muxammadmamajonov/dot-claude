# Release & Rollback Checklist

Release and rollback gate: semantic versioning, changelog maintained, staged rollout or canary configured, feature flags operational, rollback procedure tested end-to-end, database migrations are reversible, and release approval process followed.

## P0 — Blockers (must pass before proceeding/launch)

- [ ] Release version follows Semantic Versioning 2.0 (MAJOR.MINOR.PATCH) or the project's documented versioning scheme; version is bumped in all version-bearing files (`package.json`, `pyproject.toml`, `build.gradle`, `Chart.yaml`, etc.) and committed before tagging.
- [ ] Git tag matching the release version exists on the exact commit being deployed; tag is signed (GPG or SSH) or created via a protected CI workflow to prevent tampering.
- [ ] `CHANGELOG.md` (or release notes) is updated for this release: lists all user-visible changes, breaking changes, deprecations, and security fixes under the correct version heading.
- [ ] All database migrations included in this release are reversible: a tested `down` migration (or equivalent rollback script) exists for every `up` migration, and reversal has been executed successfully in a non-production environment.
- [ ] Rollback procedure for this specific release has been rehearsed: the steps are documented (which command/script, expected duration, confirmation signal) and at least one engineer has run them in staging within the last 30 days.
- [ ] Feature flags are in place for all new user-facing functionality in this release; flags default to **off** in production and can be toggled without a deployment (via LaunchDarkly, Unleash, Flagsmith, or equivalent).
- [ ] CI/CD pipeline passes all required gates (build, unit tests, integration tests, SCA scan, SAST scan) on the exact artifact being promoted to production; no manual bypasses applied.
- [ ] Release approval has been obtained from the designated approver(s) (tech lead, release manager, or automated policy gate) per the release policy document; approval is recorded (PR approval, release ticket, or signed-off deployment record).
- [ ] No open SEV-1 or SEV-2 incidents are active at release time; deployment is gated by an automated check against the incident management system.

## P1 — Important (soon after launch)

- [ ] Staged rollout (canary or blue/green) is configured to initially expose the new release to ≤ 5–10% of production traffic; automatic rollback triggers (error rate spike, latency P99 breach, crash rate) are defined and tested.
- [ ] Observability dashboards and alerts are confirmed working for the new release: key metrics (error rate, latency, saturation) show data within 5 minutes of deployment and alert thresholds are unchanged or intentionally updated.
- [ ] Smoke tests (or synthetic monitors) run automatically against production within 10 minutes of deployment and a failure halts the rollout and triggers rollback.
- [ ] Release announcement (internal changelog, Slack `#releases`, or email) sent to stakeholders immediately after successful production deployment.
- [ ] Any third-party integrations or partner API changes introduced in this release are communicated to counterparts before or simultaneous to deployment; no silent breaking changes to published APIs.
- [ ] Deprecated APIs or features included in this release have a sunset date, migration guide, and have notified consumers at least one full release cycle in advance.
- [ ] Post-deployment health soak period (minimum 30 minutes for non-trivial changes) is observed before declaring the rollout complete and closing the release.
- [ ] Deployment record (who deployed, what version, when, from which CI run, to which environment) is stored in an append-only audit log.

## P2 — Hardening

- [ ] Release train or release cadence policy is documented (e.g., weekly releases, freeze windows, hotfix process) and communicated to all contributors.
- [ ] Automated release notes generation (from conventional commits, PR labels, or equivalent) is configured to reduce manual changelog authoring and omission risk.
- [ ] Immutable artifact policy enforced: once an artifact (container image, binary, package) is published to the production registry, it cannot be overwritten — only a new version tag creates a new artifact.
- [ ] Progressive rollout automation: traffic ramp schedule (5% → 25% → 50% → 100%) with configurable dwell time at each stage and automated metric evaluation before advancing is implemented in the CD platform (Argo Rollouts, Spinnaker, Flagger, etc.).
- [ ] Breaking-change detection is integrated into the CI pipeline for public APIs: OpenAPI diff, `buf breaking`, or equivalent tool blocks merges that introduce undocumented breaking changes to published interfaces.
- [ ] Hotfix process is documented and tested: branch-from-tag workflow, expedited review policy, how hotfix is backported to `main`/`trunk`, and minimum CI gates that still apply.

## P3 — Post-launch / backlog (track, revisit after launch; never blocks)

- [ ] Release readiness review meeting (brief async or synchronous checklist walk-through) is conducted for any release that touches more than N files or N services (define thresholds in release policy).
- [ ] Release metrics tracked and reported monthly: deployment frequency, lead time for changes, change failure rate, mean time to restore (MTTR) — DORA metrics dashboard in place.
- [ ] Dependency on manual release approval removed for low-risk changes through automated policy gates (SLSA provenance verification, required CI pass, automated diff review); human approval reserved for high-risk or breaking changes.

## How to use

**When:** Every production deployment must pass P0 before the deploy command is issued. P1 items must be confirmed within 30 minutes of a successful deployment. Run this checklist in full for major releases (MAJOR version bump) and selected items for patch releases (at a minimum, P0 items always apply).

**Who:** `release-engineer` agent (`.claude/agents/engineering/release-engineer.md`) is the process owner. `devops-engineer` (`.claude/agents/engineering/devops-engineer.md`) maintains the CI/CD pipeline configuration. `technical-lead` is the default release approver.

**Command:** `/prepare-launch` (`.claude/commands/prepare-launch.md`) requires this checklist to be green. `/refactor-safely` (`.claude/commands/refactor-safely.md`) references the rollback section for any structural change.

**Tools:** Semantic Release / `standard-version` / `release-please` for versioning; Argo Rollouts / Flagger / Spinnaker for progressive delivery; LaunchDarkly / Unleash / Flagsmith for feature flags; Flyway / Liquibase / Alembic / `golang-migrate` for migration management; GitHub Releases / GitLab Releases for artifact and changelog publishing.

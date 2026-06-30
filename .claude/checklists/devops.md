# DevOps Checklist

CI/CD, environments, secrets, IaC, and release-safety gate — passing this proves that no deployment can reach any shared environment through an unsafe, manual, or unaudited path. Severity tiers: P0=blocker, P1=important (fix shortly after launch), P2=hardening, P3=post-launch / backlog (track and revisit; never blocks shipping).

## P0 — Blockers (must pass before proceeding / launch)

- [ ] No secrets, credentials, API keys, tokens, or private keys are committed anywhere in the repository history (not just the current HEAD); `git log -p | grep -E 'password|secret|key|token'` returns no matches, and gitleaks / trufflehog scan is clean.
- [ ] All secrets are consumed at runtime from an external secrets manager (Vault, AWS Secrets Manager, GCP Secret Manager, Azure Key Vault, Doppler, 1Password Secrets Automation) or environment variables injected by the CI system — zero hard-coded values in source or in container image layers.
- [ ] A pre-commit hook that blocks secret-containing commits is active in the repo and enforced in CI so it cannot be bypassed locally (`detect-secrets`, `gitleaks`, or `trufflehog` with a baseline); the hook configuration is version-controlled.
- [ ] CI pipeline runs on every pull request and blocks merge if any of the following fail: build, lint, unit tests, integration tests, SAST scan (Semgrep, CodeQL, or Bandit), and dependency-vulnerability scan (Snyk, Dependabot, or `pip-audit`).
- [ ] Infrastructure is defined 100% as code (Terraform, Pulumi, CDK, Bicep, Helm, Ansible, or equivalent); no manual click-ops changes exist in any shared environment, confirmed by a drift-detection check.
- [ ] Separate, isolated configurations exist for at minimum `development`, `staging`, and `production`; production credentials, databases, and networks are unreachable from lower environments by IAM policy or network boundary — not only by convention.
- [ ] Deployment to production requires a passing CI pipeline AND either a protected-branch merge gate or an explicit manual approval step in the pipeline; direct pushes to the main/production branch are blocked.
- [ ] Container images (if used) are built from a pinned base image using a specific digest (`FROM image@sha256:...`) or a semantically versioned tag — `latest` is banned in any build definition targeting a shared environment.
- [ ] Rollback procedure is documented with exact commands or pipeline steps, an estimated execution time (target ≤ 15 min), a named owner, and evidence that it was rehearsed in staging at least once before go-live.
- [ ] Dependency versions are pinned via committed lock files (`package-lock.json`, `yarn.lock`, `poetry.lock`, `go.sum`, `Gemfile.lock`, `requirements.txt` with exact versions); unpinned wildcard versions cause the CI build to fail.
- [ ] Every environment variable required by the application is declared in a `.env.example` (name, type, description, example value, required/optional); the actual values file is listed in `.gitignore` and never committed.

## P1 — Important (fix before scaling / shortly after launch)

- [ ] IaC plans (`terraform plan`, `pulumi preview`, `cdk diff`, or equivalent) are generated and posted as a PR comment or artifact before any `apply` is permitted; the diff is reviewed and approved by a second engineer for production changes.
- [ ] Container images are scanned for known CVEs in CI (Trivy, Grype, Snyk Container, or equivalent); builds fail automatically on CRITICAL or HIGH severity findings unless an explicit suppression with justification exists.
- [ ] Least-privilege IAM roles or service accounts are assigned to every workload; no service account has `admin`, `owner`, or a wildcard `*:*` permission; IAM policy is version-controlled and peer-reviewed.
- [ ] CI/CD runners or agents execute in ephemeral, isolated environments; build artifacts are stored in a content-addressed registry; the artifact cache is keyed to a dependency hash and validated before use.
- [ ] Staging environment mirrors production topology (same instance types, same managed services, same networking model); all smoke tests and load tests execute in staging before every production deploy.
- [ ] Deployment notifications (success/failure, commit SHA, author, diff link, duration) are sent automatically to the team's incident channel (Slack, Teams, PagerDuty, or equivalent) on every production deploy.
- [ ] Automated dependency-update PRs are active (Dependabot, Renovate) with auto-merge enabled for patch-level security fixes after CI passes, and human review required for minor/major version bumps.
- [ ] Build and deployment durations are tracked; any build that exceeds a defined threshold (e.g., 15 min for a standard CI run) triggers an alert or a required pipeline optimization investigation.

## P2 — Hardening / nice-to-have

- [ ] Software Bill of Materials (SBOM) is generated per release using Syft or CycloneDX in both SPDX and CycloneDX JSON format and stored as a release artifact alongside the binary or image digest.
- [ ] IaC state files are stored in a remote, encrypted backend with state locking and versioning (Terraform S3 + DynamoDB lock, Terraform Cloud, Pulumi backend, or equivalent); local state files do not exist in CI.
- [ ] Container image signing (Sigstore / cosign) and commit signing (GPG or SSH keys via `git config commit.gpgsign true`) are enforced to verify build provenance and prevent tampering.
- [ ] Supply-chain attestation at SLSA Level 2 or higher is configured: build provenance is generated by the build platform (GitHub Actions, GitLab CI, Google Cloud Build) and stored alongside artifacts.
- [ ] Scheduled drift detection runs at least daily; an alert fires if live infrastructure diverges from IaC state by more than a defined threshold, and a ticket is automatically created.
- [ ] Feature flags (LaunchDarkly, Flipt, Unleash, or equivalent) or canary/blue-green deployments decouple code deploy from feature activation, enabling rollback without a code revert.
- [ ] Multi-region or multi-AZ deployment is tested and documented; a failover runbook has been executed in a non-production environment, with recovery time measured against the RTO.

## P3 — Post-launch / backlog (track and revisit after launch; never blocks shipping)

- [ ] Pipeline observability is instrumented end-to-end: each CI job emits structured timing and failure-reason telemetry to a dashboard so build-health trends (failure rate, queue time, duration per job) are visible over rolling 30-day windows.
- [ ] SLSA Level 3 provenance is pursued: builds run in an isolated, hermetic environment; provenance is generated by the build platform and cryptographically signed; consumers can verify the artifact before deployment.
- [ ] Dependency update PRs are triaged and merged on a defined SLA: patch-level security fixes within 24 hours, non-security patch within 1 week, minor within 1 sprint; the SLA is tracked in the team's metrics dashboard.
- [ ] Multi-cloud or multi-region IaC is evaluated: cost, complexity, and vendor-lock-in trade-offs are documented in a decision record; if adopted, a failover drill is executed quarterly with measured RTO.
- [ ] Golden-path developer tooling (dev-container, Makefile, or task runner) is provided so any engineer can reproduce the exact build and test environment locally with a single command, eliminating "works on my machine" drift.

## How to use

Invoke the `devops` skill (`.claude/skills/devops/SKILL.md`) or run `.claude/commands/audit-production.md` to audit CI/CD configuration against this checklist. This gate is mandatory before the first staging deploy and must be re-run before every production release and after any infrastructure change. The responsible agent is `.claude/agents/engineering/devops-engineer.md`, assisted by `.claude/agents/engineering/cloud-architect.md`. Cross-reference `.claude/checklists/security.md` for SAST/DAST controls, `.claude/checklists/production.md` for observability wiring, and `.claude/checklists/launch.md` for the final go-live gate. Mark each item `[x]` when verified or `[-]` when formally waived with a written justification.

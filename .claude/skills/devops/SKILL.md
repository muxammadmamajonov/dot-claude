---
name: devops
description: Use when setting up CI/CD pipelines, defining environments, managing secrets, or writing infrastructure-as-code. Triggers when a project needs automated build/test/deploy, when adding an environment (staging/prod), when secrets must be handled safely, or when infrastructure should be reproducible. Safety-first — guards against destructive and irreversible operations.
---

# DevOps: CI/CD, Environments, Secrets, IaC

## When to use
- Standing up or improving a CI/CD pipeline for build, test, and deploy.
- Defining or hardening environments (local, CI, staging, production).
- Introducing secret management, or fixing leaked or hardcoded secrets.
- Codifying infrastructure so it is reproducible, reviewable, and reversible.
- Preparing a deployment procedure, rollback plan, or production runbook.

Applies to any deployable artifact: web/mobile/desktop apps, APIs, CLIs, services, jobs, agents, functions, containers, and embedded firmware pipelines. The principles are the same; only the tooling differs.

---

## Workflow

### Phase 1 — Map the Delivery Path

**1. Identify the artifact(s) and environments.**
List every deployable artifact (binary, container image, serverless function, static bundle, firmware image, etc.) and the environments it flows through. A typical path: `local → CI → staging → production`. Some projects add `preview` (per-PR ephemeral), `canary`, or `regional` stages. Document this path in `docs/deployment-plan.md` using `.claude/templates/deployment-plan.md` before writing any pipeline code.

**2. Define the promotion model.**
Decide: does the same built artifact get promoted through environments, or does each environment get rebuilt from source? The answer must be "same artifact, promoted." Rebuilding per environment means the artifact that reaches production was never what was tested. Record this as a constraint in `docs/decisions/`.

**3. Identify the gates between environments.**
For each promotion step, list the required gates: tests pass, security scan clean, peer review approved, manual approval, performance baseline met, compliance sign-off, etc. Gates are non-optional; skipping one requires an explicit recorded decision (`.claude/templates/decision-record.md`).

---

### Phase 2 — CI Pipeline (Build and Verify Gate)

**4. Structure the CI pipeline.**
Every push to a PR branch triggers the full CI pipeline. Order for fail-fast efficiency:

```
install (pinned deps)
→ lint + format check
→ type check / static analysis
→ unit tests (fast)
→ security / dependency vulnerability scan
→ build artifact
→ integration tests (slower; may parallelize)
→ generate / validate docs (OpenAPI spec, changelog)
→ publish artifact to registry (tagged, immutable)
```

The pipeline is a required merge gate. A red pipeline blocks merge — no exceptions without a recorded risk decision.

**5. Pin all tool and dependency versions.**
- Use a lock file (`package-lock.json`, `Cargo.lock`, `poetry.lock`, `go.sum`). Commit it. Never `.gitignore` it.
- Pin CI runner images and tool versions (Node 22.x, not `latest`).
- Use a dependency update bot (Dependabot, Renovate) to keep pins current automatically with PR review, rather than falling behind.

**6. Cache dependencies for speed.**
Slow CI is bypassed CI. Cache the dependency install layer keyed on the lock file hash. A cache miss triggers a full reinstall; a hit restores in seconds. Target: lint+types+unit tests under 5 minutes for most projects.

**7. Run security and dependency scans.**
In every CI run:
- **Dependency vulnerability scan**: `npm audit`, `cargo audit`, `trivy`, `snyk`, or equivalent. Fail on CRITICAL/HIGH by default.
- **Secret scanning**: `truffleHog`, `gitleaks`, or a platform-native equivalent. Block any commit that introduces a secret pattern, even in tests.
- **Container image scanning** (if building images): scan with `trivy` or `grype` before pushing to the registry.
- **SAST** (static application security testing): integrate a lightweight SAST tool appropriate to the language. Findings land as PR annotations, not blocking comments for warnings — block only on P0/P1 categories.

Cross-reference `.claude/skills/security/SKILL.md` for the full security checklist.

**8. Build a single, tagged, immutable artifact.**
On every CI run, build the artifact once and tag it with the commit SHA. Push to an artifact registry (container registry, package registry, S3 bucket). This tag travels with the artifact through all environments. Never rebuild from source for staging or production.

---

### Phase 3 — CD Pipeline (Deploy and Promote)

**9. Automate deployment to staging.**
On merge to the main branch: deploy the tagged artifact to staging automatically. The staging deploy must:
- Run database migrations (backward-compatible, see step 14).
- Execute smoke tests against the live staging environment.
- Emit a deploy event to the observability system.

If staging smoke tests fail, the pipeline stops. Production is not touched. The team fixes staging before promoting.

**10. Gate production with human approval for high-impact systems.**
For any system with real users, financial transactions, health data, or other high-impact state: require explicit human approval before promoting from staging to production. Implement this as a pipeline approval gate, not a convention. For internal tooling or low-risk systems with good rollback, auto-deploy to production on green staging is acceptable if documented.

**11. Use a safe rollout strategy.**
Never deploy simultaneously to all instances. Choose the strategy appropriate to the system:

| Strategy | Use when | Rollback |
|---|---|---|
| **Rolling update** | Stateless services; gradual instance replacement | Scale down new, up old |
| **Blue-green** | Zero-downtime; full parallel environment | Switch load balancer to blue |
| **Canary** | High-risk changes; gradual traffic shift (1% → 10% → 100%) | Shift traffic back to stable |
| **Feature flag** | Decouple deploy from release; control by user segment | Toggle flag off; no redeploy needed |
| **In-place** | Only for non-production or single-instance non-critical systems | Redeploy previous image |

**12. Keep a tested, fast rollback path.**
Before every production deploy, verify the rollback is ready:
- For containers: re-deploy the previous tagged image.
- For serverless: alias/version rollback.
- For static sites: CDN cache invalidation + previous artifact re-publish.
- For database migrations: the `down` migration is written, tested, and ready to run.
- For feature flags: the flag is off by default; production traffic flows through the old path.

A rollback that takes more than 15 minutes is not a rollback — it is a second incident. Design and test for speed.

---

### Phase 4 — Environment Parity and Configuration

**13. Maintain environment parity.**
Local, CI, staging, and production should differ as little as possible. Differences are explicitly documented and justified. Common acceptable differences:
- External service credentials (use a vault for all; different values per env).
- Scale (production has more replicas; staging has one).
- Logging verbosity (debug in staging, warn in production).

Unacceptable differences:
- Different language runtime versions.
- Different database engines (SQLite in dev, Postgres in prod is a common failure source).
- Skipping TLS or auth in staging.
- Hand-configured staging that was never captured in IaC.

Use Docker Compose or a local orchestration tool so every developer runs the exact same stack locally that CI and staging run.

**14. Handle database migrations safely.**
Every migration must be:
- **Backward-compatible**: the running application handles both the old and new schema simultaneously during the deploy window. This is what allows zero-downtime deploys.
- **Reversible**: the `down` migration is tested before the `up` is applied to production.
- **Expand/contract for destructive changes** (see `.claude/skills/data-modeling/SKILL.md` Phase 6): add new → backfill → switch → remove old across multiple safe deploys.
- **Never modified once applied**: migrations are append-only. Editing a migration that has already run in any environment is forbidden.

Run migrations as a pre-deploy step, not post-deploy, so the database is ready before the new application version starts.

---

### Phase 5 — Secret Management

**15. Store secrets in a vault or platform secret store.**
Acceptable stores: HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager, Azure Key Vault, platform-native secret stores (GitHub Actions secrets, Doppler, 1Password Secrets Automation). Unacceptable stores: `.env` files in VCS, plaintext in pipeline config, hard-coded in source, Docker image layers, log output.

**16. Inject secrets at runtime via environment variables.**
Applications read secrets from environment variables injected at deploy time, never from files bundled into the image. The image itself contains no secrets and is safe to store in any registry.

**17. Scope and rotate secrets.**
- One credential per environment. Production, staging, and CI each have their own credentials.
- One credential per service. The deploy pipeline credential cannot read the database; the application credential cannot deploy infrastructure.
- Rotate automatically where possible (short-lived tokens via OIDC / workload identity are preferred over long-lived static keys).
- On any suspected or confirmed credential exposure: revoke immediately, rotate, audit the access logs, and record the incident. This is a non-deferrable P0 action.

**18. Prevent secret leakage at the source.**
- Add `.env*`, `*.pem`, `*.key`, `id_rsa`, `credentials.json` to `.gitignore` globally and per-repo.
- Run secret scanning in CI (step 7) to catch any accidental commit.
- Never echo, log, or print secret values — even in debug output.
- Mask secrets in CI pipeline logs (platform-native feature; verify it is active).

---

### Phase 6 — Infrastructure as Code (IaC)

**19. Express all infrastructure as version-controlled code.**
Compute, networking, databases, queues, DNS, load balancers, IAM roles, and monitoring rules — all defined in IaC. Never provision infrastructure by clicking in a console and not recording it. "Click-ops" creates undocumented, unreproducible, ungoverned infrastructure.

Acceptable IaC tools by context:
- **Terraform / OpenTofu**: cloud-agnostic; strong ecosystem; use for multi-cloud or complex infra.
- **AWS CDK / CloudFormation**: AWS-native; type-safe with CDK; good for AWS-centric stacks.
- **Pulumi**: general-purpose, full-programming-language IaC; good when logic complexity is high.
- **Kubernetes manifests / Helm**: for workload configuration on K8s.
- **Ansible**: for configuration management on existing machines; not ideal for cloud resource provisioning.
- **Docker Compose**: acceptable for local development and small single-host deployments; not for production multi-service infra.

**20. Review IaC changes via PR with plan/diff.**
Every IaC change goes through a PR. Before the PR can merge, run `terraform plan` (or equivalent) and attach the output as a PR artifact. The diff must be reviewed by a human. A plan that shows resource destruction or replacement (`-/+`) requires explicit human approval before apply — not just PR approval, but an acknowledged "I understand this will replace the database."

**21. Secure and lock IaC state.**
- Remote state backend (Terraform Cloud, S3 + DynamoDB, GCS, etc.) — never local state files in VCS.
- State locking enabled to prevent concurrent applies.
- State files contain sensitive data; restrict access to the state bucket/project.
- Back up state before any large apply.

**22. Scope CI/CD IAM permissions to the minimum required.**
The pipeline credential should be able to deploy the application — nothing else. It should not be able to delete infrastructure, modify IAM, access other accounts, or read secrets beyond what the deploy needs. Use OIDC / workload identity federation (GitHub Actions OIDC, GCP Workload Identity) to eliminate long-lived static keys in CI entirely.

---

### Phase 7 — Observability and Deploy Safety

**23. Emit deploy markers.**
Every deploy to every environment emits an event to the observability system: what was deployed (version, commit SHA), when, by whom, and to which environment. This makes it possible to correlate a change in metrics with the deploy that caused it.

**24. Watch error rate and latency immediately post-deploy.**
Configure alerts that fire within 5 minutes of a deploy if:
- Error rate increases above baseline by more than a configured threshold.
- p99 latency increases beyond a threshold.
- Health check endpoints return non-200.

Automate rollback on health check failure where the rollback is safe and fast (stateless services with no migration). For stateful or complex deploys, alert immediately and require human-initiated rollback.

**25. Document the deployment procedure as a runbook.**
Every production deployment procedure must exist as a runbook at `docs/runbooks/deploy.md` using `.claude/templates/runbook.md`. It must include: prerequisites, step-by-step commands with expected output, verification steps, rollback procedure, and escalation contacts. Follow `.claude/skills/documentation/SKILL.md` for runbook standards. Test the runbook by running it.

**26. Record significant IaC and pipeline decisions as ADRs.**
Choices of IaC tooling, deployment strategy, secret management approach, and environment topology are decisions that future engineers need context for. Record them at `docs/decisions/` using `.claude/templates/decision-record.md`.

---

## Standards

- **Do** pin dependency and tool versions; build once and promote the same immutable tagged artifact through all environments.
- **Do** make CI the merge gate: no merge without green lint, types, tests, security scan, and build.
- **Do** keep all pipeline and IaC as code in the repo, reviewed like any other change.
- **Do** store every secret in a managed vault; inject via environment at runtime; scope minimally; rotate on exposure.
- **Do** make database migrations backward-compatible, reversible, and append-only.
- **Do** require explicit human approval for production deploys and IaC applies with a broad blast radius.
- **Do** maintain a tested, fast rollback path and emit a deploy marker to observability on every deploy.
- **Do** use workload identity / OIDC instead of long-lived static CI credentials wherever the platform supports it.
- **Do not** commit `.env` files, keys, tokens, certificates, or credentials; never echo secrets in logs or build output.
- **Do not** run `rm -rf`, `terraform destroy`, `DROP DATABASE`, force-push to shared branches, delete migrations or backups, or take any destructive production action without explicit human approval.
- **Do not** SSH into production and hand-edit anything ("snowflake" servers); all production changes go through IaC and CI/CD.
- **Do not** give CI/CD broader cloud permissions than the deploy requires; scope credentials per environment and per action.
- **Do not** rebuild the artifact per environment; what reaches production must be what was tested in staging.

## Common mistakes to avoid

- **Hardcoded or committed secrets** — one credential reused across all environments, committed in `.env` or config files. The blast radius of a breach becomes total.
- **Rebuild-per-environment** — the container image or bundle deployed to production was never the one tested in staging. Silent configuration drift causes mysterious production-only failures.
- **No rollback plan** — a bad deploy that can only be fixed forward, under pressure, with a production incident open.
- **Irreversible migrations on deploy** — a destructive schema change applied with no plan, no diff, and no rollback, blocking safe recovery.
- **Manual undocumented deploys** — "I just SSHed in and restarted it." No record, no reproducibility, no rollback.
- **Flaky or slow CI** — when CI takes 30 minutes or fails randomly 20% of the time, developers bypass it. A bypassed gate is no gate.
- **Over-privileged CI tokens** — a single long-lived key with admin permissions turns a pipeline compromise into a full cloud compromise. Use OIDC and scope permissions tightly.
- **IaC state in VCS or local files** — state files contain sensitive resource IDs and sometimes secret values; they must be in a secured remote backend.
- **Missing deploy observability** — deploying without emitting markers or watching post-deploy metrics means you discover problems from user reports, not from your own systems.
- **"It works in staging"** — when staging differs from production (different DB, different scale, different TLS, different secrets injection) it is a different system. Parity is not optional.

## Output format

All DevOps artifacts are code or documentation committed to the repository:

| Artifact | Path | Notes |
|---|---|---|
| CI pipeline config | `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, etc. | Reviewed as code; required gate on PRs |
| IaC modules | `infra/` or `terraform/` at project root | With `plan` output as PR artifact |
| Deploy runbook | `docs/runbooks/deploy.md` | Uses `.claude/templates/runbook.md`; tested |
| Rollback runbook | `docs/runbooks/rollback.md` | Uses `.claude/templates/runbook.md`; tested |
| Deployment plan | `docs/deployment-plan.md` | Uses `.claude/templates/deployment-plan.md` |
| IaC/pipeline ADRs | `docs/decisions/ADR-NNN-*.md` | Uses `.claude/templates/decision-record.md` |
| Secret management doc | `docs/secrets.md` | Which vault, rotation policy, per-env scope |

Significant decisions (IaC tool choice, deploy strategy, secret management approach) are also recorded as ADRs per `.claude/skills/documentation/SKILL.md`.

## Related checklists
- `.claude/checklists/production.md`
- `.claude/checklists/security.md`
- `.claude/checklists/devops.md`
- `.claude/checklists/qa.md`

## Related agents
- `.claude/agents/engineering/devops-engineer.md`
- `.claude/agents/engineering/cloud-architect.md`
- `.claude/agents/engineering/infrastructure-engineer.md`
- `.claude/agents/engineering/release-engineer.md`
- `.claude/agents/quality/security-auditor.md`
- `.claude/agents/quality/reliability-engineer.md`
- `.claude/agents/core/orchestrator.md`

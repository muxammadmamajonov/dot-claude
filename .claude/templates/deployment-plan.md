# Deployment Plan
**What:** Step-by-step plan for releasing software to production.  
**Who fills it in:** Lead engineer + DevOps/platform owner, once per release (or once per environment tier setup).  
**Cross-references:** `.claude/checklists/security.md`, `.claude/templates/production-readiness.md`, `.claude/templates/launch-checklist.md`

---

## 1. Release Overview

> What version or feature set is being deployed? What is the business reason for this release?

- **Release tag / version:** `<v2.4.0>`
- **Release type:** `<feature | hotfix | infra | data-migration>`
- **Target date:** `<YYYY-MM-DD HH:MM UTC>`
- **Release owner:** `<@engineer-name>`
- **Stakeholder sign-off required from:** `<Product, CTO, Security>`

---

## 2. Environments

> List every environment in promotion order. Note what "done" means before promoting to the next.

| # | Environment | Host / URL | Promotion gate |
|---|-------------|-----------|----------------|
| 1 | Local dev | `localhost` | Unit + integration tests pass |
| 2 | CI / PR | `<ci.example.com>` | All checks green, PR approved |
| 3 | Staging | `<staging.example.com>` | Smoke tests pass, QA sign-off |
| 4 | Canary (optional) | `<5 % of prod traffic>` | Error rate ≤ baseline for 30 min |
| 5 | Production | `<app.example.com>` | Go/no-go call completed |

For **mobile / desktop / embedded** projects replace URL columns with store/distribution channel (TestFlight, Play Store internal track, OTA update channel, etc.).

---

## 3. Pipeline & Automation

> Describe the CI/CD pipeline steps in order. Note which steps are fully automated vs. require a human trigger.

```
[push tag] → CI lint/test → build artifact → push to registry
→ deploy to staging (auto) → smoke tests (auto)
→ deploy to canary (manual trigger) → monitor 30 min
→ deploy to production (manual approval) → health checks
```

- **CI platform:** `<GitHub Actions | GitLab CI | CircleCI | Buildkite | Jenkins>`
- **Artifact store:** `<ECR | GCR | Artifactory | npm registry | App Store Connect>`
- **Deployment tool:** `<Helm | Terraform | Ansible | Capistrano | AWS CDK | custom script>`
- **Pipeline config file(s):** `<.github/workflows/deploy.yml>`

---

## 4. Secrets & Configuration

> List every secret or env var this release adds, changes, or removes. Never paste actual values here.

| Variable | Environment(s) | Source | Changed this release? |
|----------|---------------|--------|-----------------------|
| `DATABASE_URL` | All | `<AWS Secrets Manager / Vault / .env>` | No |
| `STRIPE_SECRET_KEY` | Staging, Prod | `<Vault path: secret/stripe>` | Yes — new key |
| `FEATURE_FLAG_X` | Prod | `<LaunchDarkly / env file>` | Added |

- **Secret rotation needed:** `<Yes / No>` — if yes, document rotation steps separately.
- **Config diff from previous release:** `<link to PR or diff>`
- No secrets are committed to source control. See `.claude/checklists/security.md`.

---

## 5. Pre-Deployment Steps

> Tasks that must be completed before the deployment window opens. Assign an owner and deadline.

| Step | Owner | Deadline | Done? |
|------|-------|----------|-------|
| Freeze feature flags | `<@engineer>` | T−2 h | ☐ |
| Back up database | `<@devops>` | T−1 h | ☐ |
| Notify on-call team | `<@sre>` | T−30 min | ☐ |
| Disable auto-scaling rules that conflict | `<@devops>` | T−15 min | ☐ |
| `<Project-specific step>` | | | ☐ |

---

## 6. Deployment Steps

> Ordered, numbered steps to execute during the deployment window. Each step must be atomic and verifiable.

1. **Merge release branch** to `main` and tag `<v2.4.0>`.
2. **Trigger pipeline** manually (or confirm it auto-triggered from tag).
3. **Validate staging deploy** — run smoke-test suite: `<npm run smoke:staging>`.
4. **Run database migrations** (if any): `<rails db:migrate RAILS_ENV=production>`. Expected duration: `<2 min>`. Risk: `<additive / backward-compatible>`.
5. **Promote to canary** — set traffic split to 5 % via `<load balancer / feature flag>`.
6. **Monitor canary** for `<30>` minutes: error rate, p95 latency, business KPIs.
7. **Promote to full production** after approval from `<@release-owner>`.
8. **Post-deploy validation** — run production smoke tests: `<link to runbook>`.
9. **Enable feature flags** for new functionality: `<list flags>`.

---

## 7. Database & Data Migrations

> Only fill if this release includes schema or data changes.

- **Migration file(s):** `<db/migrate/20260625_add_index_users.rb>`
- **Estimated run time:** `<3 min on prod dataset size>`
- **Backward compatible with current code?** `<Yes / No>`
- **Can migration be run before code deploy?** `<Yes — expand-contract pattern used>`
- **Rollback migration command:** `<rails db:rollback STEP=1>`
- **Data loss risk:** `<None | Low | High>` — justification: `<only adds nullable column>`

---

## 8. Rollback Plan

> Describe exactly how to undo this deployment within the required RTO. Be specific — no vague steps.

- **Rollback decision owner:** `<@sre-lead>`
- **Rollback trigger criteria:** Error rate > `<1 %>` for `<5>` min, or P95 latency > `<500 ms>`, or any data corruption.
- **Rollback RTO target:** `<15 minutes>`

**Rollback steps:**
1. Revert traffic to previous version: `<kubectl rollout undo deployment/app>` or `<roll back Helm release>`.
2. Revert database migration if not backward-compatible: `<rails db:rollback STEP=1>`.
3. Disable any newly-enabled feature flags.
4. Re-enable previous environment config if changed.
5. Confirm health checks pass on reverted version.
6. Post incident to `<#incidents Slack channel>` with timeline.

- **Previous stable artifact tag:** `<v2.3.1>`
- **Destructive actions (rm, DROP TABLE, etc.) forbidden** without explicit approval — see `.claude/agents/core/orchestrator.md`.

---

## 9. Observability & Health Checks

> How will the team know the deployment succeeded? List specific signals with threshold values.

| Signal | Tool | Healthy threshold | Alert channel |
|--------|------|------------------|---------------|
| Error rate | `<Datadog / Sentry>` | < `<0.5 %>`  | `<#alerts>` |
| P95 response time | `<Datadog / CloudWatch>` | < `<300 ms>` | `<#alerts>` |
| Deployment success metric | `<CI dashboard>` | All steps green | `<#deploys>` |
| Business KPI | `<Mixpanel / custom>` | `<orders/min ≥ baseline>` | `<#eng-oncall>` |

- **Monitoring window post-deploy:** `<24 hours>`
- **On-call engineer during deploy:** `<@name>`

---

## 10. Communication Plan

> Who needs to know what, and when?

| Audience | Channel | What to say | When |
|----------|---------|-------------|------|
| Internal engineering | `<#deploys Slack>` | Deploy start notice | T−5 min |
| Customer success / support | `<email / Slack>` | Maintenance window notice | T−24 h |
| End users (if downtime) | `<status page>` | Scheduled maintenance | T−48 h |
| Stakeholders | `<email>` | Release notes | T+1 h after success |

---

## 11. Post-Deployment Sign-Off

> Complete after the deployment window closes.

| Item | Status | Notes |
|------|--------|-------|
| All health checks passing | ☐ | |
| Smoke tests passed in production | ☐ | |
| No elevated error rate | ☐ | |
| Rollback plan no longer needed | ☐ | |
| Release notes published | ☐ | |
| Retrospective scheduled (if incident) | ☐ | |

**Final sign-off:** `<@release-owner>` on `<YYYY-MM-DD HH:MM UTC>`

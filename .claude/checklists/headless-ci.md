# Headless / CI Safety Checklist

Gate for running the OS **non-interactively** — in CI, cron, a webhook handler, or any background process where no human is present to approve a prompt. The defining risk: every safety mechanism in CLAUDE.md §8 that relies on "stop and ask the user" has no user to ask. This checklist makes the headless runner **fail closed**: read-only by default, no forbidden action without a human approver, writes restricted to non-prod, secrets redacted, and a deterministic non-zero exit on any gate failure. See `.claude/docs/HEADLESS_AND_ROUTINES.md` and `.claude/skills/headless-automation/SKILL.md`; emit results via `.claude/templates/headless-audit-report.md`.

## P0 — Blockers (must pass before any non-interactive run is permitted)

- [ ] The run is **read/review-only by default**: it may inspect, analyze, lint, test, and report, but performs no write or mutation unless write mode is explicitly enabled in the run config (`--allow-write` / equivalent flag), never on by default.
- [ ] The **forbidden-action set (CLAUDE.md §8)** — `rm -rf`/bulk deletion, force-push/history rewrite, DB drop/destructive migration, secret exposure, irreversible production actions, untrusted-code execution — **hard-fails closed** when no human approver is available; the runner aborts rather than auto-approving.
- [ ] **Write scope is restricted to non-production** targets only; production credentials, prod databases, prod deploy targets, and real-user-facing channels are not reachable from the headless context.
- [ ] **Secrets are redacted from all CI logs and artifacts**: tokens, keys, `.env` contents, and credentials never appear in build output, the audit report, or transcripts; the job uses masked CI secret variables, not inlined values.
- [ ] Any gate failure (security, QA, performance, accessibility, or a refused forbidden action) produces a **deterministic non-zero exit code**; the job never exits `0` on a red gate, so the pipeline blocks rather than silently passing.
- [ ] The run operates on a **pinned, known revision** (specific commit SHA) recorded in the report — not a moving branch tip resolved at unknown time.
- [ ] No interactive approval prompt can **block indefinitely**: where a human decision would be required, the runner records the blocked action and exits non-zero instead of hanging or defaulting to "yes".

## P1 — Important (soon after enabling headless runs)

- [ ] A **maximum runtime and cost budget** is enforced (wall-clock timeout + token/spend ceiling); exceeding either terminates the run cleanly and reports the overage, rather than running unbounded.
- [ ] Any **opted-in mutation is preceded by a mandatory dry-run** whose diff/plan is captured in the report; the actual write proceeds only if the dry-run is clean and within scope.
- [ ] Every run emits a structured artifact via `.claude/templates/headless-audit-report.md` — trigger, revision, scope, per-gate results, findings, actions taken, budget consumed, and exit status — stored as a CI artifact.
- [ ] The runner uses a **least-privilege identity**: a scoped CI token/service account with only the permissions the job needs, not a personal or admin credential.
- [ ] Concurrency/idempotency is handled: two overlapping runs on the same target cannot corrupt state (locking or single-flight); a re-run of the same job is safe.
- [ ] Failure of the run itself (crash, timeout, infra error) is distinguishable in the exit code and report from a clean run that found blocking issues.

## P2 — Hardening

- [ ] An **egress allowlist** constrains outbound network access to approved hosts (package registries, the project's own services); unexpected destinations are blocked and logged.
- [ ] Build/run **provenance** is captured: runner image digest, OS toolchain versions, and config hash, so a run is reproducible and tamper-evident.
- [ ] The audit report is **signed or checksummed** so its integrity can be verified after the fact.
- [ ] Write-mode runs are limited to a dedicated branch / ephemeral environment, never directly to `main`/`trunk` or a shared protected branch.

## P3 — Post-launch / backlog (track, revisit; never blocks)

- [ ] Audit reports are aggregated to a dashboard for trend review (gate pass rates, recurring findings, budget drift over time).
- [ ] Periodic review of the headless runner's scoped credential confirms it is still least-privilege and rotates it on schedule.
- [ ] A "break-glass" procedure for an emergency opted-in production action is documented, requiring a named human approver and a recorded decision (`.claude/templates/decision-record.md`).

## How to use

**When:** Apply before wiring the OS into any CI pipeline, cron job, or background trigger, and re-check whenever the job gains write permissions or a new target. The P0 block is the precondition for the runner to be allowed to act at all.

**Who:** `devops-engineer` (`.claude/agents/engineering/devops-engineer.md`) owns the CI wiring and credential scoping; `security-auditor` verifies redaction, fail-closed behavior, and forbidden-action handling; `reliability-engineer` reviews budgets and idempotency; `technical-lead` approves any P0 exception via `.claude/templates/decision-record.md`.

**Command:** `/audit-production` (`.claude/commands/audit-production.md`) covers this gate for automation. P0 items block the headless run from being enabled or from acting; P1 items are tracked issues; P2–P3 are backlog.

**Tools:** CI platform secret masking, scoped service-account tokens, wall-clock timeouts and token/spend budgets, dry-run/plan modes, egress allowlists, and the run record from `.claude/templates/headless-audit-report.md`.

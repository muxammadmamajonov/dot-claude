# Headless & Routines — unattended automation, read-first and safe

This document covers two related capabilities: running the OS **headless** (non-interactive, in CI)
and running it on a **schedule** (routines). Both remove the human who normally answers the §6 "ask
the user" and §8 "stop and ask" gates — so both are **read/review-only by default**, and any write or
destructive action requires explicit opt-in configuration with a tested rollback.

- Headless gate: `.claude/checklists/headless-ci.md` · skill: `.claude/skills/headless-automation/SKILL.md` · command: `.claude/commands/headless-run.md`
- Routine gate: `.claude/checklists/routine-safety.md` · skill: `.claude/skills/routine-authoring/SKILL.md` · command: `.claude/commands/manage-routines.md` · template: `.claude/templates/routine-template.md`

## Part 1 — Headless mode (CI / non-interactive)

### What runs headless
Read/review work, which is the OS's safe surface when no human is present:
- Audits: `/audit-security`, `/audit-performance`, `/audit-production`
- Readiness: production-readiness checks, `/plan-scale`, `/threat-model`
- Review: PR/diff review, `/review-feature`
- Hygiene: `/self-test`, docs-sync checks, dependency review, test-plan verification
- Planning artifacts: `/create-github-issues` in **dry-run** (writes the plan, does not create issues)

### The headless contract
1. **Read/review-only by default.** No writes to the repo, no mutations to external systems, unless a human
   has explicitly opted in via config — and even then, restricted to non-prod with a rollback.
2. **STOP-gates become records, not prompts.** A business-critical question that would `STOP` interactively is
   instead resolved from a documented default and **recorded as an assumption/decision** (CLAUDE.md §6–§7). If
   no safe default exists, the run **fails closed** rather than guessing.
3. **Fail closed on any §8 violation.** A forbidden action in a headless context aborts the run with a non-zero
   exit — it is never auto-approved because "no one said no."
4. **Deterministic exit codes.** Gate pass → 0; gate fail → non-zero. CI consumes this.
5. **No secret leakage in logs.** Redact tokens/`.env`; never print secrets to CI output.
6. **MCP may be absent.** Interactively-authenticated servers may not exist in CI; check, and skip-with-note or
   fail closed rather than proceeding blind.
7. **Emit a report.** Every headless run produces `.claude/templates/headless-audit-report.md` output to
   `docs/reports/` so the run is reviewable after the fact (§7 paper trail).

`/headless-run` wraps any chosen command with this contract. Verify the setup against
`.claude/checklists/headless-ci.md`.

### Typical CI usage (illustrative)
A CI job invokes Claude Code in non-interactive mode pointed at `/headless-run /audit-security`, captures the
exit code (failing the build on a red P0 gate), and uploads the `docs/reports/` artifact. The exact CLI/flag
and platform (GitHub Actions, GitLab CI, Jenkins) are project-specific — keep them in the project's CI config,
not in this portable doc.

## Part 2 — Routines (scheduled automation)

A routine is a **scheduled headless run** with extra guardrails because it fires while no one is watching.

### Safe-by-default routine principles
- **Report-first.** A routine produces a report and **recommendations**; it does not change the system. Any
  change requires a human to review the report and approve.
- **No unsupervised destructive or production actions — ever.** No production changes on a schedule while the
  user is away. The default action is "observe and report," never "fix and deploy."
- **Owner + kill-switch + idempotency + failure alert.** Every routine names an owner, has a documented
  kill-switch, is idempotent (a missed/duplicated run causes no harm), and alerts a human on silent failure.
- **Non-prod by default; least-privilege runner.** Routines run against non-prod with the narrowest credentials.
- **Change-detection before action.** A routine that *is* opted-in to act (rare) must detect that a change is
  actually needed and produce a diff for approval before applying it.

### Good routine candidates (all report-first)
| Routine | Cadence | Output |
|---|---|---|
| Project health review | daily | summary of gate status, open risks, drift |
| Security audit | weekly | `/audit-security` report |
| Dependency review | weekly | new CVEs, outdated/abandoned deps (`.claude/checklists/dependencies.md`) |
| Nightly test/audit report | nightly | test + audit summary |
| Docs-drift check | weekly | code-vs-docs mismatches |
| Production-readiness review | before release / monthly | `/audit-production` report |
| Post-launch monitoring review | weekly post-launch | SLO/error-budget + incident review |
| Backlog grooming | weekly | stale/duplicate issues flagged (proposed, not changed) |

### Runners (tool-agnostic — pick what the project uses)
A routine is **defined** once (`.claude/templates/routine-template.md`) and **run** by any of:
- **Cron / CI schedule / GitHub Actions `schedule:`** — portable, no extra dependency; runs `/headless-run`.
- **Claude Code native scheduling** — the `/schedule` cloud agents and the `scheduled-tasks` MCP, where available.
Choose the runner per project; the safety contract is identical regardless of runner. Record each routine and
its next-due date in `docs/state/routines.md` via `/manage-routines`.

## Related

- Operating model: `.claude/docs/CLAUDE_CODE_OPERATING_MODEL.md`
- Hooks safety: `.claude/docs/HOOKS_SAFETY_MODEL.md`
- Checklists: `.claude/checklists/headless-ci.md`, `.claude/checklists/routine-safety.md`
- Constitution: `.claude/CLAUDE.md` §6 (ask the user), §8 (safety)

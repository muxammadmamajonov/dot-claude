---
name: routine-authoring
description: Use when defining a scheduled/recurring routine that runs the project OS unattended — a nightly audit, a weekly dependency scan, a daily readiness check. Covers schedule, scope, report-first posture, approval gates, runner selection (cron/CI/Claude Code native /schedule + scheduled-tasks MCP), and a kill-switch. Triggers on — routine, schedule, recurring, cron, nightly, weekly, automated task, /schedule, scheduled job, run every.
---

# Routine Authoring: Define a Safe Scheduled Job

## When to use
- The user wants something to run on a schedule — nightly, weekly, on a cron expression — without being asked each time.
- You are turning a manual check (audit, scan, readiness review, report) into a recurring routine.
- A routine already exists and you are reviewing it for scope creep or unsafe actions.

This applies to every project type — a nightly security audit, a weekly dependency/supply-chain scan, a daily readiness or cost check, a recurring docs-sync. The cardinal rule: a routine **reports and recommends; it does not take unsupervised destructive or production actions**. A scheduled job runs with no human watching, so its blast radius must be near zero by construction. See `.claude/docs/HEADLESS_AND_ROUTINES.md`.

## Workflow
1. **Define scope narrowly first.** Start from `.claude/templates/routine-template.md`. State exactly what the routine inspects and produces, and what it must never touch. Prefer the smallest useful job (one audit, one scan) over a broad "do everything nightly" routine. Like headless runs, a routine is **read/review-only by default** — writes are an explicit, narrow opt-in with a rollback, never the default (`.claude/skills/headless-automation/SKILL.md`).
2. **Set a sensible schedule.** Choose frequency and timing that match the value and cost: heavy scans off-peak, light checks more often. Avoid overlapping runs (add a lock or a max-runtime). Record the cron expression / interval and the timezone explicitly so it is unambiguous.
3. **Make it report-first.** The routine's job is to *find and surface*, then recommend — open an issue, write a report, notify — not to silently fix. Any change it might suggest is presented for human action. This keeps an unattended job from causing surprise damage.
4. **Gate every consequential action behind explicit approval.** If a routine could ever do more than report (e.g. open a PR with a proposed fix), that capability must be (a) explicitly enabled, (b) limited to reversible, non-production changes, and (c) still subject to a human merge/approve step. Never let a routine delete, drop, deploy, mass-send, or perform any `.claude/CLAUDE.md` §8 action unsupervised.
5. **Select the runner deliberately.** Match the runner to the need and to what is configured:
   - **cron** — simple, host-local, no extra deps; good for a single machine.
   - **CI scheduler** (e.g. scheduled pipeline) — runs in the project's existing CI with its guards and secret store; good for repo-wide audits. Pairs with `.claude/skills/headless-automation/SKILL.md`.
   - **Claude Code native `/schedule`** + the **scheduled-tasks MCP** — when available and configured. Never assume this MCP exists; if it is needed and absent, ask the user to configure it (`.claude/skills/mcp-integration/SKILL.md`).
6. **Build in a kill-switch.** Every routine must be easy to pause and remove: a documented disable step (comment out the cron line, disable the schedule, delete the task) and, ideally, a flag/file the routine checks to no-op. A routine you cannot stop quickly is a liability.
7. **Protect secrets in the scheduled context.** The runner pulls credentials from its own secret store / env at runtime; the routine never prints or commits them, and logs must not leak them (treat logs as public, per headless rules).
8. **Verify before enabling.** Run the routine once manually, confirm the report output and that it took no unintended action, then check it against `.claude/checklists/routine-safety.md` before scheduling it live.

## Standards
- **Do** keep routines read/review-only and report-first by default; recommend, don't silently act.
- **Do** scope narrowly, set an explicit schedule + timezone, and prevent overlapping runs.
- **Do** gate any consequential action behind explicit human approval and a rollback.
- **Do** choose the runner to fit (cron / CI / native `/schedule` + scheduled-tasks MCP) and never assume an MCP is present.
- **Do** provide a documented kill-switch and a dry-run before going live.
- **Do** keep secrets in the runner's secret store; never log or commit them.
- **Do-not** let a routine perform destructive or production actions unsupervised.
- **Do-not** ship a routine with no off-switch or no report output.
- **Do-not** schedule an unverified routine, or one whose scope you can't fully state.

## Common mistakes to avoid
- Authoring a routine that auto-applies fixes instead of proposing them, causing silent surprise changes.
- A nightly job that deploys, prunes data, or rotates credentials with nobody watching.
- Overlapping long runs that stomp on each other because there's no lock or max-runtime.
- Ambiguous schedules (no timezone) that fire at the wrong hour.
- Assuming the scheduled-tasks MCP is configured and "scheduling" against a server that doesn't exist.
- Leaking a token into the scheduled run's log.
- No kill-switch, so a misbehaving routine can't be stopped without hunting for where it was defined.

## Output format
A completed `.claude/templates/routine-template.md` (saved under `docs/`): name and purpose, exact scope (and explicit out-of-scope), schedule (cron/interval + timezone), runner choice and why, report/notify target, the report-first/approval posture, any opted-in write with its rollback, the kill-switch procedure, and the dry-run result. Attach the `.claude/checklists/routine-safety.md` result. The routine ships disabled-then-verified, not enabled-then-hoped.

## Related agents
- `.claude/agents/core/orchestrator.md`
- `.claude/agents/engineering/devops-engineer.md`
- `.claude/agents/quality/reliability-engineer.md`

## Related skills/docs/checklists
- `.claude/docs/HEADLESS_AND_ROUTINES.md`
- `.claude/skills/headless-automation/SKILL.md`
- `.claude/skills/mcp-integration/SKILL.md`
- `.claude/templates/routine-template.md`
- `.claude/checklists/routine-safety.md`
- `.claude/commands/manage-routines.md`

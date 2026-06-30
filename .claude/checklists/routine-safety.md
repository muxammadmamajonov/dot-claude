# Routine Safety Checklist

Gate for **scheduled and recurring agent runs** — cron jobs, periodic routines, and any agent that fires repeatedly without a human kicking it off each time. The defining risk of a routine is *repetition without supervision*: a single bad action becomes a bad action that runs every hour, forever, until someone notices. This checklist requires that every routine has an owner, a kill-switch, an idempotency guarantee, and a failure alert; that it **reports and recommends before it acts** on anything destructive; and that it reads project classification/state before doing work. See `.claude/docs/HEADLESS_AND_ROUTINES.md`, define routines with `.claude/templates/routine-template.md`, and follow `.claude/skills/routine-authoring/SKILL.md`.

## P0 — Blockers (must pass before a routine is scheduled)

- [ ] The routine has a **named owner** (a person or rotation, not "the team") recorded in `.claude/templates/routine-template.md`, accountable for its runs and its failures.
- [ ] A **kill-switch** exists and is documented — a single, fast way to disable the routine (config flag, disabled schedule, paused job) without editing code or redeploying.
- [ ] The routine is **idempotent**: running it twice (or after a partial failure) produces the same end state and causes no duplicate side effects (no double-send, double-charge, double-deploy); the idempotency mechanism is stated, not assumed.
- [ ] A **failure alert** is wired: when a run errors, times out, or is skipped, the owner is notified (page/channel/email); silent failure of a recurring job is forbidden.
- [ ] **No destructive or production action runs unsupervised on a schedule.** For anything that deletes, mutates prod, sends to real users, deploys, or spends money, the routine **reports and recommends first** and requires explicit human approval to act — it never auto-executes the forbidden set (CLAUDE.md §8) on a timer.
- [ ] The routine **reads project classification and current state** (preset, `docs/state/`, relevant specs) **before acting**, so its actions match the actual project stage and configuration rather than stale assumptions.
- [ ] The routine runs against **non-production by default**; touching production requires explicit per-run human approval and a tested rollback (CLAUDE.md §8).

## P1 — Important (soon after the routine is live)

- [ ] A **max-run and cost budget** bounds each invocation (wall-clock cap + token/spend ceiling) and a cap on consecutive failures before the routine auto-disables and pages the owner.
- [ ] **Change-detection precedes action**: the routine checks whether anything actually changed since the last run and no-ops (or only reports) when there is nothing to do, instead of acting every cycle regardless.
- [ ] Each run emits a report to a defined destination (issue, channel, or `.claude/templates/headless-audit-report.md` artifact) covering what it found, what it recommended, and what — if anything — it did.
- [ ] The routine uses a **least-privilege scoped identity**, not a personal or admin credential; its permissions cover only what its steps require.
- [ ] An **escalation path** is defined for runs that detect a serious issue (e.g. a failing security gate): who is notified, how urgently, and what the routine does in the meantime (pause vs. continue reporting).

## P2 — Hardening

- [ ] **Drift detection** is in place: the routine flags when the environment, config, or its own assumptions have diverged from what it was authored against, and surfaces this to the owner rather than acting on a stale model.
- [ ] Runs are serialized or locked so two scheduled invocations cannot overlap and race on shared state.
- [ ] The schedule itself is reviewed for sanity (frequency vs. cost and blast radius); high-frequency routines that touch shared state get extra scrutiny.

## P3 — Post-launch / backlog (track, revisit; never blocks)

- [ ] **Run-history retention** is configured so past runs (inputs, outputs, decisions) are queryable for a defined window, supporting audit and debugging.
- [ ] Routines are **periodically re-reviewed** (e.g. quarterly): still needed? still owned? still least-privilege? still idempotent? Stale routines are retired, not left running.
- [ ] Routine reports are aggregated for portfolio-level visibility into what is running automatically across projects.

## How to use

**When:** Run this checklist before scheduling any routine, before broadening a routine's scope or permissions, and at each periodic re-review. Re-verify the P0 block whenever the routine gains the ability to act (rather than only report).

**Who:** The routine's **named owner** is accountable; `reliability-engineer` (`.claude/agents/quality/reliability-engineer.md`) reviews kill-switch, idempotency, alerting, and budgets; `security-auditor` verifies the no-unsupervised-destructive-action rule and least-privilege identity; `technical-lead` approves any P0 exception via `.claude/templates/decision-record.md`.

**Command:** `/audit-production` (`.claude/commands/audit-production.md`) covers scheduled-run readiness. P0 items block the routine from being scheduled (or from acting); P1 items are tracked issues; P2–P3 are backlog.

**Tools:** the routine definition in `.claude/templates/routine-template.md`, a documented kill-switch (config flag / paused schedule), failure alerting (pager/channel), scoped service-account credentials, wall-clock and spend budgets, change-detection, and per-run reports.

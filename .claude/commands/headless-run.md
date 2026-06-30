---
description: Run a chosen audit/review/readiness command non-interactively (CI); convert STOP gates into recorded assumptions, fail closed on any safety violation, and emit a deterministic report and exit code.
argument-hint: <command-to-run> [--allow-writes non-prod | --check-only — default: check-only]
---

# /headless-run

## Purpose
Execute one of this system's audit, review, or readiness commands in a non-interactive (CI / scheduled / automated) context where no human is present to answer a STOP gate. Where an interactive command would pause for a business-critical decision (CLAUDE.md §6), this runner instead records the decision as an assumption and continues with the **safe default**, so the run completes deterministically. It **fails closed**: any §8 safety violation, any unresolvable P0 finding, or any attempt at a destructive/production action aborts the run with a non-zero exit code. By default it is **read/review-only**; writes are confined to non-production and require explicit opt-in. The run emits a structured report and returns a deterministic exit code suitable for a CI gate.

## When to use
- In CI to enforce a quality gate on every pull request or merge (e.g. headless `/audit-security`, `/review-feature`, `/audit-performance`).
- On a schedule (nightly/weekly) to run `/audit-production` or a dependency review without a human in the loop — typically invoked via `/manage-routines`.
- Before a release, to produce a deterministic, archived readiness verdict that the pipeline can branch on.
- Never for the interactive design stages (interview, spec): those require a human and must not be defaulted away.

## Workflow

### Step 0 — Load context and parse mode (read-only)
1. Read `.claude/docs/HEADLESS_AND_ROUTINES.md` for the headless execution contract and exit-code semantics.
2. Read `.claude/skills/headless-automation/SKILL.md` for the gate-to-assumption conversion method and fail-closed rules.
3. Read `.claude/checklists/headless-ci.md` — the checklist this run must satisfy to be considered valid.
4. Read `.claude/templates/headless-audit-report.md` — the report shape to emit.
5. Parse the target command (the first argument) and the write mode: `--check-only` (default, no writes beyond the report) or `--allow-writes non-prod` (writes permitted to non-production paths only). Any value naming production is rejected here.
6. Confirm the target command exists under `.claude/commands/`. If not, **STOP** with exit code 2 (configuration error).

### Step 1 — Establish the safety envelope
Before running anything, lock the envelope for the whole run:
- **No production actions.** Deploys, migrations, prod credential use, data deletion, force-push, or anything in §8 are unconditionally forbidden and cause an immediate fail-closed abort.
- **Writes are non-prod only**, and only if `--allow-writes non-prod` was passed; otherwise the run is strictly read/review-only and may write only its own report.
- **No secrets** are read, printed, or written. A detected secret-exposure path aborts the run.
- Record the active envelope at the top of the report so the verdict is auditable.

### Step 2 — Run the target command's analysis
Invoke the target command's workflow in analysis mode. Collect its findings, severities (P0–P3), and any point where it would normally **STOP** for a human decision.

### Step 3 — Convert STOP gates to recorded decisions
For each interactive STOP the target command raises:
1. Identify the safe default (the more conservative, more reversible choice — e.g. "treat the unverified dependency as a risk", "do not skip the gate").
2. Apply that default and continue.
3. Record the substituted decision as an assumption via `.claude/templates/assumptions-log.md` in `docs/state/assumptions.md`, and as a decision record via `.claude/templates/decision-record.md` when the choice is architectural — per CLAUDE.md §6–§7. Each entry notes that it was auto-resolved in headless mode and how a human can override it on the next interactive run.

### Step 4 — Apply the fail-closed rule
Determine the verdict:
- Any §8 violation encountered, or any destructive/production action attempted → **abort, exit non-zero (≥10)**, report the violation.
- Any unresolved **P0** finding from the target command → **fail the gate, exit non-zero (1)**.
- P1–P3 findings only → **pass with warnings, exit 0**, findings listed in the report.
- Clean → **pass, exit 0**.
When uncertain whether a finding is P0, treat it as P0 (fail closed).

### Step 5 — Emit the report and exit code
1. Write `docs/reports/headless-<command>-<date>.md` from `.claude/templates/headless-audit-report.md`: the safety envelope, every finding with severity, every auto-resolved gate (with its assumption ID), and the final verdict.
2. Verify the report and run against `.claude/checklists/headless-ci.md`; if the run itself is non-conformant (e.g. missing envelope record), exit code 2.
3. Print the deterministic exit code last so the CI pipeline can branch on it.

## Agents used
- `.claude/agents/core/orchestrator.md` — drives the headless execution loop and enforces the fail-closed envelope.
- `.claude/agents/quality/production-readiness-auditor.md` — aggregates findings into the go/no-go verdict when the target is a readiness command.

## Skills used
- `.claude/skills/headless-automation/SKILL.md` — non-interactive execution method, gate-to-assumption conversion, and deterministic exit-code mapping.

## Expected outputs
| Output | Path |
|---|---|
| Headless run report | `docs/reports/headless-<command>-<date>.md` |
| Assumptions appended (auto-resolved gates) | `docs/state/assumptions.md` |
| Decision records (for architectural auto-resolutions) | `docs/decisions/` |

## Stop conditions
- Target command not found or argument malformed → exit code 2 (configuration error); no analysis run.
- Any §8 safety violation or attempted production/destructive action → fail closed, exit ≥10, report the cause.
- Write requested against a production path → reject and exit 2; headless writes are non-prod only.
- Run cannot satisfy `.claude/checklists/headless-ci.md` (e.g. report incomplete) → exit 2; the result is not a valid gate.

## Final report format
```
## /headless-run — <command> — <date>

**Mode:** check-only | allow-writes(non-prod)
**Safety envelope:** no-prod-actions=enforced  secrets=blocked  writes=<none|non-prod>

### Findings
| ID | Severity | Summary | Source step |
|---|---|---|---|
| F-001 | P0 | <blocker> | <step> |

### Auto-resolved gates (headless defaults)
| Gate | Safe default applied | Assumption ID | Human override |
|---|---|---|---|
| <gate name> | <conservative choice> | A-014 | re-run interactively |

### Verdict
<PASS | PASS-WITH-WARNINGS | FAIL | ABORT-SAFETY>  →  exit code: <0|1|2|≥10>

### Report
docs/reports/headless-<command>-<date>.md
```

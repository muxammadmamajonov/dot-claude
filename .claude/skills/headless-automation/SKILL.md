---
name: headless-automation
description: Use when running the project OS non-interactively — in CI, a pipeline, or any unattended context — where there is no human to answer prompts. Defines which commands are safe headless (audits, reviews, readiness/security/test-plan checks, issue lists, docs-sync), how STOP-gates become recorded assumptions/decisions, deterministic exit codes, and no-secret-leakage logging. Triggers on — headless, CI, non-interactive, pipeline, automated run, unattended, exit code, ci check, headless-run.
---

# Headless Automation: Run Read-Only in CI

## When to use
- Running this OS inside CI/CD, a scheduled job, or any pipeline with no human at the keyboard.
- Wanting automated audits, reviews, or readiness checks to gate a merge or deploy.
- Producing a deterministic pass/fail signal and a report artifact for a build.
- Any unattended invocation where a normal interactive STOP-and-ask would simply hang.

This applies to every project type — a web app's PR gate, a CLI tool's release check, a backend's pre-deploy audit, a data pipeline's contract check. The default posture is **read/review-only**: headless runs observe, audit, and report; they do not change code, data, or infrastructure unless writes are *explicitly* opted in for that specific job. See `.claude/docs/HEADLESS_AND_ROUTINES.md`.

## Workflow
1. **Default to read-only.** A headless run inspects and reports. It may read the repo, run tests/lint/build, and execute audit and review checklists. It must not edit files, push, deploy, mutate databases, or call destructive tools unless the job explicitly enables a narrow, named write and a rollback exists. Honor `.claude/CLAUDE.md` §8 and the guards in `.claude/settings.json` / `.claude/hooks/`.
2. **Pick headless-safe work only.** Good fits: security audit (`.claude/checklists/security.md`), QA/performance/accessibility gates, production-readiness checks (`.claude/checklists/production.md`), code review, docs-sync verification, dependency/supply-chain scan, issue/finding lists, and test-plan generation. Avoid anything that needs a business-critical human decision mid-run.
3. **Convert STOP-gates into recorded assumptions/decisions — never blocking prompts.** Interactive flows stop and ask the user. Headless cannot. When a run hits a decision point, it must (a) choose the safest default, (b) record it as an assumption (`.claude/templates/assumptions-log.md`) or, for architectural calls, a decision record (`.claude/templates/decision-record.md`), and (c) surface it in the report and exit code — not hang waiting for input. A red gate that needs a human becomes a recorded blocker, not a silent skip.
4. **Use deterministic exit codes.** Map outcomes consistently so the pipeline can act: `0` = all gates passed; non-zero = a gate failed or a P0/P1 blocker was found; reserve a distinct code for "completed with recorded assumptions needing human review". Document the mapping so CI logic and humans read it the same way. Same inputs should yield the same code.
5. **Never leak secrets in logs.** CI logs are widely visible and retained. Do not print env vars, tokens, `.env*` contents, connection strings, or full PII. Mask anything sensitive; reference secrets, never echo them (`.claude/CLAUDE.md` §8). Assume the log is public.
6. **Emit a structured report artifact.** Write findings to `.claude/templates/headless-audit-report.md` (saved as a build artifact, e.g. under `docs/state/` or the CI artifacts dir): gates run, pass/fail per gate, P0–P3 findings with locations, recorded assumptions/decisions, and the final verdict + exit code.
7. **Verify the run itself.** Check the run against `.claude/checklists/headless-ci.md` — read-only posture honored, no secrets in logs, exit codes correct, report emitted, assumptions recorded.
8. **Fail safe.** On ambiguity, tooling error, or a gate that cannot be evaluated, exit non-zero with an explanatory report rather than passing by default. A green that wasn't actually checked is worse than an honest failure.

## Standards
- **Do** keep headless runs read/review-only unless a specific write is explicitly opted in with a rollback.
- **Do** record every mid-run decision as an assumption/decision and reflect it in the report and exit code.
- **Do** use a documented, deterministic exit-code mapping.
- **Do** mask secrets and PII in all logs and artifacts; treat logs as public.
- **Do** emit the audit report artifact every run, pass or fail.
- **Do-not** prompt for interactive input in a headless context — it will hang the pipeline.
- **Do-not** perform destructive or production actions unattended.
- **Do-not** pass a gate that could not actually be evaluated; fail safe instead.

## Common mistakes to avoid
- Reusing an interactive STOP-and-ask in CI, hanging the job until it times out.
- Silently skipping a red gate instead of recording it as a blocker and exiting non-zero.
- Echoing environment variables or a token into the build log "for debugging".
- Non-deterministic exit codes, so the pipeline can't reliably gate on the result.
- Letting a headless run edit files or deploy because write-mode was left on by default.
- Exiting `0` when a tool crashed and the gate was never evaluated.
- Producing no artifact, so a failed run leaves nothing for a human to triage.

## Output format
A `.claude/templates/headless-audit-report.md` artifact: run metadata (commit, branch, time), each gate/checklist run with pass/fail, P0–P3 findings with file/line, every recorded assumption/decision with its reversal, and the final verdict mapped to the exit code. The process exit code is the machine signal; the report is the human-readable companion. Reference the relevant checklist (`.claude/checklists/security.md`, `production.md`, etc.) per gate.

## Related agents
- `.claude/agents/core/orchestrator.md`
- `.claude/agents/quality/production-readiness-auditor.md`
- `.claude/agents/quality/security-auditor.md`

## Related skills/docs/checklists
- `.claude/docs/HEADLESS_AND_ROUTINES.md`
- `.claude/skills/terminal-operations/SKILL.md`
- `.claude/templates/headless-audit-report.md`
- `.claude/templates/assumptions-log.md`
- `.claude/checklists/headless-ci.md`
- `.claude/checklists/production.md`
- `.claude/commands/headless-run.md`

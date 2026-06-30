---
description: Pre-commit Definition-of-Done gate against the STAGED diff — lint/build/test status, secret scan, DoD and safety checks; returns PASS or BLOCK without committing.
argument-hint: [strict — optional; treat P1 gaps as BLOCK, not WARN]
---

# /commit-ready

## Purpose
Act as the last gate before a commit. Inspect **only the staged diff** (`git diff --cached`), run the cheap automated checks (lint, build, tests, secret scan), then evaluate the change against the CLAUDE.md §5 ten-point Definition of Done and the §8 destructive/secret hard constraints. Return a clear **PASS** or **BLOCK** verdict with the specific gaps. This command **does not commit** — it advises; the user (or a later command) commits. It is the human-speed equivalent of the `pre-commit-check` hook, runnable on demand. Universal by default: it adapts its build/test/lint commands to whatever the project is (CLI, game, service, library, embedded) and degrades gracefully when a tool is absent.

## When to use
- Immediately before `git commit`, to confirm a change is actually Done, not just written.
- After finishing a build phase (CLAUDE.md stage 5), as the per-phase verification step.
- Before opening a pull request, as a self-review pass.
- Any time you want a fast read on whether the staged work would survive review.

## Workflow

### Step 0 — Establish the staged surface
1. Confirm this is a git repo and there is a staged change: run `git diff --cached --stat`. If nothing is staged, **STOP** and tell the user to `git add` the intended files first.
2. Record the changed-file report (paths + insertions/deletions) for the final report.
3. Detect whether any **`.claude/` system files** are staged (paths under `.claude/`). If so, set the `system-files-touched` flag — it triggers the integrity sub-gate in Step 4.
4. Read the project context that defines what the checks mean: `docs/state/active-team.md` (if present) for the active checklists, and `.claude/docs/CLAUDE_CODE_OPERATING_MODEL.md` for how this gate fits the overall operating model.

### Step 1 — Automated quality checks (lint / build / test)
Run the project's own commands; skip gracefully and mark `not-available` if a tool is missing. Examples by ecosystem (use what the repo actually defines):

| Check | Typical command |
|---|---|
| Lint | `npm run lint` / `ruff check .` / `cargo clippy` / `golangci-lint run` |
| Build | `npm run build` / `cargo build` / `go build ./...` / `make` |
| Tests | `npm test` / `pytest` / `cargo test` / `go test ./...` |

Capture pass/fail and the failing items. Prefer running tests **affected by** the staged files where the runner supports it, but never report green if you skipped the suite — say it was scoped.

### Step 2 — Secret scan on the staged diff
1. Scan the staged diff for secrets: API keys, tokens, private keys, passwords, connection strings, and any staged `.env*` file (CLAUDE.md §8).
2. Use available tooling (`gitleaks protect --staged`, `trufflehog git file://. --since HEAD`) and a direct pattern check on `git diff --cached` as a fallback.
3. **Any secret or staged `.env*` is an automatic BLOCK** — do not soften it. Never print the secret value back; reference the file and line only.

### Step 3 — Definition-of-Done evaluation (CLAUDE.md §5)
Walk the ten DoD points against the staged change and mark each PASS / WARN / FAIL / N/A:
1. **Specified** — traces to a spec or decision record; no undocumented scope.
2. **Implemented** — does what it claims; no obviously broken paths.
3. **Tested** — tests added/updated for new behaviour; suite green (from Step 1).
4. **Secure** — passes `.claude/checklists/security.md` essentials (from Steps 1–2 + diff review).
5. **Quality-checked** — lint/build clean (Step 1); edge cases and errors handled.
6. **Performant** — no obvious regression against `.claude/checklists/performance.md` targets.
7. **Accessible** — `.claude/checklists/accessibility.md` where a human interface changed; clear output/docs otherwise.
8. **Documented** — README/usage/runbook and `docs/state/assumptions.md` updated if behaviour or decisions changed.
9. **Reversible** — change is revertible; any migration has a down path (and existing migrations are untouched, §8).
10. **Reviewed** — flag whether human/agent review and any business-critical approval still owe.

### Step 4 — System-integrity sub-gate (only if `.claude/` files staged)
If `system-files-touched` is set, run the integrity check before allowing PASS:
1. Invoke `.claude/commands/self-test.md`, which runs `python3 .claude/scripts/integrity-check.py`.
2. Any integrity failure (broken link, malformed frontmatter, invalid JSON, shallow file) is a **BLOCK** — the reusable system must not be committed broken.

### Step 5 — Verdict and report
1. Compute the verdict: **BLOCK** if any hard constraint fails (secret, destructive action, broken build/tests, failed integrity, any DoD **FAIL**); otherwise **PASS** (with WARNs noted). In `strict` mode, DoD **WARN** items are also treated as BLOCK.
2. Write `docs/state/commit-readiness.md` with the full result.
3. Present the verdict. **Do not run `git commit`** — recommend the next action only.

## Agents used
- `.claude/agents/core/code-reviewer.md` — reviews the staged diff for correctness, security, and convention adherence.
- `.claude/agents/core/technical-lead.md` — owns the DoD interpretation and the PASS/BLOCK call.

## Skills used
- `.claude/skills/testing/SKILL.md` — selecting and scoping the right tests for the staged change.
- `.claude/skills/security/SKILL.md` — secret-scan patterns and diff-level security review.

## Expected outputs
| Output | Path |
|---|---|
| Commit-readiness report | `docs/state/commit-readiness.md` |
| Updated assumptions (if behaviour changed) | `docs/state/assumptions.md` |

## Stop conditions
- **Nothing staged** → **STOP**; ask the user to `git add` the intended files.
- **Secret or staged `.env*` detected** → **BLOCK immediately**; instruct the user to unstage and remove it before any commit.
- **Build or tests fail** → **BLOCK**; report the failing items, do not attempt large fixes inline.
- **`.claude/` files staged and integrity check fails** → **BLOCK**; point to the self-test output.
- **Destructive operation staged** (deleted/edited migration, bulk deletion) → **BLOCK** per §8; require explicit user intent.
- This command **never commits** — even on PASS it stops at the recommendation.

## Final report format
```
## /commit-ready — Commit Readiness Report

**Verdict:** ✅ PASS  |  ⛔ BLOCK
**Generated:** <ISO date>  |  **Mode:** normal | strict
**System files staged:** yes/no

### Staged changes
| File | + | − |
|---|---|---|
| path/to/file | N | N |

### Automated checks
| Check | Result |
|---|---|
| Lint | pass / fail / not-available |
| Build | pass / fail / not-available |
| Tests | pass (N) / fail (N) / scoped / not-available |
| Secret scan | clean / BLOCK |
| Integrity (.claude/) | pass / BLOCK / n-a |

### Definition of Done (§5)
| # | Item | Status |
|---|---|---|
| 1 | Specified | PASS/WARN/FAIL/N-A |
| … | … | … |

### Blockers (must resolve before commit)
- <blocker + file:line + fix>

### Warnings (resolve soon)
- <warning>

### Recommendation
PASS → suggested commit message: `<type>(<scope>): <summary>`  (user runs the commit)
BLOCK → fix the blockers above, re-stage, and re-run /commit-ready.
```

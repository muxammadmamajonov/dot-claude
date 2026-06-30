---
description: Improve code structure without changing behavior, guarded by tests and small reversible commits.
argument-hint: [file, module, or feature name — optional]
---

# /refactor-safely

## Purpose
Restructure existing code — extract functions/classes, rename, split modules, reduce coupling, eliminate duplication — while keeping observable behavior identical. Every step is guarded by a passing test suite and committed atomically so any step can be reverted cleanly.

## When to use
- Code smells are slowing new feature work (long functions, deep nesting, God classes, copy-paste logic).
- A module needs to be split before a new feature can be added safely.
- Tech-debt sprint or pre-release cleanup.
- Before running `/audit-security` or `/audit-performance` so findings are easier to act on.

## Workflow

### Step 0 — Understand scope
1. Read `docs/specs/` for any existing architecture decisions that constrain the refactor.
2. If an argument was given, focus on that file/module. Otherwise, ask the user to name the target. **STOP — business-critical decision: confirm scope with user before proceeding.**
3. List all files in scope. Record them as a "blast radius" comment at the top of the session.

### Step 1 — Establish a green baseline
1. Identify the existing test command (`package.json`, `Makefile`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.).
2. Run the full test suite. If it is not green, **STOP** — do not refactor a broken codebase. Report failures and ask the user how to proceed.
3. If there are no tests covering the target code, spawn `.claude/agents/quality/test-automation-engineer.md` to write characterisation tests first, then return here.
4. Commit the green baseline: `git commit -m "chore: green baseline before refactor"`.

### Step 2 — Analyse and plan
1. Read the target files in full.
2. Identify refactor candidates using this priority order:
   - Duplicate code blocks (DRY violations).
   - Functions/methods longer than ~40 lines.
   - Deep nesting (>3 levels).
   - Mixed abstraction levels within one function.
   - God classes / monolithic modules.
   - Unclear names.
3. Write a numbered refactor plan (one atomic commit per item). Each item must state: *what changes*, *why it is safe*, *which tests cover it*.
4. **STOP — show the plan to the user and get approval before making any edits.**

### Step 3 — Execute one step at a time
For each plan item:
1. Make the structural change only — no logic changes, no bug fixes, no feature additions.
2. Run the test suite. If any test fails, **revert the change immediately** (`git checkout -- <files>`). Report what broke and ask the user whether to skip or redesign this step.
3. If green, commit: `git commit -m "refactor(<scope>): <one-line description>"`.

### Step 4 — Post-refactor review
1. Run the full test suite one final time. Record the result.
2. Run a quick lint/type-check (`eslint`, `mypy`, `cargo clippy`, `go vet`, etc.) if available.
3. Update any inline doc-comments or JSDoc/docstrings that no longer match after renaming.
4. If the refactor touched public API surfaces, flag this for the user — downstream consumers may need updating.

### Step 5 — Report
Produce the Final report (see below).

## Agents used
- `.claude/agents/quality/test-automation-engineer.md` — generates characterisation tests when coverage is missing.
- `.claude/agents/core/orchestrator.md` — coordinates multi-file refactors spanning several modules.

## Skills used
- `.claude/skills/testing/SKILL.md` — language-specific refactor patterns.
- `.claude/checklists/qa.md` — post-refactor quality gates.

## Expected outputs
| Output | Path |
|---|---|
| Refactored source files | in-place edits |
| Characterisation tests (if created) | alongside existing test files |
| Commit history | one commit per atomic step |

## Stop conditions
- Test suite is not green at baseline → halt, report failures.
- No scope provided and no clear candidate → ask user.
- Any test fails after a change → revert that step, ask user.
- Change would alter public API, DB schema, file formats, or network contracts → treat as out-of-scope; open a separate task.
- Refactor would require touching >10 files simultaneously → split into smaller sessions.

## Final report format
```
## Refactor Complete

**Target:** <file/module/feature>
**Steps completed:** <N> of <N planned>

### Changes made
| Step | What changed | Tests | Commit |
|---|---|---|---|
| 1 | … | ✅ green | abc1234 |

### Skipped steps
- <step N>: <reason>

### Follow-up recommended
- <any items deferred — e.g., API surface changes, missing tests>

**Test suite:** ✅ green  |  **Lint:** ✅ clean
```

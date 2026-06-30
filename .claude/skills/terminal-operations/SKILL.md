---
name: terminal-operations
description: Use when working in a project's terminal/shell — inspecting an unfamiliar repo, understanding a codebase before editing, making small reversible code changes, running tests/lint/build and reading results, or reporting exactly which files changed. Triggers whenever Claude Code touches the filesystem or runs shell commands. Keywords — terminal, bash, shell, git status, git diff, run tests, build, lint, inspect repo, what changed.
---

# Terminal Operations: Work Safely in a Project Shell

## When to use
- Landing in an unfamiliar repository and needing to understand it before changing anything.
- Making a code or config change and wanting it small, verified, and reversible.
- Running tests, linters, type-checkers, or builds and interpreting their output.
- Reporting back precisely which files changed and why.
- Any time a shell command could be destructive, slow, or touch secrets.

This applies to every project type: a web app, a CLI tool, a mobile build, a backend service, a data pipeline, or an embedded firmware tree. The commands differ per ecosystem; the discipline — read first, change small, verify, report — does not. See `.claude/docs/CLAUDE_CODE_OPERATING_MODEL.md` for how this fits the wider operating model.

## Workflow
1. **Read before you write.** Never edit a file you have not read. Map the repo first: read `README`/`README.md`, the manifest(s) (`package.json`, `pyproject.toml`/`requirements.txt`, `go.mod`, `Cargo.toml`, `pom.xml`, `Gemfile`, `composer.json`, `*.csproj`), CI config, and any `CONTRIBUTING`/`docs/`. List structure with a non-destructive command (`git ls-files`, `ls`, `find` with depth limits) — not by deleting or moving anything.
2. **Establish the baseline.** Run `git status` and `git rev-parse --abbrev-ref HEAD` to know the working state and branch. If the tree is dirty, understand why before adding to it. If you are on the default branch and about to change code, branch first.
3. **Find the right place to change.** Use search (`grep -r`, `rg`, language tooling) to locate the symbol, route, or config you need. Confirm the framework/stack from the manifest rather than assuming.
4. **Change in small reversible slices.** Edit one coherent thing at a time. Prefer a sequence of small diffs over one large rewrite. Keep each slice independently revertible (`git revert`, `git checkout -- <file>`, or a feature flag) — see `.claude/CLAUDE.md` §8 and §5.9.
5. **Run the project's own checks.** Use the commands the repo defines (scripts in the manifest, `make` targets, `npm test`/`pytest`/`go test`/`cargo test`/`dotnet test`, the configured linter and type-checker, the build). Do not invent a test runner the project does not use.
6. **Read the results, don't just trigger them.** Parse failures: which test, which assertion, which file/line. Re-run the narrowest failing target while iterating. A green build you didn't read is not verification.
7. **Report exactly what changed.** Show the change surface with `git status --porcelain` and `git diff --stat` (and `git diff` for the substance). Name every modified file with an absolute or repo-relative path. Never claim a file changed without it appearing in the diff.
8. **Defer destructive actions to the guardrails.** Let `.claude/settings.json` (`permissions.deny`/`permissions.ask`) and the opt-in `.claude/hooks/dangerous-command-guard.json` gate dangerous commands. If a command is denied or prompts, stop and ask — do not work around the guard.

## Standards
- **Do** read files and manifests before editing; confirm the stack from evidence, not memory.
- **Do** keep changes small, scoped, and revertible; have the rollback in mind before you act.
- **Do** prefer the project's existing scripts/targets over ad-hoc commands; respect its conventions.
- **Do** quote paths, use explicit targets, and bound expensive commands (timeouts, `--maxdepth`, narrow globs).
- **Do** report changed files via `git status --porcelain` / `git diff --stat`; cite paths.
- **Do-not** run `rm -rf`, bulk/recursive deletes, `git push --force`, history rewrites, DB drops/truncates, or destructive migrations without explicit human approval (`.claude/CLAUDE.md` §8).
- **Do-not** print, echo, commit, or transmit secrets, tokens, private keys, or `.env*` files; never `cat .env`.
- **Do-not** disable security controls, pipe remote scripts to a shell, or run unvetted code.
- **Do-not** operate against production by default — non-prod first, prod only with approval and a tested rollback.

## Common mistakes to avoid
- Editing a file blind, then discovering it had a different structure than assumed.
- Assuming the test/build command (`npm test`) without checking the manifest — wasting a run on a script that does not exist.
- Running one giant change, breaking the build, and being unable to bisect which slice caused it.
- Treating a passing exit code as success without reading the output for skipped suites or warnings.
- `cat`-ing a `.env` or printing an API key into the transcript while "debugging".
- Reporting "I updated the config" with no diff, leaving the user unsure what actually moved.
- Reaching for `rm -rf node_modules` or `git reset --hard` as a quick fix without approval and a backup.

## Output format
A short operations report: the baseline (branch, dirty/clean), the commands you ran and their key results (tests/lint/build pass/fail with failing targets named), and a precise change list from `git status --porcelain` + `git diff --stat` with every path. Note any command that was denied/prompted by the guards and what you did instead. Flag any residual risk and the rollback path.

## Related agents
- `.claude/agents/core/technical-lead.md`
- `.claude/agents/core/code-reviewer.md`
- `.claude/agents/quality/security-auditor.md`

## Related skills/docs/checklists
- `.claude/docs/CLAUDE_CODE_OPERATING_MODEL.md`
- `.claude/docs/HOOKS_SAFETY_MODEL.md`
- `.claude/skills/security/SKILL.md`
- `.claude/skills/testing/SKILL.md`
- `.claude/checklists/security.md`
- `.claude/checklists/qa.md`

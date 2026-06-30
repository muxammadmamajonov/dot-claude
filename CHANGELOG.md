# Changelog

All notable changes to the Universal `.claude` AI Project OS are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the
project aims to follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] — 2026-06-30

Web + mobile engineering layers, an agent/skill power-up, and a CI integrity gate.

### Added
- **Agent power-up** — all agents upgraded to first-class Claude Code subagents with
  least-privilege `tools:`, `color:`, `## When to invoke` worked scenarios, and a
  `## When blocked / recovery` contract.
- **Web engineering layer** — `orchestration/web-routing-matrix.md`; commands `/web-audit`,
  `/web-readiness`; checklist `web-production`; agents `codebase-mapper`,
  `playwright-e2e-engineer`, `refactoring-specialist`, `bug-fix-specialist`,
  `auth-permission-reviewer`.
- **Mobile engineering layer** — `orchestration/mobile-routing-matrix.md`; commands
  `/mobile-audit`, `/store-readiness`; checklists `mobile-production`, `app-store-readiness`;
  agents `mobile-security-auditor` (MASVS), `mobile-release-engineer`, `mobile-e2e-engineer`;
  preset `telegram-mini-app`.
- **Bundled skill tooling** — `project-classification/scripts/detect_stack.py` and
  `testing/scripts/detect_test_runner.py`, each with an `evals/` set.
- **CI gate** — `.github/workflows/self-test.yml` runs the integrity check on push/PR.

### Changed
- Universal `orchestration/routing-matrix.md` now detects web vs mobile vs mixed and loads
  the matching engineering layer. Skill descriptions sharpened for reliable triggering.

## [1.0.0] — 2026-06-26

First public release of the template.

### Added
- **Constitution** — `.claude/CLAUDE.md`: the 9-stage flow (classify → interview → select →
  spec → build → audit → readiness → launch → continue), Definition of Done, and the hard
  safety rules.
- **Agents (116)** across six families — `core`, `engineering`, `quality`, `design`, `domain`,
  `stack` — each with explicit inputs, outputs, handoffs, and a Definition of Done.
- **Skills (65)** — repeatable procedures, including the operating-capability skills
  (`terminal-operations`, `memory-management`, `mcp-integration`, `headless-automation`,
  `routine-authoring`).
- **Commands (30)** — the invokable 9-stage workflow plus `/route`, `/brainstorm-project`,
  `/commit-ready`, `/create-github-issues`, `/setup-mcp`, `/headless-run`, `/manage-routines`,
  and `/self-test`.
- **Presets (37)**, **stack-matrices (20)**, **checklists (29, P0–P3)**, **templates (29)**.
- **Operating-capabilities layer** — `.claude/docs/`: `CLAUDE_CODE_OPERATING_MODEL`,
  `MCP_STRATEGY`, `HEADLESS_AND_ROUTINES`, `MEMORY_STRATEGY`, `SUBAGENT_ORCHESTRATION`,
  `HOOKS_SAFETY_MODEL` — making Terminal, Memory, MCP, Subagents, Hooks, Headless, and Routines
  first-class and safe-by-default.
- **Safety** — `.claude/settings.json` always-on deny/ask guards, plus 9 opt-in, safe-by-default
  hooks (`dangerous-command-guard`, `secret-scan`, `migration-safety-guard`, `production-file-guard`,
  and others).
- **Self-test** — `.claude/scripts/integrity-check.py` (the `/self-test` command) verifying link
  integrity, file depth, frontmatter, and JSON validity.
- **Examples** — four project briefs (web/SaaS, mobile, game, AI agent).
- Root docs: `README.md`, `START_HERE.md`, `PROJECT_OS.md`, `SECURITY.md`, `CONTRIBUTING.md`,
  `LICENSE`.

[1.0.0]: https://keepachangelog.com/

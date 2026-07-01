# Changelog

All notable changes to the Universal `.claude` AI Project OS are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the
project aims to follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.6.0] — 2026-07-01

Enterprise Phase 2 — governance & compliance.

### Added
- **`.github/CODEOWNERS`** — review ownership mapped across `.claude/` families (constitution, safety
  baseline, security/compliance-sensitive agents and checklists, orchestration, toolchain, governance
  meta). Ships with placeholder team handles for adopters to fill in.
- **RFC process** — `.claude/templates/rfc.md` + `CONTRIBUTING.md` §11: significant changes to the shared
  `.claude/` OS itself (new stage, new agent family, §8 change, schema change) require a filed, reviewed
  RFC before implementation — distinct from `.claude/templates/decision-record.md`, which stays scoped to
  a consuming project's own technical decisions.
- **`.claude/docs/COMPLIANCE.md`** — maps existing gates/checklists/agents to SOC 2, ISO/IEC 27001, SLSA,
  and OWASP (ASVS + Top 10) control families, with an explicit disclaimer that this is a control-mapping
  aid, not a certification, plus an evidence-chain guide and a list of what it deliberately does not cover.
- **`CODE_OF_CONDUCT.md`** and **`SUPPORT.md`** — complete the OSS governance set alongside the existing
  `SECURITY.md` and `CONTRIBUTING.md`.

### Changed
- `CONTRIBUTING.md`'s PR checklist gained an RFC/versioning line item.

### Notes
Second phase of the enterprise roadmap (design:
`docs/superpowers/specs/2026-06-30-enterprise-and-cross-tool-design.md`). Next: team & scale (v1.7.0).

## [1.5.0] — 2026-06-30

Enterprise Phase 1 — generated Cursor/Copilot adapters + a trust-spine linter.

### Added
- **Cross-tool adapter generator** — `.claude/scripts/generate_adapters.py` derives editor adapters from
  the canonical `.claude/` source: **Cursor** (`.cursor/rules/*.mdc` — global + web/mobile/desktop
  path rules + skills index) and **GitHub Copilot** (`.github/copilot-instructions.md` +
  `.github/instructions/*.instructions.md`). Generated files carry a `DO NOT EDIT — generated` header;
  `--check` mode fails on drift. Outputs committed so they work on clone.
- **Trust-spine linter** — `.claude/scripts/validate.py`: deterministic schema/rule checks
  (agent frontmatter `name/description/model/color/tools`, `color` enum, `tools` allowlist, required
  `When to use`/`When to invoke` section) as hard ERRORS, plus advisory WARNINGS (no-fabrication clause
  on auditors, command/checklist section completeness). `--strict` makes warnings fatal.

### Changed
- CI (`.github/workflows/self-test.yml`) now runs integrity-check **+ validate + adapter sync-check**.
- `/self-test` command documents all three checks.
- `production-readiness-auditor` and `privacy-compliance-auditor` gained explicit no-fabrication/evidence
  clauses (surfaced by the new linter).

### Notes
First of a phased enterprise roadmap (design: `docs/superpowers/specs/2026-06-30-enterprise-and-cross-tool-design.md`).
Next: governance & compliance (v1.6.0), team & scale (v1.7.0), low-magic ergonomics (v1.8.0).

## [1.4.0] — 2026-06-30

Cross-tool portability — usable beyond Claude Code.

### Added
- **`AGENTS.md`** — root cross-tool entry point so non-Claude-Code agents (Codex, Cursor, Gemini CLI,
  Copilot CLI, opencode) can adopt the system; defers to `.claude/CLAUDE.md` as the source of truth.
- **`GEMINI.md`** — Gemini CLI pointer with tool-name mapping notes.
- **Portability matrix** in `.claude/docs/CLAUDE_CODE_OPERATING_MODEL.md` — what executes natively in
  Claude Code (interactive + headless CLI) vs what travels as portable plain-markdown reference.

### Notes
- No change to Claude Code behavior — the OS remains fully native there (agents, commands, skills, hooks,
  settings). This release only widens reach: the methodology layer is portable everywhere; execution
  wiring stays Claude Code-specific and is read as a spec by other tools.

## [1.3.0] — 2026-06-30

Desktop engineering layer for macOS, Windows, and Linux.

### Added
- **Desktop engineering layer** — `.claude/orchestration/desktop-routing-matrix.md` (framework
  detection + modes incl. desktop-packaging-readiness & auto-update-readiness + per-OS caveats);
  commands `/desktop-audit` and `/desktop-readiness`; checklists `desktop-production` and
  `desktop-distribution` (macOS signing/notarization, Windows signing/installers, Linux packaging,
  secure auto-update); agents `electron-engineer`, `tauri-engineer`, `desktop-security-auditor`
  (Electron/Tauri shell + update integrity), `desktop-release-engineer` (signing/notarization/
  packaging/auto-update across mac·win·linux).

### Changed
- Universal `.claude/orchestration/routing-matrix.md` now also detects desktop and routes to the
  desktop layer; native/Qt/.NET/Flutter-desktop kept as routing knowledge via `desktop-engineer`.

## [1.2.0] — 2026-06-30

Mobile release tooling and a gate fix.

### Added
- **Mobile release scaffold** — `.claude/skills/mobile/scripts/scaffold_mobile_release.py`
  generates starter Fastlane (`Fastfile`/`Appfile`) and/or EAS (`eas.json`) config, a signing
  `.env.example` (placeholder var names only), and a `RELEASE.md` runbook. Idempotent, stdlib-only,
  no network, no secrets.
- **Per-store submission references** — `.claude/skills/mobile/references/app-store-submission.md`
  and `google-play-submission.md`: signing, build/upload (Fastlane + EAS), required disclosures, and
  the top rejection causes. Wired into the `mobile` skill and `mobile-release-engineer`.

### Changed
- **Gate fix** — `integrity-check.py` now requires frontmatter only on `SKILL.md`, not on bundled
  `references/` (progressive-disclosure files), so skills can ship reference docs without tripping `/self-test`.
- Stopped tracking machine-local `.claude/settings.local.json` (now git-ignored).

## [1.1.0] — 2026-06-30

Web + mobile engineering layers, an agent/skill power-up, and a CI integrity gate.

### Added
- **Agent power-up** — all agents upgraded to first-class Claude Code subagents with
  least-privilege `tools:`, `color:`, `## When to invoke` worked scenarios, and a
  `## When blocked / recovery` contract.
- **Web engineering layer** — `.claude/orchestration/web-routing-matrix.md`; commands `/web-audit`,
  `/web-readiness`; checklist `web-production`; agents `codebase-mapper`,
  `playwright-e2e-engineer`, `refactoring-specialist`, `bug-fix-specialist`,
  `auth-permission-reviewer`.
- **Mobile engineering layer** — `.claude/orchestration/mobile-routing-matrix.md`; commands
  `/mobile-audit`, `/store-readiness`; checklists `mobile-production`, `app-store-readiness`;
  agents `mobile-security-auditor` (MASVS), `mobile-release-engineer`, `mobile-e2e-engineer`;
  preset `telegram-mini-app`.
- **Bundled skill tooling** — `project-classification/scripts/detect_stack.py` and
  `testing/scripts/detect_test_runner.py`, each with an `evals/` set.
- **CI gate** — `.github/workflows/self-test.yml` runs the integrity check on push/PR.

### Changed
- Universal `.claude/orchestration/routing-matrix.md` now detects web vs mobile vs mixed and loads
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

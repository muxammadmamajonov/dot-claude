# AGENTS.md — entry point for any AI coding agent

This repository is the **Universal `.claude` AI Project Operating System** — a reusable, safe,
copy-into-any-project operating system for AI-assisted software delivery (web · mobile · desktop ·
backend · and more). This file is the cross-tool entry point: **Claude Code, Codex, Cursor, Gemini CLI,
Copilot CLI, opencode**, and any agent that reads an `AGENTS.md` should start here.

## Source of truth
The authoritative operating rules live in **[`.claude/CLAUDE.md`](.claude/CLAUDE.md)** — the constitution:
the 9-stage flow (classify → interview → select → spec → build → audit → readiness → launch → continue),
the Definition of Done, and the hard safety rules (§8). **Read it first and obey it regardless of which
tool you are.** This `AGENTS.md` is a thin pointer, not a second rulebook.

## How each tool consumes this system

| Layer | Claude Code (the `claude` CLI: interactive + headless) | Other agents (Codex / Cursor / Gemini / Copilot / opencode) |
|---|---|---|
| `.claude/CLAUDE.md` constitution | ✅ auto-loaded | ✅ read it as your operating instructions |
| `.claude/skills/<name>/SKILL.md` | ✅ native Agent Skills | ✅ portable — the Agent Skills format is cross-tool; load on demand, or read as procedure |
| `.claude/checklists`, `templates`, `stack-matrix`, `presets`, `docs`, `orchestration` | ✅ referenced by agents | ✅ fully portable — plain-markdown playbooks any agent or human can apply |
| `.claude/agents/*.md` (subagents) | ✅ native dispatch | ⚠️ read as role briefs; replicate via your tool's own subagent/role mechanism |
| `.claude/commands/*.md` (slash commands) | ✅ native `/command` | ⚠️ read as runnable workflows; invoke their steps manually or via your tool's command system |
| `.claude/settings.json` + `.claude/hooks/*.json` | ✅ native permissions + hooks | ⚠️ Claude Code schema — re-express the deny/ask rules and guards in your tool's config |
| `.claude/scripts/integrity-check.py` | ✅ via `/self-test` | ✅ run directly: `python3 .claude/scripts/integrity-check.py` |

**Rule of thumb:** the *methodology* (CLAUDE.md, skills, checklists, templates, docs, routing maps) is
portable to every tool. The *execution wiring* (subagent dispatch, slash commands, hooks, settings) is
Claude Code-native; in other tools, treat those files as the spec and reproduce their intent with your
own mechanism.

## Quick start
- **Claude Code:** open the project and run `/start-project` (new), `/route` (assemble the minimal team),
  or `/continue-work` (existing). Platform layers: `/web-audit`, `/mobile-audit`, `/desktop-audit` and
  their `*-readiness` ship gates.
- **Any other agent:** read `.claude/CLAUDE.md`, then `.claude/orchestration/routing-matrix.md` to pick
  the right specialists/checklists for the task, and follow the relevant `.claude/skills/*/SKILL.md`.

## Safety (applies in every tool)
The §8 hard constraints in `.claude/CLAUDE.md` are tool-independent: read before write; least privilege;
never expose secrets; human-in-the-loop for irreversible actions; headless/scheduled runs are
read/review-only by default. Honor them even where a tool can't enforce them mechanically.

## Learn more
[`README.md`](README.md) (overview) · [`PROJECT_OS.md`](PROJECT_OS.md) (architecture) ·
[`.claude/docs/CLAUDE_CODE_OPERATING_MODEL.md`](.claude/docs/CLAUDE_CODE_OPERATING_MODEL.md) (runtime
capabilities + the portability matrix) · [`SECURITY.md`](SECURITY.md).

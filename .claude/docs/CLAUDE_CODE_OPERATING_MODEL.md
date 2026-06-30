# Claude Code Operating Model — how this OS drives the runtime

This is the umbrella for the **operating-capabilities layer**: how the Universal `.claude`
Project OS uses Claude Code's runtime — Terminal, Memory, Commands, Custom Commands, Skills,
MCP, Subagents, Hooks, Headless mode, and Routines — as one coherent, safe system. It is the
piece that makes this `.claude/` tree feel like an **operating system**, not a folder of
prompts.

> This document is part of the **portable payload**: it lives in `.claude/docs/` and travels
> with the system into every project. A thin pointer also exists at `docs/CLAUDE_CODE_OPERATING_MODEL.md`.

The hard safety constraints in `.claude/CLAUDE.md` §8 are law; nothing here weakens them. The
9-stage flow (`.claude/CLAUDE.md` §2) is the spine; these capabilities are *how* the orchestrator
executes each stage.

## The ten capabilities at a glance

| # | Capability | What it is | Deep doc / artifacts |
|---|---|---|---|
| 1 | **Terminal** | The substrate — how Claude inspects, edits, tests, and reports on a repo safely. | `.claude/skills/terminal-operations/SKILL.md`; guards in `.claude/settings.json` + `.claude/hooks/` |
| 2 | **Memory** | Continuity across sessions — project memory vs docs-as-memory vs user/global memory. | `.claude/docs/MEMORY_STRATEGY.md`, `.claude/skills/memory-management/SKILL.md` |
| 3 | **Commands** | Built-in invokable workflows (the 9-stage commands + gates). | `.claude/commands/*` |
| 4 | **Custom commands** | New repeatable workflows added to `.claude/commands/`. | `.claude/commands/brainstorm-project.md`, `commit-ready.md`, `create-github-issues.md`, … |
| 5 | **Skills** | Repeatable *procedures* an agent invokes (the "how"). | `.claude/skills/*` |
| 6 | **MCP** | Reach into real tools/data (DB, GitHub, monitoring) under least privilege. | `.claude/docs/MCP_STRATEGY.md`, `.claude/skills/mcp-integration/SKILL.md`, `.claude/checklists/mcp-safety.md` |
| 7 | **Subagents** | Parallel fan-out — the orchestrator dispatches non-conflicting work and reconciles it. | `.claude/docs/SUBAGENT_ORCHESTRATION.md` |
| 8 | **Hooks** | Mechanical, safe-by-default enforcement of §8. | `.claude/docs/HOOKS_SAFETY_MODEL.md`, `.claude/hooks/*` |
| 9 | **Headless** | Unattended read/review runs in CI. | `.claude/docs/HEADLESS_AND_ROUTINES.md`, `.claude/checklists/headless-ci.md` |
| 10 | **Routines** | Scheduled headless runs — report-first, approval-gated. | `.claude/docs/HEADLESS_AND_ROUTINES.md`, `.claude/checklists/routine-safety.md` |

## How they interlock (the integration story)

- **Terminal is the substrate.** Every other capability ultimately touches the repo through the
  terminal/file tools. `terminal-operations` defines the safe loop: *inspect → understand → edit
  small → test/lint/build → report changed files → never expose secrets*. The `.claude/settings.json`
  deny/ask rules and the `.claude/hooks/` guards backstop it mechanically.
- **Memory is continuity.** Decisions, assumptions, architecture history, and known risks live in
  `docs/` as long-term memory; project conventions live in `CLAUDE.md`; the orchestrator's run-state
  lives in `docs/state/`. `/continue-work` rehydrates from there. See `MEMORY_STRATEGY.md`.
- **Commands + Skills are invocation.** A command is the *trigger* (with stop conditions and a final
  report); a skill is the *procedure* it follows. Commands stay thin; skills hold the method.
- **MCP is reach.** When a task needs a real database, issue tracker, or cloud API, the OS proposes an
  MCP server — never assuming one exists, always least-privilege, always documenting the dependency.
- **Subagents are parallelism.** The orchestrator fans out independent work (discovery spikes, the four
  audit gates, disjoint build slices), then **collects → dedupes → resolves conflicts → emits one plan**.
- **Hooks are enforcement.** They turn §8 from a promise into a mechanism: blocking destructive commands,
  guarding migrations and prod files, scanning for secrets. Safe-by-default, opt-in.
- **Headless is unattended review.** The OS runs read-only in CI — audits, readiness checks, issue lists —
  converting interactive STOP-gates into recorded assumptions, failing closed on any §8 violation.
- **Routines are scheduled headless.** Recurring audits/reviews that **report and recommend first** and
  require explicit approval before any change. No unsupervised destructive or production actions.

## The safety spine (applies to all ten)

1. **Read before write.** Understand before changing. Reversible, incremental steps only.
2. **Least privilege, least blast radius.** Narrowest scope that does the job; non-prod by default.
3. **Never expose secrets.** Reference secrets by location; never print, log, commit, or transmit them.
4. **Human-in-the-loop for the irreversible.** Destructive/production/business-critical actions stop and ask.
5. **Read/review-only by default for autonomy.** Headless and routines do not write or destroy unless a
   human has explicitly opted in with a tested rollback.
6. **Never assume external access.** If an MCP server, credential, or tool is needed and absent, ask the
   user to configure it — do not fabricate or work around it.
7. **Document the why.** Every non-trivial decision → assumptions log / decision record (`.claude/CLAUDE.md` §7).

## Cross-tool portability (Claude Code vs other agents)

"Claude Code" and the "Claude CLI" are the **same runtime** (the `claude` binary — terminal, IDE,
desktop, web). Everything in this OS is built in Claude Code's native conventions and runs there in
**both interactive and headless modes** (`claude -p`, the Agent SDK, CI, cron). No conversion is needed
for Claude Code. The cross-tool entry point for *other* agents is the root `AGENTS.md` (+ `GEMINI.md`).

**Portability matrix** — what executes natively vs what travels as portable reference:

| Layer | Claude Code (interactive + headless CLI) | Codex / Cursor / Gemini / Copilot / opencode |
|---|---|---|
| `CLAUDE.md` constitution | native (auto-loaded) | read as operating instructions (via `AGENTS.md`) |
| `skills/<name>/SKILL.md` (+ scripts/evals) | native Agent Skills | portable — Agent Skills is a cross-tool format; else read as procedure |
| `checklists` / `templates` / `stack-matrix` / `presets` / `docs` / `orchestration` | referenced by agents | fully portable plain-markdown playbooks |
| `agents/*.md` subagents | native dispatch | read as role briefs; reproduce via the tool's own subagent mechanism |
| `commands/*.md` slash commands | native `/command` | read as runnable workflows; invoke steps manually / via the tool's commands |
| `settings.json` + `hooks/*.json` | native permissions + hooks | re-express deny/ask + guards in the tool's own config |
| `scripts/integrity-check.py` | native (`/self-test`) | run directly with `python3` |

**Principle:** the *methodology* is portable everywhere; only the *execution wiring* (subagent dispatch,
slash commands, hooks, settings) is Claude Code-specific. In another tool, treat those four as the spec
and reproduce their intent. The safety spine (above) is tool-independent and applies regardless.

## Where to go next

- Driving a terminal safely → `.claude/skills/terminal-operations/SKILL.md`
- Deciding where information lives → `.claude/docs/MEMORY_STRATEGY.md`
- Connecting real tools → `.claude/docs/MCP_STRATEGY.md`
- Running many agents at once → `.claude/docs/SUBAGENT_ORCHESTRATION.md`
- Mechanical safety → `.claude/docs/HOOKS_SAFETY_MODEL.md`
- CI and scheduled automation → `.claude/docs/HEADLESS_AND_ROUTINES.md`

These capabilities are wired into the conductor in `.claude/agents/core/orchestrator.md`
(see its *Concurrency & conflict resolution* and *Tools & resources* sections) and summarized
for every project in `.claude/CLAUDE.md` §11.

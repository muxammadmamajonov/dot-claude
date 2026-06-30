# GEMINI.md — pointer for Gemini CLI

This project's operating instructions are defined once, tool-independently, in
**[`.claude/CLAUDE.md`](.claude/CLAUDE.md)** (the constitution) with the cross-tool entry point in
**[`AGENTS.md`](AGENTS.md)**. Read both, then follow them.

- **Pick the team for a task:** `.claude/orchestration/routing-matrix.md` (and the `web-`, `mobile-`,
  `desktop-routing-matrix.md` layers) map a project type to its minimal set of specialists and checklists.
- **Procedures:** `.claude/skills/<name>/SKILL.md` — load on demand. Activate the relevant skill the way
  Gemini CLI activates skills.
- **Reference playbooks:** `.claude/checklists/`, `.claude/templates/`, `.claude/stack-matrix/`,
  `.claude/presets/`, `.claude/docs/` are plain markdown — apply them directly.
- **Execution wiring** (`.claude/agents/`, `.claude/commands/`, `.claude/hooks/`, `.claude/settings.json`)
  is Claude Code-native; in Gemini CLI, read those files as the spec and reproduce their intent with
  Gemini's own subagent/command/permission mechanisms.

**Tool-name mapping:** the system is written in Claude Code tool names (Read, Write, Edit, Grep, Glob,
Bash, Task). Map them to your Gemini CLI equivalents when following a procedure.

**Safety:** the §8 hard constraints in `.claude/CLAUDE.md` apply regardless of tool — read before write,
least privilege, never expose secrets, human-in-the-loop for irreversible actions.

---
name: cli
description: >
  Activate when building, extending, or packaging a command-line interface tool
  or terminal utility — scripting tools, developer CLIs, data-processing pipes,
  ops automation, or any program invoked from a shell. Applies to Node.js
  (Commander, Oclif, Yargs), Python (Click, Typer, argparse), Go (Cobra), Rust
  (Clap), Ruby (Thor), or shell scripts. Do NOT activate for backend services
  that happen to have a CLI entrypoint (use .claude/skills/backend/SKILL.md for
  the service; combine with this skill for the CLI layer).
---

# CLI Tool Skill

## When to use

- Building a new CLI tool or developer utility from scratch
- Adding subcommands, flags, interactive prompts, or config file support
- Improving error messages, help text, or shell completion
- Packaging and distributing a CLI (npm, PyPI, Homebrew, GitHub Releases, Scoop)
- Profiling slow CLI startup or command execution

---

## Workflow

1. **Classify the project** — Read `docs/specs/product.md` to confirm target users (developers, ops, end users), distribution method, and whether the tool is a standalone binary, a language-specific package, or a plugin to an existing CLI ecosystem.

2. **Design the command interface before coding**
   - Sketch the full command tree: `tool <resource> <verb> [flags]`
   - Prefer noun-verb ordering (`tool user create`) over verb-noun (`tool create-user`) for tools with many resources
   - Map every flag to a single responsibility; avoid flags that change a command's fundamental behaviour
   - Document the interface in `docs/cli-reference.md` first; implement second

3. **Choose the parsing library**
   | Language | Production-grade choice |
   |---|---|
   | Node.js | Oclif (rich plugin ecosystem), Commander.js (simple), Yargs (flexible) |
   | Python | Typer (type-safe + auto-help), Click (battle-tested) |
   | Go | Cobra + pflag (k8s-style CLIs) |
   | Rust | Clap with derive macros |
   | Ruby | Thor |
   Match the library's conventions — don't fight its model.

4. **Implement argument and flag handling**
   - Required positional args: document clearly, give an actionable error when missing
   - Optional flags: provide sensible defaults; document defaults in `--help`
   - Global flags: `--help`, `--version`, `--config`, `--output` (format), `--quiet`, `--verbose`
   - Environment variable overrides: every flag should be settable via `TOOL_FLAG_NAME=value`; document the precedence order (flag > env var > config file > default)

5. **Implement config file support** — Load from standard OS locations:
   - macOS/Linux: `~/.config/<tool>/config.yaml` or `~/.toolrc`
   - Windows: `%APPDATA%\<tool>\config.yaml`
   - Project-local override: `.toolconfig` or `.tool.yaml` in the current directory
   Use a library (cosmiconfig, dynaconf, Viper) rather than hand-rolling config search.

6. **Design output for humans and machines**
   - Default: human-readable with colour (when stdout is a TTY)
   - `--output json`: machine-parseable; stable key names
   - `--output table`: aligned columns for tabular data
   - `--quiet`: suppress all output except errors
   - Detect TTY: when `stdout` is piped, suppress colour and progress bars automatically (`chalk.level`, `isatty`)

7. **Implement interactive prompts sparingly** — Prompts block automation. Use them only when no flag can reasonably be provided (e.g. first-run wizard, destructive confirmation). Never prompt if `--yes` or `--non-interactive` is passed. Use `inquirer`, `prompts`, `questionary`, or `dialoguer`.

8. **Handle errors gracefully**
   - Print a clear, actionable error message to `stderr` (not stdout)
   - Exit with a meaningful code: `0` success, `1` general error, `2` misuse/bad args, `3+` domain-specific
   - Suggest the fix: "Unknown flag --versbose. Did you mean --verbose?"
   - Never print a raw stack trace to end users; log it to a debug file or only when `--debug` is set

9. **Add shell completion** — Generate completion scripts for bash, zsh, fish, and PowerShell. Register the `completion` subcommand: `tool completion bash >> ~/.bashrc`. Most frameworks (Cobra, Oclif, Click) generate these automatically.

10. **Write tests**
    - Unit: flag parsing, config loading, output formatters
    - Integration: spawn the CLI as a subprocess and assert on stdout/stderr/exit code
    - Test both `--output json` and human output on key commands
    Reference `.claude/checklists/qa.md`.

11. **Package for distribution**
    - Node.js: publish to npm; add a `bin` entry in `package.json`; install globally or via `npx`
    - Python: publish to PyPI; use `pyproject.toml` with `[project.scripts]`; use `pipx` for isolated installs
    - Go / Rust: cross-compile for `linux-amd64`, `linux-arm64`, `darwin-amd64`, `darwin-arm64`, `windows-amd64`; publish binaries to GitHub Releases; provide a Homebrew formula and Scoop manifest
    - All: provide a one-line install snippet in `README.md`

12. **Measure and optimise startup time** — A CLI that takes > 500 ms to start feels slow. Profile with `node --prof` (Node.js), `py-spy` (Python), or `samply` (Rust/Go). Common culprits: loading all modules at startup, heavy `require`/`import`, slow network calls at init.

---

## Standards

**Do**
- Write `--help` text that explains what the command does, lists all flags with defaults, and shows a usage example.
- Print progress to `stderr`, final output to `stdout` — this keeps pipes clean.
- Validate all flags and args before starting any side-effectful work.
- Support `--dry-run` on any command that modifies files, network resources, or external services.
- Write a `CHANGELOG.md` and respect semantic versioning (`major.minor.patch`).
- Respect `NO_COLOR` environment variable (disable colour output when set).

**Do not**
- Prompt in a non-interactive context (CI, piped stdin) — check for TTY and require explicit flags instead.
- Write to files outside the current directory without explicit user consent.
- Execute arbitrary shell commands from user-supplied strings (command injection risk).
- Hard-code API keys or tokens in the binary; read from env vars or the config file.
- Add `sudo`-requiring steps to install scripts without clearly documenting why.
- Output progress or spinner frames to stdout when it will break downstream parsing.

---

## Common mistakes to avoid

- **Unclear error on missing args** — `Error: undefined` is useless; print "Missing required argument <name>. Usage: tool command <name>".
- **Colour codes in piped output** — always strip ANSI codes when stdout is not a TTY; piped output into `grep` or `jq` breaks otherwise.
- **No `--version` flag** — users need to report their version in bug reports; implement it from day one.
- **Config and flag precedence surprises** — document the order; a flag that silently wins over a config file key (or vice versa) confuses users.
- **Slow startup from eager imports** — loading database clients or HTTP libraries at module load time even for unrelated subcommands; use lazy-loading.
- **Breaking changes without a major version bump** — changing a flag name, removing a subcommand, or altering JSON output shape breaks scripts; treat as semver-major.
- **Not flushing stdout before exit** — some runtimes buffer stdout; call `process.stdout.write` + explicit flush or use synchronous write before `process.exit()`.

---

## Output format

A production-ready CLI project should include:

```
/
├── src/ (or cmd/, lib/)
│   ├── commands/       # One file per top-level command/subcommand
│   ├── config/         # Config file loading and validation
│   ├── output/         # Formatters (table, json, plain)
│   └── utils/          # Shared helpers
├── tests/
│   ├── unit/
│   └── integration/    # Subprocess-based end-to-end tests
├── docs/
│   └── cli-reference.md   # Full command/flag reference (auto-generated or hand-written)
├── scripts/
│   └── install.sh      # One-line installer (optional)
├── .env.example        # Supported env var overrides
├── CHANGELOG.md
└── README.md           # Install, quickstart, config, all commands summary
```

---

## Related checklists

- `.claude/checklists/security.md`
- `.claude/checklists/qa.md`
- `.claude/checklists/production.md`

## Related agents

- `.claude/agents/core/orchestrator.md`
- `.claude/agents/quality/security-auditor.md`

# Command-Line Tool Preset

## Project type
Program invoked from a shell — terminal, shell script, CI pipeline, or build system. Variants: interactive TUI (terminal UI with navigation), non-interactive batch processor, REPL, shell plugin/completion provider, build tool plugin, devops utility, data transformation tool, or SDK/framework CLI companion. May be distributed as a binary, npm/pip/cargo/brew/apt package, or Docker image.

## Typical use cases
- Developer tools (code generators, linters, formatters, test runners)
- Infrastructure and DevOps utilities (deployment, secret rotation, cluster management)
- Data processing pipelines (ETL, log parsing, report generation)
- SDK companion CLIs (authenticate, scaffold, deploy, diagnose)
- Interactive TUIs (dashboards, database explorers, log streamers)
- Automation scripts promoted to first-class distributable tools

## Required discovery questions
1. Who are the primary users — developers running interactively, CI pipelines running non-interactively, or both? How does that affect flag design and exit codes?
2. What platforms must be supported — macOS, Linux, Windows (WSL only or native CMD/PowerShell)?
3. What is the distribution method — npm/pip/cargo package, GitHub release binary, Homebrew tap, OS package manager (apt/rpm), or Docker image?
4. Does the tool need authentication to external services? If yes, how should credentials be stored (env vars, OS keychain, config file, token file)?
5. Are there subcommand groupings expected to grow (git-style `tool <command> <subcommand>`)? What is the expected command surface at v1 vs. v2?
6. Does the tool modify state — files on disk, remote resources, databases? If yes, what confirmation, dry-run, and rollback mechanisms are required?
7. Should the tool support configuration files (e.g. `.mytoolrc`, `mytool.yaml`) in addition to flags? What is the resolution order (project → user home → system)?
8. Is machine-readable output required (JSON, CSV, NDJSON) for piping into other tools or CI systems?
9. Does the tool need interactive prompts, progress bars, or live-updating displays (requires TTY detection)?
10. What are the self-update or version-pinning expectations? Should it check for new versions automatically?

## Recommended agents

### Core
- `.claude/agents/core/orchestrator.md` — command surface planning, breaking-change governance
- `.claude/agents/core/solution-architect.md` — plugin architecture, config resolution, error model
- `.claude/agents/core/project-manager.md` — command delivery phasing

### Engineering
- `.claude/agents/engineering/backend-engineer.md` — argument parsing, output formatting, TTY detection
- `.claude/agents/engineering/backend-engineer.md` — external API calls, file I/O, process management
- `.claude/agents/engineering/backend-engineer.md` — credential storage, token refresh in headless environments

### Quality
- `.claude/agents/quality/qa-engineer.md` — cross-platform shell testing, piping and stdin/stdout tests
- `.claude/agents/quality/security-auditor.md` — credential handling, shell injection prevention, file permission checks

### Domain
- `.claude/agents/core/documentation-writer.md` — man page, help text standards, changelog
- `.claude/agents/engineering/release-engineer.md` — binary release, package registry publishing, install script

## Recommended skills
- `.claude/skills/cli/SKILL.md` — argument parsing, help text, exit codes, TTY detection
- `.claude/skills/security/SKILL.md` — OS keychain, `~/.netrc`, environment variable conventions
- `.claude/skills/security/SKILL.md` — shell injection, file permission, credential exposure
- `.claude/skills/testing/SKILL.md` — golden-file testing, snapshot testing, subprocess integration tests
- `.claude/skills/devops/SKILL.md` — cross-platform binary builds, package registry CI/CD
- `.claude/skills/production-readiness/SKILL.md` — debug logging (`-v` / `--verbose`), structured error output

## Recommended stack options

| Stack | Rationale |
|---|---|
| **Go (Cobra + Viper)** | Produces single static binaries for all platforms; fast startup; excellent stdlib; Cobra is the de facto Go CLI framework. See `.claude/stack-matrix/backend.md` |
| **Rust (clap + tokio)** | Best raw performance; memory safety; rich async ecosystem; great for data-heavy or system-level tools |
| **Node.js + TypeScript (oclif or commander)** | Ideal when the tool integrates tightly with JS/TS ecosystems or needs npm distribution; watch cold-start time |
| **Python (Typer / Click)** | Best for ML/data-adjacent tools or when the team is Python-primary; use PyInstaller or Nuitka for single-binary distribution |

Reference `.claude/stack-matrix/backend.md` for detailed tradeoffs on startup time, binary size, and cross-compilation.

## Required checklists
- `.claude/checklists/security.md` — credential handling, shell injection, file permission
- `.claude/checklists/launch.md` — binary signing, package registry publishing, install script safety
- `.claude/checklists/qa.md` — help text completeness, exit codes, `--dry-run`, `--quiet` / `--json`
- `.claude/checklists/qa.md` — path separators, line endings, case sensitivity, permission models

## MVP scope pattern

**In MVP**
- Primary command(s) with `--help` text on every command and flag
- Consistent exit codes: `0` success, `1` usage error, `2` runtime error
- `--version` flag
- Basic error messages to stderr, output to stdout
- At least `--json` output mode for CI/scripting use
- `--dry-run` for any destructive operation
- README with install instructions and quickstart

**Deferred to v2**
- Shell completion (bash/zsh/fish/PowerShell)
- Plugin system for extensibility
- Interactive TUI mode (if initially non-interactive)
- Auto-update / version check
- Configuration file schema and validation
- Telemetry / anonymous usage analytics (opt-in only)
- Aliases and command shortcuts

## Production risks

| Risk | Severity | Mitigation |
|---|---|---|
| Credentials written to shell history or log files | P0 | Never accept passwords via flag; use env vars or interactive prompt with `noecho`; redact tokens in debug output |
| Shell injection via user-supplied strings in `exec` calls | P0 | Never pass user strings to shell (`sh -c`); use `exec` with explicit arg arrays; validate and allowlist shell-unsafe characters |
| Destructive operations with no confirmation or dry-run | P0 | `--dry-run` required on any write/delete; interactive confirmation prompt when stdout is a TTY; `--yes` flag only for CI contexts |
| Non-zero exit on success confusing CI pipelines | P0 | Reserve exit `0` for success; document all non-zero codes; never exit with uncaught exceptions |
| Sensitive data written to `~/.mytool/` with world-readable permissions | P0 | `chmod 600` config/token files on creation; warn if directory permissions are too open |
| Binary not signed — OS security warnings on macOS/Windows | P1 | Sign with Apple Developer / Microsoft code-signing certificate in CI; Gatekeeper notarisation for macOS |
| Startup time > 1 s degrading developer experience | P1 | Profile and defer non-critical imports; avoid heavy framework load at startup; benchmark cold start in CI |
| `--force` flag with no scope guard deletes unintended targets | P1 | Require explicit target alongside `--force`; print a summary of what will change before executing |
| Breaking changes in minor versions breaking scripts | P1 | Semver strictly; deprecation warning period before removing flags; maintain `CHANGELOG.md` |
| No `--quiet` mode — noisy in CI logs | P2 | `--quiet` suppresses info/progress; only errors and output reach stdout/stderr |

## Launch requirements
- Help text reviewed for every command and flag — no missing descriptions
- Exit codes tested in CI via shell assertion
- Binary tested on all supported platforms (matrix CI job)
- Package published to target registry (npm, crates.io, PyPI, Homebrew) with install instructions verified on a fresh machine
- Credentials and sensitive flags do not appear in `ps aux` output or shell history
- `--dry-run` confirmed working for all destructive operations
- README includes install, quickstart, and common examples
- `CHANGELOG.md` initialised with v1.0.0 entry
- Signed binary (macOS notarised, Windows Authenticode) if distributed to external users

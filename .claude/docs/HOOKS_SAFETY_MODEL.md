# Hooks Safety Model — mechanical enforcement of the constitution

Hooks turn `.claude/CLAUDE.md` §8 from a promise the agent *should* keep into a mechanism the runtime
*enforces*. They run on tool events (PreToolUse, PostToolUse) and can warn or block. This document
defines the safety model every hook in `.claude/hooks/` follows, and how to enable them.

## Two layers of protection

1. **Always-on baseline — `.claude/settings.json`.** `permissions.deny` blocks irreversible commands
   (`rm -rf`, force-push, history rewrite, `mkfs`, `truncate`, `redis-cli FLUSHALL`, secret-file reads, …);
   `permissions.ask` gates pushes, publishes, deploys, migrations, package installs, remote-exec runners
   (`npx`/`bunx`/`pnpm dlx`/`uvx`), DB CLIs (`psql`/`mysql`/`mongosh`), and git working-tree data-loss
   (`checkout --`/`restore`/`stash drop`). These apply with no setup.
2. **Opt-in hooks — `.claude/hooks/*.json`.** Each hook is an example you activate by copying its `hooks`
   block into `.claude/settings.json`. They add **content/regex** coverage that prefix-based permission rules
   cannot express (e.g. a `DROP TABLE` buried mid-command).

## Safe-by-default — the rules every hook obeys

- **Block or warn only — never mutate.** A hook may print to stderr and `exit 2` (block) or `exit 0` (pass).
  It never edits files, never installs anything, never deletes anything, never runs a destructive command.
- **Never expose secrets.** A hook may report *that* a secret was detected; it never echoes the value.
- **Read the event from stdin** (`in=$(cat); printf '%s' "$in" | grep …`) rather than acting blind.
- **Fail open on its own errors** for advisory hooks (a broken reminder must not break the workflow); fail
  **closed** (block) for safety-critical guards when the pattern matches.
- **Opt-in.** Nothing is enabled by default; the user consciously activates each hook. The `description`
  states what it does and any side-effect of enabling it.

## The hook catalogue

| Hook | Event | Action | Notes |
|---|---|---|---|
| `dangerous-command-guard.json` | PreToolUse(Bash) | **block** | Regex for `rm -rf`, force-push, `DROP/TRUNCATE/DELETE FROM` (incl. `psql -c` wrappers), `git checkout --`/`restore`/`stash drop`, `find … -delete`, `chmod 777`, fork-bombs |
| `package-install-guard.json` | PreToolUse(Bash) | **block/warn** | Blocks remote pipe-to-shell (`curl … \| sh`); warns on installs |
| `secret-scan.json` | PreToolUse(Bash) | **block** | Blocks a `git commit` whose staged diff contains a secret; reports *that*, never the value |
| `migration-safety-guard.json` | PreToolUse(Edit/Write/Bash) | **block** | Blocks edits/deletes of existing DB migrations (§8) — create a forward migration instead |
| `production-file-guard.json` | PreToolUse(Edit/Write) | **warn/block** | Cautions when touching `.env*`, `*.tf`, `k8s`/`helm`, prod manifests, deploy CI configs |
| `pre-commit-check.json` | PreToolUse(Bash) | **block** | Runs the project test suite before commit — **note:** auto-executes project test code; enable only in trusted repos |
| `pre-deploy-check.json` | PreToolUse(Bash) | **block (speed-bump)** | Pauses before a deploy command |
| `post-edit-check.json` | PostToolUse(Edit/Write) | **warn** | Reminds to lint/typecheck after edits — never blocks, never mutates |
| `docs-sync-check.json` | PostToolUse(Edit/Write) | **warn** | Reminds to update docs when code changes — never blocks |

`post-edit-check` and `docs-sync-check` are the only two safe to enable blindly (pure advisory). The
blocking guards are conservative but **prefix/regex matching cannot catch every obfuscation** (spacing,
shell vars, base64) — they are a backstop, not a sandbox. The agent must still respect §8 directly.

## How to enable a hook

1. Open the hook's JSON; copy its `hooks` block.
2. Merge it into `.claude/hooks` in `.claude/settings.json` (combine arrays if a block already exists).
3. Re-read the `description` for any side-effect (e.g. `pre-commit-check` runs your tests).
4. Test on a throwaway command before relying on it.

## Recommended-on set

For most projects, enabling `dangerous-command-guard` + `secret-scan` + `migration-safety-guard` +
`production-file-guard` gives strong always-on protection with no destructive behavior. Enable
`pre-commit-check`/`pre-deploy-check` only where their auto-run behavior is acceptable (trusted repo / CI).

## Related

- Constitution: `.claude/CLAUDE.md` §8
- Baseline: `.claude/settings.json`
- Operating model: `.claude/docs/CLAUDE_CODE_OPERATING_MODEL.md`
- Headless safety (where no human is present to approve): `.claude/docs/HEADLESS_AND_ROUTINES.md`

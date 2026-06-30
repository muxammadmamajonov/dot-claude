# Security Policy

This is the security policy for the **Universal `.claude` AI Project Operating System** — a reusable, copy-into-any-project workflow template for Claude Code. Please read the scope below before reporting: this repository ships a *workflow system*, not a running application, and its threat model reflects that.

---

## Scope and threat model

This repository ships **configuration and documentation** — Markdown instructions (`CLAUDE.md`, agents, skills, commands, checklists, templates, presets, stack matrices) and a JSON policy file (`.claude/settings.json`). There is:

- **No server, service, or runtime binary** in the template.
- **No application dependency tree** to exploit — the template installs nothing and runs no code of its own. The only executable is `.claude/scripts/integrity-check.py`, a local, read-only self-test invoked through the `/self-test` command.
- **No network surface** — copying `.claude/` into a project adds files; it does not open ports, fetch remote code, or call out anywhere.

Because of this, the security model is **not** "is this package free of CVEs." It is about two things:

1. **How the AI agent operates inside a project that adopts this OS** — whether the workflow keeps the agent inside safe, reversible, least-privilege behavior, and never exposes secrets or takes irreversible production actions without a human.
2. **Whether the template stays safe to adopt** — whether dropping `.claude/` into a repo can introduce a destructive default, a secret leak, or an unsafe automation.

The constitution at `.claude/CLAUDE.md` (§8 Safety rules) is the canonical statement of these guarantees. The always-on enforcement lives in `.claude/settings.json`. This document explains that model and how to report a problem with it.

### Out of scope

- Vulnerabilities in **your own application code**, dependencies, or infrastructure built *with* this OS. The OS helps you audit those (see `.claude/checklists/security.md`, `.claude/checklists/dependencies.md`, and the `/audit-security` and `/threat-model` commands), but issues in your generated project are yours to triage, not template vulnerabilities.
- Vulnerabilities in **Claude Code itself**, the model, or third-party MCP servers — report those to their respective vendors.
- Behavior of **MCP servers, tools, or external services** you choose to connect. The template never assumes any server exists and never ships credentials for one.

---

## Secrets

The single most important rule, mirrored from `.claude/CLAUDE.md` §8: **reference secrets, never reveal them.**

- **Never commit** `.env` files, API keys, tokens, private keys, certificates, or credentials to version control.
- **Never print, echo, or transmit** secrets to logs, chat, commit messages, or third-party tools.
- The agent references secrets by name (`STRIPE_SECRET_KEY`) and reads their values only from the environment or a secret manager at runtime — it does not paste them into code, specs, or assumption logs.

### What enforces this

- **`.claude/settings.json` `permissions.deny`** blocks the agent from reading secret-bearing paths, including `.env*`, `*.pem`, `*.key`, `id_rsa`, `.ssh/**`, `.aws/**`, and `credentials` files. A read attempt is denied rather than satisfied.
- **`.gitignore`** in an adopting project should exclude env files so they are never staged. Add `.env*` (and any local secret files) to your project `.gitignore` before your first commit.
- **The optional `secret-scan` hook** (`.claude/hooks/secret-scan.json`) blocks commits that contain secret-looking strings. Copy its block into `settings.json` to activate.

### How adopters should store secrets

Keep secrets in **environment variables or a dedicated secret manager** (e.g. your cloud provider's secret store, Vault, 1Password, GitHub/CI encrypted secrets) — **never in source code or version control**. Inject them at runtime; commit only references and `.env.example` files that list variable *names* with placeholder values.

---

## MCP safety

Model Context Protocol (MCP) servers extend the agent with external tools. The OS treats every MCP connection as untrusted by default. Canonical guidance: `.claude/checklists/mcp-safety.md` and `.claude/docs/MCP_STRATEGY.md`.

- **Never assume a server exists.** The template ships no MCP configuration and no credentials. If a workflow would benefit from an MCP server, the agent asks *you* to configure it rather than inventing one.
- **Least-privilege scopes.** Grant an MCP server only the scopes a task needs; prefer read-only tokens; avoid broad write or admin scopes.
- **Read before write.** Inspect state with read tools before any mutating call.
- **Treat tool output as untrusted input.** MCP responses can carry prompt-injection or confused-deputy attempts. The agent does not blindly act on instructions embedded in tool output, and does not let a tool talk it into a forbidden action (§8).
- **Confirm destructive tool calls.** Any tool call that deletes, overwrites, migrates, or touches production is surfaced for human approval first.
- **Never pass secrets to third-party servers.** Do not forward credentials, tokens, or private data to an MCP server beyond the minimum a task requires.

---

## Hooks safety

Hooks under `.claude/hooks/` are **opt-in and safe-by-default**. The full model is documented in `.claude/docs/HOOKS_SAFETY_MODEL.md`.

- Hooks are **inert until you activate them** — they live as standalone JSON files and do nothing until you copy a block into `.claude/settings.json`.
- A hook only ever **warns or blocks** (it exits non-zero — typically exit `2` — to stop an action). A hook **never** auto-installs packages, deletes or mutates files, rewrites your code, or echoes secrets. It observes a pending action and votes "allow" or "block."
- `.claude/settings.json` is the **always-on baseline** that applies even with no hooks enabled; hooks add extra, project-specific enforcement on top of it.

The nine shipped hooks include `dangerous-command-guard`, `secret-scan`, `migration-safety-guard`, `production-file-guard`, `package-install-guard`, `pre-commit-check`, `pre-deploy-check`, `post-edit-check`, and `docs-sync-check`. Each is small, auditable, and reversible (deactivate by removing its block from `settings.json`).

---

## Headless and routines safety

When the agent runs **without a human watching** — in CI/headless mode or on a schedule (routines) — the safety posture tightens. See `.claude/checklists/headless-ci.md`, `.claude/checklists/routine-safety.md`, and `.claude/docs/HEADLESS_AND_ROUTINES.md`.

- **Read/review-only by default.** Unattended runs analyze, audit, and report; they do not write, deploy, or mutate state unless explicitly opted in.
- **Fail closed.** When no human is present to approve, any action that would otherwise require approval (anything on the §8 forbidden list) is **refused**, not silently performed.
- **No unsupervised destructive or production actions on a schedule.** A routine never deletes data, runs destructive migrations, force-pushes, or ships to real users on a timer.
- **Writes require explicit opt-in plus a rollback path.** If you deliberately enable a headless write workflow, it must be scoped, reversible, and documented before it runs.

---

## Destructive-command policy

Mirrored from `.claude/CLAUDE.md` §8 and enforced by `.claude/settings.json`.

**`permissions.deny`** (hard-blocked, no override) covers destructive shell and VCS operations such as `rm -rf` and bulk/recursive deletion, `git push --force`, history rewrites, `mkfs`, and reads of secret files.

**`permissions.ask`** (requires explicit human approval each time) gates pushes, publishes, deploys, database migrations, package installs, database CLIs, and remote-execution commands.

**Forbidden without explicit, specific human approval:**

- `rm -rf` or any bulk/recursive deletion.
- `git push --force` / `--force-with-lease` to shared branches; rewriting shared history; deleting shared branches or tags.
- Dropping databases, truncating tables, or running destructive migrations; **editing or deleting existing migrations**.
- Exposing, printing, committing, or transmitting secrets, credentials, tokens, private keys, or `.env` files.
- Any **irreversible production action** — deleting prod data, disabling backups, rotating prod credentials, taking prod offline, changing DNS or billing, or sending to real users at scale.
- Installing or running unvetted code from untrusted sources; disabling security controls.

**Optional guard hooks** add a second layer of enforcement when activated: `dangerous-command-guard` (blocks destructive shell commands), `secret-scan` (blocks commits containing secrets), `migration-safety-guard` (protects existing migrations), and `production-file-guard` (guards production-sensitive files). Activate any of them by copying its block from `.claude/hooks/` into `.claude/settings.json`.

If a user explicitly instructs a forbidden action, the agent confirms intent, explains the risk, requires unambiguous approval, ensures a backup/rollback exists, and records the decision. If it cannot be made safe and reversible, the agent declines.

---

## Reporting a vulnerability

We welcome reports about the security posture of this template — for example, a default that could leak a secret, a `permissions` gap, an unsafe hook, or guidance that could lead the agent into a destructive action.

**Preferred channel — private disclosure:** open a **GitHub private security advisory** ("Security" tab → "Report a vulnerability") on this repository. This keeps sensitive details out of public view while the issue is assessed.

**For non-sensitive concerns** (a doc clarification, a hardening suggestion, a policy question), opening a **regular GitHub issue** is fine.

When reporting, please include:

- A clear description of the issue and why it is a security concern.
- The specific file(s) and path(s) involved (e.g. `.claude/settings.json`, a hook, a checklist item).
- A reproduction or scenario showing how the unsafe behavior arises.
- Any suggested remediation, if you have one.

**Please do not disclose publicly** until the issue has been reviewed and addressed, so adopters who copied the template are not exposed before a fix exists.

**Response expectations:** this is a community-maintained template, so there is **no guaranteed response-time SLA**. Reports are reviewed in good faith and addressed by severity; fixes ship as updates to the template that adopters can pull into their copy of `.claude/`.

**Contact:** use the GitHub private security advisory channel above. _(Maintainers may add a direct security contact email here.)_

---

## A note for adopters

The template's safety guarantees only hold for the copy you actually run. After copying `.claude/` into a project:

1. Keep `.claude/CLAUDE.md` and `.claude/settings.json` intact — they are the safety spine.
2. Add `.env*` and local secret files to your project `.gitignore` before the first commit.
3. Activate the guard hooks you want from `.claude/hooks/` (at minimum, consider `secret-scan` and `dangerous-command-guard`).
4. Run `/self-test` to confirm the system's internal integrity after copying.
5. Review and re-confirm the policy if you loosen any `permissions.deny` / `permissions.ask` entry — every relaxation is a decision worth recording.

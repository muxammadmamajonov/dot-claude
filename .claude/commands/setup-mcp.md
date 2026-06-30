---
description: Propose, scaffold, and validate MCP server configuration for the current project; write docs/state/mcp-plan.md plus a proposed (commented) .mcp.json with credential placeholders only — never secrets.
argument-hint: [server-name — optional, scope the plan to one server; default: all recommended]
---

# /setup-mcp

## Purpose
Decide which Model Context Protocol (MCP) servers this project would genuinely benefit from, then produce a reviewable plan and a *proposed* configuration shape for each — without ever assuming access, fetching credentials, or writing secrets. The command reads the project's classification, maps detected needs to candidate servers (e.g. a GitHub/issue-tracker server, a database server such as Postgres/Supabase, a scoped filesystem server, a monitoring/observability server, a docs/search server), documents each via the MCP server template, and verifies the whole plan against the MCP safety checklist. The output is a written plan plus a commented `.mcp.json` skeleton with placeholders the user fills in from their own secret store. This command never connects to, authenticates against, or invokes any MCP server.

## When to use
- Right after `/route` or `/classify-project`, once `docs/state/project-type.md` exists and the team knows what the project does.
- When a build phase is about to depend on an external system (a database, a repo host, a ticketing system, a monitoring backend) and an MCP server would let agents work against it more safely than ad-hoc scripts.
- When onboarding a new contributor or CI runner that needs a documented, reproducible MCP setup.
- When auditing an existing `.mcp.json` for over-broad scope, missing read-only defaults, or secrets accidentally committed.

## Workflow

### Step 0 — Load context (read-only)
1. Read `.claude/docs/MCP_STRATEGY.md` for the project's MCP philosophy: least-privilege, read-only-by-default, no-secrets-in-VCS.
2. Read `.claude/skills/mcp-integration/SKILL.md` for the server-selection and scaffolding method.
3. Read `.claude/checklists/mcp-safety.md` — the gate this plan must pass.
4. Read `.claude/templates/mcp-server-template.md` — the per-server documentation shape.
5. Read `docs/state/project-type.md` (classification, risk class, cross-cutting concerns). If it is absent, **STOP** and tell the user to run `/route` first.
6. If a `.mcp.json` already exists, read it to understand the current state — do **not** modify it in place yet.

### Step 1 — Detect candidate servers
From the classification and the repo contents, derive the *needs*, then map each need to at most one candidate server. Detect by reading manifests and config only (never by connecting):
- **Repo / VCS host** (GitHub, GitLab) — if `.git/config` or CI workflows reference a host.
- **Database** (Postgres, Supabase, MySQL, Mongo) — if a connection string env var, ORM config, or migration directory is present.
- **Issue tracker / project management** — if the team uses one per specs or repo metadata.
- **Monitoring / observability** — if the readiness plan calls for metrics, logs, or traces.
- **Docs / search** — if the project depends on an external knowledge base or large doc corpus.
- **Filesystem (scoped)** — only when an agent must read a directory outside the repo; scope it to the narrowest path.

For each candidate, record: the need it serves, the read vs. write surface required, and whether it touches production data (high-risk).

### Step 2 — Classify risk and default to least privilege
For every candidate server set the **default access tier to read-only**. A write-capable or production-touching server is proposed **only** when a specific build task requires it, and is flagged for explicit user opt-in. A database server pointed at production is always high-risk and must be scoped to a read replica or non-prod environment in the proposal unless the user explicitly states otherwise.

**STOP — Present the candidate list to the user.** State, per server: the need, the proposed access tier (read-only / scoped-write), and any production exposure. Ask: "Which of these MCP servers do you want me to scaffold, and for any write-capable one, do you explicitly approve write access? Reply before I write the plan." Wait for acknowledgment.

### Step 3 — Scaffold the proposed configuration (placeholders only)
For each approved server, produce a `.mcp.json` block using **placeholder tokens** for every credential, e.g. `${ENV_GITHUB_TOKEN}`, `${ENV_DATABASE_URL}` — never a real value. Add an inline comment (or a sibling note, since strict JSON has no comments) describing what each placeholder is and where the user should set it (their own secret manager / shell env, never the repo). Mark the proposed file clearly as a template: write it as `docs/state/mcp.proposed.json` (or `.mcp.json.example`), **not** as the live `.mcp.json`. Never write or overwrite the active `.mcp.json` automatically.

### Step 4 — Document each server
For every proposed server, fill in `.claude/templates/mcp-server-template.md`: purpose, tools exposed, access tier, data sensitivity, credential source (env var name only), rotation note, and the rollback (how to remove the server). Collect these into the plan.

### Step 5 — Verify against the safety checklist
Run every item in `.claude/checklists/mcp-safety.md` against the plan: no secrets in any written file; read-only default honored; write/prod servers carry explicit user approval; filesystem scope is minimal; each server is documented and removable. Any P0 failure blocks the plan.

### Step 6 — Write the plan and record assumptions
1. Write `docs/state/mcp-plan.md`: the candidate analysis, per-server documentation, the access-tier decisions, the checklist result, and clear next-step instructions for the user to supply credentials in their own environment.
2. For every non-obvious selection (a server included, a tier chosen, a candidate rejected), append an entry to `docs/state/assumptions.md` via `.claude/templates/assumptions-log.md`.

## Agents used
- `.claude/agents/core/orchestrator.md` — sequences the selection and enforces the safety gate.
- `.claude/agents/quality/security-auditor.md` — reviews the proposed scopes and credential handling for least-privilege and secret-exposure risk.

## Skills used
- `.claude/skills/mcp-integration/SKILL.md` — server-selection heuristics, scaffolding pattern, and least-privilege configuration method.

## Expected outputs
| Output | Path |
|---|---|
| MCP plan (analysis + per-server docs) | `docs/state/mcp-plan.md` |
| Proposed config (placeholders only) | `docs/state/mcp.proposed.json` |
| Assumptions appended | `docs/state/assumptions.md` |

## Stop conditions
- `docs/state/project-type.md` missing → **STOP**; instruct the user to run `/route` first.
- A candidate server would require production write access and the user has not explicitly approved it → **STOP**; do not include it; record the gap.
- The user asks to put a real credential into any tracked file → **decline**; explain that secrets belong in their secret manager and the config carries only placeholders.
- No external systems detected at all → report that no MCP servers are warranted and exit cleanly without writing a config.

## Final report format
```
## /setup-mcp — MCP Plan Report

**Project:** <name>  |  **Type:** <preset>  |  **Risk class:** <high|medium|low>

### Candidate servers
| Server | Need served | Access tier | Prod exposure | Status |
|---|---|---|---|---|
| github | PR/issue automation | read-only | none | proposed |
| postgres | schema introspection | read-only (replica) | none | proposed |

### Safety check
MCP safety checklist: <PASS | N P0 blockers>. No secrets written: <confirmed>.

### Outputs
- Plan: docs/state/mcp-plan.md
- Proposed config (placeholders): docs/state/mcp.proposed.json

### Next step (user action required)
Set the referenced env vars in your own secret store, copy the proposed config to
`.mcp.json` when ready, then re-run `/setup-mcp` to re-verify, or proceed with the build.
```

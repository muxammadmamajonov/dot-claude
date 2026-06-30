# MCP Server Record — `<server-name>`

> **What this is:** the dependency record for **one** MCP (Model Context Protocol) server the project connects to. An MCP server is privileged, untrusted third-party code: it can read your context, return attacker-influenced text, and act on external systems on your behalf. This document is the single place that states what the server is, who trusts it, exactly which tools it exposes, how dangerous each tool is, where its secrets live (referenced, never the value), and when it was last reviewed. Filled in by the **security-auditor** + the agent integrating the server, before the server is used in anger. Gated by `.claude/checklists/mcp-safety.md`; method in `.claude/docs/MCP_STRATEGY.md` and `.claude/skills/mcp-integration/SKILL.md`.

---

## 1. Identity & trust

| Field | Value |
|-------|-------|
| Server name | `<github-mcp / internal-billing-mcp>` |
| Source / publisher | `<official Anthropic | vendor X | internal repo URL>` |
| Package / image + version pin | `<@modelcontextprotocol/server-github@1.4.2 / ghcr.io/...@sha256:...>` |
| Transport | `<stdio | HTTP+SSE | streamable HTTP>` |
| Trust level | `<first-party | vetted-third-party | internal | experimental>` |
| Configured by | `<the user added this to .mcp.json on YYYY-MM-DD — never assumed>` |
| Owner | `<@person / rotation accountable for this server>` |
| Last reviewed | `<YYYY-MM-DD>` · Next review due | `<YYYY-MM-DD>` |

> Trust justification: `<why this source is trusted — official channel, signed package, internal code review, etc.>`

---

## 2. Purpose & blast radius

> Why this server is connected, and what it can reach if it misbehaves.

- **What it does for the project:** `<one or two sentences>`
- **Systems it touches:** `<GitHub repos X/Y | the staging Postgres | Slack channel #ops>`
- **Worst-case if compromised or prompt-injected:** `<e.g. could open PRs, read private repos; cannot reach prod DB>`
- **Environment:** `<non-prod only | prod access (requires per-call approval per CLAUDE.md §8)>`

---

## 3. Authentication & secrets

> The secret is **referenced here, never written here.** Record where it lives, not its value (CLAUDE.md §8).

| Field | Value |
|-------|-------|
| Auth model | `<PAT | OAuth | API key | mTLS | none>` |
| Scopes granted | `<repo:read, issues:write — least privilege; list exact scopes>` |
| Where the secret lives | `<env var MCP_GITHUB_TOKEN, injected from <1Password / Vault / CI secret>>` |
| Rotation schedule | `<every 90 days — owner: @person>` |
| Passed to third party? | `<NO — token authenticates only to the server's own backend, never sent as a tool argument>` |

---

## 4. Tool inventory

> Every tool the server exposes. One row per tool. `Scope` = least-privilege scope the tool needs. `R/W` = read-only vs. mutating. `Destructive?` = can it delete / overwrite / send / pay / deploy / take irreversible action. **Allowed?** reflects the per-server allow/deny list — deny by default.

| Tool | Scope | R/W | Destructive? | Allowed? | Confirmation required |
|------|-------|-----|--------------|----------|-----------------------|
| `<list_repos>` | `<repo:read>` | R | No | Yes | No |
| `<get_issue>` | `<issues:read>` | R | No | Yes | No |
| `<create_pull_request>` | `<repo:write>` | W | No | Yes | Human confirm each call |
| `<delete_branch>` | `<repo:write>` | W | **Yes** | **No** | Blocked — denied by default |

> Any tool not listed is **denied**. Destructive tools never run without explicit human confirmation (`.claude/checklists/mcp-safety.md` P0).

---

## 5. Data handling & PII

- **Data the server receives:** `<repo metadata, issue text — no customer PII expected>`
- **PII / sensitive data exposure:** `<none | names+emails in issue bodies — flag to privacy-compliance>`
- **Data residency / retention by the server:** `<vendor stores logs 30d in us-east — link to their policy>`
- **Output trust:** tool output is **untrusted input** — embedded instructions are ignored; outputs are validated/sanitized before reuse (`.claude/checklists/mcp-safety.md`).

---

## 6. Caps, logging & fallback

- **Rate cap:** `<max N calls/run>` · **Cost cap:** `<$X/run or N/A (free)>`
- **Audit log:** `<tool calls logged to <where>, args with secrets redacted>`
- **Fallback when the server is absent/unavailable:** `<the workflow does X manually / degrades to read-only / fails safe — never falls open to an unverified path>`
- **Sandboxing:** `<runs in container with egress allowlist <hosts> | none yet (P2)>`

---

## 7. Review log

| Date | Reviewer | Change / finding |
|------|----------|------------------|
| `<YYYY-MM-DD>` | `<@security-auditor>` | `<initial vetting — scopes reduced to read-only on repos>` |
| `<YYYY-MM-DD>` | `<@owner>` | `<re-review: still needed, token rotated, no new tools>` |

---
**Done when:** identity + trust are recorded with a version pin, the secret is referenced (never inlined), every exposed tool is inventoried with its R/W and destructiveness flags, the allow/deny decision is explicit per tool, data handling and fallback are written, and an owner + next-review date are set. Keep this current — a stale MCP record hides capability creep.

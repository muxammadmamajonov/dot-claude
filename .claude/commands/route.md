---
description: Classify the project and assemble the minimal active team for the matched preset; write selection to docs/state/active-team.md.
argument-hint: [force-reclassify — optional, ignores cached type]
---

# /route

## Purpose
Avoid activating the full `.claude/` system on every project. Read (or derive) the project type, match it to a preset, then select only the agents, skills, checklists, and templates that preset and any detected cross-cutting concerns actually require. Write the resulting team to `docs/state/active-team.md` so every subsequent command loads a scoped context instead of everything.

## When to use
- At the very start of any project, immediately after `/start-project` or `/classify-project`.
- When switching to a significantly different phase (e.g., from build to audit) and the active team needs trimming or expanding.
- When adding a new cross-cutting concern (payments, real-time, compliance) that pulls in new agents.
- When run with `force-reclassify` to re-derive the type on an existing project after a major pivot.

## Workflow

### Step 0 — Load project state
1. Read `.claude/agents/core/orchestrator.md` to understand delegation rules and context-loading policy.
2. If `force-reclassify` was NOT passed and `docs/state/project-type.md` exists, read it — use the cached classification. Skip to Step 2.
3. If no cached classification exists, proceed to Step 1.

### Step 1 — Classify (if needed)
1. Read the repo root: `README*`, `package.json`, `Cargo.toml`, `pyproject.toml`, `build.gradle`, `*.csproj`, `go.mod`, manifest files, `Dockerfile`, `Makefile`, `*.unity`, `hardhat.config.*`, `*.ino`, `requirements.txt`, `Pipfile`, `CMakeLists.txt`, etc.
2. Identify the primary project type and sub-type (e.g., `backend-api / fintech`, `game-3d / multiplayer`, `cli-tool / devtool-library`).
3. Identify the platform target(s): web, iOS, Android, desktop (win/mac/linux), embedded, server, cloud function, edge, browser extension, smart contract, etc.
4. Identify the risk class:
   - **High** — handles money, PII/PHI, authentication, regulated data, critical infrastructure.
   - **Medium** — handles user accounts, non-sensitive personal data, or has production users.
   - **Low** — internal/personal tool, no external users, no sensitive data.
5. Detect cross-cutting concerns present in the codebase or specs (check `docs/specs/` if present):
   - Payments (Stripe, PayPal, invoicing, subscriptions)
   - Real-time (WebSocket, SSE, CRDT, game networking)
   - Auth / identity (OAuth, SAML, JWT, MFA)
   - Compliance triggers: GDPR, HIPAA, PCI-DSS, SOC 2, COPPA, CCPA
   - AI/ML inference or training pipeline
   - Multi-tenant SaaS isolation
   - Mobile (offline sync, push notifications, app store submission)
   - Observability gaps (no logging/metrics/tracing yet)
   - Internationalization / localization
6. Write classification to `docs/state/project-type.md` using this structure:
   ```
   primary_type: <preset-name>          # e.g. backend-api
   sub_type: <domain or qualifier>      # e.g. fintech
   platforms: [server, web]
   risk_class: high | medium | low
   cross_cutting: [payments, auth, compliance-pci]
   classified_at: <ISO date>
   ```

### Step 2 — Match preset and read routing matrix
1. Open `.claude/orchestration/routing-matrix.md`. Find the row matching `primary_type`.
2. Read the preset's default agent set, skill set, checklist set, and template set from the matrix.
3. For each detected `cross_cutting` concern, read the corresponding expansion row in the matrix and merge any additional agents, skills, or checklists into the selection (deduplicating).
4. If `risk_class` is **high**, ensure the following are always included regardless of preset:
   - Agents: `.claude/agents/quality/security-auditor.md`, `.claude/agents/quality/privacy-compliance-auditor.md`
   - Checklists: `.claude/checklists/security.md`, `.claude/checklists/privacy-compliance.md`
   - Templates: `.claude/templates/threat-model.md`, `.claude/templates/security-model.md`

### Step 3 — Assemble minimal active team
Collect the final de-duplicated selection:
- **Core agents** always included: `.claude/agents/core/orchestrator.md`, `.claude/agents/core/technical-lead.md`
- **Preset agents** from Step 2
- **Cross-cutting additions** from Step 2
- **Risk-class additions** from Step 2 (if high)

Exclude agents, skills, checklists, and templates not referenced by any active preset or cross-cutting concern. The goal is the smallest set that covers the project — do not add "just in case" entries.

### Step 4 — Write active team manifest
Write `docs/state/active-team.md` with this exact structure:

```markdown
# Active Team — <project name>

**Generated:** <ISO date>  |  **Command:** /route  |  **Preset:** <preset-name>
**Risk class:** <high|medium|low>  |  **Cross-cutting:** <comma list or none>

## Core Agents
- .claude/agents/core/orchestrator.md
- .claude/agents/core/technical-lead.md
- <additional core agents>

## Engineering Agents
- <only the engineering agents this preset requires>

## Quality Agents
- <only the quality agents needed for this project's risk class and phase>

## Design Agents
- <if any>

## Domain Expert
- <if any>

## Active Skills
- <skill paths, one per line>

## Active Checklists
- <checklist paths, one per line>

## Active Templates
- <template paths, one per line>

## Inactive (available but not loaded)
All other agents, skills, checklists, and templates in .claude/ are available on demand
but are NOT part of the active context for this project. Reference them only if the
project scope changes.
```

**STOP — Present the active team summary to the user.** State:
- The detected project type and risk class.
- The preset matched.
- The cross-cutting concerns that triggered expansions.
- Any high-risk additions.
- Ask: "Does this team look right for your project? Reply with any corrections before we proceed."

### Step 5 — Record the routing decision
If any non-obvious selection was made (e.g., a cross-cutting concern triggered an extra quality agent, or the risk class overrode a preset default), append a decision record to `docs/decisions/` using `.claude/templates/decision-record.md`. Title it: `ADR: Team routing for <project-type> (<date>)`.

## Agents used
- `.claude/agents/core/orchestrator.md` — drives the classification logic and context-loading policy.

## Skills used
- `.claude/skills/discovery/SKILL.md` — codebase reading pattern to infer project type.
- `.claude/skills/project-classification/SKILL.md` — structured classification heuristics.

## Expected outputs
| Output | Path |
|---|---|
| Project type record | `docs/state/project-type.md` |
| Active team manifest | `docs/state/active-team.md` |
| Routing decision record (if non-obvious) | `docs/decisions/adr-routing-<date>.md` |

## Stop conditions
- No source files at all and no specs found → cannot classify; **STOP** and ask the user: "What are you building? Share a brief description, and I'll classify and route from there."
- Detected type is `custom-project` (no preset match) → route to the `custom-project` preset, activate all quality agents, and flag in the active-team manifest that manual team curation is advised.
- User rejects the proposed team in Step 4 → incorporate corrections, re-write `docs/state/active-team.md`, and record the override as a decision.

## Final report format
```
## /route — Team Assembly Report

**Project:** <name>
**Primary type:** <preset-name>  |  **Sub-type:** <qualifier>
**Platforms:** <list>  |  **Risk class:** <high|medium|low>
**Cross-cutting concerns:** <list or "none detected">

### Preset matched
`<preset-name>` — <one-line rationale>

### Active team (N agents, N skills, N checklists, N templates)

| Category | Count | Notable additions vs. base preset |
|---|---|---|
| Core agents | N | — |
| Engineering agents | N | <e.g. payments-engineer added for Stripe> |
| Quality agents | N | <e.g. privacy-compliance-auditor added (high risk)> |
| Skills | N | — |
| Checklists | N | <e.g. privacy-compliance.md added (GDPR trigger)> |
| Templates | N | <e.g. threat-model.md added (high risk)> |

### Inactive (not loaded)
<N> agents, <N> skills, <N> checklists not needed for this project type.

### Next step
Run `/create-specs` to begin the specification stage with this team, or `/continue-work`
if specs already exist.
```

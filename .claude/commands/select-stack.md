---
description: Choose the technology stack from project constraints and write Architecture Decision Records
argument-hint: [optional layer to re-evaluate, e.g. "database" or "frontend"]
---

# /select-stack

## Purpose
Select the complete technology stack for the project — language, framework, database, cache, queue, infra, CI/CD, and key libraries — by evaluating options against constraints from discovery and the cross-cutting concerns from classification. Write a decision record per major choice so the reasoning is preserved and reversible.

## When to use
- As Phase 4 of `/start-project`, after specs are approved.
- Standalone to reconsider a single layer (e.g., swapping the database) without rerunning the full flow.
- When the team composition or budget changes significantly.

## Workflow

### Step 1 — Load inputs
1. Read `docs/state/project-type.md` — primary type, preset path, cross-cutting concerns.
2. Read `docs/context/discovery-answers.md` — hard constraints, team size, budget, timeline, existing infra.
3. Read the preset from the path listed in project-type.md (e.g., `.claude/presets/web-app.md`). The preset provides opinionated defaults; individual decisions can override them.
4. Read `docs/specs/product-spec.md` — NFR section for performance targets, uptime, supported platforms.

### Step 2 — Apply hard constraints
5. Extract all hard constraints from discovery (Q6 answers). Mark each as a filter that eliminates options from the stack matrix before scoring begins.
   Examples of common hard constraints:
   - "Must run on-prem" → eliminates hosted-only databases and PaaS.
   - "Existing Azure subscription" → favours Azure services over AWS/GCP.
   - "Team only knows Python" → eliminates non-Python server frameworks unless team growth is funded.
   - "PCI DSS scope" → requires HSM key management, no plaintext card data storage.
   - "HIPAA BAA required" → eliminates vendors without a signed BAA.

### Step 3 — Evaluate each layer
6. For each stack layer below, consult `.claude/stack-matrix/` for options and score them against:
   - **Fit** (0–3): How well does this option match the project type and NFRs?
   - **Constraint pass** (Y/N): Does it pass all hard constraints from step 2?
   - **Team velocity** (0–2): How quickly can the current team ship with it?
   - **Ecosystem maturity** (0–2): Is the library/tool production-proven at the required scale?
   - **Cost** (0–2): Is the licensing and infra cost within the budget envelope?

   Layers to evaluate:

   | Layer | Read from |
   |-------|-----------|
   | Language(s) | `.claude/stack-matrix/backend.md` |
   | Frontend framework | `.claude/stack-matrix/web.md` |
   | Backend framework | `.claude/stack-matrix/backend.md` |
   | Primary database | `.claude/stack-matrix/database.md` |
   | Search engine | `.claude/stack-matrix/database.md` (search section) |
   | Cache / session store | `.claude/stack-matrix/database.md` (cache section) |
   | Message queue / event bus | `.claude/stack-matrix/realtime.md` |
   | File / object storage | `.claude/stack-matrix/database.md` |
   | Auth provider | `.claude/stack-matrix/backend.md` |
   | Infra / hosting | `.claude/stack-matrix/cloud-devops.md` |
   | CI/CD | `.claude/stack-matrix/cloud-devops.md` |
   | Observability | `.claude/stack-matrix/monitoring.md` |
   | AI / LLM (if AGT or AI concern) | `.claude/stack-matrix/ai-ml.md` |

7. For each layer, select the highest-scoring option that passes hard constraints. If two options score equally, prefer the one already used elsewhere in the stack (reduces operational surface).

8. Flag any layer where no option scores above 5/9 — this is a weak fit requiring explicit user approval or a custom solution.

### Step 4 — Write the stack summary
9. Create `docs/decisions/stack.md` with:
   - A one-row-per-layer table: Layer | Choice | Version/plan | Score | Why the runner-up lost.
   - A "Stack cohesion" paragraph explaining how the choices work together.
   - A "Known gaps" section listing any weak-fit layers or unresolved evaluations.

### Step 5 — Write Architecture Decision Records
10. For every major choice (primary database, backend framework, auth provider, infra platform, and any choice that overrides the preset default), create `docs/decisions/adr/<nnn>-<slug>.md` using the template at `.claude/templates/decision-record.md`.

    Each ADR must include:
    - **Status** — Proposed / Accepted / Deprecated / Superseded.
    - **Context** — Why a decision was needed; constraints that applied.
    - **Options considered** — at least two; for each: pros, cons, score.
    - **Decision** — the chosen option and the tiebreaker rationale.
    - **Consequences** — what becomes easier, what becomes harder, what is now locked in.
    - **Review date** — when to revisit (e.g., after 6 months or after reaching a scale milestone).

### Step 6 — Confirm with user
11. **STOP.** Present the stack summary table and the list of ADRs created.
12. Ask: "Does this stack align with your team's skills, vendor relationships, and budget? Are there any choices you would override?"
13. If the user overrides a choice:
    - Record the override in the relevant ADR as "User override: <reason given>".
    - Re-evaluate dependent layers for compatibility.
    - Do not argue against the override — document it and move on.

## Agents used
None — this command runs inline.

## Skills used
- `.claude/skills/security/SKILL.md` — consulted for auth provider and infra choices to verify they meet the security classification from product-spec.md.

## Expected outputs
| Path | Description |
|------|-------------|
| `docs/decisions/stack.md` | Full stack summary table |
| `docs/decisions/adr/<nnn>-<slug>.md` | One ADR per major decision |

## Stop conditions
- No options pass hard constraints for a required layer — halt and surface the conflict to the user. Example: "No database option passes both the on-prem constraint and the required HTAP workload. You must relax one constraint or accept a two-database architecture."
- The team has zero experience with the highest-scoring option AND the timeline is less than 3 months — flag the risk; ask whether to accept the option with a ramp-up plan or fall back to a lower-scoring but familiar option.
- Budget is insufficient for the licensing cost of the chosen option — present the delta and ask how to resolve it (upgrade budget, choose OSS alternative, reduce scope).

## Final report format
```
## /select-stack — Stack Decided

**Stack summary:**
| Layer | Choice | Version |
|-------|--------|---------|
| ...   | ...    | ...     |

**ADRs written:** <count> (paths listed)
**Preset overrides:** <list or "none">
**User overrides:** <list or "none">
**Weak-fit layers:** <list or "none">

**Next step:** /design-architecture
```

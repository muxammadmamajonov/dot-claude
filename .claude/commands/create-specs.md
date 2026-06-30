---
description: Turn discovery answers into product spec, business rules, roles/permissions, and feature specs
argument-hint: [optional feature name to generate a single feature spec]
---

# /create-specs

## Purpose
Transform the discovery record and project classification into a complete, structured specification set: a product overview, business rules, a role/permission matrix, and an individual spec file for every feature. These specs are the authoritative source of truth for architecture, data model, and build phases.

## When to use
- As Phase 3 of `/start-project`, after `/interview-founder` is complete and approved.
- Standalone to add a new feature spec without rewriting the entire product spec.
- When discovery answers are updated and specs need to be regenerated for changed sections.

## Workflow

### Step 1 — Load inputs
1. Read `docs/context/discovery-answers.md`. If it does not exist, halt and run `/interview-founder` first.
2. Read `docs/state/project-type.md` to know the primary type, presets, and cross-cutting concerns.
3. Scan for any `[DECISION NEEDED]` markers in the discovery answers. List them — they will become blocking notes inside the spec files.

### Step 2 — Write product spec
4. Create `docs/specs/product-spec.md` from the template at `.claude/templates/product-spec.md`.

   Required sections:
   - **Executive summary** — problem, solution, primary user, one-sentence value prop.
   - **User personas** — one paragraph each, including technical level, device/platform, primary goal, key pain.
   - **Scope** — what is explicitly IN and OUT of v1.
   - **Non-functional requirements** — performance targets, uptime SLA, supported platforms/browsers/OS, accessibility level (WCAG AA or AAA), data residency, security classification.
   - **Assumptions** — things believed true that have not been verified; each tagged `[ASSUMPTION]`.
   - **Open decisions** — copied from discovery `[DECISION NEEDED]` markers; each tagged with the blocking phase.

5. Every claim in the spec must trace back to a specific discovery answer by quote or paraphrase. No invented requirements.

### Step 3 — Write business rules
6. Create `docs/specs/business-rules.md`.

   Format each rule as:
   ```
   BR-<nnn>: <imperative statement>
   Source: discovery Q<n> / stakeholder assumption / regulatory requirement
   Affects: <feature names>
   ```

   Minimum rule categories to cover (populate only those relevant to the project type):
   - Data validation and integrity rules
   - Authorisation and access rules
   - Workflow / state-machine rules (e.g., order status transitions)
   - Pricing and billing rules (if applicable)
   - Compliance rules (GDPR deletion, HIPAA audit trail, PCI tokenisation, etc.)
   - Rate limits and abuse prevention
   - Notification triggers
   - Deletion and retention rules

### Step 4 — Write roles and permissions matrix
7. Create `docs/specs/roles-permissions.md`.

   - List every user role and system actor (e.g., anonymous visitor, free user, paid user, admin, superadmin, background worker, third-party webhook).
   - Build a permission table: rows = capabilities, columns = roles, cells = Allow / Deny / Conditional.
   - Mark any permission that requires an audit log with `[AUDIT]`.
   - Mark any permission that changes billing state with `[BILLING]`.

### Step 5 — Enumerate features and write feature specs
8. From the product spec scope, extract a feature list. Group features into:
   - **Core** — must ship for v1 to be functional.
   - **Enhanced** — adds significant value but v1 can launch without them.
   - **Future** — out of v1 scope; listed to prevent architectural decisions that block them.

9. For each **Core** and **Enhanced** feature, create `docs/specs/feature-specs/<feature-slug>.md` from the template at `.claude/templates/feature-spec.md`.

   Each feature spec must include:
   - **Feature ID** — `FEAT-<nnn>` for cross-referencing.
   - **One-line summary** — what it does and why it matters.
   - **User story** — "As a <persona>, I want to <action> so that <outcome>."
   - **Acceptance criteria** — numbered, testable, using "Given / When / Then" or "The system must…" form.
   - **Business rules applied** — list of `BR-<nnn>` from business-rules.md.
   - **Roles that can access** — from roles-permissions.md.
   - **Data touched** — entities created, read, updated, deleted (CRUD summary).
   - **Integrations** — any third-party APIs, queues, or services involved.
   - **Edge cases and error conditions** — what happens when input is invalid, the third party is down, the user has insufficient permissions, rate limits are hit.
   - **Out of scope for this feature** — explicit exclusions to prevent scope creep.

### Step 6 — Cross-reference and validate
10. Verify that:
    - Every business rule is referenced by at least one feature spec.
    - Every role appears in at least one feature's access list.
    - Every `[DECISION NEEDED]` marker from step 1 appears in the relevant spec file.
    - No spec contains placeholder text, "TODO", or lorem ipsum.

11. Print a validation summary listing any gaps found.

### Step 7 — Confirm with user
12. **STOP.** Present the list of spec files created and the validation summary.
13. Ask: "Do these specs capture the full v1 scope? Are there features missing or in the wrong tier (core/enhanced/future)?"
14. Incorporate any corrections before marking the phase complete.

## Agents used
None — this command runs inline without spawning sub-agents.

## Skills used
- `.claude/skills/security/SKILL.md` is consulted when writing compliance and authorisation rules (BR categories 2, 5).

## Expected outputs
| Path | Description |
|------|-------------|
| `docs/specs/product-spec.md` | Full product specification |
| `docs/specs/business-rules.md` | Numbered business rules with traceability |
| `docs/specs/roles-permissions.md` | Role/permission matrix |
| `docs/specs/feature-specs/<slug>.md` | One file per Core and Enhanced feature |

## Stop conditions
- `docs/context/discovery-answers.md` does not exist — halt, run `/interview-founder`.
- Fewer than 3 core features can be identified from the discovery answers — the scope is too vague; return to `/interview-founder` for clarification.
- A compliance requirement (HIPAA, PCI, GDPR) is present but no specific rules can be extracted from discovery — add `[DECISION NEEDED: compliance rules must be defined with legal counsel]` and halt the affected spec section rather than inventing rules.
- A feature spec's acceptance criteria reference a data entity that has not been named — note it as a gap; it will be resolved in `/design-data-model`.

## Final report format
```
## /create-specs — Spec Set Complete

**Product spec:** docs/specs/product-spec.md
**Business rules:** <count> rules written
**Roles defined:** <list>
**Feature specs:**
  Core (<count>): <list of FEAT-IDs>
  Enhanced (<count>): <list of FEAT-IDs>
  Future (<count>): <list of FEAT-IDs — not spec'd, only named>

**Validation:**
  - Unresolved [DECISION NEEDED] markers: <count>
  - Business rules with no feature reference: <count or "none">
  - Roles with no feature reference: <count or "none">

**Next step:** /select-stack
```

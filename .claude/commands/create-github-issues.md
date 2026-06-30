---
description: Convert specs, roadmap, and audit findings into well-formed issues; writes a dry-run plan to docs/state/issue-plan.md and STOPS for approval before creating anything.
argument-hint: [source: specs | roadmap | audits | all — optional, default all]
---

# /create-github-issues

## Purpose
Turn the project's written artifacts — feature specs (`docs/specs/feature-specs/`), the roadmap (`docs/roadmap/phases.md`), and audit findings (security/QA/performance/accessibility reports) — into a set of well-formed, deduplicated, prioritized issues. This command is **read-only by default**: it first writes a complete dry-run issue list to `docs/state/issue-plan.md` and **STOPS** for explicit approval. Only on confirmation does it create issues via the `gh` CLI (when a repo and remote are configured); otherwise it leaves the reviewed markdown plan as the deliverable. It **never creates issues without confirmation**, and never deletes or closes existing issues. Universal by default: works whether the backlog items are gameplay features, CLI commands, data pipelines, or API endpoints.

## When to use
- After specs and roadmap exist and you want a trackable backlog (post stage 4, during stage 5/9 planning).
- After an audit (`/audit-security`, `/audit-performance`, etc.) to file remediation work as issues.
- When onboarding an existing project: convert its reconstructed specs into a starter backlog.
- Whenever the roadmap changes and new phases need issues opened.

## Workflow

### Step 0 — Determine sources and environment
1. Read the `source` argument (`specs | roadmap | audits | all`; default `all`).
2. Read the inputs that exist: `docs/specs/feature-specs/*`, `docs/roadmap/phases.md`, and audit reports under `docs/reports/`. Skip silently any source not present and note it.
3. Detect the issue backend **non-destructively**: check for a git remote and the `gh` CLI (`gh auth status`). Record whether live creation is even possible — but do not create anything yet.

### Step 1 — Extract candidate issues
1. From **specs**: one issue per discrete, independently shippable feature or acceptance criterion cluster. Pull the user value, the acceptance criteria, and the spec path.
2. From the **roadmap**: one issue per phase deliverable, tagged with its milestone/phase.
3. From **audits**: one issue per P0/P1/P2 finding (not P3 backlog unless asked), carrying its severity, CWE/category, and affected file.
4. For each candidate capture: title, body, type label, priority, source artifact path, and any dependency on another candidate.

### Step 2 — Normalize, deduplicate, and prioritize
1. Write each issue to a consistent shape: imperative title, context paragraph, acceptance criteria checklist, source link, and labels.
2. **Deduplicate** against each other and, if `gh` is available, against existing open issues (read-only `gh issue list`) so you do not file a duplicate. Mark suspected duplicates rather than dropping them silently.
3. Assign priority from the source (audit severity P0–P2; roadmap phase order; spec must-have/nice-to-have). Map to the project's label scheme if one exists.

### Step 3 — Write the dry-run plan
Write `docs/state/issue-plan.md` with this structure:

```markdown
# Issue Plan (dry run) — <project name>

**Generated:** <ISO date>  |  **Command:** /create-github-issues  |  **Backend:** gh available: yes/no
**Sources:** <specs, roadmap, audits>  |  **Status:** AWAITING APPROVAL — nothing created yet

## Summary
| Source | Candidate issues | Suspected duplicates |
|---|---|---|
| specs | N | N |
| roadmap | N | N |
| audits | N | N |

## Proposed issues
### [1] <title>
- **Type / priority:** feature | bug | chore — P0/P1/P2
- **Labels:** <…>   |   **Milestone:** <phase or none>
- **Source:** `docs/specs/feature-specs/<file>.md`
- **Depends on:** [#? in this plan] or none
- **Body:**
  > <context paragraph>
  > Acceptance criteria:
  > - [ ] <criterion>

### [2] …

## Suspected duplicates (will be skipped unless you say otherwise)
- [n] <title> — matches existing issue #<id> "<title>"
```

### Step 4 — STOP for approval
**STOP — present the plan summary to the user.** State: the number of issues per source, any suspected duplicates, and whether live creation via `gh` is possible. Ask explicitly: **"Reply `create` to open these issues via gh, `edit <n> …` to adjust, or `keep` to leave the markdown plan only. I will not create anything until you confirm."** Do not proceed past this gate without an explicit `create`.

### Step 5 — Create on confirmation only
1. On `create` **and** `gh` available: open each non-duplicate issue with `gh issue create --title … --body … --label … [--milestone …]`. Create in dependency order. Capture each returned issue URL.
2. After creation, update `docs/state/issue-plan.md` to record the created issue numbers/URLs and mark the plan `EXECUTED`.
3. If `gh` is **not** available (no remote, not authenticated, or user said `keep`): leave `docs/state/issue-plan.md` as the deliverable and tell the user exactly how to create them later. Never attempt to authenticate or add a remote on the user's behalf.
4. Never close, edit, or delete pre-existing issues — this command only adds.

## Agents used
- `.claude/agents/core/project-manager.md` — sequences issues by phase and dependency, owns the milestone mapping.
- `.claude/agents/core/product-manager.md` — derives issues from specs and writes user-value-framed acceptance criteria.

## Skills used
- `.claude/skills/requirements-engineering/SKILL.md` — turning specs and findings into precise, testable, well-scoped work items.

## Expected outputs
| Output | Path |
|---|---|
| Dry-run issue plan | `docs/state/issue-plan.md` |
| Created issues (on approval, gh available) | GitHub issues + URLs recorded back in the plan |

## Stop conditions
- **No source artifacts found** (no specs, roadmap, or audit reports) → **STOP**; tell the user which inputs are missing and suggest running the relevant command first.
- **Always STOP at Step 4** before any creation — explicit `create` confirmation is mandatory; no exceptions.
- **`gh` unavailable or unauthenticated** → do not attempt creation; deliver the markdown plan and stop.
- **User replies `keep` or anything other than `create`** → leave the plan untouched as the deliverable.
- **A candidate matches an existing open issue** → mark it a duplicate and skip it unless the user explicitly overrides.

## Final report format
```
## /create-github-issues — Issue Plan Report

**Project:** <name>  |  **Sources:** <specs, roadmap, audits>
**Backend:** gh available: yes/no  |  **Status:** awaiting approval | executed | plan-only

### Candidates
| Source | Issues | Duplicates skipped |
|---|---|---|
| specs | N | N |
| roadmap | N | N |
| audits | N | N |

### Plan location
`docs/state/issue-plan.md` — <N> proposed issues, <N> suspected duplicates.

### Created (only if approved)
| # | Title | Priority | URL |
|---|---|---|---|
| 12 | <title> | P0 | <url> |

### Next step
Awaiting approval → reply `create` to open the issues, `edit <n>` to adjust, or
`keep` to keep the markdown plan only.
Executed → review the opened issues; re-run after the next audit or roadmap change.
```

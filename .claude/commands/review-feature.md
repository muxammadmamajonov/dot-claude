---
description: Review a built feature for correctness, security, performance, accessibility, and conventions
argument-hint: [feature name]
---

# /review-feature

## Purpose
Conduct a structured multi-dimension review of a completed feature: verify it meets its acceptance criteria, then audit for security vulnerabilities, performance problems, accessibility gaps, and convention violations. Produce a prioritised finding list and a clear pass/block verdict.

## When to use
- After `/implement-feature [feature name]` reports all tests green and the self-review checklist complete
- Before merging a feature branch or promoting to staging/production
- When requested for any pull request, diff, or change set
- The argument must name the feature; if omitted, ask which feature to review

## Workflow

**Step 1 — Load context** (orchestrator: `.claude/agents/core/orchestrator.md`)
- Read `docs/specs/feature-specs/[feature-name].md` for acceptance criteria and known deviations
- Read `docs/architecture/overview.md` for architectural constraints
- Read `docs/roadmap/phases.md` to confirm the feature is in the current phase
- Read `.claude/checklists/security.md`, `.claude/checklists/performance.md`, `.claude/checklists/accessibility.md`
- Identify all files changed by the feature (diff against the base branch or list provided by the user)

**Step 2 — Correctness review**
For each acceptance criterion in the spec:
- Confirm it is implemented (code evidence + test evidence)
- Confirm the test actually exercises the criterion (not just asserting `true`)
- Flag: missing criteria, tests that pass vacuously, untested edge cases mentioned in spec

Check logic for:
- Off-by-one errors, null/undefined handling, type coercions, race conditions, unhandled async failures
- Incorrect error propagation (errors swallowed, wrong status codes, misleading messages)
- Data integrity: writes that bypass validation, missing transactions on multi-step mutations

**Step 3 — Security review**
Walk every input boundary (HTTP, CLI, file, queue, socket, environment) and check:
- Input validation and sanitisation present and sufficient
- No SQL/NoSQL/command injection vectors (parameterised queries, safe shell invocation)
- No sensitive data in logs, error responses, or URLs
- Authentication required where spec says it is
- Authorisation enforced per-resource, not just per-route
- Secrets read from environment, never hardcoded or committed
- Dependency changes: any new package with known CVEs or unusual permissions?
- For web: XSS, CSRF, clickjacking, open redirects, insecure cookies
- For APIs: rate limiting present, verbose error messages suppressed in production
- For file operations: path traversal prevention, upload type validation

  > The web items above are the **web branch**. For other project types apply the equivalent type checklist instead: mobile (insecure storage, certificate pinning, deep-link validation), desktop (IPC/protocol-handler abuse, code signing), game (client-authority/anti-cheat, save tampering), CLI (argument/path injection, unsafe shell-out), IoT/embedded (firmware integrity, secure boot, device identity), blockchain (re-entrancy, signature replay, key custody). Keep the review universal — match the checks to the platform under review.

Severity: Critical / High / Medium / Low / Info

**Step 4 — Performance review**
- Database queries: N+1 patterns, missing indexes for filter/sort columns, unbounded result sets
- Payload sizes: responses that could grow without pagination or limit
- Blocking I/O on critical paths (synchronous file reads in request handlers, etc.)
- Caching opportunities missed for expensive or repeated reads
- Memory: large allocations per request, unbounded in-memory collections
- For UI: unnecessary re-renders, large bundle additions, unoptimised images/assets

**Step 5 — Accessibility review** (skip if feature has no user-facing UI)
Using `.claude/checklists/accessibility.md`:
- All interactive elements keyboard-reachable and focusable
- Focus order logical; focus trap present in modals/drawers
- All images have meaningful alt text (or `alt=""` for decorative)
- Form inputs have associated labels (not just placeholder)
- Error messages programmatically associated with their fields
- Colour contrast meets WCAG 2.2 AA (4.5:1 text, 3:1 UI components)
- No content conveyed by colour alone
- Screen-reader announcements for dynamic content updates (ARIA live regions)

**Step 6 — Conventions review**
- Naming: variables, functions, files, routes, events match the patterns in the rest of the codebase
- Folder structure: new files placed in the correct locations per `docs/architecture/overview.md`
- No duplicate logic that already exists elsewhere in the codebase
- Public interfaces documented (JSDoc, docstrings, OpenAPI annotations, type exports)
- No leftover debug statements, commented-out code, or `TODO` without a linked issue
- Tech debt introduced is documented in the feature spec

**Step 7 — Compile findings**
Produce a findings table:
| ID | Dimension | Severity | File:Line | Description | Recommended fix |
|----|-----------|----------|-----------|-------------|-----------------|

Severity levels: Critical (block merge) / High (block merge) / Medium (fix before next phase) / Low (fix when convenient) / Info (no action required)

**Step 8 — Verdict**

- **PASS**: zero Critical or High findings — feature is ready to merge
- **PASS WITH CONDITIONS**: zero Critical, one or more High findings — list must be fixed before promotion to production, merge to staging acceptable
- **BLOCK**: one or more Critical or High findings — must be fixed and re-reviewed before merge

STOP — present full findings and verdict to the user. Ask:
1. For any Critical/High finding: confirm the proposed fix approach before making changes
2. For any architectural finding: confirm whether it requires a spec update

**Step 9 — Fix cycle** (if BLOCK or if user requests fixes)
- For each Critical/High finding: apply the fix, re-run tests, confirm the finding is resolved
- Re-run Steps 2–6 over changed files only
- Update verdict

## Agents used
- `.claude/agents/core/orchestrator.md` — coordinates review dimensions
- `.claude/agents/quality/security-auditor.md` — Step 3 security checks (if present)
- `.claude/agents/quality/qa-engineer.md` — Step 2 test coverage checks (if present)

## Skills used
- `.claude/skills/security/SKILL.md`
- `.claude/checklists/security.md`
- `.claude/checklists/performance.md`
- `.claude/checklists/accessibility.md`

## Expected outputs
| Artefact | Status |
|----------|--------|
| `docs/reviews/[feature-name]-review.md` | created |
| Feature spec updated with resolved deviations | updated (if applicable) |
| Fixed code (if fix cycle ran) | modified |

## Stop conditions
- No feature spec or acceptance criteria found — halt, ask user to locate or write spec before review
- Diff/file list is unavailable — ask user to provide the list of changed files
- A Critical finding requires a destructive fix (e.g. data migration to correct corrupted records) — halt, present impact analysis, require explicit human approval before executing

## Final report format
```
## Feature Review — [feature name]

### Verdict: PASS | PASS WITH CONDITIONS | BLOCK

### Findings summary
| Severity | Count |
|----------|-------|
| Critical | N     |
| High     | N     |
| Medium   | N     |
| Low      | N     |
| Info     | N     |

### Acceptance criteria: N/N confirmed met

### Findings
[findings table from Step 7]

### Fix cycle: ran | not run
### Post-fix verdict: [updated verdict if fix cycle ran]

### Files reviewed
- [list]

### Files modified (fix cycle)
- [list, or "none"]

### Next step
[PASS] Merge branch and run /create-tests for regression suite
[BLOCK] Fix Critical/High findings then re-run /review-feature [feature name]
```

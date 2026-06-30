---
description: Run a security audit against the security checklist and OWASP/CWE; report P0/P1/P2 findings with fixes.
argument-hint: [scope: full | api | auth | deps | secrets — optional]
---

# /audit-security

## Purpose
Systematically audit the codebase for security vulnerabilities. Map findings to OWASP Top 10 and CWE categories. Classify each finding as P0 (critical/exploitable now), P1 (high/exploitable under realistic conditions), or P2 (medium/defence-in-depth). Produce concrete fix recommendations and, where safe, apply P0 fixes immediately.

## When to use
- Pre-launch security gate (required before running `/prepare-launch`).
- After adding authentication, authorisation, file upload, payment, or external-data features.
- After a significant dependency upgrade.
- Periodic (quarterly) security health check.
- After any penetration test to validate remediation.

## Workflow

### Step 0 — Determine scope
1. Read `docs/specs/` and `.claude/stack-matrix/` to understand the tech stack, trust boundaries, and data sensitivity.
2. If an argument was given (`full | api | auth | deps | secrets`), restrict analysis to that surface. Default is `full`.
3. Identify the project type (web API, mobile backend, CLI, embedded, etc.) — this determines which OWASP categories apply.

### Step 1 — Static analysis and dependency scan
Run all available tools for the detected stack (skip gracefully if a tool is absent):

| Tool | Purpose |
|---|---|
| `semgrep --config=auto` | General SAST patterns |
| `bandit -r .` | Python-specific |
| `npm audit --json` / `yarn audit` | Node.js deps |
| `cargo audit` | Rust deps |
| `trivy fs .` | Multi-ecosystem dep scan |
| `trufflehog filesystem .` | Secrets in repo history |
| `gitleaks detect` | Secrets in commits |
| `pip-audit` | Python deps |

Capture raw output. Do not discard findings — every warning is evaluated in Step 2.

### Step 2 — Manual code review (checklist-driven)
Work through `.claude/checklists/security.md`. For each item not covered by static analysis, read the relevant code directly.

**OWASP Top 10 mapping (always check these):**

| # | Category | Where to look |
|---|---|---|
| A01 | Broken Access Control | route guards, object-level auth, IDOR patterns |
| A02 | Cryptographic Failures | hash algorithms, TLS config, key storage |
| A03 | Injection | SQL/NoSQL queries, shell calls, template rendering |
| A04 | Insecure Design | threat model, trust boundaries in specs |
| A05 | Security Misconfiguration | env files, CORS, HTTP headers, debug flags |
| A06 | Vulnerable Components | dep scan output from Step 1 |
| A07 | Auth & Session Failures | token expiry, brute-force protection, MFA |
| A08 | Software & Data Integrity | CI/CD pipeline, unsigned packages, deserialization |
| A09 | Logging & Monitoring Failures | sensitive data in logs, missing audit trail |
| A10 | SSRF | outbound HTTP calls, URL parameters, webhooks |

Also check project-type-specific items:
- **APIs:** rate limiting, input validation schemas, mass assignment.
- **File upload:** MIME validation, storage outside web root, virus scan hook.
- **Auth:** OAuth redirect_uri validation, PKCE, refresh token rotation.
- **Mobile backends:** certificate pinning, API key exposure in app bundle.
- **CLIs:** path traversal in file args, privilege escalation.

### Step 3 — Classify and deduplicate findings
For each finding assign:
- **Priority:** P0 / P1 / P2.
- **CWE ID** (e.g., CWE-89 SQL Injection).
- **OWASP category** (A01–A10).
- **Affected file(s) and line(s)**.
- **Exploitability:** brief scenario — how an attacker reaches this.
- **Recommended fix:** concrete code change or config setting.

Priority criteria:
- **P0** — unauthenticated remote code execution, SQL injection on sensitive tables, plaintext credential storage, exposed admin endpoints, hardcoded production secrets.
- **P1** — authenticated privilege escalation, IDOR on sensitive resources, missing CSRF on state-changing endpoints, weak key derivation.
- **P2** — missing security headers, verbose error messages leaking stack traces, insecure-but-chained-requirements, outdated deps with no known exploit.

### Step 4 — Apply P0 fixes (with approval)
1. For each P0 finding, draft the minimal safe fix.
2. **STOP — present P0 findings and proposed fixes to the user. Get explicit approval before writing any code.**
3. Apply approved fixes one at a time. Run tests after each. Commit: `fix(security): <CWE-ID> <one-line description>`.
4. Do NOT auto-apply P1/P2 — record them in the report for the user to schedule.

### Step 5 — Verify no regressions
Run the full test suite after all P0 fixes. If tests fail, revert the offending fix and flag it in the report as "fix attempted — regression, needs manual resolution".

### Step 6 — Report
Produce the Final report (see below).

## Agents used
- `.claude/agents/quality/security-auditor.md` — orchestrates static analysis tool invocations.
- `.claude/agents/quality/test-automation-engineer.md` — writes regression tests for confirmed vulnerabilities.

## Skills used
- `.claude/skills/security/SKILL.md` — fix patterns for each vulnerability class.
- `.claude/checklists/security.md` — full itemised security checklist.

## Expected outputs
| Output | Path |
|---|---|
| Security audit report | `docs/reports/security-audit-<date>.md` |
| Applied P0 fixes | in-place, committed |
| Updated checklist | `.claude/checklists/security.md` (checked items) |

## Stop conditions
- Static analysis tools not installed and scope is `full` → warn user, proceed with manual review only.
- P0 finding requires architectural change (e.g., whole auth system redesign) → document it, do not attempt to fix inline; escalate to user.
- Applying a fix breaks tests and no safe alternative is obvious → revert, flag in report.
- Secrets found in commit history → **STOP immediately**, alert user — history rewrite needed before any further work.

## Final report format
```
## Security Audit Report — <date>

**Project:** <name>  |  **Scope:** <full|api|auth|deps|secrets>
**Stack:** <detected tech>  |  **Auditor:** Claude Code

### Summary
| Priority | Count | Fixed in this session |
|---|---|---|
| P0 Critical | N | N |
| P1 High | N | 0 (scheduled) |
| P2 Medium | N | 0 (scheduled) |

### P0 — Critical (must fix before launch)
#### [P0-1] <Title> — CWE-<N>, OWASP <AXX>
- **File:** `path/to/file.ext:line`
- **Exploitability:** <one-sentence attack scenario>
- **Fix applied:** ✅ commit <sha> / ❌ needs manual work
- **Fix description:** <what was done or what must be done>

### P1 — High (fix within sprint)
#### [P1-1] <Title> — CWE-<N>, OWASP <AXX>
- **File:** `path/to/file.ext:line`
- **Exploitability:** <scenario>
- **Recommended fix:** <description>

### P2 — Medium (fix within quarter)
- [P2-1] <Title> — `file:line` — <one-line description>

### Dependency vulnerabilities
| Package | Version | CVE | Severity | Fix version |
|---|---|---|---|---|

### Tools run
| Tool | Result |
|---|---|
| semgrep | <N findings> |
| trivy | <N findings> |

### Next steps
1. Schedule P1 fixes for current sprint.
2. Re-run `/audit-security` after P1 remediation.
3. Add security regression tests for confirmed P0 vectors.
```

---
name: security
description: Threat-model, harden, and security-review any feature or system — STRIDE modeling, secure-by-default code/config review, secrets/auth/authz handling, and the pre-launch security audit. Use this skill whenever the work touches authentication, authorization, sessions, passwords, tokens, secrets, encryption, user/personal/financial data, file upload, payments, SQL/queries, external input, dependencies/CVEs, CORS, or you hear "is this secure", "security review", "threat model", "audit", "pentest", "vuln", "OWASP", or a suspected leak/incident — even if the user doesn't say "security".
---

# Security: Threat-Model & Harden

## When to use
- Designing any feature that handles auth, authorization, personal/financial data, file upload, payments, or untrusted input.
- Reviewing a diff or PR for vulnerabilities before merge.
- Running the dedicated security audit phase before production readiness.
- Responding to a suspected vulnerability, leaked secret, or incident.

This applies to every project type: web, mobile, desktop, API, CLI, game, agent system, embedded, blockchain. The attack surface differs; the discipline does not.

## Workflow
1. **Define what you're protecting.** List assets (user data, credentials, funds, model/IP, availability) and trust boundaries (who/what crosses from untrusted to trusted). For agent/LLM systems, treat prompts, tool calls, and retrieved content as untrusted input.
2. **Threat-model with STRIDE.** For each trust boundary, ask: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege. Write down the realistic threats and rank by impact × likelihood. Record assumptions explicitly.
3. **Decide controls per threat.** Map each ranked threat to a concrete control (authn, authz, validation, encryption, rate limit, logging, isolation). Prefer platform/framework-provided controls over hand-rolled crypto or auth.
4. **Apply secure-by-default during build.** Validate and encode all external input at the boundary; parameterize queries; authorize every request server-side; deny by default. Keep secrets out of code and logs. See Standards.
5. **Review the diff.** Run the security review pass against `.claude/checklists/security.md`: injection, broken access control, secrets, dependency CVEs, insecure deserialization, SSRF, weak crypto, misconfig. Use SAST/dependency scanning where available.
6. **Test the controls.** Add tests that assert authorization failures, input rejection, and rate limits actually trigger. Negative tests are the point. Coordinate with `.claude/skills/testing/SKILL.md`.
7. **Audit before launch.** Verify the full checklist, confirm secrets are managed (see `.claude/skills/devops/SKILL.md`), confirm logging/alerting on security events, and document residual risks and their owners.
8. **Document & monitor.** Record the threat model and decisions in an ADR (`.claude/skills/documentation/SKILL.md`), wire up alerts for auth failures/anomalies, and define the incident path in a runbook.

## Standards
- **Do** authorize every action server-side on the resource, checking ownership/role — never trust client-supplied identity or hidden fields.
- **Do** validate input against an allowlist and encode output for its sink (HTML, SQL, shell, URL, JSON, log).
- **Do** keep secrets in a manager/vault or platform secret store; inject via env at runtime; rotate on exposure. Never commit `.env`, keys, or tokens.
- **Do** use parameterized queries / prepared statements / safe ORMs; never build queries by string concatenation.
- **Do** use vetted libraries for crypto, password hashing (argon2/bcrypt/scrypt), JWT/session handling; pin and patch dependencies.
- **Do** enforce TLS in transit and encryption at rest for sensitive data; set security headers / secure cookie flags where applicable.
- **Do** rate-limit and add abuse controls on auth, expensive, and write endpoints; fail closed.
- **Do** treat LLM/agent inputs and tool outputs as untrusted: constrain tool permissions, sanitize, and prevent prompt-injection from reaching privileged actions.
- **Do-not** roll your own crypto, auth, or session management.
- **Do-not** log secrets, tokens, full PANs, passwords, or full PII.
- **Do-not** disable TLS verification, use `eval` on input, or run untrusted code without isolation.
- **Do-not** perform destructive or irreversible production security actions (key deletion, prod data wipe, force-disabling auth) without explicit human approval — see project destructive-action rules.

## Common mistakes to avoid
- Broken access control: checking a role in the UI but not on the server; IDOR via predictable IDs with no ownership check.
- Secrets in source, CI logs, error messages, or client bundles.
- Trusting client-side validation; trusting `redirect`/`url`/`host` parameters (SSRF/open redirect).
- Verbose errors leaking stack traces, internal hostnames, or query structure to users.
- Outdated dependencies with known CVEs and no scanning in CI.
- Prompt injection in agent systems escalating to data exfiltration or unauthorized tool use because tools were over-permissioned.
- Treating "internal" services as trusted and skipping authn/authz between them.

## Output format
A threat model + hardening record: asset/trust-boundary list, ranked STRIDE threats, control per threat with status, and residual-risk register with owners. For reviews, produce a findings list with severity, location, and remediation. Reference `.claude/templates/architecture.md` for boundaries and log the model as an ADR via `.claude/skills/documentation/SKILL.md`.

## Related checklists
- `.claude/checklists/security.md`
- `.claude/checklists/production.md`
- `.claude/checklists/qa.md`

## Related agents
- `.claude/agents/quality/security-auditor.md`
- `.claude/agents/core/orchestrator.md`
- `.claude/agents/engineering/backend-engineer.md`

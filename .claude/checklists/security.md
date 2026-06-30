# Security Checklist
Gate to verify the system is hardened against common attack vectors before any environment is exposed to real users or real data. Items are severity-tagged P0/P1/P2/P3.

## P0 — Blockers (must pass before any internet-facing deployment)
- [ ] Authentication uses a proven library or service (OAuth2/OIDC provider, Passport.js, Auth0, Supabase Auth, etc.) — no hand-rolled auth logic.
- [ ] Passwords are hashed with an adaptive algorithm (bcrypt, Argon2id, or scrypt) with a work factor appropriate for current hardware; MD5/SHA-1/SHA-256 alone are unacceptable.
- [ ] All secrets (API keys, DB credentials, private keys, signing secrets) are stored in environment variables or a secrets manager — never in source code, config files committed to VCS, or client-side bundles.
- [ ] Every output rendered into HTML is context-escaped (HTML entity, attribute, JS, URL) to prevent XSS; templating engines have auto-escaping enabled by default.
- [ ] All database queries use parameterized statements or an ORM's query builder — no string concatenation forming SQL/NoSQL/LDAP queries.
- [ ] File uploads validate MIME type server-side (not just the extension), enforce size limits, are stored outside the web root or in object storage, and are never executed.
- [ ] HTTPS/TLS 1.2+ is enforced on every public endpoint; HTTP requests are redirected to HTTPS; HSTS is set with a `max-age` of at least one year.
- [ ] Dependency vulnerability scan (e.g., `npm audit`, `pip-audit`, `trivy`, `snyk`) passes with no known critical or high CVEs in production dependencies.
- [ ] CSRF protection is active on all state-changing requests from browser clients (SameSite cookies, CSRF tokens, or origin validation).
- [ ] Authorization checks verify the acting user owns or has permission to access the requested resource — not just that they are authenticated (IDOR prevention).

## P1 — Important (fix before scaling or onboarding sensitive data)
- [ ] Security HTTP headers are set on all responses: `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY` (or `frame-ancestors`), `Referrer-Policy`, `Permissions-Policy`.
- [ ] Rate limiting and brute-force protection are applied to login, password reset, OTP verification, and any unauthenticated endpoint that triggers work or reveals information.
- [ ] JWT tokens (where used) have short expiry (≤15 min access tokens), are signed with RS256 or ES256 rather than HS256 shared secrets in multi-service setups, and are validated for `iss`, `aud`, and `exp` on every request.
- [ ] Third-party and open-source dependencies are pinned to exact versions with a lock file committed; automated PRs (Dependabot, Renovate) are configured.
- [ ] Logging captures security-relevant events (login success/failure, permission denied, admin actions, data exports) with user ID, IP, and timestamp — without logging passwords, tokens, or PII in plaintext.
- [ ] Principle of least privilege is applied to all service accounts, IAM roles, and database users — no service runs as root or with admin credentials in production.
- [ ] Secrets rotation process is defined and tested: rotating a credential requires no downtime and no code change.
- [ ] Subresource Integrity (SRI) hashes are set on any third-party CDN scripts; or third-party scripts are self-hosted.

## P2 — Hardening / nice-to-have
- [ ] A responsible disclosure / bug bounty policy is published at `/.well-known/security.txt`.
- [ ] Automated DAST (Dynamic Application Security Testing) scan (OWASP ZAP, Nuclei, Burp Suite CI mode) runs against a staging environment in CI.
- [ ] Multi-factor authentication (TOTP, WebAuthn/passkeys) is available and enforced for admin and privileged roles.
- [ ] Network egress from production services is restricted to known endpoints via firewall rules or service mesh policy — no arbitrary outbound connections.
- [ ] Cryptographic keys and TLS certificates are managed by a key management service (AWS KMS, GCP Cloud KMS, HashiCorp Vault); private key material never touches application memory.
- [ ] Data at rest is encrypted for all databases, object storage buckets, and disk volumes containing user or business data.
- [ ] An incident response runbook exists and covers: credential compromise, data breach, DDoS, supply-chain attack, and unauthorized privilege escalation.
- [ ] Penetration test or red-team exercise is scheduled before the first major public launch; findings are tracked to remediation.

## P3 — Post-launch / backlog (track and revisit after launch; never blocks shipping)

- [ ] Penetration test or red-team exercise scheduled at P2 is executed, all findings are tracked to remediation, and a re-test is scheduled within 90 days of the initial engagement.
- [ ] Responsible disclosure / bug bounty policy published at P2 (`/.well-known/security.txt`) is reviewed after the first 90 days live: any reported vulnerabilities are triaged, resolved, and used to update internal threat models.
- [ ] Secrets rotation process defined at P1 is exercised end-to-end in production (not just staging) for each credential type; rotation runbook is updated with any discrepancies found.
- [ ] Network egress allowlist defined at P2 is audited against actual outbound connections observed in production logs; any undocumented egress destinations are investigated and either allowlisted with justification or blocked.
- [ ] MFA enforcement for admin and privileged roles introduced at P2 is extended to all non-admin user tiers where user-risk analysis (account-takeover rate, data sensitivity) justifies it.
- [ ] Dependency vulnerability scan cadence is reviewed: if automated PRs from Dependabot/Renovate are accumulating without merge, a triage session is scheduled and the merge policy is tightened to prevent drift.

## How to use
Run before every environment promotion (dev → staging, staging → production) and after every major feature addition.
Also triggered by `.claude/agents/core/orchestrator.md` as part of the production-readiness gate.
Cross-reference `.claude/checklists/api.md` for API-layer controls and `.claude/checklists/data-model.md` for data-at-rest controls.
Use `audit-security` skill for automated scanning assistance.
Reviewer marks each item `[x]` when satisfied or `[-]` when waived with a written reason and compensating control noted.

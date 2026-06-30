# Security Model

**What:** Identifies the system's valuable assets, threat actors, trust boundaries, STRIDE-based threat analysis, data classification, and the controls that mitigate each threat.
**Who fills it in:** Security lead + architect, reviewed by engineering lead and legal/compliance.
**When:** During architecture design — before any code handling sensitive data is written. Revisit after every major feature addition.

> This document does NOT replace a penetration test or a formal threat-model workshop. It is the standing record that informs both.

---

## 1. Scope

> What system components are in scope for this threat model? What is explicitly out of scope?

**In scope:**
- `<e.g. Web application (frontend + BFF)>`
- `<e.g. REST/GraphQL API layer>`
- `<e.g. PostgreSQL database and object storage>`
- `<e.g. Admin dashboard>`
- `<e.g. Third-party integrations: Stripe, SendGrid, Auth0>`

**Out of scope:**
- `<e.g. End-user devices / browsers>`
- `<e.g. Cloud provider infrastructure (assumed secure)>`
- `<e.g. Third-party SaaS internals>`

---

## 2. Assets

> What does an attacker want? List every valuable asset and what happens if it is compromised.

| Asset | Confidentiality impact if exposed | Integrity impact if tampered | Availability impact if lost |
|-------|----------------------------------|------------------------------|-----------------------------|
| `<User PII (name, email, phone)>` | High — regulatory liability, user harm | High — trust loss | Medium |
| `<Payment / billing data>` | Critical — PCI DSS violation | Critical | High |
| `<Auth tokens / session cookies>` | Critical — account takeover | Critical | Medium |
| `<User-generated content>` | Medium | High | Medium |
| `<API keys / secrets>` | Critical — full system access | Critical | High |
| `<Business logic / pricing>` | Low | High — fraud | Low |
| `<Audit logs>` | Low | Critical — SOC2 violation | High |
| `<Infrastructure config>` | High — lateral movement | Critical | Medium |

---

## 3. Trust Boundaries

> Draw the perimeter between zones of different trust. Traffic crossing a boundary must be authenticated and authorised.

```
[ Public Internet ]
        │  HTTPS only; TLS 1.2+ min
        ▼
[ CDN / WAF / DDoS protection ]
        │  Strip internal headers; rate-limit
        ▼
[ Load Balancer / API Gateway ]   ◄── Admin VPN access only for management port
        │  mTLS to origin (optional)
        ▼
[ Application Servers ]           ◄── Service-to-service: short-lived JWT or mTLS
        │  Private subnet only
        ▼
[ Data Tier: DB + Cache + Blobs ] ◄── No public ingress; IAM role or secret manager creds
        │
        ▼
[ Third-party APIs ]              ◄── Outbound only; credentials via secret manager
```

**Cross-boundary rules:**
- Every boundary crossing requires authentication (no implicit trust).
- Secrets never cross the public boundary — only references (IDs, signed URLs).
- Admin operations require a separate auth path (VPN + MFA or break-glass procedure).

---

## 4. Data Classification

> Classify all data the system handles. Classification drives encryption, retention, and access-control decisions.

| Class | Definition | Examples | Controls required |
|-------|-----------|----------|-------------------|
| **Critical** | Breach causes regulatory penalty or material harm | Payment card data, passwords, private keys | Encrypt at rest (AES-256) + in transit (TLS 1.3); access logged; no logging of values |
| **Confidential** | Breach causes trust loss or competitive harm | PII, health data, internal pricing | Encrypt at rest; access restricted to need-to-know; masked in logs |
| **Internal** | Should not be public but low individual harm | Aggregate metrics, internal config | Access restricted to authenticated employees |
| **Public** | Intended for anyone | Marketing copy, open API docs | No restriction |

**Retention & deletion:**
| Data type | Retention | Deletion mechanism |
|-----------|-----------|-------------------|
| `<User PII>` | `<Until account deletion + 30 days>` | `<Soft-delete → cron hard-delete>` |
| `<Audit logs>` | `<7 years (SOC2 / GDPR)>` | `<Archive to cold storage after 90 days>` |
| `<Session tokens>` | `<Session lifetime + 24 h>` | `<TTL in Redis>` |
| `<Payment records>` | `<7 years (financial)>` | `<Pseudonymise after 1 year>` |

---

## 5. Threat Analysis (STRIDE)

> For each trust boundary or component, enumerate threats using STRIDE. Rate likelihood (L) and impact (I) on a 1–3 scale; score = L × I.

### 5.1 Authentication / Session

| Threat | STRIDE category | L | I | Score | Control |
|--------|----------------|---|---|-------|---------|
| Password brute-force | Spoofing | 3 | 3 | 9 | Rate-limit login; lockout after 10 fails; CAPTCHA |
| Credential stuffing | Spoofing | 3 | 3 | 9 | Pwned-password check on signup; anomaly detection |
| Session token theft (XSS) | Spoofing | 2 | 3 | 6 | `HttpOnly; Secure; SameSite=Strict` cookies; CSP |
| JWT algorithm confusion | Spoofing | 1 | 3 | 3 | Pin algorithm to RS256; reject `alg:none` |
| Account takeover via email | Spoofing | 2 | 3 | 6 | Email verification; MFA option; suspicious-login alert |

### 5.2 API Layer

| Threat | STRIDE category | L | I | Score | Control |
|--------|----------------|---|---|-------|---------|
| IDOR (horizontal privilege escalation) | Elevation of privilege | 3 | 3 | 9 | Row-level ownership checks on every query; no sequential IDs |
| SQL / NoSQL injection | Tampering | 2 | 3 | 6 | Parameterised queries only; ORM enforced; SAST in CI |
| Mass assignment | Tampering | 2 | 2 | 4 | Explicit allowlist of writeable fields per endpoint |
| SSRF | Information disclosure | 2 | 3 | 6 | Allowlist outbound URLs; block `169.254.*`, `10.*`, `localhost` |
| Rate-limit bypass | DoS | 2 | 2 | 4 | Distribute rate limits via IP + user ID + fingerprint |
| Business logic abuse | Tampering | 2 | 3 | 6 | Server-side price/quantity validation; signed cart tokens |

### 5.3 Data Tier

| Threat | STRIDE category | L | I | Score | Control |
|--------|----------------|---|---|-------|---------|
| DB exposed to public internet | Information disclosure | 1 | 3 | 3 | DB in private subnet; no public IP |
| Backup exfiltration | Information disclosure | 1 | 3 | 3 | Backups encrypted (CMK); access restricted to ops role |
| Insider data access | Information disclosure | 2 | 3 | 6 | Column-level encryption for PII; query audit logs |
| Data corruption / ransomware | Tampering | 1 | 3 | 3 | PITR backups; immutable backup copies; tested restore |

### 5.4 Infrastructure / Supply Chain

| Threat | STRIDE category | L | I | Score | Control |
|--------|----------------|---|---|-------|---------|
| Compromised dependency (npm/pip) | Tampering | 2 | 3 | 6 | SCA in CI (Dependabot / Snyk); lockfiles committed |
| Secret leakage via git | Information disclosure | 2 | 3 | 6 | Pre-commit secret scanning (Gitleaks); secret manager |
| Container escape | Elevation of privilege | 1 | 3 | 3 | Non-root container user; read-only filesystem; no privileged mode |
| CI/CD pipeline injection | Tampering | 1 | 3 | 3 | Pin action versions by SHA; restrict who can edit pipelines |

---

## 6. Security Controls

> Map each control category to implementation details and ownership.

### 6.1 Identity & Access

| Control | Implementation | Owner |
|---------|---------------|-------|
| Authentication | `<Auth0 / Cognito / Supabase Auth — MFA optional for users, required for admins>` | `<Backend lead>` |
| Authorisation | `<RBAC: roles [admin, member, viewer]; enforced server-side via middleware>` | `<Backend lead>` |
| Service-to-service auth | `<Short-lived JWT signed with service key | mTLS>` | `<DevOps>` |
| Secret management | `<AWS Secrets Manager / HashiCorp Vault — no secrets in env vars or code>` | `<DevOps>` |
| Principle of least privilege | `<IAM roles scoped to minimum required S3 buckets / DB tables>` | `<DevOps>` |

### 6.2 Network

| Control | Implementation |
|---------|---------------|
| TLS version | TLS 1.2 minimum, TLS 1.3 preferred; HSTS with preload |
| WAF | `<Cloudflare WAF | AWS WAF — OWASP Core Rule Set enabled>` |
| DDoS protection | `<Cloudflare / AWS Shield Standard>` |
| VPC / network segmentation | App servers in private subnet; DB in isolated subnet; no direct public access |
| Egress filtering | Allowlist known third-party endpoints; block unexpected outbound |

### 6.3 Application

| Control | Implementation |
|---------|---------------|
| Input validation | Server-side only; allowlist types; reject oversized payloads (`<1 MB default>`) |
| Output encoding | Framework-level XSS escaping; `Content-Type` headers enforced |
| CSP | `default-src 'self'; script-src 'self' <trusted CDN>; object-src 'none'` |
| CSRF | `SameSite=Strict` cookies; origin check on state-changing requests |
| File upload | Type allowlist; virus scan (ClamAV / cloud API); stored outside webroot |
| Dependency scanning | `<Dependabot + Snyk in CI; block PRs with critical CVEs>` |

### 6.4 Data Protection

| Control | Implementation |
|---------|---------------|
| Encryption at rest | AES-256 (cloud-managed key or CMK) for DB volumes and backups |
| Encryption in transit | TLS everywhere, including internal service mesh |
| PII masking in logs | `<Regex scrubber middleware strips email, phone, SSN patterns>` |
| Password storage | `<bcrypt (cost 12) | Argon2id>` — never plaintext, never reversible hash |
| Payment data | `<Stripe handles card data; we store only token + last-4>` |

### 6.5 Monitoring & Incident Response

| Control | Implementation |
|---------|---------------|
| Auth event logging | All login attempts (success + failure), token refresh, MFA events |
| Privileged action logging | Admin operations, data exports, role changes |
| Anomaly detection | `<CloudWatch / Datadog alerts on: spike in 4xx, failed logins, unusual data volume>` |
| Alerting | PagerDuty / OpsGenie on P1 security events; on-call rota defined |
| Incident runbook | `.claude/checklists/production.md` |
| Vulnerability disclosure | `security@<domain>` email; 90-day coordinated disclosure policy |

---

## 7. Compliance Requirements

> Fill in only the regulations that apply to this project.

| Regulation | Applies if | Our obligation | Owner |
|------------|-----------|----------------|-------|
| GDPR | Users in EU/UK | Lawful basis, DSARs, DPA agreements with processors | `<Legal + Engineering>` |
| CCPA | Users in California | Right to know, delete, opt-out of sale | `<Legal>` |
| PCI DSS | Card data in scope | SAQ A (Stripe hosted) or SAQ D (self-hosted) | `<Finance + DevOps>` |
| SOC 2 Type II | Enterprise customers require it | Controls audit, evidence collection | `<Security + DevOps>` |
| HIPAA | Health data | BAA with vendors, PHI controls | `<Legal + Backend>` |
| `<Other>` | `<Condition>` | `<Obligation>` | |

---

## 8. Security Review Triggers

> These events require a security review before the change ships.

- New external-facing API endpoint or parameter
- Change to authentication or authorisation logic
- New third-party integration receiving user data
- New file upload or download capability
- Infrastructure change (new subnet, security group, IAM role)
- Dependency major-version upgrade with known attack surface

---

## 9. Open Risks

> Track accepted or unmitigated risks. Review at each major release.

| # | Risk | Likelihood | Impact | Mitigation plan | Accepted by | Review date |
|---|------|-----------|--------|-----------------|-------------|-------------|
| 1 | `<e.g. No MFA enforced for regular users at launch>` | Medium | High | `<Enforce MFA in v1.2; email nudge at v1.0>` | `<CTO>` | `<YYYY-MM-DD>` |
| 2 | `<e.g. Third-party JS bundle loaded from CDN>` | Low | High | `<SRI hash on script tags; evaluate self-hosting>` | `<Security lead>` | `<YYYY-MM-DD>` |

---

## 10. Related Documents

- Architecture: `.claude/templates/architecture.md`
- Testing strategy (security testing section): `.claude/templates/testing-strategy.md`
- Security audit checklist: `.claude/checklists/security.md`
- Incident response runbook: `.claude/checklists/production.md`
- Production readiness checklist: `.claude/checklists/production.md`

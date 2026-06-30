# Threat Model

**What this is:** A STRIDE-based threat model capturing the system's assets, trust boundaries, data flows, and threats per component — together with concrete mitigations and residual risk. Kept live and re-reviewed whenever architecture changes significantly.

**Who fills this:** Security auditor + solution architect, reviewed by tech lead. Re-run at major milestones (new integrations, data-model changes, infra moves).

---

## 0. Document Metadata

| Field | Value |
|---|---|
| Project | `<project-name>` |
| Version | `<v1.0>` |
| Review date | `<YYYY-MM-DD>` |
| Reviewers | `<name, role>` |
| Next review | `<YYYY-MM-DD or trigger>` |

---

## 1. Scope & Objectives

> What system or feature does this threat model cover? What is explicitly out of scope?

- **In scope:** `<API gateway, auth service, payment flow, mobile app, admin portal>`
- **Out of scope:** `<third-party CDN internals, hardware supply chain>`
- **Security objectives:** confidentiality of `<PII / payment data>`, integrity of `<order records>`, availability of `<checkout flow>`

---

## 2. Assets

> What must be protected? Classify by sensitivity.

| Asset | Type | Sensitivity | Owner |
|---|---|---|---|
| `<User PII (name, email, phone)>` | Data | High | `<Data team>` |
| `<Payment card data>` | Data | Critical | `<Payments team>` |
| `<Auth tokens / session cookies>` | Credential | Critical | `<Platform team>` |
| `<API private keys / secrets>` | Credential | Critical | `<DevOps>` |
| `<Source code & CI/CD pipelines>` | System | High | `<Engineering>` |
| `<Database backups>` | Data | High | `<Ops>` |
| `<Service availability (SLO)>` | Service | Medium | `<SRE>` |

---

## 3. Trust Boundaries

> Draw or describe where privilege levels change. Every crossing is an attack surface.

```
[Internet / Public]
        │  HTTPS 443
   [WAF / CDN]                  ← trust boundary 1: public → edge
        │
   [API Gateway]               ← trust boundary 2: edge → internal network
        │             │
   [Auth Service]  [App Servers]
        │             │
   [Identity DB]  [App DB / Cache]  ← trust boundary 3: app tier → data tier
                      │
                  [Backups / Cloud Storage]  ← trust boundary 4: data → cold storage
```

> Example trust boundaries:
> - `<Browser ↔ API Gateway>` — untrusted client, TLS required, all inputs sanitized
> - `<API Gateway ↔ Auth Service>` — internal mTLS, service account
> - `<App Server ↔ Database>` — private subnet, credentials in secrets manager

---

## 4. Data Flows

> Enumerate significant flows; note where sensitive data travels.

| Flow ID | Source | Destination | Data | Protocol | Authenticated |
|---|---|---|---|---|---|
| DF-01 | `<Browser>` | `<API GW>` | `<Login credentials>` | `<HTTPS>` | No (pre-auth) |
| DF-02 | `<API GW>` | `<Auth Service>` | `<Username + password hash>` | `<mTLS>` | Yes (service cert) |
| DF-03 | `<Auth Service>` | `<Browser>` | `<JWT + refresh token>` | `<HTTPS>` | N/A |
| DF-04 | `<App Server>` | `<Payment PSP>` | `<Tokenized card ref>` | `<HTTPS>` | Yes (API key)` |
| DF-05 | `<App DB>` | `<Backup Storage>` | `<Encrypted DB dump>` | `<TLS>` | Yes (IAM role)` |

---

## 5. STRIDE Threats by Component

For each component list threats using the STRIDE mnemonic: **S**poofing, **T**ampering, **R**epudiation, **I**nformation Disclosure, **D**enial of Service, **E**levation of Privilege.

### 5.1 Component: `<API Gateway>`

| ID | STRIDE Category | Threat | Likelihood | Impact | Risk |
|---|---|---|---|---|---|
| T-01 | Spoofing | `<Attacker crafts a JWT with a weak secret>` | Medium | High | High |
| T-02 | Tampering | `<Request body modified in transit by MitM>` | Low | High | Medium |
| T-03 | Repudiation | `<API calls not logged; attacker denies action>` | Medium | Medium | Medium |
| T-04 | Info Disclosure | `<Stack traces returned in error responses>` | High | Medium | High |
| T-05 | DoS | `<Unauthenticated flood exhausts gateway quotas>` | High | High | Critical |
| T-06 | EoP | `<Broken object-level auth lets user A read user B data>` | Medium | High | High |

### 5.2 Component: `<Auth Service>`

| ID | STRIDE Category | Threat | Likelihood | Impact | Risk |
|---|---|---|---|---|---|
| T-07 | Spoofing | `<Credential stuffing using breached passwords>` | High | High | Critical |
| T-08 | Info Disclosure | `<Timing oracle leaks valid usernames>` | Medium | Low | Low |
| T-09 | EoP | `<Insecure password reset flow allows account takeover>` | Low | Critical | High |

### 5.3 Component: `<Database / Data Store>`

| ID | STRIDE Category | Threat | Likelihood | Impact | Risk |
|---|---|---|---|---|---|
| T-10 | Tampering | `<SQL injection via unsanitized query parameter>` | Medium | Critical | Critical |
| T-11 | Info Disclosure | `<Unencrypted backup accessible via misconfigured bucket>` | Low | Critical | High |
| T-12 | DoS | `<Unbounded query causes full-table scan, brings DB down>` | Medium | High | High |

### 5.4 Component: `<Frontend / Client>`

| ID | STRIDE Category | Threat | Likelihood | Impact | Risk |
|---|---|---|---|---|---|
| T-13 | Tampering | `<XSS allows script injection into shared session>` | Medium | High | High |
| T-14 | Info Disclosure | `<Sensitive data cached in browser localStorage unencrypted>` | High | Medium | High |

> Add a section per additional component: `<Payment Service>`, `<Admin Portal>`, `<Background Workers>`, `<Third-party Integrations>`, etc.

---

## 6. Mitigations

Map each threat ID to concrete controls already in place **and** planned.

| Threat ID | Mitigation | Status | Owner | Due |
|---|---|---|---|---|
| T-01 | `<Rotate to RS256 JWT; validate aud/iss/exp strictly>` | `In progress` | `<Platform team>` | `<2024-Q3>` |
| T-02 | `<Enforce TLS 1.2+ at gateway; HSTS header>` | `Done` | `<DevOps>` | — |
| T-03 | `<Structured audit log (user, action, resource, timestamp) to immutable store>` | `Planned` | `<Platform>` | `<2024-Q4>` |
| T-04 | `<Generic error messages in prod; detailed logs server-side only>` | `Done` | `<Backend>` | — |
| T-05 | `<Rate limiting (token bucket) per IP + per user; WAF rules>` | `In progress` | `<DevOps>` | `<2024-Q3>` |
| T-06 | `<OWASP ASVS Level 2 authorization checks; resource-ownership middleware>` | `Planned` | `<Backend>` | `<2024-Q4>` |
| T-07 | `<CAPTCHA on login; account lockout after 5 failures; breached-password check (HaveIBeenPwned API)>` | `In progress` | `<Auth team>` | `<2024-Q3>` |
| T-10 | `<Parameterized queries / ORM only; no dynamic SQL>` | `Done` | `<Backend>` | — |
| T-11 | `<Encrypt backup at rest (AES-256); private bucket policy; alert on public-access change>` | `Done` | `<DevOps>` | — |
| T-13 | `<CSP header; output encoding; React default escaping; SRI on CDN scripts>` | `In progress` | `<Frontend>` | `<2024-Q3>` |

---

## 7. Residual Risk

> Threats that remain after mitigations — accepted consciously with rationale and expiry.

| Threat ID | Residual Risk | Rationale for Acceptance | Review Date |
|---|---|---|---|
| T-08 | Low | `<Timing difference < 5ms; constant-time compare added next quarter>` | `<2024-Q4>` |
| T-12 | Medium | `<Query cost limits and read replicas mitigate; full fix in DB-layer ORM update>` | `<2024-Q3>` |

---

## 8. Attack Surface Summary

> Brief narrative of the total exposure after mitigations.

- **External-facing endpoints:** `<N public API routes, N public auth endpoints, CDN assets>`
- **Admin interfaces:** `<Admin portal behind VPN + MFA>`
- **Third-party integrations:** `<Payment PSP, email provider, analytics SDK>`
- **Key risk areas:** `<Auth flow, payment data handling, file upload, admin privilege escalation>`

---

## 9. Review Cadence & Sign-off

> When to re-run this model.

- **Triggered re-review:** any new external integration, major data-model change, new admin role, third-party SDK added, infra migration
- **Scheduled review:** `<Every 6 months or after each major release>`

| Reviewer | Role | Signature / Date |
|---|---|---|
| `<Name>` | `<Security Auditor>` | `<YYYY-MM-DD>` |
| `<Name>` | `<Solution Architect>` | `<YYYY-MM-DD>` |
| `<Name>` | `<Tech Lead>` | `<YYYY-MM-DD>` |

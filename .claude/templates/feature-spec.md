# Feature Spec
**What:** A complete specification for a single feature — problem, user stories, acceptance criteria, design decisions, edge cases, and test plan. This is the contract between product and engineering before a single line of code is written.  
**Who fills it in:** Product owner drafts sections 1–3; engineering leads fill sections 4–7; both review and sign off together.  
**Cross-references:** `.claude/templates/decision-record.md`, `.claude/templates/bug-report.md`, `.claude/templates/architecture.md`

---

## Spec Metadata

| Field | Value |
|-------|-------|
| Feature name | `<Magic Link Authentication>` |
| Spec ID | `<SPEC-0021>` |
| Author | `<@product-owner>` |
| Engineering lead | `<@eng-lead>` |
| Created | `<YYYY-MM-DD>` |
| Last updated | `<YYYY-MM-DD>` |
| Status | `<Draft | In Review | Approved | In Development | Shipped>` |
| Target release | `<v3.0.0>` |
| Linked ADRs | `<ADR-0042 — auth strategy>` |

---

## 1. Problem Statement

> What pain or opportunity does this feature address? Who is affected, how often, and what is the cost of not solving it? Be specific — cite data or user research where available.

`<45 % of support tickets relate to forgotten passwords. Users on mobile abandon signup at the password creation step at a 62 % rate (analytics, Q1 2026). Competitors (Linear, Notion) offer passwordless login and report higher activation rates.>`

**Who is affected:** `<All new and returning users on web and mobile>`  
**Frequency:** `<Every login attempt — ~8 K/day>`  
**Cost of inaction:** `<Continued high support volume, lower mobile activation, competitive disadvantage>`

---

## 2. Goals and Non-Goals

> State explicitly what this feature will and will not do. Non-goals prevent scope creep and are as important as goals.

**Goals:**
- Allow users to log in by entering their email and receiving a one-time magic link.
- Eliminate the need to remember a password for users who opt in.
- Work on web (all modern browsers) and native mobile (iOS, Android).
- Complete the auth flow in ≤ 3 user actions and ≤ 30 seconds (email delivery SLA).

**Non-goals (out of scope for this release):**
- Replacing existing password login — both methods coexist.
- Passkey / WebAuthn support (tracked in `<SPEC-0028>`).
- SMS-based OTP (separate decision — `.claude/templates/decision-record.md` ADR-0045).
- Enterprise SSO / SAML (separate roadmap item).

---

## 3. User Stories

> Write one story per distinct user type or workflow. Format: "As a `<role>`, I want to `<action>` so that `<outcome>`."

| ID | User story | Priority |
|----|-----------|----------|
| US-1 | As a **new user**, I want to sign up with just my email so that I don't have to create and remember a password. | Must have |
| US-2 | As a **returning user**, I want to click a link in my email to log in so that I never get locked out. | Must have |
| US-3 | As a **mobile user**, I want the magic link to open directly in the app so that I don't have to copy-paste a code. | Must have |
| US-4 | As a **security-conscious user**, I want magic links to expire after 15 minutes so that old links cannot be reused. | Must have |
| US-5 | As an **admin**, I want to see magic link login events in the audit log so that I can investigate suspicious access. | Should have |
| US-6 | As a **user on a shared device**, I want to be warned if the link is opened in a different browser than where I requested it. | Nice to have |

---

## 4. Acceptance Criteria

> Each criterion must be independently verifiable — no vague language like "works correctly" or "is fast". Link to the user story it satisfies.

| ID | Criterion | US ref |
|----|-----------|--------|
| AC-1 | User enters a valid email and clicks "Send magic link" — a transactional email arrives within 30 seconds. | US-1, US-2 |
| AC-2 | Magic link token is a cryptographically random 32-byte value (256-bit entropy), URL-safe base64 encoded. | US-4 |
| AC-3 | Token expires exactly 15 minutes after generation; clicking an expired link shows a clear error and a resend option. | US-4 |
| AC-4 | Token is single-use: clicking the link a second time returns an error — it cannot be reused. | US-4 |
| AC-5 | On mobile, clicking the link in the email opens the native app via universal link / app link; falls back to web if app not installed. | US-3 |
| AC-6 | Successful login creates a new session and redirects to `<the page the user originally requested>` or `/dashboard`. | US-1, US-2 |
| AC-7 | Each magic link request event (email sent, link clicked, success, expiry, reuse attempt) is written to the audit log with timestamp, user ID, and IP. | US-5 |
| AC-8 | Invalid or malformed token returns HTTP 400 with a user-friendly message; no token details are leaked in the error. | US-4 |
| AC-9 | Rate limit: maximum 5 magic link requests per email per hour; excess requests return HTTP 429 with retry-after header. | US-4 |
| AC-10 | `<Project-specific criterion>` | |

---

## 5. Design & Technical Approach

> High-level design decisions. Link to ADRs for major decisions. Include data model changes, API contract, and UI flow summary.

### 5.1 Flow Overview

```
User enters email
  → POST /auth/magic-link  (rate-checked)
  → Server generates token, stores hash in DB with expiry
  → Email sent via <SendGrid / Resend / SES>
  → User clicks link: GET /auth/magic-link?token=<value>
  → Server validates token hash, expiry, single-use flag
  → Token marked used, session created, user redirected
```

### 5.2 Data Model

> Describe new or changed tables/collections/schemas.

**New table: `magic_link_tokens`**

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| `id` | UUID | PK | |
| `user_id` | UUID | FK → users.id | |
| `token_hash` | VARCHAR(64) | NOT NULL, UNIQUE | SHA-256 of raw token; raw token never stored |
| `expires_at` | TIMESTAMPTZ | NOT NULL | `created_at + 15 min` |
| `used_at` | TIMESTAMPTZ | NULL | Set on first valid use |
| `created_at` | TIMESTAMPTZ | NOT NULL | |
| `ip_address` | INET | NULL | IP that requested the link |

### 5.3 API Contract

**Request magic link**
```
POST /auth/magic-link
Body: { "email": "user@example.com" }
Response 202: { "message": "Check your email" }
Response 429: { "error": "Too many requests", "retry_after": 3600 }
```

**Consume magic link**
```
GET /auth/magic-link?token=<raw-token>
Response 302: Redirect to /dashboard (success)
Response 400: { "error": "Invalid or expired link" }
```

### 5.4 UI/UX Summary

> Reference design files if they exist; otherwise describe the screens.

- **Screen 1 — Email entry:** Single email field + "Send magic link" button. No password field visible.
- **Screen 2 — Confirmation:** "Check your inbox" message with resend option (available after 60 s).
- **Screen 3 — Error:** Clear message differentiating "expired link" from "already used link", with a single CTA to request a new link.
- **Design file:** `<Figma link>`

### 5.5 Security Considerations

- Raw token is never stored — only its SHA-256 hash.
- Tokens transmitted only over HTTPS.
- Email enumeration prevention: the API returns 202 whether or not the email exists.
- See `.claude/checklists/security.md` for full auth security checklist.

---

## 6. Edge Cases

> List every non-happy-path scenario and specify the exact expected behavior for each.

| Scenario | Expected behavior |
|----------|------------------|
| Email not registered in system | Return 202 (do not reveal whether email exists); no email sent |
| User clicks link after 15 min | Show "This link has expired" with a "Request new link" button |
| User clicks link a second time | Show "This link has already been used" with a "Request new link" button |
| User requests 6th link within an hour | Return 429; show "Too many requests, try again in X minutes" |
| User opens link on different device/browser than request origin | `<Log the mismatch; show a warning but allow login (configurable)>` |
| Email delivery failure (bounce) | `<Log the bounce, do not silently fail; surface error in admin panel>` |
| Database unavailable when link is clicked | Return 503; do not expose internal error; alert on-call |
| Token contains SQL/script injection characters | Reject at input validation before any DB query; log attempt |
| User account is suspended | Token is valid but login is rejected with "account suspended" message; audit logged |
| `<Project-specific edge case>` | `<Expected behavior>` |

---

## 7. Test Plan

> Define the test coverage required before this feature can be marked ready. Assign ownership.

### Unit Tests
- `PricingCalculator` equivalent: `TokenService` — test `generate()`, `hash()`, `validate()`, `markUsed()` independently.
- Rate limiter logic — 5-per-hour window, edge at exactly limit, reset after window.
- Token expiry — expired token returns correct error; 1-second-before-expiry passes.

### Integration Tests
- Full flow: request → email queued → token stored → link consumed → session created.
- Expired token end-to-end.
- Reused token end-to-end.
- Rate limit end-to-end.

### Security Tests
- Confirm raw token is never logged or stored.
- Confirm email enumeration protection (same response for registered/unregistered email).
- Confirm HTTPS-only; HTTP requests redirect.
- Fuzz token parameter with special characters, oversized inputs, SQL fragments.

### Manual / Exploratory QA
- Happy path on web (Chrome, Safari, Firefox).
- Happy path on iOS native app (universal link opens app).
- Happy path on Android native app (app link opens app).
- Fallback: magic link on mobile when app not installed → opens mobile web.
- Resend flow after 60-second cooldown.

### Performance
- Load test: `<500 concurrent magic-link requests/second>` — confirm rate limiter holds, no token collisions.

**Test owner:** `<@qa-lead>`  
**CI gate:** All unit + integration tests must pass before PR merge. Manual QA required before staging promotion.

---

## 8. Open Questions

> List unresolved questions that could affect implementation. Assign an owner and target resolution date.

| # | Question | Owner | Due | Resolution |
|---|----------|-------|-----|------------|
| 1 | Should we warn users when a link is opened from a different browser/device than the request? Or block? | `<@product>` | `<YYYY-MM-DD>` | `<TBD>` |
| 2 | What email provider do we use? Are transactional emails covered by existing SendGrid contract? | `<@devops>` | `<YYYY-MM-DD>` | `<TBD>` |
| 3 | Do we migrate existing users to magic-link-only, or keep passwords forever? | `<@cto>` | `<YYYY-MM-DD>` | `<TBD>` |

---

## 9. Sign-Off

> Both product and engineering must approve before development begins.

| Role | Name | Decision | Date |
|------|------|----------|------|
| Product owner | `<@product-owner>` | `<Approved / Changes requested>` | `<YYYY-MM-DD>` |
| Engineering lead | `<@eng-lead>` | `<Approved / Changes requested>` | `<YYYY-MM-DD>` |
| Security reviewer | `<@security>` | `<Approved / Changes requested>` | `<YYYY-MM-DD>` |

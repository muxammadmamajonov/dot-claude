# User Roles & Permissions

> **What this is:** the authorization model — who can do what, on which resources, under what conditions. Filled in by the **business-analyst** + **security-auditor** agents. Drives access-control implementation and the [security checklist](../checklists/security.md). Default posture: **deny by default; grant explicitly.**

---

## 1. Roles
> List every role/persona that interacts with the system, including system/service accounts.

| Role | Description | Trust level | Notes |
|------|-------------|-------------|-------|
| `<owner/admin>` | `<full control of a tenant>` | High | `<MFA required>` |
| `<member>` | `<standard user>` | Medium | |
| `<guest/viewer>` | `<read-only>` | Low | |
| `<service:billing>` | `<machine account>` | Scoped | `<token-based>` |

## 2. Permissions matrix
> Rows = roles, columns = resource:action. Mark ✓ allow, ✗ deny, ⚠ conditional (note the condition).

| Resource : Action | owner | member | viewer | service |
|-------------------|:-----:|:------:|:------:|:-------:|
| `project:create` | ✓ | ✓ | ✗ | ✗ |
| `project:delete` | ✓ | ⚠ owns | ✗ | ✗ |
| `billing:read` | ✓ | ✗ | ✗ | ✓ |
| `user:invite` | ✓ | ⚠ if seats left | ✗ | ✗ |

> ⚠ conditions: `<"owns" = actor is the resource owner; "if seats left" = plan limit not exceeded>`

## 3. Role hierarchy & inheritance
> Does a higher role inherit lower-role permissions? Avoid surprises — state it explicitly.

> `<owner ⊃ member ⊃ viewer>` (each inherits all permissions of the role below). Service roles do **not** inherit.

## 4. Scoping & multi-tenancy
> What boundary isolates data? Permissions are evaluated within this scope.

- **Tenancy boundary:** `<organization / workspace / account>`
- **Cross-tenant access:** `<forbidden unless explicit share grant>`

## 5. Sensitive actions (step-up required)
> Actions that need re-authentication, MFA, or human approval regardless of role.

- `<delete account, export all data, change payout bank, transfer ownership>` → `<require re-auth + email confirmation>`

## 6. Enforcement points
> Where authorization is checked. Must be server-side; client checks are UX only.

- `<API middleware on every route; row-level security in DB; never trust client-sent role>`

## 7. Open questions
- [ ] `<question requiring founder decision, e.g. "can members invite other members?">`

---
**Done when:** every role is defined, the matrix covers every resource:action with no blank cells, conditional grants name their condition, sensitive actions require step-up, and enforcement is server-side and default-deny. Verify against [security checklist](../checklists/security.md).

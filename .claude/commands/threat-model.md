---
description: Run a STRIDE threat model; output docs/security/threat-model.md and feed findings into the security checklist.
argument-hint: [scope: full | api | auth | data | infra — optional]
---

# /threat-model

## Purpose
Produce a structured STRIDE threat model for the project. Identify trust boundaries, data flows, assets, and entry points; enumerate threats per STRIDE category; assess likelihood and impact; recommend mitigations ranked by priority. Feed findings directly into `.claude/checklists/security.md` so audit gates reflect the real threat surface, not a generic template.

## When to use
- Before or during stage 4 (Spec) on any new project — threat modeling is cheapest when the design is still malleable.
- Required gate before `/audit-security` on high-risk projects (payments, auth, PII/PHI, regulated data).
- After a significant architecture change (new external integration, new data store, auth model change, new user role).
- When a penetration test is planned — gives testers a structured attack surface map.
- When entering a new compliance regime (SOC 2, PCI-DSS, HIPAA, ISO 27001).

## Workflow

### Step 0 — Load context
1. Read `.claude/agents/quality/security-auditor.md` — adopt its role and constraints for this command.
2. Read `.claude/skills/security/SKILL.md` — load threat modeling patterns, STRIDE definitions, and fix guidance.
3. Read `.claude/templates/threat-model.md` — this is the output skeleton to fill in.
4. If an argument was given (`full | api | auth | data | infra`), scope the model to that surface. Default is `full`.
5. Read `docs/state/project-type.md` (if present) for risk class and project type. If absent, infer from the codebase.
6. Read existing specs: `docs/specs/`, `docs/architecture.md`, `docs/decisions/`, any data-model or API spec under `docs/`. These define the intended design; the threat model must reflect it.

### Step 1 — Build the system picture
Map the system before assigning any threats. This is the foundation — a wrong map produces a useless model.

**1a. Identify assets** (what an attacker would want):
- User data: PII, credentials, session tokens, payment info, health records.
- Business data: proprietary algorithms, pricing, customer lists, audit logs.
- System resources: compute, storage, secrets, signing keys, certificates.
- Availability: uptime of critical paths, SLA obligations.

**1b. Identify trust boundaries** (where privilege or identity changes):
- Internet ↔ edge/CDN/API gateway.
- API gateway ↔ backend services.
- Backend ↔ database / queue / blob storage.
- Backend ↔ third-party services (payment processor, auth provider, email, SMS, analytics).
- Admin interface ↔ regular user interface.
- Mobile client ↔ backend API.
- CI/CD pipeline ↔ production environment.
- Any cross-tenant or cross-org boundary.

**1c. Map data flows** across each boundary (number each DFD element):
- DFD element types: External Entity (EE), Process (P), Data Store (DS), Data Flow (DF).
- For each flow note: protocol, authentication mechanism, encryption in transit, payload sensitivity.

**1d. Identify entry points** (where an attacker can inject input):
- HTTP/WebSocket endpoints (unauthenticated and authenticated).
- File upload surfaces.
- Webhook receivers (inbound from third parties).
- CLI arguments, environment variables, config files.
- Message queue consumers.
- SDK/library APIs exposed to users.
- Build pipeline inputs (SCM, package registries, container registries).

### Step 2 — Enumerate STRIDE threats
For each trust boundary and entry point from Step 1, systematically enumerate threats using the STRIDE framework. Assign a unique ID (T-001, T-002 …).

| STRIDE category | Question to ask | Examples |
|---|---|---|
| **S**poofing | Can an attacker impersonate a legitimate user, service, or component? | Forged JWT, DNS spoofing, SSRF to internal metadata |
| **T**ampering | Can an attacker modify data in transit or at rest without detection? | Unsigned webhooks, missing HMAC, writable S3 bucket |
| **R**epudiation | Can an attacker deny performing an action because logs are absent or forgeable? | No audit log on admin actions, mutable log storage |
| **I**nformation Disclosure | Can an attacker read data they should not? | Verbose error messages, unencrypted backups, over-permissioned IAM |
| **D**enial of Service | Can an attacker degrade or eliminate availability? | No rate limiting, resource exhaustion, ReDoS, large file upload |
| **E**levation of Privilege | Can an attacker gain capabilities beyond their role? | IDOR, JWT alg:none, broken RBAC, path traversal |

For each threat, record:
- **ID** (T-NNN)
- **Category** (S/T/R/I/D/E)
- **Affected component** (DFD element ID from Step 1)
- **Attack scenario** — one concrete sentence describing how an attacker exploits this.
- **Likelihood** (High / Medium / Low) — how easy is this to exploit given current controls?
- **Impact** (Critical / High / Medium / Low) — what is the worst realistic outcome?
- **Risk** = Likelihood × Impact → Critical / High / Medium / Low (use the matrix below).
- **Existing controls** — what mitigations are already in place?
- **Recommended mitigation** — concrete, actionable change (library, config, pattern, or architecture change).
- **Priority**: P0 (must fix before launch), P1 (fix within sprint post-launch), P2 (hardening), P3 (track).

Risk matrix:
| | Impact: Critical | Impact: High | Impact: Medium | Impact: Low |
|---|---|---|---|---|
| **Likelihood: High** | Critical | High | High | Medium |
| **Likelihood: Medium** | High | High | Medium | Low |
| **Likelihood: Low** | High | Medium | Low | Low |

### Step 3 — Prioritize and deduplicate
1. Sort all threats by Risk (Critical first), then by ease of exploitation.
2. Deduplicate: if two threats share the same root cause, merge them into one entry and note both attack vectors.
3. Separate structural threats (require architecture changes — must surface to user as STOP items) from tactical threats (can be mitigated in code/config without redesign).

**STOP — Present the structural threats to the user before writing the output document.** List each structural threat's ID, title, and the architectural change required. Ask: "These threats require design changes before implementation. Do you want to adjust the architecture before we continue, or document them as accepted risks?"

Wait for user acknowledgment before proceeding to Step 4.

### Step 4 — Write threat model document
Fill in `.claude/templates/threat-model.md` and write the completed document to `docs/security/threat-model.md`. The document must include:
1. Executive summary (risk posture in 3–5 sentences; highest-risk areas called out).
2. System picture: assets, trust boundaries, DFD (text representation if diagram not feasible), entry points.
3. Threat register: full table of all threats (ID, STRIDE, component, scenario, likelihood, impact, risk, controls, mitigation, priority).
4. Mitigation roadmap: threats grouped by priority (P0 / P1 / P2 / P3) with recommended owner (engineering, devops, security, architecture).
5. Assumptions and out-of-scope items (what this model does NOT cover).
6. Review date: when this model should next be revisited.

### Step 5 — Update the security checklist
Open `.claude/checklists/security.md`. For each P0 and P1 threat from the model:
- Find the matching checklist item if it exists; mark it unchecked (it is now a confirmed gap, not just a template item).
- If no matching checklist item exists, append the threat as a new item with its T-NNN ID and priority tag.

This ensures `/audit-security` picks up every identified threat as an explicit checklist gate.

### Step 6 — Optionally generate decision records
For any P0 threat that requires an architectural change, create a decision record at `docs/decisions/adr-threat-<T-NNN>-<date>.md` using `.claude/templates/decision-record.md`. Title: `ADR: Mitigation for <T-NNN> — <threat title>`. Record the options considered and the chosen mitigation approach.

## Agents used
- `.claude/agents/quality/security-auditor.md` — owns this workflow end-to-end; drives threat enumeration, risk scoring, and checklist integration.

## Skills used
- `.claude/skills/security/SKILL.md` — STRIDE patterns, attack scenarios by project type, mitigation patterns per vulnerability class.

## Expected outputs
| Output | Path |
|---|---|
| Threat model document | `docs/security/threat-model.md` |
| Updated security checklist | `.claude/checklists/security.md` (in-place) |
| Architectural decision records (P0 threats) | `docs/decisions/adr-threat-<T-NNN>-<date>.md` |

## Stop conditions
- No architecture documentation and no source code to read → cannot build the system picture; **STOP** and request: "Share the architecture (even a rough description or diagram) so I can map trust boundaries accurately."
- A structural threat requires fundamental redesign (e.g., multi-tenant isolation is absent, auth is bypassed by design) → **STOP after Step 3**, document the threat as Critical P0, and require explicit user direction before writing the rest of the model. Do not proceed to Step 4 until the user acknowledges.
- Secrets found while reading source for context → **STOP immediately**, alert the user per §8 of CLAUDE.md; do not include secrets in the threat model document.
- Scope argument given but no matching surface found (e.g., `auth` scope requested but no auth layer exists) → note the gap as a Critical finding (no auth where auth is expected) and continue with `full` scope.

## Final report format
```
## Threat Model Report — <date>

**Project:** <name>  |  **Scope:** <full|api|auth|data|infra>
**Risk class:** <high|medium|low>  |  **Modeler:** Claude Code (security-auditor role)

### Risk posture summary
<3–5 sentences: overall risk level, hottest attack surfaces, most critical gaps>

### System picture
**Assets (N):** <comma-separated top assets>
**Trust boundaries (N):** <comma-separated boundaries>
**Entry points (N):** <comma-separated entry points>

### Threat register summary
| Priority | Count | Categories |
|---|---|---|
| P0 Critical | N | S, E, I |
| P1 High | N | T, D |
| P2 Medium | N | R, I |
| P3 Low | N | D |

### P0 — Must fix before launch
| ID | Category | Component | Risk | Mitigation |
|---|---|---|---|---|
| T-001 | E | Auth service | Critical | <one-line mitigation> |

### Structural threats (require design changes)
| ID | Title | Change required |
|---|---|---|
| T-003 | No tenant isolation | Introduce row-level security in DB |

### Mitigation roadmap
- **Sprint 1 (P0):** T-001, T-002 — assigned to backend-engineer + security-auditor review.
- **Sprint 2 (P1):** T-004, T-007 — assigned to devops-engineer.
- **Backlog (P2/P3):** T-010–T-015 — tracked in docs/security/threat-model.md.

### Security checklist impact
<N> new items added to .claude/checklists/security.md.
<N> existing items confirmed as gaps (unmarked).

### Next steps
1. Address all P0 threats before `/audit-security`.
2. Re-run `/threat-model` after any significant architecture change.
3. Review this model at: <ISO date 6 months from now or after next major release>.
```

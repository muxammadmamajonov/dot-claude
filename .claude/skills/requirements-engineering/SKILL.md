---
name: requirements-engineering
description: Turn confirmed discovery and classification into testable functional and non-functional requirements, with acceptance criteria and traceability. Activate after discovery/classification and before architecture and build, or whenever a feature needs precise, verifiable specs instead of a vague request.
---

# Requirements Engineering

## When to use
- After discovery (`.claude/skills/discovery/SKILL.md`) and classification (`.claude/skills/project-classification/SKILL.md`) are confirmed and their artifacts (`docs/discovery.md`, `docs/classification.md`) are written and agreed upon.
- When a feature request is too vague to build or test against ("make it user-friendly", "support payments", "handle edge cases").
- Before architecture and data modeling — both disciplines consume requirements as their input contract. Proceeding without them guarantees rework.
- When an inherited codebase has undocumented behavior: reverse-engineer requirements from code and tests, then validate with the product owner before changing anything.
- When a change request arrives mid-project: re-enter this skill, trace the change to existing requirements, flag any FRs/NFRs that must be updated, and re-gate.

## Workflow

### 1. Restate and bound the scope
Pull the MVP scope, non-goals, personas, and constraints from `docs/discovery.md` and `docs/classification.md`. Write a one-paragraph scope statement at the top of the requirements document: what is in scope for this iteration, what is explicitly out of scope, and which personas are in scope. Get agreement (or record the assumption) before writing a single requirement. Scope drift at requirement time is free to fix; scope drift at build time is expensive.

### 2. Decompose capabilities into functional requirements (FRs)
For each capability in scope, write one or more atomic, numbered FRs using this pattern:

```
FR-NNN [Priority] [Area]
Actor: <who initiates>
Trigger: <what event or condition starts it>
Behavior: <what the system does — observable, not internal>
Result: <the post-condition the actor can verify>
```

Group FRs by user goal or domain area (auth, payments, search, notifications, etc.). Every FR must be independently testable. If a sentence contains "and" connecting two verifiable outcomes, split it into two FRs. If it contains "or", choose one meaning or write two separate FRs. Aim for fewer, sharper FRs over many vague ones.

**Decision point — ambiguous capability:** If the capability has multiple plausible interpretations, pick the one most consistent with discovery and record the others as `ASSUMPTION:`. Surface compound assumptions (ones with high blast-radius) to the user before proceeding.

### 3. Write user stories with Given/When/Then acceptance criteria
For every user-facing FR, write a story and at least one passing and one failing acceptance criterion:

```
Story: As a <role>, I want <goal>, so that <benefit>.

Scenario: <name>
  Given <precondition — system state and user state>
  When  <action the actor takes>
  Then  <observable outcome that can be asserted by a test>

Scenario: <edge/failure case>
  Given ...
  When  ...
  Then  ...
```

Acceptance criteria are the spec for both implementation and automated testing. A criterion is good if a QA agent could write a test for it without asking you a single question. If the criterion still requires interpretation, rewrite it.

### 4. Derive non-functional requirements (NFRs) — quantify everything
Open `docs/classification.md` and systematically walk every cross-cutting concern flagged. For each one that is in scope, write a quantified NFR:

| NFR-NNN | Category | Requirement | Threshold | How measured | Priority |
|---------|----------|-------------|-----------|--------------|----------|

Required categories (adapt thresholds to the project's actual targets):

- **Performance** — p95 latency per endpoint/screen, throughput (req/s, events/s), cold-start budget (for serverless/mobile), render budget (for UI: FCP, LCP, INP, CLS), batch job SLA.
- **Scalability** — peak concurrent users, data volume ceiling, horizontal vs. vertical scaling model, stateless/stateful boundary.
- **Availability** — uptime SLA (%), RTO (max acceptable downtime), RPO (max data loss window), planned maintenance window.
- **Security** — authentication model (none / session / JWT / OAuth2 + PKCE / mTLS), authorization model (RBAC / ABAC / ACL), encryption at rest and in transit, secrets management approach, vulnerability scanning cadence. See `.claude/checklists/security.md`.
- **Privacy/compliance** — applicable regimes (GDPR, CCPA, HIPAA, PCI-DSS, SOC2, WCAG, local law). Per-regime: data minimization, retention periods, deletion/portability rights, audit log requirements.
- **Accessibility** — applicable standard (WCAG 2.2 AA minimum for any human UI), platform-specific guidelines (APCA, ARIA, iOS/Android a11y APIs). See `.claude/checklists/accessibility.md`.
- **Reliability** — error budget, max acceptable error rate, retry/idempotency contract, graceful degradation behavior under partial failure.
- **Observability** — what must be logged (structured, with trace IDs), what metrics are emitted, what traces are captured, what alerting thresholds apply, what health check endpoints are required.
- **Maintainability** — code coverage floor, max cyclomatic complexity, dependency review cadence, upgrade cadence.
- **Internationalization** — languages/locales required at launch vs. later, right-to-left support, date/number/currency formatting, timezone handling.

"Fast/secure/scalable" without a number is not a requirement — it is a wish. Any NFR without a threshold and a measurement method is invalid.

### 5. Enumerate edge cases, error behavior, and invariants
For each FR, explicitly list:

- **Empty/null inputs:** what happens when required fields are missing, strings are empty, lists are empty.
- **Invalid inputs:** out-of-range values, wrong types, malformed formats (email, UUID, date).
- **Permission boundary:** what happens when an actor tries an action they are not authorized for (do not just say "403 is returned" — say what the user sees and what is logged).
- **Concurrency/race conditions:** what happens when two actors trigger the same mutation simultaneously. Define the conflict resolution policy (last-write-wins, optimistic locking, queue serialization).
- **Idempotency:** for any operation that can be retried (especially payments, emails, webhook deliveries), define the idempotency contract: which key, how long the dedup window is, what happens on a duplicate.
- **Partial failure:** for multi-step operations, define which steps are atomic and what compensating action runs if a step fails after earlier steps have committed.
- **Degraded dependency:** if a third-party service (payment gateway, email, maps API) is unavailable, what does the system do? Queue for later? Show a friendly error? Block?

Edge cases discovered here become test cases in `.claude/checklists/qa.md`. Do not leave them implicit.

### 6. Apply MoSCoW prioritization against the MVP boundary
Tag each FR and NFR:

- **Must** — launch cannot happen without it; product is broken or non-compliant.
- **Should** — high value, significant pain if missing, include in v1 if time allows.
- **Could** — nice-to-have, can slip to v1.1 without material harm.
- **Won't (v1)** — explicitly deferred; prevents scope creep if written down.

Mark the MVP cut-line clearly. Everything above it is v1; everything below goes in the backlog. If the cut-line is contested, surface to the user — it is a business decision.

### 7. Build the traceability matrix
Every requirement must link:
- **Backward** — to the discovery goal or business rule that motivated it. Orphaned requirements (no business reason) are scope creep candidates.
- **Forward** — to the architecture component, data model entity, API endpoint, or UI screen that will implement it; and to the test case that will verify it.

Maintain a lightweight matrix. At minimum:

| req id | source (discovery) | implements (architecture ref) | verified by (test ref) | status |
|--------|--------------------|-------------------------------|------------------------|--------|

Update this matrix when requirements change. An untraced requirement is invisible to auditors, test automation engineers, and future maintainers.

### 8. Resolve ambiguity — ask only business-critical questions
Before finalizing, audit the draft for:
- Vague verbs: "manage", "handle", "support", "process", "allow" — replace with observable system behavior.
- Implicit quantifiers: "fast", "secure", "simple", "many" — replace with numbers.
- Unstated actors: "the system" without specifying who can trigger it.
- Missing error paths: FRs with only happy-path text.

For gaps that are business-critical (affect money, compliance, data privacy, or irreversible behavior), ask the user. For gaps that have a defensible default, pick the default, record it as `ASSUMPTION:`, and continue. Batch questions into one pass — do not drip them one at a time.

### 9. Record and hand off
Finalize the document at `docs/requirements.md` using `.claude/templates/product-spec.md`. Run the `.claude/checklists/requirements.md` gate before declaring this stage done. Then hand off to:
- `.claude/skills/architecture/SKILL.md` — consumes FRs for component design and NFRs for style/style selection.
- `.claude/skills/data-modeling/SKILL.md` — consumes entity FRs and retention/compliance NFRs.
- `.claude/skills/api-design/SKILL.md` — consumes the FR/edge-case/idempotency spec for contract design.
- `.claude/skills/security/SKILL.md` — consumes security and privacy NFRs for threat modeling.

## Standards

- **Do** make every requirement atomic and independently testable — one verifiable statement each. If you cannot write a test for it, rewrite it.
- **Do** quantify all NFRs with concrete thresholds, units, and the measurement method (load test, synthetic monitor, static analysis, audit log query).
- **Do** write acceptance criteria that a QA agent could automate without further clarification. Given/When/Then with concrete values, not adjectives.
- **Do** state non-goals as explicitly as goals. "We will not support X in v1" prevents scope creep and aligns team expectations.
- **Do** keep requirements solution-free — specify what the system must do and the observable outcome, not how it works internally. Implementation belongs in architecture.
- **Do** trace every requirement to a business source. If you cannot find one, the requirement is a candidate for deletion.
- **Do** enumerate at least one failure scenario per FR before calling it complete.
- **Do not** bundle multiple behaviors into one requirement. The word "and" connecting two verifiable outcomes is a splitting signal.
- **Do not** invent requirements the business never asked for. Every FR traces to discovery.
- **Do not** leave NFRs implicit. Unstated performance, security, and accessibility expectations cause the most expensive rework — they are discovered at audit or in production.
- **Do not** write an "acceptance criterion" that merely restates the requirement in different words. It must define a pass/fail condition.
- **Do not** skip the edge-case matrix. The cost of specifying an edge case is a line of text; the cost of discovering it in production is an incident.

## Common mistakes to avoid

- **Vague verbs with no observable outcome.** "The system shall handle errors gracefully" tells nobody anything. "When a payment gateway returns a 5xx, the system shall display `docs/specs/error-messages.md#ERR-PAY-001`, log the failure with the trace ID, and allow the user to retry without re-entering card data" is a requirement.
- **Skipping NFRs entirely.** "We'll think about performance/security later" is how you fail an audit at launch. The cost to retrofit observability, rate limiting, or encryption into a shipped system is 10x writing them as requirements up front.
- **Acceptance criteria that test the requirement, not the behavior.** "Given the user is logged in / When they submit the form / Then it should work" is not testable.
- **Specifying the happy path only.** Almost all production bugs live in the paths you didn't think about. The edge-case matrix exists to force this thinking early.
- **Gold-plating.** Specifying NFR thresholds 10x stricter than the business actually needs. p99 < 50ms on a backoffice admin tool nobody cares about wastes engineering capacity and inflates infrastructure cost.
- **Orphaned requirements.** A requirement with no business source and no forward trace exists in a void. It will be built (wasting effort) or dropped (breaking an undiscovered contract).
- **One-pass requirements.** Requirements need a review pass from someone who will write the tests. Walk through each FR with the QA agent role and ask: "Can I automate a test for this right now?" If the answer is no, fix it before handing off.
- **Using "the user" ambiguously.** In a system with multiple personas (admin, customer, guest, API client), "the user" is undefined. Name the actor explicitly in every FR.

## Output format

A completed `.claude/templates/product-spec.md` saved at `docs/requirements.md` containing:

1. **Scope statement** — in-scope capabilities, personas, and explicit out-of-scope items for this iteration.
2. **Functional requirements table** — numbered FRs grouped by domain area, each with actor/trigger/behavior/result and a priority tag.
3. **User stories with acceptance criteria** — one story block per user-facing FR, with at least one passing and one failing Given/When/Then scenario per story.
4. **Non-functional requirements table** — `NFR-id | category | requirement | threshold | how measured | priority`, covering all in-scope categories from step 4.
5. **Edge-case and error matrix** — per FR, the empty/invalid/auth/concurrency/partial-failure/degraded-dependency cases and the defined system response.
6. **Assumptions log** — all decisions made on behalf of the user with rationale and how to reverse.
7. **Traceability matrix** — `req id | source goal | architecture ref | test ref | status`.
8. **MoSCoW priority summary** — the MVP cut-line and the explicit v1 / deferred split.

## Related checklists
- `.claude/checklists/requirements.md`
- `.claude/checklists/qa.md`
- `.claude/checklists/security.md`
- `.claude/checklists/accessibility.md`
- `.claude/checklists/performance.md`

## Related agents
- `.claude/agents/core/business-analyst.md`
- `.claude/agents/core/requirements-engineer.md`
- `.claude/agents/core/system-analyst.md`
- `.claude/agents/quality/qa-engineer.md`
- `.claude/agents/quality/security-auditor.md`
- `.claude/agents/quality/privacy-compliance-auditor.md`

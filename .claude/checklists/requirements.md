# Requirements Checklist
Passing this gate proves requirements are complete, unambiguous, testable, and agreed before any design or implementation begins — no hidden assumptions, no implicit scope, no "we'll figure it out later." Items are severity-tagged P0/P1/P2/P3.

## P0 — Blockers (must pass before proceeding)

- [ ] Every feature or capability has a single, clear purpose stated in one sentence — no compound "X and Y" requirements; split compound statements into separate requirements.
- [ ] Each requirement has at least one acceptance criterion that is binary (pass/fail), specific, and verifiable by a tester who was not present during authoring — no "fast," "nice," "intuitive," or "reasonable."
- [ ] All actors are named and their permissions are defined: human users (by role), admin types, automated jobs/schedulers, external systems, and third-party integrators. No unnamed "the system" doing things.
- [ ] Every business rule is written out explicitly: calculations, eligibility logic, state-machine transitions, validation thresholds, pricing formulas. None are left implicit in prose or assumed from domain knowledge.
- [ ] All external dependencies are named with: service name, version/API contract used, rate limits, auth mechanism, SLA, and the specified fallback behavior when the dependency is unavailable or returns an error.
- [ ] Data inputs and outputs for every workflow are described with: format (JSON, CSV, binary, protobuf), field types, size limits, valid ranges, required vs. optional, and encoding/locale assumptions.
- [ ] Out-of-scope items are explicitly listed — at minimum five per feature area — to prevent scope creep and misaligned expectations during build.
- [ ] The MVP feature set is frozen and labelled separately from post-MVP; no post-MVP work is designed or estimated until the MVP is delivered.
- [ ] Conflicting requirements are identified, flagged, discussed, and resolved — zero silent contradictions remain. Resolution is recorded in a decision record (`../templates/decision-record.md`).
- [ ] Every error state and failure mode has a defined behavior: what the user sees, what the system logs, whether the operation retries and how many times, and the recovery path. Happy-path-only requirements are not accepted.
- [ ] Regulatory and compliance constraints are documented per jurisdiction: GDPR (data subject rights, retention, DPA), HIPAA (PHI handling, BAA), PCI-DSS (scope isolation, tokenization), WCAG 2.2 AA (for any UI), local data-residency laws, financial regulations (KYC/AML, CFTC, MiFID II as applicable). "No compliance requirements" must be explicitly stated.
- [ ] Requirements are traceable: each links to a business objective or user story so engineering can always answer "why does this exist."

## P1 — Important (fix before handoff to engineering)

- [ ] Non-functional requirements are quantified for: API response latency (target p50/p95/p99), throughput (requests/second or transactions/hour), uptime SLA (e.g., 99.9% = 8.7 hours downtime/year), maximum payload sizes, peak concurrent users, data retention period, and recovery time objective (RTO) / recovery point objective (RPO).
- [ ] Priority and dependency order is set: each requirement specifies its predecessors so engineering can phase delivery without circular dependencies or rework.
- [ ] Localization and internationalization needs are decided: supported languages, date/time/number formats, currency handling, RTL layout support, plural forms, locale-specific legal text, and character encoding (UTF-8 assumed unless noted).
- [ ] Security requirements are explicit for each workflow: authentication method, session duration and invalidation, authorization model (RBAC, ABAC, ownership-based), rate limiting per endpoint, audit logging of sensitive operations, and data-at-rest/in-transit encryption requirements.
- [ ] Performance degradation behavior is specified: what must the system do when under load (queue requests, return 429, shed non-critical work, switch to read-only mode)? This is a requirements question, not only an architecture one.
- [ ] Accessibility requirements are specified for every user-facing surface: WCAG 2.2 level (A/AA/AAA), keyboard navigation mandatory, screen-reader support (ARIA), minimum color contrast ratios, and any platform-specific standards (iOS Dynamic Type, Android TalkBack).

## P2 — Hardening / nice-to-have

- [ ] Requirements are version-controlled alongside code in `docs/specs/` and linked from the project README; each requirement has a stable ID (e.g., `REQ-AUTH-003`).
- [ ] A domain glossary is defined and agreed — all actors, entities, states, and actions use the same terminology across the spec, code, database schema, and UI copy.
- [ ] Core assumptions behind major requirements are backed by user research, data, or validated hypotheses — not pure speculation. Unvalidated assumptions are logged in `docs/state/assumptions.md`.
- [ ] Capacity and load projections are reviewed by the team for realism; non-functional requirements are not copy-pasted from a generic template but sized to the actual expected usage curve.
- [ ] Future extensibility points are noted so the architecture can leave the right seams open (plugin hooks, multi-tenancy, white-labeling, internationalisation, event streaming) without over-engineering the v1.

## P3 — Post-launch / backlog (track and revisit after launch; never blocks shipping)

- [ ] Requirements are audited against actual shipped behaviour 4–8 weeks post-launch: every acceptance criterion is verified against production metrics or session recordings, and any criterion that was never met or was silently changed is updated in `docs/specs/`.
- [ ] Domain glossary is reconciled with the terms that emerged organically in code, database schemas, and UI copy during build; divergences are resolved and the agreed canonical term is propagated everywhere.
- [ ] Non-functional requirements (latency, throughput, uptime SLA) are re-evaluated against real production load data; targets that proved too loose or too strict are updated with rationale in a decision record.
- [ ] Post-MVP feature backlog is formally triaged now that v1 is live: each deferred item is re-scored against real user demand, technical feasibility, and updated business priorities before entering the next planning cycle.
- [ ] Regulatory requirements that were noted but deferred (e.g., full WCAG AAA, additional data-subject rights flows, multi-jurisdiction compliance) are assigned owners and target milestones.

## How to use
Run at the end of the discovery/interview phase, before handing off to `../agents/core/solution-architect.md` for design. Invoke via `../commands/create-specs.md` or manually before any architecture diagram is drawn. Cross-reference `../checklists/discovery.md` (must already pass) and `../checklists/architecture.md` (runs next). Reference `../skills/requirements-engineering/SKILL.md` for elicitation techniques and `../templates/product-spec.md` / `../templates/business-rules.md` for output format. Reviewer marks each item `[x]` when satisfied or `[-]` when explicitly waived with a written reason and risk classification.

---
name: documentation
description: Use when writing or updating specs, READMEs, API/reference docs, architecture decision records (ADRs), or operational runbooks — and when keeping them current as code changes. Triggers when a decision is made (record an ADR), a feature ships (update spec/reference), an operational procedure is needed (write a runbook), or docs have drifted from reality.
---

# Documentation: Specs, Docs, ADRs, Runbooks

## When to use
- Capturing a feature before build (spec) or its interface after (reference/API docs).
- Recording a significant technical decision and its rationale (ADR).
- Writing an operational procedure for a recurring or emergency task (runbook).
- Onboarding docs (README / getting-started), or fixing docs that no longer match the code.
- When a review, audit, or incident reveals that a critical procedure exists only in someone's head.

Applies to every project type. The artifacts below — spec, reference, ADR, runbook, README — exist whether the project is a web app, an API, a CLI, a game, an embedded device, or an agent system. The *format* adapts to the project; the *discipline* does not.

---

## Workflow

### Step 1 — Pick the right artifact

Choose before writing. Blurring artifact types into one wall of text is the root cause of most documentation problems.

| Artifact | When to use | Template |
|---|---|---|
| **Product/feature spec** | Captures what to build, why, for whom, acceptance criteria, and open questions — written **before** implementation. | `.claude/templates/product-spec.md` |
| **Feature spec** | Scoped to a single feature within a larger product; includes acceptance criteria, edge cases, and rollout notes. | `.claude/templates/feature-spec.md` |
| **ADR (Architecture Decision Record)** | Records a significant technical decision, the alternatives weighed, and the rationale. Immutable once accepted. | `.claude/templates/decision-record.md` |
| **API / interface reference** | Documents a public interface: endpoints, commands, SDK methods, events, schemas. Generated from source when possible. | Inline from OpenAPI / `--help` / typedoc |
| **Runbook** | Step-by-step operational procedure: deploy, rollback, secret rotation, incident response, scaling. Tested like code. | `.claude/templates/runbook.md` |
| **README / getting-started** | Entry point for anyone new to the project: what it is, how to run locally, how to test, where deeper docs live. | Custom; keep under 100 lines |
| **Assumptions log** | Running record of decisions made on behalf of the user, with blast-radius and reversal notes. | `.claude/templates/assumptions-log.md` |
| **Business rules** | Explicit domain rules that govern behavior (pricing tiers, eligibility, SLA definitions). Separate from implementation. | `.claude/templates/business-rules.md` |

If you are tempted to create a new catch-all doc, stop and pick the most specific applicable artifact type instead.

---

### Step 2 — Write the spec before building

For any non-trivial feature or project, the spec must exist before a line of implementation code is written. A spec that trails the code is a description, not a design.

A complete product or feature spec contains:
1. **Problem statement** — what user need or business gap does this address?
2. **Users / personas** — who uses this? What do they know and care about?
3. **Scope** — what is explicitly in scope, and what is explicitly out of scope (both matter equally).
4. **Requirements** — functional ("the system shall…") and non-functional (latency budget, availability target, accessibility level, security constraints).
5. **Acceptance criteria** — concrete, testable conditions that define Done. Written as "given / when / then" or as a checklist. If a criterion cannot be tested, rewrite it until it can.
6. **Open questions** — things not yet decided; owned by a named person with a resolution date.
7. **Out-of-scope risks** — adjacent concerns that were considered and explicitly deferred.

Ask the user only for business-critical inputs (§6 of CLAUDE.md). Document assumptions for the rest, using `.claude/templates/assumptions-log.md`.

---

### Step 3 — Record decisions as ADRs

One ADR per decision. ADRs are the "why we did it this way" that prevents future developers (including the user) from undoing a good decision without understanding what it replaced.

An ADR contains exactly:
- **Date** (when decided).
- **Status**: `proposed` → `accepted` → `superseded by ADR-NNN` / `deprecated`.
- **Context**: the situation and constraints that made a decision necessary.
- **Decision**: the choice made, stated unambiguously.
- **Alternatives considered**: what else was evaluated, and why it was rejected.
- **Consequences**: what gets better, what gets harder, what new constraints this creates.

ADR rules:
- **Immutable once accepted.** Never edit the body of an accepted ADR. To revise, write a new ADR and set the old one's status to `superseded by ADR-NNN`.
- **Short.** An ADR that requires 10 minutes to read is too long; edit it down.
- **Dated.** A decision made without a date cannot be interpreted in context of what was known then.
- Store at `docs/decisions/ADR-NNN-short-title.md`.

Trigger an ADR for: storage paradigm choices, framework selections, auth model, deployment topology, significant API contract decisions, security control choices, and any "we considered X but chose Y" conversation.

---

### Step 4 — Document the interface as you build

Public interfaces — APIs, CLI commands, SDK methods, event schemas, IPC contracts — must be documented at the point of creation, not as a follow-up.

**Generate from source where possible:**
- REST API: OpenAPI / Swagger spec colocated with the router, from which reference docs and client SDKs are derived. A hand-maintained API reference immediately diverges.
- CLI: `--help` text in the command source; extract it to `docs/cli.md` as part of the build.
- SDK / library: doc comments (JSDoc, Rustdoc, Godoc, etc.) that generate reference pages.
- Event bus / message schemas: JSON Schema or Protobuf definitions in a `schemas/` directory are the canonical reference.

Every interface doc must include:
- The contract: parameters/flags, types, required vs. optional, defaults.
- Return/output: shape, types, possible error codes/messages.
- Auth/authorization requirements.
- At least one real, working example — not pseudo-code.
- Edge cases and what happens at boundary conditions.

---

### Step 5 — Write runbooks for operations

A runbook is a recipe that someone who has never performed an operation before can follow successfully under pressure. Write every runbook to that standard.

**When to write a runbook:**
- Any deploy or rollback procedure.
- Rotating secrets or credentials.
- Database backup, restore, and point-in-time recovery.
- Responding to a known failure mode (high error rate, out-of-memory, full disk, certificate expiry).
- Scaling up or down (horizontal or vertical).
- Onboarding a new service or dependency.
- Any procedure that has been performed manually more than once.

**A runbook must contain:**
1. **Purpose** — what does running this accomplish?
2. **Trigger** — what condition or event should cause someone to run this?
3. **Prerequisites** — access, tools, and environment state required before starting.
4. **Steps** — numbered, with exact commands (not "restart the service" but `systemctl restart my-service && systemctl status my-service`). Include the expected output after each step so the operator knows it worked.
5. **Verification** — how to confirm the operation succeeded. Include the exact check and its expected result.
6. **Rollback** — what to do if something goes wrong mid-procedure. Numbered steps, same standard as the forward path.
7. **Escalation** — who to contact and how if the runbook fails to resolve the situation.

**Test every runbook** by following it exactly in a staging environment. A runbook that has never been followed is a hypothesis, not a procedure.

---

### Step 6 — Keep a current README

The README is the contract between the project and everyone who encounters it. It must always reflect the current state.

A minimal README contains:
- **One-line description** — what this is and who it is for.
- **Quick start** — how to run it locally in 5 steps or fewer. Every step tested.
- **Testing** — how to run the test suite.
- **Deployment** — pointer to the deployment runbook or one-sentence summary.
- **Architecture / structure** — brief (3–5 bullet) orientation to the repo layout and key concepts.
- **Where to go next** — links to deeper docs (spec, ADRs, API reference, runbooks).

The README should not contain: the full API reference, step-by-step deployment details, or a history of decisions. Those belong in their respective artifact types. Link to them.

---

### Step 7 — Tie docs to code changes

Documentation debt is created one merged PR at a time, when code changes outpace doc updates. Eliminate it at the source:

- **Same PR rule**: any PR that changes behavior, interface, configuration, or operational procedure must update the relevant doc in the same PR. A doc update is not a follow-up task.
- **Review gate**: treat missing or contradictory docs as a review blocker, the same as a failing test.
- **Automated drift detection**: where possible, auto-generate docs from source (OpenAPI, typedoc, CLI `--help`) so drift is structurally prevented, not just discouraged.
- **Date and version sensitive content**: docs that contain version numbers, URLs, or time-bounded claims must include the date they were last verified. Undated time-sensitive content is assumed stale.

---

### Step 8 — Prune actively

Stale documentation causes more harm than no documentation — it confidently misleads. Prune on a cadence:

- When a feature is removed or changed: update or delete the doc immediately, in the same PR.
- When reviewing a PR: note any docs the change renders stale and update them.
- Quarterly: review the `docs/` directory index; mark any doc not updated in 90 days for verification or deletion.
- Superseded ADRs: mark status, do not delete — the history is valuable.
- Outdated runbooks: fix or delete. A runbook that fails silently is a liability.

If a doc cannot be kept current (e.g., a reference auto-generated from source), ensure the generation pipeline is part of the CI build so staleness is caught automatically.

---

## Standards

- **Do** write for the reader who arrives with zero context; lead with the purpose of the document, then the specifics.
- **Do** keep docs next to the code in VCS, updated in the same change that alters behavior.
- **Do** prefer generated reference docs (OpenAPI, CLI help, typed schemas) over hand-maintained copies.
- **Do** make ADRs immutable and dated; supersede with a new ADR instead of editing history.
- **Do** include a concrete, runnable example in every how-to or reference doc.
- **Do** make runbooks literal and testable — exact commands, expected output, verification step, and rollback.
- **Do** state assumptions and open questions explicitly rather than implying false certainty.
- **Do** store all generated artifacts under `docs/` in the project, never under `.claude/`.
- **Do not** write filler sentences ("this section describes…") or ship placeholder/TODO content in public-facing docs.
- **Do not** duplicate the same fact in multiple documents; write it once and link to it.
- **Do not** include secrets, tokens, internal hostnames, or real PII in docs or examples.
- **Do not** let docs lag behind code; stale docs erode trust, cause incidents, and waste the next reader's time.
- **Do not** mix artifact types in one file — a doc that is half spec, half runbook, half ADR serves no use case well.

## Common mistakes to avoid

- **The trailing doc**: updating docs in a separate, later task that never happens. Same-PR discipline is the only reliable fix.
- **The omnibus document**: one giant file containing spec, reference, and operational procedures — nobody can find anything, and everything gets stale at different rates.
- **Hand-copied reference docs**: API or CLI docs typed from memory instead of generated from source; they diverge on the first code change.
- **Vague runbooks**: "restart the service" instead of the exact systemctl/kubectl/docker command, the expected output, and how to verify it worked. Vague runbooks fail at 2 AM.
- **Edited ADRs**: changing an accepted ADR in place destroys the decision history and the rationale for the current state. Always supersede.
- **Placeholder content in shipped docs**: a section that says "TODO: describe X" actively misleads readers into thinking there is no information, or that something is missing from the implementation.
- **Secrets in examples**: using real tokens, passwords, internal IPs, or real customer data in example payloads — these end up in VCS, issue trackers, and screenshots.
- **Undated claims**: docs that say "currently" or "as of the latest release" without a date are always of unknown age and reliability.
- **Documentation theater**: writing docs to satisfy a process, then never reading or maintaining them. Docs are a tool for the reader; if they do not serve a real reader, they should not exist.

## Output format

The artifact appropriate for the need, committed under `docs/` (or inline with code for generated reference docs):

| Artifact | Path | Template |
|---|---|---|
| Product spec | `docs/specs/<feature-name>.md` | `.claude/templates/product-spec.md` |
| Feature spec | `docs/specs/<feature-name>.md` | `.claude/templates/feature-spec.md` |
| ADR | `docs/decisions/ADR-NNN-short-title.md` | `.claude/templates/decision-record.md` |
| Runbook | `docs/runbooks/<operation-name>.md` | `.claude/templates/runbook.md` |
| API reference | `docs/api/` or generated to `docs/api/openapi.yaml` | Source-generated |
| README | `README.md` at project root | Custom |
| Assumptions log | `docs/state/assumptions.md` | `.claude/templates/assumptions-log.md` |

Each artifact is: concise, example-bearing, dated where time-sensitive, and committed alongside the code it describes.

## Related checklists
- `.claude/checklists/qa.md`
- `.claude/checklists/production.md`
- `.claude/checklists/security.md`
- `.claude/checklists/devops.md`

## Related agents
- `.claude/agents/core/orchestrator.md`
- `.claude/agents/core/business-analyst.md`
- `.claude/agents/core/documentation-writer.md`
- `.claude/agents/engineering/backend-engineer.md`
- `.claude/agents/quality/qa-engineer.md`

# Assumptions Log

> **What this is:** the running record of every non-trivial decision Claude made on the user's behalf without asking. Required by the constitution ([CLAUDE.md](../CLAUDE.md) §7). It is how the user keeps control without being interrogated: a wrong assumption caught at a stage gate is cheap; caught at launch it is expensive. Copy this to **`docs/state/assumptions.md`** in the project and append to it as you work — newest at the top.

> **Rule of thumb:** if a reasonable senior engineer might have chosen differently, log it.

---

## How to use
> Append one entry per decision **at the moment you make it**, not retroactively. Surface this log to the user at every stage gate. Promote architectural entries to a full [decision-record.md](decision-record.md) (ADR).

## Entry format

> Copy this block per assumption:

### A-`<n>` — `<short title>`  ·  `<YYYY-MM-DD>`  ·  Stage: `<classify|spec|build|…>`
- **Decision:** `<what was chosen>`
- **Why:** `<the reasoning / what made it the safe default>`
- **Alternatives considered:** `<options not taken, 1 line each>`
- **Blast radius if wrong:** `<who/what breaks, how badly>`  ·  **Confidence:** `<high|med|low>`
- **How to reverse:** `<the cheapest path to undo this>`
- **Needs user confirmation?** `<no | yes — flag at next gate>`

---

## Example (delete in real projects)

### A-1 — Use PostgreSQL as the primary datastore · 2026-06-26 · Stage: spec
- **Decision:** PostgreSQL (managed) for all transactional data.
- **Why:** relational model fits the domain; team knows SQL; strong integrity + ecosystem; cheaper than the alternatives at this scale.
- **Alternatives considered:** MongoDB (rejected: relational integrity matters here); DynamoDB (rejected: access patterns still fluid).
- **Blast radius if wrong:** medium — migration to another store is costly once data grows. **Confidence:** high.
- **How to reverse:** abstract data access behind a repository layer now; re-platform later if access patterns demand it.
- **Needs user confirmation?** no.

---

## Open assumptions needing confirmation
> A short list the orchestrator surfaces at each gate — the few that are business-critical or low-confidence.

- [ ] `<A-n: question for the user>`

---
**Done when:** every non-trivial autonomous decision has an entry with reversal cost and blast radius, the log lives at `docs/state/assumptions.md`, and the open-assumptions list is reviewed with the user at each stage gate.

# Business Rules Catalog

> **What this is:** the authoritative list of domain rules, calculations, validations, and policies that govern system behavior — independent of UI or implementation. Filled in by the **business-analyst** and **requirements-engineer** agents from [discovery-answers.md](discovery-answers.md). Engineering must implement these exactly; QA tests against them.

---

## 1. Purpose & scope
> Which part of the domain do these rules cover? Who owns/approves changes?

- **Domain area:** `<e.g. billing, eligibility, pricing>`
- **Rule owner:** `<role who signs off on changes>`

## 2. Rule catalog
> Each rule is atomic, testable, and traceable. Priority: P0 (must, blocks launch) / P1 / P2.

| ID | Rule (plain English) | Condition (When) | Outcome (Then) | Priority | Owner |
|----|----------------------|------------------|----------------|----------|-------|
| BR-1 | `<a user may only ...>` | `<when X is true>` | `<then Y happens>` | P0 | `<owner>` |
| BR-2 | `<orders over $X require ...>` | `<condition>` | `<outcome>` | P1 | `<owner>` |

## 3. Calculations & formulas
> Any computed value (totals, fees, scores, prorations). State the formula, inputs, units, rounding, and currency handling.

- **`<discount total>`** = `<formula>`; rounding: `<half-up to 2dp>`; currency: `<minor units / integer cents>`.

## 4. Validation rules
> What makes input valid. Include field-level and cross-field rules.

| Field / object | Rule | Error if violated |
|----------------|------|-------------------|
| `<email>` | `<must be unique, RFC-5322>` | `<BR-ERR-EMAIL>` |

## 5. State transitions
> For entities with lifecycle (order, ticket, subscription). List allowed transitions; everything else is forbidden.

> `<draft → submitted → approved → fulfilled → closed>`; `<cancelled>` allowed from `<draft|submitted>` only.

## 6. Edge cases & tie-breakers
> The cases that bite in production: empty/zero, concurrency, partial failure, timezone/DST, negative amounts, duplicates.

- `<What happens when two users claim the last item simultaneously?>`

## 7. Compliance & regulatory rules
> Rules imposed by law/standard (GDPR, PCI, HIPAA, tax, accessibility). Tag the regulation.

- `<Retain financial records for 7 years (tax)>`

## 8. Open questions
> Ambiguities only the founder/domain owner can resolve.

- [ ] `<question>`

---
**Done when:** every rule has an ID, condition, outcome, priority, and owner; calculations specify rounding/currency; state machines list only allowed transitions; and each P0 rule maps to a test in [testing-strategy.md](testing-strategy.md).

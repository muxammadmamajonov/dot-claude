# Product Specification

> **What this is:** the single source of truth for *what* we are building and *why*, before any architecture or code. Filled in by the **product-manager** agent with the founder, using answers from [discovery-answers.md](discovery-answers.md). Approved by the user before [/create-roadmap](../commands/create-roadmap.md).

---

## 1. Overview
> One paragraph: what the product is and the core value it delivers.

- **Product name:** `<name>`
- **One-liner:** `<for <audience> who <need>, this is a <category> that <key benefit>>`
- **Problem being solved:** `<the painful problem, in the user's words>`

## 2. Goals & non-goals
> What success looks like for *this* version — and what we are deliberately NOT doing.

| Goals (this version) | Non-goals (explicitly out) |
|---|---|
| `<goal 1>` | `<non-goal 1>` |
| `<goal 2>` | `<non-goal 2>` |

## 3. Target users & personas
> Who uses this? List 1–3 personas with their primary job-to-be-done.

- **`<Persona name>`** — `<role/context>`; needs to `<job>`; success = `<outcome>`.

## 4. Core features
> The features that make up the product. Tag each MoSCoW: Must / Should / Could / Won't (this version).

| ID | Feature | User value | Priority | Acceptance criteria ref |
|----|---------|-----------|----------|--------------------------|
| F1 | `<feature>` | `<why it matters>` | Must | AC-1 |
| F2 | `<feature>` | `<why it matters>` | Should | AC-2 |

## 5. User stories
> Format: As a `<persona>`, I want `<capability>`, so that `<benefit>`.

- **US-1:** As a `<persona>`, I want `<...>`, so that `<...>`.

## 6. Acceptance criteria
> Make each feature verifiable. Use Given/When/Then. A feature is not "done" until these pass.

- **AC-1 (F1):** Given `<context>`, when `<action>`, then `<observable result>`.

## 7. Success metrics
> How we will know it works after launch. Name the metric, the target, and how it's measured.

| Metric | Target | Source |
|--------|--------|--------|
| `<activation rate>` | `<e.g. 40% in week 1>` | `<analytics event>` |

## 8. Monetization & pricing model
> How the product makes money (or why it deliberately doesn't yet). Pricing is business-critical — confirm with the founder and record in [decision-record.md](decision-record.md).

- **Revenue model:** `<e.g. subscription / one-time / usage-based / freemium / ads / marketplace take-rate / free (no revenue this version)>`
- **Pricing tiers / packaging:** `<tier name → price → what it includes>`
- **Billing mechanics:** `<billing cycle, currency, trial length, who collects payment (e.g. Stripe), tax/VAT handling>`
- **Key pricing assumptions & unit economics:** `<target ARPU/LTV, rough CAC, gross-margin expectation — flag if unknown>`

## 9. MVP vs later phasing
> What ships in the first releasable slice versus what is deliberately deferred. Trace back to the MoSCoW tags in §4.

| Phase | Scope (feature IDs) | Goal of this phase | Out (deferred to later) |
|-------|---------------------|--------------------|-------------------------|
| MVP / v1 | `<F1, F2 …>` | `<smallest thing that delivers the core value / validates the riskiest assumption>` | `<F4, F5 …>` |
| Next / v1.x | `<F4 …>` | `<what unlocks once MVP is validated>` | `<…>` |
| Later / vision | `<…>` | `<longer-horizon bets>` | — |

- **MVP cut-line rationale:** `<why these features are in and those are out — what the MVP must prove>`

## 10. Competitive & positioning context
> Who/what users would use instead, and why this product wins for the target persona. Keep it honest — "do nothing / spreadsheet" is a valid competitor.

| Alternative | What it does well | Where it falls short for our user | Our differentiation |
|-------------|-------------------|-----------------------------------|---------------------|
| `<competitor / status quo>` | `<strength>` | `<gap>` | `<why we win>` |

- **Positioning statement:** `<For <persona>, unlike <main alternative>, this product <the one thing that matters most>.>`

## 11. Risks & mitigations
> The things that could sink this version: market, technical, legal/compliance, dependency, and adoption risks. Pair every risk with a mitigation or a trigger to revisit.

| Risk | Type | Likelihood × impact | Mitigation / early signal to watch |
|------|------|---------------------|-------------------------------------|
| `<risk>` | `<market / technical / legal / dependency / adoption>` | `<H/M/L × H/M/L>` | `<how we reduce or detect it>` |

- **Biggest single risk:** `<the one that most threatens this version>` → `<owner + plan>`.

## 12. Dependencies & assumptions
> External services, data, teams, or decisions this depends on. Record assumptions per the CLAUDE.md assumptions-log policy.

- **Dependency:** `<e.g. Stripe account, third-party API>`
- **Assumption:** `<assumption>` → recorded in [decision-record.md](decision-record.md) if business-critical.

## 13. Open questions
> Business-critical unknowns the founder must resolve. The orchestrator stops and asks only about these.

- [ ] `<question requiring a founder decision>`

---
**Done when:** every Must feature has a user story + acceptance criteria, success metrics are measurable, non-goals are explicit, the monetization model and MVP cut-line are stated, top risks have mitigations, and open questions are either resolved or flagged for the user. Next: [/create-roadmap](../commands/create-roadmap.md) and [/design-architecture](../commands/design-architecture.md).

# RFC — Proposed Change to the .claude/ Operating System
**What:** A proposal to change the shared, reusable `.claude/` OS itself — a new stage/gate, a new agent family, a schema/frontmatter change, a new pillar-level capability, or anything that changes behavior for every project this template is copied into.
**Who fills it in:** Whoever is proposing the change. One RFC per proposal.
**Not this:** A technical decision inside **one consuming project** (database choice, framework pick, auth model) is a `.claude/templates/decision-record.md`, filed in that project's own `docs/decisions/` — never an RFC. RFCs are for changes to the template itself; see `CONTRIBUTING.md` §11 for the full RFC-vs-decision-record-vs-normal-PR rule.
**Cross-references:** `CONTRIBUTING.md`, `.claude/CLAUDE.md`, `.claude/templates/decision-record.md`

---

## RFC Metadata

| Field | Value |
|-------|-------|
| RFC number | `<RFC-0007>` (next free number under `docs/rfcs/`) |
| Title | `<Add a "data-residency" cross-cutting concern to the routing matrix>` |
| Date | `<YYYY-MM-DD>` |
| Status | `<Draft \| In Review \| Accepted \| Rejected \| Withdrawn \| Superseded by RFC-XXXX>` |
| Author | `<@handle>` |
| Reviewers | `<@handle, @handle — from CODEOWNERS for the paths this touches>` |
| Targets version | `<e.g. v1.9.0 — see CHANGELOG.md for the current released version>` |
| Filed at | `docs/rfcs/<YYYY-MM-DD>-<slug>.md` in this repo |

---

## 1. Summary

> One paragraph. What is being added, changed, or removed, in plain language — someone skimming just this section should understand the proposal.

`<Add a new cross-cutting concern, "data-residency", to .claude/agents/core/orchestrator.md's matrix and .claude/orchestration/routing-matrix.md, so projects that must keep data in a specific jurisdiction automatically pull in the privacy-compliance checklist and a residency section in the architecture template.>`

---

## 2. Motivation

> What is broken, missing, or awkward today without this change? Who hits the gap, and how often? Cite the real friction — a hypothetical isn't enough to justify changing something every copy of this template inherits.

`<Projects with EU/data-residency requirements currently get privacy-compliance only if they're already flagged as "regulated data" — data residency is a distinct constraint (money can stay non-regulated but still need to stay in-region) that the current matrix has no row for, so it's being caught late, at the readiness gate instead of at classification.>`

---

## 3. Detailed Design

> The actual change, precisely enough that a reviewer could implement it from this section alone. Name every file touched, by path, and what changes in each. Include schema/frontmatter changes verbatim if any.

**Files added:**
- `<.claude/... — new file and its purpose>`

**Files changed:**
- `<.claude/agents/core/orchestrator.md — add a row to the cross-cutting concern matrix: signal "data residency requirement" → add checklist .claude/checklists/privacy-compliance.md, add architecture.md residency section>`
- `<.claude/orchestration/routing-matrix.md — mirror the new row>`

**Files removed / renamed (breaking):**
- `<none, or list with justification — renames/removals almost always require a MAJOR version bump; see CONTRIBUTING.md §12>`

---

## 4. Backward Compatibility & Migration

> Every project that already copied `.claude/` into their repo is on an older snapshot. Is this change purely additive (new file, new optional row — safe to ignore if unused) or does it change existing behavior/schema (existing projects must edit something to stay green)?

- **Additive / non-breaking:** `<yes/no — explain>`
- **If breaking:** migration steps an existing adopter must take: `<list>`; what happens if they don't migrate: `<explain the failure mode, e.g. validate.py starts erroring on old frontmatter>`.

---

## 5. Alternatives Considered

> At least one real alternative, including "do nothing." Say why it was rejected, not just that it exists.

- **`<Alternative A>`** — `<description>`. Rejected because `<reason>`.
- **Do nothing / status quo** — Rejected because `<reason, or accepted if this RFC is ultimately withdrawn>`.

---

## 6. Drawbacks & Risks

> Be honest. What gets worse, more complex, or more web-biased if this ships? Does it add ceremony that Pillar 4 (low-magic ergonomics, `.claude/docs/OPERATING_MODES.md`) would object to?

`<e.g. adds one more question to classification; risk of becoming a second "regulated data" flag that confuses which checklist owns what — mitigated by keeping the two signals and their checklist targets explicitly distinct in the matrix row.>`

---

## 7. Rollout Plan

> Which release/phase this ships in, and every downstream artifact that must be updated in the same PR so nothing drifts.

- [ ] Implementation PR(s): `<link when opened>`
- [ ] `.claude/scripts/integrity-check.py` / `validate.py` pass (and are updated first if the schema itself changed)
- [ ] `.claude/scripts/generate_adapters.py` re-run if the change affects Cursor/Copilot adapter content
- [ ] `CHANGELOG.md` entry added, referencing this RFC
- [ ] `README.md` / `CONTRIBUTING.md` cross-references updated if the map of the system changed
- [ ] CODEOWNERS updated if a new security/compliance-sensitive path was introduced

---

## 8. Unresolved Questions

> What don't you know yet that reviewers should weigh in on? An RFC with no open questions is either trivial or under-examined — most substantive proposals have at least one.

- `<question>`

---

## 9. Decision & Rationale

> Filled in by the reviewers when status moves to Accepted/Rejected — not by the author up front.

**Decision:** `<Accepted | Rejected | Accepted with changes: ...>`
**Rationale:** `<why, referencing the decision drivers above>`
**Follow-ups:** `<any deferred scope, filed as its own RFC or issue>`

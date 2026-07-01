# Org Config Layering — an org-wide floor, a repo-level ceiling of choice

A single team copying `.claude/` into one repo needs nothing beyond what this template already ships.
An organization running this OS across **many** repos eventually needs a second layer: rules that apply
everywhere (a banned dependency, a mandatory compliance checklist, a security contact, an org-approved
stack) without forking and hand-editing the whole `.claude/` tree in every repo. This doc defines that
layer, its precedence rule, and how it's distributed — as a documented convention, not a Claude Code
runtime feature (there is no built-in multi-file config merge; the orchestrator implements this by
reading one extra file first).

## The two tiers

- **Org tier** — shared across every repo in the organization. Sets a **floor**: mandatory checklist
  additions, banned/approved technology choices, a required compliance regime, an org security contact,
  a default review team. Owned by platform/security leadership, changed rarely.
- **Repo tier** — this project's own `.claude/` tree (the full template, unmodified) plus its own specs,
  decisions, and presets. Owned by the project team, changed often as the project evolves.

## Precedence rule

**Repo config may add restrictions or narrow choices. It may never remove or weaken an org-mandated
control or a `.claude/CLAUDE.md` §8 safety rule.** On conflict, the stricter rule wins — there is
deliberately no mechanism for a repo to opt out of an org rule silently. A repo that genuinely needs an
exception (e.g., "we need MongoDB and the org standard is Postgres") must record it as an explicit,
co-signed decision (below), never a quiet override.

## Mechanism: the `.claude/org/` overlay

Because `.claude/CLAUDE.md` is the one constitution file Claude Code auto-loads, layering is implemented
as a small, explicit overlay directory the org publishes and each repo pulls in — never a fork of the
whole template:

- **`.claude/org/org-constitution.md`** — org-wide addenda to `CLAUDE.md`: additional safety rules,
  mandatory checklist items, banned dependencies/vendors, required compliance regimes, the org security
  contact. Written in the same imperative "law" voice as `CLAUDE.md` itself, so it reads as an extension,
  not a suggestion.
- **`.claude/org/stack-matrix-overrides.md`** — org-approved/banned technology choices layered on top of
  `.claude/stack-matrix/*` (e.g. "MongoDB is banned org-wide; use PostgreSQL") — this *narrows* the
  stack-matrix's options, it does not replace the matrix's own trade-off analysis.
- **`.claude/org/checklist-additions/<name>.md`** — extra P0/P1 items appended to a specific checklist
  (e.g. one more `security.md` P0 line mandating a specific SSO provider). Additive only — never a file
  that edits or removes an existing checklist item.
- **`CLAUDE.md`'s load order** — a repo that adopts org layering keeps a one-line pointer at the top of
  its own `.claude/CLAUDE.md` (or relies on the orchestrator's Step 0, see below): "If
  `.claude/org/org-constitution.md` exists, read it first; every rule in it applies as an addition to
  this file, never a substitution."

## Distribution

The org maintains this overlay in its own small repo (e.g. `org-claude-overlay`), **separate from** a
fork of this whole template. Each project either (a) copies `.claude/org/` in at setup time alongside the
normal `.claude/` copy, or (b) — for orgs wanting live updates — adds it as a git submodule/subtree at
`.claude/org/`. Either way the overlay is small and independently reviewed; the base `.claude/` tree
stays exactly what this repo ships, so upgrading the base template (re-copying a newer version of
`.claude/`) never conflicts with org customizations living in their own directory.

## Conflict resolution & review

Because org rules can only tighten, most "conflicts" resolve themselves: the stricter of two applicable
rules wins, with no contradiction to adjudicate. The one real conflict case is a repo claiming an
exception to an org rule. That always requires an explicit decision record
(`.claude/templates/decision-record.md`) co-signed by whoever the org's `.github/CODEOWNERS` names as
owner of `.claude/org/` — never a silent override, and never something the agent decides on its own
(this is business-critical per `.claude/CLAUDE.md` §6: vendor lock-in and compliance posture are
explicitly listed there).

## Wiring into the orchestrator

`.claude/agents/core/orchestrator.md`'s *Selection algorithm* Step 0 loads
`.claude/org/org-constitution.md` if present, before topology detection or classification — so every
later step already carries the org's mandatory additions (extra baseline gates, banned stack choices) as
a matter of course rather than a step someone remembers to bolt on at the end.

## What this is not

Not a runtime feature of Claude Code — there is no automatic merge engine, no schema validation between
org and repo files beyond what `.claude/scripts/validate.py` already checks on the repo's own `.claude/`
tree. It is a documented convention plus one extra file-read the orchestrator performs first, enforced by
the same review/CODEOWNERS discipline as everything else in this system. An org that needs stronger
guarantees than "the agent reads this file first" should pair it with a repo-level CI check that fails if
`.claude/org/` is missing, modified outside what the org's CODEOWNERS permits, or stale against the org's
published version.

## Related

`.claude/agents/core/orchestrator.md` (Selection algorithm Step 0), `.claude/CLAUDE.md` §6 (business-
critical decisions) and §8 (safety rules that can never be weakened), `.github/CODEOWNERS`,
`.claude/templates/decision-record.md`, `.claude/orchestration/monorepo-routing-matrix.md` (the other
layer that runs alongside this one in a large organization's monorepo).

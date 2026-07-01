# Operating Modes — full / lite / expert

The 9-stage flow is the right default for anything non-trivial — but pretending every one-line config
tweak needs a spec, an interview, and a decision record is how senior engineers bounce off a system like
this one. Modes make the trivial/non-trivial boundary **explicit and auditable** instead of an ad-hoc
judgment call re-litigated on every request. This is Pillar 4 of the enterprise design
(`docs/superpowers/specs/2026-06-30-enterprise-and-cross-tool-design.md`): low-magic ergonomics — gets
out of your way on small work, without weakening anything on work that isn't small.

## Full mode (default)

Unchanged. The complete 9-stage flow (`.claude/CLAUDE.md` §2), every gate, full documentation. This is
what happens unless one of the conditions below is explicitly met — full mode is never silently skipped.

## Lite mode — for genuinely trivial work

**Triggers (any one):**
- Explicit: the user says "lite mode," "quick fix," "just do X, don't overthink it," or invokes
  `.claude/commands/quick-fix.md` directly.
- Implicit smallness heuristic (**all** must hold): a single file or a tight cluster of obviously-related
  files; a diff reasonably estimated under ~20–30 lines before starting; no new dependency; no
  schema/migration change; no new public API/interface contract; nothing touching auth, payments,
  secrets, or infrastructure.

**What lite mode skips:** the interview stage, formal spec documents, a written architecture note, and a
decision record for routine, easily-reversible choices.

**What lite mode never skips:** understanding the change before making it, running the relevant
tests/linter, a one-line assumption note if anything non-obvious was decided, and — non-negotiably —
every `.claude/CLAUDE.md` §8 hard constraint. Lite mode reduces ceremony, never safety.

**Hard exclusion:** anything on §8's forbidden-without-approval list, and anything security/privacy/
payments/auth-adjacent, always runs in full mode regardless of how small the diff looks — line count is
not the same thing as blast radius, and lite mode's heuristic says so explicitly above.

**Auto-escalation:** if the change turns out bigger than estimated mid-task (file count balloons, a
schema change appears, a new dependency turns out to be needed), stop and escalate to full mode rather
than pushing through under a lite-mode label — the same "stop and reassess" discipline every command in
this system already uses at its own stop conditions.

## Expert mode — for experienced users who want to self-navigate stages

**Triggers:** the user explicitly declares "expert mode" for a session or project, or an org override
(`.claude/docs/ORG_CONFIG_LAYERING.md`) opts a team into it by default.

**What changes:** the user can jump directly to a later stage (straight to stage 4 spec because stages
1–3 already happened in their head or in a doc they hand over), and can waive a specific gate with one
line instead of a fresh negotiation every time.

**What doesn't change:** gate-skips are still recorded. `.claude/CLAUDE.md` §2's existing rule — "may
proceed only with explicit acknowledgment... recorded as a risk via the decision-record template" —
still applies; expert mode makes the acknowledgment a one-line formality instead of a paragraph each
time, it does not remove the record. The Definition of Done (`.claude/CLAUDE.md` §5) still applies to
whatever ships, in every mode.

## Declaring a mode

Modes are stated, not silently inferred — beyond lite mode's own narrow trivial-task heuristic above, a
mode change is announced at the start of the response it applies to. A standing, project-level mode
choice (e.g. "this project always runs in lite mode for docs-only PRs") is logged in
`docs/state/project.md` so it survives across sessions instead of being re-decided every time.

## Relationship to escape hatches

"Skip this one gate, this one time, with a recorded reason" already exists in `.claude/CLAUDE.md` §2 and
does not need a mode to work — it is the smallest-grained escape hatch there is. Lite mode generalizes
that idea to skipping ceremony across an entire trivial task; expert mode generalizes it to skipping the
orchestrator's imposed stage sequencing. All three funnel through the same discipline: state what is
being skipped, state why, and record it when it is non-obvious enough that a colleague might have called
it differently.

## Interaction with commands

`.claude/commands/quick-fix.md` is lite mode's entry point — read it for the concrete workflow.
`.claude/commands/explain.md` is not a mode at all: it is a read-only command for a request that was
never in the 9-stage flow's scope to begin with (an explanation is not a build), kept as its own explicit
command so that boundary isn't left to interpretation.

## Related

`.claude/CLAUDE.md` §1 (Prime Directive — points here), §2 (the gate-skip rule these modes formalize),
§8 (hard constraints, unaffected by any mode); `.claude/commands/quick-fix.md`;
`.claude/commands/explain.md`; `.claude/docs/ORG_CONFIG_LAYERING.md` (an org can mandate which modes a
team may use).

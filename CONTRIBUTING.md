# Contributing to the Universal `.claude` AI Project OS

Thank you for improving this template. This repo is a **reusable, copy-into-any-project workflow system** for Claude Code. The value lives in `.claude/` — a tree of agents, skills, commands, presets, checklists, templates, hooks, and docs that drives projects through a 9-stage flow (classify → interview → select → spec → build → audit → readiness → launch → continue).

Because the same `.claude/` tree is dropped into many different repos, **every contribution must stay reusable, project-agnostic, and safe**. This guide explains the house style and the bar your change must clear.

The whole bar reduces to one command. Before any PR:

```bash
python3 .claude/scripts/integrity-check.py
```

It must report **0 broken links, 0 shallow files, 0 missing frontmatter, 0 invalid JSON**. This is the same check the `/self-test` command runs. Details are in the [Must-pass gate](#the-must-pass-gate) section.

---

## 1. Philosophy

Read these before touching anything. A change that violates them will be rejected even if it "works."

- **Universal, never web-biased.** Never assume the target project is a web app or SaaS. This system supports web, mobile, desktop, **game**, backend/API, **CLI**, browser extension, **AI agent system**, **data platform**, **IoT/embedded**, **blockchain**, and more. When you write guidance, phrase it so it applies across types, then defer type-specific detail to the matching preset. A sentence like "ship the bundle to a CDN" is wrong for a CLI, a game binary, or firmware — write "ship the artifact" and let the preset specialize.
- **Safe by default.** The system enforces the constitution in `.claude/CLAUDE.md` (§8 safety rules). Nothing you add may weaken it: no destructive automation, no auto-install of packages, no secret exposure, no irreversible production actions without explicit human approval. Hooks **warn or block** (exit 2) — they never mutate, install, or reveal secrets. Headless and routine guidance stays **read/review-only by default**; writes require an explicit opt-in plus a rollback path.
- **No shallow filler.** Every file in a content directory must carry real, specific information. Placeholder stubs, "TODO: fill this in," and generic boilerplate are rejected by the integrity check (files under ~300 words of content fail). If you can't write a substantive file, the file shouldn't exist yet.
- **No generic placeholder files.** Do not add an agent/skill/preset just to round out a count. Add it because a real project type or concern needs it.
- **The value lives in `.claude/` and must stay project-agnostic.** Generated artifacts — discovery answers, specs, ADRs, run-state — belong in a *consuming project's own* `docs/` directory (e.g. `docs/specs/`, `docs/state/`, `docs/decisions/`). They must **never** be written into `.claude/`. Keep `.claude/` clean so it copies to the next repo unchanged.
- **Document the why.** When you make a non-obvious design call inside the system, say so in the PR description (and, where the system itself models a decision, follow the assumptions/decision-record pattern the OS teaches).

---

## 2. Repository layout

| Path | What lives here | Contributions go here when… |
|---|---|---|
| `.claude/CLAUDE.md` | The constitution / operating law | You're amending core policy (rare; discuss first) |
| `.claude/settings.json` | Always-on safety guards (`permissions.deny` / `permissions.ask`) | You're tightening or extending the safety baseline |
| `.claude/agents/<family>/` | Specialized roles (core, engineering, quality, design, domain, stack) | Adding or refining a role |
| `.claude/skills/<name>/SKILL.md` | Repeatable procedures (the "how") | Adding or refining a method |
| `.claude/commands/` | Invokable slash-command workflows + gates | Adding or refining a user-facing workflow |
| `.claude/hooks/` | Opt-in, safe-by-default JSON guards | Adding a mechanical enforcement of §8 |
| `.claude/orchestration/` | `routing-matrix.md` (type → minimal active team) | Wiring a new type/concern into routing |
| `.claude/presets/` | Per-project-type starting configs | Supporting a new project type |
| `.claude/stack-matrix/` | Technology decision matrices | Adding a comparison of real tech options |
| `.claude/checklists/` | P0–P3 gate definitions | Adding a verifiable gate |
| `.claude/templates/` | Fill-in documents | Adding a document the OS produces |
| `.claude/docs/` | Portable operating-capability strategy docs | Deepening runtime guidance |
| `.claude/scripts/integrity-check.py` | The self-test | Fixing or extending the integrity check |
| Root files (`README.md`, `START_HERE.md`, `PROJECT_OS.md`, `SECURITY.md`, this file, `examples/`) | Public-facing docs | Explaining how to use the system |

When a new module joins the **core 9-stage flow** (most often a new core agent or a new command/gate), you must also wire it in: register the agent in `.claude/agents/core/orchestrator.md` (its handoffs and, if it's a stage owner, the flow), and add any new type/concern to `.claude/orchestration/routing-matrix.md`.

---

## 3. Adding an agent

**Path:** `.claude/agents/<family>/<name>.md`, where `<family>` is one of `core`, `engineering`, `quality`, `design`, `domain`, `stack` (stack agents live under a framework sub-folder, e.g. `stack/backend/`).

**Frontmatter (YAML, required):**

```yaml
---
name: <kebab-case-name>          # must match the filename
description: One or two sentences saying exactly when this agent is invoked and what it owns.
model: inherit
---
```

**Required sections** (model the structure on `.claude/agents/core/orchestrator.md`):

- `## When to use` — the concrete triggers that hand work to this agent.
- `## Responsibilities` — what it owns, as a bulleted list of accountable outcomes.
- `## Inputs` — the files, state, and answers it reads.
- `## Outputs` — the files it writes (always into the consuming project's `docs/`, never `.claude/`).
- `## Tools & resources` — the `.claude/...` skills, checklists, templates, and sibling agents it pulls in, **by path**.
- `## Must follow` — the non-negotiable rules for this role.
- `## Must not do` — the destructive/irreversible/secret-exposing actions it must refuse (mirror §8).
- `## Handoff to` and `## Handoff from` — explicit, path-referenced handoffs to and from other agents. Dropped handoffs are the most common defect; name the exact file the next agent reads.
- `## Definition of Done` — a checkbox list; the agent's phase is "done" only when these hold and its outputs exist on disk.

**Length:** ≥ 300 words of real content. A thin agent is worse than no agent.

**Universal-not-web:** write responsibilities that hold across project types. If a responsibility only makes sense for one platform, scope it to that platform explicitly, or push it into a preset.

**Register it if it joins the core flow.** A new core agent (or any agent that becomes a stage owner) must be added to the orchestrator's `## Handoff to` / `## Handoff from` and, where relevant, the routing matrix, so the orchestrator actually delegates to it.

---

## 4. Adding a skill

**Path:** `.claude/skills/<name>/SKILL.md` (one folder per skill).

**Frontmatter (YAML, required):**

```yaml
---
name: <kebab-case-name>
description: When this skill triggers and what it does. Include the trigger keywords a reader (or Claude) would use to reach for it.
---
```

**Required sections** (model the structure on `.claude/skills/security/SKILL.md`):

- `## When to use` — the situations that pull in this skill, across project types.
- `## Workflow` — the numbered, repeatable procedure. This is the heart of the skill: a method, not an essay.
- `## Standards` — the do/do-not rules the procedure enforces.
- `## Common mistakes to avoid` — the specific traps this skill exists to prevent.
- `## Output format` — what the skill produces (a report, a record, an artifact) and where it lands.
- `## Related` — related checklists and agents, by path.

**Length:** ≥ 300 words of real content.

**Procedure, not prose.** A skill is a how-to. If a reviewer can't follow it step by step to produce the stated output, it isn't done. Keep it universal: the discipline should hold for web, CLI, game, embedded, etc., even where the concrete commands differ.

---

## 5. Adding a command

**Path:** `.claude/commands/<name>.md`.

**Frontmatter (YAML, required):**

```yaml
---
description: One line describing what the command does.
argument-hint: [optional-arg — what it controls]
---
```

**Required sections** (model the structure on `.claude/commands/route.md`):

- `## Purpose` — what the command accomplishes and why it's a distinct entry point.
- `## When to use` — the moments a user (or the orchestrator) invokes it.
- `## Workflow` — numbered steps. Insert explicit **STOP** gates where the command must pause for user confirmation or for a checklist to pass. STOP gates are how the system keeps a human in the loop on business-critical and irreversible decisions.
- `## Agents used` — the `.claude/agents/...` this command delegates to, by path.
- `## Skills used` — the `.claude/skills/...` it relies on, by path.
- `## Expected outputs` — a table of `| Output | Path |` rows (paths point into the consuming project's `docs/`).
- `## Stop conditions` — when the command halts and asks instead of proceeding.
- `## Final report format` — the exact shape of the summary the command prints when it finishes.

**Length:** ≥ 300 words of real content. Commands stay thin on *method* (that lives in skills) but must be complete on *flow, gates, and outputs*.

---

## 6. Adding a checklist

**Path:** `.claude/checklists/<name>.md` (model on `.claude/checklists/dependencies.md`).

- Open with a one-paragraph statement of what the gate covers.
- Group items under **`## P0 — Blockers`**, **`## P1 — Important`**, **`## P2 — Hardening`**, **`## P3 — Post-launch / backlog`**. P0 blocks shipping; P3 is tracked and never blocks.
- **Every item is a single, verifiable pass/fail line** written as a `- [ ]` checkbox. "Inputs are validated" is too vague; "All external input is validated against an allowlist at the trust boundary" can be checked. Avoid items that can't be objectively marked done.
- End with a **`## How to use`** block stating *When* to run it, *Who* owns it (agent path), the *Command* that triggers it, and the *Tools* involved.

---

## 7. Adding a template

**Path:** `.claude/templates/<name>.md`.

- A template is a document the OS *produces* in a consuming project. It must be a real, fillable structure: section headings plus clearly marked placeholders (e.g. `<decision>`, `<owner>`, `<date>`) and brief inline guidance on what each section captures.
- **No empty sections.** Every heading either contains guidance text or a placeholder; a bare heading with nothing under it fails review.
- Keep it project-agnostic — the same template should serve a fintech API and a game equally well.

---

## 8. Adding a preset

**Path:** `.claude/presets/<type>.md`.

A preset is a starting configuration for one project type. It must name, **by path**, the recommended set of agents, skills, stack-matrix entries, checklists, and templates that this type pulls in — the "base set" the orchestrator activates. After adding a preset, wire its type into `.claude/orchestration/routing-matrix.md` so `/route` can match it. Do not add a preset for a type the system can't meaningfully support yet; a half-wired preset is worse than none.

---

## 9. Adding a stack-matrix entry

**Path:** `.claude/stack-matrix/<area>.md`.

A stack matrix compares the **real** options in a technology area so choices are consistent and defensible. It must include:

- A **comparison table** of the genuine contenders (not a single recommendation dressed up as a comparison).
- **When / when-not** guidance per option — the conditions under which each is the right or wrong call.
- **Recommended combinations** — the proven pairings (e.g. a runtime + a datastore + a deploy target) for common scenarios.

Be honest about trade-offs and risks. The matrix exists to prevent cargo-culting one stack onto every project.

---

## 10. Quality rules (apply to every contribution)

- **Links:** use root-relative `.claude/...` paths only (e.g. `.claude/skills/security/SKILL.md`). No absolute filesystem paths, no `../` walks, no broken links. For operating-capability depth, link to `.claude/docs/<NAME>.md`. **Do not** link to a top-level `docs/` file in this template repo — that directory is for a *consuming* project's generated output, not for this repo's documentation.
- **No broken links.** Every referenced path must exist. The integrity check enforces this.
- **No shallow files.** Files in content directories must clear the ~300-word substance bar.
- **Valid JSON.** `.claude/settings.json` and every hook must be valid JSON. Validate before committing.
- **Safe-by-default hooks.** A hook may warn or block (exit 2). It must never mutate files, install packages, run remote `curl | bash`, or print/transmit secrets.
- **Universal, not web-biased.** Re-read your prose and strip any assumption that the project is a web app.
- **Document assumptions and decisions.** Explain non-obvious calls in the PR; for changes the system models as decisions, follow the OS's own decision-record pattern.

---

## 11. Proposing a significant change (RFC)

Most contributions are a normal PR against the per-type rules above. A smaller set of changes affect
**every project this template gets copied into** and need a written proposal reviewed *before* code:
a new stage or gate in the 9-stage flow, a new agent family, a change to `.claude/CLAUDE.md` §8 safety
rules, a new required frontmatter field (a schema change `validate.py` must also learn), removing or
renaming a widely-referenced agent/skill/command, or a new pillar-level capability (in the spirit of the
enterprise pillars: trust & determinism, governance & compliance, team & scale, low-magic ergonomics).

**Process:**
1. Copy `.claude/templates/rfc.md`, fill it in, and save it as `docs/rfcs/<YYYY-MM-DD>-<slug>.md` in
   this repo (this repo's own `docs/rfcs/` — distinct from a *consuming* project's `docs/`, which the OS
   writes specs and decisions into once copied elsewhere; see `.claude/docs/MEMORY_STRATEGY.md`).
2. Open a PR that adds the RFC file alone (no implementation yet) so the design is reviewed before the
   diff. Status starts at `Draft`, moves to `In Review` once opened.
3. Discussion happens on the PR. The reviewers named by `.github/CODEOWNERS` for the paths the RFC would
   touch make the call; unresolved trade-offs get written into the RFC's *Unresolved Questions* section,
   not left implicit.
4. Once `Accepted`, implement in a follow-up PR (or a series of small ones) that satisfies the *Rollout
   Plan* checklist in the RFC — including the CHANGELOG entry referencing the RFC number.
5. `Rejected` or `Withdrawn` RFCs stay in `docs/rfcs/` as a record of what was considered and why it
   didn't move forward — do not delete them.

**When an RFC is *not* the right tool:**
- A single project's own technical decision (which database, which framework) is a
  `.claude/templates/decision-record.md` filed in *that project's* `docs/decisions/` — never an RFC, and
  never filed in this repo.
- Adding a new agent/skill/preset/checklist/template *within an existing family*, or refining existing
  content, follows the per-type rules in §3–§9 above as a normal PR — no RFC needed.

---

## 12. Versioning the .claude/ tree

The template versions as a whole (`CHANGELOG.md`, Semantic Versioning) — individual agents, skills, or
commands are not released or versioned independently, because they only ever ship as part of the full
`.claude/` copy a project takes. When you contribute, classify your change so the changelog entry (and
whether an RFC was required, per §11) matches its real impact:

- **Patch** — typo/doc fixes, broken-link repairs, tightening a checklist item's wording without changing
  its intent, non-behavioral refactors of an agent/skill/command's prose. No RFC.
- **Minor** — a new agent/skill/preset/checklist/template/stack-matrix entry added within an existing
  family; refining an existing agent's responsibilities without changing its frontmatter schema or
  removing a handoff another agent depends on. No RFC unless it also trips a §11 trigger.
- **Major** — anything in the §11 RFC trigger list: new stage/gate, new agent family, `.claude/CLAUDE.md`
  §8 changes, a frontmatter/schema change, or removing/renaming something other files reference by path.
  Requires an accepted RFC first, and — because an existing adopter's copy of `.claude/` may now be out
  of sync with the new schema — the RFC's *Backward Compatibility & Migration* section must say exactly
  what an existing project needs to do to stay green under `.claude/scripts/validate.py`.

**Proposing a version bump:** the PR that closes out a phase updates `CHANGELOG.md` under a new
`## [x.y.z] — <date>` heading (see the existing entries for the exact style) and, for a major bump,
links back to the accepted RFC. Do not bump the version number without a corresponding changelog entry —
`self-test` doesn't check this mechanically, so it is a review-time responsibility (`.github/CODEOWNERS`
routes `CHANGELOG.md` changes to the same maintainers who own `CONTRIBUTING.md`).

---

## The must-pass gate

Run the integrity check from the repo root before opening any PR:

```bash
python3 .claude/scripts/integrity-check.py
```

This is exactly what the `/self-test` command runs. It must report:

- **0 broken links** — every `.claude/...` reference resolves.
- **0 shallow files** — no content file falls under the substance threshold.
- **0 missing frontmatter** — every agent, skill, and command has its required YAML frontmatter.
- **0 invalid JSON** — `settings.json` and all hooks parse.

A red result is a blocker. Fix it before requesting review — do not ask a reviewer to look past a failing self-test.

### PR checklist

Copy this into your pull request description and tick every box:

- [ ] `python3 .claude/scripts/integrity-check.py` reports 0 broken links, 0 shallow files, 0 missing frontmatter, 0 invalid JSON.
- [ ] New/changed files live under the correct `.claude/<dir>/` and follow that directory's required sections and frontmatter.
- [ ] Every link is a root-relative `.claude/...` path; nothing links to a top-level `docs/` file in this repo.
- [ ] Content is universal, not web/SaaS-biased; type-specific detail is deferred to a preset.
- [ ] No shallow filler and no generic placeholder files; each new file carries real, specific content (≥ 300 words where required).
- [ ] No generated artifacts were written into `.claude/`; the tree stays project-agnostic and copy-clean.
- [ ] Any new agent/command that joins the core flow is registered in `.claude/agents/core/orchestrator.md` and/or `.claude/orchestration/routing-matrix.md`, with explicit handoffs.
- [ ] Safety preserved: no weakening of `.claude/CLAUDE.md` §8 or `.claude/settings.json`; hooks remain warn/block-only with no mutation, install, or secret exposure.
- [ ] Assumptions and non-obvious decisions are documented in the PR description.
- [ ] If this change trips an RFC trigger (§11) — new stage/gate, new agent family, §8 change, schema change, or a removal/rename other files reference — an accepted RFC is linked, and the version bump matches its real impact (§12).

Welcome aboard — keep it universal, keep it safe, keep it substantive.

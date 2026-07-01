# Design Spec — Enterprise-grade & Cross-tool `.claude` OS (2026-06-30)

## Goal
Make the Universal `.claude` AI Project OS something **senior engineers and enterprises adopt**, not just
a vibe-coder convenience — and make it usable beyond Claude Code (Cursor, GitHub Copilot, and others).

The unlock for senior-dev adoption is one principle: **transparent · deterministic · rule-enforced ·
opt-in · gets out of your way.** Nothing hand-wavy; every file schema-validated and linted; experts can
scope it down or skip gates with a recorded reason.

## Approved decisions (user)
1. **Adapters** = a **generator + committed outputs + CI sync-check** (single source of truth = `.claude/`; zero drift).
2. **Target tools** now = **Cursor** + **GitHub Copilot** (generator is extensible to Windsurf/others later; Codex/opencode already covered by `AGENTS.md`).
3. **Enterprise focus** = all four pillars: **Trust & determinism · Governance & compliance · Team & scale · Low-magic ergonomics.**
4. Approach **A — trust-spine-first, phased** (each phase its own release).

## Backbone — a tiny, dependency-free toolchain
`.claude/scripts/` grows from one integrity script into a small, stdlib-only toolset:
- `integrity-check.py` — existing gate (links, shallow, frontmatter, JSON). Unchanged contract; `/self-test` keeps using it.
- `validate.py` (new) — the **linter**: per-type schema/rule checks (frontmatter fields, `tools` allowlist, `color` enum, required sections, `argument-hint` on commands, and the **no-fabrication clause** present in every audit/review agent).
- `generate_adapters.py` (new) — emits Cursor + Copilot adapters from `.claude/`; `--check` mode fails on drift.
Single source of truth stays `.claude/`; adapters + compliance docs are **derived** and **CI-verified**.

## The four pillars (full vision)

### Pillar 1 — Trust & determinism
- Typed schemas + `validate.py` linter (above); CI-gated, fast, deterministic.
- Eval harness: extend the `evals/*.json` pattern (already on `project-classification`, `testing`) + a tiny offline runner; document which skills/agents have evals.
- Provenance: assumptions log + decision records + headless-audit-report are the evidence chain; the no-fabrication clause is now **lint-enforced**.

### Pillar 2 — Governance & compliance
- `CODEOWNERS` per `.claude/` family (security/checklists/agents require the right reviewer).
- RFC template + ADR discipline; `CONTRIBUTING.md` governance section (have CONTRIBUTING; extend).
- `.claude/docs/COMPLIANCE.md` mapping gates/checklists → **SOC2 / ISO 27001 / SLSA / OWASP ASVS**.
- `CODE_OF_CONDUCT.md` + `SUPPORT.md` for a complete OSS governance set (SECURITY.md exists).

### Pillar 3 — Team & scale
- Monorepo/multi-service orchestration doc + `/route` per-package classification.
- Org-level config layering (org base `.claude/` + per-repo override/merge model) — documented.
- `/onboard` command: codebase-mapper → active team → "how this repo works" brief.
- Versioning/contribution model for agents/skills (semver; how to propose/version one).

### Pillar 4 — Low-magic ergonomics
- Tiered modes: a documented `lite`/expert profile that skips the 9-stage ceremony for small work.
- Fast-path commands: `/quick-fix`, `/explain` (skip the full flow for trivial tasks).
- Dry-run / audit-only defaults; explicit escape hatches (skip-gate-with-recorded-reason, already in §2).
- Transparency: every command states what it will touch; no hidden writes.

## Adapters (Cursor + Copilot)
`generate_adapters.py` emits, with a `# DO NOT EDIT — generated from .claude/ by generate_adapters.py` header:
- **Cursor** `.cursor/rules/`:
  - `000-claude-os.mdc` (`alwaysApply: true`) — read `.claude/CLAUDE.md` + `AGENTS.md`; the 9-stage flow + §8 safety spine; how to pick a team.
  - `web.mdc` / `mobile.mdc` / `desktop.mdc` (`globs:` scoped) — defer to the matching routing layer.
  - `skills-index.mdc` (`description`, agent-requested) — index of available skills.
- **Copilot**:
  - `.github/copilot-instructions.md` (repo-wide) — OS summary + safety + how to use.
  - `.github/instructions/{web,mobile,desktop}.instructions.md` (`applyTo:` globs) — per-surface guidance.
- **CI sync-check**: `.github/workflows/self-test.yml` runs `generate_adapters.py --check` and fails on drift. Committed outputs so the repo works on clone.

## Phasing (each its own release; this spec covers the whole vision)
- **Phase 1 (v1.5.0) — Adapters + Trust spine** ← first implementation
  1. `generate_adapters.py` + generated Cursor + Copilot files.
  2. `validate.py` linter (schemas/rules/no-fabrication).
  3. CI: run `validate.py` + `generate_adapters.py --check`; update `/self-test` command doc.
  4. README + CHANGELOG; release v1.5.0.
- **Phase 2 (v1.6.0) — Governance & compliance**: CODEOWNERS, RFC template, COMPLIANCE.md, CODE_OF_CONDUCT, SUPPORT.
- **Phase 3 (v1.7.0) — Team & scale**: monorepo orchestration, org-config layering, `/onboard`.
- **Phase 4 (v1.8.0) — Low-magic ergonomics**: tiered modes, `/quick-fix` + `/explain`, escape-hatch docs.

## Quality standards (every artifact)
- Generated files are deterministic, headered "DO NOT EDIT", and drift-checked in CI.
- `validate.py` + `integrity-check.py` both pass; `/self-test` green; no fabricated results.
- New commands/agents follow house format (frontmatter, when-to-invoke, validation, recovery, least-privilege tools).
- Additive only — no weakening of the constitution or existing gates; Claude Code behavior unchanged.

## Risks
- **Adapter drift** → mitigated by the CI sync-check (the whole point of the generator approach).
- **Over-ceremony alienating seniors** → mitigated by Pillar 4 (lite mode, fast paths) — but that's Phase 4, so Phase 1 must not add friction (it only adds an opt-in linter + generated adapters).
- **Scope size / session limits** → strict phasing; each phase is independently shippable and verified.
- **`validate.py` false positives** could block CI → ship it advisory-first if needed, then enforce.

## Out of scope (deferred → later phases / next upgrades)
Windsurf/Cline/Zed adapters (generator is extensible), a published install CLI, a hosted docs site,
and deep per-tool subagent translation. Phases 2–4 above.

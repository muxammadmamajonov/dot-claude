---
description: Verify the integrity of the .claude Project OS itself — links, shallow files, frontmatter, JSON.
argument-hint: (none)
---

# /self-test

## Purpose
Self-verify the reusable `.claude/` Operating System after editing or extending it — before committing changes or copying it into a new project. Catches the failure modes that silently creep in when files are generated or hand-edited: broken cross-references, shallow/placeholder files, missing frontmatter, and invalid settings/hook JSON.

## When to use
- After adding or editing any agent, skill, command, preset, checklist, template, or stack-matrix file.
- After a bulk generation pass (the references between files are the first thing to rot).
- Before committing changes to the system, and before copying `.claude/` into a project.
- As a periodic regression guard.

## Workflow
1. From the project root, run the three checkers (all stdlib, read-only, no network):
   ```bash
   python3 .claude/scripts/integrity-check.py      # structure
   python3 .claude/scripts/validate.py             # lint (schemas/rules)
   python3 .claude/scripts/generate_adapters.py --check   # cross-tool adapters in sync
   ```
2. `integrity-check.py` runs four structural gates and exits non-zero if any fail:
   - **Cross-reference integrity** — every `.md` path referenced anywhere resolves to a real file. Generated `docs/` artifacts and fenced ``` code-block illustrations are correctly ignored.
   - **No shallow files** — content files under `.claude/{agents,skills,checklists,commands,presets,stack-matrix}` meet a minimum word count (default 300).
   - **Frontmatter** — every agent / skill / command declares a `description:`.
   - **JSON validity** — `settings.json` and every `hooks/*.json` parse.
3. `validate.py` lints semantics — **ERRORS fail** (agent frontmatter `name/description/model/color/tools`, `color` enum, `tools` allowlist, a `When to use`/`When to invoke` section) and **WARNINGS advise** (no-fabrication clause on auditors, command/checklist section completeness). Use `--strict` to treat warnings as failures.
4. `generate_adapters.py --check` confirms the committed **Cursor** (`.cursor/rules/*.mdc`) and **GitHub Copilot** (`.github/copilot-instructions.md`, `.github/instructions/*`) adapters are in sync with `.claude/`. If stale, run it without `--check` and commit. These three checks are the CI gate (`.github/workflows/self-test.yml`).
5. For each failure, fix the offending file. Most link failures are a wrong path: use a **root-relative** `.claude/...` reference (it resolves from any file depth — skills sit two levels deep, so `../checklists/x.md` is wrong; `.claude/checklists/x.md` is right).
6. Re-run until all three report `PASS` / clean.

## Agents used
- None required. This is a deterministic script. If a content gate fails, hand the thin file to its owning agent (e.g. `.claude/agents/quality/qa-engineer.md` for a checklist) to deepen it.

## Skills used
- `.claude/skills/documentation/SKILL.md` — conventions for keeping the system's files consistent.

## Expected outputs
- A four-line gate report and a final `PASS` / `FAIL` line printed to the terminal. No files are modified.

## Stop conditions
- `integrity-check.py` is missing → the system copy is incomplete; restore `.claude/scripts/`.
- A gate fails → stop and fix the listed files; do not proceed to commit or copy until `PASS`.

## Final report format
```
## Self-Test

[1/4] Cross-reference integrity: <OK|FAIL> (<n> broken)
[2/4] No shallow files:          <OK|FAIL> (<n> thin)
[3/4] Frontmatter description:    <OK|FAIL> (<n> missing)
[4/4] JSON validity:              <OK|FAIL> (<n> invalid)

RESULT: <PASS | FAIL — items listed above>
```

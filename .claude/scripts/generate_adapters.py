#!/usr/bin/env python3
"""generate_adapters.py — derive cross-tool adapters from the canonical .claude/ source.

Single source of truth = `.claude/`. This emits tool-specific adapter files for editors/agents
that are NOT Claude Code, so the same operating system works in Cursor and GitHub Copilot (and is
extensible to others). Every generated file is deterministic and carries a DO-NOT-EDIT header.

Usage:
    python3 .claude/scripts/generate_adapters.py            # write/refresh adapter files
    python3 .claude/scripts/generate_adapters.py --check    # exit 1 if any committed adapter is stale (CI)

Pure standard library, read-only against .claude/, no network. The methodology (CLAUDE.md, skills,
checklists, templates, docs, routing maps) is portable; the Claude-Code-specific execution wiring
(subagent dispatch, slash commands, hooks, settings) is described here as a spec for other tools.
"""
import os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HEADER = "<!-- DO NOT EDIT — generated from .claude/ by .claude/scripts/generate_adapters.py. Edit .claude/ and re-run. -->"

SAFETY = ("Safety spine (always): read before write; least privilege & least blast radius; never expose "
          "secrets (reference, never reveal); human-in-the-loop for anything irreversible; headless/scheduled "
          "runs are read/review-only by default; never assume an MCP server exists; document the why. "
          "Full rules: .claude/CLAUDE.md §8.")

FLOW = ("9-stage flow: classify → interview → select → spec → build (small safe phases) → audit "
        "(security/QA/performance/accessibility) → readiness → launch → continue. Coding is stage 5; "
        "understand first. Pick the team via .claude/orchestration/routing-matrix.md.")

GLOBS = {
    "web": "**/*.{ts,tsx,js,jsx,vue,svelte,astro,css,scss,html}",
    "mobile": "**/*.{dart,swift,kt,java,m}, **/ios/**, **/android/**, **/App.{tsx,jsx}",
    "desktop": "**/src-tauri/**, **/electron/**, **/*.rs, **/main.{ts,js}, **/*.csproj",
}
ROUTING = {
    "web": ".claude/orchestration/web-routing-matrix.md (commands: /web-audit, /web-readiness)",
    "mobile": ".claude/orchestration/mobile-routing-matrix.md (commands: /mobile-audit, /store-readiness)",
    "desktop": ".claude/orchestration/desktop-routing-matrix.md (commands: /desktop-audit, /desktop-readiness)",
}

def _list(sub, suffix=None, stem=False):
    d = os.path.join(ROOT, ".claude", sub)
    if not os.path.isdir(d):
        return []
    out = []
    for name in sorted(os.listdir(d)):
        p = os.path.join(d, name)
        if suffix and os.path.isfile(p) and name.endswith(suffix):
            out.append(name[:-len(suffix)] if stem else name)
        elif suffix is None and os.path.isdir(p):
            out.append(name)
    return out

def skills_index():
    return ", ".join(_list("skills"))

def commands_index():
    return ", ".join("/" + c for c in _list("commands", ".md", stem=True))

# ---------- Cursor (.cursor/rules/*.mdc) ----------
def cursor_core():
    return f"""---
description: Universal .claude AI Project OS — core operating rules for this repo
alwaysApply: true
---
{HEADER}

This repository uses the **Universal .claude AI Project Operating System**. Treat `.claude/CLAUDE.md`
as the constitution and `AGENTS.md` as the cross-tool entry point — read them and follow them.

- {FLOW}
- {SAFETY}
- Specs precede code; record assumptions (`.claude/templates/assumptions-log.md`) and decisions (`.claude/templates/decision-record.md`).
- The full agent/skill/checklist library lives under `.claude/`. In Cursor, treat `.claude/agents/*` and
  `.claude/commands/*` as role briefs / runnable workflows and reproduce their intent with Cursor's tools;
  apply `.claude/checklists/*` as gates and `.claude/skills/*` as procedures.
"""

def cursor_path(area):
    return f"""---
description: {area.capitalize()} engineering routing for this repo
globs: {GLOBS[area]}
alwaysApply: false
---
{HEADER}

For {area} work, follow **{ROUTING[area]}** — it maps the task to the right specialists, checklists, and
operating mode (audit-only, fix-and-verify, production-hardening, …). Honor the safety spine in
`.claude/CLAUDE.md` §8. Prefer the installed `frontend-design` skill for UI polish where relevant.
"""

def cursor_skills():
    return f"""---
description: Index of available .claude skills (load the relevant one on demand)
alwaysApply: false
---
{HEADER}

This repo ships reusable procedures under `.claude/skills/<name>/SKILL.md`. When a task matches one,
read and follow it. Available skills: {skills_index()}.

Available commands (Claude Code slash commands; in Cursor, follow their documented workflow):
{commands_index()}.
"""

# ---------- GitHub Copilot ----------
def copilot_main():
    return f"""{HEADER}

# Copilot instructions — Universal .claude AI Project OS

This repository uses the **Universal .claude AI Project Operating System**. The authoritative rules are in
`.claude/CLAUDE.md` (the constitution) with the cross-tool entry point in `AGENTS.md` — follow them.

## Operating rules
- {FLOW}
- {SAFETY}
- Specs precede code. Write small, safe, reversible changes. Record assumptions and decisions under `docs/`.
- Quality gates are non-optional: security, QA, performance, accessibility (`.claude/checklists/*`, tagged P0–P3).

## How to use the system here
- Pick the team/checklists for a task via `.claude/orchestration/routing-matrix.md` (and the web/mobile/desktop layers).
- Apply `.claude/skills/<name>/SKILL.md` as procedures; treat `.claude/agents/*` as role briefs and
  `.claude/commands/*` as runnable workflows (reproduce their steps with Copilot).
- Never fabricate test results — run the real command or say it's unverified.

Available skills: {skills_index()}.
"""

def copilot_path(area):
    glob = {"web": "**/*.ts,**/*.tsx,**/*.js,**/*.jsx,**/*.vue,**/*.svelte,**/*.css,**/*.html",
            "mobile": "**/*.dart,**/*.swift,**/*.kt,**/ios/**,**/android/**",
            "desktop": "**/src-tauri/**,**/electron/**,**/*.rs,**/*.csproj"}[area]
    return f"""---
applyTo: "{glob}"
---
{HEADER}

{area.capitalize()} work in this repo: follow **{ROUTING[area]}**. Apply the matching checklists and the
§8 safety spine from `.claude/CLAUDE.md`. Audits/readiness gates must use real evidence, never fabricated results.
"""

def build():
    files = {
        ".cursor/rules/000-claude-os.mdc": cursor_core(),
        ".cursor/rules/web.mdc": cursor_path("web"),
        ".cursor/rules/mobile.mdc": cursor_path("mobile"),
        ".cursor/rules/desktop.mdc": cursor_path("desktop"),
        ".cursor/rules/skills-index.mdc": cursor_skills(),
        ".github/copilot-instructions.md": copilot_main(),
        ".github/instructions/web.instructions.md": copilot_path("web"),
        ".github/instructions/mobile.instructions.md": copilot_path("mobile"),
        ".github/instructions/desktop.instructions.md": copilot_path("desktop"),
    }
    return files

def main():
    check = "--check" in sys.argv
    files = build()
    stale = []
    for rel, content in sorted(files.items()):
        path = os.path.join(ROOT, rel)
        existing = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if check:
            if existing != content:
                stale.append(rel)
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            if existing != content:
                open(path, "w", encoding="utf-8").write(content)
                print(f"  wrote {rel}")
            else:
                print(f"  ok    {rel}")
    if check:
        if stale:
            print("STALE adapters (run generate_adapters.py and commit):")
            for s in stale:
                print(f"  {s}")
            sys.exit(1)
        print("Adapters in sync with .claude/ ✓")
    else:
        print(f"\nGenerated {len(files)} adapter files from .claude/ (Cursor + GitHub Copilot).")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""validate.py — the .claude/ linter (trust spine).

Deterministic, dependency-free rule checks on top of integrity-check.py. ERRORS are hard
violations that fail CI; WARNINGS are advisory quality nudges (reported, non-fatal). This is what
lets senior engineers trust the system is rule-enforced, not hand-wavy.

Usage:
    python3 .claude/scripts/validate.py            # report; exit 1 if any ERROR
    python3 .claude/scripts/validate.py --strict   # also treat WARNINGS as failures
"""
import os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
A = os.path.join(ROOT, ".claude")
COLORS = {"blue", "green", "red", "magenta", "cyan", "yellow"}
TOOLS = {"Read", "Write", "Edit", "Bash", "Grep", "Glob", "Task", "TodoWrite",
         "WebFetch", "WebSearch", "NotebookEdit"}
errors, warnings = [], []

def err(p, m): errors.append((os.path.relpath(p, ROOT), m))
def warn(p, m): warnings.append((os.path.relpath(p, ROOT), m))

def frontmatter(text):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    return text[3:end]

def fm_get(fm, key):
    m = re.search(rf"^{key}:\s*(.+)$", fm, re.M)
    return m.group(1).strip() if m else None

def walk(sub):
    for dp, _, fs in os.walk(os.path.join(A, sub)):
        for fn in fs:
            if fn.endswith(".md") and not fn.startswith("._"):
                yield os.path.join(dp, fn)

def check_agents():
    for fp in walk("agents"):
        t = open(fp, encoding="utf-8", errors="ignore").read()
        fm = frontmatter(t)
        if fm is None:
            err(fp, "missing YAML frontmatter"); continue
        for k in ("name", "description", "model", "color", "tools"):
            if fm_get(fm, k) is None:
                err(fp, f"frontmatter missing '{k}:'")
        color = fm_get(fm, "color")
        if color and color not in COLORS:
            err(fp, f"color '{color}' not in {sorted(COLORS)}")
        tools = fm_get(fm, "tools")
        if tools:
            for tok in re.findall(r"[A-Za-z]+", tools):
                if tok not in TOOLS:
                    err(fp, f"tool '{tok}' not in the allowlist {sorted(TOOLS)}")
        if "## When to invoke" not in t and "## When to use" not in t:
            err(fp, "missing a '## When to use' or '## When to invoke' section")
        # advisory: auditors/reviewers should pledge no fabrication
        name = (fm_get(fm, "name") or "")
        if ("auditor" in name or "reviewer" in name or name in ("qa-engineer",)):
            if not re.search(r"fabricat|never fix silently|real evidence|never assert|run real", t, re.I):
                warn(fp, "auditor/reviewer lacks an explicit no-fabrication / evidence clause")

def check_commands():
    for fp in walk("commands"):
        t = open(fp, encoding="utf-8", errors="ignore").read()
        fm = frontmatter(t)
        if fm is None or fm_get(fm, "description") is None:
            err(fp, "command missing frontmatter 'description:'")
        if "## Workflow" not in t:
            warn(fp, "command has no '## Workflow' section")
        if "## Final report" not in t and "## Expected outputs" not in t:
            warn(fp, "command has no '## Final report format' / '## Expected outputs' section")

def check_skills():
    for dp, _, fs in os.walk(os.path.join(A, "skills")):
        if "SKILL.md" in fs:
            fp = os.path.join(dp, "SKILL.md")
            t = open(fp, encoding="utf-8", errors="ignore").read()
            fm = frontmatter(t)
            if fm is None or fm_get(fm, "name") is None or fm_get(fm, "description") is None:
                err(fp, "SKILL.md missing frontmatter 'name:'/'description:'")
            if not re.search(r"when to use|## workflow|activate when", t, re.I):
                warn(fp, "skill lacks a clear when-to-use/workflow section")

def check_checklists():
    for fp in walk("checklists"):
        t = open(fp, encoding="utf-8", errors="ignore").read()
        if "P0" not in t:
            warn(fp, "checklist has no P0 tier")
        if "How to use" not in t:
            warn(fp, "checklist has no 'How to use' block")

def main():
    strict = "--strict" in sys.argv
    check_agents(); check_commands(); check_skills(); check_checklists()
    print(f"[validate] agents/commands/skills/checklists linted under .claude/")
    if errors:
        print(f"\nERRORS ({len(errors)}):")
        for rel, m in errors[:80]:
            print(f"  ✗ {rel}: {m}")
    if warnings:
        print(f"\nWARNINGS ({len(warnings)}){' (strict: fatal)' if strict else ' (advisory)'}:")
        for rel, m in warnings[:80]:
            print(f"  ⚠ {rel}: {m}")
    failed = bool(errors) or (strict and bool(warnings))
    print("\nRESULT:", "FAIL" if failed else "PASS",
          f"— {len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()

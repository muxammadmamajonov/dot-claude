#!/usr/bin/env python3
"""
Universal Project OS — integrity self-test.

Validates the reusable `.claude/` system itself (not a project built with it):
  1. Cross-reference integrity — every `.md` path referenced in any file resolves
     to a real file. Per-project OUTPUT artifacts under `docs/` are intentionally
     absent and skipped. Paths inside fenced ``` code blocks (directory-tree
     illustrations) are ignored.
  2. No shallow content files — content-bearing files meet a minimum word count.
  3. Frontmatter present — agents / skills / commands declare a `description:`.
  4. JSON validity — settings.json and every hooks/*.json parse.

Exit code 0 = all gates pass; 1 = one or more failures (details printed).
Run from the project root:  python3 .claude/scripts/integrity-check.py
"""
import os, re, sys, json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SYS_DIRS = ("agents", "checklists", "skills", "templates", "stack-matrix", "presets", "commands", "hooks", "scripts")
FENCE = re.compile(r"```.*?```", re.S)
TOK = re.compile(r"(?<![\w./-])((?:\.{0,2}/)?[\w][\w./-]*\.md)")
MIN_WORDS = 300                      # content files below this are "shallow"
SHALLOW_DIRS = ("agents", "skills", "checklists", "commands", "presets", "stack-matrix")

def md_files():
    for dp, _, fs in os.walk(ROOT):
        if "/.git" in dp:
            continue
        for fn in fs:
            if fn.endswith(".md"):
                yield os.path.join(dp, fn)

def check_links():
    broken = []
    for fp in md_files():
        txt = FENCE.sub("", open(fp, encoding="utf-8", errors="ignore").read())
        for t in set(TOK.findall(txt)):
            if "/" not in t or t.startswith(("http", "www")):
                continue
            if t.startswith((".claude/", "docs/", "examples/")):
                cand = os.path.join(ROOT, t)
            elif t.startswith("/"):
                cand = t
            else:
                cand = os.path.normpath(os.path.join(os.path.dirname(fp), t))
            rel = os.path.relpath(cand, ROOT)
            if rel.startswith("docs/") or rel.startswith(".."):
                continue            # docs/ = generated output; .. = outside repo
            if not os.path.exists(cand):
                broken.append((os.path.relpath(fp, ROOT), rel))
    return broken

def check_shallow():
    thin = []
    for fp in md_files():
        rel = os.path.relpath(fp, ROOT)
        if not rel.startswith(".claude/"):
            continue
        parts = rel.split(os.sep)
        if len(parts) < 2 or parts[1] not in SHALLOW_DIRS:
            continue
        words = len(open(fp, encoding="utf-8", errors="ignore").read().split())
        if words < MIN_WORDS:
            thin.append((rel, words))
    return thin

def check_frontmatter():
    missing = []
    base = os.path.join(ROOT, ".claude")
    for sub in ("agents", "skills", "commands"):
        for dp, _, fs in os.walk(os.path.join(base, sub)):
            for fn in fs:
                if not fn.endswith(".md"):
                    continue
                fp = os.path.join(dp, fn)
                head = "".join(open(fp, encoding="utf-8", errors="ignore").readlines()[:8])
                if "description:" not in head:
                    missing.append(os.path.relpath(fp, ROOT))
    return missing

def check_json():
    bad = []
    cfg = os.path.join(ROOT, ".claude")
    candidates = [os.path.join(cfg, "settings.json")]
    hooks = os.path.join(cfg, "hooks")
    if os.path.isdir(hooks):
        candidates += [os.path.join(hooks, f) for f in os.listdir(hooks) if f.endswith(".json")]
    for j in candidates:
        if not os.path.exists(j):
            continue
        try:
            json.load(open(j, encoding="utf-8"))
        except Exception as e:
            bad.append((os.path.relpath(j, ROOT), str(e)))
    return bad

def main():
    failed = False
    broken = check_links()
    print(f"[1/4] Cross-reference integrity: {'FAIL' if broken else 'OK'} ({len(broken)} broken)")
    for src, tgt in broken[:50]:
        print(f"      {src}  ->  {tgt}")
    failed |= bool(broken)

    thin = check_shallow()
    print(f"[2/4] No shallow files (<{MIN_WORDS} words): {'FAIL' if thin else 'OK'} ({len(thin)} thin)")
    for rel, w in thin[:50]:
        print(f"      {rel}  ({w} words)")
    failed |= bool(thin)

    miss = check_frontmatter()
    print(f"[3/4] Frontmatter description present: {'FAIL' if miss else 'OK'} ({len(miss)} missing)")
    for rel in miss[:50]:
        print(f"      {rel}")
    failed |= bool(miss)

    bad = check_json()
    print(f"[4/4] JSON validity: {'FAIL' if bad else 'OK'} ({len(bad)} invalid)")
    for rel, err in bad:
        print(f"      {rel}: {err}")
    failed |= bool(bad)

    print("\nRESULT:", "FAIL — fix the items above." if failed else "PASS — system integrity verified.")
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()

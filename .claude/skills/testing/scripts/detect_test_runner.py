#!/usr/bin/env python3
"""detect_test_runner.py — deterministic test-runner detector.

Inspects a repository's manifests/config to report which test runner(s) it uses
and the command to run them. Pure standard library, read-only, no network. Use
this as the mechanical first step of the `testing` skill so the test plan targets
the runner the project actually uses instead of guessing.

Usage:
    python3 detect_test_runner.py [REPO_DIR]   # defaults to cwd
    python3 detect_test_runner.py --json
"""
import os, re, sys, json

def read(p):
    try:
        return open(p, encoding="utf-8", errors="ignore").read()
    except OSError:
        return ""

def detect(root):
    found = []  # (runner, command, evidence)
    j = os.path.join

    pkg = read(j(root, "package.json"))
    if pkg:
        low = pkg.lower()
        for name, cmd in [("vitest", "npx vitest run"), ("jest", "npx jest"),
                          ("mocha", "npx mocha"), ("@playwright/test", "npx playwright test"),
                          ("cypress", "npx cypress run"), ("ava", "npx ava"),
                          ("node:test", "node --test")]:
            if f'"{name}"' in low or (name == "node:test" and "node --test" in low):
                found.append((name.replace("@playwright/test", "playwright"),
                              cmd, "package.json"))
        if not found and '"test"' in low:
            found.append(("npm-script", "npm test", "package.json scripts.test"))

    if read(j(root, "pyproject.toml")).find("pytest") >= 0 or os.path.exists(j(root, "pytest.ini")) \
       or os.path.exists(j(root, "tox.ini")) or "pytest" in read(j(root, "requirements.txt")).lower() \
       or "pytest" in read(j(root, "setup.cfg")).lower():
        found.append(("pytest", "python -m pytest -q", "pytest config"))
    elif os.path.isdir(j(root, "tests")) and (os.path.exists(j(root, "pyproject.toml"))
                                              or os.path.exists(j(root, "setup.py"))):
        found.append(("unittest", "python -m unittest discover", "tests/ dir"))

    if os.path.exists(j(root, "go.mod")):
        found.append(("go test", "go test ./...", "go.mod"))
    if os.path.exists(j(root, "Cargo.toml")):
        found.append(("cargo test", "cargo test", "Cargo.toml"))

    gem = read(j(root, "Gemfile")).lower()
    if "rspec" in gem: found.append(("rspec", "bundle exec rspec", "Gemfile"))
    elif "minitest" in gem or os.path.isdir(j(root, "test")):
        if os.path.exists(j(root, "Gemfile")): found.append(("minitest", "bin/rails test", "Gemfile/test dir"))

    comp = read(j(root, "composer.json")).lower()
    if "pestphp" in comp or "pest" in comp: found.append(("pest", "./vendor/bin/pest", "composer.json"))
    elif "phpunit" in comp: found.append(("phpunit", "./vendor/bin/phpunit", "composer.json"))

    for dp, dirs, files in os.walk(root):
        if dp[len(root):].count(os.sep) > 2: dirs[:] = []
        if any(f.endswith(".csproj") for f in files):
            c = "".join(read(j(dp, f)) for f in files if f.endswith(".csproj")).lower()
            runner = "xunit" if "xunit" in c else "nunit" if "nunit" in c else "mstest" if "mstest" in c else "dotnet"
            found.append((f"dotnet test ({runner})", "dotnet test", os.path.basename(dp)))
            break

    # de-dup by runner name
    seen, uniq = set(), []
    for r, cmd, ev in found:
        if r not in seen:
            seen.add(r); uniq.append({"runner": r, "command": cmd, "evidence": ev})
    return {"runners": uniq}

def main():
    args = [a for a in sys.argv[1:] if a != "--json"]
    as_json = "--json" in sys.argv
    root = os.path.abspath(args[0]) if args else os.getcwd()
    res = detect(root)
    if as_json:
        print(json.dumps(res, indent=2)); return
    print(f"# Test-runner detection for {root}\n")
    if not res["runners"]:
        print("No test runner detected. The project may have no tests yet — the testing "
              "skill should propose one appropriate to the stack (see stack-matrix/testing.md).")
        return
    for r in res["runners"]:
        print(f"- {r['runner']:24s} run: `{r['command']}`   (from {r['evidence']})")
    print("\nNote: mechanical detection only. Use the testing skill to design the test "
          "strategy (unit/integration/e2e split, coverage targets, CI gate).")

if __name__ == "__main__":
    main()

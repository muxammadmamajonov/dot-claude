#!/usr/bin/env python3
"""detect_stack.py — deterministic project-type / stack detector.

Scans a repository for manifest and config files and prints the detected
languages, frameworks, and candidate project types (mapped to .claude presets).
Pure standard library, read-only, no network. Use this as the mechanical first
pass of the `project-classification` skill so every classification starts from
the same evidence instead of re-deriving it by hand.

Usage:
    python3 detect_stack.py [REPO_DIR]   # defaults to cwd
    python3 detect_stack.py --json       # machine-readable output
"""
import os, re, sys, json

# filename (or glob-ish suffix) -> (language, framework-hint, candidate preset)
# Checked in order; presence contributes a signal. Deps are inspected where useful.
MANIFESTS = {
    "package.json":      ("JavaScript/TypeScript", None, None),
    "tsconfig.json":     ("TypeScript", None, None),
    "Cargo.toml":        ("Rust", None, "backend-api"),
    "go.mod":            ("Go", None, "backend-api"),
    "pyproject.toml":    ("Python", None, None),
    "requirements.txt":  ("Python", None, None),
    "Pipfile":           ("Python", None, None),
    "Gemfile":           ("Ruby", None, None),
    "composer.json":     ("PHP", None, None),
    "pubspec.yaml":      ("Dart/Flutter", "Flutter", "mobile-app"),
    "pom.xml":           ("Java", None, "backend-api"),
    "build.gradle":      ("Java/Kotlin", None, None),
    "build.gradle.kts":  ("Kotlin", None, None),
    "project.godot":     ("Godot/GDScript", "Godot", "game-2d"),
    "hardhat.config.js": ("Solidity", "Hardhat", "blockchain-app"),
    "hardhat.config.ts": ("Solidity", "Hardhat", "blockchain-app"),
    "foundry.toml":      ("Solidity", "Foundry", "blockchain-app"),
    "Anchor.toml":       ("Rust/Solana", "Anchor", "blockchain-app"),
    "platformio.ini":    ("C/C++ (embedded)", "PlatformIO", "iot-embedded"),
    "Dockerfile":        (None, "Docker", None),
}
SUFFIX_SIGNALS = {
    ".csproj": ("C#/.NET", None, "backend-api"),
    ".sln":    ("C#/.NET", None, None),
    ".uproject": ("Unreal/C++", "Unreal", "game-3d"),
    ".ino":    ("Arduino/C++", "Arduino", "iot-embedded"),
    ".tf":     (None, "Terraform", None),
}

def read(path):
    try:
        return open(path, encoding="utf-8", errors="ignore").read()
    except OSError:
        return ""

def detect(root):
    langs, frameworks, presets, evidence = set(), set(), set(), []
    top = set(os.listdir(root)) if os.path.isdir(root) else set()

    for fn, (lang, fw, preset) in MANIFESTS.items():
        if fn in top:
            evidence.append(fn)
            if lang: langs.add(lang)
            if fw: frameworks.add(fw)
            if preset: presets.add(preset)

    # suffix-based signals (scan top level + one level deep, cheap)
    for dirpath, dirs, files in os.walk(root):
        depth = dirpath[len(root):].count(os.sep)
        if depth > 2 or "/." in dirpath or "node_modules" in dirpath:
            dirs[:] = [d for d in dirs if not d.startswith(".") and d != "node_modules"]
            continue
        for f in files:
            for suf, (lang, fw, preset) in SUFFIX_SIGNALS.items():
                if f.endswith(suf):
                    evidence.append(f)
                    if lang: langs.add(lang)
                    if fw: frameworks.add(fw)
                    if preset: presets.add(preset)

    # inspect package.json deps for framework + preset refinement
    if "package.json" in top:
        pkg = read(os.path.join(root, "package.json"))
        deps = pkg.lower()
        web = {"next": ("Next.js", "web-app"), "react": ("React", "web-app"),
               "vue": ("Vue", "web-app"), "nuxt": ("Nuxt", "web-app"),
               "svelte": ("Svelte", "web-app"), "@angular/core": ("Angular", "web-app"),
               "astro": ("Astro", "static-site")}
        back = {"express": "Express", "fastify": "Fastify", "@nestjs/core": "NestJS"}
        for k, (fw, preset) in web.items():
            if f'"{k}"' in deps: frameworks.add(fw); presets.add(preset)
        for k, fw in back.items():
            if f'"{k}"' in deps: frameworks.add(fw); presets.add("backend-api")
        if '"react-native"' in deps or '"expo"' in deps:
            frameworks.add("React Native"); presets.add("mobile-app")
        if '"electron"' in deps: frameworks.add("Electron"); presets.add("desktop-app")
        if '"manifest_version"' in deps or os.path.exists(os.path.join(root, "manifest.json")):
            presets.add("browser-extension")
        # CLI heuristic: a "bin" field with no web framework
        if '"bin"' in deps and not (frameworks & {"Next.js","React","Vue","Nuxt","Svelte","Angular"}):
            presets.add("cli-tool")

    # python framework refinement
    pytext = (read(os.path.join(root, "pyproject.toml")) +
              read(os.path.join(root, "requirements.txt")) +
              read(os.path.join(root, "Pipfile"))).lower()
    for k, (fw, preset) in {"fastapi": ("FastAPI", "backend-api"),
                            "django": ("Django", "backend-api"),
                            "flask": ("Flask", "backend-api")}.items():
        if k in pytext: frameworks.add(fw); presets.add(preset)

    # ruby / php refinement
    if "rails" in read(os.path.join(root, "Gemfile")).lower():
        frameworks.add("Rails"); presets.add("backend-api")
    if "laravel" in read(os.path.join(root, "composer.json")).lower():
        frameworks.add("Laravel"); presets.add("backend-api")

    # unity heuristic
    if os.path.isdir(os.path.join(root, "Assets")) and os.path.isdir(os.path.join(root, "ProjectSettings")):
        frameworks.add("Unity"); presets.add("game-3d")

    return {
        "languages": sorted(langs),
        "frameworks": sorted(frameworks),
        "candidate_presets": sorted(presets) or ["custom-project"],
        "evidence": sorted(set(evidence)),
    }

def main():
    args = [a for a in sys.argv[1:] if a != "--json"]
    as_json = "--json" in sys.argv
    root = os.path.abspath(args[0]) if args else os.getcwd()
    result = detect(root)
    if as_json:
        print(json.dumps(result, indent=2)); return
    print(f"# Stack detection for {root}\n")
    print("Languages:        " + (", ".join(result["languages"]) or "none detected"))
    print("Frameworks:       " + (", ".join(result["frameworks"]) or "none detected"))
    print("Candidate presets: " + ", ".join(result["candidate_presets"]))
    print("Evidence:         " + (", ".join(result["evidence"]) or "no manifests found"))
    print("\nNote: this is a mechanical first pass. Confirm risk tier, cross-cutting "
          "concerns, and the final preset with the project-classification skill.")

if __name__ == "__main__":
    main()

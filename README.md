# .claude — Universal AI Project Operating System

A **reusable, project-agnostic operating system for AI-assisted software delivery.** Drop the `.claude/` directory into any repository and Claude Code stops improvising. It classifies the project, interviews you for requirements, writes specs, picks a stack, designs the architecture, plans a roadmap, builds in small safe phases, audits security/QA/performance/accessibility, and walks the project to a production launch — without skipping the thinking.

It is **universal by design.** It does not assume you are building a web app. The same system drives web, mobile, desktop, games, backend APIs, CLIs, browser extensions, AI agent systems, data platforms, IoT/embedded, blockchain, SaaS, ecommerce, marketplaces, fintech, CRM/ERP, helpdesk, social/media, and bespoke projects. Detect the type first; everything downstream adapts.

---

## Get started in one prompt — works with any AI

Copy the block below into any AI coding assistant, in any project. It clones this repo, drops `.claude/`
and `AGENTS.md` into place, and hands control to the constitution — the assistant classifies your
project and takes it from there. No manual setup required first.

```
You are an AI coding assistant. Adopt the Universal `.claude` AI Project Operating System from this
repository into the current project: https://github.com/muxammadmamajonov/dot-claude.git

1. If you have shell/file access: clone that repo to a temp location and copy its `.claude/` directory
   and its `AGENTS.md` file into the root of THIS project (the one we're working in right now), next to
   the existing files — do not overwrite or delete anything else here.

     git clone --depth 1 https://github.com/muxammadmamajonov/dot-claude.git /tmp/dotclaude-os
     cp -R /tmp/dotclaude-os/.claude ./.claude
     cp /tmp/dotclaude-os/AGENTS.md ./AGENTS.md

   If you don't have shell/file access, tell me these three commands so I can run them, or fetch the
   files directly from the repository.

2. Read `.claude/CLAUDE.md` in full. It is this project's constitution and overrides your default
   behavior — follow it exactly, starting now.

3. If you are Claude Code: run `/self-test` to confirm the copy is intact, then run `/start-project`
   (new project) or `/continue-work` (existing codebase).

4. If you are any other AI tool (Codex, Cursor, Gemini CLI, Copilot, or otherwise): read `AGENTS.md`
   first, then `.claude/orchestration/routing-matrix.md`, and follow the 9-stage flow it describes
   (classify → interview → select → spec → build → audit → readiness → launch → continue) using your
   own tools to reproduce each step — do not skip straight to writing code.

5. Before doing anything else: classify this project (web, mobile, desktop, backend, CLI, game, data
   platform, or otherwise), tell me what you found, and ask me only the business-critical questions you
   genuinely cannot answer yourself. Decide everything else and log it as an assumption.

Never run a destructive or irreversible command (force-push, rm -rf, dropping a database, editing an
existing migration, exposing a secret) without asking me first and getting explicit approval — see
`.claude/CLAUDE.md` §8.
```

Works in Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot, or any other coding agent that can read
files — the constitution and the 9-stage flow are portable; only the execution wiring (subagent
dispatch, slash commands, hooks, settings) is Claude-Code-native. See [Works in any agent](#works-in-any-agent)
for the full breakdown, or [Install — copy it into a project](#install--copy-it-into-a-project) below if
you'd rather do the copy yourself and skip the prompt.

---

## Why

Left alone, an AI assistant jumps straight to code, makes silent architectural choices, and leaves no trail. This OS inverts that:

- **Understand before building.** Coding is stage 5 of 9 — four stages of understanding and design come first, four gates of verification follow.
- **Gate quality.** Security, QA, performance, and accessibility are non-optional gates with severity-tagged checklists, not afterthoughts.
- **Document the why.** Every non-trivial decision becomes a logged assumption or a decision record, so you stay in control without being interrogated.
- **Orchestrate safely.** Irreversible actions are blocked at the permission layer; the user is asked only about decisions that actually matter.

The value is the **flow and the gates between stages**, not any single clever prompt — and it is portable across every project you copy it into.

---

## What `.claude/` contains

`.claude/` is the only directory you copy into a real project. It has 13 parts:

| Part | Count | Purpose |
|------|-------|---------|
| **`CLAUDE.md`** | 1 | The constitution: the 9-stage flow, the Definition of Done, and the hard safety rules (§8). Project law. |
| **`settings.json`** | 1 | Always-on safety baseline: `permissions.deny` blocks destructive ops; `permissions.ask` gates pushes, deploys, migrations, installs. |
| **`agents/`** | 128 | Specialized roles in six families — `core`, `engineering`, `quality`, `design`, `domain`, `stack`. The doers. |
| **`skills/`** | 65 | Reusable, on-demand procedures, one folder per skill at `skills/<name>/SKILL.md`. The how-to library. |
| **`commands/`** | 39 | Slash-command entry points — the invokable workflow and its gates. |
| **`hooks/`** | 9 | Opt-in, safe-by-default JSON guards. Off until you copy one into `settings.json`; they warn or block, never mutate or expose secrets. |
| **`orchestration/`** | 5 | `routing-matrix.md` (universal) plus the `web-`, `mobile-`, `desktop-`, and `monorepo-routing-matrix.md` layers — map each project type (or each package, in a monorepo) to its minimal active team. |
| **`presets/`** | 38 | Per-project-type starting configs that pre-wire agents, skills, stack-matrix entries, checklists, and templates. |
| **`stack-matrix/`** | 20 | Technology decision matrices per concern (web, backend, database, cloud, AI/ML, payments, …) with real trade-offs. |
| **`checklists/`** | 34 | Gate definitions, every item tagged **P0/P1/P2/P3**. Audits run against these. |
| **`templates/`** | 30 | Blank, structured documents agents fill in (spec, architecture, data model, ADR, RFC, runbook, …). |
| **`scripts/`** | 3 | The toolchain behind `/self-test` + CI: `integrity-check.py` (structure), `validate.py` (lint — schemas, tools allowlist, no-fabrication), `generate_adapters.py` (Cursor + Copilot adapters). |
| **`docs/`** | 9 | Portable operating-capability guides for wielding every Claude Code primitive safely, plus compliance mapping, org-config layering, and operating modes. |

Generated artifacts (project profile, specs, ADRs, roadmap, audit reports, assumptions log) are written into the **target project's own `docs/`** — never into `.claude/`, which stays reusable and project-agnostic.

---

## Install — copy it into a project

```bash
# from the root of your target project
cp -R /path/to/this-repo/.claude ./.claude

# optional: keep the reference docs handy while you learn the system
cp /path/to/this-repo/{README.md,PROJECT_OS.md,START_HERE.md} ./
cp -R /path/to/this-repo/examples ./examples
```

Only `.claude/` is required at runtime. Commit it with your project so every collaborator — and every future AI session — shares the same operating system. An existing codebase is fine: the OS detects prior code during classification and switches into an "adopt & harden" mode instead of greenfield scaffolding.

---

## Start — one command

Open the project with Claude Code and run:

```
/start-project
```

That hands control to the **orchestrator** (`.claude/agents/core/orchestrator.md`), which drives the full lifecycle: you answer a short interview, it does the rest, pausing only at genuine decision points. Two other front doors:

```
/brainstorm-project   # shape a raw idea into a brief before classifying
/continue-work        # resume an in-flight or existing project at the right stage
```

The orchestrator runs a **strict, resumable, 9-stage pipeline** (the canonical flow in `.claude/CLAUDE.md` §2). Each stage has an owner and a gate that must pass before the next begins:

| # | Stage | What happens | Primary command(s) |
|---|-------|--------------|--------------------|
| 1 | **Classify** | Detect project type, platform(s), scale, risk class, compliance needs; pick the matching preset. | `/start-project`, `/classify-project`, `/route` |
| 2 | **Interview** | Ask only business-critical questions (users, goals, must-haves, compliance, budget, deadlines). Document assumptions for the rest. | `/interview-founder` |
| 3 | **Select** | Assemble the minimal active team: preset + agents + skills + stack-matrix + checklists + templates. | `/route`, `/select-stack` |
| 4 | **Spec** | Write specs before code: vision, scope, architecture, data model, API/interface contracts, milestones. | `/create-specs`, `/design-architecture`, `/design-data-model`, `/create-roadmap` |
| 5 | **Build** | Implement in small, safe, independently revertible phases — one coherent slice at a time. | `/build-prototype`, `/implement-feature`, `/create-tests` |
| 6 | **Audit** | Run the non-optional gates: security, QA, performance, accessibility. | `/audit-security`, `/audit-performance`, `/review-feature` |
| 7 | **Readiness** | Verify production readiness: observability, backups, rollback, runbooks, scaling, cost, compliance. | `/audit-production` |
| 8 | **Launch** | Prepare and execute launch: staged rollout, monitoring, go/no-go, comms. | `/prepare-launch` |
| 9 | **Continue** | Triage feedback, plan the next slice, re-enter the flow at the right stage. | `/continue-work` |

> Golden rule: **classify → interview → select → spec → build → audit → readiness → launch → continue.** Never skip to coding.

---

## How each primitive works

**Agents** are the doers. The `core/` orchestrator never does the deep work itself — it routes, sequences, and enforces gates, delegating to specialists across six families: `core/` (the spine), `engineering/` (the builders), `quality/` (the gate owners), `design/`, `domain/` (cross-cutting business expertise), and `stack/` (per-framework specialists). New agents register in the orchestrator so the router can dispatch to them.

**Skills** are reusable, composable know-how an agent loads on demand — how to run a security review, how to write a migration safely, how to model data for a given stack. The directory is flat: one folder per skill, each with a `SKILL.md` carrying a clear trigger and a step-by-step procedure. Agents pick them up automatically.

**Commands** are thin, human-typed entry points (slash commands) that start or steer the workflow. They delegate to agents rather than embedding logic, so the same command behaves consistently across project types. `/start-project` is the front door; the rest cover every stage and gate.

**Hooks** are opt-in, safe-by-default guards that enforce the safety rules mechanically. They are **off until you copy one into `settings.json`**. When on, they warn or block via a non-zero exit — blocking commits that contain secrets, running a checklist before a "ship" command, formatting on save — and never mutate, install, or expose anything on their own.

**Presets** are per-project-type starting configs. A preset pre-wires the right agents, skills, stack-matrix entries, checklists, and templates for a type (web-app, mobile-app, backend-api, game-2d, data-platform, blockchain-app, …) so classification lands on a sensible default team instead of a blank slate.

**Stack-matrix** entries are curated technology decision tables per concern, each comparing the real options — when to use, when not to, strengths, risks, recommended combinations — so the stack choice is informed and defensible rather than improvised.

**Templates** are blank, structured Markdown documents the agents fill in: product spec, architecture, data model, API spec, decision record, assumptions log, runbook, launch checklist, and more. Change the headings to match how your team documents work and every agent that uses the template inherits the change.

**Checklists** are the bar work must clear. Every item is severity-tagged **P0** (blocker) / **P1** (important) / **P2** (hardening) / **P3** (backlog). The audit and readiness gates run against them; a red P0 stops the stage until it is fixed or recorded as an explicit risk.

A request flows through all of them: you type a **command** → the orchestrator **agent** consults the matching **preset**, **routing-matrix**, and **stack-matrix** → it loads relevant **skills** → it writes artifacts from **templates** → at each gate it audits against **checklists**.

---

## Operating capabilities

Beyond the project-delivery flow, the OS ships portable guides in `.claude/docs/` for wielding every Claude Code runtime primitive — Terminal, Memory, Commands, Custom Commands, Skills, MCP, Subagents, Hooks, Headless, and Routines — under one safety spine.

| Guide | Covers |
|-------|--------|
| [`CLAUDE_CODE_OPERATING_MODEL.md`](.claude/docs/CLAUDE_CODE_OPERATING_MODEL.md) | The umbrella — how all the primitives fit together. |
| [`MCP_STRATEGY.md`](.claude/docs/MCP_STRATEGY.md) | When and how to add MCP servers; tool scoping and safety. Never assume a server exists. |
| [`SUBAGENT_ORCHESTRATION.md`](.claude/docs/SUBAGENT_ORCHESTRATION.md) | Delegating to subagents and composing parallel work. |
| [`MEMORY_STRATEGY.md`](.claude/docs/MEMORY_STRATEGY.md) | What to persist, where, and how memory survives sessions. |
| [`HEADLESS_AND_ROUTINES.md`](.claude/docs/HEADLESS_AND_ROUTINES.md) | Non-interactive runs and scheduled/recurring automations — read/review-only by default. |
| [`HOOKS_SAFETY_MODEL.md`](.claude/docs/HOOKS_SAFETY_MODEL.md) | The opt-in hook model that enforces the safety rules mechanically. |

These pair with commands that operationalize them: `/setup-mcp` (wire an MCP server), `/headless-run` (drive the OS non-interactively), `/manage-routines` (create and tend scheduled agents), `/commit-ready` (prep a clean, reviewed commit), and `/create-github-issues` (turn a roadmap into tracked issues).

---

## Web, mobile & desktop engineering layers

On top of the universal flow, the OS ships three elite-team **engineering layers**. `/route` detects whether a project is web, mobile, desktop, or mixed and loads only the relevant one(s).

- **Web** — `.claude/orchestration/web-routing-matrix.md`: task→specialist routing with operating **modes** (audit-only, fix-and-verify, production-hardening, ui-ux-polish, security-review, performance-review, release-readiness, documentation) and verification loops. Commands: **`/web-audit <scope> [--mode]`** (frontend, backend, api, database, security, performance, accessibility, responsive, devops, observability, full) and **`/web-readiness`** (ship gate against `.claude/checklists/web-production.md`). Specialists added: `codebase-mapper`, `playwright-e2e-engineer`, `refactoring-specialist`, `bug-fix-specialist`, `auth-permission-reviewer`.
- **Mobile** — `.claude/orchestration/mobile-routing-matrix.md`: platform detection (React Native, Expo, Flutter, native iOS/Android, KMP, Ionic/Capacitor, PWA, Telegram Mini App) plus an **app-store-readiness** mode. Commands: **`/mobile-audit <scope> [--mode]`** and **`/store-readiness`** (App Store + Google Play gate against `.claude/checklists/app-store-readiness.md` + `mobile-production.md`). Specialists added: `mobile-security-auditor` (MASVS), `mobile-release-engineer` (Fastlane/EAS/signing), `mobile-e2e-engineer` (Maestro/Detox/XCUITest/Espresso); per-framework engineers already live under `.claude/agents/stack/mobile/`. PWA & Telegram Mini Apps route to the web layer plus `.claude/presets/telegram-mini-app.md` (server-side `initData` validation is a P0).

- **Desktop** — `.claude/orchestration/desktop-routing-matrix.md`: framework detection (Electron, Tauri, Flutter Desktop, Qt/GTK, .NET desktop, native macOS/Windows/Linux) plus **desktop-packaging-readiness** and **auto-update-readiness** modes and per-OS caveats. Commands: **`/desktop-audit <scope> [--mode]`** and **`/desktop-readiness`** (ship gate against `.claude/checklists/desktop-production.md` + `desktop-distribution.md` — signing, notarization, installers, secure auto-update). Specialists added: `electron-engineer`, `tauri-engineer`, `desktop-security-auditor` (shell + update integrity), `desktop-release-engineer` (signing/notarization/packaging/auto-update across mac·win·linux). Native/Qt/.NET route to `desktop-engineer` + the matching stack engineer.

For UI/visual polish all three layers prefer the high-install `frontend-design` skill (and `vercel-react-native-skills` for RN, `tauri-v2` for Tauri) when installed. A GitHub Actions workflow (`.github/workflows/self-test.yml`) runs the integrity gate on every push/PR.

---

## Governance & compliance

On top of the core flow, the OS ships a governance layer for teams that need review discipline and a compliance paper trail, not just working code.

- **Review ownership** — [`.github/CODEOWNERS`](.github/CODEOWNERS) routes changes to the constitution, safety baseline, and security/compliance-sensitive paths to the right reviewers (ships with placeholder teams — replace them before this takes effect).
- **RFC process** — significant changes to the shared `.claude/` OS itself (a new stage, a new agent family, a schema change) go through [`.claude/templates/rfc.md`](.claude/templates/rfc.md) and `CONTRIBUTING.md` §11 before code — distinct from [`.claude/templates/decision-record.md`](.claude/templates/decision-record.md), which is for a *consuming* project's own technical decisions.
- **Compliance mapping** — [`.claude/docs/COMPLIANCE.md`](.claude/docs/COMPLIANCE.md) maps the OS's existing gates and checklists to SOC 2, ISO/IEC 27001, SLSA, and OWASP control families, so a team already running this OS can see what evidence it already produces as a byproduct of delivery. It is a mapping aid, not a certification — read its disclaimer first.
- **Complete OSS governance set** — [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) and [`SUPPORT.md`](SUPPORT.md) join the existing [`SECURITY.md`](SECURITY.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Team & scale

For a monorepo, a multi-team org, or a project someone new needs to pick up cold:

- **Monorepo orchestration** — [`.claude/orchestration/monorepo-routing-matrix.md`](.claude/orchestration/monorepo-routing-matrix.md) detects workspace topology, classifies each package independently, separates root-scoped concerns (CI, shared lockfile, release) from package-scoped ones, and sizes the blast radius of a shared-package change from the dependency graph instead of re-auditing the whole repo. `/route` runs this detection first.
- **Org config layering** — [`.claude/docs/ORG_CONFIG_LAYERING.md`](.claude/docs/ORG_CONFIG_LAYERING.md) documents a two-tier model: an org-wide `.claude/org/` overlay sets a floor (banned dependencies, mandatory checklist items, a security contact) that a repo can tighten but never weaken.
- **Fast onboarding** — **`/onboard`** (`.claude/commands/onboard.md`) runs the codebase-mapper plus classification once and writes a single `docs/ONBOARDING.md` brief — stack, how a request flows, active team, known risks, how to run it — so a new engineer or a fresh AI session starts from facts instead of re-discovering the repo.
- **Versioning discipline** — `CONTRIBUTING.md` §12 classifies every change to the shared tree as patch/minor/major and says exactly when a major bump needs an accepted RFC first.

## Low-magic ergonomics

The full 9-stage flow is the default for anything non-trivial — but a typo fix doesn't need a spec.
[`.claude/docs/OPERATING_MODES.md`](.claude/docs/OPERATING_MODES.md) makes the trivial/non-trivial
boundary explicit instead of an ad-hoc judgment call, so getting out of your way on small work never
means weakening anything on work that isn't small:

- **`/quick-fix`** — lite mode's entry point: a small, well-understood, low-risk change skips the interview/spec ceremony but never skips verification, and auto-escalates back to the full flow the moment the diff turns out bigger than expected or touches anything on the §8 safety list.
- **`/explain`** — a read-only command for when the ask is understanding, not building. Traces the real code path and answers with `file:line` references; never edits anything, never writes a file unless you ask it to.
- **Expert mode** — for experienced users who'd rather self-navigate stages than have the orchestrator force sequencing; gate-skips are still recorded, just as a one-line acknowledgment instead of a fresh negotiation every time.
- **No hidden writes** — every command in this system states what it's about to touch before touching it.

---

## Safety rules

The OS is **safe by default**, enforced two ways.

**1. Permission policy — always on (`.claude/settings.json`).** Sensitive operations are split into *deny* (never) and *ask* (explicit human approval):

- **Denied outright:** `rm -rf` and recursive force-deletes, `git push --force` to shared branches, dropping databases or destroying migrations, printing or committing secrets/`.env` files, and any irreversible production mutation.
- **Ask-first:** schema migrations, dependency/lockfile changes, infrastructure applies, package publishing, database CLIs, remote execution, and writes outside the project root.
- **Allowed:** reading code, running tests, linting, formatting, building, and writing within the project — the everyday loop runs without friction.

**2. Opt-in hooks.** Hooks are **off unless you enable them** in `settings.json`. When on they add scoped, auditable guardrails (secret-scan on commit, checklist-before-ship, format-on-save) and never run destructive actions on their own.

The **safety spine** runs through everything: read before write; least privilege and least blast radius; never expose secrets (reference, never reveal); human-in-the-loop for anything irreversible; headless and routines are read/review-only by default (writes need explicit opt-in plus a rollback path); never assume an MCP server exists; document the why. No agent may delete data, rewrite history, expose secrets, or take an irreversible production action without explicit human approval — even if it seems convenient.

---

## Verify the system

The `.claude/` tree is held together by cross-references and structured frontmatter. To confirm its integrity after copying or customizing, run:

```
/self-test
```

It executes `.claude/scripts/integrity-check.py`, which checks internal links resolve, files are not shallow, frontmatter is well-formed, and JSON parses. Run it after any edit to the system itself.

---

## Customize it

The OS is meant to be tuned per organization and per project.

- **Add a preset** — `.claude/presets/<type>.md` for a project type you build often; encode default classification answers, stack leanings, and which checklists matter most.
- **Add an agent** — `.claude/agents/<family>/<role>.md` with a focused mandate, then register it in `.claude/agents/core/orchestrator.md`.
- **Add a skill** — `.claude/skills/<name>/SKILL.md` with a clear trigger and step-by-step procedure.
- **Edit checklists** — extend `.claude/checklists/*` with your compliance, security, or accessibility requirements; they become hard gates.
- **Extend the stack-matrix** — add approved/blocked technologies in `.claude/stack-matrix/*` so stack decisions reflect your standards.
- **Tune `settings.json`** — adjust the deny/ask lists and opt-in hooks. Keep machine-specific overrides in `.claude/settings.local.json` (git-ignored).

---

## Works in any agent

It's **native to Claude Code** (the `claude` CLI — interactive *and* headless `claude -p` / Agent SDK / CI): agents, slash commands, skills, hooks, and `settings.json` all execute with zero setup. It's also **usable in other agents** (Codex, Cursor, Gemini CLI, Copilot CLI, opencode) via the root **[`AGENTS.md`](AGENTS.md)** entry point — the constitution, skills, checklists, templates, and docs are portable plain markdown; only the execution wiring (subagent dispatch, slash commands, hooks, settings) is Claude Code-specific and is read as a spec elsewhere.

For **Cursor** and **GitHub Copilot**, ready-made adapters are **generated from `.claude/`** — `.cursor/rules/*.mdc` and `.github/copilot-instructions.md` + `.github/instructions/*` — so those editors pick up the operating rules with zero setup. They're produced by `.claude/scripts/generate_adapters.py` (`.claude/` is the single source of truth) and a CI drift-check keeps them in sync; the files carry a `DO NOT EDIT — generated` header. Full breakdown: the portability matrix in [`.claude/docs/CLAUDE_CODE_OPERATING_MODEL.md`](.claude/docs/CLAUDE_CODE_OPERATING_MODEL.md).

## Learn more

- **[AGENTS.md](AGENTS.md)** — cross-tool entry point (Claude Code + Codex/Cursor/Gemini/Copilot).
- **[START_HERE.md](START_HERE.md)** — a 60-second quick start.
- **[PROJECT_OS.md](PROJECT_OS.md)** — the design philosophy and full flow in depth.
- **[examples/](examples/)** — worked project briefs across types (web/SaaS, mobile, game, AI agent).
- **[.claude/CLAUDE.md](.claude/CLAUDE.md)** — the constitution every agent obeys.
- **[CONTRIBUTING.md](CONTRIBUTING.md)** — house style, the RFC process (§11), and versioning discipline for the shared tree (§12).
- **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)**, **[SUPPORT.md](SUPPORT.md)**, **[SECURITY.md](SECURITY.md)** — the community, help, and safety-reporting docs.

Key cross-references to read first: [`.claude/agents/core/orchestrator.md`](.claude/agents/core/orchestrator.md), [`.claude/orchestration/routing-matrix.md`](.claude/orchestration/routing-matrix.md), [`.claude/checklists/security.md`](.claude/checklists/security.md), and [`.claude/templates/architecture.md`](.claude/templates/architecture.md).

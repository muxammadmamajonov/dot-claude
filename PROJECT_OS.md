# PROJECT_OS — The `.claude` AI Project Operating System

> The deep architecture and operating reference for the `.claude/` system. It explains *why* the pieces exist, *how* they connect, and *how the OS operates Claude Code itself*. For a fast orientation read `README.md` and `START_HERE.md`; for the law read `.claude/CLAUDE.md`. This file is the layer beneath those — the architecture and the runtime.

The OS has two orthogonal concerns, and this document covers both:

1. **Project delivery** — the 9-stage flow that takes any software project from idea to launch, driven by the orchestrator and a minimal active team. Covered in §1–§3.
2. **Operating capabilities** — the ten Claude Code runtime primitives (Terminal, Memory, Commands, Custom Commands, Skills, MCP, Subagents, Hooks, Headless, Routines) the OS uses to *do* that delivery, all governed by one safety spine. Covered in §4 (one named section each) and §5.

A directory map (§6) and the safety model (§7) close the document.

---

## 1. Architecture overview

### 1.1 The mental model: an OS for projects

`.claude/` maps cleanly onto a real operating system:

| OS concept | `.claude` equivalent | Role |
|---|---|---|
| Constitution / BIOS | `.claude/CLAUDE.md` | Immutable law every process obeys: the flow, safety §8, tone, destructive-action limits. |
| Kernel scheduler | `.claude/agents/core/orchestrator.md` | Decides what runs next, in what order, and who does it. |
| System calls | `.claude/commands/*.md` | The sanctioned entry points a human invokes (`/start-project`, `/implement-feature`, `/audit-security`…). |
| Processes / drivers | `.claude/agents/**` | Specialist roles, each with one responsibility and a defined contract. |
| Shared libraries | `.claude/skills/**` | Reusable procedures any agent can call (interview, threat-model, write tests). |
| Device profiles | `.claude/presets/*.md` | Per-project-type defaults that configure the rest of the system. |
| Lookup tables | `.claude/stack-matrix/*.md` | Decision data: which technology fits which constraints. |
| Integrity checks | `.claude/checklists/*.md` | Severity-tagged gates (P0/P1/P2/P3) that must pass before promotion. |
| File formats | `.claude/templates/*.md` | Canonical shapes for the artifacts the system writes. |
| Permissions / guards | `.claude/settings.json` (always-on) + `.claude/hooks/*` (opt-in) | `settings.json` deny/ask lists are the always-on rails; hooks tighten enforcement when copied in. |
| Operating manuals | `.claude/docs/*.md` | Six portable guides for the runtime capabilities (§4). |

The **kernel** is `.claude/CLAUDE.md` — a short constitution that never changes per-run. The **orchestrator** is the scheduler that reads that constitution plus the active **preset** and routes work through replaceable subsystems.

```
                       ┌───────────────────────────────────────────────┐
                       │        .claude/CLAUDE.md  (kernel/constitution) │
                       │  9-stage flow • safety • tone • destructive ban │
                       └───────────────────────┬───────────────────────┘
                                               │ governs
                       ┌───────────────────────▼───────────────────────┐
   human ─/command/──► │      orchestrator.md  (scheduler/router)        │
                       └─┬───────┬────────┬────────┬────────┬─────────┬─┘
                         │       │        │        │        │         │
                  ┌──────▼─┐ ┌───▼───┐ ┌──▼───┐ ┌──▼────┐ ┌─▼─────┐ ┌─▼──────┐
                  │ agents │ │skills │ │preset│ │stack- │ │check- │ │templates│
                  │        │ │       │ │      │ │matrix │ │lists  │ │        │
                  └────────┘ └───────┘ └──────┘ └───────┘ └───────┘ └────────┘
                         ▲                                        ▲
                         └──────── hooks + settings.json ─────────┘
                                  (mechanical safety & automation)
```

**Core invariant:** the system never jumps straight to coding. It always runs *classify → interview → select → spec → build (small phases) → audit → readiness → launch → continue*. Coding is stage 5; understanding comes first. Every transition is a checklist gate.

### 1.2 The 9-stage flow

Every project moves through nine stages in order. Each stage has an owner and a gate that must pass before the next begins.

| # | Stage | What happens | Owner |
|---|---|---|---|
| 1 | **Classify** | Detect project type, platform(s), scale, risk class, compliance needs; pick the preset. | `orchestrator` + `/classify-project` |
| 2 | **Interview** | Ask the founder only business-critical questions (goals, users, constraints, budget, timeline). | `business-analyst` + `/interview-founder` |
| 3 | **Select** | `/route` assembles the **minimal active team** — only the agents/skills/checklists the matched preset + detected concerns require. | `orchestrator` + `/route` |
| 4 | **Spec** | Write specs before code: vision, scope, architecture, data model, interface contracts, milestones. | `solution-architect` + `/create-specs` |
| 5 | **Build** | Implement in small, independently revertible phases — one coherent slice at a time. | `technical-lead` + `engineering/*` |
| 6 | **Audit** | Run the non-optional gates: security, QA, performance, accessibility. | `quality/*` + `/audit-*` |
| 7 | **Readiness** | Verify observability, backups, rollback, runbooks, scaling, cost, legal/compliance. | `production-readiness-auditor` + `/audit-production` |
| 8 | **Launch** | Staged rollout, monitoring, go/no-go, comms. | `release` + `/prepare-launch` |
| 9 | **Continue** | Triage feedback, plan the next slice, re-enter the flow at the right stage. | `orchestrator` + `/continue-work` |

**Gate rule:** a stage may not advance while its gate is red. If the user pushes to skip a gate, the OS proceeds only with explicit acknowledgment and records the skipped gate as a risk via `.claude/templates/decision-record.md`. Stages 5–6 form the inner loop: build a phase, audit it, build the next — the roadmap is never built in one shot.

A project may legitimately start mid-flow (an existing codebase joins at stage 4 or 6). When it does, the OS runs the earlier stages in "reconstruct" mode: infer classification and write the missing specs before continuing.

### 1.3 The orchestrator as conductor

The orchestrator (`.claude/agents/core/orchestrator.md`) does not do the deep work itself; it routes, sequences, and enforces. Its loop is **understand → load → delegate → verify → record → advance (or stop)**:

1. **Locate the project in the flow.** New project → stage 1. Existing work → infer the current stage from the specs and code present.
2. **Load the right context.** Read the preset, then pull in only the agents, skills, stack-matrix slices, checklists, and templates that preset selects. Load what the stage needs, not everything.
3. **Delegate to the stage owner.** Hand the task to the agent that owns the current stage.
4. **Enforce the gate.** Run the gate's checklist before advancing. Red gate → stop, report, fix or record the risk. Never silently skip.
5. **Decompose build work.** Split stage 5 into the smallest coherent, independently revertible phases; verify after each.
6. **Keep the user in the loop on business decisions only.** Surface business-critical forks; make and document safe technical choices.
7. **Maintain the paper trail.** Every assumption lands in the assumptions log; every significant decision in a decision record.

Agents do **not** call each other directly. They return to the orchestrator, which decides the next hop. This keeps routing centralized, gated between every transition, and auditable.

### 1.4 The "minimal active team" selection

Stage 3 (`/route`) is where the OS earns its universality. Rather than loading all 116 agents and 65 skills, it activates only what the project needs and leaves everything else **dormant**:

```
classify ──► match preset ──► activate ONLY relevant agents/skills/checklists ──► dormant: everything else
                                  │
                                  └─ written to docs/state/active-team.md  (backed by .claude/orchestration/routing-matrix.md)
```

Selection is a function of three inputs:

1. **The active preset** — supplies the default agent roster, skill bias, relevant stack-matrix slices, and which checklist items are P0 for this project type.
2. **The current stage** — determines the *family* of agent needed (core for the spine, engineering for build, quality for audit).
3. **Cross-cutting concerns detected in the spec** — elevate or add agents regardless of preset:
   - Handles money / PII / regulated data → activate `privacy-compliance-auditor`, raise `security` and audit-logging items to P0.
   - Real-time / collaborative → add the realtime/consistency skills and concurrency review.
   - Public-facing UI → activate `accessibility-auditor` and the a11y checklist as a launch gate.
   - High scale / low latency → activate `performance-engineer` early, not just at audit.
   - Multi-tenant → require tenant-isolation review as a P0 security item.

The result: the same spine produces a lightweight path for a CLI tool and a heavyweight, compliance-laden path for a fintech platform. The selected team is written to `docs/state/active-team.md` so a fresh session can rehydrate exactly which roles are live.

---

## 2. The delivery layers in depth

### 2.1 Commands — entry points (`.claude/commands/`, 30)
The *system calls*: the named surface a human uses to drive the OS. They carry no project logic — they declare intent, gather minimum inputs, and hand to the orchestrator. Design rule: a command is **safe to run twice** — re-running `/audit-security` re-checks; re-running `/implement-feature` resumes rather than duplicating. The delivery commands span the whole flow (`/start-project`, `/classify-project`, `/interview-founder`, `/route`, `/create-specs`, `/select-stack`, `/design-architecture`, `/design-data-model`, `/design-ui-ux`, `/create-roadmap`, `/build-prototype`, `/implement-feature`, `/review-feature`, `/create-tests`, `/fix-bugs`, `/refactor-safely`, `/audit-security`, `/audit-performance`, `/audit-production`, `/threat-model`, `/plan-scale`, `/prepare-launch`, `/continue-work`), plus integrity (`/self-test`) and the operating-capability commands covered in §4.

### 2.2 Agents — specialist roles (`.claude/agents/`, 116 across six families)
Processes with a single responsibility and a clear contract. Each agent file declares: **responsibility** (one sentence), **inputs** (artifacts it consumes), **method** (skills it invokes), **outputs** (template-shaped artifacts it writes), and **hand-off** (next agent + the gate that must pass first). The six families:

- **core/ (10)** — `orchestrator`, `business-analyst`, `product-manager`, `solution-architect`, `technical-lead`, `requirements-engineer`, `system-analyst`, `project-manager`, `documentation-writer`, `code-reviewer`. The spine of the flow.
- **engineering/ (18)** — frontend, backend, mobile, desktop, game, ai-ml, data, database-architect, api-architect, devops, cloud-architect, release, … The hands that build, one phase at a time.
- **quality/ (8)** — `security-auditor`, `qa-engineer`, `performance-engineer`, `accessibility-auditor`, `reliability-engineer`, `privacy-compliance-auditor`, `production-readiness-auditor`, `test-automation-engineer`. They gate; they do not build.
- **design/ (6)** — product, ui-ux, design-system, accessibility, … They shape experience where the project type calls for it.
- **domain/ (22)** — saas, fintech, ecommerce, healthtech, … specialists carrying cross-cutting business and regulatory concerns.
- **stack/ (52, across 7 sub-families: web, mobile, backend, game, database, cloud, ai)** — thin per-framework specialists the orchestrator instantiates only after stack selection.

### 2.3 Skills — reusable methods (`.claude/skills/`, 65)
Shared libraries: a documented *way to do a thing*, reusable across agents and project types. The directory is **flat** — one folder per skill, each holding a `SKILL.md` (e.g. `.claude/skills/security/SKILL.md`); there are no `process/`, `project-type/`, or `stack/` subfolders. They group by intent: process methods (`discovery`, `requirements-engineering`, `architecture`, `api-design`, `testing`, `security`, `performance`, `production-readiness`, `documentation`), project-type methods (`web`, `mobile`, `game`, `backend`, `cli`, …), and stack-specific methods (`react-next`, `postgres`, `docker-kubernetes`, …). Skills are the unit of reuse: when two agents need the same procedure, it lives in a skill, not duplicated in both.

### 2.4 Presets — project-type playbooks (`.claude/presets/`, 37)
The *device profile* selected by the classifier. A preset declares the default agents to activate and skip, the skills to bias toward, the relevant stack-matrix slices, the checklist items that are P0 for this type, and the template variants that apply. Presets are why the system stays universal without being generic: the spine is constant, the configuration changes per project type.

### 2.5 Stack-matrix — decision data (`.claude/stack-matrix/`, 20)
Lookup data, not prose opinion. Files such as `web.md`, `backend.md`, `database.md`, `mobile.md`, `cloud-devops.md`, `payments.md`, `realtime.md` present options scored against constraints (team skills, scale, latency, cost, compliance, time-to-market, operational burden). Selection agents read these tables, combine them with the preset's weights and the founder's answers, and emit a justified choice plus an ADR. Treating stack choice as *data + weights* makes decisions explainable and revisable.

### 2.6 Checklists — gates with P0/P1/P2/P3 (`.claude/checklists/`, 29)
Integrity checks that must pass before promotion. Items are severity-tagged: **P0** blocks (secrets in source, missing authz, no backups, irreversible data path with no migration plan); **P1** must fix before launch but may proceed in-phase; **P2** is hardening, tracked as debt; **P3** is post-launch backlog (tracked, never blocks shipping). Core gates include `security.md`, `qa.md`, `performance.md`, `accessibility.md`, `production.md`, and `launch.md`, alongside per-phase, per-type, and cross-cutting checklists. Gates are deterministic: a phase is "done" only when its required-severity items are satisfied, and that result is recorded.

### 2.7 Templates — artifacts (`.claude/templates/`, 29)
The canonical shape of everything the system writes: `product-spec`, `architecture` (with ADR sections), `data-model`, `api-spec`, `decision-record`, `assumptions-log`, `runbook`, `production-readiness`, `launch-checklist`, and more. Because outputs are template-shaped, any agent can reliably read another agent's output, and the human always knows where to look.

**Generated artifacts live in the project's own `docs/`, not in `.claude/`.** The `.claude/` tree stays reusable and project-agnostic so it can be copied to the next project unchanged. (Throughout this document, "`docs/`" means the *output* directory of a project built with the OS — its specs, decisions, and state — not a folder inside this template repo.)

---

## 3. Control flow: a request from `/start-project` to launch

```
/start-project
   │
   ▼
(1) CLASSIFY ───────────► classifier ──reads──► presets/*  (+ stack-matrix hints)
   │  output: project type, selected preset
   ▼
(2) INTERVIEW ──────────► business-analyst ──uses──► skills/discovery
   │  asks ONLY business-critical questions; records assumptions for the rest
   ▼
(3) SELECT (/route) ────► orchestrator ──reads──► orchestration/routing-matrix.md
   │  writes docs/state/active-team.md  (minimal active team; rest dormant)
   ▼
(4) SPEC ───────────────► solution-architect ──writes──► templates/product-spec, architecture, data-model, api-spec
   │  GATE: spec completeness (problem, users, scope, non-goals, constraints)
   ▼
(5) BUILD PHASE (loop) ─► technical-lead + engineering/* ──uses──► skills/*
   │  ONE phase at a time; GATE: code-review checklist (P0 must be clean)
   ▼
(6) AUDIT ──────────────► quality/* ──run──► checklists/{security,qa,performance,accessibility}.md
   │  GATE: all P0 closed; P1 triaged    (loop back to 5 until roadmap complete)
   ▼
(7) READINESS ──────────► production-readiness-auditor ──► checklists/production.md
   │  GATE: backups, monitoring, rollback, runbook, on-call, data privacy
   ▼
(8) LAUNCH ─────────────► release ──► templates/runbook.md  (release + rollback steps)
   ▼
(9) CONTINUE ───────────► /continue-work, next roadmap items, incident runbooks, iteration
```

Key properties: every arrow into a new stage crosses a gate (a checklist); a gate with an open P0 stops the flow and routes back; and assumptions are logged rather than guessed silently. The hand-off pattern is always `orchestrator → agent → (template-shaped artifact to docs/) → orchestrator → gate check → next agent or remediation`. Because agent A never calls agent B directly, the orchestrator can enforce the gate, swap specialists by preset, run independent agents in parallel, and keep one auditable trail.

---

## 4. The ten operating capabilities

The flow above governs *project delivery*. A second, orthogonal layer governs *how the OS operates Claude Code itself* — the runtime primitives every project shares. Canonical depth for each lives in `.claude/docs/`, so the operating model travels with the OS. The umbrella guide is `.claude/docs/CLAUDE_CODE_OPERATING_MODEL.md`; it explains how all ten fit together under one safety spine.

Each section below gives: **what it is**, **how this OS uses it**, its **safety posture**, and a **pointer** to the canonical doc and the relevant skills/commands.

### 4.1 Terminal
**What it is.** The shell — the runtime's hands. Reading files, running builds and tests, inspecting git, invoking CLIs.

**How this OS uses it.** Every build, audit, and verification step ultimately runs through the terminal: `engineering/*` agents run builds and tests, `quality/*` agents run scanners and checks, and `/self-test` runs `.claude/scripts/integrity-check.py` to validate the `.claude/` tree's own link integrity, frontmatter, and JSON.

**Safety posture.** This is where destructive actions are possible, so it is the most tightly governed surface. `settings.json` `permissions.deny` blocks `rm -rf`, force-push, `mkfs`, secret-file reads, and DB-drop commands outright; `permissions.ask` gates pushes, deploys, migrations, package installs, DB CLIs, and remote-exec behind explicit human approval. Read before write; least privilege; least blast radius.

**Pointer.** `.claude/docs/CLAUDE_CODE_OPERATING_MODEL.md`; skill `.claude/skills/terminal-operations/SKILL.md`; enforced by `.claude/settings.json` and the `dangerous-command-guard` / `package-install-guard` hooks.

### 4.2 Memory
**What it is.** What the OS remembers and where it lives. Claude Code has three memory tiers, and putting a fact in the wrong tier is the single most common cause of lost context and contradictory decisions. **This OS folds its memory strategy directly here** so the routing rules live in the architecture reference.

**The three tiers:**

| Tier | Lives in | Scope | Holds |
|---|---|---|---|
| **Project memory** | `CLAUDE.md` (this `.claude/CLAUDE.md` is the OS constitution; a project may add its own `CLAUDE.md`/`AGENTS.md`) | this repo | **Rules**: coding conventions, the 9-stage flow, stack choices, "always run `/self-test` before committing `.claude/`" |
| **Docs-as-long-term-memory** | the project's own `docs/` (output of a project built with the OS) | this project, durable & versioned | **Records**: specs, decision records (ADRs), the assumptions log, architecture history, known risks, runbooks, audit reports |
| **User / global memory** | `~/.claude/` (user CLAUDE.md, auto-memory) | the person, across all projects | **The person**: their role/preferences, "always ask before pushing", cross-project habits |

**Routing rules — where does a fact go?**
- True for everyone who works in this repo? → project memory (`CLAUDE.md`).
- A decision, assumption, risk, or design fact about *this* project? → the project's `docs/` (decision record, assumptions log, architecture doc) — the durable project brain.
- About the human (their preferences, cross-project habits)? → user/global memory.
- Only relevant to the current task and disposable? → don't persist it at all.

Rule of thumb: **CLAUDE.md is for *rules*, the project's `docs/` is for *records*, user memory is for *the person*.** Never write project run-state into the reusable `.claude/` tree — it pollutes the copy-to-next-project payload.

**Docs-as-memory: the canonical artifacts** (each from a template):
- **Assumptions log** — `docs/state/assumptions.md` (from `.claude/templates/assumptions-log.md`): every non-trivial decision made on the user's behalf, with alternatives, blast radius, and how to reverse it.
- **Decision records (ADRs)** — `docs/decisions/` (from `.claude/templates/decision-record.md`): architecture-shaping choices and *why*.
- **Architecture history** — `docs/architecture/` evolves; superseded designs stay in git history and are referenced by ADRs, so the *why-it-changed* is never lost.
- **Known risks** — tracked in the production-readiness and audit artifacts; P3 items are explicitly "tracked, never blocks."
- **Run-state** — `docs/state/project-type.md` (classification), `docs/state/project.md` (live phase/decisions), `docs/state/active-team.md` (selected agents), `docs/state/handoffs/` (agent-to-agent notes).

**The continuation workflow.** When a session resumes (or context is summarized), the OS rehydrates from the project's `docs/`, not from chat history: `/continue-work` reads `docs/state/project-type.md`, `docs/state/project.md`, `docs/state/assumptions.md`, the latest specs, and open decisions/risks; re-derives the current stage and active team; and surfaces open assumptions and unresolved business-critical questions before doing new work. Because the durable memory is on disk, a fresh session — or a teammate, or a headless CI run — picks up exactly where the last one stopped. This is why "document the why" is non-negotiable: the assumptions log and decision records *are* the project's memory.

**How this OS uses it.** The three tiers are wired into the flow: project rules in `CLAUDE.md`, every decision and assumption persisted to `docs/` at the moment it is made, and `/continue-work` as the rehydration path.

**Safety posture.** Persist the *why*, never secrets. Records are referenced, never re-litigated. Anti-patterns the OS forbids: decisions only in chat (volatile), project facts in user/global memory (leak and go stale), and volatile run-state in `CLAUDE.md`/`.claude/` (breaks portability).

**Pointer.** `.claude/docs/MEMORY_STRATEGY.md`; skill `.claude/skills/memory-management/SKILL.md`; command `/continue-work`; templates `assumptions-log.md` and `decision-record.md`.

### 4.3 Commands
**What it is.** The built-in command surface — the named, invokable entry points that map a human intent to a defined workflow (the OS's "system calls").

**How this OS uses it.** The 30 commands in `.claude/commands/` *are* the entry points to every stage of the 9-stage flow and to the operating-capability workflows. They contain no project logic; they declare intent and hand to the orchestrator. Each is designed to be safe to run twice.

**Safety posture.** Commands inherit the full safety spine — anything they trigger still passes through `settings.json` deny/ask gates and any active hooks. A command never bypasses a gate.

**Pointer.** `.claude/docs/CLAUDE_CODE_OPERATING_MODEL.md`; the whole of `.claude/commands/` (see §2.1).

### 4.4 Custom Commands
**What it is.** New, project- or user-authored slash commands that extend the surface without touching the universal spine.

**How this OS uses it.** Custom commands are the §5 extensibility model in action: add a markdown command file that declares intent and routes to the orchestrator or a specific agent/skill, then wire it into the presets that need it. The OS ships its own beyond the core flow — `/brainstorm-project` (shape an idea before stage 1), `/commit-ready`, `/create-github-issues`, `/setup-mcp`, `/headless-run`, `/manage-routines` — demonstrating the pattern.

**Safety posture.** A custom command must agree with the constitution; it cannot grant itself permissions. It runs under the same `settings.json` and hook enforcement as any built-in command. Keep each single-purpose and idempotent.

**Pointer.** `.claude/docs/CLAUDE_CODE_OPERATING_MODEL.md`; pattern mirrors any file in `.claude/commands/`; extensibility rules in §5.

### 4.5 Skills
**What it is.** Reusable, model-invoked procedures — a documented method the runtime can pull in when a task matches.

**How this OS uses it.** The 65 skills in `.claude/skills/` are the OS's shared libraries (§2.3): agents invoke them for interviewing, threat-modeling, data-modeling, testing, performance work, and more. The capability-specific skills — `terminal-operations`, `memory-management`, `mcp-integration`, `headless-automation`, `routine-authoring` — encode the *how* for the operating layer itself.

**Safety posture.** A skill is a method, not a permission. It describes *how* to do a thing; whether the thing is allowed is still decided by `settings.json` and the gates. Single-purpose by design — if a skill grows two jobs, split it.

**Pointer.** `.claude/docs/CLAUDE_CODE_OPERATING_MODEL.md`; the whole of `.claude/skills/`.

### 4.6 MCP
**What it is.** The Model Context Protocol — the standard way to give Claude Code external tools and data sources (databases, issue trackers, cloud APIs, design tools) via configured servers.

**How this OS uses it.** MCP is how the OS reaches outside the repo when a project genuinely needs it. `/setup-mcp` wires and scopes a server; the OS never assumes a server exists — it asks the user to configure it. Tool scope is kept minimal: grant only the tools a stage needs.

**Safety posture.** External integrations are the widest blast radius, so MCP is treated conservatively: never assume an MCP server is present; prefer read-only/review scopes; scope tools tightly; and route any write or irreversible MCP action through the same human-in-the-loop approval as a destructive terminal command. Reference credentials, never reveal them.

**Pointer.** `.claude/docs/MCP_STRATEGY.md`; skill `.claude/skills/mcp-integration/SKILL.md`; command `/setup-mcp`.

### 4.7 Subagents
**What it is.** Delegating a scoped sub-task to a separate agent context, including composing several in parallel.

**How this OS uses it.** This is the orchestrator's core mechanism (§1.3): it delegates each stage to the owning agent and can fan out independent work — e.g. running `security-auditor`, `qa-engineer`, and `performance-engineer` in parallel on the same diff during stage 6 — then collect results and enforce the gate. Subagents never call each other; they return to the orchestrator.

**Safety posture.** Centralized routing keeps every hand-off gated and auditable. A subagent operates under the same constitution and permission policy as the parent; parallelism never relaxes a gate. Each subagent's output is template-shaped so the orchestrator can verify it.

**Pointer.** `.claude/docs/SUBAGENT_ORCHESTRATION.md`; `.claude/agents/core/orchestrator.md`; `.claude/orchestration/routing-matrix.md`; commands `/route`, `/implement-feature`, `/audit-*`.

### 4.8 Hooks
**What it is.** Deterministic shell guards that fire on tool events (PreToolUse / PostToolUse), able to block an operation (exit 2) or automate a safe-and-tedious follow-up.

**How this OS uses it.** The 9 hooks in `.claude/hooks/` are **opt-in examples, off by default** — copy a hook's block into `settings.json` to activate it. They mechanically enforce the §7 policy: `dangerous-command-guard`, `package-install-guard`, `secret-scan`, `pre-commit-check`, `pre-deploy-check`, `post-edit-check`, `docs-sync-check`, and more. A PreToolUse hook can block a dangerous operation before it runs (e.g. `secret-scan` blocks a commit containing secrets); a PostToolUse hook can run formatters or append to a run log.

**Safety posture.** Safe by default: the example hooks only warn or block (via exit 2) — they never mutate, install, or expose secrets. When policy (words in `CLAUDE.md`) and enforcement (a hook) disagree, the stricter one wins and the discrepancy is flagged for a human. Hooks are the mechanical floor beneath the constitutional and procedural layers.

**Pointer.** `.claude/docs/HOOKS_SAFETY_MODEL.md`; the whole of `.claude/hooks/`; wired via `.claude/settings.json`.

### 4.9 Headless
**What it is.** Driving the OS non-interactively — in CI, a script, or a pipeline — with no human at the keyboard to answer prompts.

**How this OS uses it.** `/headless-run` runs the OS without an interactive session: classification, audits, integrity checks, and read/review reporting can all run in CI. Because the durable memory is on disk (§4.2), a headless run rehydrates state from the project's `docs/` exactly as an interactive session would.

**Safety posture.** **Read/review-only by default.** A headless run cannot answer a business-critical question or approve a gated action, so it must not perform writes or irreversible operations unless explicitly opted in *with a tested rollback path*. Anything that would normally prompt a human is, by default, a stop — not a silent yes.

**Pointer.** `.claude/docs/HEADLESS_AND_ROUTINES.md`; skill `.claude/skills/headless-automation/SKILL.md`; command `/headless-run`.

### 4.10 Routines
**What it is.** Scheduled or recurring automations — a saved task that runs on a cadence (e.g. a nightly audit or a weekly dependency check).

**How this OS uses it.** `/manage-routines` creates and tends scheduled agents. Routines are the recurring, unattended face of the headless capability: stand up a daily `/audit-security` or a periodic `/self-test`, and let it report.

**Safety posture.** Inherits the headless posture — **read/review-only by default**, since a routine runs unattended with no human to approve a gated action. Any routine that writes or deploys requires explicit opt-in plus a rollback path, and should fail closed (stop and report) rather than push through a gate.

**Pointer.** `.claude/docs/HEADLESS_AND_ROUTINES.md`; skill `.claude/skills/routine-authoring/SKILL.md`; command `/manage-routines`.

---

## 5. Orchestration workflow

This section ties the delivery flow (§1–§3) and the operating capabilities (§4) together into the single loop the orchestrator actually runs.

**The loop:** *understand → load → delegate → verify → record → advance (or stop)*.

1. **Understand.** A human invokes a **command** (§4.3) or **custom command** (§4.4). The orchestrator locates the project in the 9-stage flow — new project → stage 1; existing work → rehydrate from the project's `docs/` via the **memory** continuation workflow (§4.2).
2. **Load.** It reads the active preset and assembles the **minimal active team** (§1.4) — activating only the relevant agents, skills, checklists, and stack-matrix slices, leaving the rest dormant. It pulls in **skills** (§4.5) as methods and configures any needed **MCP** server (§4.6) with a tight scope.
3. **Delegate.** It hands the stage to the owning agent, fanning out independent work to **subagents** in parallel where safe (§4.7). All actual work happens through the **terminal** (§4.1) under the always-on permission policy.
4. **Verify.** Before advancing, it runs the stage's **checklist** gate. **Hooks** (§4.8) provide a mechanical floor — blocking a forbidden operation regardless of intent. A red P0 stops the flow and routes back to remediation.
5. **Record.** It persists the decision and any assumptions to the project's `docs/` (the durable memory of §4.2), so the next session, teammate, or **headless** run (§4.9) can pick up exactly where this one stopped.
6. **Advance or stop.** Green gate → advance to the next stage. Business-critical fork → ask the human. Red gate with no acknowledgment → stop. **Routines** (§4.10) run this same loop unattended on a schedule, in read/review-only mode by default.

The same spine produces a one-command lightweight path for a CLI tool and a multi-gate, compliance-laden path for a fintech platform — because the *configuration* (preset + active team + cross-cutting overrides) changes, never the sequence or the safety.

---

## 6. Directory map of `.claude/`

```
.claude/
├── CLAUDE.md                     # kernel: constitution, 9-stage flow, safety §8, tone
├── settings.json                 # always-on permissions (deny/ask), env, hook wiring
├── commands/                     # 30 entry points (/start-project, /route, /implement-feature, /audit-security, …)
├── docs/                         # 6 portable operating-capability guides:
│                                 #   CLAUDE_CODE_OPERATING_MODEL, MCP_STRATEGY, HEADLESS_AND_ROUTINES,
│                                 #   MEMORY_STRATEGY, SUBAGENT_ORCHESTRATION, HOOKS_SAFETY_MODEL
├── agents/                       # 116 agents across six families
│   ├── core/                     #   10 — orchestrator, business-analyst, solution-architect, technical-lead, …
│   ├── engineering/              #   18 — frontend, backend, mobile, desktop, game, ai-ml, data, devops, …
│   ├── quality/                  #    8 — security-auditor, qa-engineer, performance-engineer, accessibility-auditor, …
│   ├── design/                   #    6 — product, ui-ux, design-system, accessibility, …
│   ├── domain/                   #   22 — saas, fintech, ecommerce, healthtech, …
│   └── stack/                    #   52 — per-framework specialists in 7 sub-families: web, mobile, backend,
│                                 #        game, database, cloud, ai
├── skills/                       # 65 skills — FLAT: one folder per skill (<name>/SKILL.md), no subfolders
├── orchestration/               # routing-matrix.md — project-type → minimal active team
├── presets/                      # 37 playbooks, one per project type
├── stack-matrix/                 # 20 decision tables: web, backend, database, mobile, cloud-devops, payments, …
├── checklists/                   # 29 gates: security, qa, performance, accessibility, production, launch, … (P0/P1/P2/P3)
├── templates/                    # 29 artifacts: product-spec, architecture, decision-record, assumptions-log, runbook, …
├── hooks/                        # 9 opt-in example guards (off until copied into settings.json)
└── scripts/                      # integrity-check.py — run via /self-test
```

**In one sentence:** `CLAUDE.md` is the constitution, the orchestrator is the scheduler, commands are the entry points, agents are the processes, skills are the shared libraries, presets configure the machine per project type, the stack-matrix supplies decision data, checklists are the integrity gates, templates are the file formats, `.claude/docs/` documents the ten operating capabilities, and `settings.json` (with the opt-in hooks) is the permission system that makes the safety real.

---

## 7. Safety model

One spine runs through everything above. Its principles: **read before write; least privilege and least blast radius; never expose secrets (reference, never reveal); human-in-the-loop for anything irreversible; headless and routines are read/review-only by default (writes need explicit opt-in plus rollback); never assume an MCP server exists; document the why.**

Safety is enforced at three layers so a single failure cannot cause an irreversible action:

1. **Constitutional (`CLAUDE.md`).** The non-negotiables in words: the mandatory classify→…→continue flow, "never code first," destructive-action restraint, secret-handling rules, and ask-only-business-critical.
2. **Procedural (checklists + orchestrator gates).** Those rules encoded as **P0** items the flow cannot pass with open. Security, data-loss, and authz failures are P0 by default and become hard stops; the **Definition of Done** (specified, implemented, tested, secure, quality-checked, performant, accessible, documented, reversible, reviewed) is the universal completion gate.
3. **Mechanical (`settings.json` always-on; hooks opt-in).** `settings.json` deny/ask lists block or gate dangerous operations at execution time the moment `.claude/` is present — `deny` blocks `rm -rf`, force-push, secret reads, and DB drops; `ask` gates pushes, deploys, migrations, package installs, DB CLIs, and remote-exec. The 9 example hooks add further enforcement once copied in, and they only warn or block — never mutate, install, or expose secrets.

**Hard prohibitions** (require explicit, logged human approval — never autonomous): `rm -rf` and bulk irreversible deletes; `git push --force` / history rewrites on shared branches; dropping databases/tables or deleting/altering migrations; printing, logging, committing, or transmitting secrets or `.env` files; any irreversible production action (destructive deploy, data purge, DNS/billing change) without a rollback path.

**Default-safe behaviors:** proceed on documented assumptions, not silent guesses; prefer reversible, small-diff changes with a rollback step; treat money, PII, and regulated data as automatic P0 escalations (compliance review, audit logging, least-privilege). When policy (words) and enforcement (hooks) disagree, the stricter one wins and the discrepancy is flagged for a human.

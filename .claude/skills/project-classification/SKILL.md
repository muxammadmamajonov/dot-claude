---
name: project-classification
description: Classify a project into one or more project types, pick a matching preset, and surface cross-cutting concerns immediately after discovery and before stack selection or requirements. Activate when starting a new project, when the project's nature is ambiguous, or when someone asks "what kind of project is this" or "which preset should we use".
---

# Project Classification

## When to use
- Right after discovery (`.claude/skills/discovery/SKILL.md`) is confirmed and `docs/discovery.md` exists, before stack selection or requirements.
- When a project spans multiple types (e.g. mobile app + backend API + admin web) and you need to identify the primary type, its companions, and the integration boundaries between them.
- When an existing repo is inherited and its type must be inferred from code, docs, CI config, and package manifests — no discovery artifact exists yet.
- When a project's scope changes substantially (new platform, new market, new compliance regime) and the original classification may no longer fit.
- When someone asks "which preset should we load?" or "what checklists apply here?" — answer via classification first.

## Workflow

### 1. Read the discovery artifact and extract the classification signals
Open `docs/discovery.md`. Extract:

- **Who uses it** — human end-users, developers/API consumers, automated systems, internal operators, or a mix. What surfaces do they interact on?
- **What it must do** — the core value proposition and primary actions, not the full feature list.
- **Data sensitivity** — personal data (PII/PHI/financial), proprietary data, public data, or none. This governs compliance overlays.
- **Scale signals** — expected user count, transaction volume, data volume, geographic spread.
- **Constraints** — hard technical constraints (must run offline, must embed in a hardware device, must integrate with SAP, must run in a browser extension, etc.).
- **Team and timeline** — size, skills, deadline pressure. Relevant for feasibility of exotic types (e.g. "embedded firmware" requires C/C++/Rust skills).

If `docs/discovery.md` does not exist (inherited codebase), infer from: `package.json` / `Cargo.toml` / `pyproject.toml`, CI configuration, Dockerfile, existing README, folder structure, and any existing specs. Write down what you inferred and mark each item as `INFERRED:` so it can be corrected.

**Mechanical first pass (bundled script).** Run `python3 .claude/skills/project-classification/scripts/detect_stack.py <repo>` (add `--json` for machine-readable output). It scans manifests (`package.json` and its deps, `Cargo.toml`, `go.mod`, `pyproject.toml`/`requirements.txt`, `*.csproj`, `Gemfile`, `composer.json`, `pubspec.yaml`, `hardhat.config.*`/`foundry.toml`, `*.uproject`, `project.godot`, Unity `Assets/`+`ProjectSettings/`, `platformio.ini`, `Dockerfile`, `*.tf`, …) and prints detected languages, frameworks, and candidate presets with the evidence behind each. Treat its output as **evidence to confirm**, never the final answer — you still set the risk tier, domain overlays, and cross-cutting concerns in the steps below. Verifiable behaviour is pinned by `evals/evals.json` next to the script.

### 2. Pick exactly one primary type
The primary type is the surface where the core value is delivered. Choose one:

| Primary type | Core signal |
|---|---|
| **Web app** (SPA/SSR/MPA) | Browser is the primary UI; users navigate to a URL |
| **Static site / marketing** | Primarily content, minimal interactivity, pre-rendered or CMS-driven |
| **Backend API / service** | No end-user UI; consumed by other systems or frontends via HTTP/gRPC/GraphQL |
| **Mobile app** | iOS and/or Android native or cross-platform; distributed via app stores |
| **Desktop app** | Installed on macOS/Windows/Linux; uses native windowing; may work offline |
| **CLI / developer tool** | Run in a terminal; consumed by developers or automation pipelines |
| **Game** | Real-time interactive entertainment; loop-driven; 2D, 3D, or multiplayer |
| **Browser extension** | Runs inside the browser as an extension; modifies or augments web pages |
| **AI agent / LLM system** | Orchestrates one or more LLMs with tools, memory, and multi-step reasoning |
| **Data platform / analytics / ETL** | Ingests, transforms, stores, and exposes data; users are analysts or downstream systems |
| **IoT / embedded / firmware** | Runs on constrained hardware; may have no display; real-time or near-real-time |
| **Blockchain / smart contract** | Core logic runs on-chain; assets and trust are cryptographically enforced |
| **Library / SDK** | Consumed as a dependency by other developers; API design and compatibility are the product |

**Decision point — ambiguous primary type:** If two types seem equally valid (e.g. a product that is simultaneously a web app and a data platform), choose the one where the end user's primary value is delivered. The other becomes a companion type. If genuinely inseparable, pick the one that drives the harder technical constraints (usually the one with stricter latency, compliance, or device requirements) and make the other the companion.

Do not default to "web app" because it is the most common. An IoT fleet management dashboard is a web app in its UI layer but an IoT project in its domain, compliance, and backend architecture. The domain drives the harder problems.

### 3. Add companion types and define their boundaries
Most real projects are composites. After picking the primary, list every other significant technical component:

```
Primary: mobile-app (iOS + Android, React Native)
Companions:
  - backend-api (REST, Node/Fastify) — serves the mobile client; owns auth, business logic, persistence
  - admin-web (internal SPA) — operations team dashboard; read-heavy; shares backend API
  - data-platform (ETL + reporting) — nightly batch jobs; separate DB schema; feeds BI tool
```

For each companion, note:
- What data flows across the boundary (and in which direction)
- What the auth model is at the boundary
- Whether the companion is in scope for v1 or deferred

Companions that are deferred still get documented — they influence architecture decisions even if not built yet (e.g. an API that will eventually serve a mobile client must be designed with that in mind from day one).

### 4. Map business domain overlays
A domain overlay layers on top of the technical type and pulls in additional compliance, regulatory, and architectural requirements. A project can have multiple overlays.

| Overlay | What it implies |
|---|---|
| **SaaS** | Multi-tenancy, subscription billing, tenant isolation, usage metering, trial/upgrade flows |
| **Ecommerce** | Product catalog, cart, checkout, inventory, order management, returns |
| **Marketplace** | Two-sided (buyer + seller), escrow/split payments, trust & safety, dispute resolution |
| **Fintech / payments** | PCI-DSS (if card data), money movement regulations, KYC/AML, audit trail, reconciliation |
| **Healthtech** | HIPAA (US) / GDPR Art. 9 (EU) for health data, BAAs, de-identification, consent management |
| **Edtech** | FERPA / COPPA (if minors), learning records, LRS/xAPI, accessibility (WCAG) |
| **CRM / ERP** | Complex data model, workflow automation, integrations with existing enterprise systems |
| **Helpdesk / support** | Ticket lifecycle, SLA tracking, escalation, agent routing, knowledge base |
| **Social platform** | User-generated content, moderation, trust & safety, graph relationships, feeds |
| **Media / streaming** | Content delivery, DRM, transcoding, adaptive bitrate, rights management |
| **IoT fleet** | Device provisioning, OTA updates, telemetry ingestion, remote command, firmware versioning |
| **Gov / public sector** | Accessibility law (Section 508 / EN 301 549), data sovereignty, procurement rules |
| **Logistics / booking** | Scheduling, availability, reservations, conflict detection, geo-routing |
| **AI agent system** | Prompt injection risk, model output validation, human-in-the-loop gates, cost controls |
| **Blockchain** | Smart contract audit requirements, key management, gas cost modeling, bridge risks |

**Rule:** treat domain overlays seriously. A fintech overlay on a "simple web app" does not make it a simple web app — it makes it a regulated financial product with PCI-DSS, KYC, and audit-trail requirements that dominate the architecture. Never classify away an overlay because it feels inconvenient.

For each overlay that applies, write one line: `Overlay: fintech — trigger: the app moves real money between users (discovery §3).`

For each overlay that does NOT apply despite seeming relevant, write: `Not in scope: healthtech — the app stores fitness goals but not medical records or diagnoses (discovery §4).`

### 5. Select a preset
Match the primary type + domain overlays to a preset in `.claude/presets/`. The preset pre-loads the likely checklists, stack-matrix entries, templates, and agent roster for this project type:

- `.claude/presets/web-app.md`, `.claude/presets/mobile-app.md`, `.claude/presets/desktop-app.md`
- `.claude/presets/backend-api.md`, `.claude/presets/cli-tool.md`, `.claude/presets/browser-extension.md`
- `.claude/presets/game-2d.md`, `.claude/presets/game-3d.md`, `.claude/presets/multiplayer-game.md`
- `.claude/presets/ai-agent-system.md`, `.claude/presets/data-platform.md`, `.claude/presets/automation-tool.md`
- `.claude/presets/iot-embedded.md`, `.claude/presets/blockchain-app.md`
- `.claude/presets/saas.md`, `.claude/presets/ecommerce.md`, `.claude/presets/marketplace.md`
- `.claude/presets/fintech.md`, `.claude/presets/crm.md`, `.claude/presets/erp.md`
- `.claude/presets/helpdesk.md`, `.claude/presets/social-platform.md`, `.claude/presets/media-streaming.md`
- `.claude/presets/healthtech.md`, `.claude/presets/edtech.md`, `.claude/presets/logistics.md`, `.claude/presets/booking.md`
- `.claude/presets/static-site.md`, `.claude/presets/internal-tool.md`, `.claude/presets/devtool-library.md`
- `.claude/presets/api-integration.md`, `.claude/presets/custom-project.md`

When the primary type maps cleanly to a preset, use it. When the project is a composite (e.g. SaaS + marketplace), use the preset for the primary type and annotate the deltas from the companion overlays: "Using `saas.md` preset; additionally load `.claude/checklists/security.md` escrow and dispute-resolution sections from marketplace overlay."

When no preset fits, use `custom-project.md` and document exactly what the custom blend is. Do not silently ignore the deltas between the chosen preset and the actual project — they are where the hardest problems live.

### 6. Detect and catalog cross-cutting concerns
Walk every cross-cutting concern below. For each one, decide: **in scope**, **out of scope (reason)**, or **deferred (version)**. Justify every in-scope flag with one line from discovery.

| Concern | In scope? | Trigger from discovery |
|---------|-----------|------------------------|
| Authentication (human users) | | |
| Authorization (roles, permissions, ownership) | | |
| API authentication (machine-to-machine) | | |
| Secrets management (env vars, vaults, rotation) | | |
| Personal data / privacy (PII, PII-adjacent) | | |
| Payments / PCI | | |
| Health data / HIPAA or GDPR Art. 9 | | |
| Audit logging (immutable, tamper-evident) | | |
| Observability (structured logs, metrics, traces, alerts) | | |
| Internationalization / localization | | |
| Accessibility (UI, CLI output, docs) | | |
| Offline / local-first / sync | | |
| Real-time / push updates | | |
| Multi-tenancy (data and compute isolation) | | |
| Rate limiting / abuse prevention / bot defense | | |
| Backups / disaster recovery (RTO/RPO defined) | | |
| Scalability targets (peak load defined) | | |
| Content moderation / trust & safety | | |
| DRM / content protection | | |
| Firmware / OTA updates | | |
| Smart contract auditability | | |

Do not silently omit a concern. If multi-tenancy is not needed, write it as `out of scope — single-tenant product, no shared infrastructure between customers (discovery §2)`. This prevents it from being retrofitted later without deliberate thought.

**Concerns to never skip without explicit justification:** authentication, secrets management, personal data / privacy, observability, backups/DR. These apply to virtually every production system.

### 7. Record the classification artifact
Write `docs/classification.md` using `.claude/templates/project-brief.md`:

```
Primary type: <type>
Companions: <list with boundaries>
Domain overlays: <list with triggers>
Preset: .claude/presets/<chosen>.md
Preset deltas: <what the preset does not cover for this project>
Cross-cutting concerns: <table from step 6>
Rationale: <short paragraph explaining the primary type choice and any non-obvious decisions>
Inferred items (for inherited codebases): <list of inferences and confidence level>
```

### 8. Hand off
Pass `docs/classification.md` to:
- `.claude/skills/stack-selection/SKILL.md` — reads primary type, companions, overlays, and cross-cutting concerns to set hard constraints for stack filtering.
- `.claude/skills/requirements-engineering/SKILL.md` — reads cross-cutting concerns to derive the NFR table; reads overlays to know which compliance categories apply.
- `.claude/skills/architecture/SKILL.md` — reads type + companions + multi-tenancy/real-time/offline concerns to inform structural decisions.

## Standards

- **Do** name exactly one primary type. Ambiguity here cascades into every downstream decision: stack, architecture, checklists, agent roster. If you cannot name one, you have not understood the project yet — re-read discovery.
- **Do** justify each domain overlay with a one-line trigger from discovery. Overlays without a trigger are guesses and introduce unearned complexity.
- **Do** prefer a preset over hand-rolling. Presets encode hard-won defaults accumulated from many project patterns. Deviating from a preset requires documenting why.
- **Do** document companions even when they are deferred. Architecture for v1 must accommodate what v2 will add.
- **Do** explicitly mark out-of-scope concerns rather than omitting them. The difference between "we thought about multi-tenancy and decided we don't need it" and "we never thought about multi-tenancy" matters enormously when it is raised in a security audit.
- **Do not** force a project into a single type when it is genuinely a composite — model the boundaries instead. The boundary is where the hardest integration and security problems live.
- **Do not** silently drop a cross-cutting concern. Mark it `out of scope (reason)` or `deferred (version)` explicitly.
- **Do not** choose a stack here. Classification is technology-agnostic. The temptation to say "it's a React app" belongs in stack selection, not classification.
- **Do not** classify from the founder's wished-for future product. Classify the v1 they are actually building, with notes on what the future version adds.
- **Do not** treat domain overlays as cosmetic. A fintech or healthtech overlay fundamentally changes the compliance story, the architecture story, and the risk profile of the project.

## Common mistakes to avoid

- **Defaulting everything to "web app."** IoT, CLI, game, AI agent, and data pipeline projects have radically different default checklists, stacks, and agent rosters. A fleet-management backend classified as "web app" will miss device provisioning, OTA update, telemetry ingestion, and firmware signing requirements entirely.
- **Treating domain overlays as optional annotations.** When a project handles payments, it is a fintech project in the eyes of regulators regardless of how it is labeled. PCI-DSS does not care what preset you chose.
- **Missing multi-tenancy early.** Adding multi-tenant data isolation to a schema designed for single-tenant is a large, risky, expensive migration. Decide at classification time, not mid-build.
- **Missing audit-log requirements early.** Audit logs must be append-only and tamper-evident from day one. Retrofitting immutability into a system that uses a mutable `updated_at` column is painful.
- **Classifying from v3 of the product instead of v1.** A solo founder describing their 10-year vision should be classified at the scope of what they will build in the next 90 days. Record the future vision as notes, not requirements.
- **Picking a preset and ignoring the deltas.** The deltas are where the real project diverges from the template — and they are almost always where the hardest problems are. Document them explicitly and address them in requirements.
- **Conflating type with platform.** "React Native app" is a platform + framework choice, not a project type. The project type is "mobile app." Classification is technology-agnostic.
- **Listing the same agent twice.** Each agent role appears once in `docs/classification.md`. Duplicate entries suggest confusion about roles.

## Output format

A completed `.claude/templates/project-brief.md` saved at `docs/classification.md` containing:

1. **Primary type** — one of the named types from step 2, with a one-sentence rationale.
2. **Companion types** — list with integration boundaries (data flow, auth model, build scope).
3. **Domain overlays** — each with its trigger from discovery, or explicitly marked not in scope.
4. **Selected preset path** — `.claude/presets/<name>.md` with any deltas documented.
5. **Cross-cutting concerns table** — `concern | in scope? | trigger | priority`.
6. **Inferred items** — for inherited codebases, what was inferred vs. confirmed, with confidence.
7. **Rationale** — short paragraph covering any non-obvious classification decisions.

This artifact is the input contract for stack selection, requirements engineering, and architecture. It must be finalized and agreed before those stages begin.

## Related checklists
- `.claude/checklists/discovery.md`
- `.claude/checklists/requirements.md`
- `.claude/checklists/security.md`
- `.claude/checklists/accessibility.md`
- `.claude/checklists/production.md`

## Related agents
- `.claude/agents/core/orchestrator.md`
- `.claude/agents/core/business-analyst.md`
- `.claude/agents/core/solution-architect.md`
- `.claude/agents/core/system-analyst.md`

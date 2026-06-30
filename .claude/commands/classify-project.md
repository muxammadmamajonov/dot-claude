---
description: Classify the project type, map to a preset, detect cross-cutting concerns
argument-hint: [project idea or description]
---

# /classify-project

## Purpose
Analyse the user's idea (or the existing codebase if one is present) and output a structured classification: primary project type, secondary types, the matching preset, and a list of cross-cutting concerns that must be handled across all phases (payments, realtime, AI/ML, compliance, offline, multi-tenancy, etc.).

## When to use
- As Phase 1 of `/start-project`.
- Standalone when taking over an existing project and need to orient the system.
- When the project scope changes significantly and the preset must be re-evaluated.

## Workflow

### Step 1 — Gather input
1. If an argument was passed to the command, use it as the idea description.
2. If no argument, ask: "Describe the project in 2–5 sentences. What does it do, who uses it, and on what platforms does it run?"
3. If a codebase is present in the working directory, run a lightweight scan:
   - Check for `package.json`, `Cargo.toml`, `go.mod`, `pyproject.toml`, `Podfile`, `build.gradle`, `CMakeLists.txt`, `*.sol`, `Makefile` to detect language/runtime.
   - Check for framework markers: `next.config.*`, `angular.json`, `flutter/`, `hardhat.config.*`, `serverless.yml`, `docker-compose.*`, `k8s/`, `.github/workflows/`.
   - Record findings as raw signals; do not yet make a classification decision.

### Step 2 — Map to primary type
4. Score the input against the type table below. Choose the **single highest-scoring primary type**. If two types score equally, pick the one closer to the user-facing surface.

| Code | Primary Type | Key signals |
|------|-------------|-------------|
| WEB | Web application | Browser UI, HTML/CSS/JS framework, SPA, SSR, PWA |
| MOB | Mobile app | iOS, Android, React Native, Flutter, Expo, Capacitor |
| DSK | Desktop app | Electron, Tauri, Qt, .NET MAUI, SwiftUI/AppKit, WPF |
| API | Backend / API service | REST, GraphQL, gRPC, no primary UI, consumed by clients |
| CLI | CLI tool | Terminal interface, arg parsing, stdin/stdout pipeline |
| EXT | Browser extension | manifest.json, content scripts, background service worker |
| AGT | AI agent / LLM system | LLM calls, tool use, RAG, agentic loops, prompt chains |
| DAT | Data platform | ETL, pipelines, warehouses, dashboards, notebooks |
| IOT | IoT / embedded | Firmware, RTOS, sensors, edge hardware, microcontrollers |
| BLK | Blockchain / Web3 | Smart contracts, wallets, on-chain logic, DeFi, NFT |
| SAS | SaaS platform | Multi-tenant, subscription billing, tenant isolation |
| ECO | E-commerce | Cart, checkout, catalogue, fulfilment, marketplace |
| FIN | Fintech | Payments, ledger, trading, lending, compliance-heavy |
| CRM | CRM / ERP | Contact management, deal pipeline, resource planning |
| HLP | Helpdesk / Support | Tickets, queues, SLA, knowledge base, chat |
| SOC | Social / Media | Feeds, follows, content moderation, media upload |
| GAM | Game | Game loop, physics, multiplayer, assets, leaderboard |
| EMB | Embedded / firmware | Bare-metal, RTOS, HAL, limited RAM/flash |

5. List up to **three secondary types** that also apply (e.g., a SaaS platform might have secondary types: API, DAT).

### Step 3 — Detect cross-cutting concerns
6. Scan the idea and signals for each concern below. Mark each as **Present**, **Likely**, or **Absent**.

| Concern | Detection signals |
|---------|------------------|
| Payments / billing | Stripe, pricing tiers, invoices, subscriptions, checkout |
| Realtime / live data | WebSockets, SSE, CRDT, live collaboration, presence |
| AI / ML | LLM, embeddings, model inference, vector DB, fine-tuning |
| Compliance (GDPR / HIPAA / PCI / SOC2 / ISO27001) | Health data, financial data, EU users, card data |
| Offline / sync | PWA offline, local-first, sync engine, conflict resolution |
| Multi-tenancy | Tenant isolation, per-tenant config, tenant-scoped data |
| Internationalisation | Multiple locales, RTL, translated content |
| Authentication / identity | SSO, OAuth, MFA, passwordless, social login |
| File / media | Upload, storage, CDN, transcoding, image processing |
| Search | Full-text, vector, faceted, Elasticsearch/Typesense/Algolia |
| Third-party integrations | Webhooks, OAuth apps, partner APIs |
| Hardware / device access | Camera, GPS, Bluetooth, serial, USB |
| High availability / DR | Multi-region, failover, RTO/RPO requirements |

### Step 4 — Select preset
7. Map primary type to a preset configuration file from `.claude/presets/`. Presets contain opinionated defaults for language, framework, test runner, CI, and infra. Example mapping:

| Primary type | Default preset path |
|-------------|---------------------|
| WEB | `.claude/presets/web-app.md` |
| MOB | `.claude/presets/mobile-app.md` |
| API | `.claude/presets/backend-api.md` |
| AGT | `.claude/presets/ai-agent-system.md` |
| BLK | `.claude/presets/blockchain-app.md` |
| (others) | `.claude/presets/custom-project.md` |

8. Note any cross-cutting concerns that override preset defaults (e.g., HIPAA compliance forces encryption-at-rest regardless of preset).

### Step 5 — Write output
9. Write `docs/state/project-type.md` using the template at `.claude/templates/project-brief.md`.
   - Include: primary type, secondary types, preset path, all cross-cutting concern statuses, override notes.
   - This is the canonical classification record (CLAUDE.md §3 state convention). `/route`, `/threat-model`, and `/plan-scale` read it from this exact path.
10. Print a summary table to the terminal for human review.

## Agents used
None — this command runs inline without spawning sub-agents.

## Skills used
None at this phase. Security and compliance signals are flagged here but handled by `.claude/skills/security/SKILL.md` in later phases.

## Expected outputs
| Path | Description |
|------|-------------|
| `docs/state/project-type.md` | Structured classification record (canonical; read by /route, /threat-model, /plan-scale) |

## Stop conditions
- The user's description is fewer than two sentences and no codebase signals exist — ask for more detail before classifying.
- The idea spans more than three primary types with equal weight — present the ambiguity to the user and ask which surface to optimise for first.
- A compliance concern (HIPAA, PCI, financial regulation) is detected — flag it prominently and note that legal review is required before data model design.

## Final report format
```
## /classify-project — Result

**Primary type:** <code> — <full name>
**Secondary types:** <list or "none">
**Preset:** <path>

**Cross-cutting concerns:**
| Concern | Status |
|---------|--------|
| ...     | Present / Likely / Absent |

**Override notes:** <any preset defaults that must change due to concerns>

**Next step:** /interview-founder
```

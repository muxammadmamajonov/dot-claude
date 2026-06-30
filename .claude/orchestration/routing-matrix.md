# Routing Matrix — classify → activate only what's relevant

This is the orchestrator's quick index for assembling a **minimal active team**. It does not replace the presets — each preset (`.claude/presets/<type>.md`) holds the authoritative, linked list of recommended agents/skills/checklists. This table is the fast lookup; the cross-cutting matrix in `.claude/agents/core/orchestrator.md` adds modules on top.

## How to use
1. Classify the project (`.claude/skills/project-classification/SKILL.md`) → primary type + risk tier.
2. Open the matching preset → take its *Recommended agents / skills / checklists* as the **base set**.
3. Apply the **cross-cutting matrix** (orchestrator) for each concern present (payments, realtime, queues, search, AI, regulated data, offline, high-scale, deps, cost, hardware).
4. Add **baseline gates** (see below).
5. Everything not selected stays **dormant** — do not invoke it.
6. Write the result to `docs/state/active-team.md` via `.claude/commands/route.md`.

## Baseline gates (every project)
`.claude/checklists/security.md`, `.claude/checklists/qa.md`, `.claude/checklists/production.md`, `.claude/checklists/launch.md`, `.claude/checklists/dependencies.md`.
Add `.claude/checklists/accessibility.md` for any human UI; `.claude/checklists/privacy-compliance.md` for any personal/financial/health data; `.claude/checklists/observability.md` and `.claude/checklists/cost.md` for any always-on service.

## Project type → core modules
Short names; full linked lists live in each preset. Primary stack-matrix in parentheses.

| Project type | Preset | Primary domain / stack agent | Core skills (besides baseline) | Type checklists |
|---|---|---|---|---|
| Web app | `web-app` | stack/web/* (web) | web, ui-ux-design, api-design | web, ui-ux, api |
| Mobile app | `mobile-app` | stack/mobile/* (mobile) | mobile, ui-ux-design | mobile, ui-ux, accessibility |
| Desktop app | `desktop-app` | engineering/desktop-engineer (desktop) | desktop | desktop |
| Game (2D/3D/MP) | `game-2d` / `game-3d` / `multiplayer-game` | engineering/game-engineer (game) | game, performance | game, performance |
| Backend / API | `backend-api` | engineering/backend-engineer (backend) | backend, api-design, data-modeling | backend, api, data-model |
| CLI tool | `cli-tool` | engineering/backend-engineer | cli | backend, qa |
| Browser extension | `browser-extension` | engineering/frontend-engineer | browser-extension, security | security, web |
| AI agent system | `ai-agent-system` | domain/ai-agent-domain-expert | ai-ml | ai-ml, security |
| Data platform | `data-platform` | engineering/data-engineer (data-platform) | data-platform, data-modeling, analytics | data-model, database |
| Automation tool | `automation-tool` | domain/automation-domain-expert | messaging-queues | backend, security |
| IoT / embedded | `iot-embedded` | domain/iot-domain-expert | iot-embedded, observability | backend, incident-response |
| Blockchain | `blockchain-app` | domain/blockchain-domain-expert | blockchain, security | security |
| SaaS | `saas` | domain/saas-domain-expert | payments, observability | security, privacy-compliance |
| Ecommerce | `ecommerce` | domain/ecommerce-domain-expert | payments, search | security, privacy-compliance |
| Marketplace | `marketplace` | domain/marketplace-domain-expert | payments, search | security, privacy-compliance |
| Fintech | `fintech` | domain/fintech-domain-expert | payments, security | security, privacy-compliance |
| Healthtech | `healthtech` | domain/healthtech-domain-expert | security | privacy-compliance, security |
| Edtech | `edtech` | domain/edtech-domain-expert | ui-ux-design | accessibility, privacy-compliance |
| Logistics | `logistics` | domain/logistics-domain-expert | realtime, observability | backend, observability |
| Media streaming | `media-streaming` | domain/media-streaming-domain-expert | performance, observability | performance, cost |
| Social platform | `social-platform` | domain/social-platform-domain-expert | search, realtime | privacy-compliance, security |
| Security tool | `security-tool` | domain/security-tooling-domain-expert | security, observability | security, dependencies |
| AR / VR | `ar-vr` | domain/ar-vr-domain-expert | performance | performance, accessibility |
| Robotics | `robotics` | domain/robotics-domain-expert | observability | incident-response, release-rollback |
| Developer tool / SDK | `devtool-library` | domain/devtools-platform-domain-expert | documentation, api-design | dependencies, release-rollback |
| Internal tool / admin | `internal-tool` | engineering/fullstack-engineer | web, security | security, privacy-compliance |
| Static / marketing site | `static-site` | engineering/frontend-engineer | web | web, accessibility |
| API integration | `api-integration` | engineering/integration-engineer | messaging-queues, api-design | backend, dependencies |

## Notes
- A project may map to **multiple** rows (e.g. a fintech mobile app). Union the modules, then de-duplicate.
- Risk tier raises the bar, never lowers it: a regulated or money-moving project always pulls in `privacy-compliance`, `security`, and a threat model (`.claude/commands/threat-model.md`).
- When no row fits, use `.claude/presets/custom-project.md` and compose from the cross-cutting matrix.

## Web projects → use the web routing layer
For any web app (web-app, static-site, SaaS, ecommerce, marketplace, internal-tool, and most API/full-stack work), load `.claude/orchestration/web-routing-matrix.md` — the elite-web-team map with operating modes (audit-only, fix-and-verify, production-hardening, ui-ux-polish, security-review, performance-review, release-readiness, documentation), task→specialist routing, and verification loops. Entry commands: `.claude/commands/web-audit.md` (scope+mode audit) and `.claude/commands/web-readiness.md` (ship gate against `.claude/checklists/web-production.md`). First step on any unfamiliar web repo: `.claude/agents/core/codebase-mapper.md`. New web specialists: `.claude/agents/engineering/playwright-e2e-engineer.md`, `.claude/agents/engineering/refactoring-specialist.md`, `.claude/agents/engineering/bug-fix-specialist.md`. For UI/visual polish, prefer the installed `frontend-design` skill (anthropics/skills).

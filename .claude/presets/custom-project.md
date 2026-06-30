# Custom Project Preset

## Project type

Catch-all preset for any project that does not map cleanly to an existing preset. Use this when the classifier (`.claude/agents/core/orchestrator.md`) determines the project is a novel combination of domains, a highly vertical/niche solution, an internal tool, a research spike, or a hybrid that spans multiple preset categories.

This preset does not prescribe a fixed stack or domain model. Instead it provides a structured composition method: you identify the relevant building blocks from across the system and assemble a tailored configuration for this specific project.

---

## Typical use cases

- Internal tooling with unusual domain logic (fleet management, scientific instrument control, supply-chain optimisation, agricultural management)
- Hybrid platforms that combine two or more preset types (e.g. marketplace + ERP back-office; social platform + streaming + creator economy)
- Research or innovation projects where the final form is not yet known
- Legacy modernisation: replacing a bespoke system with no standard category equivalent
- Vertical SaaS for a specialised industry (legal tech, construction management, veterinary practice software, real estate)
- Automation / workflow engine as the primary product (IFTTT-style, iPaaS, RPA tool)
- Data-intensive internal dashboards and operational control planes
- Any project where the founder's description does not fit neatly into web-app, mobile-app, game, CRM, ERP, helpdesk, social, media-streaming, marketplace, fintech, blockchain, IoT, AI-agent, data-platform, CLI, browser-extension, or desktop presets

---

## Required discovery questions

These questions replace the domain-specific questions in typed presets. They are deliberately broad — their purpose is to identify which typed building blocks apply.

1. **What is the primary value the system delivers, and who receives that value?** (the one-sentence job-to-be-done) — drives scope prioritisation and determines which domain agents to activate.
2. **What data does the system create, consume, or transform, and how sensitive is it?** (PII, financial records, health data, IP, operational telemetry) — determines compliance regime and security posture before any other decision.
3. **Who are the user roles, and what does each role need to do vs. see?** — every answer here is a module boundary and a permission boundary.
4. **What does "done" look like at the end of the MVP?** (what can a user do that they cannot do today) — defines the Definition of Done for the first build phase.
5. **What external systems must this project integrate with, and which integrations are contractually required at launch?** — each integration is a scope item with its own reliability and security surface.
6. **What is the expected load profile?** (user count, request rate, data volume, batch frequency) — sizes infrastructure and determines whether a simple monolith or a distributed design is appropriate.
7. **What compliance, regulatory, or contractual constraints exist?** (GDPR, HIPAA, SOC 2, ISO 27001, industry-specific regulation, customer security requirements) — must be identified before architecture is designed.
8. **Is there an existing system being replaced, and does data need to be migrated?** — migration is often the riskiest phase; identify it early.
9. **What is the deployment target?** (cloud, on-premises, edge, embedded, hybrid; single-tenant vs. multi-tenant) — the highest-impact infrastructure fork.
10. **What are the hard constraints on timeline, budget, and team size?** — sets the ceiling on MVP scope and determines whether build, buy, or integrate is the right call for each component.

---

## Recommended agents

Use the discovery answers to select a subset. The groupings below guide selection; not all groups are needed for every project.

### Core (always include all)
- `.claude/agents/core/orchestrator.md`
- `.claude/agents/core/solution-architect.md`
- `.claude/agents/core/requirements-engineer.md`
- `.claude/agents/core/business-analyst.md`
- `.claude/agents/core/product-manager.md`
- `.claude/agents/core/system-analyst.md`

### Engineering (select based on what the project needs to build)

| Need | Agent |
|---|---|
| Server-side logic, APIs, background jobs | `.claude/agents/engineering/backend-engineer.md` |
| Web UI | `.claude/agents/engineering/frontend-engineer.md` |
| Full-stack feature delivery | `.claude/agents/engineering/fullstack-engineer.md` |
| Database design and query performance | `.claude/agents/engineering/database-architect.md` |
| API contracts, versioning, gateway | `.claude/agents/engineering/api-architect.md` |
| Third-party system connectors | `.claude/agents/engineering/integration-engineer.md` |
| Real-time features (WebSocket, SSE, live data) | `.claude/agents/engineering/realtime-engineer.md` |
| Mobile apps (iOS / Android) | `.claude/agents/engineering/mobile-engineer.md` |
| Desktop application | `.claude/agents/engineering/desktop-engineer.md` |
| Search (full-text, faceted, semantic) | `.claude/agents/engineering/search-engineer.md` |
| Data pipelines, ETL, warehousing | `.claude/agents/engineering/data-engineer.md` |
| CI/CD, containers, infrastructure-as-code | `.claude/agents/engineering/devops-engineer.md` |
| Cloud architecture (VPC, IAM, scaling) | `.claude/agents/engineering/cloud-architect.md` |
| Payment processing | `.claude/agents/engineering/payments-engineer.md` |
| ML model integration or training pipeline | `.claude/agents/engineering/ai-ml-engineer.md` |
| Release management and deployment strategy | `.claude/agents/engineering/release-engineer.md` |

### Quality (always include security, qa, production-readiness; add others by risk)
- `.claude/agents/quality/security-auditor.md`
- `.claude/agents/quality/qa-engineer.md`
- `.claude/agents/quality/production-readiness-auditor.md`
- `.claude/agents/quality/performance-engineer.md` *(add if load or latency is a concern)*
- `.claude/agents/quality/privacy-compliance-auditor.md` *(add if PII or regulated data)*
- `.claude/agents/quality/reliability-engineer.md` *(add if uptime SLA is contractual)*
- `.claude/agents/quality/accessibility-auditor.md` *(add if there is any human-facing UI)*
- `.claude/agents/quality/test-automation-engineer.md`

### Design (add if human-facing UI exists)
- `.claude/agents/design/ui-ux-designer.md`
- `.claude/agents/design/product-designer.md`
- `.claude/agents/design/accessibility-designer.md`
- `.claude/agents/design/design-system-architect.md` *(for multi-surface or brand-sensitive UI)*
- `.claude/agents/design/mobile-ux-specialist.md` *(mobile)*

### Domain (select the closest match or combine multiple)
- `.claude/agents/domain/saas-domain-expert.md`
- `.claude/agents/domain/fintech-domain-expert.md`
- `.claude/agents/domain/marketplace-domain-expert.md`
- `.claude/agents/domain/ecommerce-domain-expert.md`
- `.claude/agents/domain/healthtech-domain-expert.md`
- `.claude/agents/domain/edtech-domain-expert.md`
- `.claude/agents/domain/logistics-domain-expert.md`
- `.claude/agents/domain/booking-domain-expert.md`
- `.claude/agents/domain/automation-domain-expert.md`
- `.claude/agents/domain/ai-agent-domain-expert.md`
- `.claude/agents/domain/blockchain-domain-expert.md`
- `.claude/agents/domain/iot-domain-expert.md`
- `.claude/agents/domain/gaming-domain-expert.md`
- `.claude/agents/domain/crm-domain-expert.md`
- `.claude/agents/domain/erp-domain-expert.md`
- `.claude/agents/domain/helpdesk-domain-expert.md`
- `.claude/agents/domain/social-platform-domain-expert.md`
- `.claude/agents/domain/media-streaming-domain-expert.md`

### Stack (select based on team expertise and non-functional requirements)
- See `.claude/stack-matrix/` for backend, frontend, mobile, data, infra, and security options

---

## Recommended skills

Select skills that match the work this project actually requires. Do not load all skills — load only those relevant to the current stage.

| Work type | Skill |
|---|---|
| Data model design | `.claude/skills/data-modeling/SKILL.md` |
| API design | `.claude/skills/api-design/SKILL.md` |
| Security posture | `.claude/skills/security/SKILL.md` |
| Backend implementation | `.claude/skills/backend/SKILL.md` |
| PostgreSQL | `.claude/skills/postgres/SKILL.md` |
| Redis | `.claude/skills/redis/SKILL.md` |
| Testing strategy | `.claude/skills/testing/SKILL.md` |
| Performance optimisation | `.claude/skills/performance/SKILL.md` |
| Production readiness | `.claude/skills/production-readiness/SKILL.md` |
| Requirements elicitation | `.claude/skills/requirements-engineering/SKILL.md` |
| Architecture decisions | `.claude/skills/architecture/SKILL.md` |
| Discovery and research | `.claude/skills/discovery/SKILL.md` |
| Stack selection | `.claude/skills/stack-selection/SKILL.md` |
| DevOps / CI/CD | `.claude/skills/devops/SKILL.md` |
| Containerisation | `.claude/skills/docker-kubernetes/SKILL.md` |
| UI/UX design | `.claude/skills/ui-ux-design/SKILL.md` |
| Documentation | `.claude/skills/documentation/SKILL.md` |
| Mobile (cross-platform) | `.claude/skills/mobile/SKILL.md` |
| Node.js backend | `.claude/skills/node-backend/SKILL.md` |
| Python backend | `.claude/skills/python-backend/SKILL.md` |
| Go backend | `.claude/skills/go-backend/SKILL.md` |
| Rust backend | `.claude/skills/rust-backend/SKILL.md` |

---

## Recommended stack options

Because this preset is domain-agnostic, stack selection must follow the process in `.claude/skills/stack-selection/SKILL.md` and reference `.claude/stack-matrix/` files. The table below gives four general-purpose starting points.

| Stack | When to choose it |
|---|---|
| **Node/NestJS or Fastify + PostgreSQL + Redis + Next.js** | Default full-stack TypeScript choice when team is JS/TS-native and no strong reason exists to go elsewhere; suits most internal tools and moderate-scale web products. |
| **Python/FastAPI + PostgreSQL + Celery + React** | Strong for data-heavy, ML-adjacent, or scientific projects; large library ecosystem; good when Python is the team's native language. |
| **Go + PostgreSQL + Redis + React** | Best for high-throughput, low-latency, or resource-constrained environments; excellent for infrastructure tooling, CLI-backed services, or IoT data planes. |
| **Java/Spring Boot + PostgreSQL + React** | Preferred when enterprise integration (SAP, Oracle, AS400, LDAP/AD, SOAP services) is a significant part of the scope; strong transactional guarantees. |

For mobile, desktop, game, IoT, or AI-agent variants, consult the relevant preset as a secondary reference document alongside this one.

---

## Required checklists

All projects must pass all checklists before reaching production, regardless of project type.

- `.claude/checklists/security.md` — apply universally; customise threat model for this project's data sensitivity and attack surface
- `.claude/checklists/qa.md`
- `.claude/checklists/performance.md` — set targets appropriate to the project's load profile (established during discovery)
- `.claude/checklists/accessibility.md` — apply to every human-facing interface: web UI, CLI output, documentation, reports; skip only for systems with zero human interface
- `.claude/checklists/production.md`
- `.claude/checklists/launch.md`

---

## MVP scope pattern

Because the scope is project-specific, use this process rather than a fixed list:

1. **List everything the project must do** (functional requirements from the interview stage).
2. **Tag each item as MVP / Post-MVP / Out-of-scope** using this criterion: an item is MVP only if the product cannot deliver its core value proposition without it.
3. **Apply the three deferrals**: if an item can be done manually during early usage, or if it is only needed after a volume threshold, or if it depends on another deferred item — defer it.
4. **Validate the MVP list**: a new user must be able to complete the primary job-to-be-done end-to-end with only the MVP items. If they cannot, add what is missing. If the list is still large, split into Phase 1a / 1b.
5. **Record the scope decision** as a decision record using `.claude/templates/decision-record.md`.

Common deferrals that apply to almost every custom project:
- Advanced reporting and BI beyond a minimal summary view
- Mobile apps when web-responsive suffices initially
- Third-party integrations beyond those contractually required at launch
- Admin super-panel features beyond the minimum needed to operate the product
- Internationalisation / localisation beyond the primary market language
- Automated onboarding flows that can be handled manually at low user volume

---

## Production risks

These risks apply universally. Add domain-specific risks identified during discovery to the project's own risk register (`.claude/templates/decision-record.md`).

| Risk | Severity | Mitigation |
|---|---|---|
| Scope creep turns MVP into a multi-month monolith before any user feedback | **P0** | Enforce the MVP definition gate; re-validate scope against the core job-to-be-done at every sprint boundary; use decision records to document deferrals |
| Compliance obligation discovered after build begins | **P0** | Complete discovery question 7 before architecture starts; involve legal/compliance reviewer at stage 2; GDPR/HIPAA/SOC 2 gaps are never cheap to retrofit |
| Integration dependency fails to deliver API access or changes contract mid-build | **P0** | Stub all external integrations with recorded contracts from day one; build against the stub until real integration is available; document fallback if integration is unavailable at launch |
| No rollback path for database migrations | **P0** | Every migration must have a tested down script; test rollback on staging before applying to production; no irreversible migration without explicit human approval and a backup |
| Secrets or credentials committed to version control | **P0** | `.env*` in `.gitignore` from day one; pre-commit hook to detect secrets; rotate immediately if any credential is ever committed |
| Performance requirements undefined until late — system underspecified for actual load | **P1** | Define performance targets during discovery (question 6); write performance tests before load testing; establish baseline before launch |
| Single point of failure in a critical dependency not identified until production outage | **P1** | Dependency map in architecture spec; each dependency rated by criticality; fallback or degraded-mode behaviour documented for every P0 dependency |
| Security threat model never produced — common vulnerabilities ship | **P1** | Run `.claude/checklists/security.md` as a gate before any user-facing deployment; threat model written in stage 4 (spec phase) |
| Accessibility skipped because "it's an internal tool" | **P2** | Accessibility is a legal requirement in many jurisdictions for internal tools used by employees; run `.claude/checklists/accessibility.md` regardless of audience |
| Documentation absent — next engineer (or returning self) cannot understand the system | **P2** | README, architecture decision records, runbook, and API docs are part of Definition of Done (`.claude/CLAUDE.md` §5); documentation is not optional |

---

## Launch requirements

These are universal. Add project-specific gates discovered during the spec and build phases.

- [ ] All discovery questions answered and recorded; scope decisions in decision records
- [ ] Architecture spec written and reviewed before implementation began
- [ ] Every external integration tested with a live (non-mocked) call to the real endpoint in staging
- [ ] Security checklist `.claude/checklists/security.md` fully green; threat model reviewed
- [ ] No secrets in version control; secret scanning hook active
- [ ] All compliance obligations identified in discovery verified as satisfied
- [ ] Database backup and point-in-time restore tested on staging
- [ ] Rollback plan documented and tested for every migration and deployment step
- [ ] Performance baseline recorded against the targets defined in discovery; load test at 2× expected launch volume
- [ ] Accessibility checklist `.claude/checklists/accessibility.md` green for every human-facing interface
- [ ] Runbook written: on-call procedure, dependency outage response, data export/recovery, deprovisioning
- [ ] Production-readiness checklist `.claude/checklists/production.md` fully green
- [ ] Stakeholder sign-off on MVP scope — nothing deferred without a written record

---

## How to compose a custom configuration

When the classifier assigns this preset, follow these steps before proceeding to the spec stage:

1. **Answer all 10 discovery questions** with the founder/user (`.claude/agents/core/business-analyst.md`).
2. **Identify overlap with typed presets.** If the project is 70%+ one type, load that preset as a secondary reference: e.g. a vertical SaaS with a customer support module should also read `.claude/presets/helpdesk.md` for the support-specific risks and checklists.
3. **Select agents** from the tables above — aim for the minimum set that covers every aspect of the project; adding unnecessary agents dilutes focus.
4. **Select skills** from the table above — load only skills relevant to the current stage; do not pre-load all skills.
5. **Define project-specific production risks** from the discovery answers and add them to the project risk register alongside the universal risks in this file.
6. **Write the MVP scope list** using the five-step process in the MVP scope pattern section above.
7. **Record this composition** as a decision record so that any engineer joining later can see why specific agents and skills were chosen.

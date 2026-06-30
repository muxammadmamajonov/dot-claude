# Web Engineering Routing Matrix — the elite web team, assembled per task

This is the orchestrator's web-specific routing layer. It maps a web task to the **minimal**
set of agents/skills/checklists/commands needed, picks an **operating mode**, and runs the
right **verification loop**. It complements `.claude/orchestration/routing-matrix.md` (the
universal map) and the orchestrator's selection algorithm (`.claude/agents/core/orchestrator.md`).

> **Principle:** activate only what the task needs. Never load all web agents at once. Map →
> select → run → verify → report. Niche stacks stay dormant until their signal appears.

## Operating modes (the orchestrator picks ONE per task)

| Mode | Intent | Ends with |
|---|---|---|
| **audit-only** | Read & report; no code changes | findings ranked P0–P3 + evidence, no edits |
| **fix-and-verify** | Change code, then prove it works | diff + passing tests/build + re-audit of the fixed area |
| **production-hardening** | Close prod gaps | `.claude/checklists/web-production.md` green or risks recorded |
| **ui-ux-polish** | Visual/interaction quality | before/after rationale, a11y + responsive re-check |
| **security-review** | Threat + vuln pass | OWASP-aligned findings + fixes/threat model |
| **performance-review** | Speed & cost | Core Web Vitals / backend profile + budget verdict |
| **release-readiness** | Ship gate | go/no-go with the release checklist |
| **documentation** | Capture knowledge | README/ADR/API/runbook updated |

The orchestrator states the mode up front and does not silently switch modes mid-task.

## Task → team (web)

| Web task | Lead agent(s) | Support | Skills | Checklists |
|---|---|---|---|---|
| Map an unknown repo | `core/codebase-mapper` | — | discovery | — |
| Architecture review | `core/solution-architect` | architecture-auditor role | architecture | architecture |
| Frontend feature/build | `engineering/frontend-engineer` + matched `stack/web/*` | ui-ux-designer | web, react-next/vue-nuxt/… | web, ui-ux, accessibility |
| UI/UX polish | `design/ui-ux-designer` + `design/design-system-architect` | accessibility-designer | ui-ux-design + **installed `frontend-design`** | ui-ux, accessibility |
| Responsive / mobile-web | `design/mobile-ux-specialist` | accessibility-auditor | ui-ux-design | accessibility, web |
| Accessibility (WCAG) | `quality/accessibility-auditor` | accessibility-designer | ui-ux-design | accessibility |
| Backend feature/build | `engineering/backend-engineer` + matched `stack/backend/*` | api-architect | backend, api-design | backend, api |
| API design/audit | `engineering/api-architect` | backend-engineer | api-design | api |
| Database/data layer | `engineering/database-architect` + matched `stack/database/*` | — | data-modeling, postgres/… | database, data-model |
| Auth & permissions | `quality/security-auditor` | backend-engineer | security | security, privacy-compliance |
| Security audit | `quality/security-auditor` | privacy-compliance-auditor | security | security, dependencies |
| Performance | `quality/performance-engineer` | frontend/backend eng | performance | performance, cost |
| QA / tests | `quality/qa-engineer` + `quality/test-automation-engineer` | — | testing | qa |
| E2E (browser) | `engineering/playwright-e2e-engineer` | qa-engineer | testing | qa |
| DevOps / CI-CD | `engineering/devops-engineer` | cloud-architect, `stack/cloud/*` | devops, docker-kubernetes | devops, release-rollback |
| Observability / SRE | `quality/reliability-engineer` | devops-engineer | observability | observability, incident-response |
| Realtime / queues / files / notifications / payments | `engineering/{realtime,integration,payments,search}-engineer` | — | realtime, messaging-queues, payments, search | backend, performance |
| AI integration | `engineering/ai-ml-engineer` + matched `stack/ai/*` | evaluation-engineer | ai-ml | ai-ml, security |
| Refactor | `engineering/refactoring-specialist` (or technical-lead) | code-reviewer | architecture | qa |
| Bug fix | `engineering/bug-fix-specialist` (or the owning engineer) | qa-engineer | testing | qa |
| Docs | `core/documentation-writer` | — | documentation | — |
| Release | `engineering/release-engineer` | production-readiness-auditor | production-readiness | launch, release-rollback |
| Production readiness | `quality/production-readiness-auditor` | all gate owners | production-readiness | web-production, production |

## High-value external skill (discovered via /find-skills)

- **`frontend-design`** (anthropics/skills, ~600k installs) — the gold-standard UI/visual-quality
  skill. If installed (`~/.agents/skills/frontend-design` or `~/.claude/skills/frontend-design`),
  prefer it for any **ui-ux-polish** / net-new UI work; our `ui-ux-design` and `web` skills defer to
  it for visual craft and cover the OS-specific flow (tokens, a11y gate, responsive review). If it is
  not installed, suggest `npx -y skills add anthropics/skills --skill frontend-design -g`.

## Verification loops (required for fix-and-verify, hardening, release)

1. **Change** → 2. **Prove** (build + lint + the relevant tests pass; never fabricate results) →
3. **Re-audit** the changed area with the matching gate checklist → 4. **Risk review** (what could
this break; is it reversible) → 5. **Final summary** (what changed, evidence, residual risk).
For serious tasks, a second independent reviewer agent (`core/code-reviewer`) checks the diff before done.

## Commands that drive this

- `/web-audit <scope> [--mode]` — routes to the auditors above for a scope (frontend|backend|api|
  database|security|performance|accessibility|responsive|devops|observability|full).
- `/web-readiness` — runs `.claude/checklists/web-production.md` + the baseline gates → go/no-go.
- Plus the universal commands: `/route`, `/audit-security`, `/audit-performance`, `/audit-production`,
  `/implement-feature`, `/review-feature`, `/fix-bugs`, `/refactor-safely`, `/create-tests`,
  `/prepare-launch`, `/commit-ready`.

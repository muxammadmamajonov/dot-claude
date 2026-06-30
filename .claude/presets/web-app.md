# Web Application Preset

## Project type
General-purpose web application served in a browser. Variants: multi-page app (MPA), single-page app (SPA), server-side rendered (SSR), static site with client islands, progressive web app (PWA), internal tool/admin panel, SaaS dashboard, or hybrid approaches combining any of the above.

## Typical use cases
- SaaS products (dashboards, admin portals, productivity tools)
- Public-facing marketing + application sites
- Internal tools (ops dashboards, data explorers, approval workflows)
- Consumer-facing experiences (booking, reading, shopping)
- PWAs that need offline support and home-screen install

## Required discovery questions
1. Who are the primary users — public anonymous visitors, authenticated employees, or both? What is the expected concurrent user count at launch vs. 12 months out?
2. Is the application primarily read-heavy, write-heavy, or real-time collaborative? Are any pages "landing critical" (must load <2 s on 3G)?
3. Does the project require server-side rendering (SEO, social sharing), static generation (CDN edge), or is a pure SPA acceptable?
4. What authentication model is needed: social OAuth, magic link, username/password, SSO/SAML, passkeys, or no auth?
5. Are there multi-tenancy requirements (separate workspaces per org)? If yes, does data need physical or logical isolation?
6. Which payment processor, CRM, or third-party integrations are mandatory at launch versus post-launch?
7. What are the geographic regions you must serve? Any data-residency or GDPR/CCPA/HIPAA constraints?
8. Is offline functionality required (service worker, background sync)?
9. What are the accessibility requirements — WCAG 2.1 AA minimum, or stricter (AAA, ADA legal obligation)?
10. Will the frontend be a standalone project, a monorepo with a shared design system, or embedded inside another host (iframe, micro-frontend)?

## Recommended agents

### Core
- `.claude/agents/core/orchestrator.md` — project coordination and phase sequencing
- `.claude/agents/core/solution-architect.md` — system design and ADR authoring
- `.claude/agents/core/project-manager.md` — sprint and task breakdown

### Engineering
- `.claude/agents/engineering/frontend-engineer.md` — component authoring, routing, state
- `.claude/agents/engineering/backend-engineer.md` — API layer, business logic, DB models
- `.claude/agents/engineering/backend-engineer.md` — authentication, session management, RBAC

### Quality
- `.claude/agents/quality/qa-engineer.md` — test strategy, E2E, regression coverage
- `.claude/agents/quality/performance-engineer.md` — Core Web Vitals, bundle analysis, load testing
- `.claude/agents/quality/security-auditor.md` — OWASP Top 10, dependency audit, CSP

### Design
- `.claude/agents/design/ui-ux-designer.md` — information architecture, wireframes, user flows
- `.claude/agents/design/accessibility-designer.md` — WCAG audit, screen-reader testing

### Domain
- `.claude/agents/design/product-designer.md` — meta tags, structured data, sitemap (when public-facing)
- `.claude/agents/design/ui-ux-designer.md` — locale detection, RTL support, pluralisation (when multi-language)

## Recommended skills
- `.claude/skills/web/SKILL.md` — component patterns, CSS architecture
- `.claude/skills/api-design/SKILL.md` — REST/GraphQL endpoint conventions
- `.claude/skills/security/SKILL.md` — session handling, token rotation, MFA
- `.claude/skills/security/SKILL.md` — XSS, CSRF, CSP, secure headers
- `.claude/skills/testing/SKILL.md` — unit, integration, E2E pyramid
- `.claude/skills/performance/SKILL.md` — code splitting, image optimisation, caching headers
- `.claude/skills/ui-ux-design/SKILL.md` — aria roles, focus management, keyboard nav

## Recommended stack options

| Stack | Rationale |
|---|---|
| **Next.js + PostgreSQL + Prisma** | SSR/SSG/RSC in one framework; Prisma type-safe ORM; excellent ecosystem. See `.claude/stack-matrix/web.md` |
| **SvelteKit + SQLite/Turso (edge) or Postgres** | Smaller bundle, built-in transitions, edge-ready; great for low-latency read-heavy tools |
| **React SPA + Vite + FastAPI/Node API** | Best when backend is a separate service or team; API-first contract visible from day 1 |
| **Astro + headless CMS** | Content-heavy / mostly-static sites; islands architecture keeps JS minimal; strong SEO baseline |

Reference `.claude/stack-matrix/web.md`, `.claude/stack-matrix/backend.md`, `.claude/stack-matrix/database.md` for detailed tradeoffs.

## Required checklists
- `.claude/checklists/security.md` — OWASP, headers, secrets scanning
- `.claude/checklists/performance.md` — Core Web Vitals, bundle budget, lazy loading
- `.claude/checklists/accessibility.md` — WCAG 2.1 AA, keyboard nav, colour contrast
- `.claude/checklists/launch.md` — DNS, SSL, error monitoring, analytics, rollback plan
- `.claude/checklists/web.md` — robots.txt, canonical, OG tags, structured data (public sites)

## MVP scope pattern

**In MVP**
- Auth (sign-up, login, password reset)
- Core user flow (the one thing the product does)
- Basic CRUD for the primary entity
- Error states and empty states in UI
- Mobile-responsive layout (single breakpoint is acceptable)
- Logging and basic alerting

**Deferred to v2**
- Multi-language / i18n
- Advanced RBAC beyond owner/member
- Real-time collaboration (WebSocket)
- Offline support / PWA manifest
- Advanced analytics and A/B testing
- Admin super-panel for support teams
- Bulk import/export

## Production risks

| Risk | Severity | Mitigation |
|---|---|---|
| XSS via user-generated content | P0 | Sanitise all HTML (DOMPurify), strict CSP, no `innerHTML` |
| Auth token exposure (localStorage) | P0 | Use `HttpOnly` cookies; rotate refresh tokens; revoke on logout |
| Unthrottled API endpoints → abuse / DDoS | P0 | Rate limiting per IP and per user at gateway layer |
| Missing DB indexes on high-read queries | P1 | Slow-query log in staging; add indexes before launch |
| N+1 queries in ORM | P1 | Enable query logging in dev; use eager loading or DataLoader |
| Missing CSRF protection on state-mutation routes | P1 | SameSite cookie + CSRF token; validate `Origin` header |
| Unhandled async errors crashing SSR | P1 | Global error boundary; structured error logging |
| Bundle size regression blocking FCP | P2 | Bundle analyser in CI; size budget enforced |
| No GDPR consent banner on EU traffic | P2 | Cookie consent before any tracking initialises |
| Hardcoded secrets in client bundle | P0 | `.env` never committed; secrets audit in CI (`gitleaks`) |

## Launch requirements
- All P0 checklist items in `.claude/checklists/security.md` signed off
- Lighthouse score ≥ 90 Performance, 100 Accessibility on critical pages
- SSL certificate verified; HSTS header present
- Error monitoring (Sentry or equivalent) wired and producing test alerts
- Database backups automated and restoration tested
- Staging environment mirrors production (same env vars schema, same DB schema)
- Rollback plan documented and rehearsed (feature flags or blue/green deploy)
- On-call runbook drafted in `docs/runbook.md`
- GDPR/privacy policy page live and linked from footer

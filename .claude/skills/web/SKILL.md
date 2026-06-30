---
name: web
description: >
  Activate when building, extending, or debugging a web application end-to-end —
  including choosing a rendering strategy, wiring data fetching, setting up auth,
  configuring builds, and deploying. Covers SPAs, SSR/SSG frameworks (Next.js,
  Nuxt, SvelteKit, Remix, Astro), and traditional MPA setups. Do NOT activate
  for pure backend APIs (use .claude/skills/backend/SKILL.md) or mobile/desktop
  shells that happen to embed a WebView.
---

# Web Application Skill

**Scope: framework-agnostic web concerns. Next.js specifics → `.claude/skills/react-next/SKILL.md`.**

## When to use

- Starting a new web project (greenfield or from spec)
- Adding a significant feature: auth, payments, real-time, i18n, image pipeline
- Migrating rendering strategy (CSR → SSR, pages → app router, etc.)
- Diagnosing performance regressions (LCP, CLS, TTI, bundle size)
- Preparing a web app for production (HTTPS, caching, CSP, monitoring)

---

## Workflow

1. **Classify the project** — Read `docs/specs/product.md` and `.claude/stack-matrix/` to confirm framework, rendering model (CSR / SSR / SSG / ISR), and target environments (browser-only, hybrid, PWA). If none exist, ask the founder interview questions first (see `.claude/agents/core/orchestrator.md`).

2. **Confirm rendering strategy** — Match business requirements to strategy:
   | Requirement | Preferred strategy |
   |---|---|
   | SEO-critical public pages | SSR or SSG |
   | Highly dynamic per-user UI | CSR with API |
   | Mostly static, rare updates | SSG + ISR |
   | Mixed | Hybrid (e.g. Next.js App Router) |

3. **Scaffold project structure** — Use the framework CLI (`next`, `nuxt`, `create-svelte`, `astro`) with TypeScript enabled. Verify output against `.claude/templates/architecture.md`.

4. **Wire data layer** — Choose one pattern and be consistent:
   - Server components / loaders → fetch on the server, pass serialized data down
   - API routes / BFF → client calls `/api/*`, server owns data access
   - React Query / SWR → client cache + revalidation
   Validate schema at the boundary with Zod or Valibot.

5. **Implement auth** — Follow `.claude/skills/security/SKILL.md`. Prefer an established library (NextAuth/Auth.js, Lucia, Clerk) over hand-rolled sessions. Enforce HTTPS-only cookies with `SameSite=Strict`.

6. **Build UI** — Component-first. Create atomic components before page-level compositions. Enforce WCAG 2.1 AA: semantic HTML, keyboard navigation, color contrast ≥ 4.5:1. Reference `.claude/checklists/accessibility.md`.

7. **Optimize bundle** — After first working build:
   - Run `next build --analyze` (or equivalent) and identify chunks > 100 KB.
   - Code-split dynamic imports (`next/dynamic`, `React.lazy`).
   - Serve images via optimized pipeline (Next Image, Astro `<Image>`, etc.) with `loading="lazy"` and explicit width/height.

8. **Configure environment & secrets** — `.env.local` for dev; never commit secrets. Use typed env validation (`@t3-oss/env-nextjs` or equivalent). Document all required variables in `.env.example`.

9. **Write tests** — Unit: component logic with Vitest. Integration: user flows with Playwright or Cypress. Target ≥ 80% branch coverage on critical paths. Reference `.claude/checklists/qa.md`.

10. **Run pre-deploy checklist** — See `.claude/checklists/production.md`. Confirm: CSP headers, error boundaries, logging, rate-limiting on auth routes, CDN caching headers.

11. **Deploy** — Build → containerize or use platform deploy hook (Vercel, Netlify, Fly.io, AWS Amplify). Run smoke tests against preview URL before promoting to production.

---

## Standards

**Do**
- Validate all user input server-side, never trust the client.
- Use `Content-Security-Policy` headers; disable `unsafe-inline` where possible.
- Serve static assets with `Cache-Control: public, max-age=31536000, immutable` and hash-based filenames.
- Keep `node_modules` out of Docker images — copy `package.json` + lock file, run `npm ci`, then copy source.
- Lazy-load routes and heavy third-party scripts.
- Prefer relative imports with path aliases (`@/components`) defined in `tsconfig.json`.

**Do not**
- Store tokens in `localStorage` (use `httpOnly` cookies).
- Render raw user HTML without sanitization (use `DOMPurify` or server-side escaping).
- Inline `<script>` tags that bypass CSP.
- Block the main thread with synchronous I/O or heavy computation; offload to Web Workers.
- Hard-code environment-specific URLs in source code.
- Ship `console.log` or debug code to production.

---

## Common mistakes to avoid

- **Missing `key` props in lists** — causes subtle reconciliation bugs; always use stable, unique keys (not array index).
- **Fetching on every render** — memoize requests with React Query, SWR, or server-component caching; missing dependencies in `useEffect` is the classic trigger.
- **SSR/hydration mismatch** — avoid accessing `window` or `document` at module scope; guard with `typeof window !== 'undefined'` or use `useEffect`.
- **Unhandled loading and error states** — every async data fetch needs a loading skeleton and an error fallback; missing them produces blank screens.
- **Forgetting `rel="noopener noreferrer"` on external links** — tabnapping vulnerability.
- **Over-fetching in API routes** — select only the columns/fields the page needs; returning full ORM objects leaks internal data.
- **Not invalidating CDN cache after deploy** — stale assets served to users; use versioned filenames or cache-busting query params.

---

## Output format

A production-ready web project should include:

```
/
├── src/
│   ├── app/ (or pages/)        # Route files
│   ├── components/             # Reusable UI
│   ├── lib/                    # Shared utilities, data-access, auth
│   ├── styles/                 # Global CSS / Tailwind config
│   └── types/                  # Shared TypeScript types
├── public/                     # Static assets (favicon, robots.txt)
├── tests/                      # Unit + e2e tests
├── .env.example                # Required env vars (no values)
├── Dockerfile (optional)
└── README.md                   # Local setup in < 5 commands
```

---

## Related checklists

- `.claude/checklists/security.md`
- `.claude/checklists/accessibility.md`
- `.claude/checklists/performance.md`
- `.claude/checklists/qa.md`
- `.claude/checklists/production.md`

## Related agents

- `.claude/agents/core/orchestrator.md`
- `.claude/agents/engineering/frontend-engineer.md`
- `.claude/agents/quality/security-auditor.md`

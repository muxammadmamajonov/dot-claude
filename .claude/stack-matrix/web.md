# Web Frontend Stack Matrix

Choose based on three primary drivers: **team familiarity**, **rendering requirements** (SSR/SSG/SPA/islands), and **long-term maintenance cost**. For content-heavy or SEO-sensitive projects, lean toward meta-frameworks (Next, Nuxt, SvelteKit, Astro). For rich interactive apps with no SEO constraints, a pure SPA is fine. For performance-critical public sites, Astro or Qwik deserves serious consideration.

---

## React / Next.js

- **When to use:** Full-stack web apps, SaaS dashboards, e-commerce, content sites, marketplaces; any project needing SSR, SSG, ISR, or API routes in one framework. Largest hiring pool.
- **When NOT to use:** Tiny static sites that don't need JS at all; teams that find React's mental model (hooks, re-render behavior, RSC) consistently painful.
- **Strengths:** Massive ecosystem, App Router for RSC + streaming, Vercel-native CI/CD, huge community, strong TypeScript support, excellent tooling (Turbopack, ESLint, Jest, Vitest).
- **Weaknesses:** App Router learning curve is steep; bundle size creep if discipline is low; RSC adds cognitive overhead for new contributors; vendor drift toward Vercel.
- **Team fit:** Mid-to-large teams; works well when at least one member has React experience. Easiest to hire for.
- **Scale fit:** Startup MVPs through hyperscale. Vercel Edge, standalone Docker, or self-hosted Node all viable.
- **Production risks:** Over-reliance on `use client` defeats RSC benefits; hydration mismatch errors; App Router caching behavior is nuanced and bites teams in production.

---

## Vue / Nuxt

- **When to use:** Projects where the team prefers a gentler learning curve; CMS-driven sites; teams coming from Vue 2 who need to upgrade; Laravel + SPA combos.
- **When NOT to use:** Very large teams where React/Angular hiring is easier; projects needing the absolute latest RSC-style patterns (Nuxt is catching up but lags slightly).
- **Strengths:** Single-file components are highly readable; Nuxt auto-imports reduce boilerplate significantly; excellent SSR/SSG/ISR via Nuxt; growing Nitro server layer.
- **Weaknesses:** Smaller ecosystem than React; fewer ready-made SaaS UI kits; occasional Nuxt version-upgrade turbulence.
- **Team fit:** Small-to-medium teams; solo developers who find React's hook rules frustrating. Easier onboarding for developers from template-based backgrounds (Blade, Jinja, Twig).
- **Scale fit:** Good up to mid-scale; Nuxt Edge rendering works on Cloudflare Workers.
- **Production risks:** Nuxt auto-import magic can make debugging harder; Vue 2 → 3 Composition API migration is still a cost some teams carry.

---

## Angular

- **When to use:** Enterprise internal tools, large-scale B2B platforms, teams that need strict opinionated architecture enforced at framework level; organizations already invested in the Angular ecosystem.
- **When NOT to use:** Early-stage startups where velocity matters more than architecture; teams without TypeScript experience; projects needing fine-grained SSR/islands (Angular SSR is improving but not the primary draw).
- **Strengths:** Opinionated structure (modules, DI, decorators) reduces architectural drift in large teams; RxJS for complex async; strong CLI; signals-based reactivity now available; Angular Material.
- **Weaknesses:** Verbose boilerplate; steeper initial learning curve than React/Vue; slower to ship new paradigms (RSC, islands); bundle size historically large (improving with Ivy).
- **Team fit:** Large enterprise teams (10+ contributors); organizations with dedicated Angular engineers and Angular-centric hiring pipelines.
- **Scale fit:** Excellent for large monorepo enterprise apps (Nx works particularly well). Less natural for edge-first or content-heavy public sites.
- **Production risks:** RxJS misuse causes memory leaks; upgrade paths between major Angular versions can be time-consuming; SSR is mature but not ecosystem-leading.

---

## Svelte / SvelteKit

- **When to use:** Performance-sensitive consumer apps; developer-tools frontends; teams that value minimal runtime overhead; projects where developer happiness matters and React fatigue is real.
- **When NOT to use:** Large teams needing the biggest ecosystem and most third-party UI libraries; teams that need a massive pool of pre-existing Svelte developers.
- **Strengths:** Compile-time reactivity = near-zero runtime overhead; highly readable component syntax; SvelteKit covers SSR/SSG/CSR/API routes; Runes (Svelte 5) further clean up reactivity.
- **Weaknesses:** Smaller component library ecosystem; fewer third-party integrations; less mature enterprise tooling; hiring pool is smaller than React.
- **Team fit:** Tight, experienced teams who want to move fast and care about bundle size. Great for side projects and indie SaaS.
- **Scale fit:** Handles small-to-large apps well technically; ecosystem scale is the limiting factor, not framework capability.
- **Production risks:** Svelte 4 → 5 (Runes) migration has breaking changes; some npm packages assume a virtual DOM and need wrapping.

---

## Astro

- **When to use:** Content sites, blogs, documentation sites, marketing pages, landing pages — any project where most content is static and JS should be minimal by default.
- **When NOT to use:** Highly interactive applications (dashboards, real-time apps) where most of the page is dynamic; teams that want a single framework for both content and app logic.
- **Strengths:** Ships zero JS by default; islands architecture lets you sprinkle React/Vue/Svelte/Solid selectively; exceptional Core Web Vitals scores out of the box; content collections with type safety.
- **Weaknesses:** Not designed for highly interactive SPAs; multi-framework islands adds toolchain complexity; smaller community than Next.js or Nuxt.
- **Team fit:** Frontend teams building content-heavy sites who want performance without sacrificing component-driven workflow.
- **Scale fit:** Excellent for content at scale (docs, marketing sites). Less suited to app-like experiences.
- **Production risks:** Misusing islands (too many client-side) defeats the whole value proposition; SSR adapter lock-in (Node, Vercel, Cloudflare — must pick).

---

## SolidJS

- **When to use:** Projects that need React-like DX but require genuine fine-grained reactivity without virtual DOM overhead; performance-critical interactive UIs; teams with advanced React experience who want more control.
- **When NOT to use:** Teams without strong JS fundamentals; projects that rely heavily on the React ecosystem (many React libraries don't port to Solid); mainstream hiring is important.
- **Strengths:** Fine-grained reactivity (signals, no re-render of entire components); React-JSX-like syntax reduces learning curve for React devs; SolidStart for SSR/SSG; excellent Lighthouse scores.
- **Weaknesses:** Small ecosystem; few pre-built UI component libraries; SolidStart is still maturing; minimal hiring pool.
- **Team fit:** Experienced frontend engineers who have hit React's performance ceilings or re-render issues.
- **Scale fit:** Technically scales well; ecosystem immaturity is the ceiling.
- **Production risks:** Third-party library compatibility issues; risk of being an early adopter of a framework that may not reach critical mass.

---

## Qwik

- **When to use:** Public-facing pages where Time-to-Interactive must be near-instant regardless of JS bundle size; e-commerce storefronts; enterprise content sites with heavy personalization.
- **When NOT to use:** Internal tools, dashboards, or apps where TTI is not a primary concern; teams without patience for a significantly different mental model (resumability vs hydration).
- **Strengths:** Resumability architecture eliminates hydration entirely — JS executes only when the user interacts; near-zero JS on initial load even for large apps; Qwik City for routing/SSR.
- **Weaknesses:** Very different mental model (`$` suffix, lazy loading signals) requires genuine relearning; tiny ecosystem; minimal community relative to React/Vue; immature tooling.
- **Team fit:** Specialist teams focused on Core Web Vitals and conversion rate for high-traffic public pages.
- **Scale fit:** Designed for high-traffic public sites. Overkill for internal apps.
- **Production risks:** Ecosystem immaturity; risk of framework abandonment or pivot; debugging resumable state is non-trivial.

---

## Comparison Table

| Framework      | Learning Curve | Ecosystem Size | SSR/SSG | Bundle Size | Hiring Pool | Best For                          |
|----------------|---------------|----------------|---------|-------------|-------------|-----------------------------------|
| React/Next.js  | Medium-High   | Largest        | Yes     | Medium      | Largest     | SaaS, dashboards, e-commerce      |
| Vue/Nuxt       | Low-Medium    | Large          | Yes     | Small-Med   | Large       | CMS sites, Laravel backends       |
| Angular        | High          | Large          | Yes     | Medium-High | Medium-Large| Enterprise B2B, internal tools    |
| Svelte/SvelteKit| Low          | Medium         | Yes     | Smallest    | Small-Med   | Performance-first, indie SaaS     |
| Astro          | Low           | Medium         | Yes     | Near-zero   | Small-Med   | Content, docs, marketing          |
| SolidJS        | Medium        | Small          | Yes     | Very small  | Small       | Perf-critical interactive apps    |
| Qwik           | High          | Small          | Yes     | Near-zero   | Tiny        | High-traffic public storefronts   |

---

## Recommended Combinations

| Combination                          | Why                                                                                          |
|--------------------------------------|----------------------------------------------------------------------------------------------|
| Next.js + TypeScript + Tailwind + shadcn/ui | Fastest path to production SaaS; all tools interoperate seamlessly; massive community support |
| Nuxt + Pinia + Tailwind              | Clean Vue stack; auto-imports reduce boilerplate; good fit for Laravel-backed projects       |
| SvelteKit + TypeScript + Tailwind    | Minimal runtime overhead; excellent DX; ideal for indie SaaS or developer tools             |
| Astro + Tailwind + MDX               | Best-in-class content sites; zero JS overhead by default; easy content authoring            |
| Next.js + tRPC + Prisma + Postgres   | Full-stack TypeScript with end-to-end type safety; standard for modern SaaS backends        |
| Angular + Nx + Angular Material      | Large enterprise monorepo; enforced architecture; shared libraries across teams             |

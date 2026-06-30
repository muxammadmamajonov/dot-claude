# Static Site Preset

## Project type
A website whose pages are pre-rendered to HTML/CSS/JS at build time and served directly from a CDN or file host with no origin server. Variants: marketing/landing site, documentation site, blog or content publication, portfolio, event or campaign microsite, open-source project site, help center with static search, or JAMstack site with serverless functions at the edge.

## Typical use cases
- Product marketing and landing pages (conversion-focused, SEO-critical)
- Developer documentation portals (versioned docs, API references)
- Personal or company blogs (CMS-driven or markdown-based)
- Campaign and event microsites (short lifespan, high burst traffic)
- Open-source project sites with contribution guides
- Portfolios and case-study showcases
- Help center / knowledge-base (read-mostly, search-driven)

## Required discovery questions
1. Is the primary goal SEO/discovery, brand credibility, lead capture, or content delivery? What is the conversion event (sign-up, purchase, contact form)?
2. Who authors and publishes content — developers committing markdown, non-technical editors via a CMS, or both? How frequently does content change (daily vs. quarterly)?
3. What is the expected traffic profile at launch and during peak campaigns? Are there specific geographic regions that need the lowest latency?
4. Are there interactive features beyond static content — forms, search, gated content, payments, or embedded calculators — that require serverless functions or third-party integrations?
5. Is versioning required (e.g. documentation for multiple product versions)? How many versions must coexist?
6. What are the SEO requirements — meta tags, structured data (JSON-LD), XML sitemaps, canonical URLs, Open Graph, hreflang for multiple languages?
7. Does the site need to support multiple languages or locales? Is translation managed by the team or a third-party service?
8. What is the expected site lifespan and update frequency? Will the site outlive a specific campaign, or is it the long-term canonical home?
9. Are there legal/compliance requirements — cookie consent banners, privacy policy, accessibility legislation (ADA, EN 301 549)?
10. What is the deployment and preview workflow — auto-deploy from `main`, deploy previews per PR, manual publish step via CMS?

## Recommended agents

### Core
- `.claude/agents/core/orchestrator.md` — project sequencing and build-pipeline governance
- `.claude/agents/core/solution-architect.md` — rendering strategy, CDN topology, content architecture
- `.claude/agents/core/project-manager.md` — content migration planning, launch phasing

### Engineering
- `.claude/agents/engineering/frontend-engineer.md` — component authoring, templating, build configuration
- `.claude/agents/engineering/devops-engineer.md` — CI/CD pipeline, CDN configuration, preview deploys

### Quality
- `.claude/agents/quality/qa-engineer.md` — link validation, SEO smoke tests, form submission testing
- `.claude/agents/quality/performance-engineer.md` — Core Web Vitals, image optimisation, bundle budget
- `.claude/agents/quality/accessibility-auditor.md` — WCAG 2.1 AA, keyboard nav, colour contrast

### Design
- `.claude/agents/design/ui-ux-designer.md` — information architecture, landing page hierarchy, CTA design
- `.claude/agents/design/accessibility-designer.md` — focus states, ARIA landmarks, skip-nav

### Domain
- `.claude/agents/core/documentation-writer.md` — structured data, sitemap, robots.txt, meta copy

## Recommended skills
- `.claude/skills/web/SKILL.md` — component patterns, CSS architecture, responsive layout
- `.claude/skills/performance/SKILL.md` — image formats (AVIF/WebP), lazy loading, critical CSS, font subsetting
- `.claude/skills/ui-ux-design/SKILL.md` — aria landmarks, focus management, keyboard navigation
- `.claude/skills/security/SKILL.md` — CSP headers, form honeypot, bot protection on contact endpoints
- `.claude/skills/devops/SKILL.md` — CDN cache invalidation, deploy previews, branch-based routing

## Recommended stack options

| Stack | Rationale |
|---|---|
| **Astro + Markdown/MDX + Decap CMS (or no CMS)** | Best-in-class static output with zero JS by default; islands for interactive bits; excellent for docs and blogs; deploy anywhere. See `.claude/stack-matrix/web.md` |
| **Next.js (Static Export / SSG) + Contentful or Sanity** | Ideal when the team already uses React and needs a headless CMS with a visual editor; `next export` produces pure static files |
| **Hugo + Netlify CMS** | Sub-second builds even at thousands of pages; Go templates; ideal for very large documentation sites or content-heavy blogs where build speed matters |
| **Eleventy (11ty) + Netlify/Vercel** | Maximum flexibility with minimal magic; works with any templating language; excellent for highly customised marketing sites and design-system-driven builds |

Reference `.claude/stack-matrix/web.md`, `.claude/stack-matrix/cloud-devops.md` for CDN and deployment tradeoffs.

## Required checklists
- `.claude/checklists/web.md` — robots.txt, canonical URLs, OG tags, JSON-LD structured data, XML sitemap
- `.claude/checklists/performance.md` — Core Web Vitals, image optimisation, font loading, cache headers
- `.claude/checklists/accessibility.md` — WCAG 2.1 AA, keyboard nav, skip-nav, colour contrast
- `.claude/checklists/security.md` — CSP headers, HTTPS enforcement, form bot protection, secrets never in HTML
- `.claude/checklists/launch.md` — DNS, SSL, CDN cache warm-up, 404 page, error monitoring, analytics

## MVP scope pattern

**In MVP**
- All primary marketing/content pages built and responsive
- Metadata (title, description, OG image) on every page
- XML sitemap and robots.txt
- Contact or lead-capture form with validation and spam protection
- 404 page
- Google Analytics or privacy-respecting alternative wired up
- Auto-deploy from `main` branch
- Lighthouse score ≥ 90 across Performance, Accessibility, SEO on landing page

**Deferred to v2**
- Headless CMS integration (if initially markdown-based)
- Versioned documentation (if docs-type site)
- Multi-language / hreflang support
- Advanced search (Algolia DocSearch, Pagefind)
- A/B testing on landing page variants
- Dark-mode toggle
- Newsletter subscription integration
- Automated broken-link checking in CI

## Production risks

| Risk | Severity | Mitigation |
|---|---|---|
| Stale CDN cache after deploy — users see old content | P0 | Automated cache purge on every deploy; use content-hashed asset filenames |
| Secrets embedded in client-side HTML or JS bundles | P0 | Environment variables for build-time config; audit build output before publishing; never include API keys accessible client-side |
| Forms submitting to insecure or unvalidated endpoints | P0 | HTTPS-only endpoints; server-side validation; honeypot + rate limit on form handler |
| Missing HTTPS redirect — plain HTTP serving | P0 | Enforce HTTPS at CDN level; HSTS header on all responses |
| Broken links on launch (internal 404s, dead outbound links) | P1 | Automated link checker in CI (`htmltest` or Playwright); run before every deploy |
| Missing or incorrect canonical tags causing SEO dilution | P1 | Canonical URL set on every page; test with Google Search Console after launch |
| Images not optimised — LCP > 2.5 s on mobile | P1 | Use next-gen formats (AVIF/WebP); `width`/`height` attributes on `<img>`; lazy-load below fold |
| No fallback for failed third-party scripts (analytics, chat) | P1 | Load non-critical scripts with `async`/`defer`; site must be fully functional with JS blocked |
| Cookie consent banner absent on EU traffic | P1 | Implement CMP before any analytics loads; block tracking until consent |
| Accessibility violations failing automated scan | P2 | Run axe-core in CI; manual screen-reader test on nav and forms |

## Launch requirements
- Lighthouse scores ≥ 90 Performance, 100 Accessibility, 100 SEO on the landing page
- All internal links return 200; no broken external links on critical pages
- HTTPS enforced with HSTS preload submitted; SSL certificate auto-renews
- XML sitemap submitted to Google Search Console; coverage report reviewed
- CDN cache-invalidation verified: deploy followed by immediate content refresh confirmed
- Cookie consent mechanism live before any analytics or tracking script fires
- Contact form confirmed end-to-end (submission → notification → thank-you redirect)
- 404 page styled and returning correct HTTP 404 status code
- Error monitoring wired (even for serverless form functions)
- Rollback procedure documented: prior CDN snapshot or Git revert to previous deploy

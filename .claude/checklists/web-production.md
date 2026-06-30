# Web Production-Readiness Checklist

The web-specific gate before shipping a production web application. Pairs with the universal
`.claude/checklists/production.md`; this one adds the browser/HTTP/frontend concerns. Severity:
**P0** blocker · **P1** important (soon) · **P2** hardening · **P3** post-launch/backlog.

## P0 — Blockers (must pass before launch)

- [ ] **HTTPS everywhere**: TLS enforced; HTTP→HTTPS redirect; HSTS header set (`max-age` ≥ 6 months).
- [ ] **Security headers present**: `Content-Security-Policy` (no unsafe-inline scripts), `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `X-Frame-Options`/frame-ancestors.
- [ ] **Cookies hardened**: session cookies `Secure`, `HttpOnly`, `SameSite` set; no secrets/PII in localStorage.
- [ ] **AuthN/AuthZ enforced server-side**: every protected route/endpoint checks identity AND permission; no client-only guards; no IDOR (object ownership verified).
- [ ] **Input validated & output encoded**: server-side validation on all inputs; no XSS sink without encoding; parameterized queries (no SQL/NoSQL injection); SSRF/file-upload paths constrained.
- [ ] **Secrets not in the bundle or repo**: no API keys/tokens in client JS or git; server secrets from env/secret manager; `.env*` git-ignored.
- [ ] **No console errors on critical paths**; error boundary / graceful 500 page; no stack traces leaked to users.
- [ ] **Build + typecheck + lint clean**; production build succeeds; no `console.log` of sensitive data.
- [ ] **Automated tests pass** for critical user journeys (auth, checkout/core action); results are real, not assumed.
- [ ] **Rollback path exists**: previous version redeployable, or migration has a tested down path / feature flag.

## P1 — Important (soon after launch)

- [ ] **Core Web Vitals** within target on key pages: LCP < 2.5s, INP < 200ms, CLS < 0.1 (field or lab via Lighthouse).
- [ ] **Caching & CDN**: static assets fingerprinted + long-cache; HTML/API cache headers deliberate; CDN in front of static.
- [ ] **Accessibility**: WCAG 2.2 AA on key flows — keyboard reachable, visible focus, labelled controls, AA contrast, no critical axe violations.
- [ ] **Error tracking + uptime monitoring** wired (Sentry/equivalent) with release tagging; alerts route to a human.
- [ ] **Structured logging + a request/correlation id**; health/readiness endpoint; graceful shutdown.
- [ ] **Rate limiting / abuse protection** on auth and write endpoints; bot protection on public forms.
- [ ] **SEO/meta basics** (if public): title/meta/canonical, Open Graph, `sitemap.xml`, `robots.txt`, structured data where relevant.
- [ ] **DB safety**: connection pooling sized; critical queries indexed; backups running with a tested restore.
- [ ] **CI gate**: build/lint/test + dependency CVE scan block merge; preview deploy per PR.

## P2 — Hardening

- [ ] Image/font optimization (responsive images, modern formats, `font-display`); bundle analyzed, code-split, tree-shaken.
- [ ] CSP tightened to nonces/hashes; Subresource Integrity on third-party scripts; dependency `audit` clean of high/critical.
- [ ] Idempotency keys on money/side-effecting endpoints; webhooks verify signatures and are replay-safe.
- [ ] Feature flags / kill switches for risky features; staged/canary rollout for high-traffic changes.
- [ ] SLOs defined for key journeys; dashboards + error-budget policy; runbook for top incidents.
- [ ] Data retention & PII handling documented; consent/cookie banner if required by jurisdiction.

## P3 — Post-launch / backlog (track; never blocks)

- [ ] Visual-regression and a11y checks in CI; synthetic monitoring of critical journeys.
- [ ] Load/stress test to expected peak ×N; capacity & cost review.
- [ ] Edge/SSR/ISR rendering strategy reviewed per route; cache-invalidation strategy documented.
- [ ] Multi-region / failover posture reviewed if availability targets require it.

## How to use

**When:** before a production launch, before a major release, and in the quarterly readiness review.
**Who:** `production-readiness-auditor` leads; `security-auditor`, `performance-engineer`,
`accessibility-auditor`, `reliability-engineer`, and `devops-engineer` own their sections.
**Command:** `/web-readiness` runs this checklist; `/web-audit <scope>` exercises individual sections.
P0 blocks launch; P1 generates tracked issues; P2–P3 are backlog. Never mark an item passed without
real evidence (a command output, a header dump, a Lighthouse/axe run).

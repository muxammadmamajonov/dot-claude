# Web Checklist

Passing this gate proves the web application is secure over the wire, meets Core Web Vitals thresholds, is correctly indexed by search engines, passes cross-browser smoke tests, and has no mixed-content or header-misconfiguration issues blocking production readiness. Severity tiers: P0=blocker, P1=important (fix shortly after launch), P2=hardening, P3=post-launch / backlog (track and revisit; never blocks shipping).

## P0 — Blockers (must pass before proceeding / launch)

- [ ] HTTPS is enforced on all origins: HTTP redirects to HTTPS with a permanent 301; `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload` is present on all HTTPS responses and the domain is submitted to the HSTS preload list.
- [ ] No mixed-content warnings exist: every sub-resource (scripts, stylesheets, images, fonts, iframes, WebSockets, API calls) is loaded over HTTPS; `upgrade-insecure-requests` CSP directive is set as a secondary defense.
- [ ] Content Security Policy (CSP) is deployed as an HTTP response header (not meta-tag-only): no `unsafe-eval`; no bare wildcard (`*`) in `script-src`; policy is tested with [csp-evaluator.withgoogle.com](https://csp-evaluator.withgoogle.com); violations are captured via `report-uri` or `report-to` endpoint.
- [ ] Security headers are present on all HTML responses and verified with securityheaders.com or equivalent: `X-Content-Type-Options: nosniff`; `X-Frame-Options: DENY` or `SAMEORIGIN` (or `frame-ancestors` CSP directive); `Referrer-Policy: strict-origin-when-cross-origin`; `Permissions-Policy` explicitly restricting all unused browser features (camera, microphone, geolocation, payment, etc.).
- [ ] Core Web Vitals pass in field data or lab simulation on the production URL: LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 — measured via Lighthouse CI, PageSpeed Insights, or CrUX dashboard on real traffic.
- [ ] `<meta charset="UTF-8">` and `<meta name="viewport" content="width=device-width, initial-scale=1">` are present on every HTML document; `user-scalable=no` is not used (blocks zoom — accessibility and mobile policy violation).
- [ ] Critical pages render meaningful content with JavaScript disabled (via SSR, static generation, or a noscript fallback) so search-engine crawlers and no-JS users receive indexable content; Googlebot can discover all primary content without JavaScript execution.
- [ ] `robots.txt` is present and correct: staging, preview, and development environments are fully blocked from crawling via `Disallow: /`; production allows crawling of intended pages only; no sensitive admin paths exposed to crawlers.
- [ ] `sitemap.xml` is generated, reflects the current URL structure, excludes 404 and noindex pages, and has been submitted to Google Search Console and Bing Webmaster Tools.
- [ ] All third-party `<script>` and `<link>` tags loaded from external CDNs include Subresource Integrity (SRI) `integrity` and `crossorigin` attributes; any CDN asset that changes frequently uses a versioned URL or is self-hosted.

## P1 — Important (fix before scaling / shortly after launch)

- [ ] Canonical `<link rel="canonical" href="...">` tags are present on every indexable page pointing to the definitive URL; duplicate-content variants (www vs non-www, trailing-slash vs no trailing-slash, `?utm_*` parameters) each 301-redirect to the canonical URL.
- [ ] Unique `<title>` (≤ 60 characters) and `<meta name="description">` (≤ 160 characters) per page; both are descriptive, keyword-relevant, and do not contain the same text repeated across multiple pages.
- [ ] Open Graph tags (`og:title`, `og:description`, `og:image`, `og:url`, `og:type`) and Twitter/X Card tags (`twitter:card`, `twitter:title`, `twitter:image`) present on all shareable pages; OG image ≥ 1200 × 630 px, < 8 MB, and validated in the Facebook Sharing Debugger and Twitter Card Validator.
- [ ] Structured data (JSON-LD) implemented for all primary content types applicable to the product (Article, Product, FAQPage, BreadcrumbList, Event, Organization, etc.) and validated with Google's Rich Results Test; no manual-action penalties in Search Console.
- [ ] Lighthouse CI is integrated into the CI pipeline; the build fails if Performance score < 85, Accessibility score < 90, SEO score < 90, or Best Practices score < 90 on any primary page template.
- [ ] Cross-browser smoke tests (primary task flows: sign-up, core action, checkout) pass on: latest Chrome, latest Firefox, latest Safari (macOS + iOS 17+), and latest Edge — automated via Playwright or BrowserStack on every release.
- [ ] Web fonts are loaded with `font-display: swap` or `font-display: optional`; subset to only the Unicode ranges used; self-hosted or served from a CDN with correct `Cache-Control` and `CORS` headers (`Access-Control-Allow-Origin`); no render-blocking `<link rel="stylesheet">` font loads in `<head>` without preload.
- [ ] `rel="noopener noreferrer"` is set on all `target="_blank"` links to prevent tab-napping; outbound links to untrusted domains are evaluated for `rel="nofollow ugc"` where appropriate.
- [ ] 404 responses return HTTP 404 (not 200 "soft 404"); 5xx error pages return the correct status code; both display a human-readable message, a link back to the homepage, and optionally a search field; they do not expose stack traces or internal paths.
- [ ] Cookie consent mechanism (if required by GDPR, CCPA, ePrivacy, or applicable jurisdiction) fires before any non-essential cookies or tracking pixels are set; consent state is recorded in a first-party cookie and honored across sessions; consent can be withdrawn without refreshing the page.
- [ ] `preconnect` and `dns-prefetch` resource hints are added for every critical third-party origin (analytics, fonts, payment SDK, CDN) to eliminate connection-setup latency on the critical path.
- [ ] Images are served in modern formats (WebP or AVIF with JPEG/PNG fallback), sized to match display dimensions (no 2× oversized images on mobile), and use responsive `srcset` / `sizes` attributes; Largest Contentful Paint image has `fetchpriority="high"` and an explicit `width`/`height` to prevent CLS.

## P2 — Hardening / nice-to-have

- [ ] Service worker implemented (if PWA or offline experience is a product requirement): cache strategy is documented (stale-while-revalidate, cache-first, network-first per asset type); offline mode shows a meaningful UI, not a blank page; `manifest.json` is present with name, `icons` (192 px and 512 px PNG), `theme_color`, and `display: standalone`.
- [ ] Web Vitals field data (LCP, INP, CLS, TTFB, FCP) collected via the `web-vitals` JS library or a Real User Monitoring (RUM) tool (Datadog RUM, Vercel Speed Insights, etc.) and visualized in a dashboard; P75 field values are tracked alongside lab scores.
- [ ] Internationalization implemented with `hreflang` annotations on every page for each language/region variant; locale detection does not rely solely on IP geolocation; a `x-default` hreflang points to the fallback locale.
- [ ] Print stylesheet or `@media print` CSS defined for pages users are likely to print (invoices, reports, confirmation pages, articles); navigation, cookie banners, and ads are hidden in print output.
- [ ] Favicon set is complete: `favicon.ico` at root, `<link rel="icon">` 32 × 32 SVG or PNG, `<link rel="apple-touch-icon">` 180 × 180 PNG, `manifest.json` entries for 192 × 192 and 512 × 512 PNG; tested in Chrome, Safari, and as a pinned tab.
- [ ] Server-sent security scan run (e.g., OWASP ZAP baseline, Mozilla Observatory) and results reviewed; any HIGH findings addressed or accepted with written rationale.
- [ ] HTML is validated against the W3C validator on all primary page templates; no structural errors that could cause inconsistent browser parsing.

## P3 — Post-launch / backlog (track and revisit after launch; never blocks shipping)

- [ ] Real User Monitoring (RUM) field data for LCP, INP, CLS, and TTFB is segmented by device class (low-end Android, mid-range, high-end), connection type (4G, 3G, WiFi), and geographic region; segments falling outside "Good" thresholds are prioritized as separate backlog items with owners.
- [ ] Search Console Core Web Vitals report is reviewed monthly: URL groups with "Needs Improvement" or "Poor" ratings are investigated, root-caused against recent deploys, and resolved within the following sprint.
- [ ] Internationalization and `hreflang` coverage is audited for every new locale added after launch: canonical/hreflang chain is validated with a crawler (Screaming Frog or equivalent), and `x-default` routing is confirmed correct for each new language/region variant.
- [ ] CSP policy is tightened from reporting-only to enforcement mode after 30 days of production `report-uri` data confirms no legitimate sources are blocked; `unsafe-inline` exceptions are eliminated by migrating remaining inline scripts to nonce-based or hash-based allowlisting.
- [ ] Third-party script audit is conducted quarterly: each external script's performance impact (TBT contribution, data transfer, render-blocking) is measured with WebPageTest; scripts whose cost exceeds their value are removed or replaced with self-hosted alternatives.
- [ ] Print and export stylesheets are validated for all newly added page types (invoices, reports, data exports) that users are likely to print or save as PDF; browser print-preview is tested in Chrome and Safari.

## How to use

**Stage:** gate 6 (Audit) before any production deploy; gate 8 (Launch readiness) for the initial launch. LCP/CLS/INP checks should also run in CI via Lighthouse CI on every PR that touches the critical render path.

**Agent:** `.claude/agents/engineering/frontend-engineer.md` owns implementation; `.claude/agents/quality/performance-engineer.md` owns Web Vitals targets; `.claude/agents/quality/security-auditor.md` owns header and CSP configuration; `.claude/agents/quality/accessibility-auditor.md` owns the WCAG subset.

**Skill:** `.claude/skills/web/SKILL.md` for web-specific patterns; `.claude/skills/performance/SKILL.md` for Core Web Vitals optimization; `.claude/skills/security/SKILL.md` for CSP and header configuration; `.claude/skills/devops/SKILL.md` for CI integration of Lighthouse CI and ZAP scans.

**Commands:** `npx lighthouse-ci autorun` (or the `audit-performance` command) runs automated Web Vitals checks; `audit-security` runs header and CSP validation; `audit-production` covers the full checklist. Cross-reference `.claude/checklists/security.md` for cookie flags, SameSite, CORS, and CSRF; `.claude/checklists/accessibility.md` for the full WCAG 2.2 AA matrix; `.claude/checklists/launch.md` as the final go/no-go before DNS cutover. Mark each item `[x]` when verified or `[-]` when waived with written rationale; P0 failures are launch blockers and must be recorded in `.claude/templates/decision-record.md`.

# Ecommerce Preset

## Project type

Online retail systems for selling physical or digital goods to consumers or businesses. Common variants:

- **Direct-to-consumer (DTC) store** — brand sells its own products; custom storefront; Shopify or headless commerce.
- **Multi-brand / department store** — curated catalogue from multiple brands; category management; supplier feeds.
- **Digital goods store** — software licenses, ebooks, courses, music, templates; immediate delivery; no inventory or shipping.
- **B2B ecommerce** — bulk ordering, net-30 invoicing, quote flows, customer-specific pricing, ERP integration.
- **Subscription commerce** — recurring physical box, digital subscription, replenishment (consumables).
- **Headless commerce** — decoupled frontend (React/Vue/mobile) over a commerce API (Medusa, Commercetools, Shopify Storefront API).
- **Omnichannel** — unified inventory and order management across web, mobile app, and physical POS.

## Typical use cases

- Fashion, apparel, and accessories retail.
- Consumer electronics and gadgets.
- Food and beverage: CPG, specialty foods, meal kits, wine/spirits.
- Beauty, health, and wellness products.
- Home goods, furniture, and décor.
- Sports, outdoor, and hobby equipment.
- Digital: fonts, stock photos, templates, plugins, SaaS add-ons.
- B2B industrial supplies, office equipment, wholesale.

## Required discovery questions

1. What are you selling? (Physical goods with inventory / digital goods / both.) Are products variable (size, colour, format) or simple SKUs?
2. Who are the buyers? (B2C anonymous guests, registered members, B2B account holders.) What is the expected order volume (orders/day at launch and at 12 months)?
3. Which payment methods must be supported at launch? (Cards via Stripe/Adyen, PayPal, Buy Now Pay Later, bank transfer, COD, regional wallets.) Multi-currency?
4. How is fulfilment handled? (In-house warehouse, 3PL, dropship, print-on-demand, digital delivery.) What shipping carriers and rate calculation logic?
5. What tax obligations exist? (US nexus states, EU VAT OSS, Canada GST/HST, other.) Will you use a tax engine (Avalara, TaxJar, Stripe Tax)?
6. Is this a new build, a migration from an existing platform (Shopify, WooCommerce, Magento), or an extension of an existing codebase?
7. What integrations are required at launch? (ERP, WMS, PIM, email marketing — Klaviyo/Mailchimp, analytics — GA4/Meta Pixel, loyalty programme.)
8. What are the performance requirements? (Peak traffic at product launch or sale event; target page load time; Core Web Vitals targets for SEO.)
9. Are there legal/regulatory requirements? (Age verification for alcohol/tobacco, FDA labelling for supplements, GDPR/CCPA for EU/CA customers, accessibility — WCAG 2.1 AA.)
10. What does success look like in 6 months? (Revenue target, conversion rate, AOV, repeat purchase rate, CAC.)

## Recommended agents

**Core**
- `.claude/agents/core/orchestrator.md` — flow control and gate enforcement.
- `.claude/agents/core/product-manager.md` — catalogue, funnel, and conversion scope.
- `.claude/agents/core/solution-architect.md` — commerce platform choice, integration architecture, checkout flow.

**Engineering**
- `.claude/agents/engineering/backend-engineer.md` — order management, inventory, payment processing, webhooks.
- `.claude/agents/engineering/frontend-engineer.md` — storefront, product pages, cart, checkout, performance.
- `.claude/agents/engineering/devops-engineer.md` — CDN configuration, image optimisation pipeline, CI/CD.

**Quality**
- `.claude/agents/quality/security-auditor.md` — PCI-DSS scope, injection, session fixation, card data handling.
- `.claude/agents/quality/performance-engineer.md` — Core Web Vitals, image delivery, edge caching, peak load.
- `.claude/agents/quality/accessibility-auditor.md` — WCAG 2.1 AA; checkout must be fully keyboard-navigable.
- `.claude/agents/quality/qa-engineer.md` — order lifecycle, payment failure paths, inventory edge cases.
- `.claude/agents/quality/privacy-compliance-auditor.md` — GDPR/CCPA consent, cookie banner, data retention.

**Domain**
- `.claude/agents/domain/ecommerce-domain-expert.md` — catalogue modelling, promotions engine, fulfilment integration, returns.

## Recommended skills

- `.claude/skills/backend/SKILL.md` — order state machine, idempotent payment capture, webhook handlers.
- `.claude/skills/security/SKILL.md` — PCI-DSS scope reduction, OWASP, secrets, fraud signals.
- `.claude/skills/performance/SKILL.md` — CDN, image optimisation, lazy loading, edge caching, CWV.
- `.claude/skills/ui-ux-design/SKILL.md` — conversion-optimised product pages, frictionless checkout.
- `.claude/skills/data-modeling/SKILL.md` — product catalogue, variants, inventory, orders, promotions schema.
- `.claude/skills/devops/SKILL.md` — zero-downtime deploys, environment promotion, feature flags for A/B.
- `.claude/skills/testing/SKILL.md` — end-to-end checkout tests, payment sandbox, inventory concurrency tests.
- `.claude/skills/production-readiness/SKILL.md` — uptime during peak sales, runbooks for payment outage.

## Recommended stack options

| Stack | Rationale |
|-------|-----------|
| **Shopify + Hydrogen (Remix) + Shopify Payments** | Fastest to launch for DTC; battle-tested at scale; Shopify handles PCI, fraud, and fulfilment integrations; Hydrogen for headless performance. See `.claude/stack-matrix/backend.md`. |
| **Medusa.js + Next.js + Stripe + PostgreSQL** | Open-source, self-hosted commerce engine; full control over data and customisation; strong for brands outgrowing Shopify limits or needing complex B2B logic. |
| **WooCommerce + WordPress + Stripe/PayPal** | Best for content-heavy stores where SEO and editorial workflows matter; huge plugin ecosystem; lowest cost to launch for small catalogues. |
| **Commercetools + Next.js + Adyen** | Enterprise headless; API-first composable commerce; suits large catalogues, multi-region, and omnichannel with complex pricing rules. |

## Required checklists

- `.claude/checklists/security.md` — extend with: PCI-DSS scope documented (prefer hosted payment fields to stay out of scope), no card data touches your servers, CSRF protection on checkout, bot and card-testing protection (rate limit, CAPTCHA).
- `.claude/checklists/performance.md` — extend with: Largest Contentful Paint < 2.5 s on mobile 3G, product images served via CDN in next-gen formats (WebP/AVIF), category page tested with full catalogue size.
- `.claude/checklists/accessibility.md` — extend with: checkout flow keyboard-navigable, error messages announced to screen readers, colour contrast AA on all CTAs.
- `.claude/checklists/qa.md` — extend with: full order lifecycle tested (place → confirm → fulfil → ship → deliver → return/refund), payment decline paths handled gracefully, inventory oversell scenario tested.
- `.claude/checklists/production.md` — extend with: peak-load plan for sale events (auto-scaling or CDN static fallback), payment provider status page monitored, order confirmation emails tested end-to-end.

## MVP scope pattern

**In the first cut:**
- Product catalogue with variants (size, colour); single currency; simple flat-rate or carrier-calculated shipping.
- Guest checkout + optional account creation post-purchase.
- Card payment via Stripe or Shopify Payments (hosted fields — stay out of PCI scope).
- Order confirmation email; basic order status page.
- Inventory tracking: decrement on order, restore on cancellation.
- Admin panel: product CRUD, order list, basic fulfilment status update.
- Simple promotion: discount code with percentage or fixed-amount off.
- Basic analytics: GA4 + purchase event tracking.

**Deferred to later:**
- Loyalty / points programme.
- Product reviews and UGC.
- Advanced promotions engine (tiered discounts, bundle deals, free gift with purchase).
- Subscription / replenishment.
- Multi-currency and international tax (EU VAT OSS, US nexus).
- ERP / WMS integration.
- Personalisation and recommendation engine.
- Mobile app (start with a PWA or responsive web).
- B2B features (net terms, quote flow, account pricing).
- Abandoned cart recovery (add after baseline conversion is measured).

## Production risks

| Risk | Priority | Notes |
|------|----------|-------|
| Payment capture not idempotent — double-charge on retry | P0 | Use Stripe idempotency keys on every charge; store charge ID before acknowledging order; handle webhook events with deduplication. |
| Inventory oversell during high-traffic sale events | P0 | Use database-level locking or atomic decrement on inventory; test concurrent checkout under load before sale events. |
| Card data touching your servers (PCI scope expansion) | P0 | Use hosted payment fields (Stripe Elements, Shopify Payments) — never handle raw card numbers. |
| Order confirmation email not sent on payment success | P1 | Trigger email from payment webhook (not from checkout page); retry on failure; monitor email delivery rate. |
| No fraud detection — high chargeback rate | P1 | Enable Stripe Radar or equivalent; block high-risk signals; review chargeback rate weekly. |
| Product images not optimised — slow mobile LCP | P1 | Serve via image CDN (Cloudinary, imgix, Next.js Image); enforce WebP/AVIF; lazy-load below-the-fold images. |
| Tax calculation wrong — under-collection liability | P1 | Use a tax engine (Stripe Tax, TaxJar, Avalara) from day one if selling across US states or into EU; do not hand-code tax rates. |
| No rate limiting on checkout — card-testing attacks | P1 | Rate-limit checkout and payment endpoints by IP; require CAPTCHA after N failures; monitor for card-testing spikes. |
| Checkout inaccessible to keyboard/screen-reader users | P1 | Run full WCAG 2.1 AA audit on checkout flow before launch; keyboard-only test is mandatory. |
| No rollback plan if payment provider goes down during peak sale | P2 | Document: how to switch payment methods, how to take orders with deferred payment, comms to customers. |
| Missing cookie consent banner — GDPR fine risk | P2 | Cookie consent management before launch for EU traffic; map all third-party tracking pixels. |

## Launch requirements

- End-to-end order flow tested in payment sandbox: place order, receive confirmation email, admin sees order, inventory decrements.
- Payment failure path graceful: customer sees clear error, no charge applied, inventory not decremented.
- PCI-DSS scope documented; hosted payment fields confirmed; no card data in logs.
- Product images served via CDN; LCP < 2.5 s measured on mobile 3G equivalent.
- Checkout keyboard-navigable; screen-reader tested on add-to-cart, checkout, and confirmation.
- GDPR/CCPA cookie consent in place; privacy policy and terms live.
- Tax calculation verified for all target markets.
- Fraud rules configured in payment provider; card-testing rate limiting active.
- Error monitoring active; alert on checkout error rate > baseline.
- Load test run at 2× expected peak concurrent users; no inventory race conditions observed.
- Runbook for: payment provider outage, inventory data corruption, accidental price error on live product.

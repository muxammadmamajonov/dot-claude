# Two-Sided Marketplace Preset

## Project type

Platforms that connect two distinct user groups — supply and demand — and facilitate transactions between them. Common variants:

- **Product marketplace** — buyers purchase physical or digital goods from multiple sellers (eBay, Etsy, Amazon 3P).
- **Service marketplace** — clients hire freelancers, contractors, or professionals (Upwork, Fiverr, Thumbtack).
- **Rental / sharing marketplace** — hosts list assets for short-term use; guests book (Airbnb, Turo, Spinlister).
- **B2B marketplace** — businesses buy from verified suppliers; procurement workflows, net terms, bulk pricing.
- **Gig / on-demand marketplace** — real-time matching, GPS-tracked fulfilment (Uber, DoorDash, TaskRabbit).
- **Vertical marketplace** — deep domain focus with bespoke trust signals (legal, medical, education, finance professionals).
- **Reverse marketplace** — buyers post requests; sellers bid or apply (staffing, custom manufacturing, RFQs).

## Typical use cases

- Freelance talent platforms (design, engineering, writing, legal, finance).
- Short-term rental of property, vehicles, or equipment.
- Local services (cleaning, repairs, tutoring, pet care).
- Digital asset marketplaces (stock photos, fonts, themes, audio, NFTs).
- Wholesale / B2B supply platforms.
- Professional services with regulated credentials (lawyers, doctors, accountants).
- Event ticketing (primary + resale).

## Required discovery questions

1. Who are the two sides? What does each side want to achieve? Is either side also using the other (e.g. drivers who also ride)?
2. What is the unit of transaction? (Physical good, digital file, time-block, project, task, subscription seat.) How is it priced — fixed, bid/ask, negotiated, or dynamic?
3. What is the platform's revenue model? (Take-rate % on GMV, listing fee, subscription for supply side, lead fee, SaaS + marketplace hybrid.) What is the target take rate?
4. How are payments handled? (Platform collects and splits, or peer-to-peer with platform fee.) Is escrow required — hold funds until work/delivery is confirmed?
5. How is supply onboarded and quality-controlled? (Self-serve listing, manual review, credential verification, background check, licensing.) Who bears liability if supply is fraudulent?
6. How are disputes resolved? (Self-service refund, mediation, arbitration, chargeback escalation.) What is the dispute SLA?
7. What trust and safety mechanisms are required? (Identity verification, rating/review system, insurance, buyer/seller protection policy.)
8. What is the cold-start strategy? Will you manually seed supply, geo-fence to one city/category, or partner with existing supply aggregators?
9. Are there regulatory requirements specific to the supply side? (Professional licensing, background checks, insurance minimums, local operating permits — e.g. STR regulations, taxi/TNC licences.)
10. What does liquidity look like at launch, and what triggers the "marketplace is working" signal? (Minimum listings per category, fill rate, time-to-first-transaction.)

## Recommended agents

**Core**
- `.claude/agents/core/orchestrator.md` — flow control and gate enforcement.
- `.claude/agents/core/product-manager.md` — liquidity strategy, trust mechanics, fee model.
- `.claude/agents/core/solution-architect.md` — payment split architecture, search/matching, notification system.
- `.claude/agents/core/requirements-engineer.md` — transaction lifecycle invariants, dispute state machine.

**Engineering**
- `.claude/agents/engineering/backend-engineer.md` — listings, search, booking/order engine, payment split, webhooks.
- `.claude/agents/engineering/frontend-engineer.md` — dual-persona UX (buyer and seller dashboards), search/filter, messaging.
- `.claude/agents/engineering/devops-engineer.md` — CI/CD, search index management, notification delivery pipelines.

**Quality**
- `.claude/agents/quality/security-auditor.md` — payment flow integrity, identity data handling, fraud vectors.
- `.claude/agents/quality/privacy-compliance-auditor.md` — PII for both sides, KYC data retention, GDPR/CCPA.
- `.claude/agents/quality/qa-engineer.md` — transaction lifecycle end-to-end, concurrent booking conflicts, payout edge cases.
- `.claude/agents/quality/production-readiness-auditor.md` — fraud monitoring, payout failure alerting, SLA runbooks.
- `.claude/agents/quality/performance-engineer.md` — search latency, listing page load, real-time availability checks.

**Domain**
- `.claude/agents/domain/marketplace-domain-expert.md` — liquidity mechanics, trust and safety, payment split patterns, escrow design.

## Recommended skills

- `.claude/skills/backend/SKILL.md` — booking engine, idempotent payment split, payout scheduling, webhook handlers.
- `.claude/skills/security/SKILL.md` — fraud signals, identity verification integration, PII handling, payment data scope.
- `.claude/skills/data-modeling/SKILL.md` — listings, availability/calendar, transactions, reviews, escrow ledger.
- `.claude/skills/performance/SKILL.md` — full-text and geo search, availability query optimisation, CDN for listing images.
- `.claude/skills/ui-ux-design/SKILL.md` — dual-persona onboarding, trust indicators, review UI, messaging UX.
- `.claude/skills/devops/SKILL.md` — feature flags for trust experiments, zero-downtime schema migrations.
- `.claude/skills/testing/SKILL.md` — concurrent booking race condition tests, payout idempotency tests.
- `.claude/skills/production-readiness/SKILL.md` — GMV monitoring, fraud rate alerting, payout failure runbooks.

## Recommended stack options

| Stack | Rationale |
|-------|-----------|
| **Next.js + Node.js + PostgreSQL + Stripe Connect + Elasticsearch** | Stripe Connect handles payment split, escrow, and payouts natively; Elasticsearch for listing search with geo and facets; Next.js for fast SEO-indexable listing pages. See `.claude/stack-matrix/backend.md`. |
| **Rails + PostgreSQL + Stripe Connect + Algolia** | Rapid iteration; strong convention for transactional apps; Algolia for instant search with geo-filtering; Stripe Connect for split payments. |
| **FastAPI + PostgreSQL + Stripe Connect + Meilisearch** | Python suits ML-powered matching and recommendations; Meilisearch self-hosted for search sovereignty; FastAPI for high-throughput booking API. |
| **Node.js (NestJS) + PostgreSQL + Adyen MarketPay + Typesense** | Adyen MarketPay for enterprise-grade split payments with richer compliance controls; Typesense for open-source faceted search. |

## Required checklists

- `.claude/checklists/security.md` — extend with: KYC/identity data encrypted at rest, payment split amounts validated server-side (never trust client), seller payout bank details verified, fraud signals logged and monitored.
- `.claude/checklists/qa.md` — extend with: concurrent booking of same slot tested (only one succeeds), payout idempotency tested (duplicate webhook does not double-pay), dispute state machine fully exercised.
- `.claude/checklists/production.md` — extend with: GMV and take-rate dashboard live, payout failure alert active, fraud rate baseline established, dispute queue monitored.
- `.claude/checklists/performance.md` — extend with: search latency < 200 ms at P95, listing page LCP < 2.5 s, availability check < 100 ms under concurrent load.

## MVP scope pattern

**In the first cut:**
- One supply category, one geography or vertical.
- Seller onboarding: self-serve listing creation with photos, description, price, and availability calendar.
- Buyer flow: search (keyword + basic filter), listing detail, booking/purchase, payment via Stripe Connect.
- Escrow-lite: Stripe captures funds at booking; releases to seller after confirmation window (e.g. 24–48 h after service/delivery).
- Flat platform fee (percentage of transaction) deducted from seller payout automatically.
- Simple ratings: buyer rates seller after transaction completes; seller can rate buyer.
- Basic trust signals: email-verified accounts; ID verification stub (real KYC deferred).
- Messaging: in-platform thread between buyer and seller, scoped to a transaction.
- Admin panel: user list, transaction list, dispute flag, manual payout release.

**Deferred to later:**
- Real-time availability and instant booking (start with request-to-book).
- Background checks and professional licence verification.
- Seller subscription tiers (featured listing, promoted placement).
- Advanced search: geo radius, availability-aware facets, ML ranking.
- Buyer and seller protection insurance programme.
- Dispute mediation workflow beyond manual admin action.
- Mobile apps (start with responsive web).
- Referral and affiliate programme.
- B2B invoicing, net terms, and procurement workflows.
- International expansion: multi-currency, local payment methods, VAT/GST.

## Production risks

| Risk | Priority | Notes |
|------|----------|-------|
| Concurrent booking double-booking the same slot | P0 | Use database-level locking or optimistic concurrency on availability records; test with parallel requests in CI. |
| Payment split computed client-side — manipulable | P0 | Always compute platform fee and seller payout server-side from the canonical listing price; reject mismatched client amounts. |
| Funds released before service/delivery confirmed — chargeback exposure | P0 | Hold in escrow via Stripe Connect `on_behalf_of` with delayed transfer; release only after buyer confirmation or auto-release timeout. |
| Seller payout to wrong bank account (account takeover) | P0 | Require re-authentication before changing payout bank details; send notification to old address; delay payout 24 h after bank detail change. |
| No fraud detection — stolen cards fund fake seller payouts | P0 | Enable Stripe Radar; monitor velocity of new accounts + first transaction + payout within N hours; hold new-seller first payout for manual review. |
| KYC/PII data breach — identity documents exposed | P0 | Store KYC documents only via third-party KYC provider (Stripe Identity, Persona, Jumio); do not store document images in your own storage. |
| Cold-start liquidity — buyers find no supply, leave and never return | P1 | Solve in product strategy before engineering; geo-fence or category-fence MVP; seed supply manually if needed. |
| Review manipulation — fake 5-star reviews on new sellers | P1 | Only allow reviews from verified completed transactions; flag review velocity anomalies; moderate flagged reviews. |
| Payout failure leaving sellers unpaid — trust loss | P1 | Alert on payout failures within 1 h; retry logic with exponential backoff; manual intervention runbook; communicate to seller proactively. |
| Regulatory non-compliance — unlicensed professionals listed | P1 | Define licence verification requirements per category in product spec; block listing creation in regulated categories without verified credential. |
| Search returns stale or unavailable listings | P2 | Sync availability index on every booking event; show real-time availability check on listing page before booking CTA. |
| Messaging used to take transactions off-platform — fee circumvention | P2 | Monitor for phone/email patterns in messages; show policy warning; for high-risk verticals, consider structured booking flow only. |

## Launch requirements

- Concurrent booking race condition tested and confirmed safe under parallel load.
- Payment split, fee deduction, and escrow release tested end-to-end in Stripe Connect test mode for all lifecycle events (capture, release, refund, dispute).
- Seller payout tested: funds reach seller bank account in sandbox; payout delay after bank-detail change enforced.
- KYC/identity data flows through third-party provider; no document images in platform storage.
- Fraud rules configured; new-seller first-payout manual review queue operational.
- Search returns results with correct availability; stale listing scenario tested.
- Review system only accepts input from completed transactions; confirmed in automated test.
- Admin dispute queue accessible; manual payout release and refund flows tested.
- GMV, take-rate, and payout failure dashboards live in production.
- Legal: terms of service cover buyer protection policy, seller payout terms, and prohibited items/services; reviewed by counsel.
- Privacy policy covers KYC data retention and deletion; GDPR/CCPA consent in place for applicable markets.
- Runbook documented for: double-booking incident, payout batch failure, fraudulent seller identified post-payout.

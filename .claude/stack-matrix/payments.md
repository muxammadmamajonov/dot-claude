# Payments Stack Matrix

Choose a payment provider based on: geography (where your customers pay), business model (one-time, subscription, marketplace), required payment methods (cards, wallets, bank transfers, local methods), and compliance burden you're willing to own. No single provider wins globally — regional coverage is the most common reason to use more than one. Always design payment flows to be provider-agnostic at the service layer so you can swap or add providers without rewriting business logic.

Key decision drivers: supported countries and currencies, fee structure, PCI scope reduction, webhook reliability, fraud tooling, and developer experience.

---

## Stripe

- **When to use:** Default choice for SaaS, subscriptions, marketplaces, and any product primarily serving North America, Europe, and Australia. Excellent developer experience and the broadest API surface in the industry.
- **When NOT to use:** Markets where Stripe isn't available or has limited local payment method support (e.g., India, most of Southeast Asia, sub-Saharan Africa). High-volume enterprises that can negotiate better interchange rates with an acquirer directly.
- **Strengths:** Best-in-class API and documentation; Stripe Billing handles subscription lifecycle (trials, upgrades, proration, dunning); Stripe Connect for marketplace/split payments; Stripe Radar for ML-based fraud; native support for 135+ currencies and 40+ payment methods; webhooks are reliable and well-documented; extensive SDKs for web, mobile, and server.
- **Weaknesses:** 2.9% + $0.30 per transaction is expensive at scale; Stripe Connect fees add up for marketplace platforms; limited support for local payment methods in LATAM, SEA, and Africa; account holds and reserves can freeze funds without warning for new businesses.
- **Team fit:** Any team size. Especially productive for small teams: Stripe handles PCI compliance, fraud, and subscription lifecycle so you don't have to build it.
- **Scale fit:** Handles millions of transactions per day; above ~$1M monthly volume, negotiate custom rates.
- **Production risks:** Webhook idempotency — process each event exactly once (store event IDs). Stripe account holds. Hardcoded price IDs in code that drift from Stripe dashboard state.

---

## PayPal

- **When to use:** Consumer-facing products where buyer trust and PayPal wallet conversion matter; markets where PayPal is a preferred payment method (Germany, Netherlands, US consumers); B2C ecommerce with high cart abandonment concern.
- **When NOT to use:** SaaS/subscription products where Stripe Billing is far superior; developer-first teams who value API quality; products that need complex marketplace flows.
- **Strengths:** 400M+ consumer accounts create trust signal at checkout; PayPal Credit and Pay Later increases conversion; widely accepted for international personal payments; Braintree (PayPal's developer platform) offers a cleaner API.
- **Weaknesses:** API is among the worst in the industry (legacy XML, inconsistent REST); checkout UX redirects users off your site (hurts conversion); frequent account holds and dispute resolution is opaque; webhook reliability is poor; poor subscription management compared to Stripe.
- **Team fit:** Non-technical founders/operators who want a familiar brand. Avoid for developer-led teams building complex payment flows.
- **Scale fit:** Handles high volume but operational issues (holds, chargebacks) become more painful at scale.
- **Production risks:** IPN (webhook) delivery failures; account holds freezing entire balance; PayPal disputes often favor buyers regardless of evidence.

---

## Adyen

- **When to use:** Enterprise and high-volume merchants (typically $10M+ annual revenue) operating across multiple geographies who need a single acquirer with global direct connections, sophisticated risk tooling, and in-person (POS) payments alongside online.
- **When NOT to use:** Startups and SMBs — minimum monthly fees and integration complexity are prohibitive. Projects that need rapid prototyping; Adyen's onboarding takes weeks.
- **Strengths:** Single platform for online, mobile, and in-store payments globally; direct card scheme connections (lower interchange); built-in issuing capabilities; strong local payment method coverage in Europe, APAC, and LATAM; best-in-class authorization rate optimization; dedicated account management.
- **Weaknesses:** High integration complexity; minimum processing volumes required; revenue share / interchange++ pricing requires finance expertise to evaluate; documentation is thorough but dense; no free tier or sandbox that's truly instant.
- **Team fit:** Dedicated payments engineer or team; enterprise with payment operations function.
- **Scale fit:** Designed for large merchants processing billions per year; the more you process, the better the unit economics.
- **Production risks:** Misconfigured risk rules blocking legitimate transactions; interchange++ pricing surprises; multi-currency settlement reconciliation complexity.

---

## Braintree

- **When to use:** Teams that want PayPal's ecosystem (PayPal, Venmo in the US) alongside card payments but with a cleaner API than PayPal direct; direct competitors to Stripe for card-first flows.
- **When NOT to use:** Projects that need advanced subscription management or billing automation — Stripe Billing is significantly better. Teams outside the US where Braintree's payment method coverage is thinner.
- **Strengths:** Owned by PayPal so includes PayPal and Venmo as payment methods alongside cards; Drop-in UI reduces PCI scope; vault tokenization; no monthly fees; competitive interchange for US merchants.
- **Weaknesses:** Less feature-rich than Stripe for subscriptions and marketplace payouts; slower product velocity than Stripe; smaller ecosystem of plugins and integrations; documentation quality is below Stripe's standard.
- **Team fit:** US-focused ecommerce or marketplaces where PayPal/Venmo are important alongside cards.
- **Scale fit:** Handles enterprise volume (owned by a Fortune 500 company); used by Uber, Airbnb historically.
- **Production risks:** PayPal account holds affecting Braintree settlement; limited local payment methods outside US/EU.

---

## Square

- **When to use:** SMBs with a physical retail or restaurant presence that want unified in-person (POS hardware) and online payments from one provider. Especially strong for food and beverage, retail, and appointment-based businesses.
- **When NOT to use:** Pure digital products, SaaS, or marketplaces; projects needing international payment methods; teams that need advanced API customization.
- **Strengths:** Best-in-class POS hardware ecosystem; Square for Restaurants and Retail offer vertical-specific POS software; free card reader for in-person; simple flat-rate pricing (2.6% + $0.10 in-person); integrated inventory, payroll, and CRM tools for SMBs.
- **Weaknesses:** US-centric (limited to US, Canada, UK, Australia, Japan); weak API for complex online payment flows; not suitable for marketplaces; limited subscription management; payment processing is only competitive for low-volume merchants.
- **Team fit:** Non-technical business owners; product teams building on top of Square's ecosystem for brick-and-mortar verticals.
- **Scale fit:** Suitable up to mid-market retail volume; above $2M annual in-person volume, dedicated POS/acquirer solutions may be more cost-effective.
- **Production risks:** Square account holds; limited webhook event types for complex online flows.

---

## Mercado Pago (LATAM)

- **When to use:** Products targeting Brazil, Argentina, Mexico, Colombia, Chile, and other LATAM markets. Mercado Pago is the dominant payment infrastructure in LATAM, with local payment methods (PIX, Boleto, OXXO, PSE) that global providers don't support natively.
- **When NOT to use:** Outside LATAM — there is no reason to use Mercado Pago in North America or Europe.
- **Strengths:** Market-leader in LATAM (backed by MercadoLibre); PIX (Brazil instant payment) and Boleto support; installment payments (parcelamento) which are culturally expected in Brazil; cash payment via convenience stores (OXXO in Mexico); local acquiring improves authorization rates.
- **Weaknesses:** API quality and documentation are inconsistent; English documentation is incomplete; webhook reliability varies by market; integration complexity is higher than Stripe; regulatory compliance varies by country.
- **Team fit:** Teams with LATAM market focus; benefit from a local technical resource familiar with LATAM payment quirks.
- **Scale fit:** Scales to enterprise LATAM volume; large merchants should evaluate direct PIX integration and local acquirer agreements.
- **Production risks:** PIX instant payment reversibility edge cases; Boleto has 1-3 day settlement delay; installment plan logic needs careful accounting treatment.

---

## Razorpay (India)

- **When to use:** Products operating in India. Razorpay is the leading payment gateway for Indian startups and enterprises, with the broadest local payment method coverage (UPI, NetBanking, Wallets, EMI, NACH for recurring).
- **When NOT to use:** Outside India — Razorpay does not support international markets. For purely international card payments from Indian businesses, consider Stripe India or Cashfree.
- **Strengths:** UPI integration (India's dominant payment rail, 10B+ monthly transactions); support for all major Indian wallets (Paytm, PhonePe); NACH for bank mandate-based recurring payments; RBI-compliant tokenization; Razorpay Subscriptions for recurring billing; strong developer experience for the Indian market.
- **Weaknesses:** India-only; UPI payment success rates vary by bank; RBI regulatory changes affect product features with little warning; customer support slower than Stripe at scale.
- **Team fit:** Any team targeting the Indian market. Razorpay's documentation is good and SDKs cover all major frameworks.
- **Scale fit:** Used by Indian unicorns; handles millions of daily transactions.
- **Production risks:** UPI payment pending state requires polling or webhook handling; RBI mandated recurring payment changes (e-mandates, AFA) require compliance updates.

---

## Paystack (Africa)

- **When to use:** Products targeting Nigeria, Ghana, Kenya, South Africa, and other sub-Saharan African markets. Now owned by Stripe, Paystack provides local card, bank transfer, and mobile money support in Africa.
- **When NOT to use:** Outside Africa; markets where M-Pesa direct integration (via Safaricom API) is preferred over an aggregator.
- **Strengths:** Best developer experience in African fintech; supports local bank transfers, mobile money (M-Pesa), and cards; strong webhook reliability; growing market coverage across Africa; Stripe ownership means improving infrastructure.
- **Weaknesses:** Coverage limited to a subset of African countries; mobile money coverage varies by country; documentation gaps for some markets; FX settlement for USD payouts adds complexity.
- **Team fit:** Developer teams building for African consumers; pairs well with Stripe for teams that need global + Africa coverage under one SDK philosophy.
- **Scale fit:** Handles high transaction volumes in supported markets; enterprise contracts available.
- **Production risks:** Bank transfer confirmation delays; mobile money USSD sessions time out if user doesn't respond; compliance requirements differ by country.

---

## One-Time vs Subscription vs Marketplace Payment Models

**One-time payments:** Simplest model. Charge on purchase, issue receipt, fulfill. Works with any provider. Key concerns: refund policy, chargeback rate, failed payment handling.

**Subscription / recurring:** Use Stripe Billing, Razorpay Subscriptions, or Recurly as a billing layer on top of the payment provider. Key concerns: dunning (failed payment retries), proration on plan changes, trial period logic, invoice generation, tax compliance (VAT/GST via Stripe Tax or TaxJar), and cancellation flows.

**Marketplace / split payments:** Funds flow from buyer → platform → seller. Use Stripe Connect (Express or Custom accounts), Adyen for Platforms, or Mangopay. Key concerns: KYC/KYB for payees (regulatory requirement), payout schedules, platform fee retention, refund responsibility, and cross-border tax withholding.

---

## Comparison Table

| Provider | Geography | Card | Local methods | Subscriptions | Marketplace | Dev experience | Fee model |
|---|---|---|---|---|---|---|---|
| Stripe | Global (60+ countries) | Yes | 40+ | Excellent (Billing) | Yes (Connect) | Best in class | 2.9% + $0.30 |
| PayPal | Global | Yes | PayPal, Venmo | Basic | Limited | Poor | 3.49% + fixed |
| Adyen | Global (enterprise) | Yes | 250+ | Basic | Yes (Platforms) | Good (complex) | Interchange++ |
| Braintree | US, EU focused | Yes | PayPal, Venmo | Limited | Basic | Good | 2.59% + $0.49 |
| Square | US, CA, UK, AU, JP | Yes | In-person | Basic | No | Good (POS) | 2.6% + $0.10 |
| Mercado Pago | LATAM | Yes | PIX, Boleto, OXXO | Basic | Yes | Fair | Varies by country |
| Razorpay | India | Yes | UPI, Wallets, NACH | Good | Basic | Good | 2% + GST |
| Paystack | Africa (subset) | Yes | Bank transfer, M-Pesa | Basic | No | Good | 1.5% + ₦100 |

---

## Recommended Combinations

- **Global SaaS (subscriptions):** Stripe Billing + Stripe Tax — handles the full subscription lifecycle, proration, and VAT/GST globally with minimal code.
- **Global + LATAM expansion:** Stripe (primary) + Mercado Pago (LATAM) — route by billing address country; abstract behind a PaymentService interface in your backend.
- **Global + India expansion:** Stripe (primary) + Razorpay (India) — UPI is non-negotiable for India conversion rates; Stripe India has limited UPI support.
- **Marketplace / platform:** Stripe Connect (Custom) — worth the complexity for the payout control; use Express accounts for simpler seller onboarding.
- **Enterprise multi-region:** Adyen — single acquirer for all geographies, better interchange at scale, POS + online unified.
- **Brick-and-mortar SMB:** Square POS + Square Online — unified inventory and payment reporting across in-person and online without integration work.
- **African consumer app:** Paystack + Stripe (for international cards) — Paystack for local rails, Stripe for cross-border.

Cross-reference: `.claude/checklists/security.md` for PCI-DSS scope considerations, `.claude/templates/architecture.md` for abstracting the payment provider behind a service interface to enable multi-provider routing.

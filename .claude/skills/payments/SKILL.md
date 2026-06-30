---
name: payments
description: Use when integrating a payment provider (Stripe, Adyen, PayPal, Square, Braintree, regional PSPs), implementing checkout flows, subscriptions, invoicing, webhooks, refunds, disputes, reconciliation, or reducing PCI scope. Triggers on any task that handles money movement, billing, or card data — including design (to scope PCI/SCA obligations), build (provider SDK wiring), and audit (compliance gate). Also activates for regional payment methods (iDEAL, SEPA, PIX, UPI, Alipay, Klarna, Afterpay).
---

# Payments & Billing

## When to use
- Selecting or integrating a payment provider (Stripe, Adyen, PayPal, Square, Braintree, Razorpay, Mercado Pago, regional PSPs).
- Building checkout: one-time charges, saved cards, guest vs. authenticated, 3DS/SCA, buy-now-pay-later.
- Implementing subscription billing: plans, trials, metered usage, proration, dunning, grace periods, reactivation.
- Implementing invoicing, tax calculation (Stripe Tax, Avalara, TaxJar), coupons, promotions.
- Wiring payment webhooks with idempotency and retry safety.
- Implementing refunds, disputes/chargebacks, and partial captures.
- Reconciling provider payouts with internal ledger; handling failed payouts.
- Reducing PCI DSS scope; meeting SCA/3DS2 requirements for EU/UK.
- Supporting regional/alternative payment methods (iDEAL, SEPA Direct Debit, ACH, PIX, UPI, Alipay, WeChat Pay, BNPL).

Applies to web, mobile (native + webview), backend APIs, platforms (SaaS, marketplace, e-commerce), and internal billing tools.

---

## Workflow

### Phase 1 — Scope & Compliance First

**1. Classify the payment use case.**
Determine: one-time vs. recurring, platform (collect on behalf of others?) vs. direct, B2C vs. B2B, geographies and currencies, required alternative payment methods. A marketplace collecting on behalf of sellers is fundamentally different from a SaaS billing its own customers — provider features and contract structures differ.

**2. Assess PCI scope and SCA obligations.**
- Use a provider-hosted payment element (Stripe Elements / PaymentElement, Adyen Drop-in, Braintree Hosted Fields) to keep card data out of your servers and reach **PCI DSS SAQ A** (the lowest scope). Never accept raw card numbers server-side unless you have a full PCI ROC.
- For EU/UK transactions, 3DS2/SCA is mandatory for most consumer card transactions. Use a provider that handles SCA authentication automatically (Stripe's PaymentIntents API, Adyen's 3DS2 server, etc.).
- Classify card data sensitivity: PANs must never appear in logs, analytics, error messages, or client-side JS outside the secure iframe.

**3. Choose the provider and integration model.**
Consult `.claude/stack-matrix/payments.md`. Key decision axes: global coverage, split-pay/connect for marketplaces, SCA support, local payment methods, contract/pricing model, and SDK maturity for your platform. Document the choice via `.claude/templates/decision-record.md`.

---

### Phase 2 — Design the Payment Model

**4. Design the data model before writing code.**
Minimum entities for any payment integration:

```
Customer          → maps your user to provider customer ID (idempotent creation)
PaymentMethod     → stored card/bank/wallet token (never raw PAN)
Order / Cart      → what is being purchased, amounts, tax, currency
PaymentIntent     → one payment attempt lifecycle (created → processing → succeeded / failed)
Subscription      → recurring plan: plan_id, status, current_period, trial, cancel_at
Invoice           → line items, amounts, tax, due date, status
Refund            → linked to PaymentIntent, amount, reason, status
WebhookEvent      → idempotency_key, provider_event_id, type, payload, processed_at, status
```

Record in `docs/specs/payment-data-model.md` using `.claude/templates/data-model.md`. Include the currency precision rule: store all amounts as integers in the smallest currency unit (cents, pence, øre). Never float.

**5. Map the happy path and every failure path.**
Draw out: checkout initiation → payment intent creation → 3DS challenge (if required) → webhook confirmation → order fulfillment. Then map: declined card, 3DS failure, network timeout, duplicate submission, refund requested, dispute opened, payout failed. Each failure path needs a defined user-facing message, a retry policy, and an idempotency strategy.

**6. Design webhook processing as a queue, not a synchronous handler.**
Webhooks must be: (a) received and immediately ACKed with HTTP 200, (b) stored in a webhook_events table with the raw payload and idempotency key, (c) processed asynchronously by a worker, (d) idempotent — running the same event twice must be safe. See Standards.

---

### Phase 3 — Implement

**7. Implement server-side PaymentIntent / charge creation.**
- Always create the PaymentIntent server-side, never client-side. The client only confirms.
- Pass `idempotency_key` on every mutating API call (use order ID + attempt number, or a UUID stored with the order). Stripe, Adyen, and Braintree all support this header.
- Set `capture_method: manual` if you need to authorize now and capture after fulfillment (physical goods, reservations).
- For subscriptions, use the provider's subscription API (Stripe Subscriptions + Invoices, Adyen Recurring) rather than rolling your own. Provider handles dunning, retry logic, and SCA re-authentication.

**8. Implement the client-side payment UI.**
- Embed the provider's hosted element (Stripe PaymentElement, Adyen Drop-in) inside your checkout UI. This element handles card input, 3DS flow, and APM rendering without your page ever touching raw card data.
- On confirmation, the client calls `stripe.confirmPayment()` (or equivalent), which handles the 3DS redirect and returns a result. Your client then polls your backend for order status — never trust client-side confirmation alone; always confirm via webhook.

**9. Implement webhook handler.**
```
POST /webhooks/stripe  (or /webhooks/adyen etc.)
  1. Verify signature (Stripe-Signature header / HMAC)
  2. Insert into webhook_events (event_id, type, payload) ON CONFLICT DO NOTHING
  3. Return 200 immediately
  (worker) Process event by type:
    payment_intent.succeeded → fulfill order
    payment_intent.payment_failed → update order, notify user
    invoice.payment_failed → dunning flow
    charge.dispute.created → alert ops, freeze fulfillment if needed
    customer.subscription.deleted → revoke access
```

**10. Implement refunds and disputes.**
- Refunds are always initiated server-side via the provider API. Partial refunds require tracking refunded amount on the order.
- Store dispute metadata; chargebacks can arrive months after payment. Do not delete order/payment records based on data-retention policies that would prevent dispute evidence submission.
- Wire `charge.dispute.created` webhook to alert ops within minutes.

**11. Implement reconciliation.**
- Daily/hourly: fetch provider payout reports (Stripe Sigma, Adyen Settlement Detail Report) and reconcile against your internal order/payment records.
- Check: amount transferred = sum(succeeded charges) - fees - refunds - disputes for that payout window. Any gap is a bug or fraud signal.
- Store provider fee per transaction to enable margin analysis.

---

### Phase 4 — Harden & Audit

**12. Run the payment security checklist (cross-ref `.claude/checklists/security.md`).**
- Webhook signature verification in place and tested.
- No card data in logs, analytics, Sentry, or error messages.
- Idempotency key on every mutating provider API call.
- Provider API key in secret manager, not in code or `.env` committed to VCS.
- Test mode vs. live mode keys are different; only live keys are in production secrets.
- Stripe Radar / Adyen fraud rules configured.
- Amount mismatch validation: confirm server-side that the amount on the PaymentIntent matches your order total before fulfilling.

**13. Test in the provider's sandbox using test card suites.**
Test: success, generic decline, insufficient funds, 3DS required, 3DS failed, network error, duplicate idempotency key, refund, partial refund, dispute. For subscriptions: trial end, invoice payment, failed renewal, dunning retry, cancellation, reactivation.

---

## Standards

**Do:**
- Store amounts as integer cents/smallest-unit. Convert to display format only in the UI layer. Use a `Money` value object or dedicated library (dinero.js, py-moneyed) for arithmetic to avoid float rounding.
- Verify webhook signatures on every inbound event. Reject without a valid signature.
- Use idempotency keys on all mutating provider API calls; include the attempt number if supporting retries.
- Fulfill orders only after receiving the `payment_intent.succeeded` (or equivalent) webhook — never on client-side confirmation alone.
- Keep provider keys in a secret manager (AWS Secrets Manager, Vault, Doppler); rotate on suspected exposure.
- Use `HTTPS` everywhere, enforce TLS 1.2+ on webhook endpoints.
- Handle `402`, `429` (rate limit), `500`-range provider errors: retry with exponential backoff, log the error with the provider's request ID.
- Scope PCI surface to provider-hosted fields only (SAQ A). If you ever need to accept raw card data, engage a qualified security assessor.
- Support 3DS2/SCA for EU/UK from day one — retrofitting later is expensive.
- Test cancellations, refunds, and failed charges in staging before every release that touches billing.

**Do not:**
- Log, store, or transmit PANs, CVVs, or full card numbers. Not in application logs, analytics events, Sentry breadcrumbs, or support tickets.
- Trust the client's reported payment status — always confirm server-side via webhook.
- Use floating-point numbers for monetary amounts anywhere in the stack.
- Retry webhook processing without idempotency guards (double-fulfillment risk).
- Use test API keys in production or production keys in test/staging.
- Hard-code prices or amounts client-side where they could be tampered; validate server-side.
- Roll your own recurring billing logic (dunning, proration) when the provider offers it.
- Delete payment or order records while a chargeback window is still open (typically 120 days for Visa/Mastercard, 180 for Amex).

---

## Common mistakes to avoid

- **Double-fulfillment**: processing `payment_intent.succeeded` twice because the worker isn't idempotent. Fix: `INSERT ... ON CONFLICT DO NOTHING` on `webhook_events.event_id`, process only once.
- **Trusting client redirect**: fulfilling an order because the browser returned to the success URL — not because the webhook confirmed. Redirects can be spoofed.
- **Currency mismatch**: creating a PaymentIntent for `$10.00` but storing `10.00` (float) in the database, then comparing to `1000` cents. Use one canonical representation.
- **Missing SCA handling for saved cards**: off-session payments (subscription renewals, saved-card reuse) require `setup_future_usage: off_session` during initial setup and proper handling of `requires_action` on renewal.
- **Webhook secret not verified**: skipping signature verification because "we'll add it later" — this allows anyone to send fake fulfillment events.
- **Provider rate limits in refund storms**: bulk refund flows hit rate limits. Implement a queue with back-pressure.
- **No payout reconciliation**: assuming the provider deposits exactly what you expect. Fees, disputes, and processing errors cause discrepancies; catch them daily.
- **Tax not collected correctly**: treating price as inclusive of tax everywhere vs. exclusive in some jurisdictions. Use a tax calculation service (Stripe Tax, Avalara) rather than hard-coding rates.

---

## Output format

Primary deliverables:
- **Payment integration spec**: `docs/specs/payment-integration.md` (use `.claude/templates/feature-spec.md` + data model section from `.claude/templates/data-model.md`). Cover: provider choice rationale, data model, event flow diagrams, PCI scope decision, SCA strategy, webhook contract, reconciliation approach, test plan.
- **Decision record**: `docs/decisions/payment-provider-<name>.md` (use `.claude/templates/decision-record.md`).
- **Runbook** for payment incidents (webhook processing failures, payout failures, dispute surges): `docs/runbooks/payments.md` (use `.claude/templates/runbook.md`).

Supporting code artifacts (in the project source):
- Server-side payment service (PaymentIntent creation, webhook handling, refunds) with idempotency.
- Webhook event table migration + idempotent worker.
- Reconciliation job/script.
- Test suite covering all card scenarios.

---

## Related checklists
- `.claude/checklists/security.md` — webhook signature verification, secrets, PCI surface.
- `.claude/checklists/production.md` — payment keys in secret manager, monitoring on failed payments.
- `.claude/checklists/qa.md` — payment test coverage (success, decline, 3DS, refund, dispute, dunning).

## Related agents
- `.claude/agents/engineering/payments-engineer.md` — primary implementation owner.
- `.claude/agents/quality/security-auditor.md` — PCI scope review, webhook security, secret management.
- `.claude/agents/quality/production-readiness-auditor.md` — reconciliation, alerting on payment failures.
- `.claude/agents/domain/fintech-domain-expert.md` — regulatory nuances, regional payment methods, compliance.
- `.claude/agents/domain/ecommerce-domain-expert.md` — checkout UX, cart abandonment, refund policies.

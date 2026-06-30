# Booking Preset

## Project type

Software products that allow users to reserve a time slot, seat, resource, or service in advance, managing availability, scheduling, and confirmations. Common variants:

- **Appointment scheduling** — 1:1 or small-group bookings with a professional (doctor, therapist, consultant, tutor, stylist); calendar sync; reminders; cancellation/rescheduling.
- **Activity and experience booking** — tours, classes, workshops, escape rooms, sports courts; capacity-based inventory; group bookings; waivers.
- **Hospitality / accommodation** — hotel, vacation rental, hostel, glamping; nightly rates with date-range availability; channel manager integration (Airbnb, Booking.com, OTAs).
- **Restaurant / table reservation** — party-size and time-slot management; waitlist; POS integration; dietary notes.
- **Event ticketing** — concerts, conferences, sporting events; seating maps; tiered ticket types; barcode/QR entry.
- **Transportation / seat reservation** — bus, ferry, train, charter; seat map; passenger manifest; boarding passes.
- **Space and resource booking** — meeting rooms, co-working desks, equipment, vehicles; often internal enterprise tool.
- **Marketplace booking platform** — multi-vendor; each provider manages their own availability; platform collects fee on transaction.
- **Subscription / recurring appointment** — weekly fitness class, monthly cleaning service; recurring billing; easy skip/reschedule.

## Typical use cases

- Medical practice offering online appointment booking with provider-specific availability and insurance capture.
- Yoga studio managing class schedules, waitlists, memberships, and per-class drop-in purchases.
- Vacation rental owner listing a property with nightly pricing, availability calendar, and instant-book.
- Conference platform selling tiered tickets (general admission, VIP, speaker) with a seating map.
- Co-working space letting members book hot desks and meeting rooms by the hour.
- Multi-location hair salon franchise with per-stylist availability, service menu, and deposit collection.
- Tour operator offering group and private experiences with capacity limits and dynamic seasonal pricing.

## Required discovery questions

1. What is being booked, and who provides it? (A professional's time, a physical space, a seat in a class/event, a rental property.) Is there one provider or a marketplace of many? What is the unit of inventory — time slot, seat, night, item?
2. What does the availability model look like? (Provider sets hours/blackouts, slots are fixed vs. dynamic, capacity is per-slot vs. total-inventory, overbooking allowed with waitlist, real-time vs. periodic sync.) How far in advance can bookings be made, and what is the cancellation/reschedule policy?
3. What payment model is required at launch? (Full payment at booking, deposit + balance at service, pay-at-venue, subscription/membership with unlimited or credit-based access, split payment for groups.) Which processor (Stripe, PayPal, regional)? Refund rules?
4. How many providers/resources are in scope at launch, and what is the 12-month target? This drives the multi-tenancy and calendar-sync complexity.
5. What calendar and scheduling integrations are required? (Google Calendar, Outlook/Exchange, Apple Calendar for two-way sync; iCal feed export; provider app for managing their own calendar.)
6. What notification and reminder strategy is needed? (Email confirmation, SMS reminder N hours before, calendar invite attachment, no-show follow-up, rebooking prompt.) What happens if a provider cancels — who is notified and how?
7. Are there regulatory or industry-specific requirements? (HIPAA if booking medical appointments with PHI, PCI-DSS for card data, GDPR/CCPA for customer data, age verification, waiver/consent capture before certain activities, local business licensing disclosure.)
8. What does the customer experience look like for groups? (One person books for multiple attendees, each attendee may need their own profile, split payment, per-attendee forms or waivers.)
9. What channel management or third-party listing integrations are required? (Airbnb, Booking.com, Google Reserve, Mindbody, ClassPass, OpenTable, Fareharbor.) These require two-way availability sync and can be complex.
10. What metrics define success? (Booking conversion rate, no-show rate, utilisation rate of available slots, revenue per available slot, repeat-booking rate, provider satisfaction.)

## Recommended agents

**Core**
- `.claude/agents/core/orchestrator.md` — flow control and gate enforcement.
- `.claude/agents/core/product-manager.md` — booking funnel optimisation, cancellation policy design, notification strategy.
- `.claude/agents/core/solution-architect.md` — availability engine design, calendar sync architecture, payment flow.
- `.claude/agents/core/requirements-engineer.md` — availability invariants, concurrency rules, refund policy edge cases.

**Engineering**
- `.claude/agents/engineering/backend-engineer.md` — availability engine, booking state machine, payment integration, calendar sync, notifications.
- `.claude/agents/engineering/frontend-engineer.md` — booking widget, availability calendar UI, checkout, confirmation flow, provider dashboard.
- `.claude/agents/engineering/mobile-engineer.md` — consumer booking app, provider schedule management app, push notifications.
- `.claude/agents/engineering/integration-engineer.md` — Google/Outlook calendar sync, OTA channel manager, third-party marketplace APIs.
- `.claude/agents/engineering/realtime-engineer.md` — live slot availability during checkout (prevent double-booking race), waitlist promotion.
- `.claude/agents/engineering/payments-engineer.md` — deposit + balance collection, marketplace split payments, refund automation, subscription billing.

**Quality**
- `.claude/agents/quality/qa-engineer.md` — double-booking race conditions, cancellation/refund edge cases, calendar sync conflicts, payment failure paths.
- `.claude/agents/quality/security-auditor.md` — PCI-DSS scope, PII in booking records, HIPAA if medical context, provider credential isolation.
- `.claude/agents/quality/privacy-compliance-auditor.md` — GDPR/CCPA for customer booking data, retention schedules, right-to-erasure for past bookings.
- `.claude/agents/quality/performance-engineer.md` — availability query latency, checkout concurrency, calendar sync throughput.
- `.claude/agents/quality/accessibility-auditor.md` — WCAG 2.1 AA for booking widget; date picker keyboard navigation; form accessibility.

**Domain**
- `.claude/agents/domain/booking-domain-expert.md` — availability engine patterns, channel manager protocols, no-show management, yield/pricing models, waiver capture.

## Recommended skills

- `.claude/skills/backend/SKILL.md` — booking state machine, pessimistic/optimistic locking for slot reservation, idempotent payment capture.
- `.claude/skills/data-modeling/SKILL.md` — availability slot schema, booking/attendee hierarchy, provider calendar model, pricing rule tables.
- `.claude/skills/api-design/SKILL.md` — availability query API design, webhook events for booking lifecycle, calendar sync protocol.
- `.claude/skills/security/SKILL.md` — PCI-DSS scope for card capture, PII in booking records, provider data isolation.
- `.claude/skills/testing/SKILL.md` — concurrent booking race-condition tests, calendar sync conflict tests, payment failure and refund path tests.
- `.claude/skills/performance/SKILL.md` — availability query optimisation (date-range indexes), checkout lock timeout tuning, calendar sync batching.
- `.claude/skills/devops/SKILL.md` — scheduled reminder jobs, calendar sync background workers, auto-scaling for event on-sale traffic spikes.
- `.claude/skills/mobile/SKILL.md` — native date/time picker UX, push notification for reminders, provider schedule management on mobile.

## Recommended stack options

| Stack | Rationale |
|-------|-----------|
| **Next.js + Node.js (NestJS) + PostgreSQL + Stripe + Google Calendar API** | Full-stack TypeScript; Postgres handles date-range availability queries and pessimistic slot locking; Stripe covers payment, deposits, refunds, and Connect for marketplace payouts; Google Calendar API for two-way sync. See `.claude/stack-matrix/web.md`, `.claude/stack-matrix/backend.md`, `.claude/stack-matrix/payments.md`. |
| **React + Django (Python) + PostgreSQL + Stripe + Celery** | Django's mature ORM handles complex availability queries; Celery manages reminder emails, calendar sync jobs, and async payment capture; good choice when provider-facing admin needs rapid iteration. See `.claude/stack-matrix/backend.md`. |
| **React Native + Node.js + PostgreSQL + Stripe** | Mobile-first consumer booking (fitness, beauty, health) where app-store presence is a competitive requirement; React Native shares logic across iOS and Android; push notifications for reminders and provider alerts. See `.claude/stack-matrix/mobile.md`. |
| **Headless (Next.js) + Supabase + Stripe** | Fastest path for a focused single-provider or small-team booking tool; Supabase real-time subscriptions power live slot availability updates; Row Level Security isolates provider data; good for an MVP that may grow into a marketplace. See `.claude/stack-matrix/database.md`, `.claude/stack-matrix/backend.md`. |

## Required checklists

- `.claude/checklists/security.md` — extend with: no card data stored by the application (delegate entirely to Stripe/processor); booking records containing PII encrypted at rest; provider accounts isolated (provider A cannot read provider B's bookings); HIPAA safeguards if any medical appointment data is captured.
- `.claude/checklists/qa.md` — extend with: concurrent booking test — two users attempting the last slot simultaneously results in exactly one confirmed booking and one graceful rejection; cancellation refund calculated correctly for all policy tiers (full refund, partial, non-refundable); reminder job fires at correct time for all timezone configurations; calendar sync conflict (provider blocks time after customer books) handled without silent data loss.
- `.claude/checklists/production.md` — extend with: availability query P99 latency within 500 ms under load; reminder job monitored and alerted if delayed; double-booking alert if invariant is violated in production; provider onboarding flow tested end-to-end before any real provider is live.
- `.claude/checklists/accessibility.md` — extend with: date-picker fully keyboard-operable and screen-reader-announced; time-zone selection clearly labelled; booking confirmation readable without colour cues; form error messages associated with their inputs via aria-describedby.

## MVP scope pattern

**In the first cut:**
- Single provider or single resource type; no marketplace complexity.
- Fixed-duration time slots; no variable-length or multi-resource booking.
- Availability calendar showing open/booked slots; customer selects slot, enters contact details, pays, receives confirmation email.
- Full payment at booking via Stripe Checkout; no deposit/balance split yet.
- Provider dashboard: view upcoming bookings, block time, manually cancel with automated customer notification.
- Email confirmation and one reminder (24 hours before); no SMS yet.
- Cancellation policy enforced: customer cancels → refund calculated and issued via Stripe; provider cancels → full refund + apology email.
- iCal export for customer and provider (no two-way sync yet — reduces OAuth and conflict-resolution complexity).
- Booking state machine: pending\_payment → confirmed → completed / cancelled / no\_show.

**Deferred to later:**
- Two-way Google/Outlook calendar sync (OAuth complexity and conflict resolution; add when providers demand it).
- Marketplace multi-provider (adds tenancy, payout splits, and discovery features; validate single-provider first).
- Waitlist with automatic promotion (useful but complex; add when no-show rate data justifies it).
- OTA / channel manager integration (Airbnb, Booking.com — high effort; add when distribution channel is validated).
- Dynamic/yield pricing (revenue-management complexity; start with fixed rates).
- SMS reminders (add Twilio/Vonage after email reminders are proven; increases cost and compliance scope).
- Group booking with per-attendee forms and split payment (complex checkout; add when group bookings are a validated use case).
- Subscription / membership passes (recurring billing adds complexity; add after single-booking revenue is stable).
- Seating map for events (significant frontend investment; required for assigned-seat events, defer for general-admission MVP).

## Production risks

| Risk | Priority | Notes |
|------|----------|-------|
| Double-booking: two customers confirmed for the same slot | P0 | Pessimistic lock on slot row during checkout; database-level unique constraint on (resource_id, start_time, status=confirmed); load-test with concurrent booking requests before launch. |
| Payment captured but booking not confirmed — customer charged with no reservation | P0 | Idempotency key on Stripe PaymentIntent; booking state transitions only on Stripe webhook confirmation, not on client redirect; reconciliation job detects orphaned charges daily. |
| Refund not issued on provider cancellation — customer payment stranded | P0 | Provider cancellation flow triggers Stripe refund atomically; refund failure surfaces to admin queue; customer notified of refund status regardless of Stripe outcome. |
| Reminder job silent failure — customers miss appointment, blame platform | P1 | Reminder job monitored with a heartbeat; alert if job does not run within scheduled window; dead-letter queue for failed sends with retry; log delivery status per booking. |
| Calendar sync conflict: provider blocks time already booked by a customer | P1 | Detect conflict on sync and surface to provider dashboard rather than silently cancelling the booking; provider must explicitly cancel (triggering refund); never auto-cancel confirmed bookings. |
| Timezone mismatch — appointment shown to customer in wrong timezone | P1 | Store all times in UTC; convert to customer's local timezone only at display; send calendar invite with explicit TZID; test booking across DST boundary and across international timezones. |
| Provider data isolation breach — booking records from one provider visible to another | P1 | Row-level security or application-layer tenant scoping on all provider queries; automated cross-provider isolation test in CI. |
| Checkout availability stale — customer selects a slot that was just taken | P1 | Re-validate slot availability server-side at payment confirmation, not just at slot selection; return a clear "slot no longer available" error with redirect to reschedule. |
| On-sale traffic spike for a popular event overwhelms availability queries | P2 | Load test at 10× normal concurrency; queue checkout requests under extreme load rather than returning errors; database read replica for availability queries. |
| No-show rate high, providers lose revenue with no recourse | P2 | No-show policy (forfeit deposit) enforced automatically; provider can mark no-show within a time window after appointment; no-show rate visible in provider analytics. |

## Launch requirements

- Double-booking invariant verified: load test with 50 concurrent requests for the same last slot produces exactly one confirmation and 49 graceful rejections.
- Payment-booking atomicity verified: Stripe webhook handler tested with delayed delivery, duplicate delivery, and out-of-order events; booking state remains consistent in all cases.
- Cancellation and refund flows tested end-to-end for all policy tiers (full, partial, non-refundable) and for both customer-initiated and provider-initiated cancellation.
- Reminder job fires at correct time tested across at least three timezones including one with DST; monitoring alert configured for job delay.
- Provider data isolation confirmed by automated test: authenticated provider A cannot retrieve bookings, availability, or customer data belonging to provider B.
- Timezone handling verified: booking made in UTC-8 displays correctly for a customer in UTC+5:30; calendar invite has correct TZID.
- Availability query P99 latency within 500 ms under expected launch concurrency.
- Stripe webhook endpoint verified with Stripe CLI event replay for all booking lifecycle events.
- Privacy policy live; cookie/consent banner in place for EU customers; data-retention schedule defined and documented.
- WCAG 2.1 AA accessibility verified on booking widget: date picker, time selector, checkout form, and confirmation page all keyboard-navigable and screen-reader-announced.
- Error monitoring active; alerts fire on booking failure rate spike, payment error threshold, and reminder job delay.
- Provider onboarding flow tested end-to-end by a real non-technical user before any providers are invited.

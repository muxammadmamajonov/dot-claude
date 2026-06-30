---
name: analytics
description: Use when designing a product analytics system, defining an event taxonomy or tracking plan, integrating an analytics SDK (Segment, Amplitude, Mixpanel, PostHog, GA4), setting up a data warehouse pipeline (BigQuery, Snowflake, Redshift), building dbt models, implementing a consent/privacy layer, or designing A/B experimentation infrastructure. Triggers on any task that involves measuring user behavior, building dashboards, or running experiments.
---

# Product & Data Analytics

**Scope: product/business events & funnels. System health/SLOs → `.claude/skills/observability/SKILL.md`; relevance → `.claude/skills/search/SKILL.md`.**

## When to use
- Designing an event taxonomy and tracking plan for a new product or feature.
- Integrating a client-side or server-side analytics SDK (Segment, Amplitude, Mixpanel, PostHog, RudderStack, GA4, Heap).
- Building or auditing a data warehouse pipeline: raw events → warehouse (BigQuery, Snowflake, Redshift, ClickHouse) → dbt models → BI dashboards.
- Implementing consent management and privacy-safe tracking (GDPR, CCPA, COPPA).
- Designing A/B or multivariate experimentation infrastructure (feature flags, assignment, analysis).
- Building product dashboards, funnels, retention curves, or cohort analyses.
- Auditing tracking coverage: finding gaps where events are missing or definitions are inconsistent.
- Migrating from one analytics provider to another.

Applies to web apps, mobile apps (iOS/Android/React Native/Flutter), backend APIs, AI/agent products, games, and data platforms.

---

## Workflow

### Phase 1 — Define Before You Instrument

**1. Start with business questions, not events.**
Analytics serve decisions. Before defining a single event, list the top 10 business questions the team needs to answer in the next quarter. Examples: "What percentage of sign-ups complete onboarding?", "Which feature correlates with 90-day retention?", "What is the conversion rate from free to paid by acquisition channel?". The event taxonomy exists to answer these questions — not to log everything and figure it out later.

**2. Design the event taxonomy.**
Use a consistent naming convention across the entire product. The most widely adopted pattern:

```
<noun>_<verb>   (snake_case)
  object        → what was acted on
  action        → what happened (past tense)

Examples:
  user_signed_up
  onboarding_step_completed
  feature_enabled
  checkout_started
  payment_succeeded
  subscription_cancelled
  search_performed
  experiment_assigned
```

Document every event in a **tracking plan** (see Output format). Each event entry specifies: event name, trigger description (when it fires), properties (name, type, required/optional, example value), platforms (web/iOS/Android/server), owner (team/squad).

**3. Define a standard property schema.**
Every event carries a base set of properties automatically (via the SDK or middleware):

```
# Identity
anonymous_id      string   pre-auth session identifier
user_id           string   post-auth stable identifier (internal ID, not email)

# Session / context
session_id        string
timestamp         ISO-8601 UTC
timezone          string (IANA)
locale            string (BCP-47)

# Platform
platform          web | ios | android | server
app_version       string (semver)
os_version        string
browser           string (web only)

# Acquisition
utm_source        string
utm_medium        string
utm_campaign      string
referrer          string

# Experiment
active_experiments  array<{experiment_id, variant}>
```

Custom events then add their own properties on top of this base. Never put PII (email, name, phone) in event properties unless it is a deliberate, consent-gated action (e.g., identify call for CRM sync). Use internal IDs everywhere.

**4. Identify PII risks and design the consent layer.**
Map every event property to a PII classification: non-PII, pseudonymous (user_id), or PII (email, name, IP). IP address is PII under GDPR. For EU/UK users, you need consent before firing analytics events to third-party tools. Design this before instrumentation starts:
- Implement a Consent Management Platform (CMP) or use the SDK's built-in consent controls (Segment Consent Manager, PostHog's cookieless mode, GA4 consent mode).
- Server-side tracking reduces browser-level PII exposure and is more resilient to ad blockers.
- If targeting users under 13 (COPPA) or under 16 (GDPR child provisions), analytics must be strictly necessary only.

---

### Phase 2 — Instrument

**5. Choose the instrumentation layer: client-side, server-side, or hybrid.**

| Layer | Use when | Pros | Cons |
|-------|----------|------|------|
| Client-side SDK | Behavioral events (clicks, scroll, form interactions), attribution, session replay | Rich context, low latency | Blocked by ad blockers, PII leakage risk, harder to enforce schema |
| Server-side API | Business events (payment succeeded, account created, subscription changed) | Authoritative, no blockers, enforces schema | No client context (browser, referrer) unless forwarded |
| Hybrid | Most production systems | Best of both | Two code paths to maintain |

Use Segment or RudderStack as the Customer Data Platform (CDP) to route one stream of events to multiple destinations (warehouse, Amplitude, Intercom, CRM) rather than adding multiple SDKs.

**6. Implement tracking plan enforcement.**
Schema drift kills data quality. Enforce it:
- Use TypeScript types or a JSON Schema for each event, generated from the tracking plan. Use Segment Protocols, RudderStack Data Catalog, or Amplitude Data to enforce schemas at ingestion.
- In CI: add a lint step that validates any new `analytics.track()` call against the tracking plan definition. Reject events with unknown names or missing required properties.
- In production: log schema violations to a dead-letter queue; alert on spike in violations.

**7. Instrument using the identify → group → track → page/screen pattern.**
```
// On auth:
analytics.identify(userId, { plan: 'pro', created_at: '...' })

// On org-level context (B2B):
analytics.group(orgId, { name: 'Acme Corp', employee_count: 500 })

// On every meaningful action:
analytics.track('checkout_started', {
  cart_value_cents: 4999,
  item_count: 3,
  currency: 'USD'
})

// On page/screen views (web/mobile):
analytics.page('Checkout', { step: 'address' })
```

Use server-side `identify` and `track` for business events to prevent client-side tampering. The server is the source of truth for conversion and revenue events.

Examples shown in JS/Node; the same patterns apply across platforms — equivalents (mobile, Go, Python, etc.) follow the Standards table.

---

### Phase 3 — Warehouse Pipeline

**8. Design the raw → modeled → serving layer architecture.**
```
Raw events (immutable, append-only)
  └── Segment/RudderStack → warehouse raw schema
        e.g. bigquery.segment_raw.tracks, .pages, .identifies

Staging models (dbt, clean & typed)
  └── stg_users.sql, stg_events.sql, stg_sessions.sql

Mart models (business-oriented)
  └── fct_events.sql          → one row per event
  └── fct_sessions.sql        → sessionized events
  └── dim_users.sql            → user attributes at snapshot
  └── fct_funnel_steps.sql    → funnel analysis
  └── fct_retention_cohorts.sql

BI layer (Looker, Metabase, Superset, Mode)
  └── reads from mart models only
```

Preserve raw events immutably. Never transform in place. dbt transforms are deterministic and re-runnable — if a business logic rule changes, re-run the model rather than patching raw data.

**9. Define sessions and identity stitching.**
Sessions: group events by `anonymous_id` with a 30-minute inactivity timeout (configurable). This requires a sessionization SQL window function in dbt. Sessions that cross auth boundaries (anonymous → identified) must be merged so the full journey is visible.

Identity stitching: when a user signs up, alias their `anonymous_id` to `user_id`. Record this alias event. Your warehouse model must propagate the `user_id` back to pre-signup events for that `anonymous_id`. Without this, sign-up conversion is systematically undercounted.

**10. Implement dbt models with tests.**
Every dbt model must have:
```yaml
# schema.yml
models:
  - name: fct_events
    columns:
      - name: event_id
        tests: [unique, not_null]
      - name: user_id
        tests: [not_null]
      - name: event_name
        tests: [not_null, accepted_values: {values: [...]}]
      - name: event_timestamp
        tests: [not_null]
```

Run `dbt test` in CI. A failing uniqueness test on `event_id` indicates duplicate event delivery — fix the deduplication logic, not the test.

---

### Phase 4 — Experimentation

**11. Design the experiment assignment layer.**
Experiments require: assignment (which variant?), exposure logging (when was the user first assigned?), and analysis (did the variant move the metric?).

- Use a feature flag + experimentation platform: PostHog, LaunchDarkly, Statsig, Optimizely, GrowthBook (open source), or a homegrown feature flag service.
- Assign variants server-side for consistency across platforms and to prevent variant leakage.
- Log an `experiment_assigned` event at first exposure with `{experiment_id, variant, assignment_method}`.
- Enforce one experiment assignment per user per experiment (sticky assignment). If the user's bucket changes mid-experiment, the data is polluted.
- Define the metric (primary + guardrail) and minimum detectable effect **before** launching the experiment. Use a sample size calculator (`statsig.com/calculator`, or `scipy.stats.norm`).

**12. Run analysis correctly.**
- Use the exposure event (not the page view or sign-up) as the experiment entry point. Analyzing users who were never exposed is a common bias.
- Use two-sample t-test (continuous metrics) or z-test for proportions (conversion metrics). Apply Bonferroni correction if testing multiple metrics.
- Do not peek at results and stop early when p < 0.05 — this inflates false positives. Use sequential testing (CUPED, mSPRT) if you need early stopping guarantees.
- Run experiments for at least one full business cycle (typically 2 weeks) to avoid day-of-week effects.

---

## Standards

**Do:**
- Define the tracking plan in a versioned document before writing any instrumentation code. Treat it like a schema migration.
- Use server-side events for all business-critical conversions (payment, sign-up, subscription). Client-side events are supplementary.
- Enforce the event schema in CI and at ingestion time. Reject or quarantine events that fail validation.
- Store raw events immutably. Model in dbt; never transform raw tables.
- Use internal user IDs in events, never email addresses. Resolve to PII only in controlled, consented contexts.
- Version your dbt models and run `dbt test` in CI.
- Document every metric definition: numerator, denominator, filter, time window. "DAU" is ambiguous without this.
- Set data retention policies: raw events 12–24 months hot, archive thereafter. PII-bearing tables have shorter retention + right-to-erasure procedures.

**Do not:**
- Put PII (email, phone, full name, IP) in general event properties without explicit consent and a documented retention policy.
- Instrument without a tracking plan — "log everything and figure it out later" produces unmaintainable, contradictory data.
- Create events named `button_clicked` without a noun — `checkout_button_clicked` vs `nav_menu_button_clicked` are different events with different semantics.
- Add high-cardinality identifiers (order IDs, session UUIDs) as properties on high-volume events if the warehouse bill is a concern — use them on low-volume business events only. (For metric-label cardinality in time-series backends, observability owns the guidance: see `.claude/skills/observability/SKILL.md`.)
- Mutate or delete raw event records. Corrections belong in a correction table or a dbt `is_valid` flag.
- Share A/B test results before the experiment has reached statistical significance and the pre-defined minimum sample size.
- Run multiple experiments on the same user population concurrently without interaction analysis.

---

## Common mistakes to avoid

- **Identity fragmentation**: desktop anonymous_id, mobile anonymous_id, and user_id all treated as separate users. Fix: alias calls at sign-up; warehouse-level identity stitching.
- **Conversion undercounting**: counting sign-ups only for users who triggered the server-side event, missing users whose request failed after payment. Fix: log `payment_succeeded` after confirmation, not after client redirect.
- **Schema drift accumulation**: property names change across releases (`user_plan` → `subscription_tier` → `plan_name`). Fix: breaking changes in the tracking plan require a migration ticket and a dbt model update on the same day.
- **Experiment novelty effect**: testing a new UI element sees an inflated conversion in week 1 due to novelty. Fix: run experiments for at least 2 full business cycles; check for novelty decay in daily breakdown.
- **Self-selection bias in cohort analysis**: comparing users who adopted feature X to those who didn't — adopters are inherently more engaged. Fix: use experiment assignment as the causal mechanism, not feature adoption.
- **Warehouse cost explosion**: loading raw events into BigQuery with scan-based pricing and running queries on the full history. Fix: partition on `event_timestamp`; cluster on `event_name`; require partition filters in queries.
- **Missing funnel denominators**: reporting "20% of users completed step 3" when the denominator was anyone who ever visited the page, not users who entered the funnel at step 1. Fix: anchor every funnel to a clearly defined entry event.

---

## Output format

Primary deliverables:
- **Tracking plan**: `docs/specs/tracking-plan.md` — event taxonomy table (event name, trigger, properties, platform, owner), identity strategy, consent layer design, SDK/CDP choice.
- **Data model spec**: `docs/specs/analytics-data-model.md` — warehouse schema layers (raw, staging, mart), dbt model graph, retention policy, identity stitching logic.
- **Experimentation runbook**: `docs/runbooks/experimentation.md` (use `.claude/templates/runbook.md`) — how to create, launch, analyze, and close an experiment; statistical requirements.

Supporting artifacts (in project source):
- Tracking plan enforcement schema (JSON Schema or TypeScript types per event).
- Analytics middleware / wrapper module with base properties injected.
- dbt `schema.yml` with tests for each mart model.
- dbt staging and mart model SQL.
- CI lint step for tracking plan compliance.
- Consent gate implementation (CMP integration or SDK consent controls).

---

## Related checklists
- `.claude/checklists/privacy-compliance.md` — consent layer, PII in events, retention policies, GDPR right-to-erasure, CCPA opt-out.
- `.claude/checklists/production.md` — analytics pipeline health monitoring; alert on event volume drop (missing tracking).
- `.claude/checklists/data-model.md` — warehouse schema design, partitioning, access control.

## Related agents
- `.claude/agents/engineering/data-engineer.md` — warehouse pipeline, dbt models, event ingestion.
- `.claude/agents/engineering/backend-engineer.md` — server-side event instrumentation.
- `.claude/agents/quality/privacy-compliance-auditor.md` — consent design, PII classification, GDPR/CCPA/COPPA review.
- `.claude/agents/core/product-manager.md` — tracking plan ownership, metric definitions, experiment prioritization.
- `.claude/agents/domain/saas-domain-expert.md` — SaaS-specific metrics (MRR, churn, NRR, product-qualified leads).
- `.claude/agents/domain/ecommerce-domain-expert.md` — e-commerce funnels, cart abandonment, GMV tracking.

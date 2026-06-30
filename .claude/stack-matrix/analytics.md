# Analytics Stack Matrix

Choose based on three axes: **who owns the data** (your warehouse vs. vendor-hosted), **what you're measuring** (product behavior vs. marketing attribution vs. business metrics), and **who consumes the results** (engineers vs. product managers vs. executives). A startup validating PMF needs fast event tracking with zero infra; a growth-stage company needs a warehouse-native stack they own forever.

Key drivers: data ownership and portability, event volume and cost at scale, self-serve BI needs, compliance/PII handling, existing data warehouse investment, and team SQL literacy.

---

## PostHog

**When to use**
- Product analytics + session replay + feature flags + A/B testing in one self-hostable platform
- Startups and scale-ups wanting full data ownership (self-host on your infra or EU cloud)
- Engineering-led product teams who want to query raw events in SQL or ClickHouse
- Need to avoid sending user PII to third-party SaaS vendors (GDPR, HIPAA-adjacent workflows)

**When NOT to use**
- Marketing attribution and campaign analytics — PostHog is product-centric, not marketing-centric
- Enterprise BI and cross-source reporting — it's an analytics tool, not a data warehouse
- Teams needing deep cohort analysis with complex multi-touch attribution models out of the box

**Strengths**
- Single platform: funnels, retention, session replay, heatmaps, feature flags, experiments
- Self-hostable (Docker/Kubernetes on your cloud) — full data ownership
- Built on ClickHouse: fast queries on billions of events without sampling
- Generous free tier on PostHog Cloud; no per-seat pricing on most features
- Open source (MIT for core); active community and plugin ecosystem

**Weaknesses**
- Self-hosting ops complexity: ClickHouse cluster management at scale is non-trivial
- Weaker marketing attribution vs. Amplitude or Mixpanel
- Dashboard sharing / executive reporting less polished than dedicated BI tools
- Mobile SDK maturity lags behind Amplitude

**Team fit**
- Engineering-heavy product teams; privacy-conscious companies; B2B SaaS
- CTOs who want to own their data without per-seat SaaS costs

**Scale fit**
- PostHog Cloud: effectively unlimited (ClickHouse backend). Self-hosted: scales with your ClickHouse fleet.

**Risks**
- Self-hosted: you own backups, upgrades, ClickHouse cluster health
- Plugin/CDP ecosystem smaller than Segment/Amplitude

---

## Amplitude

**When to use**
- Consumer or B2C product analytics at scale with non-technical stakeholders
- Need best-in-class funnel analysis, retention cohorts, pathfinder, and behavioral segmentation
- Growth and product teams want self-serve analysis without writing SQL
- Need Amplitude Experiment for server-side feature flag + experiment management

**When NOT to use**
- Cost-sensitive projects: Amplitude scales in price with Monthly Tracked Users (MTUs) — can be very expensive
- Teams needing full raw event data export as first-class feature (available but gated)
- Marketing multi-channel attribution — Amplitude is product-centric
- Data warehouse-first organizations who prefer SQL over a proprietary query UI

**Strengths**
- Best UX for non-technical product managers: drag-and-drop cohorts, pathfinder, impact analysis
- Amplitude Experiment: server-side experiments with statistical significance monitoring
- Data warehouse connections (Amplitude → BigQuery/Snowflake) for power users
- Strong mobile SDKs (iOS, Android, React Native, Flutter)
- Amplitude Analytics AI (Spark): natural language query interface

**Weaknesses**
- MTU-based pricing becomes expensive for consumer apps with large DAUs
- Vendor lock-in: proprietary data model and query interface
- Complex behavioral queries require Amplitude's own formula language (AQL)
- Raw event export costs extra; not a data warehouse replacement

**Team fit**
- Growth, product, and marketing teams in B2C/consumer apps
- Organizations where non-engineers own product analytics

**Scale fit**
- Handles billions of events/month on their infrastructure; pricing pain starts before scale limits

**Risks**
- MTU pricing spikes on viral growth — budget carefully
- Platform dependency: if Amplitude changes pricing or is acquired, migration is painful

---

## Mixpanel

**When to use**
- Event-based product analytics with strong user-level analysis (flows, funnels, segmentation)
- Teams that moved off Google Analytics and want true event tracking with user identity
- Need Mixpanel's Lexicon for governance: centralized event/property definitions across teams
- B2B SaaS: user-level and account-level (group analytics) analysis in one tool

**When NOT to use**
- Need session replay, heatmaps, or feature flags — Mixpanel is pure analytics
- Very high event volume: pricing by events ingested (not MTUs) can spike with high-frequency tracking
- Marketing attribution — Mixpanel is product analytics, not marketing analytics
- Teams wanting SQL/warehouse-native workflow

**Strengths**
- Clean, fast funnel and retention analysis; industry-standard for event-based product analytics
- Group Analytics: B2B account-level metrics alongside user-level
- Lexicon: data governance layer for event schema, definitions, owners
- Warehouse Connectors: sync data to/from BigQuery, Snowflake, Databricks
- Generous free tier (20 M events/month)

**Weaknesses**
- No session replay, heatmaps, or experimentation (need to pair with other tools)
- Pricing per event can surprise teams with high-frequency instrumentation
- Dashboard and visualization layer less powerful than BI tools
- Mobile SDK less actively developed than Amplitude's in recent years

**Team fit**
- Product analysts and PMs at B2B SaaS companies
- Teams wanting clean event governance without a data warehouse

**Scale fit**
- Handles tens of billions of events/month; pricing by event count not users

**Risks**
- Event volume pricing: a poorly instrumented app can generate 10x expected events
- Mixpanel's proprietary query layer limits advanced analysis without raw data export

---

## GA4 (Google Analytics 4)

**When to use**
- Marketing and acquisition analytics: SEO, paid ads, social, email attribution
- E-commerce conversion tracking tied to Google Ads campaigns
- Teams with Google Marketing Platform (Google Ads, Search Console, Display & Video 360)
- Zero-budget projects: free tier is genuinely generous for small-to-mid traffic

**When NOT to use**
- Deep product analytics (funnels, retention, behavioral cohorts) — GA4's UI is poor for this
- Privacy-focused products or EU-regulated companies (GA4 data goes to Google servers; GDPR risk)
- B2B SaaS with server-side events and complex user identity (GA4 is session/cookie-centric)
- Need raw event-level data access without BigQuery export (export requires GA4 360)

**Strengths**
- Free; integrates natively with Google Ads, Search Console, Looker Studio
- BigQuery export (free on GA4) enables SQL analysis of raw hit-level data
- Cross-platform: web + app tracking unified in one property
- Machine learning: predictive audiences, churn probability, purchase propensity

**Weaknesses**
- UI is notoriously poor for product analytics; funnel/path analysis is limited
- Data sampling on free tier for large sites; 360 removes sampling but costs ~$150 k/year
- PII and consent management: GA4 data processed by Google — compliance burden in EU
- Session-based model doesn't map cleanly to event-sourced product analytics
- 14-month data retention on free tier; limited historical analysis

**Team fit**
- Marketing teams managing paid acquisition and SEO; content sites
- E-commerce teams running Google Shopping and Smart Bidding campaigns

**Scale fit**
- No hard limit; sampling becomes an issue on free tier at millions of sessions/month

**Risks**
- GDPR enforcement against GA4 in several EU countries — legal risk in regulated markets
- Google deprecates or restructures products; GA Universal was sunset in 2023

---

## Snowplow

**When to use**
- Data engineering teams building a self-owned behavioral data pipeline
- Need highly structured, schema-validated event tracking (Iglu schema registry)
- Want raw events in your own data warehouse with no vendor lock-in
- Enterprise: complex multi-brand, multi-platform tracking with unified data model

**When NOT to use**
- Teams wanting out-of-the-box dashboards and product analytics UI — Snowplow is a pipeline, not a BI tool
- Startups without a data engineering team — setup and schema governance is non-trivial
- Need product analytics features (funnels, retention) without building them yourself in SQL/BI

**Strengths**
- Events land in YOUR warehouse (Snowflake, BigQuery, Redshift, Databricks, S3)
- Schema validation at collection time — bad events rejected before reaching warehouse
- Iglu Schema Registry: centralized, versioned event schemas across teams
- Open source pipeline (Community Edition) or managed (BDP Cloud/Enterprise)
- Rich enrichments: IP lookups, user agent parsing, campaign attribution, weather, PII pseudonymization

**Weaknesses**
- No built-in BI or product analytics UI — requires dbt + Looker/Metabase/Superset on top
- Significant setup: collectors, enrichers, loaders, schema registry — 2–4 weeks to production
- Schema evolution is rigorous but complex; teams need schema governance discipline
- Community support; enterprise support requires BDP contract

**Team fit**
- Data engineering teams at growth-stage or enterprise companies
- Organizations building a central data product with behavioral data as a core asset

**Scale fit**
- Tens of billions of events/month in production at enterprise customers; pipeline scales with cloud infra

**Risks**
- High upfront investment; wrong for teams that need analytics in days not months
- Schema registry governance becomes bottleneck if ownership not established early

---

## Warehouse-Native (BigQuery + dbt + BI Tool)

**When to use**
- Already have a data warehouse (BigQuery, Snowflake, Redshift, Databricks) as source of truth
- Want analytics on events + product data + revenue + support data in a single SQL model
- Data team is SQL-literate and wants to own metrics definitions in version-controlled dbt models
- Need to combine behavioral data with CRM, billing, and operational data for full customer 360

**When NOT to use**
- No data engineering capacity to build and maintain dbt models and BI dashboards
- Need real-time product analytics with <1-minute latency — warehouse ingestion adds lag
- Product and growth team needs self-serve without SQL literacy
- Small startup without existing warehouse investment

**Strengths**
- Single source of truth: all data in one place, no silos between product/marketing/finance analytics
- Full control over data model, metric definitions, and lineage
- dbt: version-controlled, tested, documented transformations — enterprise-grade data quality
- Choose best-in-class BI: Looker, Metabase, Superset, Lightdash, Evidence.dev
- No per-user pricing from analytics vendor; costs are warehouse compute + BI tool

**Weaknesses**
- Latency: real-time behavioral analytics requires streaming into warehouse (Pub/Sub/Kafka → BigQuery Streaming) — adds complexity
- Cold start: 2–6 months to have reliable, trusted metrics in production
- Product managers need SQL or BI tool training; self-serve analytics is harder to democratize
- No built-in session replay, funnels UI, or feature flags

**Team fit**
- Data-mature companies with dedicated analytics engineers and data team
- B2B SaaS with complex multi-source reporting needs

**Scale fit**
- Effectively unlimited — warehouse scales independently of analytics tooling

**Risks**
- dbt model sprawl: without governance, models become untrusted "metric soup"
- Warehouse costs can exceed SaaS analytics tools at very high query/compute load
- Hiring bottleneck: analytics engineers are expensive and scarce

---

## ClickHouse (self-hosted analytics backend)

**When to use**
- Need sub-second aggregation queries on billions of rows of event/telemetry data
- Building a custom analytics product (multi-tenant SaaS analytics, internal dashboards)
- High-write-throughput event ingestion that PostgreSQL or standard OLAP tools can't handle
- Cost-sensitive at scale: ClickHouse is dramatically cheaper per query than BigQuery/Snowflake at volume

**When NOT to use**
- Need a full product analytics UI — ClickHouse is a database, not an analytics platform
- Small datasets where Postgres OLAP or SQLite would suffice
- Teams without experience running distributed databases (ClickHouse Keeper, replication, sharding)
- Need ACID transactions or complex JOIN-heavy relational queries

**Strengths**
- Fastest columnar database for aggregation queries: 10–1000x faster than row stores on analytics workloads
- Extremely high write throughput: millions of rows/second per node
- SQL-native with extensions: window functions, array functions, approximate aggregations (uniqCombined, quantileTDigest)
- ClickHouse Cloud (managed): removes ops burden; Altinity for managed on AWS/GCP
- PostHog, Plausible, Metabase, Grafana all use ClickHouse as their analytics backend

**Weaknesses**
- Not a product analytics tool — no funnels, cohorts, session replay out of the box
- JOIN performance can be poor for normalized schemas; denormalized wide tables preferred
- Schema changes (ADD COLUMN is fine; DROP, RENAME require care) in distributed mode are complex
- Mutation (UPDATE/DELETE) operations are expensive and async — designed for append-only workloads

**Team fit**
- Backend/data engineers building custom analytics pipelines or products
- Companies that have outgrown their OLAP database and need raw performance

**Scale fit**
- Petabytes of compressed data; hundreds of thousands of QPS on aggregation queries in clusters

**Risks**
- Distributed ClickHouse cluster (ZooKeeper/Keeper) adds significant ops complexity
- Data modeling mistakes (wrong sort keys, missing TTL) are hard to fix without reprocessing

---

## Comparison Table

| Criterion | PostHog | Amplitude | Mixpanel | GA4 | Snowplow | Warehouse-native | ClickHouse |
|---|---|---|---|---|---|---|---|
| **Type** | Product analytics platform | Product analytics platform | Product analytics platform | Marketing analytics | Event pipeline | Analytics layer | Columnar database |
| **Data ownership** | Full (self-host or cloud) | Vendor-hosted | Vendor-hosted | Google-hosted | Full (your warehouse) | Full (your warehouse) | Full (your infra) |
| **Self-serve UI** | Yes | Yes (best-in-class) | Yes | Yes (limited) | No (BI tool required) | Via BI tool | No |
| **Session replay** | Yes | No | No | No | No | No | No |
| **Feature flags / experiments** | Yes | Yes (Experiment) | No | No | No | No | No |
| **Raw data access** | Yes (ClickHouse) | Partial (export) | Partial (export) | BigQuery export (free) | Full (warehouse) | Native | Native |
| **Funnels / retention** | Yes | Excellent | Excellent | Basic | Build in dbt/BI | Build in SQL/BI | Build in SQL |
| **Marketing attribution** | No | Partial | Partial | Excellent | Via enrichments | Yes (combine sources) | No |
| **Pricing model** | Events (free tier generous) | MTU-based | Events-based | Free / 360 enterprise | Volume / managed tier | Warehouse + BI costs | Compute / managed |
| **GDPR / self-host** | Yes (self-host option) | No (vendor-hosted) | No (vendor-hosted) | Risk (Google-hosted) | Yes (full control) | Yes (your cloud) | Yes (your infra) |
| **Setup complexity** | Low–medium | Low | Low | Very low | High | High | High |
| **Best for** | Product + privacy + flags | B2C growth analytics | B2B product analytics | Marketing + SEO | Enterprise event pipeline | Multi-source BI | Custom analytics backend |

---

## Recommended Combinations

| Combination | Why |
|---|---|
| **PostHog (Cloud) + Segment** | PostHog for product analytics + session replay; Segment routes events to PostHog and other destinations without re-instrumentation. |
| **Amplitude + Snowflake (Amplitude Data Export)** | Product analytics UI for PMs; raw events in Snowflake for data team SQL analysis and cross-source joining. |
| **Snowplow + dbt + Looker** | Enterprise self-owned stack: validated event collection, modeled metrics in dbt, governed BI in Looker. |
| **GA4 + BigQuery + Looker Studio** | Free marketing + acquisition analytics with raw data access via BigQuery; Looker Studio for custom dashboards. |
| **ClickHouse + Grafana** | Custom metrics/telemetry dashboards: high-frequency write ingestion, sub-second aggregation, time-series visualization. |
| **PostHog (self-hosted on ClickHouse) + dbt** | Full ownership: PostHog's built-in ClickHouse as analytics source; dbt models for custom metrics on raw event tables. |
| **Mixpanel + Warehouse-native (dbt)** | Mixpanel for PM self-serve funnel/retention; dbt + Snowflake for data team building compound business metrics. |
| **Amplitude + LaunchDarkly** | Amplitude for behavioral analytics; LaunchDarkly for feature flags; connect experiment assignment to Amplitude for impact analysis. |

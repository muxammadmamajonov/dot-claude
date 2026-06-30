# Database Stack Matrix

Choose your database by answering three questions: (1) What is your primary data shape — relational/tabular, document, key-value, or time-series/analytics? (2) What consistency guarantee do you need — ACID, eventual, or tunable? (3) Are you optimizing for developer speed, operational simplicity, or raw query throughput? Most production systems use 2–3 databases for different jobs; do not force one tool to do everything.

Key decision drivers: data model fit, team familiarity, hosting complexity, query patterns (OLTP vs OLAP), vendor lock-in tolerance, and cost at scale.

---

## PostgreSQL

- **When to use:** Primary relational store for any project where correctness matters — SaaS apps, fintech, healthcare, CRM, ERP, marketplaces. The right default when you are unsure.
- **When NOT to use:** Pure key-value caching, write-heavy time-series at petabyte scale, or teams that cannot manage a stateful server.
- **Strengths:** Full ACID, rich SQL (window functions, CTEs, JSON operators), extensions (pgvector, PostGIS, pg_partman), large ecosystem, proven at massive scale (Shopify, GitHub, Notion).
- **Weaknesses:** Vertical scaling hits limits; horizontal sharding is complex without Citus or managed equivalents; replication lag under heavy write load.
- **Team fit:** Any backend team. SQL knowledge is universal; migrations are well-tooled (Flyway, Alembic, Prisma).
- **Scale fit:** Single-node handles tens of millions of rows with proper indexing. Multi-TB with read replicas + partitioning. Citus or Aurora for horizontal.
- **Production risks:** `VACUUM` bloat on high-churn tables; long-running transactions blocking locks; replication slot leaks filling disk.

---

## MySQL / MariaDB

- **When to use:** Existing LAMP stacks, legacy CMS (WordPress, Magento), teams deeply familiar with MySQL, projects where max compatibility with off-the-shelf PHP software is required.
- **When NOT to use:** New greenfield projects (PostgreSQL is objectively more capable); workloads needing advanced JSON, arrays, or window functions; analytical queries.
- **Strengths:** Ubiquitous hosting support, fast for simple read-heavy OLTP, wide shared-hosting availability, InnoDB is solid for transactional workloads.
- **Weaknesses:** Weaker standard SQL compliance (missing `FULL OUTER JOIN`, limited CTE support in older versions), JSON support less ergonomic than PostgreSQL, MariaDB/MySQL feature divergence causes confusion.
- **Team fit:** Teams from PHP/WordPress backgrounds. Newer teams should default to PostgreSQL.
- **Scale fit:** Similar to PostgreSQL for OLTP. PlanetScale (MySQL-compatible) adds horizontal branching/sharding.
- **Production risks:** Silent data truncation (strict mode off by default in older versions); MyISAM tables without transactions; schema migrations lock tables on older engines.

---

## SQLite

- **When to use:** CLI tools, desktop apps, embedded devices, mobile apps (iOS/Android local storage), test fixtures, edge functions where a full server is impossible.
- **When NOT to use:** Multi-writer concurrent servers, distributed systems, any service handling high-concurrent writes (> ~1 writer at a time).
- **Strengths:** Zero operational overhead — one file, no server process. Excellent read concurrency (WAL mode). Ships with every language runtime. Turso/Litestream add replication.
- **Weaknesses:** Single writer at a time (WAL mode mitigates but does not eliminate); no native type enforcement beyond affinity; not suited for large-scale multi-user backends.
- **Team fit:** Any team. Ideal as the embedded database for apps, test suites, or edge compute.
- **Scale fit:** Single process local use. Turso enables lightweight multi-region replicas for edge. Not for high-concurrency SaaS backends.
- **Production risks:** Writes blocked during checkpoint; file corruption risk without proper backup (Litestream mitigates); accidental use in multi-process deployments.

---

## MongoDB

- **When to use:** Flexible/evolving document schemas (catalogs, CMS, event logs), rapid prototyping where schema changes frequently, teams that prefer JSON-native APIs, geospatial workloads.
- **When NOT to use:** Workloads that require multi-document ACID transactions as the primary pattern (use PostgreSQL); reporting/analytics with complex joins; teams comfortable with relational modeling.
- **Strengths:** Schema flexibility without migrations, horizontal sharding native, rich aggregation pipeline, Atlas cloud is mature, change streams for event-driven patterns.
- **Weaknesses:** Multi-document transactions are slower and more complex than PostgreSQL; inconsistent query language vs SQL; data duplication necessary to avoid lookups; Atlas pricing escalates quickly.
- **Team fit:** Node.js teams, mobile backend teams, teams building content platforms or catalog systems.
- **Scale fit:** Sharded clusters scale to petabytes. Atlas handles operations. Self-hosted sharding is complex.
- **Production risks:** Missing indexes on large collections (full collection scans are silent); uncontrolled document growth; oplog window too small for change stream consumers.

---

## Redis

- **When to use:** Caching (query results, sessions, API responses), rate limiting, pub/sub messaging, leaderboards, job queues (BullMQ/Sidekiq), real-time counters.
- **When NOT to use:** Primary durable data store for important business data; large datasets exceeding available RAM budget; complex relational queries.
- **Strengths:** Sub-millisecond latency, rich data structures (sorted sets, streams, bitmaps), Lua scripting, wide client support, Redis Cluster for horizontal scale.
- **Weaknesses:** In-memory means cost scales with dataset size; durability options (RDB/AOF) add latency; eviction policies can silently drop data; not a primary store.
- **Team fit:** All teams benefit from Redis as the caching/queue layer. Minimal learning curve.
- **Scale fit:** Single node handles ~100k ops/sec. Redis Cluster distributes data across nodes. Upstash/Redis Cloud for serverless.
- **Production risks:** `maxmemory` policy evicting unexpectedly; AOF rewrite pausing replication; accidental use as sole source of truth without persistence enabled.

---

## ClickHouse

- **When to use:** Analytical workloads requiring sub-second queries over billions of rows — dashboards, log analytics, product analytics, time-series aggregations, BI backends.
- **When NOT to use:** OLTP (frequent small writes, point lookups by primary key, UPDATE/DELETE-heavy workflows); teams without columnar database experience.
- **Strengths:** Fastest columnar query engine for analytics; extreme compression ratios; vectorized execution; MaterializedViews for pre-aggregation; ClickHouse Cloud simplifies ops.
- **Weaknesses:** Poor at point lookups; mutations (UPDATE/DELETE) are expensive; complex joins are slower than row-stores; no full ACID transactions.
- **Team fit:** Data engineering teams, analytics engineers, teams already using dbt or Airflow. Not ideal as a first database for a generalist team.
- **Scale fit:** Handles petabytes with proper partitioning. Horizontal sharding via distributed tables or ClickHouse Cloud.
- **Production risks:** Wrong sort key (primary key order) destroys query performance; unbounded mutations filling tmp disk; forgetting to set TTL for log retention.

---

## Elasticsearch / OpenSearch

- **When to use:** Full-text search (e-commerce product search, document search, log search), faceted filtering, relevance ranking, observability/log aggregation (with OpenSearch).
- **When NOT to use:** Primary transactional database; exact-match lookups where a DB index suffices; teams unable to manage JVM cluster ops.
- **Strengths:** Best-in-class full-text and fuzzy search, rich aggregation framework, near-real-time indexing, OpenSearch is fully open source (Elastic license is restrictive).
- **Weaknesses:** Operationally heavy (JVM tuning, shard management, snapshot lifecycle); expensive at scale; not ACID; data duplication from primary store.
- **Team fit:** Backend teams with dedicated ops capacity or using managed services (Elastic Cloud, OpenSearch Serverless, Bonsai).
- **Scale fit:** Multi-terabyte search indices with sharding. Managed services abstract shard management.
- **Production risks:** Shard explosion (too many small indices); OOM on JVM heap; mapping explosion from dynamic field detection; cluster yellow/red state from replica failure.

---

## Firebase / Firestore

- **When to use:** Mobile-first apps (iOS/Android) needing real-time sync, offline-first support, and rapid prototyping without backend code; small teams shipping consumer apps fast.
- **When NOT to use:** Complex relational queries, reporting, cost-sensitive projects at scale (pricing is per-read/write), server-side data processing, enterprise apps with strict data residency.
- **Strengths:** Real-time listeners built in, offline SDK, zero server ops, Google authentication integration, generous free tier, rapid prototyping.
- **Weaknesses:** Vendor lock-in (no standard query language), expensive at scale (per-document reads), limited query capabilities (no joins, limited range queries), data modeling must denormalize aggressively.
- **Team fit:** Mobile developers and small startup teams. Not ideal for data engineers or backend teams needing SQL.
- **Scale fit:** Google infrastructure scales automatically but costs grow non-linearly. Optimize reads aggressively.
- **Production risks:** Unexpected bill spikes from fan-out writes; security rules misconfiguration exposing all data; no transactions across collections in older SDK versions.

---

## Supabase

- **When to use:** Projects that want Firebase-like developer experience (real-time, auth, storage, auto-generated REST/GraphQL APIs) but on PostgreSQL with full SQL power and open-source stack.
- **When NOT to use:** Pure mobile offline-first (Firestore has better offline SDKs); teams needing extreme customization of the database layer without Supabase's opinions.
- **Strengths:** Built on PostgreSQL (all PG strengths apply); Realtime subscriptions via logical replication; Row Level Security for auth-integrated data access; edge functions; vector support via pgvector; open source and self-hostable.
- **Weaknesses:** Still maturing (some enterprise features lag Firebase); RLS can be complex to debug; self-hosting has more ops burden than the managed tier.
- **Team fit:** Full-stack JS/TS teams, indie hackers, SaaS startups. Strong Next.js and React Native ecosystem.
- **Scale fit:** Managed tier scales to large PostgreSQL workloads. Self-hosted scales with standard PG tooling.
- **Production risks:** RLS policies with bugs silently expose or hide data; pooler connection limits under heavy load; Realtime channel fan-out at very high subscriber counts.

---

## DynamoDB

- **When to use:** AWS-native applications requiring single-digit millisecond latency at any scale, serverless workloads (Lambda-driven backends), high-traffic key-value/document access patterns, global tables for multi-region.
- **When NOT to use:** Complex queries, ad-hoc analytics, joins, or any access pattern not known at design time; non-AWS environments; teams without NoSQL/DynamoDB experience.
- **Strengths:** Truly serverless (no cluster management), predictable latency at any scale, global tables for active-active multi-region, DynamoDB Streams for event-driven, tight IAM integration.
- **Weaknesses:** Rigid single-table design requirements (high cognitive overhead); no SQL; expensive for read-heavy workloads without DAX caching; migration pain if access patterns change.
- **Team fit:** AWS-specialist backend teams comfortable with single-table design and access pattern modeling upfront.
- **Scale fit:** Unlimited horizontal scale on AWS. Designed for millions of requests per second.
- **Production risks:** Hot partitions from poor key design; over-provisioned capacity units; GSI write amplification; Streams consumer falling behind.

---

## Comparison Table

| Database | Data Model | ACID | Horizontal Scale | Query Power | Ops Complexity | Best For |
|---|---|---|---|---|---|---|
| PostgreSQL | Relational + JSON | Full | Hard (Citus/Aurora) | Excellent (SQL++) | Medium | Primary store, any app |
| MySQL/MariaDB | Relational | Full (InnoDB) | Medium (PlanetScale) | Good (SQL) | Medium | LAMP stacks, CMS |
| SQLite | Relational | Full | No (Turso adds lite) | Good (SQL) | None | Embedded, edge, tests |
| MongoDB | Document | Multi-doc (4.0+) | Native sharding | Aggregation pipeline | Medium-High | Flexible schema, catalogs |
| Redis | Key-value/struct | None (by default) | Redis Cluster | Limited | Low-Medium | Cache, queue, pub/sub |
| ClickHouse | Columnar | Limited | Native (distributed) | Excellent (analytics) | High | Analytics, logs, BI |
| Elasticsearch | Document/inverted | No | Native sharding | Full-text + agg | High | Search, observability |
| Firestore | Document | Within-doc | Google-managed | Limited | None | Mobile real-time |
| Supabase | Relational (PG) | Full | PG-based | Excellent (SQL) | Low (managed) | SaaS, full-stack JS |
| DynamoDB | Key-value/document | Item-level | AWS-managed | Very Limited | Low (managed) | AWS serverless, KV at scale |

---

## Recommended Combinations

- **PostgreSQL + Redis** — Relational OLTP with cache layer. PostgreSQL as source of truth, Redis caches expensive queries and sessions. Most common production combo.
- **PostgreSQL + ClickHouse** — OLTP + analytics. Postgres for writes and transactions; replicate to ClickHouse for dashboards and reporting. Avoids OLAP load on the primary.
- **PostgreSQL + Elasticsearch** — OLTP + full-text search. Postgres as authoritative store; sync to ES for search and faceting. Standard e-commerce pattern.
- **Supabase + Redis (Upstash)** — Full-stack JS app with managed Postgres, real-time, and serverless Redis caching. Zero-ops rapid delivery.
- **DynamoDB + ElastiCache (Redis) + OpenSearch** — AWS-native trio: DynamoDB for the hot path, Redis for rate limiting/sessions, OpenSearch for search.
- **MongoDB + Redis** — Document store + cache. Common in Node.js stacks needing flexible schemas with fast cache invalidation.
- **SQLite (Turso) + Upstash Redis** — Edge-native: SQLite replicated to edge PoPs, Redis for global rate limiting. Works with Cloudflare Workers / Vercel Edge.
- **ClickHouse + Kafka** — Streaming analytics: Kafka ingests events, ClickHouse consumes via Kafka engine or Kafka Connect for real-time dashboards.

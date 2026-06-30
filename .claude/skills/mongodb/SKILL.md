---
name: mongodb
description: >
  Activate when designing MongoDB schemas, writing aggregation pipelines, planning indexes,
  handling transactions, configuring sharding, or setting up Atlas. Triggers: any mention of
  MongoDB, document model, Atlas, Mongoose, aggregation pipeline, embed vs reference, or
  sharding strategy.
---

# MongoDB

## When to use
- Designing or reviewing document schemas (embed vs. reference decisions)
- Writing or optimizing aggregation pipelines
- Planning index strategies (compound, partial, text, geospatial, Atlas Search)
- Implementing multi-document ACID transactions
- Configuring sharding keys and cluster topology
- Setting up MongoDB Atlas (clusters, Atlas Search, Atlas Vector Search, Triggers, App Services)
- Migrating from relational models to document model

## Workflow

1. **Clarify access patterns first.** List every query the application will run, their frequency, and sort/filter fields. Schema design follows access patterns, not entity relationships.

2. **Embed vs. reference decision:**
   - Embed when: 1-to-few relationship (< ~16 MB doc limit), child data is always read with parent, child has no independent lifecycle, child is not queried standalone.
   - Reference when: 1-to-many with unbounded growth, child accessed independently, many-to-many, data shared across multiple parents, or child updates frequently without parent needing reload.
   - Hybrid: embed a bounded summary (e.g., last 5 comments) + reference full collection.

3. **Design the schema:**
   - Keep hot fields at the top level for index efficiency.
   - Use sub-documents for cohesive nested data (address, metadata).
   - Use arrays sparingly on the reference side of a relationship; unbounded arrays cause document growth and index bloat.
   - Add `created_at` / `updated_at` at the top level on every collection.
   - Avoid polymorphic arrays of mixed types; use a `type` discriminator field if necessary.

4. **Index strategy:**
   - Single-field index: simple equality filters.
   - Compound index: follow ESR rule — Equality fields first, then Sort fields, then Range fields.
   - Partial index: `{ partialFilterExpression: { status: "active" } }` to index only relevant docs.
   - Sparse index: when field is absent on most documents.
   - TTL index: automatic document expiry (`expireAfterSeconds`).
   - Text / Atlas Search: full-text needs Atlas Search (Lucene-backed) for production; avoid `$text` at scale.
   - Avoid redundant indexes; each write pays for every index. Run `db.collection.getIndexes()` and `$indexStats` regularly.
   - Use `.explain("executionStats")` to verify IXSCAN vs COLLSCAN and nReturned vs nScanned ratio.

5. **Aggregation pipeline:**
   - Push `$match` and `$limit` as early as possible to reduce working set.
   - `$match` on an indexed field before `$group` is the single biggest performance lever.
   - Use `$project` to drop unused fields before expensive stages.
   - `$lookup` is expensive; consider denormalizing if called in hot paths. Use `pipeline` form of `$lookup` with a `$match` to limit joined documents.
   - `$facet` runs multiple sub-pipelines on the same input; good for search + pagination + counts in one round-trip.
   - Use `allowDiskUse: true` only for ETL/reporting pipelines, not user-facing queries.
   - Prefer `$merge` or `$out` for materializing aggregation results into summary collections.

6. **Transactions (multi-document ACID):**
   - Available on replica sets (default Atlas) and sharded clusters.
   - Keep transactions short (< 60 s, ideally < 1 s) — long transactions cause lock contention and oplog pressure.
   - Never perform network I/O, external API calls, or user interaction inside a transaction.
   - Retry on `TransientTransactionError` and `UnknownTransactionCommitResult` using the official retry loop pattern.
   - Prefer single-document atomicity (embedded sub-documents) over transactions when the data fits.

7. **Sharding:**
   - Choose a shard key with high cardinality, low frequency (no hot shard), and query isolation (most queries include the shard key).
   - Hashed shard key: good write distribution, bad for range queries.
   - Ranged shard key: efficient range queries, risk of hot shards.
   - Compound shard key: `{ tenant_id: 1, _id: 1 }` for multi-tenant SaaS — isolates per-tenant data.
   - Once set, shard key cannot be changed (MongoDB 5.0+ allows resharding but it is expensive).
   - Pre-split chunks for predictable large initial loads.

8. **Atlas setup:**
   - Use M10+ for production; M0/M2/M5 are shared, no backups, no VPC peering.
   - Enable backup (continuous or snapshot-based) on all production clusters.
   - Use VPC peering or Private Link; never expose clusters to the public internet.
   - Atlas Search: define index in Atlas UI or IaC (`mongocli`/`atlas` CLI); use `$search` aggregation stage.
   - Atlas Vector Search: store embeddings as `float[]` arrays; define vector index with `numDimensions` and `similarity` metric.
   - Use Atlas Triggers for change-stream-driven serverless logic rather than polling.
   - Connection string: always use SRV format `mongodb+srv://...`; set `maxPoolSize`, `serverSelectionTimeoutMS`, `connectTimeoutMS`.

9. **Driver best practices (Node.js / PyMongo / Motor):**
   - Create one `MongoClient` per process and reuse it; never open a new client per request.
   - Use `session` objects for transactions; always call `session.endSession()` in a `finally` block.
   - Set `w: "majority"` write concern for critical writes; `w: 0` only for fire-and-forget logging.
   - Use `readPreference: "secondaryPreferred"` for analytics/reporting queries to offload primaries.

## Standards

**Do:**
- Design schema for the dominant read pattern.
- Use `_id` as the shard key suffix for uniqueness guarantees.
- Run `explain()` before declaring a query fast.
- Use connection pooling (default pool size 100 in Node driver).
- Enable `retryWrites: true` and `retryReads: true` in connection string (Atlas default).
- Use Mongoose discriminators for polymorphic collections.
- Store monetary values as integers (cents) or `Decimal128`, never `float`.
- Use Atlas Data API or App Services for mobile/browser direct access instead of exposing the driver.

**Do not:**
- Store large binary files (> 16 MB) in documents; use GridFS or S3 + reference URL.
- Use `$where` or server-side JavaScript — security risk and disables query optimizer.
- Create an index on every field "just in case" — write amplification degrades throughput.
- Use `remove()` / `update()` without a filter — drops entire collection / updates all docs.
- Use `findOne` in a loop; batch with `$in` or cursor iteration.
- Run `mongodump` on Atlas production as a backup strategy; use Atlas Backup instead.
- Rely on `ObjectId` sort order as a substitute for a `created_at` timestamp — ObjectId encodes seconds, not milliseconds.

## Common mistakes to avoid

- **Unbounded array growth:** embedding all comments/events in a parent document until it hits the 16 MB BSON limit. Solution: reference pattern or bucket pattern.
- **Missing compound index:** running a query that filters on `status` and sorts on `created_at` without a `{ status: 1, created_at: -1 }` index causes a COLLSCAN + in-memory sort.
- **Ignoring write concern in transactions:** `w: 1` in a transaction can lose committed data on primary failure.
- **Sharding on `_id` (ObjectId) alone:** monotonically increasing shard key concentrates all writes on the last chunk (hot shard). Use hashed or compound key.
- **Opening a new MongoClient per Lambda invocation:** cold-start overhead and connection pool exhaustion. Cache the client outside the handler.
- **Using `$lookup` on unindexed foreign field:** always index the `foreignField` in the joined collection.
- **Storing ISO date strings instead of BSON Date:** loses timezone math, range query efficiency, and TTL index support.

## Output format

- Schema designs → `docs/data-model/` (use template `.claude/templates/data-model.md`)
- Aggregation pipelines → inline code blocks in implementation docs under `docs/specs/`
- Index plan → `docs/decisions/mongodb-indexes-<feature>.md` (use template `.claude/templates/decision-record.md`)
- Atlas configuration → `docs/deployment/atlas-setup.md` (use template `.claude/templates/deployment-plan.md`)

## Related checklists
- `.claude/checklists/data-model.md`
- `.claude/checklists/database.md`
- `.claude/checklists/performance.md`
- `.claude/checklists/security.md`

## Related agents
- `.claude/agents/core/database-architect.md`
- `.claude/agents/engineering/data-engineer.md`
- `.claude/agents/engineering/backend-engineer.md`
- `.claude/agents/quality/performance-engineer.md`

---
name: data-modeling
description: Design entities, relationships, constraints, indexes, and a safe migration strategy from requirements and architecture. Activate before persistence code is written, when adding or reshaping a domain entity, or when query performance/data integrity issues point to a model or index problem.
---

# Data Modeling

## When to use
- After architecture (`.claude/skills/architecture/SKILL.md`) defines components and their owned data, before persistence code is written.
- When introducing a new domain entity or significantly reshaping an existing one.
- When integrity bugs, slow queries, or scaling limits trace back to schema or indexing.
- When evaluating a storage-paradigm change (e.g., adding a document store or time-series DB alongside relational tables).

## Workflow

### Phase 1 — Domain Extraction (Inputs → Conceptual Model)

**1. Gather inputs.**
Collect `docs/requirements.md`, `docs/architecture.md`, and any existing `docs/data-model.md`. Pull the entity vocabulary directly from requirements — what nouns does the business actually name? (user, order, subscription, device, transaction, job, session, etc.)

**2. List entities, attributes, and relationships.**
For each entity: name, description in one plain sentence, the key attributes (name, type, constraints), and the lifecycle states it passes through. For each relationship: which entities, what cardinality (one-to-one / one-to-many / many-to-many), whether it is optional or mandatory on each side, and what the relationship itself means in business terms.

**3. Validate against the domain, not the UI.**
Examine every entity and ask: does this appear in the business language, or did it come from a UI screen or implementation artifact? Remove or rename anything that is a UI concern masquerading as a domain entity. This is the single most common source of brittle schemas.

**4. Produce a conceptual ER diagram.**
Use Mermaid (`erDiagram`). Show entities, key attributes, cardinality notation (||, }|, |{, etc.), and relationship labels. Share with a domain expert or product owner for sign-off before proceeding — changes here are cheap; changes to a deployed schema are expensive.

---

### Phase 2 — Logical Design (Paradigm + Keys + Normalization)

**5. Choose the storage paradigm per data set.**
Evaluate against actual access patterns, not general preference. Use the stack decision in `docs/stack.md` as the anchor; this step may propose additions.

| Pattern | Choose when | Avoid when |
|---|---|---|
| Relational (SQL) | Complex joins, strong integrity, ACID transactions, ad-hoc queries | Schema changes very frequently, document varies wildly per row |
| Document (NoSQL) | Aggregate-oriented reads, flexible/optional structure, hierarchical data | Need cross-document transactions or complex multi-collection joins |
| Key-value | Caches, sessions, idempotency locks, counters | Need to query by anything other than the key |
| Wide-column / time-series | High-volume append, time-windowed aggregates, IoT telemetry | Need strong relationships between records |
| Graph | Relationship traversal is the primary operation (social graphs, recommendations, access-control graphs) | Data is flat and tabular |
| Search index (e.g., Elasticsearch) | Full-text search, faceted filtering, fuzzy match | Single source of truth — always backed by a primary store |
| Object/blob store | Binary files, media, large payloads | Queryable structured data |

Mixed paradigms are fine; each must be justified and documented.

**6. Define primary keys and identity.**
- Prefer stable surrogate keys: UUIDv4 (random, privacy-safe), UUIDv7 / ULID (time-ordered, better index locality, recommended for high-insert tables).
- Use natural keys only when they are truly immutable, unique, and meaningful to the business (e.g., ISO country code, ISIN for securities).
- For distributed inserts without a coordinator, use client-generated UUIDv7/ULID — avoids round-trips and hotspot inserts.
- Never expose internal sequential integers as public IDs; they leak record counts and are enumerable.

**7. Normalize to 3NF first.**
Eliminate transitive and partial dependencies. Third normal form prevents anomalies (insert, update, delete). Document every deviation from 3NF with its rationale and consistency plan before accepting it.

**8. Denormalize deliberately, not habitually.**
Denormalize only where a measured read pattern requires it and replication can be kept consistent. Acceptable denormalization patterns:
- **Materialized/computed columns** maintained by the database engine.
- **Summary/rollup tables** refreshed by a scheduled job or trigger — document the staleness window.
- **Embedded documents** in a document store when the sub-entity is always read with its parent and never queried independently.
- **Read replicas / CQRS projections** when read and write models genuinely diverge at scale.

---

### Phase 3 — Constraints and Integrity

**9. Apply NOT NULL, defaults, and uniqueness.**
Every column that must always have a value gets `NOT NULL`. Nullable columns are opt-in with a documented reason. Unique constraints enforce real-world uniqueness at the database level — email addresses, usernames, order numbers, idempotency keys. Do not rely on application code alone for uniqueness invariants.

**10. Define foreign keys with explicit referential action.**
For every FK:
- `ON DELETE RESTRICT` (default safe): block deletion of a parent that has children.
- `ON DELETE CASCADE`: use only when child records are meaningless without the parent and bulk deletion is safe (e.g., cascade-delete line items when an order is hard-deleted).
- `ON DELETE SET NULL`: use when the child should be orphaned rather than deleted (e.g., reassigning tasks when a user is deleted).
- Document the choice; the wrong default silently corrupts data on bulk parent deletions.

**11. Add CHECK constraints and enums.**
Database-level checks enforce domain rules: valid ranges, non-negative amounts, valid state transitions where the set is finite and stable. For state/status columns: use `CHECK` + a string enum or a lookup table (not an integer code). Use lookup tables when the set of values must be queryable and joinable (e.g., `order_statuses`).

---

### Phase 4 — Index Design

**12. Derive indexes from the actual query list.**
Write out every query the application will run (filter conditions, join conditions, sort order, aggregation keys). Only then design indexes to serve them. An index you cannot trace to a named query is a candidate for removal.

**13. Apply index design rules.**
- **Single-column index** on a FK used in joins and on high-cardinality filter columns.
- **Composite index**: column order matters — put the highest-cardinality equality filter first, then range columns, then the sort column. `WHERE status = 'active' AND created_at > ?` → index on `(status, created_at)`.
- **Partial index**: index only a subset of rows to save space and improve speed for sparse queries. Example: `WHERE deleted_at IS NULL`.
- **Covering index**: include non-key columns in the index so the engine can answer a query from the index alone without a table lookup. Use for hot read paths.
- **Unique index**: serves as both a uniqueness constraint and an index.
- **Full-text / vector index**: use the engine's native FTS or a dedicated search index; do not emulate with LIKE.
- Index every FK column that will be used to load children given a parent. Without this, child lookups full-scan the table.

**14. Verify with EXPLAIN / query plans.**
Before finalizing, run EXPLAIN (ANALYZE) on the top 5 queries against representative data volumes. The plan should show index seeks / index scans, not sequential scans on large tables. Adjust composite key order if needed.

**15. Identify and remove redundant indexes.**
Indexes that are a prefix-superset of another, or indexes on very low-cardinality columns (e.g., a boolean with 95% true), are often better removed. Document the decision.

---

### Phase 5 — Sensitive Data, Scale, and Lifecycle

**16. Classify and protect sensitive data.**
Produce a sensitive-data table: column, entity, classification (PII / PHI / PCI / internal-confidential), encryption requirement (at-rest only, field-level, tokenized), retention limit, and jurisdiction if relevant. Apply:
- **Encryption at rest** for the whole database (standard, usually platform-default).
- **Field-level encryption** for high-sensitivity columns (credit card tokens, SSNs, health data) that must be unreadable even to a compromised DB admin.
- **Tokenization** for PCI-scoped data — store a token and let a PCI-compliant vault hold the real PAN.
- **Data minimization** — do not collect data you do not need; delete it when retention expires.
- Cross-reference `.claude/checklists/security.md` before finalizing.

**17. Plan audit, history, and lifecycle.**
- **Audit columns** (`created_at`, `updated_at`, `created_by`, `updated_by`) on all mutable entities — use DB-level defaults/triggers so they cannot be omitted.
- **Soft delete** (`deleted_at TIMESTAMPTZ`): prefer over hard delete for records with audit/legal requirements. Add a partial index on `WHERE deleted_at IS NULL`.
- **Immutable event log**: for financial, compliance, or domain-event use cases, write events to an append-only table rather than mutating state. The current state is a projection.
- **Partitioning and archival**: for high-volume tables (logs, events, telemetry), design range or list partitioning upfront. Define the archival/purge strategy before data accumulates.

---

### Phase 6 — Migration Strategy

**18. Version and sequence migrations.**
Every schema change is a migration file: sequentially numbered, named descriptively (`0023_add_user_preferences_table.sql`), stored in VCS, reviewed like code. Migrations run in order on deploy.

**19. Write forward and rollback for every migration.**
Every migration has an `up` and a `down`. Test both. If a `down` cannot be written without data loss, that is a signal the change is destructive and needs additional review.

**20. Use the expand/contract pattern for destructive changes.**
Never rename a column, drop a column, or change a type in a single deploy. Use three phases across three safe deploys:
1. **Expand**: add the new column/table alongside the old one; start writing to both.
2. **Backfill**: migrate existing data; verify completeness.
3. **Contract**: switch all reads to the new; remove the old column in a later deploy once confident.

This makes every schema change zero-downtime and independently reversible.

**21. Guard destructive migrations.**
Any migration that drops columns, drops tables, truncates data, or changes column types in a narrowing direction is **destructive** and requires:
- Explicit human approval before apply.
- A verified, current backup.
- A documented rollback procedure (not just a `down` migration — a time estimate and a smoke test).
- Log the decision in `docs/decisions/`.

---

### Phase 7 — Documentation and Handoff

**22. Document in `docs/data-model.md`.**
Use the template at `.claude/templates/data-model.md`. Sections: ER diagram (Mermaid), per-entity field tables, relationship list with cardinality and referential action, index plan tied to named queries, sensitive-data classification table, audit/retention rules, and migration strategy summary.

**23. Hand off to API design.**
A complete data model is the input to `.claude/skills/api-design/SKILL.md`. The data model defines what can be exposed; the API design defines how.

---

## Standards

- **Do** use one naming convention across the entire schema (snake_case for SQL is conventional; enforce it without exception). Singular or plural table names — pick one and never mix.
- **Do** enforce referential integrity and invariants at the database level for all critical data; application-level enforcement alone is insufficient.
- **Do** make every migration reversible and code-reviewed; ship forward + rollback together.
- **Do** derive indexes from real, named queries and verify with EXPLAIN/ANALYZE before deploying.
- **Do** record `created_at` / `updated_at` on all mutable entities using DB-level defaults.
- **Do** classify all sensitive fields and specify protection before writing persistence code.
- **Do** prefer UUIDv7 or ULID over sequential integer IDs for distributed systems.
- **Do not** run destructive migrations (DROP TABLE/COLUMN, narrowing type change, truncate) without explicit human approval and a verified backup — this is a guarded, irreversible action.
- **Do not** store secrets, full card numbers (PCI), or unencrypted PII/PHI in plain columns.
- **Do not** over-normalize to the point of unusable query complexity (6+ table joins for a common read path is a sign to revisit), nor denormalize without a documented consistency plan.
- **Do not** skip the conceptual ER step and jump straight to DDL — the conceptual step catches domain misunderstandings before they solidify.
- **Do not** use magic integer codes for status/type columns; use string enums or lookup tables that are self-documenting in queries.

## Common mistakes to avoid

- **Modeling tables from UI screens** instead of the domain, producing brittle schemas coupled to the current UI design.
- **Missing FK indexes** — foreign key columns used in joins without an index cause silent full-table scans at scale. Index every FK.
- **Over-indexing** — an index on every column cripples write throughput. Each index must trace to a real query.
- **Nullable everything** — when everything is nullable the schema enforces no invariants and bugs accumulate silently in the data.
- **Hard-deleting records that audit or compliance requires retained** — add `deleted_at`; the cost is low and the recovery value is high.
- **Irreversible single-step migrations** — renaming or dropping a column in one deploy with no rollback blocks safe recovery.
- **Deferring PII/encryption classification** until an audit forces a costly, live-data redesign.
- **Choosing a storage paradigm by familiarity** rather than by access patterns — e.g., using a relational table for time-series telemetry, or a document store for data with complex cross-entity transactions.
- **Natural key creep** — using mutable user-facing values (email, username, phone) as primary or foreign keys. When the value changes, cascades break.
- **Not testing the `down` migration** — the rollback only matters in an emergency; discovering it is broken then is the worst possible time.

## Output format

A completed `docs/data-model.md` using `.claude/templates/data-model.md`, containing:
1. Mermaid `erDiagram` covering all entities and relationships.
2. Per-entity field tables: `field | type | nullable | constraints | notes`.
3. Relationship/cardinality list with referential actions.
4. Index plan: each index named, columns listed with order rationale, tied to a named query or use case.
5. Sensitive-data classification table: column, entity, classification, protection method, retention.
6. Audit and lifecycle rules (soft-delete strategy, partitioning plan if applicable).
7. Migration strategy: expand/contract pattern description, rollback approach, and any already-written migration file paths.

Migration files live in the project's `migrations/` (or equivalent) directory, each with an `up` and `down`, sequentially numbered.

## Related checklists
- `.claude/checklists/security.md`
- `.claude/checklists/performance.md`
- `.claude/checklists/database.md`
- `.claude/checklists/production.md`

## Related agents
- `.claude/agents/core/solution-architect.md`
- `.claude/agents/engineering/database-architect.md`
- `.claude/agents/quality/security-auditor.md`
- `.claude/agents/quality/performance-engineer.md`

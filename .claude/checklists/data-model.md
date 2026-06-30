# Data Model Checklist

Data-model integrity, safety, and migration gate — passing this proves the schema enforces correctness at the database layer, migrations are reversible, sensitive data is protected, and the model will not become a liability as data volumes grow. Items are severity-tagged P0/P1/P2/P3.

## P0 — Blockers (must pass before schema is applied to staging or production)

- [ ] Every table or collection has a primary key that is stable, globally unique, non-reusable, and not derived from mutable business data; surrogate UUIDs (v4 or v7), ULIDs, or auto-increment surrogate integers are acceptable; email addresses, usernames, phone numbers, and external IDs are prohibited as primary keys.
- [ ] Foreign key constraints (or equivalent referential integrity for document stores and ORMs) are defined for every relationship; orphaned records are structurally impossible — the database, not application code, enforces this.
- [ ] NOT NULL constraints are applied to every column that must always carry a value; every nullable column is explicitly justified in the data dictionary or schema comment (`-- nullable because: ...`).
- [ ] Unique constraints are defined for all natural-key business rules (e.g., `UNIQUE(user_id, plan_id)` for one active subscription per user, `UNIQUE(order_reference)` for order numbers); these are database-level constraints, not only application-level checks.
- [ ] Sensitive fields are identified in the schema and confirmed to be stored in their correct protection form: passwords are stored only as a strong hash (bcrypt, Argon2id, or scrypt — never MD5/SHA1); PII columns at rest are encrypted (AES-256 or equivalent) if required by policy; payment tokens reference a PCI-compliant vault, not raw card data; plaintext secrets are absent from every table.
- [ ] Every migration script is idempotent and has a validated, tested rollback path (a `down` migration or a documented manual reversal) checked in alongside the `up` migration before the PR is merged.
- [ ] No migration drops a column, renames a column, changes a column's data type, or drops a table without a multi-phase deprecation plan: (1) stop writing to the old shape while the new shape is deployed, (2) migrate existing data, (3) remove the old shape in a separate subsequent deployment — with at least one full production deploy cycle between phases.
- [ ] Default values for new NOT NULL columns added to existing tables are compatible with existing rows: either a `DEFAULT` value is provided in the `ALTER TABLE` statement, or the column is added as nullable first and back-filled before the NOT NULL constraint is applied, avoiding a full table lock.
- [ ] Check constraints validate domain rules at the database level for columns with finite valid ranges (e.g., `CHECK (amount > 0)`, `CHECK (status IN ('active','inactive','deleted'))`) so invalid states cannot be persisted even by a buggy application.

## P1 — Important (fix before data volumes make it costly)

- [ ] Indexes exist on: all foreign key columns, all columns used in WHERE, JOIN, and ORDER BY clauses in documented query patterns, and all high-cardinality filter columns; the absence of an index on a foreign key is a specific, flagged omission.
- [ ] Data types are the tightest correct fit: `TIMESTAMPTZ` (not `TIMESTAMP WITHOUT TIME ZONE`) for all timestamps; `NUMERIC` or `DECIMAL(precision, scale)` for monetary amounts (never `FLOAT` or `DOUBLE`); `TEXT` or `VARCHAR(n)` with a justified length; `BOOLEAN` for flags (not `INT` or `CHAR(1)`).
- [ ] Soft-delete strategy is decided, documented, and consistent across the schema: either `deleted_at TIMESTAMPTZ` (nullable), a `status` enum column, or a separate archive table — the choice is uniform; no table uses a different approach without justification.
- [ ] An audit or event-log table, or a Change Data Capture (CDC) strategy (Debezium, AWS DMS, Postgres logical replication), is implemented for every entity that requires a history trail: financial records, user consent events, configuration changes, and admin actions; the audit record stores actor, timestamp, before-state, and after-state.
- [ ] Multi-tenancy isolation is enforced at the database layer (not only the application layer): row-level security policies on tenant_id, separate schemas per tenant, or separate databases, depending on the isolation level required by the product spec and compliance obligations.
- [ ] Large binary assets, documents, and media files are stored in object storage (S3, GCS, Azure Blob, or equivalent); the database holds only the reference URI or storage key; blob fields (`BYTEA`, `BLOB`) larger than a defined threshold (e.g., 1 MB) are prohibited.
- [ ] All lookup / reference values (status codes, category codes, type enumerations) are stored as enum types or normalized lookup tables, not as magic strings or bare integers; bare numeric codes without a lookup table are a blocker.
- [ ] Estimated row counts and growth rates per table are documented in the data dictionary; tables projected to exceed 10 million rows within 12 months have a partitioning or archival strategy planned before they hit that threshold.
- [ ] Schema migration tool is the single source of truth for all DDL (Flyway, Liquibase, Alembic, Prisma Migrate, Knex, or golang-migrate); no ad-hoc DDL has been executed manually in any shared environment since the migration tool was adopted.

## P2 — Hardening / nice-to-have

- [ ] Full-text search requirements are served by a dedicated search index (Elasticsearch, OpenSearch, Typesense, Meilisearch, or `pg_trgm`/`to_tsvector` for smaller datasets) rather than `LIKE '%term%'` queries on large text columns; query plans for all search-adjacent queries show no sequential scans on large tables.
- [ ] Data retention and deletion policies are implemented and tested: scheduled purge jobs, TTL indexes (MongoDB/Redis), or time-based partition drops aligned with the privacy policy, legal obligations, and the data-retention policy in the product spec; the right to erasure (GDPR Article 17) is mechanically enforceable.
- [ ] A data dictionary is maintained in version control: every table and every column has a human-readable description, the owning team, the data classification (public/internal/confidential/restricted), and a `since_version` marker.
- [ ] Seed data and test fixtures are version-controlled and can recreate a representative, anonymized dataset for local development and CI environments in under 5 minutes; production data is never used in non-production environments unless it is anonymized.
- [ ] Query performance is validated under representative data volumes: EXPLAIN ANALYZE output for all critical queries shows index scans (not sequential scans) on tables projected to exceed 100,000 rows; slow-query thresholds are configured in the database engine and logged.

## P3 — Post-launch / backlog (track and revisit after launch; never blocks shipping)

- [ ] Data dictionary is reviewed against the live schema 60–90 days post-launch; any columns added during build that lack descriptions, data classifications, or `since_version` markers are backfilled and the data dictionary is re-published.
- [ ] Slow-query log from production is reviewed monthly; any query with a sequential scan on a table that has grown beyond 100,000 rows since launch is assigned an index or a query-rewrite ticket with an SLA.
- [ ] Partitioning or archival strategy for tables projected to exceed 10 million rows is implemented before the threshold is reached, using the growth rates documented at design time against observed production rates.
- [ ] Data retention purge jobs and TTL policies are verified end-to-end against production data after the first full retention cycle completes (e.g., 30, 90, or 365 days post-launch depending on the policy).
- [ ] Anonymised seed data and test fixtures are refreshed from a sanitised production snapshot to keep local and CI datasets representative of the actual data distribution after 3–6 months of real usage.

## How to use

Run after the data model is drafted using `.claude/templates/data-model.md` and before any migration is executed against a shared database (staging or production). The primary agents are `.claude/agents/engineering/database-architect.md` and `.claude/agents/quality/security-auditor.md`. This gate is triggered by `.claude/commands/design-data-model.md` at the design stage. For every subsequent migration PR, re-run P0 items as a merge-gate checklist. Pair with `.claude/checklists/security.md` for encryption-at-rest and access-control checks, and `.claude/checklists/production.md` for backup and disaster-recovery verification. Mark each item `[x]` when verified or `[-]` when formally waived with a written justification and a named approver.

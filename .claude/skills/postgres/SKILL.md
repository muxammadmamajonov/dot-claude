---
name: postgres
description: >
  Activate when designing schemas, writing queries, tuning performance,
  managing migrations, or securing a PostgreSQL database — regardless of
  application language or ORM. Use whenever the work touches Postgres, `psql`,
  SQL DDL/queries, indexes, `EXPLAIN`/query plans, JSONB, partitions, extensions,
  or migrations — even if the user just says "the database" or "my SQL".
---

# PostgreSQL Development

## When to use
- Designing or reviewing table schemas, constraints, and indexes
- Writing or optimising complex SQL queries, CTEs, or window functions
- Authoring or debugging database migrations
- Configuring connection pooling, vacuuming, replication, or backups
- Diagnosing slow queries with `EXPLAIN (ANALYZE, BUFFERS)`
- Implementing row-level security, roles, or audit logging

## Workflow

1. **Understand the access patterns first** — what queries will run most frequently and at what volume? Schema design follows query design, not the reverse.
2. **Design the schema**:
   - Choose the correct data types (avoid `TEXT` where `VARCHAR(n)` or a domain type is better; use `TIMESTAMPTZ` not `TIMESTAMP`; use `UUID` or `BIGSERIAL` for PKs).
   - Add constraints early: `NOT NULL`, `UNIQUE`, `CHECK`, foreign keys with `ON DELETE` policy.
   - Normalise to 3NF by default; denormalise only when a proven performance need exists with a comment explaining why.
3. **Create indexes deliberately**:
   - Single-column B-tree for equality and range filters on high-cardinality columns.
   - Composite index column order: most selective equality columns first, then range columns.
   - Partial indexes for sparse conditions: `CREATE INDEX ON orders (user_id) WHERE status = 'pending'`.
   - GIN for `jsonb`, full-text search, and array containment.
4. **Write the migration**:
   - One migration file per logical change with an `up` and `down` (or an explicit comment if rollback is destructive).
   - Never add a `NOT NULL` column without a `DEFAULT` in the same statement on a live table — it rewrites the full table pre-PG11.
   - Add indexes `CONCURRENTLY` on production tables to avoid locking.
5. **Write queries**:
   - Parameterise all user input — never string-interpolate into SQL.
   - Use CTEs for readability; materialise with `MATERIALIZED` only when the planner is misestimating.
   - Prefer `JOIN` over correlated subqueries in `SELECT` list.
6. **Profile slow queries**:
   - `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)` on the exact query with real parameters.
   - Look for: `Seq Scan` on large tables, high `Rows Removed by Filter`, `Hash Batches > 1` (spill to disk), nested loops with large outer sets.
   - Run `pg_stat_statements` to find top-N slow queries by total time.
7. **Audit for security** — see .claude/checklists/security.md. Row-level security, principle of least privilege on roles, encrypted connections.
8. **Verify backup/restore** before going live — a backup that has never been restored is an untested backup.

## Standards

### Schema design
- Primary keys: `BIGSERIAL` for append-heavy tables; `UUID` (`gen_random_uuid()`) for distributed or externally referenced entities.
- Always `TIMESTAMPTZ` for timestamps — store in UTC, display in application layer.
- Foreign keys must have an index on the referencing column unless they are almost never queried by FK.
- Use `ENUM` types or a lookup table for finite, stable sets of values; use `CHECK (status IN (...))` for small, unlikely-to-change sets.

### Migrations
- Migrations are immutable once merged — never edit a committed migration; write a new one.
- Test `up` and `down` migrations in CI against a real Postgres container.
- Large table changes (adding a column, changing a type): do in multiple small migrations with no-downtime patterns (expand/contract).
- Never `DROP TABLE` or `DROP COLUMN` in the same deployment as the code that stops using it — wait one release.

### Queries
- Use `RETURNING` to get generated IDs/timestamps in a single round trip instead of a follow-up `SELECT`.
- `LIMIT` + `OFFSET` pagination degrades at high offsets; use keyset pagination (`WHERE id > $last_id ORDER BY id LIMIT $n`).
- `COUNT(*)` is fast; `COUNT(DISTINCT col)` on large tables is slow — consider HyperLogLog via `pg_hll` for approximations.
- Wrap multi-step mutations in explicit transactions with appropriate isolation level (`READ COMMITTED` default; `REPEATABLE READ` for read-modify-write cycles).

### Performance
- `autovacuum` must be healthy: check `pg_stat_user_tables.n_dead_tup`. Tune `autovacuum_vacuum_scale_factor` for large tables.
- Connection pooling is mandatory at scale — use PgBouncer (transaction mode) or `pgpool-II`; never open one Postgres connection per application thread.
- `shared_buffers` = 25% of RAM; `effective_cache_size` = 75% of RAM; `work_mem` = RAM / (max_connections × 2) as a starting point.

### Security
- Application user has `SELECT`, `INSERT`, `UPDATE`, `DELETE` on required tables only — never `SUPERUSER` or schema-owner.
- Enable `ssl = on`; require `hostssl` in `pg_hba.conf`.
- Never store plain-text passwords; store argon2/bcrypt hashes.
- Use Row-Level Security (`ALTER TABLE ... ENABLE ROW LEVEL SECURITY`) for multi-tenant data.

### Do not
- Do not use `SELECT *` in application queries — always list columns explicitly.
- Do not run `VACUUM FULL` or `REINDEX` without a maintenance window — they take `AccessExclusiveLock`.
- Do not create indexes without profiling first — every index slows writes.
- Do not use `serial` / `bigserial` for new projects — use `GENERATED ALWAYS AS IDENTITY` (SQL standard).
- Do not share a database superuser account in application connection strings.

## Common mistakes to avoid

| Mistake | Fix |
|---|---|
| Adding a `NOT NULL` column to a large live table | Use `ADD COLUMN col TYPE DEFAULT val`, then backfill, then add `NOT NULL` in a later migration (PG<11). PG11+ handles this in one DDL. |
| Index not used despite existing | Check column order, data type mismatch, or function wrapping in WHERE clause (`WHERE lower(email) = ?` needs functional index). |
| `LIKE '%term%'` not using index | Use `pg_trgm` GIN index: `CREATE INDEX ON t USING gin (col gin_trgm_ops)`. |
| Long-running transaction blocking autovacuum | Set `statement_timeout` and `idle_in_transaction_session_timeout` in `postgresql.conf`. |
| JSONB overuse replacing relational columns | Use JSONB for truly variable/schemaless attributes; model known fields as typed columns. |
| Missing `FOR UPDATE` in optimistic lock patterns | Use `SELECT ... FOR UPDATE` or `UPDATE ... WHERE version = $v` with row count check. |

## Output format

- Schema change: `CREATE TABLE` or `ALTER TABLE` DDL with all constraints, followed by `CREATE INDEX` statements.
- Migration file: numbered file (`YYYYMMDDHHMMSS_description.sql`) with `-- migrate:up` and `-- migrate:down` sections.
- Query optimisation: original query, `EXPLAIN ANALYZE` snippet of the problem node, rewritten query, and expected improvement.
- Role/permission setup: `CREATE ROLE`, `GRANT`, `REVOKE` statements with comments on why each privilege is granted.

## Related checklists
- .claude/checklists/security.md
- .claude/checklists/performance.md
- .claude/checklists/qa.md

## Related agents
- .claude/agents/core/orchestrator.md
- .claude/agents/engineering/database-architect.md

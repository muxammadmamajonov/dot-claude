---
name: mysql
description: >
  Activate when designing schemas, writing queries, tuning performance, managing
  migrations, or administering MySQL 8.0+ / MariaDB 10.6+ (InnoDB) — indexing,
  transactions/isolation levels, replication, query optimisation, and safe
  migration patterns. Use whenever the work touches MySQL/MariaDB, `mysql` CLI,
  SQL DDL/queries, `EXPLAIN`, indexes, or replication — even if the user just
  says "the database" or "my SQL".
---

# MySQL / MariaDB Development

## When to use
- Designing or reviewing table schemas, constraints, and indexes for MySQL/MariaDB
- Writing or optimising SQL queries, stored procedures, or CTEs (MySQL 8.0+)
- Authoring database migrations with attention to locking and online DDL
- Configuring InnoDB settings, replication (GTID / binlog), and read replicas
- Diagnosing slow queries with `EXPLAIN` and the slow query log
- Planning backups, point-in-time recovery, or failover strategies
- Migrating from MySQL 5.7 to 8.0 or from MyISAM to InnoDB

## Workflow

1. **Understand the access patterns first** — schema design follows query design. Identify the top-10 most frequent read queries and write patterns before choosing indexes or partitioning strategies.
2. **Design the schema**:
   - Storage engine: **always InnoDB** — do not create MyISAM tables (no transactions, no FK enforcement, no crash recovery).
   - Character set: `utf8mb4` with collation `utf8mb4_unicode_ci` (or `utf8mb4_0900_ai_ci` for MySQL 8.0) for all new tables. Set globally in `my.cnf`: `character-set-server = utf8mb4`.
   - Primary keys: `BIGINT UNSIGNED AUTO_INCREMENT` for append-heavy tables; `BINARY(16)` for UUIDs stored efficiently (use `UUID_TO_BIN(uuid, 1)` / `BIN_TO_UUID(id, 1)` in MySQL 8.0+). Avoid `VARCHAR` or `CHAR` PKs — they bloat the clustered index.
   - Always `NOT NULL` with a default unless the column is genuinely nullable.
   - Use `DATETIME` for timestamps needing to store outside of Unix range; use `TIMESTAMP` (UTC-stored, auto-converts timezone) for "created/updated" columns within 1970–2038.
3. **Create indexes deliberately**:
   - Primary key is the clustered index (InnoDB B-Tree) — secondary indexes contain the PK value; keep PKs small.
   - Composite index column order: equality predicates first (`WHERE status = ?`), then range predicates (`AND created_at > ?`), then `ORDER BY` columns.
   - Covering indexes: if the query selects only indexed columns, InnoDB never touches the row — add the selected columns as trailing columns in the index.
   - Use `EXPLAIN FORMAT=JSON` to confirm `Using index` (covering) vs `Using index condition` (ICP) vs full `table scan`.
   - Avoid low-cardinality indexes (e.g. boolean columns alone) — the optimiser will skip them.
4. **Write the migration**:
   - Online DDL (MySQL 8.0+): most `ALTER TABLE` operations support `ALGORITHM=INPLACE, LOCK=NONE` but verify with the MySQL Online DDL support matrix before running.
   - For tables >1 GB in production use `gh-ost` or `pt-online-schema-change` — they perform the change without a prolonged table lock.
   - Never `DROP COLUMN` or `RENAME COLUMN` in the same deployment as the code that stops using it — wait one release cycle.
   - Adding a `NOT NULL` column without a `DEFAULT` on MySQL <8.0 (strict mode off) silently inserts empty strings. In MySQL 8.0 strict mode, it fails. Always provide a `DEFAULT`.
5. **Write queries**:
   - Parameterise all user input — never string-interpolate into SQL regardless of library.
   - Prefer `JOIN` over correlated subqueries in `SELECT`; the optimiser may not flatten them.
   - For pagination on large tables: keyset (`WHERE id > :last_id ORDER BY id LIMIT :n`) over `LIMIT :offset, :n` (full index scan grows with offset).
   - `COUNT(*)` is efficient for InnoDB; `COUNT(DISTINCT col)` is not — consider approximate counts via `information_schema.tables.TABLE_ROWS` for display purposes.
6. **Tune InnoDB**:
   - `innodb_buffer_pool_size`: 70–80% of RAM on a dedicated DB server.
   - `innodb_log_file_size` (≤8.0) / `innodb_redo_log_capacity` (8.0+): large enough to avoid frequent checkpoints — 1–4 GB for write-heavy workloads.
   - `innodb_flush_log_at_trx_commit = 1` for ACID (default); `= 2` trades 1 second of durability for higher throughput.
   - `max_connections` + connection pooling: never set `max_connections` above what RAM can sustain. Use ProxySQL or PgBouncer equivalent (ProxySQL for MySQL).
7. **Configure replication**:
   - Use GTID-based replication (`gtid_mode=ON`, `enforce_gtid_consistency=ON`) — simpler failover and position tracking.
   - `binlog_format=ROW` for deterministic replication of all DML; `binlog_row_image=MINIMAL` to reduce binlog size.
   - Read replicas for reporting queries: route with `/*replica*/` comment hints or ProxySQL query rules.
   - Semi-synchronous replication (`rpl_semi_sync_master_enabled`) to reduce data loss risk on failover.
8. **Profile slow queries**:
   - Enable slow query log: `slow_query_log=ON`, `long_query_time=1`, `log_queries_not_using_indexes=ON`.
   - `EXPLAIN SELECT ...` to check: `type` (avoid `ALL`), `key` (index used), `rows` (estimate), `Extra` (avoid `Using filesort`, `Using temporary`).
   - `EXPLAIN ANALYZE` (MySQL 8.0.18+) for actual execution metrics.
   - `SHOW STATUS LIKE 'Handler_%'` and `SHOW PROCESSLIST` for live diagnostics.
9. **Backup and recovery**:
   - Logical: `mysqldump --single-transaction --routines --triggers --events` for small/medium databases.
   - Physical (faster restore): Percona XtraBackup for hot backups of InnoDB without locking.
   - Binlog for point-in-time recovery: `mysqlbinlog --start-datetime=... --stop-datetime=... binlog.000001 | mysql`.
   - Test restores — an untested backup is not a backup.
10. **Audit** against `.claude/checklists/security.md` and `.claude/checklists/database.md`.

## Standards

### InnoDB specifics
- Never create tables without a primary key — InnoDB creates a hidden 6-byte row ID, which means no meaningful clustered index.
- Foreign keys: define `ON DELETE` / `ON UPDATE` policy explicitly (`CASCADE`, `RESTRICT`, `SET NULL`). InnoDB enforces FKs only if both tables use InnoDB.
- Row format: `ROW_FORMAT=DYNAMIC` (default in MySQL 8.0) allows inline storage of variable-length columns up to 768 bytes before overflow.

### Transaction isolation
- Default: `REPEATABLE READ` — prevents dirty reads and non-repeatable reads; phantom reads are largely prevented in InnoDB via gap locks.
- Use `READ COMMITTED` for high-concurrency OLTP where reduced locking outweighs phantom read risk (also reduces binlog size with `binlog_format=ROW`).
- Explicit transactions: `START TRANSACTION; ... COMMIT;`. Avoid long-running transactions — they hold undo log segments and can block `PURGE`.
- Deadlocks: design transactions to acquire locks in a consistent order; keep transactions short; handle `ER_LOCK_DEADLOCK` (1213) with application-level retry.

### Indexing rules
- Every `JOIN` condition column on the right side (child table) needs an index.
- Avoid functions on indexed columns in `WHERE`: `WHERE YEAR(created_at) = 2024` disables the index. Rewrite as `WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01'`.
- Prefix indexes (`INDEX(col(10))`) for long `VARCHAR` columns — choose a prefix length with high cardinality (check with `COUNT(DISTINCT LEFT(col, n)) / COUNT(*)`).
- Monitor unused indexes with `sys.schema_unused_indexes` (MySQL 8.0 Performance Schema).

### Security
- Application DB user: grant only required privileges (`SELECT, INSERT, UPDATE, DELETE` on specific databases/tables). Never `GRANT ALL` or `GRANT ... WITH GRANT OPTION` to application users.
- `REQUIRE SSL` on user accounts to enforce encrypted connections.
- Never store plaintext passwords; handle hashing in the application layer (bcrypt, argon2).
- Validate connection string: host, port, and database should come from environment/secrets — never hardcoded.
- Enable `validate_password` plugin (MySQL 8.0) for user account passwords.

### Migrations
- Migrations are immutable once applied to shared environments — write new migrations, never edit applied ones.
- For lock-free DDL on large tables: `gh-ost` (recommended), `pt-online-schema-change`, or MySQL 8.0 instant ADD COLUMN (`ALGORITHM=INSTANT`).
- Test migrations against a production-sized dataset copy before applying — row count and index cardinality affect ALTER duration.
- Always have a rollback plan: either a `down` migration or a documented manual revert procedure.

### Do not
- Do not use `MyISAM` for any new table.
- Do not use `SELECT *` in application queries.
- Do not use `FULLTEXT` on InnoDB for high-write tables without understanding the index maintenance overhead.
- Do not use `LOCK TABLES` in application code — use explicit transactions instead.
- Do not run `OPTIMIZE TABLE` on InnoDB (it rebuilds the table with a full lock); use `ALTER TABLE t ENGINE=InnoDB` during a maintenance window if reclaiming space is needed.

## Common mistakes to avoid

| Mistake | Fix |
|---|---|
| `utf8` charset (MySQL's 3-byte variant) on new tables | Use `utf8mb4` everywhere — `utf8` cannot store 4-byte Unicode characters (emoji, CJK extensions) |
| Index not used because of implicit type coercion | Match the column type to the query parameter type; `WHERE int_col = '123'` causes a cast that can prevent index use |
| Long `ALTER TABLE` blocking production | Use `gh-ost` or `ALGORITHM=INSTANT` where available; run during low-traffic window with a kill plan |
| High `Threads_connected` causing OOM | Configure ProxySQL with connection pooling; lower `max_connections`; investigate connection leaks |
| Replication lag on read replicas | Identify and tune slow queries on the replica; use parallel replication (`slave_parallel_workers`); offload heavy reads to a dedicated replica |
| `AUTO_INCREMENT` gaps after transaction rollback | Gaps are normal and expected in InnoDB — do not treat `AUTO_INCREMENT` as a gapless sequence |
| DATETIME vs TIMESTAMP confusion | Use `TIMESTAMP` for "created_at/updated_at" (auto UTC conversion); use `DATETIME` when you need dates outside 1970–2038 or need to store a specific local time without timezone shifting |

## Output format

- Schema change: `CREATE TABLE` or `ALTER TABLE` DDL with all constraints, charset, and index definitions; include `gh-ost` invocation for large-table changes.
- Migration file: timestamped SQL file with `-- migrate:up` and `-- migrate:down` sections; note if a `down` migration is destructive.
- Query optimisation: original query, `EXPLAIN FORMAT=JSON` key nodes, rewritten query, and expected index usage.
- Replication setup: `my.cnf` excerpt, `CHANGE MASTER TO` command, and `SHOW SLAVE STATUS` health checks.

Output artifacts go to `docs/specs/` for schema decisions and `docs/decisions/` for significant architecture choices.

## Related checklists
- .claude/checklists/security.md
- .claude/checklists/performance.md
- .claude/checklists/database.md
- .claude/checklists/production.md

## Related agents
- .claude/agents/core/solution-architect.md
- .claude/agents/engineering/database-architect.md
- .claude/agents/quality/performance-engineer.md
- .claude/agents/quality/security-auditor.md

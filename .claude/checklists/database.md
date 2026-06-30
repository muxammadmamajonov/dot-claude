# Database Checklist
Gate for database layers covering indexes, backups, migrations, connection limits, and query budgets. Severity tiers: P0=blocker, P1=important (fix shortly after launch), P2=hardening, P3=post-launch/backlog.

## P0 — Blockers (must pass before any production traffic)

- [ ] **Automated backups enabled and tested**: Point-in-time recovery (PITR) or scheduled snapshots are active; a restore to a test environment from the most recent backup has been verified to succeed within the documented RTO.
- [ ] **Backup retention meets RPO**: Retention period (e.g., 7 days for daily snapshots + PITR) covers the agreed Recovery Point Objective; retention policy is documented and enforced, not left at provider defaults.
- [ ] **Every migration has a rollback script**: `down` migrations exist and have been tested on a staging clone; applying and reversing the migration leaves the schema identical to its prior state.
- [ ] **No migration locks production for more than a few seconds**: DDL operations use lock-minimising strategies (e.g., `CREATE INDEX CONCURRENTLY`, `ADD COLUMN … DEFAULT NULL` on PostgreSQL; `pt-online-schema-change` on MySQL) and have been timed on a production-sized dataset.
- [ ] **Connection pool sized correctly**: The pool size (max connections per app instance × number of instances) does not exceed the database's `max_connections`; headroom is reserved for admin access and replication; verified under expected peak load.
- [ ] **No credentials hardcoded**: Database connection strings, passwords, and IAM roles are loaded from environment variables or a secrets manager; `git grep` confirms none are committed.
- [ ] **Superuser / root access not used by the application**: The application connects with a least-privilege role (SELECT, INSERT, UPDATE, DELETE on owned tables only); no DDL privileges in the application role.
- [ ] **Encryption at rest and in transit enabled**: Storage encryption (AES-256 or equivalent) is active; TLS is enforced for all client connections; `ssl_mode=require` (or equivalent) is set in the application connection string.

## P1 — Important (fix before scaling or shortly after launch)

- [ ] **Indexes support all frequent query patterns**: `EXPLAIN ANALYZE` on the top-20 queries by frequency shows index scans (not sequential scans) on tables with more than 10 000 rows; missing indexes are added before launch.
- [ ] **Slow query log enabled with actionable threshold**: Queries exceeding the threshold (e.g., 1 s) are logged with execution plan; log is reviewed weekly and findings ticketed.
- [ ] **Query budget enforced on unbounded queries**: All application-level list queries include a `LIMIT`; ORM calls that could fetch entire tables are audited and guarded; no query may return more than a documented maximum row count without pagination.
- [ ] **Foreign key constraints and NOT NULL enforced at DB level**: Data integrity rules are enforced in the schema, not only in application code; orphaned rows and null-in-required-fields bugs are impossible at the storage layer.
- [ ] **Read replicas or caching used for read-heavy workloads**: Heavy analytical or reporting queries run against a read replica or a cache layer (Redis, Memcached) to avoid contending with write traffic on the primary.
- [ ] **Vacuum / autovacuum tuned (PostgreSQL) or equivalent maintenance active**: Table bloat and dead-tuple accumulation are monitored; autovacuum is not disabled; index bloat is checked quarterly and `REINDEX CONCURRENTLY` is scheduled if needed.
- [ ] **Connection leak detection active**: Long-idle connections are terminated by a connection pool (e.g., PgBouncer `idle_in_transaction_session_timeout`) or a DB-side timeout; application code always closes connections in `finally` blocks or via context managers.
- [ ] **Migration history tracked in version control**: All migration files are committed to the repository in order; the migration tool (e.g., Flyway, Alembic, golang-migrate) is the sole source of truth for schema state; no ad-hoc manual DDL in production.
- [ ] **Disaster recovery runbook documented and rehearsed**: A step-by-step runbook exists for restoring from backup, promoting a replica, and switching application traffic; it has been rehearsed at least once on a non-production system.

## P2 — Hardening / nice-to-have

- [ ] **Partitioning strategy for large tables**: Tables expected to exceed 50 M rows have a range or hash partitioning plan; partition pruning is confirmed active in query plans.
- [ ] **Index coverage reviewed for write amplification**: Indexes on high-write tables are the minimum necessary; write throughput has been benchmarked with the current index set to confirm no unacceptable write penalty.
- [ ] **Soft deletes implemented where hard deletes are risky**: Tables where accidental deletion would be catastrophic use a `deleted_at` column rather than physical `DELETE`; purge jobs run on a schedule with logging.
- [ ] **Data archival / TTL policy defined**: Time-series, log, event, and audit tables have a documented retention period; rows older than the retention window are archived to cold storage or deleted on a schedule.
- [ ] **Multi-region or cross-AZ replication configured**: Replication lag is monitored and alerted on; failover to a replica in a second availability zone is tested and scripted.
- [ ] **Database version is current and patched**: The DB engine version is within the provider's supported lifecycle; a plan exists to upgrade to the next major version before EOL.
- [ ] **Schema documented in the repository**: An up-to-date ERD or schema description lives in `.claude/templates/` and is regenerated (or reviewed) on every migration; column names and types match the description.
- [ ] **Sensitive columns encrypted at application level**: Columns containing PII (SSN, card numbers, health data) use field-level encryption in addition to storage encryption; the encryption key is stored separately from the data.

## P3 — Post-launch / backlog (track and revisit after launch; never blocks shipping)

- [ ] **Query performance regression suite in CI**: A curated set of the top-50 production queries (by frequency × cost) is run against a representative data clone in CI; a query whose execution plan regresses to a sequential scan or whose cost increases by more than 20 % fails the build.
- [ ] **Data quality monitoring rules defined**: Column-level invariants (non-null rates, value-range bounds, referential integrity across denormalized tables) are encoded in a data quality framework (e.g., Great Expectations, dbt tests) and run on a schedule; violations alert the owning team before they surface as application bugs.
- [ ] **Historical data tier / cold-storage migration executed**: Tables identified in P2 archival policy have their purge/archive jobs running in production and verified to complete within the maintenance window; cold-storage restore path is tested annually.
- [ ] **Database version major upgrade rehearsed**: Upgrade to the next major DB engine version (e.g., PostgreSQL 16 → 17) is performed on a production clone, including extension compatibility checks, `pg_upgrade` or logical replication cutover, and a timed rollback drill; findings are documented before scheduling production cutover.
- [ ] **Row-level security or column masking for multi-tenant data**: Where multiple tenants share tables, row-level security policies (PostgreSQL RLS, MySQL VPD equivalent) or view-based column masking are implemented and penetration-tested to confirm cross-tenant data leakage is impossible at the database layer.
- [ ] **Logical replication or CDC pipeline for downstream consumers**: A Change Data Capture stream (e.g., Debezium, pglogical, Postgres logical replication slots) is set up and monitored for replication lag; downstream analytics or search indexes consume it without polling the primary.

## How to use

**When**: Run this checklist before promoting any schema change to production, before a significant traffic increase, and as part of the quarterly infrastructure review.

**Who**: Database administrator or backend engineer owns P0 items. Engineering lead signs off P1 items. Platform/SRE team reviews P2 during capacity and disaster-recovery planning.

**Command / agent**: Ask the agent `"Run .claude/checklists/database.md for <service/schema>"` — it will inspect migration files for rollback scripts, scan for hardcoded credentials, run `EXPLAIN` on instrumented queries, and check connection pool configuration. Items requiring a live restore test or replica promotion drill are flagged for human scheduling. Cross-reference `.claude/checklists/backend.md` for service-level timeout and pool configuration, and `.claude/checklists/security.md` for encryption key management.

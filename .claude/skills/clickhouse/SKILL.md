---
name: clickhouse
description: >
  Activate when the project uses ClickHouse for OLAP analytics, event ingestion,
  time-series data, log storage, or building a data warehouse. Also activate when
  designing ClickHouse table engines, materialized views, sharding/replication
  topology, or diagnosing slow analytic queries.
---

# ClickHouse Skill

## When to use

- Designing ClickHouse schemas for event streams, log pipelines, or analytical dashboards
- Choosing the right table engine (MergeTree family, ReplacingMergeTree, AggregatingMergeTree, CollapsingMergeTree, Distributed)
- Writing efficient OLAP queries (aggregations, window functions, array operations)
- Setting up materialized views for pre-aggregation
- Configuring replication with ClickHouse Keeper or ZooKeeper
- Ingesting data from Kafka, S3, HTTP, or other ClickHouse engines
- Diagnosing slow queries via `EXPLAIN`, `system.query_log`, and `system.parts`

---

## Workflow

1. **Define the query patterns first** — ClickHouse schema design is query-driven. Know the top 5 queries that must be fast before choosing an ORDER BY key or partition expression.
2. **Choose the table engine**:
   - `MergeTree` — default; immutable append-only facts.
   - `ReplacingMergeTree` — deduplicate rows by primary key (eventual; use `FINAL` in queries to force merge).
   - `AggregatingMergeTree` — store partial aggregation states for incremental rollups.
   - `CollapsingMergeTree` — OLAP-style deletes via sign column.
   - `Distributed` — query shard cluster; always back it with local replicated tables.
   - `Kafka` — read directly from Kafka topics (use as a source, not a storage engine).
3. **Design the ORDER BY (primary key) carefully** — ClickHouse stores data sorted by the `ORDER BY` columns. Put low-cardinality columns first (e.g. `(event_type, toDate(timestamp), user_id)`). The primary key determines sparse index granularity.
4. **Set a `PARTITION BY` clause** — use date-level granularity for time-series: `PARTITION BY toYYYYMM(timestamp)`. This enables partition pruning and TTL-based data expiry.
5. **Use materialized views for pre-aggregation** — create a target `AggregatingMergeTree` table and a `MATERIALIZED VIEW` that feeds into it on insert. This moves computation from query time to ingest time.
6. **Batch inserts** — never insert one row at a time. Minimum effective batch: 1 000 rows; recommended: 10 000–100 000 rows per INSERT. Use the async insert mode (`async_insert=1`) for high-frequency small-batch sources.
7. **Tune with `EXPLAIN`** — run `EXPLAIN indexes=1 <query>` to confirm index granules are being skipped. If `Granules: <large number>`, revisit ORDER BY or add a skip index.
8. **Set TTL** for automatic data expiry: `TTL timestamp + INTERVAL 90 DAY DELETE`.
9. **Monitor** via `system.query_log`, `system.parts`, `system.merges`. Alert on merge queue depth and part count per table (`SELECT count() FROM system.parts WHERE table = 'events' AND active`).

---

## Standards

### Do
- Use `UInt32`/`UInt64` for IDs and counters — smaller types compress better and query faster than `String` UUIDs unless UUID comparison is required.
- Use `LowCardinality(String)` for columns with < ~10 000 distinct values (event type, status, country code).
- Use `Nullable(T)` sparingly — nullable columns disable some optimizations; prefer a sentinel value (empty string, 0) when the null state has no semantic meaning.
- Compress columns explicitly for high-cardinality strings: `CODEC(ZSTD(3))`.
- Run DDL changes (ADD COLUMN, DROP COLUMN) on all replicas via the `ON CLUSTER` clause in replicated setups.
- Test queries on a sampled dataset: `SELECT … FROM table SAMPLE 0.01` before running on the full table.

### Do not
- Do not use `JOIN` as the primary access pattern — ClickHouse is optimized for denormalized wide tables. Pre-join data at ingest or use dictionaries for small reference tables.
- Do not `UPDATE` or `DELETE` rows frequently — mutations in ClickHouse are expensive async rewrites. Use `ReplacingMergeTree` or `CollapsingMergeTree` for mutable data.
- Do not `SELECT *` in OLAP queries — ClickHouse is columnar; reading unused columns wastes I/O.
- Do not use `ORDER BY rand()` for sampling — use `SAMPLE` clause or `sipHash64(id) % N = 0`.
- Do not create more than ~500 partitions per table — too many small parts degrade merge performance.
- Do not expose ClickHouse's native TCP port (9000) or HTTP port (8123) to the internet without authentication and TLS termination.

---

## Common mistakes to avoid

| Mistake | Consequence | Fix |
|---|---|---|
| Wrong ORDER BY (high-cardinality first) | Index granules not skipped; full scan on every query | Put low-cardinality columns first in ORDER BY |
| Inserting one row per INSERT | Extremely slow ingest; merge storm | Buffer inserts client-side; send 10k+ rows per batch |
| Using `ReplacingMergeTree` without `FINAL` | Duplicate rows returned | Append `FINAL` to SELECT, or use `GROUP BY` with `argMax` |
| Too many partitions (daily partition on 3 years of data) | 1000+ parts per table; slow queries | Switch to monthly partition; merge old partitions with `OPTIMIZE TABLE … FINAL` |
| Missing `ON CLUSTER` in DDL on replicated cluster | Schema drift between shards | Always suffix DDL with `ON CLUSTER <cluster_name>` |
| Not setting TTL | Unbounded disk growth | Define TTL at table creation; add TTL to existing tables with `ALTER TABLE … MODIFY TTL` |
| Using `String` for UUIDs in JOINs | Poor join performance | Use `UUID` type or `UInt64` hash of UUID |

---

## Output format

Table definition pattern:
```sql
CREATE TABLE events
(
    timestamp   DateTime64(3) CODEC(Delta, ZSTD(1)),
    event_type  LowCardinality(String),
    user_id     UInt64,
    session_id  UInt64,
    properties  String CODEC(ZSTD(3))
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (event_type, toDate(timestamp), user_id)
TTL timestamp + INTERVAL 365 DAY DELETE
SETTINGS index_granularity = 8192;
```

Materialized view pattern:
```sql
CREATE TABLE events_daily_agg
(
    event_type  LowCardinality(String),
    date        Date,
    count       AggregateFunction(count, UInt64)
)
ENGINE = AggregatingMergeTree()
ORDER BY (event_type, date);

CREATE MATERIALIZED VIEW events_daily_mv TO events_daily_agg AS
SELECT event_type, toDate(timestamp) AS date, countState() AS count
FROM events
GROUP BY event_type, date;
```

---

## Related checklists
- `.claude/checklists/performance.md`
- `.claude/checklists/database.md`
- `.claude/checklists/devops.md`

## Related agents
- `.claude/agents/engineering/backend-engineer.md`
- `.claude/agents/engineering/data-engineer.md`
- `.claude/agents/quality/performance-engineer.md`

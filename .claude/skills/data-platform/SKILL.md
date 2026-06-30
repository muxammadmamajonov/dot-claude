---
name: data-platform
description: >
  Activate when the project involves a data platform, data lake, data warehouse, ETL/ELT pipelines,
  streaming ingestion, BI reporting, or data quality. Triggers on: keywords like "pipeline",
  "warehouse", "dbt", "Spark", "Kafka", "Airflow", "Flink", "Snowflake", "BigQuery", "Redshift",
  "Delta Lake", "Iceberg", "data quality", "lineage", or "BI dashboard".
---

# Data Platform Development

## When to use
- Designing or extending a data ingestion layer (batch or streaming)
- Building or migrating a data warehouse / lakehouse schema
- Writing transformation pipelines (dbt, Spark, Flink, Beam)
- Wiring orchestration (Airflow, Prefect, Dagster, Temporal)
- Setting up data quality checks, SLA monitoring, or data contracts
- Building BI/analytics layers (Looker, Metabase, Superset, Redash)
- Designing data governance, lineage tracking, or access control

## Workflow

1. **Classify the data motion** — identify which zones are in scope:
   | Zone | Also called | Typical storage |
   |------|-------------|-----------------|
   | Ingestion / landing | Bronze / Raw | Object store (S3, GCS, ADLS) |
   | Cleansed / conformed | Silver | Delta Lake / Iceberg table |
   | Aggregated / serving | Gold | Warehouse (Snowflake, BigQuery, Redshift) |
   | Operational / feature | Feature store | Redis, DynamoDB, Feast |

2. **Define data contracts before writing pipelines** — agree on schema, SLAs, and ownership:
   - Source → contract (field names, types, nullability, expected volume, freshness SLA).
   - Document in `docs/data-contracts/<source>.yaml`; break the pipeline if the contract is violated.
   - Use JSON Schema or Great Expectations for runtime validation at ingestion.

3. **Design the ingestion layer**:
   - **Batch**: pull from source API/DB → land raw files (Parquet/JSONL) → partition by `date=YYYY-MM-DD`.
   - **CDC / streaming**: Debezium → Kafka → Flink/Spark Structured Streaming → sink to Iceberg/Delta.
   - Always land raw data unchanged before any transformation — raw zone is append-only and immutable.
   - Capture `_ingested_at` (UTC timestamp) and `_source_file` on every raw record.

4. **Write transformations (dbt or Spark)**:
   - **dbt**: staging models → intermediate models → mart models. One file per model; no `SELECT *`.
   - **Spark**: use DataFrame API over RDD; cache only when the same DataFrame is consumed 3+ times.
   - Transformations must be idempotent: re-running on the same partition produces the same result.
   - Incremental models: prefer `MERGE` / `UPSERT` over full table scans for large tables.

5. **Orchestrate with dependency awareness**:
   - Express upstream/downstream dependencies explicitly (Airflow DAG edges, Dagster asset deps).
   - Set `retries=3`, `retry_delay=5 min`, and `execution_timeout` on every task.
   - Separate ingestion DAGs from transformation DAGs; avoid monolithic pipelines.
   - Use sensors / triggers rather than hard-coded time gaps between stages.

6. **Data quality gates** — enforce at every zone transition:
   - Row count non-zero, not more than 2× or less than 0.5× yesterday's count.
   - Primary key uniqueness, no unexpected nulls in NOT NULL columns.
   - Referential integrity between fact and dimension tables.
   - Tools: Great Expectations, dbt tests (`unique`, `not_null`, `relationships`), Soda Core.

7. **Warehouse schema design**:
   - OLAP: star schema (fact + dimension tables); avoid snowflake unless join cardinality demands it.
   - Partition fact tables by date; cluster / sort on the most common filter column.
   - Use surrogate integer keys in the warehouse; preserve natural/business keys in a separate column.
   - Materialized views or pre-aggregated gold tables for BI queries; never let BI tools scan raw data.

8. **Access control & governance**:
   - Column-level masking for PII fields (Snowflake Dynamic Data Masking, BigQuery column policies).
   - Row-level security for multi-tenant warehouses.
   - Data catalog integration (DataHub, Amundsen, Alation) — emit metadata on every pipeline run.
   - Lineage: emit OpenLineage events from Spark/Airflow; surface in Marquez or DataHub.

9. **Observability**:
   - Pipeline metrics: rows read, rows written, bytes processed, duration, error count — emit to your metrics store (Prometheus, Datadog).
   - Freshness alerts: fail the SLA check if a gold table has not been updated within `expected_freshness`.
   - Cost tracking: log BigQuery/Snowflake query credits per job; alert on anomalies.

10. **Production readiness**:
    - Backfill strategy documented: how to replay N days of data without duplicates.
    - Blue/green deployment for breaking schema changes: add column → backfill → switch consumers → drop old column.
    - Disaster recovery: RTO/RPO defined per pipeline; raw zone is the source of truth for replay.

## Standards

**Do:**
- Treat raw zone as immutable append-only; never overwrite or delete raw files.
- Encode all timestamps as UTC; store as `TIMESTAMP` not `VARCHAR`.
- Name columns consistently: `snake_case`, `_at` suffix for timestamps, `_id` suffix for keys, `is_` prefix for booleans.
- Version dbt models and Spark jobs in Git; tag releases before production deploys.
- Use column pruning and predicate pushdown — always specify only needed columns in SELECT.

**Do not:**
- Run transformations directly against the raw zone; always copy to a staging layer first.
- Use `SELECT *` in production SQL — breaks silently when upstream schema changes.
- Store credentials in DAG code or Spark configs; use secret managers (Vault, AWS Secrets Manager, GCP Secret Manager).
- Drop and recreate large tables for incremental updates — use MERGE/UPSERT.
- Skip data quality checks to save time; failed data reaching gold tables is costlier to fix downstream.

## Common mistakes to avoid

- **No idempotency**: re-running a pipeline inserts duplicate rows. Always use `MERGE` or partition-overwrite, never plain `INSERT`.
- **Schema drift without detection**: upstream adds/removes a column and the pipeline silently writes nulls or drops data. Enforce contracts at ingestion.
- **Timezone confusion**: mixing local and UTC timestamps causes off-by-one day errors in date partitions. Standardize on UTC everywhere.
- **Monolithic DAGs**: one giant DAG makes partial failures hard to retry and obscures lineage. One DAG = one logical data domain.
- **Over-caching in Spark**: caching every DataFrame bloats executor memory. Cache only DataFrames used in multiple downstream branches.
- **Forgetting the backfill path**: pipelines built only for incremental runs break when you need historical data. Design backfill from day one.
- **Wide tables in the serving layer**: 200-column mart tables slow BI tools and confuse analysts. Separate into domain-specific marts.

## Output format

A data platform project structure:

```
ingestion/
  batch/
    <source>_extractor.py
  streaming/
    <source>_consumer.py
transform/
  dbt/
    models/
      staging/
      intermediate/
      marts/
    tests/
    dbt_project.yml
  spark/
    jobs/
      <job_name>.py
    tests/
orchestration/
  dags/
    ingestion/
    transformation/
    quality/
docs/
  data-contracts/
    <source>.yaml
  lineage/
infra/
  warehouse/        # DDL / Terraform for warehouse objects
  kafka/
  airflow/
```

Reference architecture template: `.claude/templates/architecture.md`

## Related checklists
- `.claude/checklists/security.md` — PII masking, access control, secret management
- `.claude/checklists/performance.md` — query optimization, partition strategy, cost control
- `.claude/checklists/launch.md` — data quality gates, SLA definitions, runbook

## Related agents
- `.claude/agents/core/orchestrator.md` — overall project flow
- `.claude/agents/stack/database/` — database and warehouse selection
- `.claude/agents/stack/backend/` — API layers serving data to consumers
- `.claude/agents/quality/` — testing and data quality strategy

# Data Platform Stack Matrix

Choose your data platform components by separating four concerns: (1) ingestion pattern — batch vs. streaming vs. micro-batch; (2) storage and query layer — the warehouse or lakehouse; (3) transformation — how raw data becomes clean, trusted tables; (4) orchestration — how jobs are scheduled, monitored, and retried. These are independent layers; mix and match per project needs. Most teams do not need a full streaming stack — start with batch and add streaming only when latency requirements demand it.

Key decision drivers: data volume and velocity, acceptable latency (minutes vs. milliseconds), team SQL/Python/JVM skill balance, budget for managed services vs. self-operated clusters, and whether you need real-time serving or offline analytics.

---

## Batch vs. Streaming

- **Batch:** Process data in scheduled windows (hourly, daily). Simpler, cheaper, easier to debug and reprocess. Right for most analytics, reporting, and ML feature pipelines where results do not need to be fresher than minutes-to-hours.
- **Micro-batch (Spark Structured Streaming, Flink, Kafka Streams):** Sub-minute latency by processing small windows continuously. Adds complexity but avoids full streaming architecture.
- **True Streaming (Kafka + Flink/Spark Streaming):** Sub-second event-by-event processing. Required for fraud detection, real-time recommendations, live dashboards, alerting on events as they happen. High operational complexity — only adopt when the business requires it.

**Decision rule:** If stakeholders ask for "real-time" but accept 5-minute data, micro-batch satisfies them at a fraction of the complexity. Reserve true streaming for latency SLAs under 30 seconds.

---

## BigQuery (Google Cloud)

- **When to use:** Serverless analytics on Google Cloud. No cluster to manage, pay-per-query or flat-rate pricing, scales to petabytes, excellent dbt integration. Best choice for GCP-native data teams.
- **When NOT to use:** Non-GCP shops (egress costs and ecosystem friction); workloads requiring sub-second query latency on small datasets (ClickHouse is faster here); real-time row-level updates (BigQuery is append-optimized).
- **Strengths:** True serverless (no cluster sizing), automatic scaling, federated queries across GCS/Sheets/Cloud SQL, INFORMATION_SCHEMA for cost auditing, ML models via BigQuery ML, built-in geospatial, strong BI tool integrations.
- **Weaknesses:** On-demand pricing can surprise on large scans; slot reservations require capacity planning; DML (UPDATE/DELETE/MERGE) is expensive; cold query start latency.
- **Team fit:** SQL-first data teams, GCP shops, teams using Looker, Metabase, or dbt Cloud.
- **Scale fit:** Petabyte-scale analytics. Google handles all infrastructure.
- **Production risks:** Full-table scans on un-partitioned tables causing cost spikes; slot contention on shared reservations; streaming inserts at high volume exceeding quotas.

---

## Snowflake

- **When to use:** Cloud-agnostic data warehouse (runs on AWS, GCP, Azure), multi-cloud data sharing, organizations with mixed cloud footprints, data clean rooms, fine-grained RBAC for data governance.
- **When NOT to use:** Teams fully committed to a single cloud with a native warehouse (BigQuery/Redshift is often cheaper); startups on tight budgets (Snowflake credits add up quickly); real-time analytics (ClickHouse is faster per dollar).
- **Strengths:** True separation of compute and storage (scale each independently), zero-copy cloning for dev/test environments, data sharing across organizations, Time Travel for audit/recovery, strong governance (column masking, row access policies), multi-cloud native.
- **Weaknesses:** Pricing complexity (credits, warehouse sizes, cloud storage markup); warehouse cold-start latency; no open storage format (proprietary FDN format); expensive at scale vs. open table formats.
- **Team fit:** Enterprise data teams, organizations sharing data across business units or external partners, multi-cloud data mesh architectures.
- **Scale fit:** Petabyte scale. Virtual warehouses auto-suspend to control cost.
- **Production risks:** Warehouse left running incurring credits; missing auto-suspend/resume settings; data retention window expiry losing Time Travel; credit exhaustion from runaway queries.

---

## ClickHouse

- **When to use:** Sub-second analytical queries on billions of rows, real-time dashboards updated by streaming ingestion, log analytics, product analytics, time-series aggregations. See also `.claude/stack-matrix/database.md`.
- **When NOT to use:** OLTP writes, heavy UPDATE/DELETE patterns, teams without columnar DB experience, arbitrary JOIN-heavy OLAP (BigQuery/Snowflake handle complex joins better).
- **Strengths:** Fastest columnar query engine per dollar, MaterializedViews for real-time pre-aggregation, native Kafka engine for streaming ingestion, ClickHouse Cloud for zero-ops, extreme compression.
- **Weaknesses:** Poor for point lookups and mutations; limited JOIN optimizer vs. BigQuery; requires careful sort-key design upfront; community support smaller than BigQuery/Snowflake.
- **Team fit:** Data engineers comfortable with SQL and columnar concepts. Excellent for product analytics stacks (Posthog, Plausible use it internally).
- **Scale fit:** Petabyte-scale analytics on self-managed clusters or ClickHouse Cloud.
- **Production risks:** Suboptimal primary key destroying query performance; unbounded mutations filling tmp space; TTL not set on high-volume tables.

---

## Redshift (AWS)

- **When to use:** AWS-native analytics shops, organizations with large existing AWS data pipelines (S3, Glue, Kinesis), workloads needing tight IAM integration, Redshift Serverless for variable workloads.
- **When NOT to use:** Teams not on AWS; workloads better served by ClickHouse (real-time) or BigQuery (serverless convenience); new projects where Snowflake or BigQuery offer better dev experience.
- **Strengths:** Deep AWS ecosystem integration (S3, Glue, Kinesis, SageMaker), Redshift Spectrum for querying S3 without loading, Redshift Serverless auto-scales to zero, columnar MPP at petabyte scale.
- **Weaknesses:** Cluster management complexity (node types, sort/dist keys); historically weaker DX than Snowflake/BigQuery; COPY performance requires careful tuning; vacuum/analyze maintenance overhead.
- **Team fit:** AWS-native data engineering teams, organizations with Glue + S3 data lakes already built.
- **Scale fit:** Petabyte-scale with RA3 nodes. Serverless handles variable workloads.
- **Production risks:** Skewed distribution keys causing hot nodes; vacuum not keeping up with delete-heavy workloads; WLM queue management complexity.

---

## Kafka / Kinesis / Pub/Sub

- **When to use:** Decoupling producers from consumers in event-driven architectures, streaming data ingestion at high throughput, event log as a durable replayable source of truth, real-time pipelines feeding multiple consumers.

### Apache Kafka
- **Use when:** High-throughput event streaming, multi-consumer fan-out, exactly-once semantics needed, long message retention (replay from beginning), on-premise or cloud-agnostic. Confluent Cloud or AWS MSK for managed.
- **Risk:** High operational complexity self-hosted; Zookeeper/KRaft management; consumer group rebalancing causing lag spikes; schema registry needed to prevent chaos.

### AWS Kinesis
- **Use when:** AWS-native, simpler throughput requirements, 24-hour default retention is sufficient, team wants managed service without Kafka complexity. Kinesis Data Streams + Firehose for S3 delivery.
- **Risk:** 24h default retention (extendable to 365 days at cost); shard management at scale; less ecosystem than Kafka.

### Google Pub/Sub
- **Use when:** GCP-native, serverless, auto-scaling message bus. BigQuery subscription delivers directly to BigQuery tables. Simple and well-integrated in GCP.
- **Risk:** At-least-once delivery (idempotent consumers required); no message ordering guarantee without ordering keys; message retention limited.

**Team fit:** Kafka for platform teams and complex streaming; Kinesis for AWS teams preferring managed; Pub/Sub for GCP teams.

---

## dbt (Data Build Tool)

- **When to use:** SQL-based transformation layer for any warehouse. The standard tool for building modular, tested, documented transformation pipelines. Works with BigQuery, Snowflake, Redshift, ClickHouse, PostgreSQL, DuckDB.
- **When NOT to use:** Spark/PySpark-heavy transformations too large for SQL; teams with no SQL knowledge; real-time row-by-row processing (dbt is batch/micro-batch).
- **Strengths:** SQL models with Jinja templating, built-in testing (not-null, unique, referential integrity, custom), documentation site generation, lineage DAG, dbt Cloud for managed scheduling/CI, incremental models for efficiency.
- **Weaknesses:** SQL-only (complex Python logic requires dbt-python models or separate pipelines); lineage breaks with external tools not modeled in dbt; large projects need careful DAG structure to avoid slow builds.
- **Team fit:** Analytics engineers, SQL-first data teams. The standard; adopt by default.
- **Scale fit:** Works at any warehouse scale — dbt itself is just a SQL compiler. Cloud handles the compute.
- **Production risks:** Missing `--select` on production runs rebuilding everything; untested models silently producing bad data; circular references in DAG; schema drift in source systems breaking models.

---

## Orchestration: Airflow / Dagster / Prefect

- **When to use:** Scheduling and monitoring data pipelines, managing dependencies between tasks, retrying failures, alerting on SLA breaches. Every production data platform needs an orchestrator.

### Apache Airflow
- **Use when:** Standard in data engineering, large community, wide operator ecosystem (S3, BigQuery, Snowflake, dbt, Spark), MWAA (AWS managed) or Cloud Composer (GCP managed) for zero-ops.
- **Risk:** Python DAG code runs at import time causing scheduler overhead; dynamic DAGs are complex; UI is dated; scheduler/worker architecture requires maintenance.
- **Team fit:** All data teams. Airflow is the lingua franca.

### Dagster
- **Use when:** Software-engineering-first teams that want typed assets, built-in data quality checks, first-class dbt integration, and a modern UI. Better local development experience than Airflow.
- **Risk:** Steeper initial learning curve; smaller community than Airflow; Dagster Cloud pricing for managed.
- **Team fit:** Teams building data asset-centric pipelines, SWE-heavy data teams.

### Prefect
- **Use when:** Python-native teams wanting minimal boilerplate, decorator-based flows, simple dynamic task mapping, Prefect Cloud for managed runs. Fastest to get started.
- **Risk:** Less mature ecosystem than Airflow; Prefect Cloud required for persistent history/UI (self-hosted Prefect server is more limited).
- **Team fit:** Python teams wanting quick setup over configuration depth.

---

## Spark / Flink

### Apache Spark
- **When to use:** Large-scale batch processing that outgrows SQL-only tools, ML feature engineering at scale, ETL across terabytes of files (Parquet, Delta, Iceberg), PySpark for Python-first teams. Managed via Databricks, EMR, or Dataproc.
- **When NOT to use:** Sub-minute latency requirements (Flink is better); small datasets (<100GB — SQL in ClickHouse/BigQuery is faster); teams without Spark/JVM knowledge.
- **Strengths:** Unified batch/stream (Structured Streaming), DataFrame and SQL APIs, MLlib for ML, Delta Lake / Iceberg for ACID lakehouse, massive community, runs everywhere.
- **Weaknesses:** JVM complexity and tuning (GC pauses, executor memory); slow job startup; over-provisioning waste; Databricks pricing is high for heavy usage.
- **Production risks:** OOM from skewed data; small file problem on S3/HDFS output; shuffle spill to disk killing performance; unpredictable cluster costs.

### Apache Flink
- **When to use:** True stateful stream processing with sub-second latency, complex event patterns (CEP), exactly-once guarantees in streaming, large-scale real-time aggregations feeding serving layers.
- **When NOT to use:** Batch-only workloads (Spark is simpler); teams without JVM/streaming expertise; early-stage projects where event-driven architecture is speculative.
- **Strengths:** True streaming (not micro-batch), stateful operations with RocksDB-backed state, exactly-once via checkpointing, event time processing, FlinkSQL for SQL over streams.
- **Weaknesses:** High operational complexity; JVM-heavy; checkpoint recovery time under large state; smaller community than Spark; Flink-on-Kubernetes config is non-trivial.
- **Production risks:** State backend misconfiguration causing checkpoint failures; checkpoint interval too long (large recovery time); backpressure cascades; JAR dependency conflicts.

---

## Comparison Table

| Component | Category | Ops Complexity | Latency | Cost Model | Best For |
|---|---|---|---|---|---|
| BigQuery | Warehouse | None (serverless) | Seconds | Per query / slot | GCP analytics, serverless |
| Snowflake | Warehouse | Low (managed) | Seconds | Credit-based | Multi-cloud, data sharing |
| ClickHouse | OLAP DB | Medium | Sub-second | Infra / Cloud | Real-time analytics, logs |
| Redshift | Warehouse | Medium | Seconds | Node/hour or serverless | AWS-native analytics |
| Kafka | Streaming | High | Milliseconds | Infra / Confluent | High-throughput event bus |
| Kinesis | Streaming | Low (managed) | Seconds | Per shard-hour | AWS-native streaming |
| Pub/Sub | Streaming | None (serverless) | Seconds | Per message | GCP-native messaging |
| dbt | Transform | Low | N/A (compiler) | Free / dbt Cloud | SQL transformations |
| Airflow | Orchestration | Medium | N/A | Infra / MWAA | Standard pipeline scheduling |
| Dagster | Orchestration | Low-Medium | N/A | Infra / Cloud | Asset-centric, SWE teams |
| Prefect | Orchestration | Low | N/A | Infra / Cloud | Python-first, fast setup |
| Spark | Batch compute | High | Minutes | Cluster / Databricks | Large-scale batch, ML features |
| Flink | Stream compute | Very High | Milliseconds | Cluster / managed | Stateful real-time streams |

---

## Recommended Combinations

- **BigQuery + dbt + Airflow (Cloud Composer) + Pub/Sub** — GCP-native modern data stack. Pub/Sub ingests events, Airflow orchestrates dbt transformations, BigQuery serves analytics. Low ops overhead.
- **Snowflake + dbt Cloud + Fivetran/Airbyte** — Cloud-agnostic ELT: Fivetran/Airbyte for ingestion, dbt Cloud for transformation, Snowflake as warehouse. Fast to production, strong governance.
- **Kafka + Flink + ClickHouse** — Real-time analytics stack: Kafka ingests, Flink aggregates, ClickHouse serves sub-second dashboards. Adopted by Cloudflare, ByteDance, Uber at scale.
- **S3 (Delta Lake/Iceberg) + Spark (Databricks) + dbt + Airflow** — Open lakehouse: raw files in S3 with ACID via Delta/Iceberg, Spark for heavy ETL, dbt for SQL layer, Airflow for scheduling.
- **Kinesis + Lambda + Redshift (Serverless) + dbt** — AWS-native streaming to warehouse: Kinesis ingests, Lambda transforms and loads, Redshift Serverless for analytics, dbt for models.
- **Kafka + Spark Structured Streaming + BigQuery** — Micro-batch streaming: Kafka for durable events, Spark Structured Streaming for windowed aggregations, BigQuery as sink for analysis.
- **Postgres (source) + Airbyte + ClickHouse + Metabase** — Lean product analytics: replicate operational DB to ClickHouse via Airbyte, Metabase for dashboards. Cost-effective for startups.
- **Dagster + dbt + Snowflake + Great Expectations** — Data quality-first: Dagster assets wrap dbt models, Great Expectations validates data at each stage, Snowflake stores results.

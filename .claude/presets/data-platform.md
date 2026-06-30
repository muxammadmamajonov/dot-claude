# Data Platform Preset

## Project type

A system whose primary purpose is to move, store, transform, and serve data at scale. Encompasses data lakes, data warehouses, lakehouses, ETL/ELT pipelines, streaming ingestion, CDC (change-data capture), reverse ETL, BI and analytics layers, data quality / observability tooling, feature stores for ML, and data governance platforms. The data platform is often a horizontal capability used by many upstream producers and downstream consumers across the organisation.

---

## Typical use cases

- Centralised data warehouse or lakehouse (Snowflake, BigQuery, Databricks, Redshift)
- Batch ETL/ELT pipeline (dbt + orchestrator, Spark, Beam)
- Real-time streaming ingestion and processing (Kafka + Flink / Spark Structured Streaming)
- CDC pipeline (Debezium → Kafka → sink to warehouse or lake)
- Reverse ETL (warehouse → operational systems: CRM, marketing automation)
- BI and analytics layer (Looker, Metabase, Superset, Redash, Tableau)
- Feature store for ML model training and serving (Feast, Tecton, Vertex AI Feature Store)
- Data quality / observability platform (Great Expectations, Soda, Monte Carlo)
- Data governance, cataloguing, and lineage (DataHub, Amundsen, Alation, OpenMetadata)
- Data API / semantic layer serving data products to downstream consumers

---

## Required discovery questions

1. **Data sources** — What systems produce data that must flow into this platform? (Databases, SaaS APIs, event streams, files, IoT devices.) What is the data volume and velocity per source (rows/day, GB/hour)?
2. **Consumers and use cases** — Who consumes the data and how? (BI analysts via SQL, ML engineers via feature store, application developers via API, data scientists via notebooks.) Use cases determine the serving layer design.
3. **Batch vs. streaming** — Which pipelines require near-real-time freshness (< 5 minutes) vs. daily batch is fine? Streaming adds significant operational complexity and cost.
4. **Data freshness SLAs** — For each key dataset, what is the maximum acceptable age of data before a business decision is impaired? These are your SLA targets and the basis for alerting.
5. **Scale targets** — Expected daily data volume ingested (GB/TB), number of tables/models, number of concurrent BI users, and peak query load? Scale drives warehouse and compute sizing.
6. **PII and compliance** — What categories of personal, financial, or health data flow through the platform? Which jurisdictions and regulations apply (GDPR, CCPA, HIPAA, PCI)? This drives masking, retention, access control, and audit requirements.
7. **Data quality and trust** — What level of data quality is required? Are there existing quality issues in source systems that must be detected and handled? What happens when bad data reaches the serving layer?
8. **Existing infrastructure** — Is there an existing data stack to migrate or integrate with? What cloud provider, warehouse, and orchestrator are already in use or mandated?
9. **Team ownership model** — Who owns pipeline code? Central data engineering team, embedded team per domain, or self-serve model where domain teams write their own pipelines? This determines the platform layer design.
10. **Cost constraints** — What is the monthly budget for warehouse compute, storage, and tooling? Warehouse costs can scale non-linearly with query volume; cost governance must be designed in from the start.

---

## Recommended agents

**Core**
- `.claude/agents/core/orchestrator.md` — drives the 9-stage flow; data platforms require thorough spec before any pipeline code
- `.claude/agents/core/solution-architect.md` — zone architecture (bronze/silver/gold), storage formats, ingestion patterns, serving layer design
- `.claude/agents/core/requirements-engineer.md` — data contracts, SLAs, quality requirements, access control policies

**Engineering**
- `.claude/agents/engineering/data-engineer.md` — pipeline implementation, dbt models, Spark jobs, orchestration DAGs, data quality checks
- `.claude/agents/engineering/backend-engineer.md` — data API / semantic layer, reverse-ETL triggers, data product APIs
- `.claude/agents/engineering/cloud-architect.md` — cloud storage, compute sizing, warehouse configuration, network topology
- `.claude/agents/engineering/infrastructure-engineer.md` — orchestrator deployment (Airflow, Dagster, Prefect), Kafka cluster, Spark cluster, CI/CD for pipelines

**Quality**
- `.claude/agents/quality/qa-engineer.md` — pipeline test strategy, golden dataset validation, end-to-end data integrity tests
- `.claude/agents/quality/security-auditor.md` — PII data flow audit, column-level masking, row-level security, access control review

**Domain**
- `.claude/agents/domain/ai-agent-domain-expert.md` — if ML feature store or AI-powered data quality is in scope

---

## Recommended skills

- `.claude/skills/data-platform/SKILL.md` — zone architecture, data contracts, ingestion patterns, dbt workflow, orchestration, data quality gates, governance
- `.claude/skills/data-modeling/SKILL.md` — star schema, dimensional modelling, fact/dimension design, slowly-changing dimensions
- `.claude/skills/clickhouse/SKILL.md` — if ClickHouse is used for high-throughput OLAP or event analytics
- `.claude/skills/postgres/SKILL.md` — operational database patterns, CDC source configuration, metadata store
- `.claude/skills/redis/SKILL.md` — feature store serving layer, result caching, rate limiting on data APIs
- `.claude/skills/python-backend/SKILL.md` — Spark jobs, pipeline scripts, data quality checks, orchestrator plugins
- `.claude/skills/docker-kubernetes/SKILL.md` — containerised pipeline deployment, Airflow on Kubernetes, Spark on K8s
- `.claude/skills/security/SKILL.md` — PII masking, column-level security, secret management in pipeline code, audit logging

---

## Recommended stack options

| Stack | Rationale |
|---|---|
| **dbt + Snowflake/BigQuery + Airflow/Dagster + Great Expectations** | Most common modern data stack; strong ecosystem, managed warehouse eliminates ops overhead; dbt provides version-controlled SQL transformations; best starting point for new platforms. See `.claude/skills/data-platform/SKILL.md`. |
| **Apache Spark + Delta Lake / Apache Iceberg + Airflow + Databricks** | Best for very large data volumes (TB–PB), complex ML feature engineering, or teams already on Databricks; unified batch and streaming; lakehouse format enables time-travel and schema evolution. |
| **Kafka + Flink / Spark Structured Streaming + Iceberg + dbt** | Needed when sub-5-minute data freshness is a hard requirement; Kafka as the durable event log; Flink for stateful stream processing; Iceberg as the real-time lake table format. |
| **ClickHouse + Kafka + dbt-clickhouse + Grafana** | High-throughput event analytics (billions of rows/day) at low cost; excellent for product analytics, log analytics, and time-series use cases; less suited for complex multi-join SQL typical in finance/ERP. |

---

## Required checklists

- `.claude/checklists/security.md` — PII column masking, row-level security, secret management in DAG code, access control audit, data retention enforcement
- `.claude/checklists/performance.md` — query latency SLAs per consumer, pipeline duration SLAs, warehouse cost per job, partition and clustering strategy
- `.claude/checklists/qa.md` — row-count checks, uniqueness, referential integrity, freshness SLA, schema drift detection, golden dataset tests
- `.claude/checklists/production.md` — backfill strategy documented, disaster recovery tested (RPO/RTO per pipeline), SLA monitoring and alerting, runbooks for common failure modes

---

## MVP scope pattern

**In the first cut**
- One source system ingested end-to-end to a queryable gold/serving table (prove the pipeline works)
- Raw zone: land data unchanged as Parquet/JSONL partitioned by ingestion date; append-only; never modified
- One dbt staging model and one mart/aggregate model downstream of it; tests on both
- Basic orchestration: the pipeline runs on a schedule, fails loudly with an alert, and is idempotent on re-run
- Data quality gate: row-count non-zero, primary key uniqueness, freshness within SLA — all automated checks
- Access control: analysts get read-only access to gold layer only; raw and silver are restricted to data engineering

**Defer until post-MVP**
- Streaming / real-time ingestion (batch first; add streaming when a use case with < 5 min SLA is confirmed)
- Full data catalogue and automated lineage (emit OpenLineage events from day one; catalogue UI deferred)
- Data governance portal / self-serve access request (enforce access control from day one, self-serve UI later)
- Reverse ETL (design the output contracts, implement the sync jobs after gold tables are stable)
- Feature store (build and validate features in notebooks first, productionise into a feature store later)
- Full multi-source ingestion (add one source at a time; don't build all ingestion in parallel)
- BI dashboard tooling (analysts can query with SQL client first; BI tool added when the data model is stable)

---

## Production risks

| Risk | Priority | Mitigation |
|---|---|---|
| No idempotency — re-run inserts duplicates | P0 | All pipelines use `MERGE`/`UPSERT` or partition-overwrite; never plain `INSERT` for incremental loads; tested on every PR |
| PII written to unmasked tables and accessed by unauthorised roles | P0 | Column-level masking configured before any PII reaches the warehouse; access control audit in `.claude/checklists/security.md` |
| Schema drift — upstream drops or renames a column, pipeline silently writes nulls | P0 | Enforce data contracts at ingestion with JSON Schema or Great Expectations; fail the pipeline and alert on contract violation |
| Credentials in DAG code or Spark configs committed to VCS | P0 | All secrets via secret manager (Vault, AWS Secrets Manager, GCP Secret Manager); pre-commit hook blocks `.env` commits |
| Pipeline runs on stale or failed upstream data without detection | P1 | Use sensors / data availability checks before transformation steps; never start a transform DAG on an empty or partial source partition |
| Warehouse cost runaway from untuned queries or missing partition filters | P1 | Query cost governance: label every production query; alert on queries exceeding cost threshold; partition pruning enforced in dbt models |
| Missing backfill strategy — pipeline only designed for incremental, breaks on historical replay | P1 | Backfill procedure documented in runbook before any pipeline goes to production; tested on at least 7-day historical replay |
| Timezone inconsistency causing off-by-one day partitioning | P1 | Standardise all timestamps to UTC at ingestion; add `_ingested_at_utc` on every raw record |
| Raw zone overwritten or mutated by a transformation job | P1 | IAM/RBAC: transformation service accounts have no write access to raw zone; raw zone is append-only enforced at storage level |
| Data quality failure reaching gold tables undetected | P1 | Quality gates between every zone transition; pipeline stops and alerts when a gate fails; never auto-promote bad data |

---

## Launch requirements

- All items in `.claude/checklists/production.md` are green
- Every production pipeline is idempotent: re-run on the same partition produces identical results (tested)
- Data quality checks pass for all gold tables: uniqueness, not-null, freshness within SLA, referential integrity
- PII audit complete: every PII field documented with masking rule, retention period, and access scope
- Backfill playbook tested: replayed 30 days of historical data with no duplicates in serving tables
- Disaster recovery tested: simulated loss of one pipeline; confirmed data can be replayed from raw zone within RPO
- SLA monitoring live: freshness alerts fire within 5 minutes of a table missing its SLA window
- Cost governance active: per-job cost tracked; daily spend alert configured
- Access control verified: analyst role cannot read raw or silver zone; no credentials in pipeline code
- Lineage captured: OpenLineage events emitted from orchestrator; queryable for at least 90 days
- Runbooks complete: pipeline failure, schema drift incident, backfill, warehouse cost spike, PII breach
- All P0/P1 bugs resolved; P2 triaged

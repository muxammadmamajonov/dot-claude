# Search Stack Matrix

Choose based on four axes: **query flexibility** (full-text vs. structured vs. vector/semantic), **operational model** (managed vs. self-hosted), **scale** (document count and QPS), and **relevance tuning** needs. A product catalog search and a petabyte log analytics cluster have nothing in common — pick the tool sized to the problem.

Key drivers: document volume, query latency SLA, relevance control needed, vector/hybrid search requirement, engineering bandwidth for ops, and budget.

---

## Elasticsearch

**When to use**
- Full-text search with complex queries: nested objects, aggregations, geospatial, percolators
- Log and observability data (ELK/EFK stack)
- Large scale: billions of documents, complex relevance scoring (BM25 + custom)
- Need fuzzy matching, autocomplete, synonyms, language analyzers out of the box
- Hybrid dense+sparse vector search (kNN + BM25 combined in 8.x+)

**When NOT to use**
- Small projects that don't justify JVM/cluster ops overhead
- Strict relevance without custom scoring — defaults are powerful but hard to tune simply
- Budget-sensitive projects: Elastic Cloud is expensive at scale; self-hosting requires ops expertise
- Teams needing a simple hosted search-as-a-service with zero config

**Strengths**
- Battle-tested at enormous scale (Wikipedia, GitHub, Uber)
- Rich aggregation framework: facets, histograms, date ranges, pipeline aggregations
- Lucene underneath: best-in-class inverted index performance
- Strong ecosystem: Kibana, Logstash, Beats, APM, Security features
- kNN vector search with HNSW indexes and hybrid scoring since 8.x

**Weaknesses**
- JVM memory management and GC tuning is non-trivial
- Shard management, hot-warm-cold tiering — significant ops surface area
- Lucene query DSL is verbose; easy to write slow queries accidentally
- License changed to SSPL in 7.11 — not true open source

**Team fit**
- Platform/DevOps teams; data engineering; companies with dedicated search engineers
- Java/JVM shops comfortable with heap tuning

**Scale fit**
- Proven to hundreds of billions of documents. Effective at any scale with correct shard sizing.

**Risks**
- "Oversharding" is a common trap — too many small shards kill cluster stability
- Cross-cluster search and replication complexity in multi-region setups
- License (SSPL) means it cannot be offered as a managed service by others

---

## OpenSearch

**When to use**
- Need Elasticsearch-compatible API under a true open-source license (Apache 2.0)
- AWS workloads: OpenSearch Service (managed) integrates natively with IAM, VPC, CloudWatch
- Replacing Elasticsearch post-7.10 in regulated industries requiring OSS licensing
- Need ML-powered features: neural search, anomaly detection, PPL query language

**When NOT to use**
- Need the absolute latest Elastic features (vector search, ES|QL) — OpenSearch lags by 12–18 months on some capabilities
- Non-AWS cloud: OpenSearch Service is an AWS product; self-hosting elsewhere loses managed benefit

**Strengths**
- True Apache 2.0 license; AWS-backed with active community
- API-compatible with Elasticsearch 7.10 — most clients/tooling work unchanged
- Neural search: semantic search with text-embedding models integrated natively
- OpenSearch Dashboards (Kibana fork) included

**Weaknesses**
- Feature parity with modern Elasticsearch is not guaranteed; diverging over time
- AWS-managed service has VPC/endpoint quirks; not as seamless outside AWS

**Team fit**
- AWS-centric teams replacing Elasticsearch for licensing or managed-service reasons
- Teams building regulated products needing OSS without SSPL concerns

**Scale fit**
- Same as Elasticsearch; OpenSearch Service scales to petabytes with UltraWarm/cold storage tiers

**Risks**
- Divergence from Elasticsearch may create migration friction later
- Community is smaller than Elastic's; fewer third-party plugins

---

## Meilisearch

**When to use**
- Developer-facing product search: e-commerce, SaaS in-app search, documentation search
- Need instant search-as-you-type with <50 ms response times by default
- Small-to-medium datasets (<100 M documents) with minimal ops
- Want simple REST API with sensible relevance defaults, typo-tolerance, faceting

**When NOT to use**
- Complex aggregations or analytics on search results
- Multi-petabyte datasets — Meilisearch is single-node; clustering is experimental
- Need log/observability search, geospatial queries, or nested document scoring
- Production requires HA with automatic failover today (clustering in beta)

**Strengths**
- Out-of-the-box relevance: typo tolerance, synonym support, stop words, custom ranking
- Sub-50 ms queries on typical datasets — no tuning needed
- Simple HTTP API; SDKs for all major languages; embed in minutes
- Lightweight Rust binary; easy Docker deployment
- Vector search (semantic search) supported since v1.6

**Weaknesses**
- Single-node architecture; horizontal scaling not yet production-stable
- Less flexible relevance customization than Elasticsearch
- No aggregation pipeline for analytics use cases
- Dataset size bounded by RAM+disk on a single machine

**Team fit**
- Product engineers who want working search without a search specialist
- Startups and mid-size SaaS products

**Scale fit**
- Sweet spot: 1 M–50 M documents. Tens of millions of queries/day on single large instance.

**Risks**
- Cluster/HA limitations mean planned downtime for upgrades
- Index rebuilds block writes (task queue); large index builds can be slow

---

## Typesense

**When to use**
- Instant search for product catalogs, directories, in-app search on datasets up to ~100 M docs
- Want Meilisearch alternative with built-in clustering (Typesense Cluster) for HA
- Need vector search + keyword search hybrid out of the box
- Want hosted option (Typesense Cloud) without self-hosting ops

**When NOT to use**
- Complex aggregations, log analytics, or deeply nested document models
- Datasets requiring petabyte-scale distributed indexing
- Need full Elasticsearch query DSL compatibility

**Strengths**
- Multi-node clustering with leader election — HA without external orchestration
- Typo-tolerance, faceting, geo search, dynamic sorting native
- Hybrid vector + keyword search in single query
- Clean REST API and SDKs; InstantSearch.js adapter available
- Faster cold-start than Elasticsearch; written in C++

**Weaknesses**
- Smaller ecosystem than Elasticsearch; fewer community integrations
- Collection schema changes require reindex
- Limited aggregation support compared to Elasticsearch

**Team fit**
- Product/fullstack engineers; teams that tried Meilisearch but need clustering
- JavaScript/React/Vue frontends using InstantSearch

**Scale fit**
- Up to ~100 M documents per cluster; horizontal sharding across nodes

**Risks**
- Hosted cloud pricing can exceed Algolia at scale
- Schema evolution is more painful than schema-less systems

---

## Algolia

**When to use**
- Need hosted, zero-ops search with SLA-backed 99.999% uptime
- E-commerce, marketplace, or media site where developer time is more expensive than search cost
- Want InstantSearch UI components (React, Vue, Angular, iOS, Android) out of the box
- Need A/B testing of search ranking, analytics dashboard, personalization features

**When NOT to use**
- Cost-sensitive products: Algolia is expensive at scale (priced per 1 k search operations + records)
- Datasets requiring complex joins, aggregations, or log-style queries
- Need full-text flexibility or custom scoring algorithms beyond Algolia's ranking formula
- Regulated industries requiring data residency control — Algolia is SaaS-only

**Strengths**
- Best-in-class developer experience and time-to-production (minutes, not hours)
- Global CDN-backed: <10 ms queries from anywhere
- InstantSearch libraries are production-grade and maintained by Algolia
- Rich analytics: click-through rates, zero-result queries, conversion tracking
- NeuralSearch (vector + keyword hybrid) in recent versions

**Weaknesses**
- Cost: can be 10–50x more expensive than self-hosted alternatives at scale
- Limited control over ranking internals — black box beyond custom ranking formula
- Record size limits and attribute limits require data modeling discipline
- No self-hosting option

**Team fit**
- Product teams optimizing for speed-to-market over infra cost
- E-commerce teams needing merchandising, pinning, A/B testing on search

**Scale fit**
- Proven at billions of search operations/month; pricing becomes prohibitive before scale limits hit

**Risks**
- Vendor lock-in is significant; InstantSearch binds UI to Algolia API shape
- Cost overruns if indexing or search volume spikes unexpectedly
- Data leaves your infrastructure — compliance consideration for PII in documents

---

## pgvector / PostgreSQL Full-Text Search

**When to use**
- Already on PostgreSQL; want search without a new system
- Semantic/vector search on moderate datasets (<5 M vectors reasonably; 10–50 M with pgvector 0.7+ HNSW)
- Simple keyword search on structured data where FTS adequacy is good enough (tsvector + GIN index)
- Hybrid search: combine SQL filters with vector similarity in one query

**When NOT to use**
- High QPS full-text search on large document corpora — Postgres FTS does not scale like dedicated search engines
- Need typo tolerance, autocomplete, faceting, or synonym engines out of the box
- Datasets >50 M vectors where HNSW memory usage becomes prohibitive
- Sub-10 ms p99 latency at thousands of QPS on complex queries

**Strengths**
- Zero new infrastructure if Postgres is already running
- ACID transactions: update document and search index atomically
- SQL joins: filter search results by relational conditions in one query
- pgvector 0.7+: HNSW indexing with good recall/speed trade-offs
- FTS with ts_rank, phrase search, dictionaries — sufficient for many internal tools

**Weaknesses**
- Relevance quality below dedicated search engines; no BM25 by default (pg_bm25 extension available via ParadeDB)
- FTS index maintenance adds write amplification on high-write tables
- No typo tolerance, autocomplete, or faceting out of the box
- Vector search memory: HNSW index lives in RAM; large indexes require large Postgres instances

**Team fit**
- Teams wanting to avoid new infrastructure; data-heavy applications already on Postgres
- Internal tools, admin panels, small product search

**Scale fit**
- FTS: up to ~10 M rows with proper GIN indexing. Vectors: up to ~50 M with HNSW on large memory instances.

**Risks**
- Mixing heavy search load with OLTP on the same Postgres instance causes resource contention
- Search quality may require switching to a dedicated engine later — plan for migration

---

## Vespa

**When to use**
- Combine ranking, vector search, filtering, and ML-computed features in one system
- Large-scale retrieval + ranking pipeline: news feed, recommendation, ad serving
- Need real-time index updates with zero-downtime scaling (streaming updates)
- Want to embed custom ML models (ONNX) directly in the ranking pipeline

**When NOT to use**
- Simple product/document search without custom ranking models
- Small teams — Vespa has a steep learning curve and verbose XML/JSON configuration
- Need a fully managed SaaS with minimal setup (Vespa Cloud exists but less polished than Algolia)

**Strengths**
- Unified vector search + BM25 + structured filtering in a single query
- Inline ML ranking: deploy ONNX models; rank with tensor computations in query path
- Stateful streaming updates: documents update in real-time without reindex
- True distributed: horizontal scaling with automatic resharding
- Used by Yahoo, Spotify, OkCupid — proven at extreme scale

**Weaknesses**
- Configuration complexity: application packages, search definitions, rank profiles — steep learning curve
- Smaller community and ecosystem vs. Elasticsearch
- Debugging relevance requires deep understanding of rank profiles and match phases
- Vespa Cloud (managed) is less mainstream than Elastic Cloud or Algolia

**Team fit**
- Dedicated search/ML engineering teams; companies building recommendation or personalization systems
- Organizations willing to invest in search as a core competency

**Scale fit**
- Petabyte-scale document stores; hundreds of thousands of QPS with proper fleet sizing

**Risks**
- Operational complexity rivals Elasticsearch without equivalent community resources
- Application package redeployment required for schema changes — affects uptime if not managed carefully

---

## Comparison Table

| Criterion | Elasticsearch | OpenSearch | Meilisearch | Typesense | Algolia | pgvector/FTS | Vespa |
|---|---|---|---|---|---|---|---|
| **Query flexibility** | Very high | High | Medium | Medium | Medium | Medium (SQL) | Very high |
| **Relevance control** | High (custom scoring) | High | Medium (ranking rules) | Medium | Medium (formula) | Low–medium | Very high (rank profiles) |
| **Vector / hybrid search** | Yes (8.x+) | Yes (neural) | Yes (v1.6+) | Yes | Yes (NeuralSearch) | Yes (pgvector) | Yes (native) |
| **Typo tolerance** | Via analyzers | Via analyzers | Native | Native | Native | No | Limited |
| **Ops complexity** | High | High | Low | Low–medium | None (SaaS) | None (existing PG) | High |
| **Clustering / HA** | Yes | Yes | Beta | Yes | Managed | Via PG HA | Yes |
| **Max practical scale** | Petabytes | Petabytes | ~100 M docs | ~100 M docs | Billions of ops/mo | ~50 M vectors | Petabytes |
| **Latency (typical)** | 5–50 ms | 5–50 ms | <50 ms | <50 ms | <10 ms (CDN) | 10–100 ms | 5–30 ms |
| **Managed option** | Elastic Cloud | AWS OpenSearch | Meilisearch Cloud | Typesense Cloud | SaaS only | Any PG provider | Vespa Cloud |
| **License** | SSPL | Apache 2.0 | MIT | Apache 2.0 | Proprietary SaaS | PostgreSQL | Apache 2.0 |
| **Aggregations / analytics** | Excellent | Excellent | Basic | Basic | Basic | SQL-native | Good |
| **Best for** | Logs, complex FT search | AWS OSS search | In-app product search | HA instant search | E-commerce SaaS | Simple/semantic on PG | Ranking + ML at scale |

---

## Recommended Combinations

| Combination | Why |
|---|---|
| **Elasticsearch + Kibana + Logstash** | Classic ELK stack for log aggregation and observability; battle-tested at any scale. |
| **Algolia + InstantSearch.js** | Fastest path to production e-commerce or SaaS search; zero ops, great UI components. |
| **Typesense + Typesense Instantsearch Adapter** | Open-source Algolia alternative with clustering; self-host for cost control, keep InstantSearch UX. |
| **Meilisearch + Next.js** | Documentation sites, in-app search for small/mid SaaS products; instant results, minimal infra. |
| **pgvector + pgai (Timescale)** | RAG pipelines on Postgres; embed generation + vector search without leaving SQL. |
| **OpenSearch Service + Amazon Kendra** | AWS: OpenSearch for keyword/faceted search; Kendra for enterprise semantic document search. |
| **Vespa + ONNX model serving** | Production ML-ranked search: embed ranking models directly, skip a separate feature store for retrieval. |
| **Elasticsearch (write) + Typesense (read)** | Dual-write pattern: rich indexing/analytics in ES; fast, cheap read path in Typesense for user-facing search. |

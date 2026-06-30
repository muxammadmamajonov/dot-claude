---
name: search
description: >
  Activate for any search, relevance, or discovery feature. Triggers: full-text search,
  faceted search, autocomplete/typeahead, vector/semantic search, hybrid search,
  Elasticsearch, OpenSearch, Meilisearch, Typesense, Solr, pgvector, Weaviate,
  Qdrant, Pinecone, ranking/scoring, synonym handling, search index sync, relevance tuning.
---

# Search & Relevance

**Scope: retrieval & relevance. Event analytics → `.claude/skills/analytics/SKILL.md`.**

## When to use
- Adding search to an application (product catalogue, docs, users, content)
- Improving relevance or ranking of existing search
- Adding semantic / AI-powered search (embeddings + vector DB)
- Implementing hybrid search (BM25 + vector recall merged with RRF)
- Designing index sync pipeline from primary DB to search engine
- Facets, filters, aggregations, geo-search, autocomplete
- Multi-tenant search with per-tenant index or filter isolation

## Workflow

1. **Clarify requirements** — corpus size (docs count + avg size), query types (keyword, semantic, mixed), latency SLA (p99 <X ms), language(s), facets needed, freshness requirement (real-time vs eventually consistent), multi-tenancy?
2. **Select engine** — Use decision matrix in Standards.
3. **Design index schema** — Fields, data types, analyzers per language, `keyword` vs `text` mappings (ES/OS), sortable/filterable flags (Meilisearch/Typesense), dense_vector dimension.
4. **Build indexing pipeline** — Source of truth → transformer → bulk index. For real-time: CDC (Debezium) or application-level dual-write. Batch: scheduled full re-index weekly + incremental sync on change events.
5. **Implement query layer** — BM25 for keyword, ANN (HNSW) for vector. Hybrid: reciprocal rank fusion (RRF) or linear combination. Boost recency/popularity via `function_score` or equivalent.
6. **Tune analyzers** — Language-specific tokenization (ICU plugin, kuromoji for Japanese). Custom synonym files per domain. Edge-ngram for prefix autocomplete. Phonetic/stemming for recall.
7. **Relevance evaluation** — Define golden dataset (query + expected top-K). Measure NDCG@10, MRR. Run A/B or shadow test before promoting ranking changes.
8. **Add facets & filters** — Keyword-mapped fields for facets. Cache heavy aggregations. Pagination with `search_after` (not `from+size` past 10k).
9. **Observability** — Log query, latency, result count, zero-result rate. Alert on p99 > SLA. Track zero-result queries weekly for gaps.
10. **Security** — Tenant isolation: per-tenant index or mandatory filter injected server-side (never trust client). Role-based index-level permissions (ES/OS security plugin). No PII in indexed fields unless encrypted at field level.
11. **Scaling** — Shard count: 1 shard per ~30–50 GB of data. Replicas: 1 per shard in prod. For high-write: hot-warm-cold architecture.

## Standards

### Engine selection matrix

| Requirement | Best choice | Avoid |
|---|---|---|
| Large corpus (>10M docs), complex aggregations, log analytics | **Elasticsearch 8.x** or **OpenSearch 2.x** | Typesense (limited aggregations) |
| Simple full-text, fast setup, SaaS/SMB product | **Typesense 0.26+** or **Meilisearch v1.x** | Elasticsearch (operational complexity) |
| Already on Postgres, <1M docs, vector search | **pgvector 0.7+** extension | Separate infra cost |
| Pure semantic / embedding search | **Qdrant**, **Weaviate**, or **Pinecone** | BM25-only engines |
| Hybrid (keyword + vector) production | **Elasticsearch** (RRF GA in 8.14) or **OpenSearch** (neural-search plugin) | pgvector alone (no BM25) |
| Managed, AWS-native | **OpenSearch Serverless** or **Amazon Kendra** | Self-hosted Kafka |
| Offline / edge / embedded | **Tantivy** (Rust) or **MiniSearch** (JS) | Elasticsearch |

### Elasticsearch / OpenSearch index design
```json
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "analysis": {
      "analyzer": {
        "english_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "english_stop", "english_stemmer", "synonym_filter"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "title":       { "type": "text", "analyzer": "english_analyzer", "boost": 2 },
      "body":        { "type": "text", "analyzer": "english_analyzer" },
      "title_kw":    { "type": "keyword" },
      "category":    { "type": "keyword" },
      "created_at":  { "type": "date" },
      "embedding":   { "type": "dense_vector", "dims": 1536, "index": true, "similarity": "cosine" }
    }
  }
}
```
- Never use dynamic mapping in production (`"dynamic": "strict"`).
- Use `_source: false` for fields only needed for ranking, not retrieval.
- Alias indices; re-index to new index then atomically swap alias (zero-downtime schema changes).

### Hybrid search with RRF (Elasticsearch 8.14+, OpenSearch 2.11+)
```json
{
  "retriever": {
    "rrf": {
      "retrievers": [
        { "standard": { "query": { "match": { "body": "query text" } } } },
        { "knn": { "field": "embedding", "query_vector": [0.1, ...], "k": 50 } }
      ],
      "rank_window_size": 100,
      "rank_constant": 60
    }
  }
}
```
- RRF `rank_constant=60` is a reasonable default; tune via offline evaluation.
- Pre-compute embeddings with `text-embedding-3-small` (1536 dims) or `text-embedding-3-large` (3072 dims) for OpenAI; or `BAAI/bge-m3` for multilingual open-source.

### pgvector (Postgres extension ≥0.7)
```sql
CREATE EXTENSION vector;
CREATE TABLE items (id BIGSERIAL PRIMARY KEY, content TEXT, embedding vector(1536));
CREATE INDEX ON items USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);
SELECT id, content, 1 - (embedding <=> query_vec) AS score
FROM items ORDER BY embedding <=> query_vec LIMIT 20;
```
- HNSW is preferred over IVFFlat for recall (≥95% vs ~90%).
- Combine with `WHERE` clause for filtered ANN (partial index if selectivity >5%).
- `SET hnsw.ef_search = 100` at query time to trade latency for recall.

### Meilisearch / Typesense
- **Meilisearch**: configure `searchableAttributes` order (title first), `filterableAttributes`, `sortableAttributes`. Vector search via `_vectors` field. Tenant token JWTs for multi-tenancy.
- **Typesense**: schema-first (all fields declared upfront). Use `Collection aliases` for zero-downtime re-index. `drop_tokens_threshold` for partial match.

### Index sync patterns
- **Dual-write** (simplest): application writes DB + calls search index API in same request. Risk: partial failure. Use with small corpora.
- **CDC-based** (robust): Debezium captures Postgres WAL → Kafka topic → search indexer consumer. Guarantees eventual consistency without coupling.
- **Scheduled batch**: cron job queries `updated_at > last_run`, bulk-indexes changes. Latency = cron interval. Acceptable for <5 min freshness.
- **Full re-index**: always write to new index alias, then swap. Never mutate live index schema.

### Autocomplete / typeahead
- Edge-ngram analyzer on a dedicated `title.autocomplete` sub-field (min_gram=2, max_gram=10).
- Or use Elasticsearch Completion Suggester for very fast prefix lookup.
- Debounce client-side to 200–300 ms; cancel in-flight requests on new keystroke.

### Multi-tenancy isolation
- **Index-per-tenant**: strongest isolation, higher ops cost. Use when tenants number <1000 or have very different schemas.
- **Single index + filter**: mandatory `term` filter injected server-side on `tenant_id` field (keyword, not analyzed). Enable `index.query.default_field` to prevent filter bypass. Use ES/OS role-based DLS (document-level security) in enterprise setups.

## Common mistakes to avoid

- **`from + size` pagination past 10 000** — causes heap pressure; use `search_after` with sort tiebreaker.
- **Analyzing filter fields** — `category` should be `keyword`, not `text`; analyzed text cannot be reliably filtered.
- **Dynamic mapping enabled in production** — unexpected field explosions cause mapping conflicts and OOM.
- **Single shard for large corpus** — no parallelism, query bottleneck; cannot split later without reindex.
- **Embedding every document on write with synchronous API call** — slows writes; batch embed asynchronously via queue.
- **Trusting client-provided filters for tenant isolation** — always inject tenant filter server-side.
- **No zero-result monitoring** — zero-result queries are a direct revenue/UX signal; alert weekly.
- **Forgetting stopword lists per language** — English stopwords on Spanish content wrecks recall.
- **Shard count set too high** — >1 shard per 30 GB wastes resources; over-sharding is harder to fix than under-sharding.

## Output format

Produce artifacts in `docs/search/` using `.claude/templates/architecture.md` adapted for search:
- `index-schema.json` — full mapping/schema definition
- `query-patterns.md` — documented query templates (keyword, vector, hybrid, autocomplete, facets)
- `sync-pipeline.md` — indexing pipeline design (source, trigger, transform, bulk, error handling)
- `relevance-evaluation.md` — golden dataset approach, metrics (NDCG, MRR), tuning methodology
- Code examples (language matching project stack) inline as fenced code blocks

## Related checklists
- `.claude/checklists/architecture.md`
- `.claude/checklists/performance.md`
- `.claude/checklists/security.md`
- `.claude/checklists/backend.md`

## Related agents
- `.claude/agents/engineering/backend-engineer.md`
- `.claude/agents/engineering/search-engineer.md`
- `.claude/agents/engineering/data-engineer.md`
- `.claude/agents/engineering/database-architect.md`
- `.claude/agents/quality/performance-engineer.md`
- `.claude/agents/core/solution-architect.md`

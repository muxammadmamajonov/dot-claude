# AI / ML Stack Matrix

Choose your AI/ML components by separating three concerns: (1) the model provider (who runs inference), (2) the orchestration layer (how you chain calls and manage context), and (3) the retrieval/memory layer (how you ground the model in your data). These are independent choices — mix and match. Avoid over-engineering early: a direct API call often beats a full framework until retrieval or multi-step reasoning is genuinely needed.

Key decision drivers: latency requirements, cost per token, data privacy/residency, context window needs, whether you need fine-tuning, and how much vendor lock-in you can tolerate.

---

## OpenAI

- **When to use:** Default choice for production LLM applications. GPT-4o for multimodal tasks (vision + text + audio), o1/o3 for complex reasoning, GPT-4o-mini for cost-sensitive high-volume tasks. Largest third-party ecosystem.
- **When NOT to use:** Data privacy requirements that preclude sending data to third parties; latency-critical real-time inference that needs on-prem; cost-sensitive workloads at massive volume where open models are cheaper.
- **Strengths:** Best ecosystem (libraries, tools, integrations), function/tool calling is the most mature, Structured Outputs for reliable JSON, Assistants API for stateful threads, Realtime API for low-latency voice, Batch API for 50% cost reduction on async tasks.
- **Weaknesses:** Pricing premium vs. open models; data leaves your infrastructure; rate limits affect high-volume use; policy restrictions on some content; no self-hosting.
- **Team fit:** Any team. Lowest integration friction. Best starting point before evaluating alternatives.
- **Scale fit:** Enterprise tier removes rate limits. Batch API reduces cost. Azure OpenAI Service provides private endpoint + SLA for regulated industries.
- **Production risks:** Model deprecations requiring migration; prompt injection via user input; API rate limits causing cascading failures; cost runaway without token budgets; storing PII in API requests.

---

## Anthropic (Claude)

- **When to use:** Long-context tasks (200K token window), instruction-following precision, complex reasoning and analysis, document processing, code generation. Claude 3.5 Sonnet is competitive with GPT-4o on most benchmarks at lower cost.
- **When NOT to use:** Workloads requiring OpenAI-specific features (Assistants threads, Realtime API, DALL-E image generation); teams where OpenAI ecosystem lock-in is already deep.
- **Strengths:** 200K context window handles entire codebases or documents, strong on nuanced instruction following, computer use capability (beta), MCP (Model Context Protocol) for tool integration, competitive pricing, lower refusal rates on ambiguous content.
- **Weaknesses:** Smaller third-party ecosystem than OpenAI; image generation not built-in (requires third-party); Assistants-equivalent stateful API less mature; fewer community tutorials.
- **Team fit:** Teams processing large documents, long-context RAG, code generation pipelines. Good OpenAI alternative for cost optimization.
- **Scale fit:** Enterprise tier, AWS Bedrock and Google Cloud Vertex AI deployments available for private endpoints.
- **Production risks:** Same third-party data exposure risks as OpenAI; very long prompts increasing latency and cost; context window not a substitute for proper retrieval architecture.

---

## Google / Gemini

- **When to use:** Multimodal tasks requiring native video/audio understanding, workloads already in Google Cloud (Vertex AI), projects needing the longest context windows (Gemini 1.5 Pro: 1M tokens), code with Google-ecosystem integrations.
- **When NOT to use:** Teams outside the Google ecosystem; workloads where OpenAI/Anthropic tooling is preferred; latency-critical tasks (Gemini can be slower than GPT-4o-mini on simple tasks).
- **Strengths:** 1M token context window, native video/audio/image understanding, tight Vertex AI integration, competitive pricing, Gemini Flash for very fast/cheap inference, Google Search grounding built-in.
- **Weaknesses:** API less mature than OpenAI; documentation quality inconsistent; tool calling less ergonomic than OpenAI; smaller third-party ecosystem.
- **Team fit:** GCP-native teams, ML teams already using Vertex AI, multimodal projects with video/audio requirements.
- **Scale fit:** Vertex AI enterprise scaling, global Google infrastructure.
- **Production risks:** API surface changes more frequently; grounding/search integration costs; 1M context window doesn't guarantee quality at extreme lengths; model versioning complexity.

---

## Open / Local LLMs (Llama, Mistral, etc.)

- **When to use:** Data privacy requirements (data cannot leave your infrastructure), cost optimization at very high volume, fine-tuning on proprietary data, air-gapped environments, research and experimentation, latency control.
- **When NOT to use:** Teams without GPU infrastructure or ML ops capacity; tasks where frontier model quality is required; rapid prototyping (setup overhead is high).
- **Strengths:** Full data privacy, no per-token cost after infrastructure investment, fine-tunable on proprietary data, no content policy restrictions, models like Llama 3.1 405B and Mistral Large 2 approach frontier quality.
- **Weaknesses:** Requires GPU hardware (expensive) or managed serving; ops burden (model updates, serving infrastructure, quantization decisions); quality gap vs. GPT-4o/Claude on complex reasoning; no built-in tool ecosystem.
- **Team fit:** ML engineering teams, organizations with strict data compliance (healthcare, finance, defense), high-volume inference teams optimizing cost.
- **Scale fit:** vLLM, TGI, or Ollama for serving. Scales with GPU investment. Managed via Replicate, Together AI, Fireworks, or Groq for serverless open-model inference.
- **Production risks:** Model serving reliability; GPU cost overruns; quantization quality tradeoffs; keeping models updated; safety/alignment gaps vs. aligned frontier models.

---

## LangChain

- **When to use:** Rapid prototyping of chains and agents, teams wanting pre-built integrations (100+ LLM providers, vector stores, document loaders), tutorials and community examples.
- **When NOT to use:** Production systems where you need full control and minimal abstraction; teams bothered by LangChain's abstraction leaks; simple single-call LLM integrations (direct SDK is cleaner).
- **Strengths:** Huge ecosystem of integrations, LangSmith for observability and tracing, active community, LCEL (LangChain Expression Language) for composable chains, LangGraph for stateful agent workflows.
- **Weaknesses:** Heavy abstraction layers make debugging painful; API instability across versions; import overhead; can obscure what's actually happening in LLM calls; overkill for simple use cases.
- **Team fit:** Teams building complex RAG pipelines, multi-step agents, or needing fast integration with many LLM providers. Python-first.
- **Scale fit:** LangSmith scales observability. LangServe for deploying chains as APIs. LangGraph Cloud for stateful agents.
- **Production risks:** Hidden token usage from abstraction layers; silent failures in chains; LangChain version upgrades breaking pipelines; tracing overhead in high-throughput paths.

---

## LlamaIndex

- **When to use:** RAG (Retrieval-Augmented Generation) pipelines, document ingestion and indexing, building knowledge bases over structured and unstructured data. More focused on data than LangChain.
- **When NOT to use:** General-purpose agent workflows where LangChain/LangGraph is stronger; teams not doing retrieval-heavy work.
- **Strengths:** Best-in-class RAG tooling, rich document loaders (PDF, HTML, SQL, APIs), query engines, sub-question decomposition, metadata filtering, LlamaCloud for managed ingestion pipelines.
- **Weaknesses:** Less versatile than LangChain for non-RAG use cases; smaller ecosystem; Python-first (TS support is secondary).
- **Team fit:** Teams building document Q&A, enterprise search, knowledge management systems, or any RAG application.
- **Scale fit:** LlamaCloud handles large-scale document ingestion. Query engines work with any vector store backend.
- **Production risks:** Chunking strategy significantly affects quality; retrieval quality hard to evaluate without proper eval frameworks; index staleness if documents update frequently.

---

## Vector DBs: pgvector / Pinecone / Qdrant / Weaviate

- **When to use:** Semantic search, RAG retrieval, similarity search, recommendation systems, duplicate detection. Required when your retrieval needs semantic (embedding-based) rather than keyword matching.
- **When NOT to use:** Simple keyword search (use Elasticsearch); small datasets where brute-force cosine similarity in memory is fast enough; teams not doing embedding-based retrieval.

### pgvector
- Use when you already have PostgreSQL and want to avoid another database. Supports HNSW and IVFFlat indexes. Excellent for < 1M vectors. Free. Integrates with Supabase.
- Risk: Performance degrades at very high vector counts vs. dedicated vector DBs.

### Pinecone
- Managed, serverless vector DB. Best developer experience, no infra to manage. Serverless pricing scales to zero. Use for teams wanting zero-ops retrieval with fast startup.
- Risk: Vendor lock-in; cost scales with index size; no SQL alongside vectors.

### Qdrant
- Open source, self-hostable, Rust-based (fast). Rich filtering, sparse+dense hybrid search, on-disk indexing. Strong alternative to Pinecone with full data control.
- Risk: Self-hosted ops burden; smaller managed offering than Pinecone.

### Weaviate
- Open source, supports multi-tenancy, built-in vectorization modules (text2vec, img2vec). Strong for multi-modal and multi-tenant SaaS. GraphQL query interface.
- Risk: GraphQL interface unusual; heavier to self-host; JVM-like resource profile.

**Team fit:** pgvector for SQL-first teams; Pinecone for zero-ops teams; Qdrant for cost-sensitive self-hosted; Weaviate for multi-modal/multi-tenant.

---

## Eval Frameworks

- **When to use:** Any production AI system. Evals are non-negotiable before shipping an LLM feature and for detecting regressions after model/prompt updates.
- **When NOT to use:** There is no valid reason to skip evals in production.

### Options
- **LangSmith** — Built into LangChain ecosystem. Tracing, dataset management, prompt versioning, human annotation. Best if already using LangChain.
- **Braintrust** — Provider-agnostic eval platform. YAML/code-defined evals, scoring functions, dataset versioning, CI integration. Strong for teams not using LangChain.
- **RAGAS** — RAG-specific eval: faithfulness, answer relevancy, context recall, context precision. Essential for validating RAG pipeline quality.
- **PromptFoo** — Open source, CLI-driven, runs eval suites in CI. Fast iteration on prompt changes. Language-agnostic.
- **Anthropic Evals / OpenAI Evals** — Provider-specific frameworks for model-level evaluation. Useful for fine-tuning validation.
- **Pytest + custom fixtures** — For teams preferring code-based evals over platforms. Pair with Weave (W&B) or Langfuse for logging.

---

## Gateway / routing & LLM observability

A fourth concern, separate from the model provider, the orchestration layer, and retrieval: the **operational layer** that sits between your app and the provider APIs. Add it once you run LLM calls in production — for resilience (failover when a provider rate-limits or errors), cost control (budgets/caps, semantic caching), and visibility (what each call cost, how it performed, why it failed). A single direct SDK call doesn't need this; multi-provider, multi-team, or cost-sensitive production traffic does.

### LLM gateways / routers
Sit in front of one or more providers and present a unified API with failover, load balancing, cost caps, and caching.
- **LiteLLM** — Open-source proxy/SDK normalizing 100+ providers to the OpenAI API shape. Self-hostable; budgets, virtual keys, fallback routing, caching. Use when you want provider-agnostic code and full control without a vendor.
- **OpenRouter** — Hosted marketplace fronting many models behind one API key and one bill. Automatic fallback and price/latency routing. Use for fast access to many models with minimal setup; SaaS dependency.
- **Portkey** — Hosted (or self-host) AI gateway with routing, retries, caching, budgets, and built-in observability/guardrails. Use when you want gateway + tracing in one product.
- **Cloudflare AI Gateway** — Edge gateway adding caching, rate limiting, retries, and analytics in front of provider APIs with minimal code change. Use when already on Cloudflare or wanting a thin, low-latency caching/observability layer.

**When/why:** reach for a gateway when you need failover across providers, hard cost ceilings, response caching, or one audit point for all LLM traffic. Trade-off: an added hop/dependency in the critical path — keep a direct-SDK fallback path and watch the gateway's own latency.

### LLM observability
Trace prompts, completions, token usage, cost, and latency per call/chain — distinct from eval frameworks (which score quality offline).
- **Langfuse** — Open-source (self-host or cloud) tracing, prompt management, cost/latency analytics, and dataset/eval hooks. Strong default when you want to own the data.
- **Helicone** — Proxy-based observability: one-line base-URL swap to capture logs, cost, caching, and rate-limit analytics. Lowest-friction adoption.
- **Phoenix (Arize)** — Open-source OpenTelemetry-native tracing and evaluation for LLM/RAG apps, with strong retrieval-quality debugging. Use when standardizing on OTel or debugging RAG.

**When/why:** add observability the moment LLM calls reach production — you cannot debug agent misbehavior, cost spikes, or quality regressions without per-call traces. Prefer OTel-compatible tooling to fold LLM spans into your existing observability stack (`.claude/skills/observability/SKILL.md`).

---

## Comparison Table

| Tool | Category | Hosting | Cost Model | Data Privacy | Best For |
|---|---|---|---|---|---|
| OpenAI | Frontier LLM | Cloud only | Per token | Low (data to OpenAI) | General LLM apps, broadest ecosystem |
| Anthropic | Frontier LLM | Cloud only | Per token | Low (data to Anthropic) | Long-context, code, reasoning |
| Google/Gemini | Frontier LLM | Cloud/Vertex | Per token | Medium (Vertex VPC) | Multimodal, video, 1M context |
| Llama/Mistral | Open LLM | Self-host/managed | Infra cost | High (on-prem option) | Privacy, cost at volume, fine-tuning |
| LangChain | Orchestration | N/A (library) | Free (LangSmith paid) | Depends on backend | Complex chains, agents, wide integrations |
| LlamaIndex | Orchestration/RAG | N/A (library) | Free (LlamaCloud paid) | Depends on backend | RAG, document Q&A, knowledge bases |
| pgvector | Vector DB | Self/Supabase | Infra cost | High | SQL-first teams, < 1M vectors |
| Pinecone | Vector DB | Managed SaaS | Per vector/query | Medium | Zero-ops RAG, fast startup |
| Qdrant | Vector DB | Self/managed | Infra cost | High (self-hosted) | Self-hosted, hybrid search |
| Weaviate | Vector DB | Self/managed | Infra cost | High (self-hosted) | Multi-modal, multi-tenant |
| LangSmith | Evals | Cloud SaaS | Usage-based | Low | LangChain teams, tracing + evals |
| Braintrust | Evals | Cloud SaaS | Usage-based | Medium | Provider-agnostic evals |
| RAGAS | Evals | Library | Free | High | RAG quality measurement |

---

## Recommended Combinations

- **OpenAI (GPT-4o) + pgvector + LlamaIndex + RAGAS** — Standard RAG stack: OpenAI for inference, pgvector for retrieval (no extra DB), LlamaIndex for pipeline, RAGAS to measure quality. Good starting point for most teams.
- **Anthropic (Claude Sonnet) + Pinecone + LlamaIndex + Braintrust** — Long-context RAG for large documents: Claude handles 200K context when retrieval misses, Pinecone for zero-ops vector search, Braintrust for eval CI.
- **Open LLM (Llama via vLLM) + Qdrant + LangChain + PromptFoo** — Privacy-first: everything on-prem, full data control, LangChain for orchestration, PromptFoo for CI evals.
- **OpenAI + LangGraph + LangSmith** — Agentic workflows: LangGraph for stateful multi-step agents with memory and branching, LangSmith for tracing every node execution.
- **Gemini (Vertex) + pgvector + LlamaIndex** — GCP-native: Vertex AI Gemini for inference, Cloud SQL PostgreSQL + pgvector for retrieval, LlamaIndex for pipeline. Single-cloud, enterprise-friendly.
- **OpenAI + Anthropic (fallback) + PromptFoo** — Multi-provider resilience: route to Claude when OpenAI rate-limits or fails, PromptFoo validates both providers produce equivalent outputs.
- **Mistral/Llama (Groq) + Pinecone + LangChain** — Cost-optimized cloud: Groq for fast/cheap open-model inference, Pinecone for managed retrieval, LangChain for orchestration. 10x cheaper than GPT-4o at volume.

---
name: ai-ml
description: >
  Activate when the project builds AI/ML features or products: LLM integration, RAG pipelines,
  fine-tuning, model serving, embeddings, agents, evals, guardrails, or classical ML.
  Triggers on: keywords like "LLM", "RAG", "embedding", "fine-tune", "prompt", "vector store",
  "agent", "tool calling", "model", "inference", "evaluation", "hallucination", "guardrail",
  "OpenAI", "Anthropic", "Hugging Face", "Ollama", "LangChain", "LlamaIndex", "MLflow".
---

# AI/ML Feature & Product Development

## When to use
- Integrating an LLM (chat, completion, structured output, tool calling) into any application
- Building a RAG (Retrieval-Augmented Generation) pipeline
- Designing or running evals for an AI feature
- Adding guardrails, moderation, or safety filters
- Fine-tuning or instruction-tuning a model
- Serving a model in production (batch inference or real-time)
- Building an AI agent with tool use / function calling
- Classical ML: training, feature engineering, experiment tracking, deployment

## Workflow

1. **Choose the right AI approach before writing code**:
   | Need | Recommended approach |
   |------|---------------------|
   | General Q&A / summarization | Prompt-engineered API call (cheapest, fastest) |
   | Grounding in private docs | RAG over a vector store |
   | Consistent structured output | LLM + JSON schema / function calling |
   | Domain-specific style or facts | Fine-tuning (only if RAG + prompting fall short) |
   | Multi-step reasoning / actions | Agent with tool calling |
   | Tabular prediction | Classical ML (XGBoost, sklearn) — not LLM |

2. **Model selection criteria**:
   - Latency budget: streaming tokens arrive in ~200 ms for frontier models; embeddings are synchronous.
   - Cost: estimate `(input_tokens × price_in + output_tokens × price_out) × daily_requests`.
   - Privacy: does the data contain PII or regulated content? Use on-premises / private deployment (Ollama, vLLM, AWS Bedrock VPC endpoint).
   - Context window: choose a model whose context fits your largest expected document + prompt + output with 20% headroom.
   - Never hardcode a model name in application code — read from config/env so models can be swapped without deploys.

3. **Prompt engineering**:
   - Write prompts in version-controlled files (`.claude/prompts/<name>.md` or `prompts/<name>.txt`), not inline strings.
   - System prompt defines role, constraints, output format, and tone. Keep it ≤500 tokens.
   - Use few-shot examples when zero-shot produces inconsistent structure.
   - Separate instructions from data with clear delimiters (`<document>`, `<user_query>`, XML tags or `---`).
   - Never interpolate raw user input directly — always sanitize or wrap in a delimiter.

4. **RAG pipeline** (when needed):
   a. **Chunking**: split documents into ~400–800 token chunks with 10–15% overlap. Chunk at semantic boundaries (paragraphs, sections), not fixed byte offsets.
   b. **Embedding**: embed chunks with the same model you'll use at query time. Store `(chunk_id, text, embedding, metadata)`.
   c. **Vector store**: Pinecone, Qdrant, Weaviate, pgvector, or ChromaDB. Index `chunk_id` and filterable metadata fields.
   d. **Retrieval**: top-k cosine similarity (k=5–10) + optional metadata filter. Re-rank results with a cross-encoder if precision matters.
   e. **Prompt assembly**: `system_prompt + retrieved_chunks + user_query`. Include source citations in the context.
   f. **Citation**: instruct the model to cite `[source_id]` inline; validate citations point to real retrieved chunks.
   g. **Freshness**: re-embed and re-index documents when source content changes; track `last_indexed_at`.

5. **Structured output**:
   - Use JSON mode or function/tool calling — never parse free-text JSON from model output with `json.loads` directly.
   - Define output schema with Pydantic (Python) or Zod (TypeScript); validate before using in application logic.
   - Set `temperature=0` for deterministic structured outputs; use `temperature=0.7` only for creative generation.

6. **Agents & tool calling**:
   - Define each tool with a clear name, description, and typed parameters (the model reads these descriptions).
   - Tools must be idempotent where possible; flag destructive tools explicitly and require human confirmation.
   - Set a max iteration limit (e.g., 10 steps) to prevent runaway loops.
   - Log every tool call and its result for auditability.
   - Apply the principle of least privilege: agent tools can only access data/actions the user is authorized for.

7. **Evals** — build before shipping any AI feature:
   - Collect a golden dataset: 50–200 representative inputs with expected outputs / quality criteria.
   - Run evals on every prompt change and model upgrade.
   - Eval types: exact match, semantic similarity (cosine ≥ 0.85), LLM-as-judge (GPT-4 / Claude scores 1–5), human spot-check.
   - Track eval results in MLflow, Weights & Biases, or a simple CSV in Git.
   - Define minimum passing threshold before merging a prompt or model change.

8. **Guardrails & safety**:
   - Input filtering: detect and block prompt injection, jailbreaks, PII in prompts going to third-party APIs.
   - Output filtering: scan responses for PII leakage, harmful content, and hallucinated URLs before returning to users.
   - Use dedicated moderation APIs (OpenAI Moderation, AWS Comprehend) for user-generated content.
   - For regulated domains (medical, legal, financial): add a disclaimer and route edge cases to human review.
   - Rate-limit per user to prevent abuse and runaway cost.

9. **Observability**:
   - Log every LLM call: `model`, `prompt_tokens`, `completion_tokens`, `latency_ms`, `cost_usd`, `request_id`.
   - Trace multi-step agent runs end-to-end (LangSmith, Langfuse, Arize Phoenix, or OpenTelemetry).
   - Alert when: error rate > 1%, p95 latency > 5 s, daily cost > budget threshold.
   - Store a sample of inputs + outputs for ongoing quality review (with user consent / data policy compliance).

10. **Production model serving**:
    - Self-hosted: vLLM or TGI behind a load balancer; autoscale on GPU utilization.
    - Managed API: use retries with exponential backoff; handle rate-limit (429) and timeout (504) errors.
    - Caching: cache identical prompts (exact-match or semantic cache with Redis) to cut cost and latency.
    - Model versioning: pin to a specific model version in production; test new versions in staging with eval suite before promoting.

## Standards

**Do:**
- Version-control every prompt; treat prompt changes as code changes (PR, review, eval).
- Always set a `max_tokens` / `max_completion_tokens` limit to prevent runaway output costs.
- Chunk and embed asynchronously; never block a request while indexing new documents.
- Separate retrieval logic from generation logic — testable independently.
- Use streaming responses for user-facing chat to reduce perceived latency.

**Do not:**
- Use an LLM for tasks a deterministic function can handle (arithmetic, date parsing, regex extraction).
- Embed user PII in vector stores without encryption and a documented retention/deletion policy.
- Deploy a new model or prompt to 100% of traffic immediately — use feature flags or canary rollout.
- Trust model output as ground truth without validation — always sanity-check structured outputs.
- Store API keys in source code or `.env` files committed to Git.

## Common mistakes to avoid

- **Prompt injection via user input**: user supplies `"Ignore previous instructions and..."`. Always wrap untrusted input in delimiters; never concatenate raw user text into the system prompt.
- **No eval before ship**: first version "feels good" in manual testing, but degrades on edge cases. Build the golden dataset on day one.
- **Context window overflow**: long documents silently get truncated. Measure token counts before every LLM call; truncate or chunk proactively.
- **Hallucinated citations in RAG**: model cites a source not in the retrieved chunks. Validate every citation against the retrieved set before returning to the user.
- **Model name hardcoded**: `gpt-4` pinned in 30 files; model gets deprecated. Use a single config constant or env var.
- **No cost controls**: agent loops calling GPT-4 for 50 iterations per request. Set `max_iterations`, token budgets, and daily spend alerts.
- **Skipping temperature=0 for structured output**: non-zero temperature on JSON output causes intermittent parse failures in production.

## Output format

A production AI feature module:

```
ai/
  prompts/
    <feature>_system.md
    <feature>_user.md
  rag/
    chunker.py
    embedder.py
    retriever.py
    indexer.py
  agents/
    <agent_name>/
      agent.py
      tools/
        <tool>.py
  evals/
    datasets/
      <feature>_golden.jsonl
    run_evals.py
    results/          # gitignored; tracked in MLflow/W&B
  serving/
    inference.py
    cache.py
  guardrails/
    input_filter.py
    output_filter.py
config/
  ai.yaml             # model names, thresholds, cost limits
```

Reference architecture template: `.claude/templates/architecture.md`

## Related checklists
- `.claude/checklists/security.md` — prompt injection, PII, API key hygiene
- `.claude/checklists/performance.md` — latency, caching, token budgets
- `.claude/checklists/launch.md` — eval pass rate, guardrails, cost controls

## Related agents
- `.claude/agents/stack/ai/` — AI/ML stack selection and configuration
- `.claude/agents/core/orchestrator.md` — overall project flow
- `.claude/agents/quality/` — testing strategy including LLM evals
- `.claude/agents/engineering/` — feature implementation workflow

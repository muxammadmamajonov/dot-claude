# Example Project Brief — "Scholar" (AI Agent System)

> A worked example showing how the Project OS classifies and scopes an AI agent product with tools + RAG. Illustrative, not a real product.

## One-line idea
A research-assistant agent that answers questions over a team's private documents, cites its sources, and can run multi-step research (search → read → synthesize) using tools — with grounded, verifiable answers.

## Classification result
- **Project type:** AI agent system (with RAG)
- **Preset:** [ai-agent-system](../.claude/presets/ai-agent-system.md)
- **Cross-cutting concerns:** retrieval grounding & citation, evaluation harness (answer quality / hallucination), guardrails (prompt-injection from ingested docs, PII leakage), cost & latency budgets per query, privacy (private corpus), observability of agent traces. Secondary type: backend API + web UI.
- **Specialists pulled in:** [ai-agent-domain-expert](../.claude/agents/domain/ai-agent-domain-expert.md), [rag-engineer](../.claude/agents/stack/ai/rag-engineer.md), [evaluation-engineer](../.claude/agents/stack/ai/evaluation-engineer.md), [anthropic-engineer](../.claude/agents/stack/ai/anthropic-engineer.md), [security-auditor](../.claude/agents/quality/security-auditor.md).

## Founder discovery answers
- **Problem:** Teams drown in their own docs (wikis, PDFs, tickets); answers exist but nobody can find them, and generic chatbots make things up.
- **Target users:** Knowledge workers at 20–200-person companies; first wedge = support & solutions engineers.
- **Value proposition:** Ask in plain language, get an answer grounded in *your* docs with citations you can click — and the agent does multi-step research instead of one-shot guessing.
- **Constraints:** 3 engineers; $60k initial budget incl. model spend; design-partner pilot in 8 weeks; data must stay private (no training on customer data).
- **Success metrics:** Answer "helpful + correct" rate ≥ 85% on the eval set; grounded-citation rate ≥ 95%; p95 latency ≤ 6 s; cost ≤ $0.05/query; pilot NPS ≥ 30.
- **Key risks:** Hallucination/wrong citations eroding trust; prompt injection via ingested documents; retrieval quality on messy corpora; runaway token cost; eval blind spots.
- **Budget / timeline:** $60k; pilot in 8 weeks, GA in ~5 months.

## Recommended stack (with rationale)
- **LLM:** Anthropic Claude (latest Opus/Sonnet) for reasoning + tool use; structured tool calls and MCP for connectors. See [.claude/stack-matrix/ai-ml.md](../.claude/stack-matrix/ai-ml.md).
- **Retrieval:** pgvector on Postgres (Supabase) — keeps corpus + embeddings + app data in one secure store; hybrid (BM25 + vector) search. See [.claude/stack-matrix/database.md](../.claude/stack-matrix/database.md).
- **Orchestration:** thin custom agent loop (LangChain/LlamaIndex only where they earn it) — keep the loop debuggable and the prompts owned.
- **Backend:** Python/FastAPI (mature AI ecosystem). **Frontend:** Next.js chat UI with streamed responses + inline citations. See [.claude/stack-matrix/backend.md](../.claude/stack-matrix/backend.md).
- **Evals & tracing:** a versioned eval dataset + LLM-as-judge in CI; trace every agent step (tool calls, retrieved chunks, tokens, cost).

## MVP scope
**In:** ingest PDFs + Markdown + a Notion/Confluence connector, chunk + embed + hybrid retrieve, grounded answer with clickable citations, one research tool (web/internal search) the agent can call, streamed chat UI, per-query cost/latency logging, a 100-item eval set gating deploys, basic prompt-injection guardrail on ingested content.
**Deferred:** fine-tuning, multi-agent collaboration, more connectors, role-scoped document permissions beyond workspace, agent "actions" that write to external systems, on-prem deployment.

## First 3 safe phases
1. **RAG walking skeleton** — ingest a small doc set, hybrid-retrieve, answer one question with correct citations (no agent loop yet). Proves grounding quality. → [/build-prototype](../.claude/commands/build-prototype.md)
2. **Eval harness first** — build the 100-item eval set + LLM-judge + cost/latency tracing *before* expanding features, so quality is measurable. → [evaluation-engineer](../.claude/agents/stack/ai/evaluation-engineer.md)
3. **Agent loop + guardrails** — add the multi-step research tool and the prompt-injection/PII guardrails, then run [/audit-security](../.claude/commands/audit-security.md) and the [ai-ml checklist](../.claude/checklists/ai-ml.md).

---
**Next command to run:** [/start-project](../.claude/commands/start-project.md) → confirms the ai-agent-system preset, then [/interview-founder](../.claude/commands/interview-founder.md) drills into eval targets, cost ceilings, and the privacy model.

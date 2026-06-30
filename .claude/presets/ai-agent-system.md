# AI Agent System Preset

## Project type

A software system where one or more AI language models (or other ML models) act as autonomous or semi-autonomous agents: receiving goals, using tools, maintaining memory, orchestrating sub-agents, and producing actions in a loop. Encompasses coding assistants, research agents, customer-service bots, autonomous task runners, multi-agent pipelines, RAG systems, AI-powered APIs, and agent frameworks. Can be a standalone product, a backend service, a CLI, a browser extension, or embedded in a larger platform.

---

## Typical use cases

- Coding agent or developer assistant (file reading, code generation, test execution, PR creation)
- Research / deep-research agent (web search, document retrieval, source synthesis, fact verification)
- Customer-support agent with tool use (CRM lookup, order status, escalation routing)
- Multi-agent pipeline (orchestrator delegates to specialist sub-agents)
- RAG (Retrieval-Augmented Generation) service embedded in a product
- Autonomous task runner (schedule-triggered, event-triggered, or human-in-the-loop approval flows)
- AI-powered API / microservice wrapping LLM calls with tool chains and guardrails
- Evaluation and red-teaming harness for other AI systems
- Document processing pipeline (ingest → extract → classify → route → output)

---

## Required discovery questions

1. **Goal and autonomy level** — What task does the agent perform? Does it act autonomously (fire-and-forget), semi-autonomously (human-in-the-loop approval on key actions), or as a copilot (always-on assistant)? The autonomy level determines the guardrail and audit requirements.
2. **Tools and integrations** — What external systems does the agent read from or write to? (APIs, databases, filesystems, browsers, code execution sandboxes, email, calendar.) Each write-capable tool is a blast-radius amplifier that needs explicit safeguards.
3. **Memory and state** — What must the agent remember across turns or sessions? Conversation history, extracted facts, user preferences, task progress? Where is memory stored (in-context, vector DB, structured DB, key-value)?
4. **Orchestration model** — Single agent with tools, chain of agents (sequential), parallel fan-out with aggregator, hierarchical orchestrator/sub-agent, or event-driven DAG? The model drives the concurrency and failure-recovery design.
5. **LLM provider and model** — Which providers are in scope (Anthropic, OpenAI, Gemini, local/Ollama)? Any model-switching or cost-tiering strategy (large model for reasoning, small model for routing)?
6. **Latency and throughput requirements** — Is this interactive (response < 3 s) or batch/background (minutes acceptable)? Expected requests per day or concurrent agents at peak?
7. **Guardrails and safety** — What must the agent never do? (Delete prod data, send emails without approval, reveal PII, call paid APIs without a spend cap.) Who approves irreversible actions?
8. **Evaluation and quality bar** — How is agent quality measured? Task-completion rate, accuracy on a golden dataset, human preference scores? Is there a regression test suite to prevent prompt regressions?
9. **Data sensitivity and compliance** — Does the agent process PII, PHI, financial data, or confidential company data? Which jurisdictions? Are LLM API calls allowed to send this data to third-party providers?
10. **Cost and spend controls** — What is the monthly LLM API budget? Are per-request token limits enforced? Is prompt caching used for repeated context? Who is alerted when spend anomalies occur?

---

## Recommended agents

**Core**
- `.claude/agents/core/orchestrator.md` — drives the 9-stage flow; spec the agent architecture before writing any tool code
- `.claude/agents/core/solution-architect.md` — agent topology, memory architecture, tool design, failure recovery
- `.claude/agents/core/requirements-engineer.md` — write precise agent behaviour specs (what the agent must/must-not do per scenario)

**Engineering**
- `.claude/agents/engineering/ai-ml-engineer.md` — LLM integration, prompt engineering, tool definitions, embedding/retrieval design
- `.claude/agents/engineering/backend-engineer.md` — agent runtime, API layer, job queue, persistent memory store
- `.claude/agents/engineering/data-engineer.md` — RAG pipeline (ingest, chunk, embed, index, retrieve)
- `.claude/agents/engineering/api-architect.md` — tool API contracts, MCP server design, webhook integrations

**Quality**
- `.claude/agents/quality/qa-engineer.md` — golden-dataset eval suite, regression tests for prompt changes, adversarial input testing
- `.claude/agents/quality/security-auditor.md` — prompt injection, tool permission scope, secret exposure, data exfiltration paths

**Domain**
- `.claude/agents/domain/ai-agent-domain-expert.md` — agentic loop patterns, memory architectures, eval frameworks, guardrail design

---

## Recommended skills

- `.claude/skills/ai-ml/SKILL.md` — prompt engineering, tool use / function calling, embeddings, retrieval, evals
- `.claude/skills/security/SKILL.md` — prompt injection defence, tool permission model, secret management, audit logging
- `.claude/skills/python-backend/SKILL.md` — agent runtime implementation (most agent SDKs are Python-first)
- `.claude/skills/node-backend/SKILL.md` — alternative for TypeScript agent stacks (Vercel AI SDK, LangChain.js)
- `.claude/skills/data-platform/SKILL.md` — RAG ingestion pipeline design, vector store selection, data contracts
- `.claude/skills/testing/SKILL.md` — eval harness design, golden datasets, CI regression on prompt changes
- `.claude/skills/redis/SKILL.md` — short-term memory, rate limiting, result caching, pub/sub for async agent events
- `.claude/skills/postgres/SKILL.md` — long-term structured memory, task/run audit log, tool-call history

---

## Recommended stack options

| Stack | Rationale |
|---|---|
| **Python + Anthropic SDK (Claude) + LangGraph + PostgreSQL + pgvector** | Typed tool definitions with Claude's native tool-use API; LangGraph for complex multi-agent DAGs; pgvector for RAG without a separate vector service; strong community patterns. |
| **Python + OpenAI Agents SDK + Pinecone/Weaviate + Redis** | If OpenAI models are required; Pinecone for high-scale vector search; Redis for fast short-term memory and rate-limiting; well-documented patterns. |
| **TypeScript + Vercel AI SDK + Claude/OpenAI + Upstash Redis** | For teams in a Next.js / Node ecosystem; streaming UI with AI SDK; lightweight and edge-deployable; suited for copilot / assistant products. |
| **Python + CrewAI / AutoGen + local Ollama + ChromaDB** | Fully air-gapped / self-hosted when data must not leave the network (PHI, confidential enterprise data); lower capability ceiling but no external API dependency. |

---

## Required checklists

- `.claude/checklists/security.md` — prompt injection defence, tool permission minimisation, secret handling, PII data paths, audit logging every tool call
- `.claude/checklists/performance.md` — LLM latency p50/p95/p99 per task type; token throughput; retrieval latency; cost per task
- `.claude/checklists/qa.md` — golden-dataset eval pass rate; regression on prompt changes; adversarial / red-team inputs; tool error handling
- `.claude/checklists/production.md` — spend caps enforced; observability on every LLM call; human-in-the-loop gates for irreversible actions; runbook for model outage

---

## MVP scope pattern

**In the first cut**
- One primary task type end-to-end (e.g. "answer questions about our docs using RAG", or "run a coding task given a spec")
- Minimum tool set required for that task; no speculative tools
- Single-agent loop (orchestrator + tools), not multi-agent — add sub-agents when single-agent hits a ceiling
- Short-term conversation memory (in-context window); long-term memory deferred until a concrete use case demands it
- Synchronous request-response (< 30 s); streaming for interactive paths; async job queue deferred to v2
- Eval harness with 20–50 golden examples covering the primary task and the most common failure modes
- Hard spend cap per request and per day at the LLM provider level

**Defer until post-MVP**
- Multi-agent orchestration (define the interfaces now, implement sub-agents later)
- Long-term semantic memory / vector knowledge base (design the schema, load real data after core is stable)
- Full human-in-the-loop approval workflow UI (console-log approvals first, build UI after flow is validated)
- Multi-provider model routing / fallback (pick one provider for MVP, add fallback when reliability data exists)
- Fine-tuning on task-specific data (gather production examples first, then fine-tune)
- Full audit dashboard (log everything from day one, build the UI dashboard after)

---

## Production risks

| Risk | Priority | Mitigation |
|---|---|---|
| Prompt injection via user-supplied or tool-retrieved content | P0 | Treat all external content as untrusted; separate system prompt from data using structured tool-result formatting; validate tool outputs before feeding to next LLM call |
| Tool with write access used destructively by model error | P0 | Principle of least privilege on every tool: read-only by default; write tools require explicit confirmation gate or human approval for irreversible actions |
| PII or secrets exfiltrated to LLM provider | P0 | Scrub / mask sensitive fields before sending to external APIs; audit what is in the context window; use self-hosted models for regulated data |
| Unbounded LLM spend from runaway agent loop | P0 | Hard token budget per task; max iteration count; cost anomaly alert; kill-switch endpoint to terminate running agents |
| Prompt regression — a prompt change breaks previously passing evals | P1 | Run golden-dataset evals in CI on every prompt change; version prompts like code |
| Non-determinism in agentic loops — different runs produce different tool calls | P1 | Log every LLM call + response + tool call for reproducibility; use `temperature=0` for deterministic routing steps |
| Tool API rate limits causing cascading agent failures | P1 | Implement exponential backoff and retry with jitter on every tool; circuit-breaker pattern for downstream APIs |
| Memory poisoning — attacker injects malicious facts into long-term memory | P1 | Validate and sanitise all inputs before writing to memory; scope memory reads to trusted namespaces |
| Hallucinated tool call arguments causing data corruption | P1 | Validate all tool arguments against a typed schema before execution; reject malformed calls and return structured error to agent |
| No human oversight on autonomous irreversible actions | P1 | Require human-in-the-loop confirmation for: deleting data, sending external communications, making financial transactions, and any action flagged as irreversible |

---

## Launch requirements

- All items in `.claude/checklists/production.md` are green
- Eval golden dataset passes at agreed threshold (e.g. ≥ 90% task completion rate); threshold documented in `docs/specs/evals.md`
- Every LLM call and tool invocation logged with: timestamp, model, input tokens, output tokens, tool name, arguments, result, latency, cost — queryable for at least 30 days
- Hard spend cap enforced at LLM provider and at application layer; tested by injecting a runaway loop in staging
- Prompt injection red-team test executed; all identified injection paths mitigated
- Tool permission audit complete: every tool has documented minimum-permission scope; write tools have confirmation gates
- PII data-flow map complete: every field of user data documented with: where it goes, whether it leaves the network, retention period
- Human-in-the-loop approval flow tested for every irreversible action class
- Runbook for: LLM provider outage (failover or graceful degradation), bad model release (rollback to previous prompt version), spend anomaly (kill-switch and investigation)
- All P0/P1 bugs resolved; P2 triaged
- Monitoring active: LLM latency p95, error rate, cost per task, tool call failure rate — all with alerting thresholds

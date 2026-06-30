# AI/ML Checklist
Gate for AI/ML projects covering eval coverage, guardrails, cost/latency, hallucination/safety, and fallback behaviour. Severity tiers: P0=blocker, P1=important (fix shortly after launch), P2=hardening, P3=post-launch/backlog.

## P0 — Blockers (must pass before any user-facing AI feature ships)

- [ ] **Eval suite covers primary task**: A quantitative evaluation set (≥ 100 representative examples, ideally 500+) exists for every AI-powered feature; the eval runs in CI and produces a pass/fail signal against a defined minimum score threshold.
- [ ] **Guardrails block prohibited outputs**: Content moderation or output classifiers are in place; adversarial prompts from the red-team test set are rejected at the required rate (e.g., ≥ 99 % block rate on clearly harmful content).
- [ ] **PII / sensitive data is not leaked in outputs**: Automated checks confirm the model does not reproduce verbatim PII from the training set or context window into responses seen by other users; verified with a memorisation probe.
- [ ] **Prompt injection mitigated**: User-supplied text that attempts to override system instructions is detected and blocked or sandboxed; tested with a curated prompt-injection suite.
- [ ] **Fallback path exists for model unavailability**: If the model API returns a 5xx or times out, the system falls back gracefully (cached response, degraded mode, or user-facing error) rather than crashing or hanging indefinitely.
- [ ] **API key / model credentials are not exposed to clients**: Model provider API keys are server-side only; no key appears in client bundles, browser network requests, or mobile binaries.
- [ ] **Cost guardrails active**: Per-request and per-user token budgets are enforced; runaway loops or adversarial long contexts cannot cause unbounded spend; alerts fire when daily cost exceeds a configured threshold.

## P1 — Important (fix before scaling or shortly after launch)

- [ ] **Latency p50/p95/p99 measured and within SLO**: Model inference latency is measured end-to-end (including pre/post-processing); p95 is within the product SLO (e.g., < 3 s for interactive features); streaming is used where supported to reduce perceived latency.
- [ ] **Hallucination rate measured for factual tasks**: For features that return factual claims, a hallucination benchmark (e.g., TruthfulQA subset, domain-specific fact-check set) has been run; the rate is below a documented acceptable threshold.
- [ ] **Model version is pinned**: The exact model version (e.g., `claude-sonnet-4-5`, `gpt-4o-2024-08-06`) is pinned in configuration; auto-upgrade to a new model version requires a deliberate change and re-evaluation.
- [ ] **Regression detection in CI**: Eval scores are tracked over time (e.g., in a results file or eval platform); a PR that degrades a key metric by more than the defined threshold fails CI automatically.
- [ ] **Human review queue for low-confidence outputs**: Outputs below a confidence threshold or flagged by the guardrail layer are routed to a human review queue; the queue drains within a documented SLA.
- [ ] **System prompt versioned and auditable**: The system prompt is stored in version control with change history; each deployed version is tagged so that an output can be traced back to the exact prompt that produced it.
- [ ] **User opt-out of AI features available**: Users can disable AI-generated content or data-use for model training (where applicable) per privacy regulations (GDPR, CCPA); opt-out is honoured before the next request.
- [ ] **Input/output logging with retention policy**: All prompts and completions are logged with user/session ID for debugging and safety auditing; retention period is documented and compliant with the privacy policy; access is restricted to authorised personnel.
- [ ] **Token usage tracked per tenant/user**: Token consumption is attributed per user or tenant for cost allocation, abuse detection, and fair-use enforcement; reports are accessible to ops.

## P2 — Hardening / nice-to-have

- [ ] **Caching for repeated/similar queries**: Semantic caching (exact-match or embedding-based) reduces duplicate model calls for frequently repeated prompts; cache hit rate and cost savings are measured.
- [ ] **Multi-model fallback chain**: If the primary model is unavailable or returns an error, a secondary model (same or different provider) is tried automatically; fallback is logged and alerted on.
- [ ] **Bias and fairness evaluation**: Outputs are tested across demographic subgroups relevant to the use case (gender, nationality, dialect); disparate error rates above a threshold block the release.
- [ ] **Adversarial robustness tested**: The system is tested against character-level perturbations, paraphrasing attacks, and jailbreak templates circulating in public red-team repositories; findings are tracked.
- [ ] **Model card / data card documented**: A model card describing training data provenance, known limitations, evaluation results, and intended use cases is maintained in `.claude/templates/` and linked from the README.
- [ ] **Cost forecast for scale**: Token usage at 10× and 100× current traffic is modelled; the cost forecast is reviewed before a marketing push or public launch.
- [ ] **Retrieval quality measured (RAG systems)**: For retrieval-augmented features, retrieval precision@k and recall@k are tracked; chunk size, embedding model, and re-ranker choices are documented with benchmark results.
- [ ] **A/B test framework in place**: Model changes, prompt changes, and parameter changes can be rolled out to a subset of traffic and compared statistically against the control before full rollout.

## P3 — Post-launch / backlog (track and revisit after launch; never blocks shipping)

- [ ] **Continuous eval drift detection**: Eval scores are re-run automatically against a rolling sample of real production inputs weekly; a statistically significant drop (e.g., >2 % on primary metric) triggers an alert and a root-cause investigation before the next model or prompt change ships.
- [ ] **Fine-tuning or RLHF pipeline established**: A curated set of production examples (with human preference labels or correction pairs) is collected under a data governance policy and used to fine-tune or align future model versions; the pipeline is end-to-end tested before first use.
- [ ] **Explainability / citation layer for high-stakes outputs**: For outputs used in consequential decisions (medical, legal, financial), an attribution mechanism (retrieved source citations, chain-of-thought logging, or SHAP/LIME for ML classifiers) is implemented and surfaced to end users.
- [ ] **Model card published externally**: The model card (training data provenance, known failure modes, evaluation results, intended and prohibited uses) is published in a user-accessible location (docs site, HuggingFace Hub, or in-product help) and kept current with each model version change.
- [ ] **Shadow mode evaluation for model upgrades**: New model versions serve a shadow copy of live traffic in parallel with the incumbent; output diffs are sampled and reviewed by a human panel before the new version receives any live traffic share.
- [ ] **Regulatory compliance review scheduled**: Applicable AI regulations (EU AI Act risk classification, US EO on AI, sector-specific rules) are reviewed annually or when regulations change; a compliance gap assessment is documented and gaps are tracked to closure.

## How to use

**When**: Run this checklist before shipping any new AI-powered feature to users and again when upgrading a model version, changing the system prompt, or scaling traffic significantly.

**Who**: ML engineer owns P0 eval and guardrail items. Product/safety lead signs off P1 hallucination and opt-out items. Platform/ops team reviews P2 cost and caching items.

**Command / agent**: Ask the agent `"Run .claude/checklists/ai-ml.md for feature <name>"` — it will execute the eval suite, check prompt-injection probes, verify the model version pin, scan for exposed API keys, and report cost-budget configuration. Items requiring human red-teaming or legal/privacy review are listed separately. Cross-reference `.claude/checklists/security.md` for key management and `.claude/checklists/backend.md` for timeout and fallback infrastructure.

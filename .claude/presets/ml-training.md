# ML Training / MLOps Preset

## Project type

A system whose primary purpose is to **train, register, serve, monitor, and retrain machine-learning models** as a repeatable production lifecycle — not a one-off notebook experiment. This is the MLOps preset. It covers supervised and unsupervised model training, fine-tuning of foundation/base models, recommendation and ranking systems, computer-vision and NLP models, tabular/gradient-boosted models, and the surrounding infrastructure: experiment tracking, a model registry, training pipelines, an inference/serving tier with an SLA, drift detection, and automated or human-triggered retraining.

This is **distinct from `data-platform`** (`.claude/presets/data-platform.md`). Data-platform is about moving and modelling data (ELT/ELT, warehouse, lakehouse, BI). ML-training *consumes* that data to produce model artifacts and serve predictions. A serious ML project usually sits **on top of** a data platform: the platform provides clean, lineage-tracked datasets; this preset turns them into models. It is also distinct from `ai-agent-system` (autonomous LLM agents) and `chatbot` (conversational assistants), which call models rather than train them.

---

## Typical use cases

- Training and shipping a tabular model (fraud scoring, churn, credit risk, demand forecasting)
- Recommendation / ranking systems with frequent retraining on fresh interaction data
- Computer-vision models (classification, detection, segmentation) with GPU training
- NLP models and fine-tuning / LoRA adaptation of open-weight foundation models
- A managed feature store feeding both training and low-latency online serving
- Continuous-training pipelines that retrain on a schedule or on a drift trigger
- A model registry + serving tier that other product teams consume via API

---

## Required discovery questions

1. **Prediction target and business metric** — What exactly does the model predict, and which business metric does a better model move? An offline metric (AUC, F1, RMSE) is meaningless unless it ties to a business outcome.
2. **Training data source and lineage** — Where does training data come from, who owns it, and can you reproduce the exact dataset a model was trained on months later? (Dataset lineage is non-negotiable for audit and rollback.)
3. **Online vs. batch inference** — Does serving need low-latency online predictions (p99 latency budget?) or is batch scoring on a schedule sufficient? This drives the entire serving architecture.
4. **Serving SLA and scale** — Target latency, throughput (predictions/sec), and availability for the inference tier? What is the cost ceiling per million predictions?
5. **Retraining trigger** — Is retraining time-based (nightly/weekly), volume-based, or drift-triggered? Who approves promoting a freshly trained model to production?
6. **GPU / compute budget** — Is GPU training required? What is the monthly compute budget for training *and* serving? GPUs dominate cost; spot/preemptible strategy must be decided early.
7. **Acceptable failure mode** — What is the cost of a wrong prediction, and what is the safe fallback if the model is unavailable or degraded (last-good model, heuristic, human review)?
8. **Fairness / regulation** — Is the model subject to fairness, explainability, or regulatory constraints (credit, hiring, health)? This drives the eval gate and audit trail.
9. **Existing ML stack** — Is there a mandated platform (SageMaker, Vertex AI, Databricks, Kubeflow, plain Kubernetes)? Build-vs-buy here is a §6 business-critical decision (vendor lock-in, cost).
10. **PII in features** — Do features contain personal data? This drives masking, access control on the feature store, and `.claude/checklists/privacy-compliance.md`.

---

## Recommended agents

**Core**
- `.claude/agents/core/orchestrator.md` — drives the 9-stage flow; ML projects need a spec (data contract, eval plan, serving SLA) before any training code
- `.claude/agents/core/solution-architect.md` — train/register/serve/monitor topology, feature store design, online/offline split

**Engineering**
- `.claude/agents/engineering/ai-ml-engineer.md` — model selection, training pipeline, experiment tracking, evaluation harness, serving, drift monitoring (primary builder)
- `.claude/agents/engineering/data-engineer.md` — training-data pipelines, feature engineering, dataset versioning, feature-store population, lineage capture
- `.claude/agents/engineering/cloud-architect.md` — GPU/compute provisioning, autoscaling serving infra, cost-optimised spot/preemptible strategy
- `.claude/agents/engineering/devops-engineer.md` — CI/CD for models, pipeline orchestration, reproducible training environments (containerised)

**Quality**
- `.claude/agents/quality/qa-engineer.md` — eval datasets, offline/online metric validation, regression gates on model quality before promotion
- `.claude/agents/quality/reliability-engineer.md` — serving SLOs, error budgets, rollback-to-previous-model, on-call for inference degradation
- `.claude/agents/quality/performance-engineer.md` — inference latency/throughput tuning, batching, quantisation, cost per prediction
- `.claude/agents/quality/privacy-compliance-auditor.md` — when features contain PII or the model is regulated

---

## Recommended skills

- `.claude/skills/ai-ml/SKILL.md` — model selection, training loops, evaluation frameworks, guardrails, inference cost/latency management
- `.claude/skills/data-platform/SKILL.md` — upstream dataset pipelines, feature pipelines, lineage, data-quality gates feeding training
- `.claude/skills/performance/SKILL.md` — serving latency, batching, quantisation, profiling the inference path
- `.claude/skills/observability/SKILL.md` — metrics/traces/logs for the training pipeline and the serving tier, drift dashboards
- `.claude/skills/docker-kubernetes/SKILL.md` — reproducible training containers, model serving on Kubernetes, GPU scheduling
- `.claude/skills/security/SKILL.md` — feature-store access control, secret handling in pipelines, model artifact integrity

---

## Recommended stack-matrix entries

- `.claude/stack-matrix/ai-ml.md` — model frameworks, training infra, experiment tracking, registry, and serving options with tradeoffs
- `.claude/stack-matrix/data-platform.md` — the upstream data/feature stack that feeds training
- `.claude/stack-matrix/monitoring.md` — for drift, model-quality, and serving-health monitoring tooling
- `.claude/stack-matrix/cloud-devops.md` — for compute, GPU, and pipeline-orchestration platform choices

| Stack | Rationale |
|---|---|
| **MLflow + scikit-learn/XGBoost + FastAPI serving + Evidently (drift)** | Lightweight, framework-agnostic starting point; MLflow tracks experiments and is the model registry; great for tabular models on modest budgets. |
| **SageMaker / Vertex AI managed pipelines + endpoints** | Managed train→register→serve→monitor lifecycle; least ops overhead; best when already on AWS/GCP and a §6 build-vs-buy decision favours managed. |
| **Kubeflow / Metaflow on Kubernetes + Seldon/KServe serving** | Portable, cloud-neutral, GPU-native; best for teams that need control and want to avoid managed-platform lock-in. |
| **Feast (feature store) + Ray Train + BentoML serving** | Strong online/offline feature parity and scalable distributed training; good for recommendation/ranking with online inference. |

---

## Required checklists

- `.claude/checklists/ai-ml.md` — eval gates, training reproducibility, drift monitoring, model-card / documentation, fairness checks
- `.claude/checklists/cost.md` — GPU and serving cost governance, spot-instance strategy, per-prediction cost tracking, training-run budget caps
- `.claude/checklists/production.md` — rollback to previous model, serving SLA monitoring, retraining runbook, on-call readiness
- `.claude/checklists/security.md` — feature-store access control, no secrets in pipeline code, model artifact provenance
- `.claude/checklists/privacy-compliance.md` — when features contain PII or the model is regulated

---

## MVP scope pattern

**In the first cut**
- One model trained end-to-end from a versioned dataset to a registered artifact (prove the pipeline reproduces)
- Experiment tracking on from day one: every run logs params, metrics, dataset version, and code commit
- An offline eval gate: a held-out test set with a documented metric threshold the model must clear to be promotable
- A model registry entry with stage (`staging`/`production`) and the exact dataset+code that produced it
- One serving path (batch *or* online — not both) behind a versioned endpoint, with the model version surfaced in responses
- Rollback proven: promoting a model and rolling back to the previous version is a tested, one-step operation

**Defer until post-MVP**
- Automated drift-triggered retraining (start with scheduled or manual retrain; add drift triggers once a drift baseline exists)
- Full feature store (engineer features in the pipeline first; introduce a store when online/offline parity becomes a real problem)
- Multi-model A/B or shadow deployment (ship one model behind a flag first)
- Distributed/multi-GPU training (single-GPU or CPU baseline first unless data volume forces it)
- Online inference if batch scoring meets the use case (online serving adds large operational cost)
- Self-serve retraining portal for other teams

---

## Key risks

| Risk | Priority | Mitigation |
|---|---|---|
| **Training/serving skew** — features computed differently at train vs. inference time | P0 | Single feature definition shared by both paths (feature store or shared library); test parity on a golden record set |
| **No dataset lineage** — cannot reproduce the dataset a production model was trained on | P0 | Version every training dataset; the registry entry records dataset hash + code commit; never train on an unsnapshotted live table |
| **No rollback path** — a bad model is promoted and there is no fast way back | P0 | Previous model always retained in the registry; rollback to last-good is one tested step; never delete the prior production artifact |
| **Silent quality regression** — a retrain ships worse than the incumbent | P0 | Hard eval gate in CI: a candidate must beat (or match within tolerance) the production model on the held-out set before promotion |
| **PII leaking through features or artifacts** | P0 | Mask/exclude PII before the feature store; access-control the store; audit feature provenance (`.claude/checklists/privacy-compliance.md`) |
| **Undetected data/concept drift** — accuracy decays in production unnoticed | P1 | Drift monitoring on inputs and predictions; alert when drift exceeds threshold; documented retraining trigger |
| **GPU/serving cost runaway** | P1 | Budget caps on training runs; spot/preemptible for training; autoscale-to-zero or right-sized serving; per-prediction cost tracked |
| **Non-reproducible training** — same code + data yields different models | P1 | Pin seeds, dependency versions, and container image; record the full environment with every run |
| **Stale model with no freshness SLA** | P1 | Define a max model age; alert when exceeded; schedule or trigger retraining before staleness bites |

---

## Launch requirements

- All items in `.claude/checklists/ai-ml.md` and `.claude/checklists/production.md` are green
- The production model is reproducible: dataset version + code commit + environment are recorded in the registry
- Eval gate enforced: no model reaches production without clearing the documented quality threshold on a held-out set
- Rollback tested: promoted a model, then rolled back to the previous version with no serving downtime
- Drift monitoring live: input and prediction drift dashboards exist; alerts fire on threshold breach
- Serving SLA verified under load: p99 latency and throughput meet the budget; behaviour under model-unavailable is graceful (last-good or fallback)
- Cost governance active: training-run and serving spend are tracked; budget alerts configured (`.claude/checklists/cost.md`)
- Retraining runbook complete: how to retrain, evaluate, promote, and roll back, including who approves promotion
- PII audit complete where applicable: every feature documented with its source, masking, and access scope
- A model card / decision record (`.claude/templates/decision-record.md`) documents intended use, limitations, metrics, and known failure modes

---
name: performance
description: Use when setting performance budgets, diagnosing slowness or high cost, or optimizing latency/throughput/resource use. Triggers when defining non-functional requirements in a spec, when a hot path or expensive operation is built, when users/metrics report slowness, and during the performance audit before launch. Measure before optimizing — this skill is about profiling, not guessing.
---

# Performance: Budgets, Profiling, Optimization

## When to use
- Setting performance/cost targets for a feature or the system (part of the spec's non-functional requirements).
- A page, query, endpoint, job, render loop, or model call is slow or expensive.
- Capacity, latency, throughput, memory, or cloud cost is trending the wrong way.
- Running the performance audit phase before production readiness.

Applies to all project types: web vitals, mobile frame time and battery, API latency/throughput, batch job runtime, game frame budget, query cost, and LLM/agent token cost + latency.

## Workflow
1. **Set budgets first.** Define measurable targets tied to user impact: e.g. p95 latency, throughput at target load, payload/bundle size, memory ceiling, frame budget (16.6ms @60fps), cost per request/1k operations. Record them in the spec's non-functional section.
2. **Establish a baseline.** Measure current behavior with representative data and load before changing anything. Without a baseline you cannot prove improvement or regression.
3. **Profile to find the real bottleneck.** Use a profiler/tracer/flame graph, query `EXPLAIN`, network waterfall, or APM trace. Identify where time/CPU/memory/allocations/cost actually go. Do not optimize from intuition.
4. **Fix the dominant cost first.** Target the biggest contributor per Amdahl's law. Common wins: eliminate N+1 queries, add the right index, cache or memoize, batch/parallelize I/O, reduce payload/serialization, stream instead of buffer, defer/lazy-load, raise concurrency, pick a better algorithm/data structure.
5. **Re-measure against the baseline and budget.** Confirm the change moved the metric and did not regress others (correctness, memory, cost). Keep changes small and individually measured.
6. **Add a guardrail.** Add a perf test, benchmark, or budget check so the gain doesn't silently regress. Wire budget assertions (e.g. bundle size, query count, p95) into CI where feasible — see `.claude/skills/devops/SKILL.md`.
7. **Validate under load.** For throughput-sensitive systems, run a load/soak test at and beyond target load; watch latency percentiles, error rate, saturation, and cost. Find the knee of the curve.
8. **Audit before launch.** Confirm budgets are met at expected scale, scaling/back-pressure works, and cost is acceptable. Document the profile, the fix, and remaining headroom.

## Standards
- **Do** measure before and after every change; optimize against data, never against a hunch.
- **Do** use percentiles (p95/p99), not averages — tail latency is what users feel.
- **Do** test with production-scale data and realistic load; small datasets hide N+1s and missing indexes.
- **Do** fix algorithmic complexity (O(n²) → O(n log n)) and bad queries before micro-tuning.
- **Do** cache deliberately with explicit invalidation and TTLs; cache correctness bugs are worse than slowness.
- **Do** treat cost as a budget too (cloud spend, egress, tokens) — fast but bankrupting is a failure.
- **Do** offload slow/expensive work to async jobs/queues and add back-pressure and timeouts.
- **Do-not** optimize prematurely or sacrifice correctness, readability, or security for speed that no budget required.
- **Do-not** add caching/concurrency without thinking through invalidation, races, and memory growth.
- **Do-not** rely on one run; account for warmup, GC, JIT, and noise — repeat measurements.
- **Do-not** ship perf changes without a regression guard.

## Common mistakes to avoid
- Optimizing the wrong thing: tuning a function that's 2% of runtime while ignoring the 70% spent in a query.
- Testing performance on tiny datasets, so N+1 queries and missing indexes never surface until production.
- Reporting averages that hide a brutal p99; or a single benchmark run treated as truth.
- Caching without invalidation, producing stale-data bugs that are hard to trace.
- Adding threads/async and creating races, deadlocks, or unbounded resource growth.
- Premature micro-optimization that complicates code for gains no budget asked for.
- Ignoring cost: a "fast" design that 10× the cloud or token bill at scale.

## Output format
A performance record: the budgets, the baseline numbers, the profiling evidence (flame graph / EXPLAIN / trace summary), the change made, and the after numbers vs budget, plus the guardrail added. For audits, a table of budget vs measured at target load with pass/fail and remaining headroom. Link from the spec's non-functional section (`.claude/templates/product-spec.md`).

## Related checklists
- `.claude/checklists/performance.md`
- `.claude/checklists/production.md`
- `.claude/checklists/qa.md`

## Related agents
- `.claude/agents/quality/performance-engineer.md`
- `.claude/agents/engineering/backend-engineer.md`
- `.claude/agents/core/orchestrator.md`

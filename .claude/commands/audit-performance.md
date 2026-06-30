---
description: Profile and audit performance; find bottlenecks; propose and verify improvements against budgets.
argument-hint: [scope: full | api | db | frontend | infra — optional]
---

# /audit-performance

## Purpose
Identify performance bottlenecks through profiling, static analysis, and load testing. Measure against defined budgets (or establish them if none exist). Propose improvements ranked by impact/effort. Apply safe, low-risk improvements; flag architectural changes for human scheduling.

## When to use
- Response times or resource consumption have regressed.
- Pre-launch performance gate (run before `/prepare-launch`).
- After adding a new high-traffic feature or data-intensive query.
- Periodic health check when traffic grows significantly.
- Before scaling infrastructure — confirm code is the bottleneck first.

## Workflow

### Step 0 — Establish budgets and scope
1. Read `docs/specs/` for any stated SLOs (latency p95, throughput RPS, memory limits, bundle size budgets, battery/CPU targets for mobile/embedded).
2. If no budgets exist, **STOP — ask the user to confirm target budgets** before measuring. Suggest sensible defaults based on project type:
   - Web API: p95 < 200 ms, p99 < 500 ms.
   - Web page (LCP): < 2.5 s on 4G mobile.
   - CLI tool: command startup < 300 ms.
   - Background job: throughput target in records/sec.
   - Mobile/embedded: CPU < 30% sustained, memory within OS limits.
3. Confirm scope from argument or default to `full`.

### Step 1 — Gather baseline metrics
Run available profiling and measurement tools for the detected stack. Capture raw numbers before any change.

**Backend / API:**
- `curl -w "%{time_total}" ...` or `wrk`/`hey`/`k6` for HTTP latency and RPS.
- APM traces if instrumented (Datadog, Jaeger, OpenTelemetry).
- Database slow-query logs; `EXPLAIN ANALYZE` on suspicious queries.
- Memory and CPU profiling: `py-spy`, `async-profiler`, `pprof`, `perf`, language-native profilers.

**Frontend (web):**
- Lighthouse CI (`lighthouse --output json`) for Core Web Vitals.
- `webpack-bundle-analyzer` / `rollup-visualizer` / `vite-bundle-visualizer` for bundle size.
- Network waterfall via `webpagetest` or browser DevTools HAR export.

**Mobile / embedded:**
- Platform profilers (Xcode Instruments, Android Profiler, Valgrind).
- Binary size analysis.

**Database:**
- Schema index audit: missing indexes on columns used in WHERE, JOIN, ORDER BY.
- N+1 query detection via ORM log analysis.
- Connection pool saturation check.

**Infra:**
- CPU/memory headroom on current instances.
- Cache hit rate (Redis, CDN).
- Egress volume that could move to CDN or edge.

Record every baseline number in a table. Do not skip this — improvements must show delta against baseline.

### Step 2 — Identify bottlenecks
Categorise findings by type:

| Category | Common patterns |
|---|---|
| Database | N+1 queries, missing index, full-table scan, unbounded result sets |
| Compute | O(n²) algorithms, synchronous work on hot path, missing memoisation |
| I/O | Serial awaits that could be parallel, missing connection pooling |
| Network | Chatty APIs (many small calls), large uncompressed payloads, no HTTP/2 |
| Caching | Cache-miss storms, no CDN for static assets, session affinity breaking distributed cache |
| Frontend | Render-blocking resources, unoptimised images, large JS bundles, layout thrash |
| Memory | Unbounded in-memory caches, large allocations on hot path, GC pressure |
| Startup | Eager loading of rarely-used modules, heavy initialisation on every cold start |

Rank each finding by: **estimated impact × implementation risk ÷ effort**.

### Step 3 — Propose improvements
For each bottleneck produce:
- **What:** exact code or config location.
- **Why it is slow:** data (query time, allocations, bundle bytes).
- **Proposed fix:** concrete change (add index, parallelise awaits, add cache TTL, lazy-load module).
- **Expected gain:** estimated % improvement or absolute delta.
- **Risk:** none / low / medium / high (requires arch change).

**STOP — present the ranked list to the user. Confirm which items to apply in this session.**

### Step 4 — Apply approved low-risk improvements
For each approved item:
1. Make the change.
2. Re-run the relevant benchmark from Step 1.
3. Record the before/after delta.
4. If the improvement is negligible or a regression occurs, revert and note it.
5. Commit: `perf(<scope>): <one-line description> — <delta>`.

Do not apply items rated "high risk" or "requires arch change" — document them for human scheduling.

### Step 5 — Verify budgets met
After all approved improvements:
1. Re-run full benchmark suite from Step 1.
2. Check each metric against the budgets established in Step 0.
3. Flag any budget still breached as a remaining action item.

### Step 6 — Report
Produce the Final report (see below).

## Agents used
- `.claude/agents/core/orchestrator.md` — coordinates parallel profiling across multiple services.
- `.claude/agents/quality/performance-engineer.md` — runs sustained load tests and captures p95/p99 distributions.

## Skills used
- `.claude/skills/performance/SKILL.md` — stack-specific optimisation patterns (index design, caching strategies, bundle splitting).
- `.claude/checklists/performance.md` — itemised performance checklist per project type.

## Expected outputs
| Output | Path |
|---|---|
| Performance audit report | `docs/reports/perf-audit-<date>.md` |
| Applied optimisations | in-place edits, committed |
| Benchmark baseline + results | `docs/reports/perf-benchmarks-<date>.json` |

## Stop conditions
- No performance budgets exist and user cannot provide them → establish defaults, document them, proceed with defaults.
- Profiling requires production traffic (no staging env) → document limitation; analyse code statically only; flag for user.
- An improvement requires database migration → do not apply; log as "scheduled migration needed".
- A change causes test failures → revert immediately.
- Bottleneck is infrastructure-level only (undersized instances) → recommend scaling plan, do not code.

## Final report format
```
## Performance Audit Report — <date>

**Project:** <name>  |  **Scope:** <scope>
**Stack:** <detected tech>

### Budget status
| Metric | Budget | Baseline | After fixes | Status |
|---|---|---|---|---|
| API p95 latency | 200 ms | 480 ms | 190 ms | ✅ |
| LCP (mobile 4G) | 2.5 s | 4.1 s | 2.3 s | ✅ |
| JS bundle (gzip) | 200 KB | 380 KB | 210 KB | ⚠️ close |

### Bottlenecks found — ranked by impact
| # | Category | Location | Impact | Risk | Applied |
|---|---|---|---|---|---|
| 1 | Database N+1 | `UserRepo.findAll()` | −310 ms p95 | Low | ✅ commit abc1234 |
| 2 | Bundle size | `moment.js` → `date-fns` | −120 KB | Low | ✅ commit def5678 |
| 3 | Arch: read replica | DB layer | −200 ms p99 | High | ❌ scheduled |

### Applied improvements detail
#### [1] Database N+1 — `UserRepo.findAll()`
- **Before:** 1 + N queries, 480 ms p95
- **Fix:** eager-load with JOIN / `include`
- **After:** 2 queries, 170 ms p95  (−64%)
- **Commit:** abc1234

### Deferred items (scheduled)
- [3] Add read replica — requires infra provisioning; estimated −200 ms p99.

### Remaining budget breaches
- JS bundle (gzip): 210 KB vs 200 KB budget — 5% over; consider splitting admin chunk.

### Recommended next steps
1. Address remaining bundle overage with route-level code splitting.
2. Re-run `/audit-performance` after read replica is provisioned.
```

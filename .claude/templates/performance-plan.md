# Performance Plan

**What:** Defines performance budgets, key user journeys to measure, expected load profile, target metrics, and the optimization backlog.
**Who fills it in:** Engineering lead + DevOps, reviewed by product manager.
**When:** During architecture design, before infrastructure is provisioned. Revisit before each major launch and quarterly in production.

> Applies to any project type: web frontend, mobile app, backend API, data pipeline, game, CLI, or embedded system. Skip sections that don't apply; note the reason.

---

## 1. Performance Goals & Priorities

> State the non-negotiable performance outcomes for users and the business. Use these to resolve trade-offs.

1. `<e.g. The time from page load to interactive must not exceed 2.5 s on a median mobile device on 4G.>`
2. `<e.g. API endpoints used in the core checkout flow must respond in < 200 ms at p95 under expected peak load.>`
3. `<e.g. A data pipeline run processing 1 M rows must complete within 10 minutes.>`
4. `<e.g. The game must maintain 60 fps on the minimum-spec device during the most intensive combat scenario.>`

---

## 2. User Journeys to Measure

> List the journeys that matter most to the user experience and the business. These are the scenarios you will run in load/perf tests and monitor in production.

| Journey ID | Name | Entry point | Key steps | Success metric |
|------------|------|-------------|-----------|----------------|
| J-01 | `<Initial page load>` | `<Landing page URL>` | `<DNS → TLS → FCP → TTI>` | `<LCP < 2.5 s; TTI < 3.5 s>` |
| J-02 | `<User login>` | `<Sign-in screen>` | `<Submit credentials → session created → redirect>` | `<API p95 < 200 ms>` |
| J-03 | `<Core action — e.g. Search results>` | `<Search bar>` | `<Type query → results render>` | `<First result visible < 300 ms>` |
| J-04 | `<Core action — e.g. Checkout>` | `<Cart page>` | `<Enter payment → confirm → receipt>` | `<Full flow < 5 s; payment API p95 < 500 ms>` |
| J-05 | `<Data export / heavy report>` | `<Reports page>` | `<Request → generate → download link>` | `<Start download < 10 s for 10k rows>` |
| J-06 | `<Real-time feature — e.g. Live feed>` | `<Dashboard>` | `<WS connect → first event>` | `<Event latency < 500 ms p99>` |

---

## 3. Performance Budgets

### 3.1 Frontend / Client

| Metric | Budget | Measurement |
|--------|--------|-------------|
| Largest Contentful Paint (LCP) | `< 2.5 s` | Lighthouse CI / CrUX |
| First Input Delay (FID) / INP | `< 200 ms` | CrUX / RUM |
| Cumulative Layout Shift (CLS) | `< 0.1` | CrUX / RUM |
| Time to Interactive (TTI) | `< 3.5 s` | Lighthouse CI |
| Total Blocking Time (TBT) | `< 300 ms` | Lighthouse CI |
| JavaScript (initial, gzipped) | `< 250 kB` | Bundlewatch / size-limit |
| CSS (initial, gzipped) | `< 30 kB` | Bundlewatch |
| Images per page (unoptimised) | 0 — all served via CDN with format negotiation | CI check |
| Third-party JS weight | `< 100 kB gzipped` | Lighthouse third-party audit |
| Lighthouse Performance score | `≥ 90` | Lighthouse CI |

### 3.2 Backend API

| Metric | Budget | Measurement |
|--------|--------|-------------|
| Read endpoint p50 | `< 50 ms` | APM (Datadog / Grafana) |
| Read endpoint p95 | `< 200 ms` | APM |
| Read endpoint p99 | `< 500 ms` | APM |
| Write endpoint p95 | `< 300 ms` | APM |
| Error rate (5xx) | `< 0.1%` | APM + alerting |
| Throughput at expected peak | `<X RPS>` — sustain for 30 min | Load test |
| DB query p95 | `< 50 ms` | DB slow-query log / APM |
| External API call timeout | `< 5 s` (with fallback) | APM |

### 3.3 Mobile

| Metric | Budget | Measurement |
|--------|--------|-------------|
| Cold start (time to interactive) | `< 2 s` | Instruments / Android Profiler |
| Warm start | `< 0.5 s` | Instrumented tests |
| Scroll frame rate | 60 fps sustained | Frame profiler |
| Memory (typical session) | `< 150 MB RSS` | Profiler |
| Battery drain (background/hour) | `< 2%` | Profiler |
| App binary size (initial install) | `< 50 MB` | Build artifact |

### 3.4 Data Pipeline / Batch Jobs

| Job | Input volume | Target duration | Resource cap |
|-----|-------------|-----------------|-------------|
| `<ETL pipeline>` | `<1 M rows>` | `< 10 min` | `<4 vCPU, 8 GB RAM>` |
| `<ML training run>` | `<dataset size>` | `< X hours` | `<GPU instance type>` |
| `<Report generation>` | `<10k rows>` | `< 30 s` | `<2 vCPU, 4 GB RAM>` |

### 3.5 Game / Real-Time

| Metric | Minimum-spec device | Target device | Measurement |
|--------|---------------------|---------------|-------------|
| Frame rate | 30 fps | 60 fps / 120 fps | FPS counter + profiler |
| Frame time (ms) | `< 33 ms` | `< 16 ms` | GPU profiler |
| Load time (scene) | `< 5 s` | `< 2 s` | Boot timer |
| Memory (heap) | `< 1.5 GB` | `< 2 GB` | Memory profiler |
| Draw calls per frame | `< 500` | `< 200` | GPU profiler |

---

## 4. Load Profile

> Define expected traffic so tests are calibrated to reality.

| Scenario | Concurrent users | Requests/second | Notes |
|----------|-----------------|-----------------|-------|
| Normal weekday | `<500>` | `<100>` | Baseline |
| Peak (daily) | `<2 000>` | `<400>` | Evening `<HH:MM – HH:MM TZ>` |
| Launch spike | `<10 000>` | `<2 000>` | First 30 min after major announcement |
| Seasonal peak | `<5 000>` | `<1 000>` | `<Black Friday / fiscal year-end>` |

**Growth assumption:** `<2×>` traffic year-over-year. Infrastructure must scale to `<next year's peak>` without redesign.

**Spike policy:** The system must degrade gracefully — return cached content or queue work — rather than fail with 5xx errors during a spike.

---

## 5. Infrastructure & Scaling Strategy

| Concern | Decision |
|---------|---------|
| Horizontal scaling | `<Auto Scaling Group (AWS) | HPA (Kubernetes) | Fly.io autoscale>` |
| Scale-out trigger | CPU `> 70%` for 2 min OR request queue depth `> 100` |
| Scale-in delay | 10 min (avoid flapping) |
| Database scaling | `<Read replicas for read-heavy queries; connection pooling via PgBouncer>` |
| Cache layer | `<Redis — cache rendered pages / API responses / session data; TTL: see below>` |
| CDN | `<Cloudflare / CloudFront — static assets: 1 year Cache-Control; HTML: no-cache>` |
| Rate limiting | `<100 req/min per IP on public endpoints; 1 000 req/min per authenticated user>` |
| Circuit breaker | `<Opossum / Resilience4j — trip at 50% error rate over 10 s; half-open after 30 s>` |

**Cache TTL table:**

| Resource | TTL | Invalidation |
|----------|-----|-------------|
| Static assets (JS, CSS, images) | 1 year (immutable) | Content-hash filename |
| API: read-only list responses | `<60 s>` | Event-driven purge on write |
| API: user-specific data | `<0 — no shared cache>` | Private cache only |
| HTML pages (SSR) | `<10 s stale-while-revalidate>` | CDN purge on deploy |
| Search results | `<30 s>` | Purge on content change |

---

## 6. Observability Setup

> Performance is invisible without measurement. Define what to instrument.

### 6.1 Metrics to Collect

| Signal | Tool | Key metrics |
|--------|------|------------|
| Frontend RUM | `<Datadog RUM | Grafana Faro | Sentry Performance>` | LCP, INP, CLS, JS error rate |
| Backend APM | `<Datadog APM | OpenTelemetry + Tempo>` | Request duration p50/p95/p99, error rate, throughput |
| Infrastructure | `<CloudWatch | Prometheus + Grafana>` | CPU, memory, disk I/O, network |
| Database | `<pg_stat_statements | Datadog DB Monitoring>` | Query duration, wait events, connections |
| Cache | `<Redis INFO | Prometheus redis_exporter>` | Hit rate, eviction rate, memory usage |
| Custom business metrics | `<StatsD / Prometheus custom metrics>` | `<e.g. Orders per minute, pipeline rows/sec>` |

### 6.2 Alerting Thresholds

| Alert | Threshold | Severity | Action |
|-------|-----------|---------|--------|
| API p95 response time | `> 500 ms` for 5 min | P1 | Page on-call |
| Error rate (5xx) | `> 1%` for 2 min | P0 | Page on-call + auto-rollback option |
| LCP (RUM) | `> 4 s` for 10 min | P2 | Slack alert |
| DB connection pool | `> 80%` utilisation | P1 | Slack + PagerDuty |
| Cache hit rate | `< 70%` | P2 | Slack alert |
| Auto-scale ceiling hit | Any instance at 90% CPU | P1 | Slack alert |

---

## 7. Performance Testing in CI/CD

> How performance is gated. See `.claude/templates/testing-strategy.md` §2.7 for full test setup.

| Test type | Tool | Environment | Cadence | Pass/fail criteria |
|-----------|------|-------------|---------|-------------------|
| Bundle size check | `<size-limit / Bundlewatch>` | CI (every PR) | Per PR | Fail if JS > budget |
| Lighthouse CI | `<LHCI>` | CI (every PR) | Per PR | Fail if score < 90 |
| Load test (baseline) | `<k6 / Locust>` | Staging | Nightly | p95 < budget; error rate < 0.1% |
| Load test (peak) | `<k6>` | Staging | Pre-release | 2× baseline RPS sustained 30 min |
| Spike test | `<k6>` | Staging | Pre-release | System recovers within 30 s |

---

## 8. Optimization Backlog

> Known performance improvements, prioritised. Update this as profiling reveals new bottlenecks.

| Priority | Item | Expected gain | Effort | Owner | Status |
|----------|------|--------------|--------|-------|--------|
| P0 | `<e.g. Add database index on users.email>` | `<Query time: 200 ms → 5 ms>` | `<XS>` | `<Backend lead>` | `<Todo>` |
| P1 | `<e.g. Lazy-load non-critical JS chunks>` | `<TTI: -0.8 s>` | `<S>` | `<Frontend lead>` | `<In progress>` |
| P1 | `<e.g. Serve images in WebP/AVIF via CDN>` | `<Image bytes: -60%>` | `<S>` | `<DevOps>` | `<Todo>` |
| P2 | `<e.g. Paginate /api/items (currently unbounded)>` | `<Eliminates timeout risk at scale>` | `<M>` | `<Backend>` | `<Todo>` |
| P2 | `<e.g. Cache expensive report query in Redis>` | `<Report load: 8 s → 0.3 s>` | `<M>` | `<Backend>` | `<Todo>` |
| P3 | `<e.g. Preconnect to third-party analytics origin>` | `<LCP: -100 ms>` | `<XS>` | `<Frontend>` | `<Todo>` |

---

## 9. Device & Network Test Matrix

> Ensure budgets are measured on realistic devices, not just developer machines.

### Web

| Tier | Device profile | CPU throttle | Network |
|------|---------------|-------------|---------|
| Low-end mobile | Moto G4-class | 4× slowdown | Slow 3G (1.5 Mbps) |
| Mid-range mobile | Pixel 5-class | 2× slowdown | 4G (12 Mbps) |
| Desktop | MacBook / i5 | None | Broadband |

### Mobile (Native)

| Tier | iOS device | Android device |
|------|-----------|---------------|
| Minimum spec | `<iPhone 12>` | `<Pixel 4a, Android 10>` |
| Target spec | `<iPhone 15>` | `<Pixel 8, Android 14>` |

### Game

| Tier | Device | GPU |
|------|--------|-----|
| Minimum | `<e.g. GTX 970 / Intel HD 630>` | `<Integrated / low-end discrete>` |
| Recommended | `<e.g. RTX 3060>` | `<Mid-range discrete>` |

---

## 10. Open Questions

| # | Question | Owner | Date needed |
|---|----------|-------|-------------|
| 1 | `<e.g. What is the expected user count at launch? Affects infra provisioning.>` | `<PM>` | `<YYYY-MM-DD>` |
| 2 | `<e.g. Do we need a CDN for API responses or only assets?>` | `<Arch lead>` | `<YYYY-MM-DD>` |
| 3 | `<e.g. Is a 2 s cold-start acceptable on low-end Android or must we target 1 s?>` | `<Mobile lead + PM>` | `<YYYY-MM-DD>` |

---

## 11. Related Documents

- Architecture: `.claude/templates/architecture.md`
- Testing strategy (performance tests section): `.claude/templates/testing-strategy.md`
- Mobile spec (mobile budgets): `.claude/templates/mobile-spec.md`
- Production readiness checklist: `.claude/checklists/production.md`
- Security model (rate-limiting, DoS controls): `.claude/templates/security-model.md`

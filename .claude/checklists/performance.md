# Performance Checklist
Passing this gate proves the system meets its latency, throughput, resource efficiency, and scaling targets under realistic load — verified by instrumentation and load tests, not by local timing or intuition. Severity tiers: P0=blocker, P1=important (fix shortly after launch), P2=hardening, P3=post-launch / backlog (track and revisit; never blocks shipping).

## P0 — Blockers (must pass before launch)

- [ ] All API endpoints that back user-facing screens respond within the agreed latency budget at p95 under representative load — verified by a load test against staging, not local timing. Default target: ≤ 200 ms p95 for read endpoints, ≤ 500 ms p95 for write endpoints. Exceptions require written justification.
- [ ] No N+1 query pattern exists on any hot path: verified by inspecting ORM query logs, slow-query logs, or an APM query trace at the controller/resolver level. Each relationship traversal that emits a query per row is rewritten to a JOIN, eager-load, or batched query (DataLoader, `IN (...)`, etc.).
- [ ] Every database column used in `WHERE`, `JOIN`, `ORDER BY`, or `GROUP BY` has an appropriate index. `EXPLAIN ANALYZE` (PostgreSQL), `EXPLAIN` (MySQL/MariaDB), or the equivalent for the project's DB engine confirms no full-table scans on tables with more than 10,000 rows in the production data model.
- [ ] All list and search endpoints enforce a maximum page size in the server — not enforced only by the client. Requests without a `limit` parameter either default to a safe cap or return an error. No endpoint can return an entire table in one call.
- [ ] Memory leaks are verified absent: the process heap is stable (not monotonically growing) under a 30-minute soak test at expected peak concurrency, measured by heap snapshots or process memory sampling at 1-minute intervals.
- [ ] No third-party script, SDK, or widget blocks the main thread for more than 50 ms (measured via Chrome DevTools Performance panel, Lighthouse Total Blocking Time, or a profiler for non-browser platforms). Blocking third-party code is loaded async or moved to a worker.
- [ ] Background jobs and batch processes have: a per-job execution timeout, a max-concurrency limit, and a dead-letter queue or failed-job log. They cannot starve the application thread pool or connection pool under normal or failure conditions.
- [ ] The application's critical user path meets the agreed performance budget for the platform type:
  - Web: Largest Contentful Paint (LCP) ≤ 2.5 s, First Input Delay (FID) / Interaction to Next Paint (INP) ≤ 200 ms, Cumulative Layout Shift (CLS) ≤ 0.1 — Core Web Vitals "Good" thresholds on a mid-range Android device on a 4G connection.
  - Mobile native: app cold-start to interactive ≤ 2 s on a mid-range device; frame rate ≥ 60 fps on all scrollable lists and animations.
  - CLI: command response ≤ 500 ms for interactive sub-commands; ≤ 2 s for operations that read from disk or network on typical hardware.
  - Backend API: p99 latency within 3× of p95 (no long tail); request timeout on all outbound calls.
  - Game: frame time ≤ 16.7 ms (60 fps) or ≤ 11.1 ms (90 fps) for the target platform at minimum spec hardware; no frame spikes > 2× the target frame time during normal gameplay.
- [ ] Database connection pool is sized and tested: pool exhaustion does not crash the service or return 500 errors. Overflow requests queue with a bounded wait timeout and return a 429 or 503 with a `Retry-After` header.

## P1 — Important (fix before scaling / shortly after launch)

- [ ] Caching strategy is documented, implemented, and tested for every expensive read operation: HTTP cache headers (`Cache-Control`, `ETag`, `Last-Modified`) for HTTP responses; in-process LRU/LFU cache for hot small objects; distributed cache (Redis/Memcached/Valkey) for shared cross-instance data. Cache invalidation logic is explicit and tested.
- [ ] Static assets are served with `Cache-Control: public, max-age=31536000, immutable` and content-addressed filenames (build hash in the URL) for optimal CDN hit rate. First-party fonts and icons are self-hosted or preloaded, not loaded from a cross-origin CDN that blocks rendering.
- [ ] Images and video are served at appropriate resolutions (responsive `srcset` for web, platform-specific asset catalogs for mobile); compressed to a modern format (WebP or AVIF for images, H.264/H.265/AV1 for video); lazy-loaded for below-the-fold content. No image > 200 KB is served at the original upload size without transformation.
- [ ] Slow-query and slow-transaction monitoring is configured: alerts fire when any query exceeds 500 ms (database) or any trace span exceeds 1 s (application), with the query text and caller captured.
- [ ] All operations with expected duration > 500 ms are offloaded to a background queue: email delivery, PDF/report generation, large file processing, third-party webhook delivery, batch data exports. Users receive an immediate acknowledgement and a status-poll endpoint or webhook callback.
- [ ] API and page payload sizes are audited: the largest typical API response is < 1 MB after compression; binary blobs (files, images, exports) are streamed to the client rather than buffered in application memory.
- [ ] HTTP response compression is enabled for all text-based responses ≥ 1 KB: Brotli where the client supports it (`Accept-Encoding: br`), gzip as fallback. Compression is verified by inspecting the `Content-Encoding` response header in a live request.
- [ ] Frontend bundle size is within budget: initial JavaScript bundle ≤ 200 KB gzipped for web apps (excluding large-but-necessary vendor libraries with explicit justification); code-splitting is in place so routes load only what they need.
- [ ] Read-heavy queries use read replicas or a query-specific cache so write load on the primary database does not affect read latency under peak concurrent usage.

## P2 — Hardening / nice-to-have

- [ ] Performance regression tests (k6, Gatling, Locust, Artillery, or equivalent) are added to CI or a scheduled job; the build flags a regression when p95 latency degrades by more than 20% or throughput drops by more than 15% versus the established baseline.
- [ ] CDN is configured for static assets and, where appropriate, for edge-cached API responses with correct `Vary` headers and surrogate-key-based purging strategy.
- [ ] Auto-scaling policy (HPA, ASG, Cloud Run min/max instances, or equivalent) is defined, tested with a burst load scenario in staging, and tuned so scale-out begins before latency degrades past SLA thresholds (scale-out lag < 2 minutes under a step-load increase).
- [ ] A CPU flame graph and heap snapshot baseline is committed to the repo (or stored as a CI artifact) so future performance regressions can be diffed against a known-good state.
- [ ] HTTP/2 or HTTP/3 is enabled on all public-facing endpoints; multiplexing eliminates per-request TCP handshake overhead for browsers and mobile clients that support it.
- [ ] Query depth limits, complexity limits, and field-count limits are set for GraphQL APIs to prevent deliberately expensive introspection or nested queries from exhausting DB or CPU resources.
- [ ] Cold-start latency is measured and minimized for serverless functions (Lambda, Cloud Run, Azure Functions): cold start < 1 s for synchronous user-facing functions; provisioned concurrency or warm-up pings configured for latency-critical paths.

## P3 — Post-launch / backlog (track and revisit after launch; never blocks shipping)

- [ ] Continuous performance profiling (Pyroscope, Clinic.js, async-profiler, or equivalent) is running in production with sampling enabled; flame graphs for CPU and heap are stored as weekly artifacts so regressions are visible without reproducing them locally.
- [ ] Database query plan regression detection is automated: slow-query log thresholds are tightened from 500 ms to 200 ms, and any new query plan that introduces a sequential scan on a table > 1,000 rows triggers a Slack alert and a required index review.
- [ ] Resource rightsizing review is scheduled every 90 days: CPU/memory utilization P95 over the preceding period is compared against reserved capacity, and over-provisioned instances are downsized or spot/preemptible options are adopted to reduce cost without degrading SLAs.
- [ ] Frontend performance budget is enforced in CI with per-route bundle-size and Core Web Vitals regression thresholds; any route whose LCP degrades by > 10% versus the previous release baseline blocks the PR until the regression is explained and accepted.
- [ ] GraphQL or REST query complexity limits and depth caps are tuned based on 30 days of production trace data to tighten the maximums without impacting legitimate client requests.

## How to use
Run the `../skills/performance/SKILL.md` audit skill or invoke `../commands/audit-performance.md` to populate this checklist. The primary owner is `../agents/quality/performance-engineer.md`. Re-run this checklist after any change that touches: database schema or ORM queries, data-access layers, frontend bundle configuration, caching configuration, or infrastructure scaling settings. Cross-reference `../checklists/qa.md` for load-test execution and `../checklists/production.md` for load-test sign-off before scaling to production traffic. Reviewer marks each item `[x]` when satisfied or `[-]` when explicitly waived with a written reason, the measured alternative metric, and the risk classification.

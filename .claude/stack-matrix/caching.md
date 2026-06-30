# Caching Stack Matrix

Caching trades freshness and complexity for latency and cost. Choose by answering: (1) **Where** does the cache live — inside the app process, in a shared network service, or at the edge near the user? (2) **What** are you caching — rendered HTML/assets, expensive query results, computed objects, or session state? (3) **How fresh** must it be — can readers tolerate staleness measured in seconds, minutes, or not at all? Most production systems layer caches: an edge/CDN tier for static and cacheable responses, a distributed tier (Redis) for shared application data, and a small in-process tier for the hottest, smallest objects. Add caching only where a measured hot path justifies it — a cache is a second source of truth, and every one you add is a correctness and invalidation liability.

Key decision drivers: locality (process vs. cluster vs. edge), invalidation difficulty, consistency tolerance, dataset size vs. memory budget, multi-instance coherence, and operational overhead.

---

## Comparison Table

| Option | Tier | Scope | Latency | Invalidation control | Ops complexity | Best for |
|---|---|---|---|---|---|---|
| In-process (Caffeine / Guava / `lru-cache`) | App memory | Single instance | Nanoseconds | Hard across instances | None | Tiny, hot, read-mostly data |
| Memcached | Distributed | Shared cluster | Sub-ms (LAN) | Manual (key delete) | Low-Medium | Simple shared object/string cache |
| Redis | Distributed | Shared cluster | Sub-ms (LAN) | Rich (keys, TTL, pub/sub) | Medium | Shared app cache, sessions, rate limits |
| Varnish | Reverse proxy | Origin edge | Sub-ms | VCL purge / ban | Medium | Cacheable HTML in front of an origin |
| Cloudflare | CDN / edge | Global PoPs | Single-digit ms | Tag/URL purge API | Low (managed) | Global static + cacheable dynamic |
| Fastly | CDN / edge | Global PoPs | Single-digit ms | Instant surrogate-key purge | Low-Medium | Edge logic, instant purge at scale |
| AWS CloudFront | CDN / edge | Global PoPs | Single-digit ms | Path invalidation | Low (managed) | AWS-native asset + API delivery |
| Akamai | CDN / edge | Largest PoP footprint | Single-digit ms | Fast purge | Medium (enterprise) | Enterprise scale, media, hard reach |

---

## In-process cache (Caffeine, Guava, `lru-cache`)

- **When to use:** The hottest, smallest, read-mostly data that every request touches — feature flags, config, reference lookups, compiled templates. When you want zero network hops and the data is cheap to recompute or rarely changes.
- **When NOT to use:** Anything that must be coherent across instances, large datasets (you pay the memory on every node), or data whose staleness has real consequences. Horizontally scaled fleets get N divergent copies.
- **Strengths:** Fastest possible (in-heap, nanoseconds); no extra infrastructure; Caffeine offers excellent eviction (W-TinyLFU), size/time-based expiry, and async refresh.
- **Weaknesses:** No cross-instance coherence; cache duplicated per process; lost on restart/deploy; competes with the app for heap (GC pressure).
- **Risks:** Stale reads after a write lands on a different instance; unbounded growth if size limits are not set; memory pressure causing GC pauses or OOM.

---

## Memcached

- **When to use:** A simple, large, shared cache of opaque blobs/strings where you want predictable memory and horizontal scale-out by adding nodes. Classic in front of a database for query-result caching.
- **When NOT to use:** When you need data structures, persistence, pub/sub, or atomic operations beyond get/set/incr — that is Redis territory.
- **Strengths:** Dead simple; multithreaded so it uses all cores well; very predictable LRU memory behaviour; trivially horizontally partitioned by client-side hashing.
- **Weaknesses:** Values only (no lists/sets/sorted-sets); no native persistence or replication; no built-in invalidation beyond delete; consistent-hashing is the client's job.
- **Risks:** Node loss drops its share of keys (thundering herd to the origin); no TLS/auth in older deployments — keep it on a private network.

---

## Redis

- **When to use:** The default distributed cache for almost any app. Cached query results and computed objects, session store, rate-limit counters, leaderboards, and pub/sub for cache-invalidation fan-out. The right answer when one shared cache must serve a fleet.
- **When NOT to use:** As the only source of truth for durable business data (it is a cache, configure persistence deliberately); when dataset far exceeds an affordable RAM budget; pure static-asset delivery (use a CDN).
- **Strengths:** Sub-millisecond; rich types (hashes, sorted sets, streams, bitmaps); TTLs per key; Lua for atomic multi-step ops; pub/sub and keyspace notifications enable event-driven invalidation; Redis Cluster and managed tiers (ElastiCache, Upstash, Redis Cloud) scale horizontally.
- **Weaknesses:** Cost scales with RAM; persistence (RDB/AOF) adds latency and tuning; eviction can silently drop entries; cluster mode complicates multi-key operations.
- **Risks:** `maxmemory` eviction dropping data you assumed was present; AOF rewrite pausing; treating it as a primary store without persistence; hot keys overloading a single shard.

---

## Varnish

- **When to use:** A reverse-proxy HTTP cache in front of your own origin to serve cacheable HTML and API responses without hitting app servers. Strong when you control cache rules tightly via VCL and host the cache yourself.
- **When NOT to use:** When a managed CDN already fronts your traffic globally (Varnish is single-region unless you build out PoPs yourself); HTTPS-heavy setups where you would rather not terminate TLS in front of Varnish.
- **Strengths:** Extremely fast for HTML; VCL gives surgical control over what is cached, for how long, and how it is purged (`purge`/`ban`); grace mode serves stale-while-revalidate during backend trouble.
- **Weaknesses:** VCL is its own language and a learning curve; no native TLS (front it with a TLS terminator); you operate and scale it yourself.
- **Risks:** Caching authenticated/personalised responses by accident (leak between users); ban-list growth degrading performance; cache key misconfiguration causing wrong-content delivery.

---

## CDN / edge — Cloudflare, Fastly, AWS CloudFront, Akamai

- **When to use:** Caching static assets (JS/CSS/images/video) and cacheable dynamic responses at PoPs close to users, globally. The first cache every public web property should have. Cloudflare for breadth + DDoS + ease; Fastly for instant purge and edge logic; CloudFront for AWS-native pipelines (S3/Lambda@Edge); Akamai for the largest footprint and enterprise media.
- **When NOT to use:** Highly personalised, per-user dynamic content with no cacheable surface (cache only fragments or skip); strict data-residency rules that forbid edge replication.
- **Strengths:** Global latency reduction; origin-offload (huge cost saving); built-in TLS, compression, and (Cloudflare/Akamai) DDoS protection; edge compute (Workers / Compute@Edge / Lambda@Edge) for logic near users; surrogate-key/tag purge (Fastly, Cloudflare) for targeted invalidation.
- **Weaknesses:** Invalidation latency varies — Fastly purges in ~150 ms, CloudFront path invalidation can take longer; per-provider config models differ (vendor lock-in of cache rules); cost models (requests + egress) need watching.
- **Risks:** Caching `Set-Cookie` or auth responses and leaking them across users; missing/incorrect `Cache-Control`/`Vary` headers causing stale or unshareable caches; purge storms; origin shielding misconfigured so the origin still gets hammered.

---

## Read-through vs. write-through vs. write-behind

- **Read-through (cache-aside):** App checks cache; on miss, loads from source, populates cache, returns. Simplest and most common. Risk: the miss path is where **stampedes** happen. Best default for most caches.
- **Write-through:** Writes go to the cache and the source synchronously, so the cache is always warm and consistent. Costs write latency; good when reads vastly outnumber writes and staleness is unacceptable.
- **Write-behind (write-back):** Writes hit the cache and are flushed to the source asynchronously. Lowest write latency, highest throughput — but a cache failure can lose unflushed writes. Only with durability guarantees and acceptable data-loss risk.

---

## Invalidation strategies

- **TTL expiry:** Simplest — set a time bound and accept staleness up to the TTL. Use everywhere as a safety net even when you also invalidate explicitly.
- **Explicit delete/purge on write:** Invalidate the affected key(s) when the underlying data changes. Precise but requires the write path to know every cache key it affects.
- **Tag / surrogate-key purge:** Tag cached entries by entity (e.g. `product-42`); purge by tag to drop all related entries at once (Fastly surrogate keys, Cloudflare cache tags). Best for dependency-heavy invalidation.
- **Event-driven (pub/sub):** Publish a change event; subscribers evict in-process caches across the fleet (Redis keyspace notifications or a message bus). Needed to keep in-process caches coherent.
- **Versioned keys:** Embed a version/hash in the key (`user:42:v7`); bump the version to logically invalidate without deleting. Avoids race conditions in distributed invalidation.

---

## Cache stampede (thundering herd)

When a hot key expires, many concurrent requests miss simultaneously and all hammer the origin to recompute the same value, often collapsing it. Defences:

- **Request coalescing / single-flight:** Let one request recompute while others wait for its result (Caffeine does this in-process; implement a per-key lock in Redis for distributed cases).
- **Probabilistic early expiration (XFetch):** Refresh a value slightly before its TTL, jittered, so not everything expires at the same instant.
- **Stale-while-revalidate:** Serve the stale value and refresh in the background (`Cache-Control: stale-while-revalidate`, Varnish grace mode, CDN-level SWR).
- **Locked recompute with fallback:** First miss takes a short-lived lock and recomputes; others serve stale or wait briefly.
- **Jittered TTLs:** Never give a whole batch of keys the same expiry; add randomness so expirations spread out.

---

## Recommended combinations

- **Cloudflare (edge) + Redis (app) + Caffeine (in-process)** — The canonical three-tier web stack: CDN absorbs static + cacheable responses, Redis caches shared query results and sessions, in-process holds the tiny hottest objects. Each tier shrinks load on the one below.
- **Fastly + Redis** — When you need instant, surgical purge: tag cached pages with surrogate keys, purge by entity on write in ~150 ms, with Redis for application data and rate limits.
- **CloudFront + ElastiCache (Redis) + DynamoDB** — AWS-native: CloudFront for delivery and origin shield, ElastiCache for the hot path / session store, DynamoDB as the durable store.
- **Varnish + origin app** — Self-hosted, single-region HTML acceleration when you want full VCL control and are not on a global CDN; add grace mode for resilience.
- **Memcached + RDBMS** — Minimal, proven query-result cache for a read-heavy app that needs nothing beyond get/set; scale by adding nodes.
- **Akamai + Redis** — Enterprise media/global reach at the edge with Redis for shared application state behind the origin.

Cross-reference: `.claude/stack-matrix/database.md` (Redis as a data store and its persistence/eviction tradeoffs), `.claude/stack-matrix/realtime.md` (pub/sub fan-out for event-driven invalidation), and `.claude/checklists/performance.md` for setting and enforcing cache-hit-rate and latency targets.

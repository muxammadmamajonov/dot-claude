---
name: redis
description: >
  Activate when the project uses Redis (or Valkey / Upstash / Redis Cloud / KeyDB)
  for caching, session storage, rate limiting, queuing (BullMQ, Sidekiq, Celery),
  pub/sub messaging, leaderboards, or distributed locks. Also activate when
  diagnosing cache stampedes, key eviction issues, or memory pressure.
---

# Redis Skill

## When to use

- Adding a caching layer in front of a database, API, or expensive computation
- Implementing distributed rate limiting, session storage, or idempotency keys
- Designing a job queue with BullMQ (Node), Celery (Python), Sidekiq (Ruby), or Resque
- Setting up Redis pub/sub or Redis Streams for event fan-out
- Diagnosing high memory usage, eviction storms, or hot-key contention
- Building leaderboards, counters, or sliding-window analytics with sorted sets

---

## Workflow

1. **Choose the right data structure first** — string for simple cache values, hash for objects with partial updates, sorted set for leaderboards/rate-limit windows, list for FIFO queues, stream for event logs with consumer groups.
2. **Define a key naming convention** before writing any code: `<app>:<entity>:<id>:<field>` e.g. `api:user:abc123:session`. Document it in a `redis-keys.md` or inline comment.
3. **Set TTL on every cache key** — call `SET key value EX <seconds>` or `EXPIRE key <seconds>`. Never store a key without a TTL unless it is a permanent registry (leaderboard, session index).
4. **Implement cache-aside pattern**:
   a. Try `GET key`.
   b. On miss: fetch from source, `SET key value EX <ttl>`, return value.
   c. On hit: return cached value.
   Use a short jitter on TTL (±10%) to prevent stampedes on mass-expiry.
5. **For queues**: use BullMQ (Node), Celery + Redis broker (Python), or Sidekiq (Ruby). Define job retry count, backoff strategy, and dead-letter queue before deploying workers.
6. **For distributed locks**: use the Redlock algorithm (`ioredis-lock`, `redlock` npm, `pottery` Python) — not raw `SETNX`. Always set a lock expiry shorter than the expected operation duration + safety margin.
7. **Monitor**: check `INFO memory`, `INFO stats`, `SLOWLOG GET 25`, and `MONITOR` (briefly, in dev only). Set `maxmemory` and `maxmemory-policy` in `redis.conf`; `allkeys-lru` is the safest default for pure cache deployments.
8. **Connection pooling**: use a shared client instance (singleton) per process; never create a new connection per request. Configure `maxRetriesPerRequest` and connection timeouts.

---

## Standards

### Do
- Use pipelining (`MULTI/EXEC` or client pipeline API) when issuing 3+ sequential commands in one logical operation.
- Prefix all keys with an environment namespace (`prod:`, `staging:`) when sharing a Redis instance across environments.
- Use `SCAN` instead of `KEYS *` in production — `KEYS` blocks the event loop.
- Store large values as compressed JSON (zstd or gzip) to reduce memory and network overhead.
- Set `requirepass` and TLS in production; use ACL rules to limit each service to only the key prefixes it owns.
- Use Redis Streams (not pub/sub) when message delivery durability is required — pub/sub drops messages when there are no subscribers.

### Do not
- Do not use Redis as a primary database for business-critical data — treat it as an ephemeral store.
- Do not store secrets, PII, or payment card data in Redis unless the instance is encrypted at rest and access is tightly ACL-controlled.
- Do not use blocking commands (`BLPOP`, `BRPOP`) in the same connection used for non-blocking operations — they can starve other requests.
- Do not store values larger than 10 MB in a single key; this causes latency spikes for all clients sharing the instance.
- Do not use `FLUSHDB`/`FLUSHALL` in any automated script without an explicit human approval gate.
- Do not issue `MONITOR` in production beyond short diagnostic windows — it can double Redis CPU load.

---

## Common mistakes to avoid

| Mistake | Consequence | Fix |
|---|---|---|
| No TTL on cache keys | Memory fills up; old data served forever | Always pass `EX` or `PX` in `SET`; audit with `TTL <key>` |
| Cache stampede on popular key expiry | Hundreds of DB queries simultaneously | Add random jitter to TTL; use a probabilistic early refresh (XFetch pattern) |
| Using `KEYS *` in production | Blocks Redis for seconds on large keyspaces | Replace with `SCAN 0 MATCH prefix:* COUNT 100` with a cursor loop |
| One Redis connection per HTTP request | Connection exhaustion | Use a singleton client with a connection pool |
| Storing entire ORM objects in cache | Stale nested objects; large serialization overhead | Cache only IDs or slim DTOs; rebuild the full object from DB on cache miss |
| Pub/sub for reliable task delivery | Worker restart drops in-flight messages | Use Redis Streams with `XREADGROUP` and `XACK` for at-least-once delivery |
| Not setting `maxmemory-policy` | Redis fills RAM, crashes, or starts refusing writes | Set `maxmemory 512mb` + `maxmemory-policy allkeys-lru` in config |

---

## Output format

Client setup (Node / `ioredis`):
```ts
// lib/redis.ts — singleton pattern
import Redis from "ioredis";
const redis = new Redis(process.env.REDIS_URL!, {
  maxRetriesPerRequest: 3,
  enableReadyCheck: true,
  lazyConnect: false,
});
export default redis;
```

Cache-aside helper:
```ts
async function cached<T>(key: string, ttlSeconds: number, fetch: () => Promise<T>): Promise<T> {
  const hit = await redis.get(key);
  if (hit) return JSON.parse(hit) as T;
  const value = await fetch();
  await redis.set(key, JSON.stringify(value), "EX", ttlSeconds + Math.floor(Math.random() * 30));
  return value;
}
```

---

## Related checklists
- `.claude/checklists/performance.md`
- `.claude/checklists/security.md`
- `.claude/checklists/devops.md`

## Related agents
- `.claude/agents/engineering/backend-engineer.md`
- `.claude/agents/quality/performance-engineer.md`
- `.claude/agents/engineering/infrastructure-engineer.md`

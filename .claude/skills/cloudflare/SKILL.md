---
name: cloudflare
description: >
  Activate for any Cloudflare Workers, Pages, D1, R2, KV, Durable Objects, Queues,
  AI Gateway, WAF, Turnstile, or edge architecture work. Triggers: Cloudflare, Workers,
  D1, R2, KV, Durable Objects, Hyperdrive, Queues, Workers AI, Turnstile, Wrangler,
  Pages, or "deploy to edge".
---

# Cloudflare

## When to use
- Building or reviewing Cloudflare Workers / Pages applications
- Designing state at the edge: KV, D1 (SQLite), R2 (object storage), Durable Objects
- Event-driven edge patterns with Queues
- Security configuration: WAF, rate limiting, Turnstile (bot detection), mTLS
- Edge caching strategy, Cache API, cache rules
- Migrating from traditional servers to edge-native architecture
- Workers AI (inference at edge) or AI Gateway (LLM proxy)
- Multi-tenant isolation using Durable Objects

## Workflow

1. **Determine runtime environment:** Workers (V8 isolates, no Node.js by default) vs Workers for Platforms (multi-tenant). Understand what's NOT available: no filesystem, no native Node.js modules, limited `process.*`. Use `nodejs_compat` compatibility flag sparingly for npm packages that require it.

2. **Choose the right storage primitive:**
   - **KV (Workers KV):** globally replicated key-value, eventually consistent (15-60 s lag). Best for read-heavy config, feature flags, static data, session tokens. Not suitable for counters or real-time state.
   - **D1 (SQLite at the edge):** relational SQL, strongly consistent per D1 database, replicated read. Best for structured data, user records, content. Use `prepare().bind()` for parameterized queries — never string interpolation. Supports D1 Sessions for read-your-writes consistency.
   - **R2 (Object Storage):** S3-compatible, zero egress fees. Best for large files, user uploads, static assets, backups. Use presigned URLs for direct browser upload. Bind via `env.BUCKET`.
   - **Durable Objects (DO):** single-threaded stateful actor, globally unique per ID. Best for collaborative editing, rate limiters, WebSocket chat rooms, real-time coordination, counters. Each DO runs in one Cloudflare location — co-locate with users using `idFromName()` with geographic sharding or user ID.
   - **Queues:** at-least-once message delivery between Workers. Producer Worker enqueues; consumer Worker batch-processes. Use for background jobs, webhook fan-out, retry logic. Max message size 128 KB; max batch size 10,000 messages.
   - **Hyperdrive:** connection pooling proxy for external PostgreSQL/MySQL. Reduces cold-start latency to remote databases. Bind as `env.DB` with standard `pg` driver using `nodejs_compat`.

3. **Worker structure (TypeScript, Wrangler v3+):**
   ```typescript
   export default {
     async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> { ... },
     async queue(batch: MessageBatch<T>, env: Env): Promise<void> { ... },
     async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext): Promise<void> { ... },
   } satisfies ExportedHandler<Env>;
   ```
   - Always type `Env` from wrangler-generated types (`wrangler types`).
   - Use `ctx.waitUntil()` for fire-and-forget async work that must complete after response is sent.
   - Use `ctx.passThroughOnException()` to fall back to origin on unhandled errors.

4. **Durable Objects design:**
   - One DO class = one actor type. Each instance is a single JavaScript object running in one location.
   - Use `this.state.storage` (transactional SQLite under the hood in DO Storage) for durable state.
   - WebSocket hibernation API (`acceptWebSocket()`) keeps the DO alive only when messages arrive — dramatically reduces cost for chat/presence.
   - Use `this.state.blockConcurrencyWhile()` for initialization to prevent race conditions.
   - Avoid storing large blobs in DO storage; reference R2 instead.
   - DO IDs: `idFromName(string)` for deterministic routing (e.g., `idFromName(roomId)`); `newUniqueId()` for auto-generated.
   - Alarm API: schedule future callbacks without external cron. Use for TTL cleanup, scheduled aggregation.

5. **D1 SQL patterns:**
   ```typescript
   // Parameterized query — always
   const result = await env.DB.prepare("SELECT * FROM users WHERE id = ?").bind(userId).first();
   // Batch for transactions
   await env.DB.batch([
     env.DB.prepare("INSERT INTO orders (user_id, total) VALUES (?, ?)").bind(userId, total),
     env.DB.prepare("UPDATE inventory SET qty = qty - ? WHERE sku = ?").bind(qty, sku),
   ]);
   ```
   - Use D1 migrations (`wrangler d1 migrations create`, `wrangler d1 migrations apply`) for schema changes.
   - Indexes are critical — SQLite query planner is the same as traditional SQLite.
   - D1 is not suitable for high-frequency writes (> 1000 writes/s) — use Durable Objects or Queues for write-heavy patterns.

6. **R2 patterns:**
   - List objects with `list({ prefix, cursor, limit })` — paginated.
   - Put with custom metadata: `put(key, body, { httpMetadata: { contentType }, customMetadata: { userId } })`.
   - Generate presigned URLs (time-limited): use `createPresignedUrl` from Workers R2 binding.
   - For public assets: attach custom domain to R2 bucket; enable public access; use Cache-Control headers.
   - Use R2 event notifications to trigger a Queue when objects are created/deleted.

7. **Security — WAF, rate limiting, Turnstile:**
   - **WAF:** enable Cloudflare Managed Ruleset + OWASP ruleset. Use custom rules for application-specific logic (e.g., block `/admin` from non-corporate IPs). Use rate limiting rules (requests/IP/period) in WAF.
   - **Rate limiting in Workers:** use KV or Durable Objects for IP-based rate limiting. DO is preferred for strict per-user limits. Pattern: DO per user/IP acting as rate limiter actor.
   - **Turnstile:** CAPTCHA-free bot detection. Client renders `<div class="cf-turnstile">`, submits token in form/JSON. Worker validates: `POST https://challenges.cloudflare.com/turnstile/v0/siteverify`. Verify server-side on every sensitive action.
   - **mTLS / API Shield:** validate client certificates at the edge for B2B APIs.
   - **Workers secrets:** use `wrangler secret put SECRET_NAME` — never commit secrets; access as `env.SECRET_NAME`.
   - **CORS:** handle `OPTIONS` preflight in Worker; set `Vary: Origin` header.

8. **Caching strategy:**
   - Cache API: `caches.default` — cache keyed by URL (and optionally custom key from `cf.cacheKey`).
   - Set `Cache-Control: public, max-age=N, s-maxage=N` for CDN caching.
   - Use Cache Rules in Cloudflare dashboard for path-based caching without Worker overhead.
   - Bypass cache for authenticated requests (`Authorization` header present or auth cookie set).
   - Use `cf.cacheTtlByStatus` to cache 404s briefly and prevent origin hammering.
   - Purge programmatically via Cloudflare API `POST /zones/{id}/purge_cache`.

9. **Workers AI:**
   - Run inference at the edge: `await env.AI.run('@cf/meta/llama-3.1-8b-instruct', { messages })`.
   - AI Gateway: proxy your OpenAI/Anthropic/etc. calls through `gateway.ai.cloudflare.com` — adds caching, rate limiting, logging, fallbacks.
   - Use AI Gateway for cost visibility and prompt caching across AI providers.
   - Vectorize: managed vector database for semantic search. Pair with Workers AI embeddings model.

10. **Wrangler & deployment:**
    - `wrangler.toml`: declare all bindings (`kv_namespaces`, `d1_databases`, `r2_buckets`, `durable_objects`, `queues`).
    - Environments: `[env.staging]` and `[env.production]` sections override defaults.
    - CI/CD: `wrangler deploy --env production` in GitHub Actions using `CF_API_TOKEN` secret (use API token with Workers:Edit scope, not global API key).
    - `wrangler dev --remote` for testing against real Cloudflare infrastructure bindings.
    - Use `wrangler tail` for live log streaming in production debugging.
    - Deployment rollback: `wrangler rollback` to previous version instantly.

## Standards

**Do:**
- Use TypeScript for all Workers — `strict: true` in tsconfig.
- Always parameterize D1 queries — SQL injection is possible even in SQLite.
- Set `compatibility_date` in `wrangler.toml` to a recent date and update quarterly.
- Use `nodejs_compat` flag only for packages that require it; prefer Web-standard APIs.
- Validate all Turnstile tokens server-side — client-side only is bypassable.
- Use `env.AI` bindings for Workers AI; avoid direct fetch to AI APIs from Worker when AI Gateway can proxy them.
- Scope API tokens to minimum permissions (Workers:Edit, D1:Edit, R2:Edit as needed).
- Use Cloudflare Pages for frontend + Worker backends via `functions/` directory (file-based routing).

**Do not:**
- Use `console.log` for sensitive data in Workers — logs are visible in Wrangler tail and Workers Logs dashboard.
- Rely on KV for real-time consistency — it is eventually consistent; use Durable Objects or D1 instead.
- Store secrets in `wrangler.toml` or environment variables in plain text — use `wrangler secret put`.
- Use `fetch` to call your own Worker recursively in a loop — can trigger subrequest limits (50 subrequests default).
- Block the event loop with synchronous CPU-intensive work > ~50 ms (Workers CPU time limit is 10 ms on Free, 30 s on Paid).
- Create a new Durable Object ID per request for shared state — use deterministic `idFromName()` to route to the same instance.
- Use Durable Objects for data you can afford to lose — they are durable but do not replace a replicated database for critical data.

## Common mistakes to avoid

- **KV for counters or real-time leaderboards:** KV eventual consistency means concurrent writes lose data. Use Durable Objects with atomic in-memory state.
- **D1 without indexes:** D1 uses SQLite; a full-table scan on millions of rows times out. Add indexes matching your `WHERE` and `ORDER BY` patterns.
- **Missing `await` on `ctx.waitUntil()`:** omitting it causes the promise to run but the runtime may kill it before completion. Always `ctx.waitUntil(promise)`.
- **Returning non-`Response` from fetch handler:** Workers runtime requires a `Response` object. Wrap errors in `new Response('error', { status: 500 })`.
- **Not handling WebSocket hibernation:** using `server.accept()` instead of `state.acceptWebSocket()` keeps the DO awake 24/7 even with no active connections — 100× more expensive.
- **Turnstile validation only on client:** the widget can be bypassed by replaying tokens or calling the API directly. Always verify the token in the Worker.
- **R2 without a CDN layer for public assets:** R2 requests are billed per operation; put CloudFlare CDN / Cache Rules in front to cache asset responses and avoid per-request charges.

## Output format

- Architecture decisions → `docs/decisions/cloudflare-<topic>-<date>.md` (use `.claude/templates/decision-record.md`)
- Worker specs → `docs/specs/architecture.md` (use `.claude/templates/architecture.md`)
- Security configuration → `docs/specs/security-model.md` (use `.claude/templates/security-model.md`)
- Deployment plan → `docs/deployment/cloudflare-deploy.md` (use `.claude/templates/deployment-plan.md`)

## Related checklists
- `.claude/checklists/architecture.md`
- `.claude/checklists/security.md`
- `.claude/checklists/performance.md`
- `.claude/checklists/production.md`
- `.claude/checklists/devops.md`

## Related agents
- `.claude/agents/core/solution-architect.md`
- `.claude/agents/engineering/backend-engineer.md`
- `.claude/agents/engineering/fullstack-engineer.md`
- `.claude/agents/engineering/cloud-architect.md`
- `.claude/agents/quality/security-auditor.md`
- `.claude/agents/quality/performance-engineer.md`

---
name: node-backend
description: >
  Activate when building, reviewing, or debugging Node.js backend services
  using NestJS, Fastify, or Express — API design, middleware, auth, database
  integration, testing, and production readiness. Use whenever the work touches
  Node/TypeScript server code, `package.json`, route handlers/controllers, or
  keywords like "nestjs", "fastify", "express", "middleware" — even if the user
  never says "backend".
---

# Node.js Backend Development

## When to use
- Writing REST or GraphQL APIs with Express, Fastify, or NestJS
- Designing middleware, guards, interceptors, or pipes
- Implementing authentication, authorization, or rate-limiting
- Integrating ORMs (Prisma, TypeORM, Drizzle) or raw query builders
- Writing unit/integration tests with Jest or Vitest
- Profiling performance or fixing memory leaks in a Node.js process

## Workflow

1. **Classify** — REST, GraphQL, gRPC, WebSocket, or worker/queue service.
2. **Choose the framework tier**:
   - NestJS: structured enterprise services (DI, modules, decorators, CLI scaffolding).
   - Fastify: high-throughput APIs where raw RPS matters; schema-first with JSON Schema.
   - Express: simple services or legacy projects; minimal overhead.
3. **Scaffold the project** using the framework CLI:
   - NestJS: `nest new my-service --strict`
   - Fastify: `npm create fastify`
   - Express: plain `npm init` + `express`, `helmet`, `pino` minimal setup
4. **Design the module/layer boundary**:
   - NestJS: `Module → Controller → Service → Repository`
   - Fastify/Express: `routes → handlers → services → data-access`
5. **Define data contracts first** — TypeScript interfaces or Zod/class-validator schemas before any handler code.
6. **Implement handlers** — keep controllers thin (parse, delegate, respond). Business logic lives in services.
7. **Authenticate and authorize** before any business logic:
   - JWTs: validate signature + expiry; never decode without `verify`.
   - API keys: constant-time comparison with `crypto.timingSafeEqual`.
8. **Add error handling globally** — NestJS: `ExceptionFilter`; Fastify: `setErrorHandler`; Express: 4-arg error middleware at the end.
9. **Write tests**: unit tests for services (mock dependencies), integration tests hitting the real DB via test containers.
10. **Harden**: helmet, cors (explicit allowlist), rate-limit, request size cap, SQL injection prevention via parameterised queries.
11. **Audit** against .claude/checklists/security.md and .claude/checklists/performance.md before deploying.

## Standards

### TypeScript
- Enable `strict: true`, `noImplicitAny`, `strictNullChecks` in `tsconfig.json`.
- Use `zod` or `class-validator` for runtime validation of all external input.
- Avoid `any`; use `unknown` and narrow explicitly.

### NestJS specifics
- One feature per module; no circular module imports — use forwardRef only as last resort.
- Providers are singletons by default; use `REQUEST` scope only when truly request-scoped.
- Use `@UseGuards`, `@UsePipes`, `@UseInterceptors` at the controller/handler level, not ad-hoc in services.
- Config: `@nestjs/config` with a typed `ConfigService`; never `process.env.X` inline.

### Fastify specifics
- Register all plugins with `fastify-plugin` wrapper to share decorations across encapsulation.
- Define JSON Schema for every route's `body`, `querystring`, `params`, `response` — this enables auto-validation and serialisation optimisation.
- Use Fastify's `pino` logger (already included); do not add Winston on top.

### Database
- Use connection pooling (pg-pool, Prisma connection limit, TypeORM pool config) — never create a new connection per request.
- All mutations must be in transactions for multi-step writes.
- Parameterise every query — never string-interpolate user input into SQL.
- Run migrations in CI before integration tests; never auto-migrate in production startup.

### Error model
- Return RFC 7807 Problem+JSON (`type`, `title`, `status`, `detail`, `instance`).
- 4xx for client errors, 5xx for server faults; never return a stack trace to clients.
- Log correlation IDs with every error; propagate `X-Request-ID` through service calls.

### Do not
- Do not use `require()` for dynamic plugin loading at request time — startup-time only.
- Do not store secrets in environment-unguarded constants; use `.env` + validation at startup.
- Do not swallow errors with empty `catch {}` blocks.
- Do not use synchronous `fs`, `crypto.randomBytes` (sync), or any blocking call in an async route handler.

## Common mistakes to avoid

| Mistake | Fix |
|---|---|
| JWT secret hardcoded in code | Load from `process.env`; validate its presence at startup. |
| Unhandled promise rejections crashing the process | Attach `process.on('unhandledRejection', ...)` and handle in async middleware. |
| Missing `await` on async middleware | `next()` fires before the async work finishes; always `await` or return the promise. |
| N+1 queries from ORMs | Use `include`/`join` or `DataLoader` pattern for batching. |
| Returning 200 on validation failure | Return 400 with structured error body; never 200 for errors. |
| Listening on port before DB is ready | Health-check the DB in startup; delay `listen()` or crash fast. |

## Output format

- New service: directory tree showing `module / controller / service / dto / entity` files.
- Route handler: TypeScript with typed request/response, validation pipe/schema, and error handling.
- Test file: Jest/Vitest describe block with happy path, validation failure, and auth failure cases.
- Config changes: diff of `tsconfig.json`, `package.json` scripts, environment variable list.

## Related checklists
- .claude/checklists/security.md
- .claude/checklists/performance.md
- .claude/checklists/qa.md

## Related agents
- .claude/agents/core/orchestrator.md
- .claude/agents/engineering/devops-engineer.md

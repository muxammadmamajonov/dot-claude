---
name: go-backend
description: >
  Activate when building, reviewing, or debugging Go backend services —
  standard-library HTTP, chi/Gin/Echo routers, goroutine/channel concurrency,
  database access with pgx/sqlc, testing, and production hardening. Use whenever
  the work touches Go server code, `go.mod`, `.go` files, goroutines/context, or
  keywords like "gin", "chi", "echo", "pgx" — even if the user never says "backend".
---

# Go Backend Development

## When to use
- Writing HTTP APIs, gRPC services, or CLI tools in Go
- Designing package boundaries, interfaces, and dependency injection
- Implementing concurrency with goroutines, channels, and context propagation
- Integrating databases via `pgx`, `sqlc`, or `database/sql`
- Writing table-driven tests and benchmarks
- Profiling CPU/memory with `pprof`

## Workflow

1. **Confirm Go version** — check `go.mod`. Prefer Go 1.21+ (range over func, `slog` logger, `slices`/`maps` stdlib packages).
2. **Establish package layout** before writing code:
   ```
   cmd/server/main.go          # binary entrypoints only
   internal/                   # private packages
     api/                      # HTTP handlers
     service/                  # business logic
     store/                    # data access layer
     domain/                   # pure types, no imports from above
   pkg/                        # reusable packages safe to import externally
   ```
3. **Define interfaces in the consumer package**, not the implementation package. The `store` package defines the `UserRepository` interface; the `postgres` package implements it.
4. **Inject dependencies through constructors** — `func NewUserService(repo UserRepository, log *slog.Logger) *UserService`. No global state.
5. **Propagate `context.Context` as the first argument** to every function that may block: DB calls, HTTP calls, goroutines with timeouts.
6. **Handle errors explicitly** — check every `err != nil`; wrap with `fmt.Errorf("doing X: %w", err)` to preserve the chain.
7. **Write the handler**: parse → validate → call service → serialise. Use `encoding/json` with `json.NewDecoder(r.Body).Decode(&req)` + a size-limited reader.
8. **Write tests**: table-driven with `t.Run`; use `httptest.NewRecorder` for handlers; use `testcontainers-go` for integration DB tests.
9. **Profile if needed**: `go tool pprof` on `/debug/pprof/` endpoints; `go test -bench -benchmem` for hot paths.
10. **Audit** against .claude/checklists/security.md and .claude/checklists/performance.md before deploying.

## Standards

### Error handling
- Never discard errors; `_ = f()` only for documented intentional ignores with a comment.
- Sentinel errors: `var ErrNotFound = errors.New("not found")`.
- Use `errors.Is` / `errors.As` for matching wrapped errors — not string comparison.
- Return descriptive errors from service layer; translate to HTTP status codes in the handler layer only.

### Concurrency
- Always pass context to goroutines so they can be cancelled.
- Use `sync.WaitGroup` or `errgroup.Group` (`golang.org/x/sync`) for fan-out; never fire-and-forget without tracking.
- Mutexes protect shared state; keep critical sections minimal. Prefer channels for ownership transfer.
- Data races are bugs: run `go test -race ./...` in CI.

### Database (`pgx` / `sqlc`)
- Use `pgxpool.Pool` for connection pooling — never `sql.Open` a new conn per request.
- Prefer `sqlc` to generate type-safe query functions from `.sql` files; avoid raw string queries with interpolated user input.
- Wrap multi-step writes in explicit transactions: `pool.BeginTx → defer tx.Rollback → ... → tx.Commit`.
- Set `pool.MaxConns` and query timeouts via context deadline.

### HTTP
- Use the standard `net/http` handler interface; choose a router (chi, Gin, Echo) for middleware chaining and path params.
- Always set `http.Server` timeouts: `ReadTimeout`, `WriteTimeout`, `IdleTimeout`.
- Validate all path/query/body inputs; return 400 before any business logic on bad input.
- Middleware order: logging → recovery → auth → rate-limit → handler.

### Do not
- Do not use `init()` for dependency setup — makes testing and startup order unpredictable.
- Do not use global `http.DefaultServeMux` in production services — create an explicit `http.ServeMux`.
- Do not ignore goroutine leaks — use `goleak` in tests.
- Do not use `interface{}` / `any` where a concrete type or generic can be used.
- Do not hard-code configuration — read from env vars at startup with validation.

## Common mistakes to avoid

| Mistake | Fix |
|---|---|
| Closing `http.Response.Body` before reading it fully | `io.Copy(io.Discard, resp.Body)` then `resp.Body.Close()`, or read fully first. |
| Range loop variable capture in goroutine | Copy the loop var: `v := v` before the goroutine (fixed in Go 1.22+). |
| Mutex copy (passed by value) | Always pass `sync.Mutex` / `sync.RWMutex` by pointer or embed in a struct. |
| Unbounded goroutine creation under load | Use a worker pool with a buffered channel or `semaphore.Weighted`. |
| JSON numbers decoded to `float64` by default | Use `json.Number` or decode into typed structs, not `map[string]interface{}`. |
| Missing `context.WithTimeout` on outbound calls | Every external call must have a deadline; absence causes goroutine leaks on slow deps. |

## Output format

- New package: directory tree + `package doc` comment + public interface definition.
- Handler: function signature, input struct, service call, and error-to-HTTP translation.
- Test file: `TestXxx(t *testing.T)` with table cases, subtests via `t.Run`, and assertion using `testify/assert`.
- Benchmark: `BenchmarkXxx(b *testing.B)` with `b.ResetTimer()` and `b.ReportAllocs()`.

## Related checklists
- .claude/checklists/security.md
- .claude/checklists/performance.md
- .claude/checklists/qa.md

## Related agents
- .claude/agents/core/orchestrator.md
- .claude/agents/engineering/devops-engineer.md

---
name: rust-backend
description: >
  Activate when building, reviewing, or debugging Rust backend services —
  Axum/Actix-web, async Tokio, error handling with thiserror/anyhow,
  SQLx/SeaORM, testing, and production hardening. Use whenever the work touches
  Rust server code, `Cargo.toml`, `.rs` handlers, async/await, or keywords like
  "axum", "actix", "tokio", "sqlx" — even if the user never says "backend".
---

# Rust Backend Development

## When to use
- Writing HTTP APIs or gRPC services with Axum, Actix-web, or Warp
- Designing ownership-safe data models and async service layers
- Implementing error types with `thiserror` and propagation with `anyhow`/`?`
- Integrating databases via `sqlx` (async, compile-time checked) or SeaORM
- Writing unit, integration, and property-based tests
- Profiling CPU/allocation with `perf`, `flamegraph`, or `criterion`

## Workflow

1. **Confirm Rust edition and MSRV** — check `Cargo.toml` (`edition = "2021"`, `rust-version`). Use stable toolchain unless a nightly feature is justified and documented.
2. **Establish crate/module layout**:
   ```
   src/
     main.rs           # binary entrypoint: init tracing, DB pool, router, server
     lib.rs            # re-exports for integration tests
     api/              # Axum handlers, extractors, middleware
     services/         # business logic (pure functions over domain types)
     db/               # sqlx queries, repository impls
     domain/           # types, enums, value objects (no I/O)
     errors.rs         # AppError enum + IntoResponse impl
     config.rs         # typed config from env vars
   ```
3. **Define domain types and the `AppError` enum first** — they drive everything else.
   ```rust
   #[derive(Debug, thiserror::Error)]
   pub enum AppError {
       #[error("not found")] NotFound,
       #[error("db: {0}")] Db(#[from] sqlx::Error),
   }
   ```
4. **Set up the `AppState`** — `#[derive(Clone)]` struct holding `PgPool`, config, and shared clients. Pass via `axum::Extension` or state extractor.
5. **Write handlers** — thin: extract → call service → return `impl IntoResponse`. Validation via `validator` crate + custom extractor.
6. **Async runtime** — `#[tokio::main]` with `tokio::runtime::Builder` for production (configure worker threads). Never `block_on` inside async code.
7. **Database queries with `sqlx`**:
   - Use `sqlx::query_as!` macros — compile-time checked against a live DB (`DATABASE_URL` in `.env`).
   - All multi-step writes in explicit `pool.begin()` transactions.
   - Set `connect_options.statement_cache_capacity` and pool max connections.
8. **Write tests**:
   - Unit: pure functions, no I/O, in `#[cfg(test)]` modules within the same file.
   - Integration: `tokio::test`, real DB via `sqlx::test` attribute (creates an isolated DB per test).
   - Use `axum::body::to_bytes` + `serde_json` to assert handler responses.
9. **Benchmark hot paths** with `criterion`; run `cargo flamegraph` to visualise.
10. **Audit** against .claude/checklists/security.md and .claude/checklists/performance.md.

## Standards

### Ownership and types
- Prefer `&str` over `String` in function parameters where the callee doesn't need ownership.
- Use `Arc<T>` for shared state across async tasks; `Mutex<T>` only inside synchronous critical sections — prefer `tokio::sync::Mutex` in async contexts.
- Newtype pattern for domain IDs: `struct UserId(Uuid)` prevents accidental ID mixups.
- Derive `Debug`, `Clone`, `PartialEq` for domain types; derive `Serialize`/`Deserialize` only at API boundary structs.

### Error handling
- Define one `AppError` enum per crate/service with `thiserror`.
- Use `?` for propagation; never `.unwrap()` or `.expect()` in production code paths.
- Implement `axum::response::IntoResponse` for `AppError` to map to HTTP status + JSON body.
- Log errors at the point of origin; propagate the type, not a string.

### Async / Tokio
- CPU-bound work: `tokio::task::spawn_blocking` or `rayon` threadpool — never block in an async context.
- Set timeouts with `tokio::time::timeout` on every external call.
- Structured concurrency: `tokio::select!`, `JoinSet`, or `FuturesUnordered` over bare `tokio::spawn` when you need to collect results.

### Security
- Validate all input with the `validator` crate and reject early with 422.
- Hash passwords with `argon2` (use `argon2` crate, not raw `bcrypt`).
- Use `secrecy::Secret<String>` for tokens and passwords to prevent accidental `Debug` leakage.
- Set `Content-Security-Policy`, `X-Frame-Options`, and security headers via `tower-http::set-header`.

### Do not
- Do not use `unsafe` without a `SAFETY:` comment block explaining the invariants upheld.
- Do not panic in library code (`panic!`, `unwrap`, `expect`) — return a `Result` instead.
- Do not use `.clone()` reflexively to satisfy the borrow checker — restructure first.
- Do not place `#[allow(unused_*)]` globally; fix the warnings instead.

## Common mistakes to avoid

| Mistake | Fix |
|---|---|
| `async fn` that holds a non-`Send` type across `.await` | Restructure to drop the non-Send value before the await point. |
| `sqlx::query!` failing at runtime due to missing `DATABASE_URL` at compile time | Set `DATABASE_URL` in `.env` and run `cargo sqlx prepare` to embed offline metadata. |
| Cloning `PgPool` repeatedly into handlers | `PgPool` is already `Clone + Send + Sync` cheaply (Arc-backed); clone freely. |
| Shadowing outer error types with `anyhow::Error` | Use `thiserror` for typed errors in libraries; `anyhow` only in binaries/tests. |
| `Mutex<Vec<T>>` contention under load | Use `DashMap` or channel-based message passing for concurrent collections. |
| Missing `tower::ServiceBuilder` middleware order | Middleware applies inside-out; put logging outermost, auth innermost. |

## Output format

- New handler: `async fn` with typed extractors, service call, and `AppError` propagation.
- Error enum: `thiserror` enum with `#[from]` conversions and `IntoResponse` impl.
- `Cargo.toml` additions: feature-flagged dependencies with version pinning.
- Test: `#[sqlx::test]` annotated async function with setup, action, and assertion.

## Related checklists
- .claude/checklists/security.md
- .claude/checklists/performance.md
- .claude/checklists/qa.md

## Related agents
- .claude/agents/core/orchestrator.md
- .claude/agents/engineering/devops-engineer.md

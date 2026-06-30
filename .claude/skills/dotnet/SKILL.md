---
name: dotnet
description: >
  Activate when building, reviewing, or debugging .NET 8+ / ASP.NET Core services
  or applications — minimal APIs, MVC, EF Core, DI, middleware pipeline, options
  pattern, health checks, AOT compilation, and testing. Use whenever the work
  touches C#/.NET code, `.csproj`/`.sln`, `Program.cs`, controllers/EF entities,
  or keywords like "asp.net", "ef core", "blazor", "c#" — even if the user just
  says ".NET".
---

# .NET / ASP.NET Core Development

## When to use
- Scaffolding or extending ASP.NET Core services (REST APIs, gRPC, Blazor, background workers)
- Designing the middleware pipeline, filters, or DI container in .NET 8+
- Mapping domain objects to the database via Entity Framework Core 8+
- Implementing authentication (JWT Bearer, cookie, OIDC) with ASP.NET Core Identity or custom schemes
- Adding health checks, OpenTelemetry, and structured logging with `ILogger`
- Optimising startup performance with NativeAOT or `PublishReadyToRun`
- Writing tests: xUnit, integration tests with `WebApplicationFactory`, Testcontainers

## Workflow

1. **Scaffold** with `dotnet new` templates — `webapi` (minimal API, .NET 8 default), `mvc`, `worker`, `grpc`. Use `--use-minimal-apis` flag for new REST services; MVC is preferred for apps with many controllers or complex filters.
2. **Choose the project structure**:
   ```
   src/
     MyApp.Api/         ← Entry point, middleware, endpoint definitions
     MyApp.Application/ ← Use cases, commands/queries (CQRS with MediatR optional)
     MyApp.Domain/      ← Entities, value objects, domain events
     MyApp.Infrastructure/ ← EF Core DbContext, migrations, external clients
   tests/
     MyApp.UnitTests/
     MyApp.IntegrationTests/
   ```
3. **Register services at startup** in `Program.cs` using `builder.Services.Add*`. Group registrations by feature using extension methods (`services.AddOrderingFeature()`). Never scatter `AddSingleton` across the codebase.
4. **Define the data contracts** with C# records (immutable DTOs). Add data annotations or FluentValidation rules. Use `IValidator<T>` from FluentValidation for complex rules; never validate in controllers.
5. **Map the data model** with EF Core code-first. Configure via `IEntityTypeConfiguration<T>` — do not use data annotation attributes on domain entities. Migrations: `dotnet ef migrations add`, never `EnsureCreated` in production.
6. **Secure the application**:
   - JWT Bearer: register `AddAuthentication().AddJwtBearer(...)` and validate `Issuer`, `Audience`, `SigningKey` from options.
   - Use `[Authorize]` attribute or `RequireAuthorization()` on minimal API groups.
   - ASP.NET Core Identity for user management; use `UserManager<TUser>` — never raw SQL for password operations.
   - CORS: explicit allowlist via `builder.Services.AddCors(options => options.AddPolicy(...))` — never `AllowAnyOrigin` in production.
7. **Add health checks**: `builder.Services.AddHealthChecks()` with database, upstream HTTP, and queue checks. Expose `/health/ready` and `/health/live` separately for Kubernetes probes.
8. **Structured logging**: use `ILogger<T>` (injected); configure Serilog or `Microsoft.Extensions.Logging` with JSON sink for production. Never `Console.WriteLine` or `Debug.WriteLine` in production code.
9. **Enable OpenTelemetry** via `OpenTelemetry.Extensions.Hosting` — traces, metrics, and logs to OTLP endpoint. Use `ActivitySource` for custom spans.
10. **Native AOT considerations** (if publishing AOT): avoid reflection, dynamic code gen, `XmlSerializer`, `BinaryFormatter`. Use source generators (`System.Text.Json` source gen). Run `dotnet publish -r linux-x64 -p:PublishAot=true` to validate early.
11. **Write tests**:
    - Unit: xUnit with `FluentAssertions`; mock with `NSubstitute` or `Moq`.
    - Integration: `WebApplicationFactory<Program>` with in-memory or Testcontainers Postgres for EF Core.
    - Avoid `[InlineData]` for complex inputs — use `[MemberData]` or `[ClassData]` with typed inputs.
12. **Audit** against `.claude/checklists/security.md` and `.claude/checklists/production.md`.

## Standards

### Dependency Injection
- Only constructor injection. No `ServiceLocator`, no static `IServiceProvider` access.
- Lifetime mismatches are bugs: never inject `Scoped` into `Singleton`. Use `IServiceScopeFactory` in background services to create a scope per work item.
- Register options with `builder.Services.Configure<MyOptions>(config.GetSection("MyOptions"))` and inject `IOptions<T>` (singleton) or `IOptionsSnapshot<T>` (per-request) — never `IConfiguration` directly in business logic.
- Validate options at startup: call `.ValidateDataAnnotations().ValidateOnStart()` after `Configure<T>`.

### EF Core
- `AsNoTracking()` on all read-only queries — significant performance gain for query-heavy endpoints.
- Never `Include()` navigation properties speculatively; load only what the use case needs.
- For bulk operations use `ExecuteUpdateAsync()` / `ExecuteDeleteAsync()` (EF Core 7+) — avoids loading entities into memory.
- Migrations are immutable once applied to a shared environment — never edit, always add a new migration.
- `DbContext` is `Scoped` — never inject it into a `Singleton` service.
- Connection resiliency: `options.EnableRetryOnFailure()` for SQL Server / `Npgsql.EnableRetryOnFailure()` for PostgreSQL.

### Minimal APIs vs MVC
- Minimal APIs: prefer for microservices, small surface areas, AOT targets, or when OpenAPI customisation is via extension methods.
- MVC controllers: prefer for large APIs with many filters, complex model binding, or existing teams with MVC conventions.
- Do not mix both in the same project without a clear boundary.

### Error handling
- Register `app.UseExceptionHandler("/error")` or `IProblemDetailsService` (`AddProblemDetails()`) for RFC 7807 responses.
- Return `TypedResults.Problem(...)` from minimal API endpoints — not raw `500` strings.
- Never return stack traces to clients; log them with correlation IDs.

### Security
- Enable `UseHttpsRedirection` and `UseHsts` for browser-facing apps.
- `AntiForgery` middleware for Blazor/MVC apps that use cookies.
- Secrets via `dotnet user-secrets` (local dev) and environment variables / Azure Key Vault / AWS Secrets Manager (all other environments) — never in `appsettings.json` committed to VCS.
- `Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options` headers via middleware or `NWebsec`.

### Do not
- Do not use `HttpContext.Request.Form` without `[FromForm]` and anti-forgery validation in MVC.
- Do not suppress nullable warnings with `!` (null-forgiving operator) in production code; fix the nullability.
- Do not block on `.Result` or `.Wait()` in async code — always `await`.
- Do not use `EnsureCreated()` or `migrate: true` in production startup code.
- Do not `new DbContext(options)` manually — always inject from DI.

## Common mistakes to avoid

| Mistake | Fix |
|---|---|
| `DbContext` disposed before async result materialised | Always `await` EF Core queries; never return `IQueryable<T>` from repository methods |
| Scoped service in a hosted background `IHostedService` | Use `IServiceScopeFactory.CreateScope()` per work iteration |
| Missing `CancellationToken` propagation | Accept and pass `CancellationToken` from controller action to service and down to EF Core / HttpClient calls |
| `appsettings.json` with real secrets | Use `dotnet user-secrets add` locally; env vars in CI/prod |
| Integration tests sharing `WebApplicationFactory` across test classes | Use `IClassFixture<WebApplicationFactory<Program>>` for sharing; reset DB state per test class |
| N+1 from lazy navigation loading (disabled in EF Core by default) | Use `Include` / `ThenInclude` or split queries (`AsSplitQuery()`) for collection includes |
| AOT failure at publish time | Run `dotnet publish -p:PublishAot=true` in CI; fix trim/reflection warnings before they accumulate |

## Output format

- New service: `Program.cs` with middleware pipeline, `appsettings.json` skeleton, and dependency registration extension methods.
- Entity + migration: `IEntityTypeConfiguration<T>` class and corresponding `dotnet ef migrations` SQL preview.
- Test class: xUnit with `WebApplicationFactory`, FluentAssertions assertions, and Testcontainers setup.
- Options class: `record MyOptions` with data annotations and startup validation.

Output artifacts go to `docs/specs/` for design decisions; code files alongside source.

## Related checklists
- .claude/checklists/security.md
- .claude/checklists/performance.md
- .claude/checklists/qa.md
- .claude/checklists/production.md

## Related agents
- .claude/agents/core/solution-architect.md
- .claude/agents/engineering/backend-engineer.md
- .claude/agents/engineering/database-architect.md
- .claude/agents/quality/security-auditor.md

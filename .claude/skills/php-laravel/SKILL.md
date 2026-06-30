---
name: php-laravel
description: >
  Activate when building, reviewing, or debugging PHP applications with Laravel 11+ —
  Eloquent ORM, queues, migrations, Form Request validation, Sanctum/Passport auth,
  Laravel Octane, and PHPUnit / Pest testing. Use whenever the work touches PHP/Laravel
  code, `composer.json`, `artisan`, Blade/controllers/Eloquent models, or keywords like
  "laravel", "eloquent", "artisan", "sanctum" — even if the user just says "PHP".
---

# PHP + Laravel Development

## When to use
- Scaffolding or extending a Laravel 11+ application (REST API, web app, background jobs)
- Designing Eloquent models, relationships, and query scopes
- Writing database migrations and managing schema changes
- Implementing API authentication with Laravel Sanctum (SPA / mobile tokens) or Passport (OAuth2)
- Setting up queued jobs, listeners, and scheduled commands
- Optimising with Laravel Octane (Swoole/RoadRunner) for high-throughput scenarios
- Testing with PHPUnit or Pest, factories, and feature/unit split

## Workflow

1. **Scaffold** with `composer create-project laravel/laravel my-app` or the Laravel Installer (`laravel new my-app`). For APIs set `APP_URL`, disable unnecessary middleware (`web` group if API-only).
2. **Structure the application**:
   ```
   app/
     Http/
       Controllers/   ← Thin, delegate to services/actions
       Requests/      ← FormRequest validation classes
       Resources/     ← API resources (JSON transformers)
     Actions/         ← Single-responsibility action classes
     Models/          ← Eloquent models
     Services/        ← Business logic
   database/
     migrations/
     factories/
     seeders/
   ```
   Keep controllers thin: accept `FormRequest`, call one `Action` or `Service`, return an `ApiResource`.
3. **Define the data model** — see `.claude/skills/data-modeling/SKILL.md`. Create migrations with `php artisan make:migration`; never hand-edit existing migrations that have run on shared environments.
4. **Validate at the boundary** using `FormRequest` classes (`php artisan make:request`). The `authorize()` method checks policy/gate; `rules()` returns the validation array. Never validate in controllers with `$request->validate(...)` for complex rules.
5. **Write Eloquent models carefully**:
   - Always define `$fillable` (or `$guarded = []` with caution) — never leave both empty.
   - Define relationship methods (`hasMany`, `belongsTo`, `belongsToMany`) and use `with()` in the query to eager-load, avoiding N+1.
   - Use local query scopes (`scopeActive($q)`) to keep query logic in the model, not in controllers.
   - Use Model Observers for side-effects on lifecycle events (`created`, `updated`, `deleted`).
6. **Authenticate and authorise**:
   - Sanctum for SPAs (cookie-based) and mobile/CLI (token-based): `sanctum` middleware, `$user->createToken(...)`.
   - Passport for full OAuth2 (third-party clients needing authorization code flow).
   - Gates and Policies (`php artisan make:policy`) for resource-level authorisation; call `$this->authorize('update', $post)` in controllers.
7. **Queue jobs** for anything taking >200ms or that can fail and retry: `php artisan make:job`. Use `ShouldQueue`, set `$tries`, `$timeout`, and `$backoff`. Use `ShouldBeUnique` for idempotent jobs. Run workers with Supervisor; use Redis queue driver in production.
8. **Schedule commands** in `routes/console.php` (Laravel 11) or `app/Console/Kernel.php` (≤10) with `$schedule->command(...)->dailyAt(...)`. Avoid cron jobs that duplicate scheduler logic.
9. **Optimise for production**:
   - `php artisan config:cache && route:cache && view:cache && event:cache` in deploy step.
   - Octane (if needed): `php artisan octane:start --server=swoole`. Be aware of state leakage in singletons across requests — reset state in `octane:request` lifecycle hook.
10. **Write tests** with PHPUnit or Pest:
    - Unit tests: plain PHP, no Laravel bootstrap, for domain/service logic.
    - Feature tests: `RefreshDatabase` trait, real HTTP through `$this->getJson('/api/...')`, factories for data setup.
    - Always seed with model factories (`php artisan make:factory`); never hard-code test data as raw SQL.
11. **Audit** against `.claude/checklists/security.md` and `.claude/checklists/production.md`.

## Standards

### Eloquent
- Always use `$fillable` — never trust `$guarded = []` unless you have a comprehensive test suite and intentional policy.
- Avoid `DB::statement()` for DML in application logic — use Eloquent or the Query Builder with parameter binding.
- Chunking for large datasets: `Model::chunk(500, fn ($rows) => ...)` or `lazy()` cursor — never `->get()` a full table.
- Soft deletes (`SoftDeletes` trait): remember to add `->withTrashed()` when querying across deletion states.
- Use database transactions for multi-step writes: `DB::transaction(function () { ... })` or `DB::beginTransaction()` / `commit()` / `rollBack()`.

### Migrations
- Migrations are immutable once run on a shared/production environment — add new migrations, never edit old ones.
- Add indexes in the same migration as the column: `$table->index('user_id')` or `$table->foreign('user_id')->references('id')->on('users')->onDelete('cascade')`.
- For large tables, add indexes separately with raw `CREATE INDEX CONCURRENTLY` (PostgreSQL) or use `Schema::table()` in a separate migration with a note about the lock risk on MySQL.
- Always write `down()` methods that truly reverse `up()` — do not leave them empty.

### Queues
- Set `$timeout` slightly less than the `--timeout` flag on the worker to allow clean shutdown.
- Use `$this->fail($exception)` in `failed()` method to mark the job as failed with context.
- Dispatch to named queues (`->onQueue('high')`) and run separate worker pools per queue priority.
- For idempotency, check preconditions at the start of `handle()` and bail early if the work is already done.

### Security defaults
- `csrf` middleware is on by default for `web` routes — never remove it for browser sessions.
- For APIs using Sanctum tokens, ensure `stateful` domains list is tight (not `*`).
- Rate limiting: use `RateLimiter::for(...)` in `RouteServiceProvider` / routes — never rely on a reverse proxy alone.
- File uploads: validate MIME type with `mimes:pdf,jpg` and size; store in non-publicly-accessible disk with `Storage::disk('s3')->put(...)` or local private disk. Never `public_path()` for user uploads.
- Mass assignment: `$fillable` on every model — verify in code review.
- SQL injection: always use Query Builder bindings or Eloquent — never string-concatenate into `DB::raw()`.

### Do not
- Do not return Eloquent model instances directly from API controllers — always use `JsonResource` or `ResourceCollection`.
- Do not use `Request::all()` as a mass-assignment input without filtering through `FormRequest`.
- Do not share state between requests in Octane workers (class-level static variables, non-resettable singletons).
- Do not run `composer install` in production without `--no-dev --optimize-autoloader`.
- Do not use `env()` outside of config files — call `config('app.key')` in application code so config caching works.

## Common mistakes to avoid

| Mistake | Fix |
|---|---|
| N+1 queries from missing `with()` | Use `with('relation')` in the controller query; detect with `barryvdh/laravel-debugbar` or Telescope |
| `env()` call inside business logic with config caching active | Move to a `config/` file, reference via `config('key')` |
| Missing `failed()` method on queued jobs | Implement `failed(Throwable $e)` to clean up or notify; log the error with context |
| Unguarded mass assignment via `Model::create($request->all())` | Use `$request->validated()` from `FormRequest` |
| Route model binding with soft-deleted records not found | Add `->withTrashed()` on the binding or define `resolveRouteBindingQuery` |
| Tests not resetting database state | Use `RefreshDatabase` (transactions, fast) or `DatabaseMigrations` (slower, needed for tests that check FK behaviour) |
| Octane state leak between requests | Bind singletons with `$this->app->scoped(...)` and reset in `RequestHandled` event |

## Output format

- New API endpoint: `FormRequest` class, slim controller method, `JsonResource` class.
- Eloquent model: model class with `$fillable`, relationships, and scopes; corresponding migration.
- Queue job: job class with `handle()`, `failed()`, retry config, and feature test.
- Policy: `Policy` class registered in `AuthServiceProvider`; `@can` or `$this->authorize()` usage.

Output artifacts go to `docs/specs/` for design decisions; code in `app/` tree.

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

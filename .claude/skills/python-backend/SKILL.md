---
name: python-backend
description: >
  Activate when building, reviewing, or debugging Python backend services using
  FastAPI, Django (DRF), or Flask — async patterns, Pydantic models, ORM usage,
  auth, testing, and production readiness. Use whenever the work touches Python
  server code, `requirements.txt`/`pyproject.toml`, route handlers/views, or
  keywords like "fastapi", "django", "flask", "pydantic" — even if the user
  never says "backend".
---

# Python Backend Development

## When to use
- Writing REST or GraphQL APIs with FastAPI, Django REST Framework, or Flask
- Designing Pydantic models, serialisers, or schema validation
- Implementing authentication (OAuth2, JWT, session) or permission layers
- Integrating SQLAlchemy, Django ORM, or raw psycopg queries
- Writing tests with pytest (sync and async)
- Profiling and fixing slow endpoints or memory growth

## Workflow

1. **Classify** — sync Django/DRF vs async FastAPI, type of data access, auth model.
2. **Set up the environment**:
   - Python 3.11+ with `pyproject.toml` (PEP 517/518).
   - Dependency manager: `uv` (fast) or `poetry`. Avoid bare `pip install` in CI.
   - Virtual env: always isolated — never install into system Python.
3. **Scaffold**:
   - FastAPI: `app = FastAPI()` in `main.py`; split into `routers/`, `models/`, `schemas/`, `deps/`, `core/`.
   - Django: `django-admin startproject`; apps map to bounded contexts.
4. **Define Pydantic schemas (FastAPI) or serialisers (DRF) before handlers** — they document and enforce the contract.
5. **Implement business logic in service functions**, not in view/route handlers. Handlers parse → call service → serialise response.
6. **Database access**:
   - FastAPI + SQLAlchemy async: use `AsyncSession` with `async with session.begin()`.
   - Django ORM: `select_related` / `prefetch_related` to prevent N+1; use `transaction.atomic` for multi-step writes.
7. **Auth**: FastAPI uses `Depends(get_current_user)`; DRF uses `permission_classes`. Validate JWT with `python-jose` or `authlib`; never decode without signature verification.
8. **Error handling**: FastAPI `HTTPException`; DRF `ValidationError` / `APIException`; Flask `@app.errorhandler`. Always return structured JSON errors.
9. **Test**: `pytest` + `httpx.AsyncClient` for FastAPI; Django `TestClient`; use `pytest-anyio` for async tests. Cover happy path, 422/400 validation, and auth failure.
10. **Harden**: CORS allowlist, rate limiting (`slowapi` / Django Ratelimit), request size limits, SQL injection prevention via ORM/parameterised queries.
11. **Audit** against .claude/checklists/security.md and .claude/checklists/performance.md before deploying.

## Standards

### Type safety
- Use Python 3.10+ type hints everywhere: `def get_user(user_id: int) -> UserSchema:`.
- Run `mypy --strict` or `pyright` in CI.
- Pydantic v2 (`model_config = ConfigDict(strict=True)`) for FastAPI schemas.

### FastAPI specifics
- All path/query/body parameters must be typed; Pydantic validates automatically.
- Use `Depends()` for DB sessions, auth, pagination — not global variables.
- Background tasks (`BackgroundTasks` or Celery) for anything not in the critical path.
- Mount routers with prefix and tags: `app.include_router(users.router, prefix="/users", tags=["users"])`.

### Django/DRF specifics
- Use `get_object_or_404` not bare `Model.objects.get` — prevents 500 on missing records.
- ViewSets for CRUD resources; `APIView` for custom endpoints.
- `settings.py` split: `base.py`, `local.py`, `production.py`; use `django-environ` for env vars.
- Never use `DEBUG=True` in production; `ALLOWED_HOSTS` must be explicit.

### Database (SQLAlchemy)
- Always use parameterised queries — never `f"SELECT ... WHERE id={user_id}"`.
- Define models with explicit `__tablename__`, column types, and constraints.
- Async sessions must be closed; use context managers or `async_scoped_session`.
- Alembic for migrations; check migration against production schema in CI.

### Do not
- Do not use mutable default arguments (`def f(items=[])`).
- Do not catch bare `Exception` without re-raising or logging with full traceback.
- Do not use `pickle` for untrusted data deserialization.
- Do not import at module level what belongs behind a function scope (avoids circular imports and slow startup).
- Do not store secrets in `settings.py`; load from environment and validate at startup.

## Common mistakes to avoid

| Mistake | Fix |
|---|---|
| Blocking I/O in an async FastAPI handler | Use `await asyncio.to_thread(sync_fn)` or an async library. |
| SQLAlchemy lazy load outside session scope | Either `expire_on_commit=False`, eager-load, or keep the session open. |
| Django ORM queries in serialiser `to_representation` | Move queries to the view with `select_related`; serialisers must be query-free. |
| Returning Python exceptions as 500 with stack trace | Catch in error handler; return `{"detail": "..."}` with appropriate status. |
| Tests hitting the production database | Use `pytest-django`'s `@pytest.mark.django_db` with a test DB, or SQLite in-memory. |
| Circular import in FastAPI `Depends` chain | Restructure deps into a `deps.py` module imported by both sides. |

## Output format

- New endpoint: route function + Pydantic schema + service function, all typed.
- Module layout: directory tree showing `routers/`, `schemas/`, `services/`, `models/`, `tests/`.
- Test file: `pytest` functions covering success, 422 validation error, and 401 auth failure.
- Migration: Alembic `upgrade`/`downgrade` functions with comments on intent.

## Related checklists
- .claude/checklists/security.md
- .claude/checklists/performance.md
- .claude/checklists/qa.md

## Related agents
- .claude/agents/core/orchestrator.md
- .claude/agents/engineering/devops-engineer.md

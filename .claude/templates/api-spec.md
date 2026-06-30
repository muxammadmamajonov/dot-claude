# API Specification

> **What this is:** the contract for the system's interface — endpoints/operations, schemas, errors, auth, and versioning. Filled in by the **api-architect** agent after the data model. Stable contracts protect clients; breaking changes follow the versioning policy. Reviewed against the [api checklist](../checklists/api.md).

---

## 1. Overview & style
> What kind of interface, and why (reference the decision record).

- **Style:** `<REST | GraphQL | gRPC | events | SDK>` · **Base URL:** `<https://api.example.com>`
- **Format:** `<JSON>` · **Spec source of truth:** `<OpenAPI / GraphQL SDL / proto file>`

## 2. Conventions
> Cross-cutting rules every endpoint follows. Consistency here prevents a thousand small bugs.

- **Auth:** `<Bearer JWT / API key>`; scopes/roles per [user-roles-permissions.md](user-roles-permissions.md).
- **Versioning:** `<URL /v1 | header>`; breaking changes → new version, old supported `<N months>`.
- **Pagination:** `<cursor-based: ?limit=&cursor=>`; responses include `next_cursor`.
- **Errors:** standard envelope `{ "error": { "code": "<MACHINE_CODE>", "message": "<human>", "details": [] } }`.
- **Idempotency:** mutating POSTs accept `Idempotency-Key` header.
- **Rate limits:** `<headers: X-RateLimit-Remaining; 429 on exceed>`.

## 3. Resources & operations
> One row per operation. Keep names consistent (nouns for REST resources).

| Method/Op | Path / name | Auth (scope) | Description |
|-----------|-------------|--------------|-------------|
| GET | `/v1/resources` | `resource:read` | List resources (paginated) |
| POST | `/v1/resources` | `resource:create` | Create a resource (idempotent) |
| GET | `/v1/resources/{id}` | `resource:read` | Fetch one |
| PATCH | `/v1/resources/{id}` | `resource:update` | Partial update |
| DELETE | `/v1/resources/{id}` | `resource:delete` | Soft-delete |

## 4. Endpoint detail (repeat per non-trivial operation)
### `POST /v1/resources`
> Request body, response, status codes, side effects.

- **Request:**
```json
{ "name": "<string, required>", "tags": ["<string>"] }
```
- **Success `201`:**
```json
{ "id": "<uuid>", "name": "<string>", "created_at": "<iso8601>" }
```
- **Errors:** `400 VALIDATION_ERROR`, `401 UNAUTHENTICATED`, `403 FORBIDDEN`, `409 CONFLICT`, `429 RATE_LIMITED`.

## 5. Schemas / models
> Shared object definitions referenced above. Mark required vs optional and types.

> `Resource { id: uuid, name: string(1..120), tags: string[], created_at: datetime, updated_at: datetime }`

## 6. Error catalog
> Every machine code, its HTTP status, and meaning. Clients branch on `code`, not message text.

| Code | HTTP | Meaning |
|------|------|---------|
| `VALIDATION_ERROR` | 400 | `<input failed validation>` |
| `FORBIDDEN` | 403 | `<authenticated but not permitted>` |
| `CONFLICT` | 409 | `<duplicate / state conflict>` |

## 7. Webhooks / events (if any)
> Outbound events: name, payload, delivery guarantees, signature verification, retry.

- `<resource.created>` → `<payload>`; signed with `<HMAC header>`; retried `<with backoff, at-least-once>`.

## 8. Versioning & deprecation policy
> How clients are protected from breaking changes.

> `<Additive changes are non-breaking. Breaking changes ship under a new version; deprecated versions get a sunset header and N-month notice.>`

## 9. Open questions
- [ ] `<contract question, e.g. "GraphQL or REST for the mobile client?">`

---
**Done when:** every operation lists auth + request/response + error codes, the error catalog is complete, pagination/idempotency/rate-limits are defined once and applied everywhere, and the versioning policy is explicit. Review with the [api checklist](../checklists/api.md).

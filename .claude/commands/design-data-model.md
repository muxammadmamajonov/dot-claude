---
description: Design entities, relationships, indexes, migration strategy, and data lifecycle/retention
argument-hint: [optional entity or domain to focus on, e.g. "billing" or "user"]
---

# /design-data-model

## Purpose
Translate the product spec, business rules, and architecture into a concrete data model: entities with typed fields, relationships with cardinality and constraints, indexes for the access patterns identified in feature specs, a safe migration strategy, and a data lifecycle and retention policy. Produces an ERD and a canonical reference that build agents use to generate schema files.

## When to use
- As Phase 6 of `/start-project`, after the architecture is approved.
- Standalone when adding a new domain or entity to an existing project.
- When the database choice changes and the model must be adapted (e.g., relational → document).

## Workflow

### Step 1 — Load inputs
1. Read `docs/architecture/overview.md` — components, trust boundaries, data sensitivity classifications.
2. Read `docs/specs/business-rules.md` — validation, state machine, retention, and compliance rules.
3. Read `docs/specs/roles-permissions.md` — which roles own or access which entities.
4. Read all files in `docs/specs/feature-specs/` — CRUD summary per feature gives access patterns.
5. Read `docs/decisions/stack.md` — primary database type (relational, document, time-series, graph, ledger) and any secondary stores (cache, search index, blob storage).
6. Read `docs/state/project-type.md` — check for compliance cross-cutting concerns (GDPR, HIPAA, PCI).

### Step 2 — Extract entities from specs
7. Go through every feature spec's "Data touched" section and collect all named entities. Deduplicate. For each entity, note:
   - The features that create, read, update, or delete it.
   - The user roles that access it (from roles-permissions.md).
   - Any business rules that constrain its fields or state.

8. Classify each entity:
   - **Core** — must exist for any feature to function.
   - **Supporting** — exists to enrich or relate core entities.
   - **Audit / log** — append-only records for compliance or debugging.
   - **Cache / projection** — derived from other entities; can be rebuilt.

### Step 3 — Define entities and fields
9. For each entity, write a definition block in `docs/architecture/data-model.md`:

   ```
   ### <EntityName>

   | Field | Type | Nullable | Default | Constraints | Notes |
   |-------|------|----------|---------|-------------|-------|
   | id    | UUID / BIGINT | No | generated | PK | Use UUID for public-facing IDs; BIGINT for internal FKs |
   | ...   | ...  | ...      | ...     | ...         | ...   |
   | created_at | TIMESTAMPTZ | No | now() | | |
   | updated_at | TIMESTAMPTZ | No | now() | | Trigger-maintained |

   **Indexes:** <list: field(s), type (B-tree/GIN/GiST/hash), covering fields, purpose>
   **Business rules:** <list of BR-nnn that apply>
   **Access roles:** <list from roles-permissions.md>
   **Sensitivity:** Public / Internal / Confidential / Restricted (PII / PHI / PCI)
   ```

   Field typing conventions:
   - Monetary amounts: `BIGINT` (store in smallest currency unit, e.g. cents) for relational; `Decimal128` for document stores. Never `FLOAT`.
   - Passwords: never stored — store `password_hash TEXT` (bcrypt/Argon2 output).
   - PII fields (email, phone, name): mark sensitivity; if GDPR applies, note that these fields are subject to erasure.
   - Enums: prefer DB-level enum or constrained `VARCHAR` with a `CHECK` constraint; list all valid values.
   - JSON/JSONB columns: only for genuinely variable structure — document the expected shape in the Notes column.

### Step 4 — Define relationships
10. List every relationship between entities with:
    - **Type** — one-to-one, one-to-many, many-to-many.
    - **FK placement** — which table holds the foreign key.
    - **Cascade behaviour** — ON DELETE (CASCADE / RESTRICT / SET NULL / SET DEFAULT).
    - **Nullability** — is the FK nullable (optional relationship)?
    - **Join table** (for many-to-many) — name and fields.

    Relationship rules:
    - Every FK must have an index unless the selectivity is provably too low to be useful.
    - Soft-delete entities must use `deleted_at TIMESTAMPTZ NULL` rather than physical deletes where referential integrity would break cascades.
    - Entities that span trust boundaries (e.g., tenant isolation) must have a `tenant_id` column indexed and included in all row-level security policies.

### Step 5 — Draw ERD
11. Write a Mermaid `erDiagram` block in the data-model file. Show:
    - All Core and Supporting entities.
    - Relationships with cardinality notation (`||--o{`, `}o--||`, etc.).
    - FK fields labelled on the relationship line.
    - Audit/log and Cache/projection entities in a secondary diagram block to keep the primary ERD readable.

### Step 6 — Define access patterns and index strategy
12. From feature specs, extract every query pattern that will run in production. For each pattern:

    | Feature | Query description | Table(s) | Filter fields | Sort field | Index recommendation |
    |---------|-----------------|---------|--------------|-----------|---------------------|
    | FEAT-001 | List orders by user, newest first | orders | user_id | created_at DESC | `(user_id, created_at DESC)` |
    | ...      | ...             | ...     | ...          | ...       | ...                 |

13. Flag any query that:
    - Requires a full-table scan on a table expected to exceed 100k rows — must have an index.
    - Requires a cross-entity join of more than 4 tables — consider a materialised view or read model.
    - Returns an unbounded result set — must have pagination enforced by business rule.

### Step 7 — Compliance and sensitivity handling
14. For each sensitivity level, document the required treatment:
    - **Restricted (PII/PHI)** — fields that must be encrypted at the column level or application level; key management component reference from architecture.
    - **PCI** — card data fields that must never be stored; tokenisation pattern; which third-party vault holds them.
    - **GDPR** — erasure procedure per entity; pseudonymisation fields; data export procedure.
    - **HIPAA** — audit log requirements for all PHI access; minimum-necessary access pattern.
    - **Audit logs** — append-only table structure: `(id, entity_type, entity_id, action, actor_id, actor_role, ip_address, changed_fields JSONB, created_at)`.

### Step 8 — Migration strategy
15. Write the migration strategy section:
    - **Tool** — migration tool from the stack (e.g., Alembic, Flyway, Prisma Migrate, golang-migrate, Liquibase, Rails ActiveRecord, Knex).
    - **Naming convention** — `<timestamp>_<description>.sql` or framework equivalent.
    - **Branching model** — how migrations are managed across feature branches (linear only vs. branch-aware).
    - **Zero-downtime rules** — mandatory patterns for production migrations:
      1. Never rename a column directly — add new, backfill, switch reads, remove old (multi-deploy).
      2. Never add a NOT NULL column without a default or a two-phase migration.
      3. Never drop a column in the same deploy that removes the code reading it.
      4. Index creation on large tables must use `CREATE INDEX CONCURRENTLY` (or DB equivalent).
      5. Any migration that locks a table for > 1 second requires explicit user approval before running.
    - **Rollback procedure** — every migration must have a corresponding down migration unless it is an additive-only change.
    - **Seeding** — which seed data is required for the system to function (enum values, admin user, feature flags); seed scripts stored in `docs/ops/seeds/`.

### Step 9 — Data lifecycle and retention
16. Write the retention policy section. For each entity or entity group:
    - **Retention period** — how long records are kept after they are logically deleted or superseded.
    - **Purge mechanism** — soft-delete + scheduled purge job, TTL index (document DB), partitioned tables with partition drops, archival to cold storage.
    - **Legal hold** — if applicable, the mechanism to exempt records from purge.
    - **Backup frequency and RTO/RPO** — per the NFRs in the product spec.

### Step 10 — Confirm with user
17. **STOP.** Present the entity list, the ERD Mermaid block, the index strategy table, and the migration strategy.
18. Ask: "Are all the entities correct? Any fields missing, relationships drawn wrong, or indexes you want to add or remove?"
19. Iterate on corrections. Do not allow build to start until the data model is approved.

## Agents used
None — this command runs inline.

## Skills used
- `.claude/skills/security/SKILL.md` — column sensitivity, encryption-at-rest requirements, row-level security patterns.

## Expected outputs
| Path | Description |
|------|-------------|
| `docs/architecture/data-model.md` | Full data model: entities, fields, relationships, ERD, index strategy, compliance treatment, migration strategy, retention policy |

## Stop conditions
- Architecture is not approved — `docs/architecture/overview.md` must exist and have passed user confirmation before this command runs.
- An entity is referenced in two feature specs with conflicting field requirements — surface the conflict to the user before designing the entity.
- A monetary amount field is proposed as `FLOAT` or `DOUBLE` — reject; ask the user to confirm `BIGINT` cents or `DECIMAL(19,4)`.
- A PCI-scoped field (full card number, CVV) is proposed for storage — hard stop. Instruct to use a tokenisation vault and document the decision in the relevant ADR.
- A migration is proposed that would lock a production table — do not write the migration; explain the zero-downtime alternative pattern and ask the user to confirm before including it.
- The total number of entities exceeds 50 and no domain grouping exists — propose domain packages (e.g., Identity, Billing, Catalogue) and ask the user to approve the grouping before designing each domain's model.

## Final report format
```
## /design-data-model — Data Model Complete

**Entities defined:** <count>
  Core: <count> — <list>
  Supporting: <count> — <list>
  Audit/log: <count> — <list>
  Cache/projection: <count> — <list>

**Relationships:** <count>
**Indexes recommended:** <count>
**Queries mapped:** <count>
  Full-table scan risks flagged: <count or "none">

**Compliance:**
  PII fields: <count>
  PHI fields: <count>
  PCI-scoped fields: <count> (all tokenised — none stored)
  GDPR erasure procedure: <documented / not applicable>

**Migration tool:** <name>
**Retention policies:** <count of entity groups with defined policy>

**Output:** docs/architecture/data-model.md
**Next step:** roadmap-agent → build phases
```

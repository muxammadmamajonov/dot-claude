# Data Model

> **What this is:** the entities, relationships, constraints, indexes, and migration/retention strategy that the persistence layer implements. Filled in by the **database-architect** + **data-engineer** agents after the product spec and architecture. Reviewed against the [data-model checklist](../checklists/data-model.md).

---

## 1. Overview
> What is stored, the storage engine(s) chosen, and the consistency model.

- **Primary store:** `<from .claude/stack-matrix/database.md, e.g. PostgreSQL>`
- **Consistency:** `<strong / eventual where>` · **Multi-tenancy:** `<shared schema + tenant_id / schema-per-tenant>`

## 2. Entities
> For each entity: purpose, attributes (name, type, constraints), and notes. Repeat the block per entity.

### `<Entity: User>`
> Purpose: `<who/what it represents>`

| Attribute | Type | Constraints | Notes |
|-----------|------|-------------|-------|
| id | `<uuid>` | PK | `<generated>` |
| email | `<text>` | unique, not null | `<citext / lowercased>` |
| created_at | `<timestamptz>` | not null, default now | |
| tenant_id | `<uuid>` | FK → Tenant, not null | `<scoping key>` |

## 3. Relationships
> Cardinality and ownership (text ERD). Note cascade behavior.

```
Tenant 1───* User 1───* <Resource>
<Resource> *───* Tag   (via <ResourceTag> join)
```
> On delete: `<User soft-deleted; Resources reassigned, not cascaded>`

## 4. Indexes
> Index every foreign key and every column used in WHERE/ORDER/JOIN on hot paths. State the query each serves.

| Index | Columns | Serves query | Type |
|-------|---------|--------------|------|
| `<idx_resource_tenant_created>` | (tenant_id, created_at desc) | `<list resources per tenant>` | btree |

## 5. Data lifecycle & retention
> How long data lives, when it's archived/deleted, and how (soft vs hard delete).

| Data | Retention | Deletion method |
|------|-----------|-----------------|
| `<audit logs>` | `<7 years>` | `<archive then purge>` |
| `<PII on account close>` | `<30 days then erase>` | `<hard delete / anonymize>` |

## 6. Migration strategy
> How schema changes ship safely. Forward-only, reversible, zero-downtime where needed.

- **Tool:** `<from stack, e.g. Prisma/Flyway/Alembic>`
- **Rules:** `<expand-then-contract; never drop a column in the same release that stops writing it; migrations are reviewed and reversible; never delete a migration file>`

## 7. Data integrity rules
> Constraints enforced at the DB level (not just app): uniqueness, FKs, checks, not-null.

- `<CHECK (amount >= 0)>`; `<UNIQUE (tenant_id, email)>`

## 8. Classification & privacy
> Tag sensitive fields. Drives encryption, access control, and compliance.

| Field | Classification | Handling |
|-------|----------------|----------|
| `<email, name>` | PII | `<encrypt at rest, restrict access>` |
| `<card data>` | PCI | `<do not store; tokenize via processor>` |

## 9. Open questions
- [ ] `<modeling question, e.g. "single-table or per-tenant schema?">`

---
**Done when:** every entity has typed attributes and constraints, relationships state cardinality + delete behavior, all FKs and hot-path columns are indexed, retention and migration rules are explicit, sensitive fields are classified, and integrity is enforced in the DB. Review with the [data-model checklist](../checklists/data-model.md).

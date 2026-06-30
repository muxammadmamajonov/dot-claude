# Architecture / Technical Decision Record (ADR)
**What:** A permanent, dated record of a significant technical or architectural decision — why it was made, what alternatives were considered, and what consequences it carries.  
**Who fills it in:** The engineer or team who owns the decision. One ADR per decision.  
**Cross-references:** `.claude/templates/feature-spec.md`, `.claude/templates/architecture.md`

---

## ADR Metadata

| Field | Value |
|-------|-------|
| ADR number | `<ADR-0042>` |
| Title | `<Use PostgreSQL as the primary datastore instead of MongoDB>` |
| Date | `<YYYY-MM-DD>` |
| Status | `<Proposed | Accepted | Deprecated | Superseded by ADR-XXXX>` |
| Deciders | `<@eng-lead, @backend-1, @backend-2>` |
| Consulted | `<@cto, @security>` |
| Informed | `<all engineering>` |

---

## 1. Context

> What situation, constraint, or problem forced this decision? Describe the technical and business pressures that made the decision necessary. Keep it factual — this is not the place for advocacy.

`<We need to persist user and transaction data for the payments feature. The data is relational: users have many orders, orders have many line items, and we need ACID guarantees for financial records. The team has strong SQL experience but limited MongoDB expertise. We are on a timeline of 6 weeks to launch.>`

**Constraints driving the decision:**
- `<ACID compliance required for financial data>`
- `<Team SQL expertise vs. learning curve>`
- `<Existing infrastructure: we already run Postgres for the auth service>`
- `<Budget: managed database cost must stay under $X/month at expected scale>`

---

## 2. Decision Drivers

> List the criteria that matter most for evaluating options. Rank or weight them if helpful.

1. **Data integrity** — ACID guarantees for financial records (highest priority)
2. **Team familiarity** — reduce ramp-up time under tight deadline
3. **Operational cost** — leverage existing infrastructure where possible
4. **Query flexibility** — complex reporting queries needed by finance team
5. **Scalability** — must handle `<10 M rows / 1 TB>` within 2 years
6. `<Add project-specific driver>`

---

## 3. Options Considered

> Describe each option evaluated. Be fair — include strengths and weaknesses for every option, not just the one that lost.

### Option A — `<PostgreSQL (chosen)>`

**Description:** `<Use the managed PostgreSQL instance already running in our AWS RDS cluster, adding a new database for payments.>`

**Strengths:**
- Full ACID compliance, mature ecosystem
- Team already proficient; no training needed
- Reuses existing RDS infrastructure — no new ops burden
- Strong support for complex joins and aggregations needed by finance reports

**Weaknesses:**
- Horizontal write scaling requires sharding (not needed at current scale)
- Schema migrations require care in a live system

**Cost estimate:** `<+$80/month on existing RDS cluster>`

---

### Option B — `<MongoDB Atlas>`

**Description:** `<Use MongoDB Atlas with multi-document transactions for the payments data model.>`

**Strengths:**
- Flexible schema could simplify certain document shapes
- Atlas managed service handles ops

**Weaknesses:**
- Multi-document ACID transactions available but more complex to reason about
- Team unfamiliar — estimated 2-week ramp-up, unacceptable on current timeline
- Additional vendor relationship and cost (~$200/month)
- Financial audit queries (complex aggregations) are harder to write and optimize

**Cost estimate:** `<$200/month>`

---

### Option C — `<SQLite (embedded, for mobile/desktop variant)>`

**Description:** `<Only applicable if the product is a local-first desktop or mobile app with no server-side persistence requirement.>`

**Strengths:**
- Zero ops, zero cost, built into most runtimes

**Weaknesses:**
- Single-writer, no server-side multi-user access
- Does not meet the multi-user payments requirement

**Verdict:** Eliminated early — wrong fit for this use case.

---

## 4. Decision

> State the chosen option in one sentence. Do not hedge.

**We will use `<Option A — PostgreSQL>`.**

`<We will add a payments database to the existing RDS PostgreSQL cluster. The schema will be managed with incremental, backward-compatible migrations using <Flyway / Alembic / rails db:migrate>. Connection pooling will be handled by <PgBouncer / RDS Proxy>.>`

---

## 5. Rationale

> Explain why this option best satisfies the decision drivers. Reference specific trade-offs accepted.

- **Data integrity:** PostgreSQL's native ACID transactions are the simplest path to correct financial records with no additional complexity.
- **Speed:** Team can deliver in the 6-week window without a learning curve. MongoDB would require 2 weeks of ramp-up we cannot afford.
- **Cost:** Reusing the existing RDS cluster saves ~$120/month over Atlas and introduces no new operational surface.
- **Trade-off accepted:** We accept that horizontal write scaling via sharding is more complex in Postgres than in MongoDB. This is not a concern at our current scale, and we will revisit in `<ADR-XXXX>` if write throughput exceeds `<50 K TPS>`.

---

## 6. Consequences

> What becomes easier, harder, or newly required as a result of this decision?

**Positive consequences:**
- Financial records have strong consistency guarantees out of the box.
- Finance team can run ad-hoc SQL reports without ETL.
- No new infrastructure to provision or on-call.

**Negative consequences / new obligations:**
- Schema migrations must be planned carefully — additive-only pattern required for zero-downtime deploys.
- If the team grows beyond `<X writes/sec>`, we will need to add read replicas or consider sharding — flag this at `<$Y ARR or Z MAU>`.
- Engineers must not bypass the ORM with raw SQL without a review, to maintain migration traceability.

**Follow-up actions:**

| Action | Owner | Due |
|--------|-------|-----|
| Create `payments` database and initial schema migration | `<@backend-1>` | `<YYYY-MM-DD>` |
| Configure PgBouncer connection pooling | `<@devops>` | `<YYYY-MM-DD>` |
| Add DB scaling review to engineering calendar at 50 K TPS | `<@eng-lead>` | `<recurring>` |

---

## 7. References

> Links to any supporting material — benchmarks, RFCs, prior art, vendor docs, incident reports that informed this decision.

- `<Link to load test results comparing Postgres vs. MongoDB at target scale>`
- `<Link to team survey on database familiarity>`
- `<PostgreSQL ACID documentation>`
- `<ADR-0038 — Database infrastructure standardisation>`

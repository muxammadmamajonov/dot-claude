# Architecture Document

> **What this is:** the technical blueprint — components, boundaries, data flow, and the trade-offs behind them. Filled in by the **solution-architect** agent after specs and stack selection. Pairs with [decision-record.md](decision-record.md) for each major choice. Reviewed against the [architecture checklist](../checklists/architecture.md).

---

## 1. Context & goals
> What is this system, and what must the architecture optimize for (and tolerate)?

- **System:** `<one line>`
- **Primary drivers (rank them):** `<e.g. time-to-market > cost > scale>`
- **Constraints:** `<team size/skills, budget, compliance, deadlines, existing systems>`

## 2. Non-functional requirements (NFRs)
> The numbers the architecture must hit. Vague NFRs cause bad designs — quantify.

| NFR | Target |
|-----|--------|
| Availability | `<99.9%>` |
| p95 latency (key path) | `<200 ms>` |
| Throughput | `<1k req/s peak>` |
| Data durability / RPO / RTO | `<RPO 5 min / RTO 1 h>` |
| Concurrent users | `<10k>` |

## 3. System context
> The system and its external actors/integrations (text C4-context).

```
[User] -> [<App/Client>] -> [<API / Backend>] -> [<Datastore>]
                                   |-> [<3rd-party: payments/email/...>]
```

## 4. Components & responsibilities
> Each major component, its single responsibility, and what it owns.

| Component | Responsibility | Owns (data/contract) | Tech |
|-----------|----------------|----------------------|------|
| `<API service>` | `<business logic, auth>` | `<orders, users>` | `<from stack-matrix>` |
| `<Worker>` | `<async jobs>` | `<job queue>` | |

## 5. Data flow
> How a key request travels end-to-end (the "walking skeleton" path). Note sync vs async.

> `<1. Client submits → 2. API validates + authorizes → 3. writes to DB → 4. enqueues job → 5. worker processes → 6. notifies client>`

## 6. Integrations
> External systems, protocol, auth, failure mode, idempotency.

| Integration | Direction | Protocol | Failure handling |
|-------------|-----------|----------|------------------|
| `<Stripe>` | out + webhook in | HTTPS/webhook | `<retry + idempotency key>` |

## 7. Cross-cutting concerns
> How auth, errors, logging/tracing, config/secrets, and caching are handled *consistently*.

- **AuthN/Z:** `<...>` · **Errors:** `<standard envelope>` · **Observability:** `<logs+metrics+traces>` · **Secrets:** `<vault/env, never in code>`

## 8. Scaling, availability & failure
> How it scales, where the single points of failure are, and how it degrades.

- **Scale strategy:** `<stateless horizontal, read replicas, queue buffering>`
- **SPOFs & mitigations:** `<...>` · **Degradation:** `<read-only mode, circuit breakers>`

## 9. Risks & trade-offs
> The honest list. What did we choose against, and what does it cost us?

| Decision | Trade-off accepted | Revisit when |
|----------|--------------------|--------------|
| `<monolith first>` | `<harder to scale teams later>` | `<>20 engineers>` |

## 10. Decision records
> Link every foundational choice to an ADR.

- ADR-001: `<language/framework>` → [decision-record.md](decision-record.md)

---
**Done when:** components have single responsibilities and clear ownership, NFRs are quantified, the key data flow is traced, integrations specify failure handling, cross-cutting concerns are consistent, and every major choice has an ADR. Review with the [architecture checklist](../checklists/architecture.md).

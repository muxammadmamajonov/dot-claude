---
description: Produce architecture overview, component diagram, integration map, and trade-off analysis
argument-hint: [optional component or concern to focus on, e.g. "auth" or "realtime"]
---

# /design-architecture

## Purpose
Translate the approved stack and specs into a concrete architecture: bounded components, communication patterns, data flows, integration topology, non-functional requirement (NFR) allocations, and documented trade-offs. The output is the reference document that build agents use to generate directory structures, interfaces, and deployment configs.

## When to use
- As Phase 5 of `/start-project`, after the stack is confirmed.
- Standalone when adding a major new component (a background job system, a new integration, a microservice split).
- When re-evaluating an existing architecture after a scale or compliance change.

## Workflow

### Step 1 — Load inputs
1. Read `docs/decisions/stack.md` and all ADRs in `docs/decisions/adr/`.
2. Read `docs/specs/product-spec.md` — NFR section, scope, and platform list.
3. Read `docs/specs/business-rules.md` — state machines, data boundaries, compliance rules.
4. Read `docs/specs/roles-permissions.md` — trust boundaries between actor types.
5. Read `docs/state/project-type.md` — primary type shapes the default architectural style.

### Step 2 — Choose architectural style
6. Select the primary architectural style from the table below, guided by primary project type and NFRs. Record the choice and rationale.

| Style | Best fit for | Key trade-off |
|-------|-------------|---------------|
| Monolith (modular) | Small team, tight deadline, single deploy unit | Simple to start; harder to scale individual components later |
| Layered (MVC/MVVM) | Traditional web/desktop apps, clear UI-logic-data split | Familiar; can become entangled if layering is not enforced |
| Microservices | Large team, multiple domains, independent scaling needs | Operational complexity; requires service mesh or gateway |
| Event-driven | Async workflows, audit trails, decoupled producers/consumers | Eventual consistency; harder to debug end-to-end |
| Serverless | Bursty workloads, low ops overhead, pay-per-use budget | Cold starts; limited execution time; vendor lock-in |
| Edge-first | Low-latency global delivery, CDN logic, offline-capable | Complex cache invalidation; limited runtime environment |
| Hexagonal (Ports & Adapters) | Domain-heavy logic, multiple delivery mechanisms, testability | More boilerplate; learning curve for smaller teams |
| Plugin / Extension | Extensible platform, third-party developer ecosystem | Plugin isolation; versioning of contracts |
| Client-server (embedded) | IoT/embedded with a cloud backend | Bandwidth and power constraints on device side |
| Smart contract + backend | Blockchain; on-chain logic with off-chain indexing | Gas costs; immutability trade-offs; oracle trust |

### Step 3 — Define components and boundaries
7. List every component the system needs. For each component:
   - **Name** — short identifier used consistently in all docs.
   - **Responsibility** — one sentence; what it owns and what it never does.
   - **Technology** — the specific choice from the stack.
   - **Scaling unit** — how it scales (horizontal pod, lambda invocation, single process, etc.).
   - **Failure mode** — what breaks and what degrades gracefully if this component goes down.

8. Identify **trust boundaries** — lines across which authentication/authorisation checks are required. Every cross-boundary call must show the auth mechanism (JWT, mTLS, API key, IAM role).

### Step 4 — Draw component diagram
9. Write a Mermaid `graph TB` diagram into `docs/architecture/overview.md`. Include:
   - All components as nodes.
   - Synchronous calls as solid arrows with the protocol label (HTTP/REST, gRPC, SQL, etc.).
   - Asynchronous calls as dashed arrows with the queue/event name.
   - Trust boundaries as subgraph blocks.
   - External third-party services as a separate `External` subgraph.

   Example node naming convention: `[ClientApp]`, `[APIGateway]`, `[AuthService]`, `[DB:Postgres]`, `[Queue:SQS]`, `[Ext:Stripe]`.

### Step 5 — Map integrations
10. For each third-party integration identified in specs, write an entry in the integrations section of `overview.md`:
    - **Name** — e.g., Stripe, SendGrid, Twilio, AWS S3.
    - **Direction** — inbound (they call us), outbound (we call them), or bidirectional.
    - **Auth mechanism** — API key, OAuth2 client credentials, webhook signature, mTLS.
    - **Failure handling** — retry policy, circuit breaker, fallback behaviour, dead-letter queue.
    - **Data sensitivity** — what PII or sensitive fields cross this boundary.
    - **Vendor lock-in risk** — low / medium / high; mitigation if high.

### Step 6 — Allocate NFRs to components
11. Take every NFR from `product-spec.md` and map it to the component(s) responsible for meeting it.

    Example:
    | NFR | Target | Responsible component(s) | How met |
    |-----|--------|--------------------------|---------|
    | p99 latency < 200 ms | API reads | APIGateway, Cache | Redis cache-aside; DB index coverage |
    | 99.9% uptime | All | APIGateway, DB | Multi-AZ DB; health-check load balancer |
    | GDPR right-to-erasure < 30 days | All PII stores | UserService, DB | Soft-delete + async purge job |

### Step 7 — Document trade-offs
12. For each significant trade-off made during architecture design, write a short entry:
    - **Decision** — what was chosen.
    - **Alternative not chosen** — what was considered.
    - **Why** — the constraint or priority that decided it.
    - **Cost** — what becomes harder or more expensive as a result.
    - **Reversibility** — can this be changed later and at what cost?

### Step 8 — Identify cross-cutting concerns implementation
13. For each concern marked "Present" or "Likely" in `docs/state/project-type.md`, describe the implementation pattern:
    - **Payments** — which component handles checkout; how payment state is persisted; how idempotency is ensured.
    - **Realtime** — WebSocket server component; connection lifecycle; message fan-out strategy; presence tracking.
    - **AI/ML** — inference component; prompt construction; context window management; cost guardrail; fallback if model is unavailable.
    - **Offline/sync** — local store; sync protocol; conflict resolution strategy (LWW, CRDT, manual merge).
    - **Multi-tenancy** — isolation level per component; tenant context propagation; data leakage prevention.
    - **Auth/identity** — token issuance component; token validation at each trust boundary; session revocation.

### Step 9 — Write the output file
14. Create `docs/architecture/overview.md` with all sections from steps 2–8 in order. Use Mermaid blocks for the diagram. Keep prose tight — tables and bullets preferred over paragraphs.

### Step 10 — Confirm with user
15. **STOP.** Present the architecture overview and the component list.
16. Ask: "Does this architecture match your mental model? Are there components missing, boundaries drawn in the wrong place, or trade-offs you would decide differently?"
17. Iterate on any corrections. Do not proceed to data model until the architecture is approved.

## Agents used
None — this command runs inline.

## Skills used
- `.claude/skills/security/SKILL.md` — trust boundary verification, auth mechanism review.
- `.claude/skills/performance/SKILL.md` — NFR allocation and scaling strategy review.

## Expected outputs
| Path | Description |
|------|-------------|
| `docs/architecture/overview.md` | Full architecture document with Mermaid diagrams, integration map, NFR allocations, and trade-offs |

## Stop conditions
- Stack is not approved — read `docs/decisions/stack.md`; if it does not exist or has no `Status: Accepted` entries, halt and run `/select-stack` first.
- NFRs in the product spec are expressed only as vague adjectives ("fast", "secure", "scalable") with no numeric targets — return to the spec and ask the user for measurable targets before designing to meet them.
- A cross-cutting concern (e.g., multi-tenancy) has no clear isolation model — do not guess; present two or three concrete options to the user and ask them to choose before designing the affected components.
- The component count exceeds 15 for a team of fewer than 5 developers — flag the operational complexity risk; ask whether to consolidate components or confirm the team has DevOps capacity.

## Final report format
```
## /design-architecture — Architecture Complete

**Style:** <chosen architectural style>
**Components defined:** <count>
**Trust boundaries:** <count>
**Integrations mapped:** <count>
**NFRs allocated:** <count>
**Trade-offs documented:** <count>
**Cross-cutting concerns addressed:** <list>

**Diagram:** docs/architecture/overview.md (Mermaid block)
**Open items:** <any unresolved decisions or concerns>

**Next step:** /design-data-model
```

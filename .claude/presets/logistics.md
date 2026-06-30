# Logistics Preset

## Project type

Software products that plan, execute, track, and optimise the physical movement of goods, vehicles, or people through a supply chain or delivery network. Common variants:

- **Transportation Management System (TMS)** — shipment planning, carrier selection, freight booking, rate management, tracking, and settlement.
- **Warehouse Management System (WMS)** — inbound receiving, putaway, pick/pack/ship, inventory location management, cycle counting, labour management.
- **Last-mile delivery platform** — route optimisation, driver dispatch, real-time tracking, proof of delivery, customer notifications.
- **Fleet management** — vehicle tracking (GPS/telematics), maintenance scheduling, driver hours-of-service (HOS) compliance, fuel management.
- **Freight marketplace / digital freight brokerage** — connects shippers and carriers; spot rate quoting, load board, automated matching, digital POD.
- **Supply chain visibility platform** — multi-tier supplier tracking, ETA prediction, exception management, carbon reporting.
- **3PL / fulfilment platform** — multi-client warehouse operations, order management, billing per client, white-label tracking pages.
- **Cold-chain / specialised cargo** — temperature monitoring, regulatory chain-of-custody (pharma, food), reefer telematics.
- **Customs and trade compliance** — import/export documentation, HS code classification, duty calculation, AES/CBP filings.

## Typical use cases

- E-commerce brand using a last-mile platform to dispatch 5,000 parcels per day from a fulfilment centre.
- Regional LTL carrier building a TMS to automate load planning, carrier rate shopping, and invoice auditing.
- 3PL offering WMS-as-a-service to 50 e-commerce brands, each with isolated inventory and billing.
- Food distributor tracking cold-chain temperature continuously and alerting on excursions.
- Ride-hailing or on-demand delivery network dispatching drivers in real time.
- Enterprise manufacturer tracking inbound component shipments across a 200-supplier network.
- Digital freight broker aggregating spot rates from 100+ carriers and auto-tendering loads.

## Required discovery questions

1. What physical flows does the product manage — inbound, outbound, inter-facility, last-mile, or international? What modes of transport (road, rail, air, sea, parcel)?
2. Who are the users? (Dispatchers, warehouse operators, drivers on mobile, third-party carriers, customers tracking their orders, finance teams reconciling freight invoices.) What device and connectivity constraints do field users have?
3. What external systems must the product integrate with at launch? (ERP/OMS for order feeds, carrier APIs for rate and tracking, telematics/GPS providers, EDI trading partners, customs systems, e-commerce platforms.)
4. What are the real-time requirements? (Driver location updates frequency, ETA recalculation interval, customer notification latency, warehouse event processing throughput.) What happens when connectivity is lost in the field?
5. What optimisation problems does the product need to solve? (Vehicle Routing Problem with time windows, bin packing, load consolidation, dynamic re-routing, zone-based rate shopping.) What scale — how many stops, vehicles, or shipments per optimisation run?
6. What regulatory and compliance obligations apply? (DOT/FMCSA ELD mandate for HOS, IFTA fuel tax, ADR/IATA for hazardous materials, FDA Food Safety Modernization Act, customs/AES/CBP filing, GDPR for driver data in EU.)
7. What is the data model for a shipment? (Shipper, consignee, origin/destination, cargo description, weight/dimensions, special requirements, carrier, rate, status history, documents.) How many status transitions exist and what triggers them?
8. What SLA commitments govern the platform? (Carrier on-time delivery tracking, customer-facing ETA accuracy, warehouse throughput targets, system availability during peak shipping seasons.)
9. What billing and settlement model is in scope? (Freight invoice auditing and payment, carrier payment terms, 3PL per-order billing to clients, driver pay-per-stop, marketplace transaction fee.)
10. What geospatial and mapping requirements exist? (Map provider, geocoding quality in operating region, routing engine — OSRM/GraphHopper/Google/HERE, reverse geocoding for address correction, geofence events for arrival/departure detection.)

## Recommended agents

**Core**
- `.claude/agents/core/orchestrator.md` — flow control and gate enforcement.
- `.claude/agents/core/solution-architect.md` — event-driven shipment state machine, integration architecture, geospatial data model.
- `.claude/agents/core/requirements-engineer.md` — SLA invariants, regulatory acceptance criteria, offline-first field requirements.
- `.claude/agents/core/product-manager.md` — operational workflow scope, carrier/driver UX, customer notification strategy.

**Engineering**
- `.claude/agents/engineering/backend-engineer.md` — shipment lifecycle engine, carrier API integrations, EDI/webhook processing, billing engine.
- `.claude/agents/engineering/mobile-engineer.md` — driver app (offline-capable), proof-of-delivery capture, barcode scanning, turn-by-turn navigation handoff.
- `.claude/agents/engineering/realtime-engineer.md` — GPS/telematics event ingestion, real-time ETA engine, live tracking map, push notifications.
- `.claude/agents/engineering/data-engineer.md` — route analytics, on-time performance reporting, carrier scorecard, fuel/carbon reporting.
- `.claude/agents/engineering/devops-engineer.md` — high-availability for operational systems, peak-season scaling, EDI integration infrastructure.
- `.claude/agents/engineering/integration-engineer.md` — carrier API adapters, EDI X12/EDIFACT, ERP connectors, telematics device integration.

**Quality**
- `.claude/agents/quality/reliability-engineer.md` — 24/7 operational availability, failover for dispatch systems, offline field operations.
- `.claude/agents/quality/security-auditor.md` — driver PII protection, cargo data confidentiality, carrier credential management, EDI security.
- `.claude/agents/quality/performance-engineer.md` — route optimisation latency, GPS event throughput, concurrent dispatch operations.
- `.claude/agents/quality/qa-engineer.md` — shipment lifecycle edge cases, ETA accuracy validation, integration failure recovery, offline sync conflicts.
- `.claude/agents/quality/production-readiness-auditor.md` — operational incident runbooks, on-call for dispatch outages, monitoring dashboards.

**Domain**
- `.claude/agents/domain/logistics-domain-expert.md` — shipment state machines, carrier API patterns, EDI X12/EDIFACT, VRP optimisation, HOS compliance, customs documentation.

## Recommended skills

- `.claude/skills/backend/SKILL.md` — event-driven shipment state machine, idempotent status updates, carrier webhook adapters.
- `.claude/skills/mobile/SKILL.md` — offline-first driver app, background GPS tracking, POD photo/signature capture, conflict resolution on sync.
- `.claude/agents/engineering/realtime-engineer.md` — high-throughput GPS event ingestion, WebSocket live tracking, geofence detection.
- `.claude/skills/data-modeling/SKILL.md` — shipment and leg hierarchy, location history time-series, carrier rate tables, inventory location model.
- `.claude/skills/api-design/SKILL.md` — carrier integration adapter pattern, webhook idempotency, EDI-to-JSON normalisation.
- `.claude/skills/performance/SKILL.md` — geospatial index strategy (PostGIS), route optimisation batching, time-series GPS data partitioning.
- `.claude/skills/devops/SKILL.md` — peak-season auto-scaling, queue-based carrier API calls with backpressure, multi-region for geographically distributed operations.
- `.claude/skills/testing/SKILL.md` — shipment lifecycle integration tests, GPS replay testing, carrier API mock/contract tests, offline sync conflict tests.

## Recommended stack options

| Stack | Rationale |
|-------|-----------|
| **Node.js / TypeScript + PostgreSQL + PostGIS + Redis + React** | PostGIS handles all geospatial queries (proximity, geofence, route geometry) natively; Redis stores live vehicle positions and pub/sub for real-time map updates; strong TypeScript ecosystem for carrier SDK integration. See `.claude/stack-matrix/backend.md`, `.claude/stack-matrix/database.md`. |
| **Go + PostgreSQL + PostGIS + Kafka + React Native (driver) + React (ops)** | Go's concurrency model handles high-throughput GPS event ingestion efficiently; Kafka decouples telematics ingest from downstream processing; React Native for driver app. See `.claude/stack-matrix/backend.md`, `.claude/stack-matrix/realtime.md`. |
| **Python (FastAPI/Django) + PostgreSQL + PostGIS + Celery + React** | Python ecosystem has strong OR-Tools integration for VRP optimisation; Celery manages route-calculation jobs and carrier polling; good for optimisation-heavy TMS. See `.claude/stack-matrix/backend.md`, `.claude/stack-matrix/ai-ml.md`. |
| **Java / Kotlin (Spring Boot) + PostgreSQL + PostGIS + ActiveMQ + React** | JVM suits enterprise WMS or TMS with complex EDI integration; mature EDI and carrier API libraries; Spring Batch for high-volume freight invoice processing. See `.claude/stack-matrix/backend.md`. |

## Required checklists

- `.claude/checklists/security.md` — extend with: driver PII (location history, personal details) access restricted to authorised dispatchers and the driver themselves; cargo manifest data confidential between shipper and carrier; carrier API credentials stored in secrets manager and rotated; no GPS history retained beyond operational retention policy.
- `.claude/checklists/qa.md` — extend with: shipment state machine tested for all valid and invalid transitions; ETA recalculation tested with simulated traffic events; offline driver app syncs correctly on reconnect without duplicating events; carrier API failure does not leave shipment in an indeterminate state.
- `.claude/checklists/production.md` — extend with: dispatch system availability target met (typically 99.9 %+ during operating hours); operational monitoring dashboard shows live shipment health; on-call rotation covers 24/7 if carrier or driver operations span time zones; database replicas tested for read-query failover.
- `.claude/checklists/performance.md` — extend with: route optimisation for 200 stops completes within acceptable dispatch latency; GPS event ingest benchmarked at peak fleet size; geospatial queries (nearest driver, geofence check) respond within 200 ms at P99; peak-season load test at 3× normal volume.

## MVP scope pattern

**In the first cut:**
- One primary flow end-to-end: either last-mile dispatch + tracking, or warehouse pick/pack/ship, or TMS shipment booking — not the full supply chain.
- Shipment state machine with explicit states: created → assigned → in-transit → delivered / failed; every transition logged with timestamp and actor.
- Driver or operator mobile app with essential field actions (accept job, update status, capture POD) that works offline and syncs when connectivity returns.
- Real-time tracking page for the end customer (public URL with signed token, auto-updates via WebSocket or polling).
- Integration with one carrier or one ERP/OMS for order feed — hardcode the adapter, then generalise.
- Basic dispatcher dashboard: active shipments map, status filter, manual reassignment.
- Operational alert: notify dispatcher when a shipment is late against its scheduled window.
- Driver PII encrypted at rest; GPS history retained only for the operational and legal minimum.

**Deferred to later:**
- Route optimisation (VRP) — start with manual assignment or simple nearest-driver; add optimisation once daily volume justifies the compute cost.
- EDI X12/EDIFACT integration (complex and carrier-specific; negotiate and build per enterprise customer).
- Multi-carrier rate shopping and automated carrier selection (build after single-carrier model is proven).
- Freight invoice auditing and automated payment (add when finance team validates the reconciliation workflow).
- Cold-chain IoT temperature monitoring (requires hardware partnership; validate logistics core first).
- Customs and trade compliance filings (jurisdiction-specific; add when international lanes are launched).
- Carbon/emissions reporting (add as a premium feature after operational data is flowing).
- Machine-learning ETA prediction (start with rule-based; replace with ML once historical data accumulates).

## Production risks

| Risk | Priority | Notes |
|------|----------|-------|
| Dispatch system outage during peak operations — drivers cannot receive jobs | P0 | 99.9 %+ availability target during operating hours; auto-failover to read replica for query traffic; manual dispatch fallback procedure documented and practiced. |
| GPS event loss causes stale ETA — customer and dispatcher see wrong location | P0 | Detect GPS silence > threshold and show "last known position" with timestamp; ETA marked as stale; alert dispatcher; driver app retries location post in background. |
| Shipment stuck in terminal state due to carrier API failure — no recovery path | P0 | Every carrier API call has a compensating action; stuck shipments surface in a manual-review queue within 15 minutes; runbook for each carrier's failure modes. |
| Offline sync conflict corrupts shipment status — two drivers claim the same load | P0 | Optimistic locking with server-side conflict resolution; assignment is single-writer (server owns authoritative state); driver app shows conflict and requires dispatcher resolution. |
| Driver PII (real-time location) exposed to unauthorised parties | P1 | Signed short-lived tokens for customer tracking URLs; dispatcher access logged; driver location purged from public-facing layer after delivery; GDPR right-to-erasure for driver data. |
| Route optimisation produces infeasible routes — driver cannot complete schedule | P1 | VRP solver output validated against hard constraints (time windows, vehicle capacity, HOS limits) before dispatch; solver timeout falls back to current manual assignment. |
| EDI message processing error silently drops a shipment booking | P1 | EDI ingest pipeline has a dead-letter queue; every inbound EDI message acknowledged only after successfully parsed and persisted; alert on DLQ depth > 0. |
| Peak-season volume spike crashes the database — Black Friday or holiday peak | P1 | Load test at 3× normal volume before peak season; read replicas for reporting queries; connection pooler (PgBouncer) sized for peak fleet; auto-scaling policy tested. |
| Geofence events misfiring — false arrival/departure triggers incorrect status updates | P2 | Geofence radius tuned per location type; require N consecutive fixes inside boundary before triggering; manual override available to dispatcher. |
| Carrier rate data stale — shipment booked at wrong rate causing financial loss | P2 | Rate validity window enforced; re-validate rate at booking confirmation; alert on rate expiry before automated re-booking. |

## Launch requirements

- Shipment state machine tested for all valid transitions and all invalid transition attempts (must be rejected with a clear error).
- Offline driver app tested: complete a job start-to-POD with airplane mode; verify all events sync correctly on reconnect with no duplicates or state corruption.
- Customer tracking page loads within 3 seconds on a mobile connection and updates location within the documented refresh interval.
- Dispatcher alert fires within 5 minutes of a shipment passing its expected-delivery window.
- Carrier API adapter tested against the carrier's sandbox for all in-scope operations (book, track, cancel); failure scenarios produce a recoverable error state.
- GPS event ingest load-tested at peak fleet size; P99 latency within acceptable operational window.
- Driver PII access controls verified: dispatcher A cannot view driver location history for shipments outside their assigned fleet.
- Operational runbooks written and reviewed for: dispatch system outage, carrier API unavailability, stuck shipment recovery, GPS stream interruption.
- On-call rotation active with escalation path; alert thresholds calibrated for operating hours and overnight.
- Database backup tested with restore drill; data integrity of shipment state verified post-restore.
- All regulatory obligations confirmed in scope (ELD, IFTA, HazMat — if applicable): compliance features tested before any regulated operation begins.

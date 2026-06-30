# Fintech Preset

## Project type

Financial technology products that move, store, lend, insure, or report on money. Common variants:

- **Payment processor / gateway** — accept card and ACH payments on behalf of merchants; manage settlement.
- **Digital wallet / stored value** — user balance held on platform; top-up, spend, and transfer flows.
- **Neobank / banking-as-a-service** — current account, debit card, direct deposit, via a bank sponsor or BaaS partner (Stripe Treasury, Synapse, Column).
- **Lending platform** — consumer or SMB loans; origination, underwriting, servicing, collections.
- **Investment / brokerage** — buy/sell securities, crypto, or fractional assets; portfolio management.
- **Insurance tech** — policy purchase, premium collection, claims processing.
- **Accounting / bookkeeping SaaS** — general ledger, invoicing, expense management, reconciliation.
- **Payroll / HR finance** — payroll processing, tax filing, on-demand pay, benefits administration.
- **Expense management / corporate cards** — virtual/physical cards, spend controls, receipt capture, ERP sync.
- **B2B payments / AP-AR automation** — supplier payments, invoice financing, FX, cross-border transfers.

## Typical use cases

- Consumer app with a linked bank account for spending analytics and savings goals.
- Marketplace payout platform distributing earnings to thousands of sellers/gig workers.
- SMB lending underwriting engine consuming open-banking data.
- Cross-border remittance with FX conversion and local payout rails.
- Corporate card programme with per-employee spend limits and policy enforcement.
- Embedded finance: an e-commerce platform offering BNPL or merchant cash advance.
- Tax filing software with bank feed aggregation and automated categorisation.

## Required discovery questions

1. What money movement does the product perform? (Accept payments, store balances, disburse funds, lend, invest, insure.) Which flows are in scope at launch?
2. What licences, registrations, or bank partnerships are required in the target markets? (MSB registration, money transmitter licence, EMI/PI licence, bank charter, broker-dealer registration, insurance licence — or operating under a BaaS sponsor's licence.)
3. What payment rails are in scope? (Card networks — Visa/Mastercard; ACH/SEPA/Faster Payments; wire/SWIFT; RTP/FedNow; open banking APIs.) Who are the processing partners?
4. What KYC/AML programme is required? (CIP for account opening, ongoing transaction monitoring, SAR filing, OFAC screening.) Will you build this or use a vendor (Persona, Sardine, ComplyAdvantage)?
5. What are the data residency, encryption, and audit requirements? (PCI-DSS level, SOC 2 Type II, ISO 27001, GDPR, CCPA, local financial regulator requirements.)
6. Is the ledger the source of truth for balances, or does a third-party hold funds and you reflect their state? (Affects double-entry vs. shadow ledger design.)
7. What are the idempotency and exactly-once delivery requirements for transactions? What is the acceptable window for a failed transaction to be retried vs. flagged for manual review?
8. What is the dispute, chargeback, and fraud loss model? Who bears liability — the platform, the end user, or the bank partner?
9. What reporting obligations exist? (1099s, CTRs, SARs, regulatory capital reports, audit trails that must be immutable and retained for N years.)
10. What does the error recovery path look like for a stuck or failed transaction at each step of the payment rail? (Partial failure scenarios must be specified before any money-movement code is written.)

## Recommended agents

**Core**
- `.claude/agents/core/orchestrator.md` — flow control and gate enforcement.
- `.claude/agents/core/solution-architect.md` — ledger architecture, rail integration, idempotency model.
- `.claude/agents/core/requirements-engineer.md` — transaction invariants, compliance acceptance criteria, failure modes.

**Engineering**
- `.claude/agents/engineering/backend-engineer.md` — ledger, payment rail integration, idempotent transaction engine, webhooks.
- `.claude/agents/engineering/devops-engineer.md` — secrets management, audit log pipeline, zero-downtime migration strategy.

**Quality**
- `.claude/agents/quality/security-auditor.md` — PCI-DSS scope, secrets, access control on financial data, fraud vectors.
- `.claude/agents/quality/privacy-compliance-auditor.md` — KYC data, PII retention and deletion, regulatory reporting.
- `.claude/agents/quality/qa-engineer.md` — idempotency tests, partial-failure recovery, double-entry invariant verification.
- `.claude/agents/quality/reliability-engineer.md` — exactly-once delivery, reconciliation jobs, SLA on money movement.
- `.claude/agents/quality/production-readiness-auditor.md` — transaction monitoring alerts, runbooks, rollback procedures.

**Domain**
- `.claude/agents/domain/fintech-domain-expert.md` — double-entry ledger design, KYC/AML, PCI-DSS, reconciliation, audit trails.

## Recommended skills

- `.claude/skills/backend/SKILL.md` — idempotent API design, webhook handling, transaction state machines.
- `.claude/skills/security/SKILL.md` — PCI-DSS scope reduction, secrets management, least-privilege access to financial data.
- `.claude/skills/data-modeling/SKILL.md` — double-entry ledger schema, immutable journal entries, account hierarchy.
- `.claude/skills/devops/SKILL.md` — secrets vault, audit log pipeline, zero-downtime schema migrations on financial tables.
- `.claude/skills/testing/SKILL.md` — idempotency tests, ledger balance invariant assertions, rail sandbox integration tests.
- `.claude/skills/production-readiness/SKILL.md` — transaction failure alerting, reconciliation job monitoring, incident runbooks.
- `.claude/skills/performance/SKILL.md` — ledger query optimisation, high-throughput event ingestion, time-series balance snapshots.

## Recommended stack options

| Stack | Rationale |
|-------|-----------|
| **Node.js / TypeScript + PostgreSQL (double-entry ledger) + Stripe Treasury / Connect** | Stripe handles PCI compliance, KYC (Stripe Identity), and payment rails; Postgres gives ACID guarantees for ledger entries; TypeScript catches type errors on financial amounts. See `.claude/stack-matrix/backend.md`. |
| **Go + PostgreSQL + Plaid + Stripe** | Go's concurrency model suits high-throughput payment processing; strong typing prevents amount/currency errors; Plaid for open-banking data ingestion. |
| **Java / Kotlin (Spring Boot) + PostgreSQL + Modern Treasury** | JVM's mature financial library ecosystem; Modern Treasury abstracts multi-rail payment orchestration with built-in reconciliation; suited to enterprise B2B fintech. |
| **Python (FastAPI) + PostgreSQL + Stripe + SQLAlchemy** | Rapid development for lending/underwriting products where ML models (risk scoring) are central; ACID transactions via SQLAlchemy; Stripe for payment collection. |

## Required checklists

- `.claude/checklists/security.md` — extend with: PCI-DSS scope documented and minimised; no card data in application logs; all financial data encrypted at rest and in transit; privileged access to ledger tables requires MFA + audit log; secrets rotated on any suspected exposure.
- `.claude/checklists/qa.md` — extend with: double-entry invariant (Assets = Liabilities + Equity) asserted in automated test after every test transaction; idempotency key prevents duplicate charges in all retry scenarios; partial-failure recovery leaves ledger consistent; reconciliation job matches ledger to rail statement.
- `.claude/checklists/production.md` — extend with: real-time alert on ledger imbalance, on failed transaction > threshold, and on reconciliation discrepancy; manual review queue for stuck transactions; immutable audit log retained per regulatory requirement (minimum 5–7 years depending on jurisdiction).
- `.claude/checklists/performance.md` — extend with: ledger write path benchmarked at peak TPS with ACID guarantees maintained; balance read queries respond < 100 ms at P99; reconciliation job completes within settlement window.

## MVP scope pattern

**In the first cut:**
- One payment rail, one currency, one market.
- Double-entry ledger as the source of truth for all balances from day one — never a running balance column.
- Idempotency keys on every money-movement API endpoint; deduplication enforced at the database level.
- KYC for account opening: collect required identity data via a vetted vendor (Stripe Identity, Persona); do not store raw identity documents internally.
- OFAC/sanctions screening on account creation and before each transaction.
- Transaction state machine with explicit states: initiated → pending → settled / failed / reversed.
- Reconciliation job runs daily: compares ledger entries to rail settlement file; flags discrepancies for manual review.
- Immutable audit log: every state transition in the ledger appends a record with actor, timestamp, and before/after state — no updates or deletes allowed.
- Basic transaction monitoring: flag transactions above regulatory reporting threshold (e.g. $10k CTR in the US).

**Deferred to later:**
- Multi-rail support (ACH + card + wire + RTP).
- Multi-currency and FX conversion.
- Real-time fraud scoring (start with rule-based; add ML model after data volume justifies it).
- Full AML transaction monitoring programme (use a vendor from day one; custom models deferred).
- Self-service dispute portal (start with manual support queue).
- Advanced reporting (1099s, tax engine, regulatory capital calculations).
- Instant payouts / real-time payments (ACH same-day or RTP — add after standard rails proven).
- Embedded finance / white-label product.

## Production risks

| Risk | Priority | Notes |
|------|----------|-------|
| Non-idempotent transaction causes double charge or double payout | P0 | Idempotency key on every money-movement endpoint; database-level unique constraint on (idempotency_key, account_id); test all retry scenarios in CI. |
| Ledger imbalance — funds created or destroyed by a bug | P0 | Assert Assets = Liabilities + Equity in every transaction test; run invariant check as a scheduled job in production; alert immediately on any discrepancy. |
| Partial failure leaves funds in transit with no recovery path | P0 | Every payment rail call must have a defined compensating transaction for each failure mode; document and test all failure scenarios before writing code. |
| Card data or secrets in application logs | P0 | Structured logging with field-level redaction; PCI-DSS log review; automated secret-scanning in CI. |
| Unlicensed money transmission — regulatory enforcement action | P0 | Obtain required licences or contract with a licensed BaaS partner before accepting real money; legal review in each target market. |
| OFAC match not screened — sanctions violation | P0 | Screen on account creation and before every transaction; block and alert immediately on any match; retain screening audit log. |
| Reconciliation not run — undetected fund discrepancy grows | P0 | Reconciliation job is mandatory from day one; alert if job fails to run within settlement window; escalation path for any discrepancy > $0. |
| KYC data stored insecurely or retained beyond regulatory window | P1 | Delegate document storage to vetted KYC vendor; implement data-retention policy with automated deletion; document retention schedule. |
| Insufficient access controls on ledger tables — insider threat | P1 | Database role separation: application reads/writes via limited role; no application-level access to audit log table (append-only via DB trigger or separate service). |
| No SAR/CTR filing process — AML violation | P1 | Define and test the reporting workflow before launch; use AML vendor for threshold alerting and case management. |
| Settlement file format changes break reconciliation | P1 | Parse rail settlement files defensively; alert on unexpected format; maintain file format version in configuration. |
| Rate limits on payment rail API cause cascading failures | P2 | Implement queue-based submission with backpressure; circuit breaker pattern; retry with exponential backoff + jitter. |

## Launch requirements

- Idempotency verified: submitting the same transaction request N times results in exactly one debit and one credit in the ledger.
- Double-entry invariant passing in automated test suite and verified clean in production ledger before any real-money transactions.
- Reconciliation job successfully completed at least one full cycle against a rail sandbox settlement file.
- OFAC screening active on account creation and transaction submission; test match handled correctly (block + alert + log).
- KYC flow tested end-to-end with rail sandbox; no identity documents stored in platform storage.
- Immutable audit log verified: no UPDATE or DELETE possible on journal entry or audit tables via the application role.
- PCI-DSS scope documented; card data confirmed absent from all logs, databases, and analytics systems.
- All required licences or BaaS partnership agreements in place and reviewed by counsel before accepting real money.
- Transaction failure alerting active: alert fires within 5 minutes of a stuck or failed transaction above threshold.
- Incident runbook documented for: ledger imbalance discovered, stuck transaction in rail, suspected fraud event, regulatory data request.
- Privileged access to financial data restricted to named individuals with MFA; access logged and reviewed monthly.
- Backup and restore tested: ledger restored to a consistent double-entry state from backup within documented RTO.

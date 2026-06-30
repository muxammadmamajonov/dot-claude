# ERP Preset

## Project type

Enterprise Resource Planning system. Integrates core business processes — finance/accounting, procurement, inventory, manufacturing, HR/payroll, and sales/fulfillment — into a single shared data model with a unified ledger as the source of truth. Variants span from lightweight SMB back-office tools to full industry-vertical ERP suites.

Common variants:
- **Finance-first ERP** — general ledger, accounts payable/receivable, bank reconciliation, financial reporting
- **Manufacturing ERP** — BOM, production orders, MRP, shop-floor scheduling, quality control
- **Distribution ERP** — purchase orders, inventory, warehousing, shipping, 3PL integration
- **HR/Payroll ERP** — headcount, time & attendance, benefits, payroll runs, tax filing
- **Service ERP** — project accounting, resource planning, professional-services billing
- **Vertical ERP** — industry-specific (retail, construction, healthcare, agri) with specialized modules

---

## Typical use cases

- Double-entry general ledger: every financial event produces balanced debit/credit journal entries
- Period-end close: trial balance → income statement → balance sheet → cash-flow statement
- Accounts payable: vendor invoices, three-way match (PO → receipt → invoice), payment runs
- Accounts receivable: customer invoices, aging reports, collections workflow
- Inventory management: stock movements, valuation (FIFO/LIFO/average cost), reorder points
- Purchase-to-pay cycle: requisition → PO → goods receipt → vendor payment
- Order-to-cash cycle: sales order → pick/pack/ship → invoice → cash application
- Payroll run: time entries → gross pay → statutory deductions → net pay → bank file
- Consolidated reporting across legal entities, currencies, and cost centres

---

## Required discovery questions

1. **Which modules are required at launch?** (Finance / Inventory / Procurement / HR / Manufacturing / Projects) — each module is a major scope item; do not assume a monolith is needed.
2. **What is the primary accounting standard?** (GAAP, IFRS, local GAAP) and **which tax regimes apply?** (VAT/GST, US sales tax, withholding tax) — drives the chart-of-accounts structure, tax engine, and reporting format.
3. **How many legal entities / companies need to be managed?** — single-entity is dramatically simpler; multi-entity requires intercompany eliminations and consolidated reporting.
4. **What currencies are in scope?** (functional vs. presentation currency, revaluation, exchange-rate source) — multi-currency adds significant ledger and reporting complexity.
5. **What data must be migrated, and from which legacy systems?** (opening balances, transaction history, master data: vendors, customers, items) — migration is often the riskiest phase.
6. **What compliance and audit requirements apply?** (SOX controls, local statutory filings, e-invoicing mandates, audit trail requirements) — mandates immutable ledger, period locking, and access controls.
7. **Who are the user roles, and what approval workflows are needed?** (CFO, controller, AP clerk, warehouse manager, HR admin; PO approval thresholds, invoice approval chains) — workflow engine complexity scales with role count.
8. **What integrations are required on day one?** (bank feeds, payment gateway, payroll processor, e-commerce, 3PL, tax authority e-filing) — each integration has its own data format and reliability requirements.
9. **What is the volume and frequency of transactions?** (invoices/month, inventory movements/day, payroll records) — sizes the database, indexing strategy, and batch-job schedules.
10. **Is a custom report builder or BI layer required, or is a fixed report set sufficient for launch?** — determines whether an OLTP-only model suffices or a reporting/analytics layer is needed from day one.

---

## Recommended agents

### Core
- `.claude/agents/core/orchestrator.md`
- `.claude/agents/core/solution-architect.md`
- `.claude/agents/core/requirements-engineer.md`
- `.claude/agents/core/business-analyst.md`
- `.claude/agents/core/system-analyst.md`
- `.claude/agents/core/technical-lead.md`

### Engineering
- `.claude/agents/engineering/backend-engineer.md`
- `.claude/agents/engineering/database-architect.md`
- `.claude/agents/engineering/api-architect.md`
- `.claude/agents/engineering/integration-engineer.md`
- `.claude/agents/engineering/frontend-engineer.md`
- `.claude/agents/engineering/data-engineer.md`

### Quality
- `.claude/agents/quality/security-auditor.md`
- `.claude/agents/quality/qa-engineer.md`
- `.claude/agents/quality/privacy-compliance-auditor.md`
- `.claude/agents/quality/reliability-engineer.md`
- `.claude/agents/quality/production-readiness-auditor.md`
- `.claude/agents/quality/performance-engineer.md`

### Design
- `.claude/agents/design/ui-ux-designer.md`
- `.claude/agents/design/accessibility-designer.md`

### Domain
- `.claude/agents/domain/erp-domain-expert.md`
- `.claude/agents/domain/fintech-domain-expert.md` *(for finance module)*

### Stack
- `.claude/agents/stack/backend/java-spring-engineer.md` or `.claude/agents/stack/backend/dotnet-engineer.md`
- `.claude/agents/stack/database/postgres-engineer.md`

---

## Recommended skills

- `.claude/skills/data-modeling/SKILL.md` — normalized ledger schema, chart of accounts, entity hierarchy
- `.claude/skills/backend/SKILL.md` — double-entry engine, idempotent transaction processing
- `.claude/skills/postgres/SKILL.md` — partitioned ledger tables, advisory locks, serializable transactions
- `.claude/skills/api-design/SKILL.md` — internal module APIs and external integration contracts
- `.claude/skills/security/SKILL.md` — role-based access, period locking, immutable audit log
- `.claude/skills/testing/SKILL.md` — financial calculation accuracy tests, reconciliation tests
- `.claude/skills/performance/SKILL.md` — batch job design, period-close query optimization
- `.claude/skills/production-readiness/SKILL.md`
- `.claude/skills/requirements-engineering/SKILL.md`
- `.claude/skills/devops/SKILL.md` — blue/green deployments that respect in-flight transactions

---

## Recommended stack options

| Stack | Rationale |
|---|---|
| **Java/Spring Boot + PostgreSQL + React** | Spring's transaction management and type system suit ledger correctness; mature ecosystem for ERP patterns (Hibernate, Spring Batch for period-close); Postgres serializable isolation for double-entry. See `.claude/stack-matrix/backend.md`. |
| **.NET / ASP.NET Core + SQL Server + React/Blazor** | Dominant in mid-market ERP; SQL Server's financial-grade features (row versioning, temporal tables); strong Windows-ecosystem integrations (Active Directory, Office). See `.claude/stack-matrix/backend.md`. |
| **Python/Django + PostgreSQL + Vue/Nuxt** | Faster iteration for SMB-scope ERP; Django ORM handles multi-tenant schemas; Celery for batch jobs; good for finance-first or service-ERP scope. See `.claude/stack-matrix/backend.md`. |
| **Node/NestJS + PostgreSQL + Next.js** | Full TypeScript stack; suitable for lightweight or vertical ERP where real-time collaboration matters; use Prisma with explicit transaction blocks for ledger writes. |

---

## Required checklists

- `.claude/checklists/security.md` — emphasize: period locking prevents back-dated entries, role separation (AP clerk cannot approve own invoices), immutable audit log, SOX-relevant access controls
- `.claude/checklists/qa.md` — financial calculation accuracy (decimal precision, rounding modes), trial-balance reconciliation tests
- `.claude/checklists/performance.md` — period-close batch must complete within acceptable window; GL query performance at full transaction history
- `.claude/checklists/accessibility.md`
- `.claude/checklists/production.md`
- `.claude/checklists/launch.md`

---

## MVP scope pattern

**In the first cut:**
- Chart of accounts and general ledger (double-entry, journal entries, trial balance)
- Accounts payable: vendor master, purchase invoices, payment scheduling
- Accounts receivable: customer master, sales invoices, receipt recording
- Basic inventory: item master, stock movements (goods-in / goods-out), on-hand balance
- Fixed report set: trial balance, aged AP, aged AR, inventory valuation summary
- User roles: admin, accountant, read-only viewer
- Period open/close with lock on closed periods
- CSV data import for opening balances and master data

**Deferred to later iterations:**
- Manufacturing module (BOM, production orders, MRP)
- HR/payroll module
- Multi-entity / multi-currency consolidation
- Three-way PO match automation
- Workflow approval engine (configurable approval chains)
- Bank feed integration and automated reconciliation
- Tax filing / e-invoicing connectors
- Custom report builder or BI embed
- Mobile app for approvals and expense capture
- Customer/vendor self-service portal

---

## Production risks

| Risk | Severity | Mitigation |
|---|---|---|
| Ledger imbalance — debits ≠ credits after a bug or crash | **P0** | Enforce double-entry constraint in DB transaction; nightly reconciliation job; alert on any imbalance immediately |
| Back-dated entry after period close corrupts financial statements | **P0** | Database-enforced period lock; closed periods are immutable; any correction requires a reversing journal entry in the open period |
| Data migration creates opening-balance errors | **P0** | Trial-balance comparison between legacy and new system before go-live; signed-off by controller; rollback plan to legacy system |
| Decimal precision errors in multi-currency or tax calculations | **P0** | Store monetary amounts as integers (minor currency units) or `NUMERIC(19,4)`; never use `float`; use a dedicated rounding library |
| Unauthorized access to payroll or financial data | **P0** | Segregation of duties enforced at API + DB level; no shared service accounts; all access logged |
| Batch period-close job times out or partially completes | **P1** | Idempotent batch steps with checkpoint/resume; run in off-peak window; alert on partial completion; never auto-retry destructively |
| Integration failure (bank feed, payment processor) causes silent data gap | **P1** | Each integration writes a reconciliation log; dead-letter queue for failed messages; daily gap-detection report |
| Schema migration locks tables during business hours | **P1** | Use online DDL (pg_repack / gh-ost); test migration duration on production-size data; schedule in maintenance window with rollback tested |
| Audit trail gaps make statutory audit non-compliant | **P2** | Append-only audit log for every write; store who, what, when, previous value; never allow UPDATE/DELETE on ledger rows |

---

## Launch requirements

- [ ] Trial balance ties out to legacy system (controller sign-off required)
- [ ] Period-lock mechanism tested: attempt to post to closed period returns rejection
- [ ] Double-entry constraint verified: automated test asserts zero imbalance after 10 k randomised transactions
- [ ] Decimal precision validated for all monetary calculations including tax and forex rounding
- [ ] Role segregation verified: AP clerk cannot approve own invoices; no cross-module privilege escalation
- [ ] Audit log verified: every write captured with user, timestamp, before/after values
- [ ] Batch period-close job tested at full production data volume; completion time documented
- [ ] Integration data reconciliation report runs and matches for all connected systems
- [ ] Database backup, point-in-time restore, and failover tested on staging
- [ ] Rollback plan to legacy system documented and agreed with stakeholders
- [ ] Security checklist `.claude/checklists/security.md` fully green
- [ ] Go-live window confirmed to avoid month-end close overlap

# Launch Checklist Instance
**What:** A filled-in, dated go/no-go checklist for a specific product or feature launch.  
**Who fills it in:** Release owner coordinates; each item gets an assigned owner and completion date.  
**Cross-references:** `.claude/templates/deployment-plan.md`, `.claude/templates/production-readiness.md`, `.claude/checklists/security.md`

---

## Launch Metadata

| Field | Value |
|-------|-------|
| Feature / product name | `<Payments v2 — Stripe integration>` |
| Launch date target | `<YYYY-MM-DD HH:MM UTC>` |
| Release owner | `<@name>` |
| Go/no-go decision time | `<YYYY-MM-DD HH:MM UTC — 1 hour before launch>` |
| Decision maker | `<CTO / Product lead / @name>` |
| Rollback owner | `<@sre-lead>` |

---

## Status Key
- ✅ Done
- ⏳ In progress
- ❌ Blocked / failed
- ➖ Not applicable to this launch

---

## A — Engineering & Code

| # | Item | Owner | Due | Status | Notes |
|---|------|-------|-----|--------|-------|
| A1 | Production-readiness review completed and approved | `<@eng-lead>` | `<T−2d>` | ☐ | Link: `<production-readiness.md>` |
| A2 | All P0/P1 bugs closed | `<@qa-lead>` | `<T−1d>` | ☐ | |
| A3 | Code merged to `main`, tagged `<v2.0.0>` | `<@eng-lead>` | `<T−4h>` | ☐ | |
| A4 | CI pipeline green on release tag | `<@devops>` | `<T−4h>` | ☐ | Link: `<CI run>` |
| A5 | Database migrations reviewed and tested in staging | `<@backend>` | `<T−2d>` | ☐ | |
| A6 | Secrets/env vars provisioned in production vault | `<@devops>` | `<T−1d>` | ☐ | |
| A7 | Third-party API keys / webhooks configured for prod | `<@backend>` | `<T−1d>` | ☐ | |

---

## B — Quality & Testing

| # | Item | Owner | Due | Status | Notes |
|---|------|-------|-----|--------|-------|
| B1 | Full regression test suite passed in staging | `<@qa-lead>` | `<T−2d>` | ☐ | Link: `<test report>` |
| B2 | Load/performance test at 2× expected peak | `<@sre>` | `<T−3d>` | ☐ | P95 < `<300 ms>` |
| B3 | Manual exploratory QA completed | `<@qa-lead>` | `<T−1d>` | ☐ | |
| B4 | Accessibility audit passed (user-facing only) | `<@frontend>` | `<T−3d>` | ☐ | WCAG 2.1 AA |
| B5 | Cross-browser / cross-device testing done | `<@qa-lead>` | `<T−2d>` | ☐ | |
| B6 | End-to-end payment flow tested with real Stripe test keys | `<@qa-lead>` | `<T−1d>` | ☐ | |

---

## C — Security

| # | Item | Owner | Due | Status | Notes |
|---|------|-------|-----|--------|-------|
| C1 | Security checklist completed | `<@security>` | `<T−3d>` | ☐ | Link: `.claude/checklists/security.md` |
| C2 | Dependency vulnerability scan clean | `<@security>` | `<T−1d>` | ☐ | |
| C3 | No secrets in source control (scan result) | `<@security>` | `<T−1d>` | ☐ | |
| C4 | PII handling reviewed and compliant | `<@security>` | `<T−3d>` | ☐ | |
| C5 | Penetration test / threat-model review done | `<@security>` | `<T−5d>` | ☐ | Or scheduled for 30 days post-launch |

---

## D — Infrastructure & Operations

| # | Item | Owner | Due | Status | Notes |
|---|------|-------|-----|--------|-------|
| D1 | Deployment plan written and reviewed | `<@devops>` | `<T−2d>` | ☐ | Link: `<deployment-plan.md>` |
| D2 | Staging deploy rehearsal completed | `<@devops>` | `<T−1d>` | ☐ | |
| D3 | Rollback procedure tested in staging | `<@devops>` | `<T−1d>` | ☐ | RTO: `<15 min>` |
| D4 | Auto-scaling and resource limits configured | `<@devops>` | `<T−2d>` | ☐ | |
| D5 | CDN / edge config updated (if applicable) | `<@devops>` | `<T−1d>` | ☐ | |
| D6 | DNS / SSL / domain changes ready | `<@devops>` | `<T−2d>` | ☐ | |
| D7 | Database backup taken immediately pre-launch | `<@devops>` | `<T−1h>` | ☐ | |

---

## E — Observability

| # | Item | Owner | Due | Status | Notes |
|---|------|-------|-----|--------|-------|
| E1 | Dashboards created and verified | `<@sre>` | `<T−2d>` | ☐ | Link: `<dashboard>` |
| E2 | Alerts configured with correct thresholds | `<@sre>` | `<T−2d>` | ☐ | Routes to `<#alerts>` |
| E3 | On-call rotation includes this service | `<@sre>` | `<T−1d>` | ☐ | Link: `<PagerDuty schedule>` |
| E4 | Runbook written for top failure scenarios | `<@sre>` | `<T−2d>` | ☐ | Link: `<runbook>` |
| E5 | Error tracking (Sentry / equivalent) receiving test events | `<@eng>` | `<T−1d>` | ☐ | |

---

## F — Product & Business

| # | Item | Owner | Due | Status | Notes |
|---|------|-------|-----|--------|-------|
| F1 | Product owner / stakeholder sign-off | `<@product>` | `<T−1d>` | ☐ | |
| F2 | Feature flags configured for gradual rollout | `<@eng>` | `<T−1d>` | ☐ | Start at `<10 %>` |
| F3 | Analytics / event tracking verified firing | `<@product>` | `<T−2d>` | ☐ | |
| F4 | A/B test or experiment configured (if applicable) | `<@product>` | `<T−2d>` | ☐ | |
| F5 | Pricing, billing, subscription logic verified end-to-end | `<@product>` | `<T−2d>` | ☐ | |

---

## G — Communications & Support

| # | Item | Owner | Due | Status | Notes |
|---|------|-------|-----|--------|-------|
| G1 | User-facing release notes / changelog drafted | `<@product>` | `<T−2d>` | ☐ | |
| G2 | Customer support team briefed | `<@cs-lead>` | `<T−1d>` | ☐ | |
| G3 | In-app / email announcement prepared | `<@marketing>` | `<T−1d>` | ☐ | Sends at `<T+1h>` |
| G4 | Status page updated (maintenance window if needed) | `<@sre>` | `<T−24h>` | ☐ | |
| G5 | Help documentation / FAQs published | `<@product>` | `<T>` | ☐ | |
| G6 | Social / press announcement scheduled (if applicable) | `<@marketing>` | `<T>` | ☐ | |

---

## Go / No-Go Decision

> Completed by the decision maker at the scheduled go/no-go time. Any unchecked item in sections A–E is grounds for NO-GO unless a documented waiver is in place.

| Section | All items ✅? | Waiver if not | Decision |
|---------|-------------|--------------|----------|
| A — Engineering | ☐ | | |
| B — Quality | ☐ | | |
| C — Security | ☐ | | |
| D — Infrastructure | ☐ | | |
| E — Observability | ☐ | | |
| F — Product | ☐ | | |
| G — Comms | ☐ | | |

**Final decision:** `<GO | NO-GO>`  
**Decision maker:** `<@name>`  
**Decision time:** `<YYYY-MM-DD HH:MM UTC>`  
**Reason if NO-GO:** `<specific blocking item(s)>`  
**New launch target (if NO-GO):** `<YYYY-MM-DD>`

---

## Post-Launch Monitoring Window

> Track status for the first 24 hours after launch.

| Time | Error rate | P95 latency | Key business metric | Notes |
|------|-----------|-------------|---------------------|-------|
| T+15 min | | | | |
| T+1 h | | | | |
| T+4 h | | | | |
| T+24 h | | | | |

**Launch declared stable:** `<YYYY-MM-DD HH:MM UTC>` by `<@name>`

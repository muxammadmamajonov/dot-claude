# Compliance Control Mapping

This maps the OS's existing gates, checklists, agents, and templates to control families in four
widely-required frameworks — **SOC 2**, **ISO/IEC 27001**, **SLSA**, and **OWASP** — so a team that
already runs this OS can see, at a glance, which of its compliance evidence already exists as a
byproduct of normal delivery, and which gaps are still theirs to close outside of code.

## Scope and disclaimer — read this first

**This is a control-mapping aid, not a certification, and not legal advice.** Copying `.claude/` into a
repo and passing its checklists does **not** make a project SOC 2 attested, ISO 27001 certified, or
OWASP-compliant. Certification and attestation require a real external auditor, a defined audit period,
and organizational controls this repository cannot see or enforce: HR/personnel security, physical
security, vendor and sub-processor due diligence, insurance, legal contracts, and management sign-off.
Treat every row below as "this artifact produces evidence relevant to this control" — never as "this
control is satisfied." Always confirm scope and interpretation with your own compliance lead, legal
counsel, and auditor before making a representation to a customer or regulator.

## How to use this map

1. Identify which framework(s) your compliance program targets (often more than one — SOC 2 and ISO
   27001 share the majority of their technical controls).
2. For each control family below, find the OS artifact that already produces relevant evidence, and
   confirm it is actually in your project's **active team** (`docs/state/active-team.md` — a dormant
   checklist produces no evidence).
3. Route every genuine gap to `.claude/checklists/privacy-compliance.md` (P0–P3) or a decision record —
   do not silently assume "not applicable."
4. Assemble your audit evidence package from the artifacts named in *Evidence chain* below, not from
   memory or after-the-fact reconstruction.

## SOC 2 (Trust Services Criteria)

| TSC criterion | OS artifact | What it covers | Still your responsibility |
|---|---|---|---|
| CC — Security (common criteria) | `.claude/checklists/security.md`, `.claude/agents/quality/security-auditor.md` | Access control, input validation, secure defaults, vulnerability management (P0–P3 tagged) | Employee background checks, security awareness training, physical facility controls |
| CC — Change management | `.claude/commands/refactor-safely.md`, decision records, `.claude/checklists/release-rollback.md` | Reviewed, reversible, documented changes with a rollback path | A formal change-advisory process/approval workflow if your auditor requires one |
| A — Availability | `.claude/agents/quality/reliability-engineer.md`, `.claude/checklists/observability.md`, `.claude/templates/slo-sla.md` | SLOs/SLIs, alerting, incident runbooks, tested backup/restore | Actual uptime track record; DR test execution and evidence retention |
| PI — Processing integrity | `.claude/checklists/qa.md`, `.claude/agents/quality/qa-engineer.md`, `.claude/agents/quality/test-automation-engineer.md` | Test coverage, acceptance verification, error handling | Business-rule sign-off from process owners (`.claude/templates/business-rules.md`) |
| C — Confidentiality | `.claude/checklists/security.md` (secrets handling), `.claude/CLAUDE.md` §8 | Secrets never exposed/committed; least-privilege access | Data classification policy; NDAs and contractual confidentiality terms |
| P — Privacy | `.claude/agents/quality/privacy-compliance-auditor.md`, `.claude/checklists/privacy-compliance.md` | Data inventory, minimization, retention/deletion, consent, DSAR flow | Published privacy notice; a named Data Protection Officer where required |

## ISO/IEC 27001:2022 (Annex A themes)

| Annex A theme | OS artifact | Coverage | Gap this OS cannot close |
|---|---|---|---|
| Organizational controls (A.5) | `.claude/templates/decision-record.md`, `.claude/templates/assumptions-log.md`, CODEOWNERS | Documented decisions, ownership, review routing | ISMS policy documents, risk register, management review cadence |
| People controls (A.6) | — | — | Screening, employment terms, disciplinary process, security training program |
| Physical controls (A.7) | — | — | Entirely outside code-repository scope |
| Technological controls (A.8) | `.claude/checklists/security.md`, `.claude/checklists/dependencies.md`, `.claude/agents/quality/security-auditor.md`, `.claude/docs/HOOKS_SAFETY_MODEL.md` | Access control, malware/dependency scanning, secure configuration, logging, secrets management, secure development lifecycle (this OS's whole 9-stage flow is, itself, A.8.25–A.8.29 evidence) | Endpoint management, network hardware controls, cryptographic key custody outside the app layer |

## SLSA (Supply-chain Levels for Software Artifacts)

`.claude/checklists/dependencies.md` already carries an explicit SLSA ladder — this section is a pointer,
not a duplicate.

| SLSA level | OS artifact | What it requires |
|---|---|---|
| Level 1 — Provenance exists | `.claude/checklists/dependencies.md` P1 | Build provenance metadata generated and attached to release artifacts |
| Level 2 — Hosted build, signed provenance | `.claude/checklists/dependencies.md` P2 | Hosted CI (e.g. GitHub Actions + `slsa-github-generator`), tamper-evident provenance |
| Level 3 — Hardened builds | `.claude/checklists/dependencies.md` P2–P3 | Non-falsifiable provenance, isolated/hermetic builds (P3) |
| Source/dependency integrity | `.claude/checklists/dependencies.md` P0 | Lockfiles committed, SCA scan clean of Critical/High, pinned versions, signed images (cosign/Sigstore) |

## OWASP (ASVS + Top 10)

| OWASP artifact | OS artifact | Coverage |
|---|---|---|
| Top 10 (2021), broadly | `.claude/checklists/security.md`, `.claude/agents/quality/security-auditor.md` | Each Top-10 category (broken access control, cryptographic failures, injection, insecure design, …) has a corresponding P0/P1 checklist line; the security-auditor agent audits against it before every merge touching auth/session/upload/payment/external-data surfaces |
| ASVS V1 (architecture) | `.claude/templates/threat-model.md`, `.claude/commands/threat-model.md` | STRIDE threat modeling before build, re-run on major architecture change |
| ASVS V2–V4 (auth, session, access control) | `.claude/agents/quality/auth-permission-reviewer.md`, `.claude/checklists/security.md` | Auth/session/authorization-specific review, invoked on any auth-touching change |
| ASVS V5 (validation/encoding) | `.claude/checklists/security.md`, `.claude/checklists/qa.md` | Input validation and output encoding line items |
| ASVS V10 (malicious code) | `.claude/checklists/dependencies.md`, `.claude/hooks/package-install-guard.json` (opt-in) | SCA scanning, blocked remote pipe-to-shell installs |
| ASVS V14 (configuration) | `.claude/settings.json`, `.claude/docs/HOOKS_SAFETY_MODEL.md` | Secure-by-default permission baseline, secrets never in config |

Pick an **ASVS level** (1 = opportunistic, 2 = standard, 3 = advanced/high-value) deliberately per project
risk tier in `docs/state/project-type.md` — this OS does not default one for you.

## Assembling an audit evidence package

An auditor wants artifacts, not assertions. The evidence chain this OS produces, in the order an auditor
typically wants to see it:

1. `docs/state/project-type.md` — risk classification and why it was set.
2. `docs/decisions/*` (`.claude/templates/decision-record.md`) — every non-obvious control decision, with alternatives considered.
3. `docs/state/assumptions.md` — what was assumed and by whom, so nothing is silently undocumented.
4. Checklist run history — a dated pass/fail record per gate (security, QA, performance, accessibility, privacy-compliance), not just the checklist file itself.
5. `docs/production-readiness.md` (`.claude/templates/production-readiness.md`) and `.claude/templates/headless-audit-report.md` for CI-run evidence — never fabricated; every audit agent in this OS is lint-enforced (`.claude/scripts/validate.py`) to carry a no-fabrication clause.
6. `.claude/templates/runbook.md` and `.claude/templates/incident-postmortem.md` — operational maturity evidence for availability/incident-response criteria.

## What this does NOT cover

Legal contracts and DPAs; HR policy and background checks; physical/facility security; vendor and
sub-processor risk assessments; cyber insurance; a real penetration test or external audit engagement;
business continuity plan testing cadence; and any representation of compliance status made to a customer,
partner, or regulator. Those require your own compliance, legal, and security leadership — this document
only prevents you from having to rediscover, from scratch, which of your engineering artifacts already
double as evidence.

## Related

`.claude/checklists/security.md`, `.claude/checklists/privacy-compliance.md`, `.claude/checklists/dependencies.md`,
`.claude/agents/quality/privacy-compliance-auditor.md`, `.claude/agents/quality/security-auditor.md`,
`.claude/templates/threat-model.md`, `.claude/commands/threat-model.md`, `.claude/commands/audit-security.md`,
`CONTRIBUTING.md` (governance process), `.github/CODEOWNERS` (who owns compliance-sensitive paths).

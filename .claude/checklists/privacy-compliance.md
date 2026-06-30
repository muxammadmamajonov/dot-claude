# Privacy & Compliance Checklist

Gate for data privacy and regulatory requirements: GDPR, CCPA, HIPAA, PCI-DSS, consent, data subject rights, retention, DPA, data residency, and PII inventory.

## P0 — Blockers (must pass before launch)

- [ ] PII inventory is complete: every field, table, log line, and queue message containing personal data is catalogued with its legal basis for processing (GDPR Art. 6/9).
- [ ] Privacy policy is live and accurately describes data collection, use, sharing, and retention; version-controlled and timestamped.
- [ ] Explicit, granular consent is obtained before collecting non-essential personal data; consent records (timestamp, version, channel) are stored and auditable.
- [ ] Cookie/tracking consent banner meets GDPR/ePrivacy requirements: no analytics or ad pixels fire before opt-in; banner cannot be pre-ticked.
- [ ] Data minimisation enforced: no field is collected that is not required for a stated, lawful purpose; verified with schema audit.
- [ ] Sensitive data categories (health, financial, biometric, race, religion, children) identified and subject to elevated controls (encryption at rest + in transit, restricted access, separate legal basis).
- [ ] Data subject rights flows are implemented and tested: access, rectification, erasure (right to be forgotten), restriction, portability, and objection — all completable within 30 days.
- [ ] Data retention schedules defined per data class; automated deletion or anonymisation jobs exist and have been tested end-to-end.
- [ ] All third-party processors are covered by a signed Data Processing Agreement (DPA) or equivalent; list of sub-processors disclosed.
- [ ] Data residency requirements met: personal data stored and processed only in legally permitted regions; transfer mechanisms (SCCs, adequacy decisions) documented for cross-border flows.
- [ ] HIPAA: if PHI is handled — Business Associate Agreements (BAAs) signed with all vendors touching PHI; minimum-necessary access enforced; audit logs for PHI access retained ≥ 6 years.
- [ ] PCI-DSS: if payment card data is handled — scope is minimised (tokenisation/vaulting via certified provider); SAQ or QSA assessment completed; no raw PANs stored in logs or databases.
- [ ] Children's data (COPPA / GDPR Art. 8): age gate or parental consent in place if service may collect data from users under 13 (US) / 16 (EU).
- [ ] Data breach notification procedure documented: detection → internal escalation → supervisory authority (≤ 72 h GDPR) → affected individuals — tested with a tabletop drill.

## P1 — Important (address soon after launch)

- [ ] Privacy-by-design review completed for every new feature that touches personal data before development starts (DPIA for high-risk processing).
- [ ] DPIA (Data Protection Impact Assessment) filed for high-risk processing activities (profiling, large-scale special category data, systematic monitoring).
- [ ] Data Protection Officer (DPO) appointed and contact published if required under GDPR Art. 37; role and responsibilities documented.
- [ ] All internal teams with access to production PII are trained on data handling policies; training completion tracked annually.
- [ ] Vendor/third-party risk assessments completed and scored; re-assessment cadence defined (annual minimum for critical processors).
- [ ] Anonymisation and pseudonymisation techniques validated: k-anonymity, differential privacy, or equivalent applied to analytics and reporting datasets; re-identification risk assessed.
- [ ] CCPA compliance if serving California residents: privacy notice at collection, "Do Not Sell or Share My Personal Information" opt-out link present, and honored within 15 business days.
- [ ] Opt-out signals (Global Privacy Control / GPC) are detected and respected automatically in all data flows.
- [ ] Records of Processing Activities (RoPA) maintained and current (GDPR Art. 30).
- [ ] Privacy is **built, not just audited**: consent capture, data-subject-access/erasure (DSAR), and retention/deletion pipelines are implemented up front as engineering work — owned by `data-engineer` / `backend-engineer` from the spec stage — not bolted on at the audit gate. This checklist verifies that work; it does not replace it.

## P2 — Hardening

- [ ] Automated PII scanning runs in CI/CD to detect accidental inclusion of personal data in logs, error messages, test fixtures, or version control.
- [ ] Data lineage tracked from collection to deletion; visualised for auditor review.
- [ ] Encryption key management audited: keys rotated on schedule, HSM or KMS used, no keys in source code or environment variable plain text.
- [ ] Access to personal data is role-based, least-privilege, and reviewed quarterly; privileged access requires MFA and is fully logged.
- [ ] Anonymised or synthetic data used in all non-production environments; production data copy to dev/staging prohibited.

## P3 — Post-launch / backlog

- [ ] Annual third-party privacy audit or penetration test with a privacy focus scheduled.
- [ ] Automated DSAR (Data Subject Access Request) portal reduces manual effort and risk of error.
- [ ] Privacy maturity model (e.g. NIST Privacy Framework, ISO 29100) self-assessment completed; gaps tracked as roadmap items.
- [ ] Consent management platform (CMP) integrated for multi-jurisdiction consent lifecycle management.

## How to use

**Shift left — privacy is built, not just checked here.** Treat this as a verification gate, not the moment privacy work begins. Consent capture, data-subject-access/erasure (DSAR) flows, and retention/deletion pipelines are implementation work the `data-engineer` and `backend-engineer` own from the spec and build stages (§2/§4) — designed in up front, not retrofitted under audit pressure. A control that does not exist in the codebase cannot be made compliant by a checklist; this checklist confirms the engineering was done.

Run this checklist via the `audit-security` command or the `privacy-compliance-auditor` agent before any production launch and after any material change to data collection, processing, or sharing. P0 items block launch sign-off. Assign each item an owner; record evidence links in the adjacent `docs/compliance/` folder.

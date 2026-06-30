# Healthtech Preset

## Project type

Software products built for healthcare delivery, clinical workflows, patient engagement, or health data management. Common variants:

- **Patient-facing app / digital health** — symptom checkers, chronic disease management, mental wellness, medication reminders, remote patient monitoring.
- **Clinical decision support (CDS)** — evidence-based alerts, dosage calculators, differential-diagnosis tools embedded into EHR workflows.
- **Electronic health record (EHR) / EMR** — longitudinal patient records, encounter notes, problem lists, medication lists, lab results; often HL7 FHIR-based.
- **Telemedicine / virtual care platform** — video consults, async messaging, e-prescribing, asynchronous triage.
- **Health data platform / HIE** — aggregating patient data across providers via FHIR APIs; population health analytics; care coordination.
- **Medical device software (SaMD)** — software that qualifies as a medical device (FDA 21 CFR Part 11, EU MDR, IEC 62304); diagnostic or therapeutic function.
- **Hospital operations / scheduling** — bed management, OR scheduling, staff rostering, supply chain.
- **Pharma / life sciences** — clinical trial management, pharmacovigilance, regulatory submissions.
- **Payer / benefits platform** — eligibility verification, claims adjudication, prior authorisation, member portals.

## Typical use cases

- Chronic disease management app (diabetes, hypertension, COPD) with connected device readings and care-team messaging.
- Mental health platform with therapist matching, video sessions, and progress tracking.
- Telemedicine service allowing patients to see a clinician in under 15 minutes.
- FHIR-based patient portal aggregating records from multiple health systems.
- Clinical trial recruitment and ePRO (electronic patient-reported outcomes) platform.
- Care coordination tool for case managers tracking high-risk patients across settings.
- Revenue cycle management tool for small practices handling claims, coding, and collections.

## Required discovery questions

1. Does the product create, transmit, store, or process Protected Health Information (PHI)? If so, what HIPAA compliance programme (BAA, safeguards, audit controls) and which jurisdictions (US HIPAA, EU GDPR Article 9, Canada PIPEDA, UK NHS Data Security)?
2. Is the software a regulated medical device (FDA SaMD, EU MDR Class I/IIa/IIb/III, IEC 62304)? If yes, what classification path and regulatory strategy has been chosen, and who owns the quality management system?
3. What interoperability standards are required? (HL7 FHIR R4/R5 API, HL7 v2 interfaces, DICOM for imaging, SMART on FHIR for EHR launch, C-CDA document exchange.)
4. Who are the users? (Patients / consumers, licensed clinicians, care coordinators, administrators, payers.) What licensing or credentialing constraints apply to the provider-facing workflows?
5. What EHR or health information system must the product integrate with, and via what mechanism? (Epic App Orchard, Cerner open.epic, Athena API, standalone FHIR server, custom HL7 v2 interface engine.)
6. What is the consent and data-sharing model? (Patient consent for each data use, break-glass access for emergencies, research de-identification pipeline, opt-in vs. opt-out for analytics.)
7. What clinical safety obligations apply? (Clinical risk management per DCB0129/0160 in the UK, IEC 82304-1, adverse event reporting obligations, clinical governance process.)
8. What are the availability and disaster-recovery requirements? (Clinical systems often require 99.9 %+ uptime; RTO/RPO that supports patient safety; maintenance window constraints.)
9. What payment and billing model is in scope? (Insurance reimbursement and CPT codes, self-pay with FSA/HSA card support, employer benefits sponsor, subscription B2B.) Does the product touch insurance claims or prior-auth workflows?
10. Who will operate the product long-term, and what clinical oversight model ensures safety after launch? (Medical director, clinical advisory board, post-market surveillance process.)

## Recommended agents

**Core**
- `.claude/agents/core/orchestrator.md` — flow control, compliance gate enforcement.
- `.claude/agents/core/product-manager.md` — clinical workflow scope, regulatory milestone planning.
- `.claude/agents/core/solution-architect.md` — FHIR data architecture, PHI boundary design, integration strategy.
- `.claude/agents/core/requirements-engineer.md` — clinical safety requirements, consent flows, audit trail invariants.

**Engineering**
- `.claude/agents/engineering/backend-engineer.md` — FHIR API server, HL7 interface engine, PHI encryption, audit log.
- `.claude/agents/engineering/frontend-engineer.md` — accessible patient-facing UI, clinician dashboard, SMART app launch.
- `.claude/agents/engineering/mobile-engineer.md` — iOS/Android patient app with offline capability and biometric auth.
- `.claude/agents/engineering/data-engineer.md` — de-identification pipelines, population health analytics, claims data ingestion.
- `.claude/agents/engineering/devops-engineer.md` — HIPAA-eligible cloud infrastructure, PHI access logging, disaster recovery.
- `.claude/agents/engineering/realtime-engineer.md` — telemedicine video (WebRTC), real-time vitals streaming, care-team alerts.

**Quality**
- `.claude/agents/quality/security-auditor.md` — HIPAA Security Rule technical safeguards, PHI at-rest and in-transit encryption, access control, breach risk.
- `.claude/agents/quality/privacy-compliance-auditor.md` — HIPAA Privacy Rule, GDPR Article 9, consent management, data-retention schedules, breach notification.
- `.claude/agents/quality/qa-engineer.md` — clinical workflow edge cases, medication safety checks, data integrity across HL7 transforms.
- `.claude/agents/quality/accessibility-auditor.md` — WCAG 2.1 AA for patient-facing apps; ADA / Section 508 where applicable.
- `.claude/agents/quality/reliability-engineer.md` — high-availability for clinical systems, RTO/RPO validation, fail-safe behaviour.
- `.claude/agents/quality/production-readiness-auditor.md` — clinical incident runbooks, PHI audit trail completeness, SLA against patient-safety needs.

**Domain**
- `.claude/agents/domain/healthtech-domain-expert.md` — HIPAA/HITECH, FHIR, HL7 v2, clinical terminology (SNOMED, LOINC, ICD-10, RxNorm), SaMD regulatory pathway.

## Recommended skills

- `.claude/skills/backend/SKILL.md` — FHIR RESTful API, HL7 v2 parsing, PHI boundary enforcement, audit logging.
- `.claude/skills/security/SKILL.md` — PHI encryption at rest and in transit, HIPAA Security Rule controls, secrets management.
- `.claude/skills/data-modeling/SKILL.md` — FHIR resource mapping, clinical terminology binding, longitudinal patient record schema.
- `.claude/skills/api-design/SKILL.md` — SMART on FHIR OAuth2 scopes, FHIR search parameters, bulk FHIR export ($export).
- `.claude/skills/devops/SKILL.md` — HIPAA-eligible cloud regions, VPC isolation, PHI access log pipeline, DR automation.
- `.claude/skills/testing/SKILL.md` — FHIR conformance tests, HL7 transform validation, consent-enforcement test suite.
- `.claude/skills/production-readiness/SKILL.md` — clinical SLA monitoring, PHI breach-detection alerts, on-call runbooks.
- `.claude/skills/mobile/SKILL.md` — offline-first patient app, biometric auth, HealthKit/Google Health Connect integration.

## Recommended stack options

| Stack | Rationale |
|-------|-----------|
| **Node.js / TypeScript + HAPI FHIR Server + PostgreSQL + AWS GovCloud / HIPAA-eligible** | HAPI FHIR is the most mature open-source FHIR R4/R5 server; Node backend handles SMART on FHIR OAuth2; Postgres stores clinical data with row-level security; AWS provides HIPAA BAA and a full suite of HIPAA-eligible services. See `.claude/stack-matrix/backend.md`, `.claude/stack-matrix/cloud-devops.md`. |
| **Java / Kotlin (Spring Boot) + HAPI FHIR + PostgreSQL + Azure Health Data Services** | JVM ecosystem has the broadest HL7/FHIR library support; Azure Health Data Services provides a managed FHIR server, DICOM service, and MedTech IoT connector with built-in HIPAA controls. |
| **Python (FastAPI/Django) + PostgreSQL + GCP Healthcare API** | Suits data-heavy or ML-adjacent healthtech (predictive risk, NLP on clinical notes); GCP Healthcare API manages FHIR and DICOM at scale; BigQuery for population analytics. See `.claude/stack-matrix/ai-ml.md`. |
| **React Native + Node.js backend + FHIR + AWS** | Mobile-first patient engagement apps requiring iOS and Android from a single codebase; HealthKit / Google Health Connect integration; AWS HIPAA-eligible infrastructure. See `.claude/stack-matrix/mobile.md`. |

## Required checklists

- `.claude/checklists/security.md` — extend with: PHI encrypted at rest (AES-256) and in transit (TLS 1.2+); access to PHI restricted by role with audit log on every read/write; BAA signed with all cloud and third-party vendors who may touch PHI; automatic session timeout for clinician-facing sessions; vulnerability scan before go-live.
- `.claude/checklists/qa.md` — extend with: FHIR resource validation against published StructureDefinitions; HL7 v2 round-trip fidelity tested; consent revocation propagates correctly to all data consumers; medication safety calculations tested with boundary values; de-identification verified against HIPAA Safe Harbor or Expert Determination standard.
- `.claude/checklists/production.md` — extend with: PHI access audit log is immutable and queryable for breach investigation; breach detection alert fires within 24 hours of anomalous access; RTO/RPO tested and meets patient-safety SLA; disaster recovery runbook reviewed by clinical operations team.
- `.claude/checklists/accessibility.md` — extend with: patient-facing interfaces meet WCAG 2.1 AA; keyboard navigation covers all critical clinical workflows; colour is never the sole means of conveying clinical status (e.g. critical lab values).

## MVP scope pattern

**In the first cut:**
- Single-use-case clinical workflow (e.g. telemedicine consult, chronic disease check-in, or appointment scheduling) — not the entire care continuum.
- PHI stored only in HIPAA-eligible cloud services; BAAs in place for all vendors before storing any real PHI.
- Role-based access: patient, clinician, and admin roles with least-privilege enforcement.
- Full audit trail from day one: every PHI read, write, and share logged with actor, timestamp, resource ID, and access reason.
- FHIR R4 as the internal data model even if external integration comes later — avoids a costly re-model.
- Consent capture and storage before any PHI is collected; granular consent for data sharing.
- Encrypted backups with a tested restore procedure before handling real patient data.
- Basic breach response runbook documented and assigned to a named owner before launch.

**Deferred to later:**
- EHR integration via Epic/Cerner (complex certification process; negotiate early, build later).
- HL7 v2 interface engine for legacy systems (high effort; validate demand first).
- FHIR bulk export for population analytics ($export operation).
- AI/ML clinical decision support (requires separate clinical validation, IRB considerations, and potentially SaMD classification).
- Multi-provider / multi-organisation tenancy.
- Insurance billing and claims submission (requires payer contracts and clearinghouse integration).
- SaMD regulatory submission (FDA 510(k), De Novo, PMA) — begin quality management system early; submission deferred until clinical evidence is gathered.
- DICOM viewer and medical imaging workflow.

## Production risks

| Risk | Priority | Notes |
|------|----------|-------|
| PHI breach triggering HIPAA breach notification (60-day clock) and regulatory fine | P0 | Encryption at rest and in transit; access restricted by role; audit log immutable; breach-detection alert active before any real PHI is stored. |
| Unauthorized PHI access or insider misuse | P0 | Row-level security on all PHI tables; audit every access; automatic anomaly alert on bulk reads; privileged access requires MFA + justification. |
| SaMD deployed without FDA/regulatory clearance — enforcement action | P0 | Classify software early; if SaMD, do not launch commercially without required clearance or a documented exemption confirmed by regulatory counsel. |
| Patient safety incident due to incorrect clinical data or calculation | P0 | Clinical logic reviewed by a licensed clinician before deployment; safety-critical calculations (dosing, allergy checks) have independent test verification; post-market surveillance process defined. |
| BAA not signed with a vendor who processes PHI — HIPAA violation | P0 | Vendor inventory maintained; BAA required before any vendor integration is enabled in production; legal review of all BAAs. |
| Data integrity loss during HL7/FHIR transform — wrong data presented to clinician | P1 | Round-trip tests for every HL7/FHIR mapping; validation against published profiles; alert on mapping failures. |
| Consent not captured before PHI collection — HIPAA Privacy Rule violation | P1 | Consent gate enforced in application code; automated test verifies PHI cannot be stored without a consent record. |
| RTO/RPO breach during an outage affecting active patient care | P1 | DR runbook tested with timed restore; clinical operations team knows the manual fallback procedure; on-call escalation path defined. |
| EHR integration downtime causing data sync gaps | P1 | Async integration with retry queue; stale-data indicator shown to clinicians; reconciliation job fills gaps when connectivity restores. |
| Accessibility failure locks out patients with disabilities | P2 | WCAG 2.1 AA automated and manual test before launch; assistive-technology smoke test on critical flows (booking, medication review). |
| Third-party analytics SDK exfiltrating PHI | P2 | No third-party analytics SDK may receive PHI; review all SDK data-collection settings; use HIPAA-eligible analytics (e.g. server-side events only). |

## Launch requirements

- BAA signed with every cloud provider and SaaS vendor that touches PHI before any real patient data enters the system.
- PHI encryption at rest (AES-256 minimum) and in transit (TLS 1.2+) verified by a security scan.
- Audit log active and immutable; tested by attempting a direct database UPDATE on an audit record (must fail).
- Role-based access controls tested: patient cannot access other patients' records; clinician access limited to their assigned patients; admin cannot view clinical notes without clinical role.
- Consent flow tested end-to-end: PHI storage blocked if consent record is absent.
- Breach response runbook documented, assigned, and signed off by a data-protection officer or legal counsel.
- Disaster recovery drill completed: restore from backup within documented RTO; data integrity verified post-restore.
- Clinical safety review completed by a licensed clinician for any safety-critical workflow before launch.
- Privacy policy, terms of service, and HIPAA Notice of Privacy Practices live and accessible from the app.
- Accessibility smoke test passed on all patient-facing critical paths (WCAG 2.1 AA minimum).
- Error monitoring and PHI-access anomaly alerting active; on-call rotation with escalation path defined.

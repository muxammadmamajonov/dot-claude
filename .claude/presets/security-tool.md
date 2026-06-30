# Security Tool Preset

## Project type
A software product whose primary value is protecting systems, code, data, or users from threats. Variants include:

- **SAST / SCA** — static code analysis, dependency vulnerability scanning (e.g., Semgrep, Snyk, Trivy)
- **DAST / IAST** — dynamic/interactive runtime scanning (e.g., OWASP ZAP, Burp Suite-style tools)
- **Secrets detection** — credential scanning in repos, CI pipelines, cloud configs (e.g., TruffleHog, GitGuardian)
- **EDR / Host security** — endpoint detection & response, process monitoring, kernel-level agents
- **SIEM / Log analytics** — event correlation, threat hunting, alert triage
- **Pentest tooling** — authorized offensive tools for red-team / bug-bounty workflows
- **Vulnerability management** — asset inventory + CVE correlation + remediation tracking
- **Cloud security posture** — CSPM, misconfiguration detection, IaC policy enforcement
- **Network security** — IDS/IPS, packet inspection, zero-trust proxies
- **Identity / PAM** — privileged-access management, anomaly detection in auth flows

## Typical use cases
- Developer-facing scanner integrated into CI/CD to gate PRs on vulnerability findings
- Enterprise SIEM ingesting multi-source logs for SOC alert triage
- SaaS secrets scanner monitoring org-wide commits and cloud credentials
- On-premise EDR agent deployed fleet-wide by security operations team
- CLI pentest tool used by authorized red teams on in-scope targets only
- IaC policy enforcer blocking insecure Terraform/CloudFormation before deploy
- Vulnerability management dashboard for CISO reporting and remediation SLAs

## Required discovery questions
1. What attack surface does this tool target — code, runtime, network, identity, cloud config, or combination?
2. Who are the primary users — developers (shift-left), SOC analysts, red-teamers, or automated pipeline agents?
3. What is the acceptable false-positive rate, and what escalation path handles disputed findings?
4. How are findings/exploit payloads stored and transmitted — and what access controls govern that data?
5. Does the tool execute active probes/exploits or only observe/analyze passively? If active, what authorization proof is required from the target owner?
6. What compliance frameworks must findings map to (CVSSv3, CWE, OWASP Top 10, NVD, MITRE ATT&CK, SOC 2, PCI-DSS)?
7. What is the expected scale — lines of code, events/second, endpoints, or repositories per scan?
8. How are detection rules/signatures updated, and who controls the update pipeline (to prevent supply-chain poisoning)?
9. What responsible-disclosure and coordinated-vulnerability-disclosure (CVD) policy applies to findings the tool itself uncovers?
10. Are there export-control or regulatory constraints on distributing offensive-capable modules (EAR, Wassenaar)?

## Recommended agents

**Core:**
- `.claude/agents/core/product-manager.md`
- `.claude/agents/core/solution-architect.md`
- `.claude/agents/core/technical-lead.md`
- `.claude/agents/core/requirements-engineer.md`

**Engineering:**
- `.claude/agents/engineering/backend-engineer.md`
- `.claude/agents/engineering/api-architect.md`
- `.claude/agents/engineering/devops-engineer.md`
- `.claude/agents/engineering/integration-engineer.md`

**Quality:**
- `.claude/agents/quality/security-auditor.md`
- `.claude/agents/quality/qa-engineer.md`
- `.claude/agents/quality/performance-engineer.md`
- `.claude/agents/quality/privacy-compliance-auditor.md`
- `.claude/agents/quality/production-readiness-auditor.md`

**Domain:**
- `.claude/agents/domain/security-tooling-domain-expert.md`
- `.claude/agents/domain/devtools-platform-domain-expert.md`

## Recommended skills

- `.claude/skills/security/SKILL.md` — threat modeling, OWASP, CVE handling
- `.claude/skills/backend/SKILL.md` — rule engine, analysis pipeline
- `.claude/skills/api-design/SKILL.md` — findings API, webhook integrations
- `.claude/skills/testing/SKILL.md` — unit + integration tests for detection logic
- `.claude/skills/performance/SKILL.md` — scan throughput, latency budgets
- `.claude/skills/devops/SKILL.md` — CI/CD integration, agent deployment
- `.claude/skills/observability/SKILL.md` — detection metrics, alert pipelines
- `.claude/skills/data-platform/SKILL.md` — log ingestion, event correlation (SIEM variant)

## Recommended stack options

| Option | Stack | Rationale |
|--------|-------|-----------|
| **Go engine** | Go + gRPC + PostgreSQL + Redis | High-throughput scanning, single binary deployment, ideal for CLI/agent tools |
| **Python analysis** | Python + FastAPI + Celery + PostgreSQL | Rich security library ecosystem (bandit, semgrep-python, pycryptodome); best for SAST/SCA |
| **JVM (enterprise)** | Java/Kotlin + Spring Boot + Kafka + Elasticsearch | Enterprise SIEM integration, mature CVE libraries, Elasticsearch for log search |
| **Rust engine** | Rust + Axum + RocksDB | Zero-overhead parsing of untrusted input (binary analysis, network traffic); memory safety for exploit handling |

See `.claude/stack-matrix/backend.md` and `.claude/stack-matrix/monitoring.md`.

## Required checklists

- `.claude/checklists/security.md` — mandatory; the tool's own security posture
- `.claude/checklists/privacy-compliance.md` — handling of vulnerability data, PII in logs
- `.claude/checklists/api.md` — findings API, rate limiting, auth
- `.claude/checklists/performance.md` — scan throughput SLOs
- `.claude/checklists/production.md`
- `.claude/checklists/observability.md` — detection rate, FP/FN dashboards
- `.claude/checklists/dependencies.md` — no malicious transitive deps in a security tool
- `.claude/checklists/release-rollback.md` — rolling back a broken rule update safely
- `.claude/checklists/launch.md`

## MVP scope pattern

**In MVP:**
- Core detection engine for one attack class (e.g., SAST for SQL injection + XSS)
- Finding output: severity, CWE ID, file+line, remediation guidance
- CLI entrypoint with exit-code policy (fail-on-high)
- JSON/SARIF output for CI integration
- Basic authentication on findings API
- Severity classification aligned to CVSSv3
- False-positive suppression (inline comment or config file)
- Audit log of who ran scans and on what targets

**Deferred:**
- Full OWASP Top 10 coverage
- IDE plugin / real-time scanning
- Multi-tenant SaaS findings dashboard
- Ticket-system integrations (Jira, GitHub Issues)
- Auto-remediation / PR fix suggestions
- MITRE ATT&CK mapping
- Custom rule authoring UI

## Production risks

| Risk | Tag | Mitigation |
|------|-----|------------|
| False negatives: critical vulns missed | P0 | Benchmark against known-vulnerable corpora (NIST Juliet, OWASP WebGoat); publish detection rates |
| Exploit payloads stored in DB leaked | P0 | Encrypt at rest with envelope encryption; restrict access to findings DB; redact from logs |
| Tool used offensively against unauthorized targets | P0 | Require signed authorization token/scope from target owner; no unauthenticated active probes |
| Supply-chain attack on rule update channel | P0 | Sign rule bundles (sigstore/cosign); verify signature before load; pin rule bundle hashes in CI |
| High false-positive rate causes alert fatigue | P1 | Track FP rate per rule; auto-suppress rules exceeding FP threshold; tuning feedback loop |
| Scan causes service disruption (DAST/active) | P1 | Rate-limit probe frequency; honor robots.txt / exclusion list; time-bounded scan windows |
| CVE data staleness | P1 | Daily NVD/OSV feed sync; alert on feed lag > 24 h |
| Scan process executes attacker-controlled code | P1 | Sandbox analysis in gVisor/Firecracker; no network access from analysis worker |
| Export-control violation for offensive modules | P2 | Legal review before distributing exploit PoC code; geo-block restricted jurisdictions |
| Findings data subject to data-residency laws | P2 | Per-region deployment option; data-residency controls documented |
| Responsible disclosure gap (tool finds 0-day) | P2 | Written CVD policy; 90-day disclosure timeline; vendor notification workflow built in |

## Launch requirements

1. **Detection benchmark published** — precision and recall against at least one public vulnerable-app corpus.
2. **Responsible-use policy** — documented, linked from README; pentest/active modules require authorization proof.
3. **CVD policy** — responsible disclosure page live before public release.
4. **Findings encryption** — all stored findings encrypted at rest and in transit (TLS 1.2+).
5. **Authorization enforcement** — active-probe modules reject requests without a valid target-owner authorization token.
6. **Audit trail** — immutable log of scan targets, timestamps, initiating user/token.
7. **False-positive rate ≤ 5%** (or tool-class-appropriate threshold) verified on benchmark set.
8. **Supply-chain verification** — rule bundles signed; CI enforces signature check.
9. **Dependency audit clean** — no known-high CVEs in tool's own dependencies at ship time.
10. **Legal review complete** — export-control analysis for any offensive-capable modules.

# Dependencies Checklist

Supply-chain and dependency hygiene gate: SCA, lockfiles, pinned versions, SBOM, license compliance, no abandoned or vulnerable packages, provenance attestation (SLSA), and update policy.

## P0 — Blockers (must pass before proceeding/launch)

- [ ] All direct and transitive dependencies are locked via a committed lockfile (`package-lock.json`, `Pipfile.lock`, `go.sum`, `Cargo.lock`, `Gemfile.lock`, `poetry.lock`, etc.) and the lockfile is not in `.gitignore`.
- [ ] SCA scan (Snyk, OWASP Dependency-Check, `npm audit`, `pip-audit`, `trivy fs`, or equivalent) shows **zero Critical or High CVEs** in direct dependencies.
- [ ] No dependency has a known actively-exploited vulnerability (CISA KEV catalogue cross-reference or equivalent feed).
- [ ] All production dependencies specify a pinned version range; wildcard (`*`) or unbounded (`>=`) constraints are forbidden in lock-free manifests.
- [ ] No dependency is end-of-life or unmaintained (last commit > 18 months AND no stated successor project); verify via `deps.dev`, `endoflife.date`, or equivalent.
- [ ] License of every dependency is compatible with the project's distribution model; copyleft licenses (GPL, AGPL) are flagged and explicitly approved by legal/compliance.
- [ ] Container base images (if used) are pinned by digest (`sha256:…`) or to a specific minor tag, not `latest`.
- [ ] Private/internal package registry credentials are stored in secrets management (not hardcoded in manifests or CI configs).
- [ ] CI pipeline fails the build on any new Critical/High CVE introduced by a PR (policy-as-code gate via Snyk, Dependabot alerts, or equivalent).

## P1 — Important (soon after launch)

- [ ] SBOM (Software Bill of Materials) generated in CycloneDX or SPDX format and stored as a release artifact for each production build.
- [ ] SCA scan covers transitive dependencies to at least 3 levels deep; recursive scanning is enabled in the chosen tool.
- [ ] Medium-severity CVEs have a documented remediation SLA (e.g., ≤ 30 days) and are tracked in the issue tracker.
- [ ] Dependabot (GitHub), Renovate, or equivalent is configured to open automated PRs for dependency updates on a weekly schedule.
- [ ] Dependency diff is reviewed in every PR; no unreviewed dependency additions reach `main`/`trunk`.
- [ ] Build artifacts are reproducible: same source + same lockfile produces a bit-for-bit identical artifact (verify via `reprotest` or equivalent).
- [ ] SLSA Level 1 provenance: build provenance metadata is generated and attached to release artifacts.
- [ ] Third-party scripts fetched at runtime (CDN `<script>` tags, `curl | bash` installers) are validated with Subresource Integrity (SRI) hashes.

## P2 — Hardening

- [ ] SLSA Level 2 provenance achieved: builds run on a hosted CI platform with tamper-evident provenance (e.g., GitHub Actions with `slsa-github-generator`).
- [ ] Supply-chain policy enforced via Sigstore/cosign or in-toto attestations; images signed and verified at deploy time.
- [ ] All internal/forked dependencies are mirrored to a controlled registry (Artifactory, AWS CodeArtifact, GitHub Packages) rather than fetched from upstream on each build.
- [ ] Dependency allowlist policy (e.g., `permitted-packages.json` or OPA policy) is enforced in CI to block unapproved new dependencies.
- [ ] License compliance report is generated automatically and reviewed quarterly; FOSS obligations (notices, attribution files) are fulfilled.
- [ ] Dev/test dependencies are explicitly separated from production dependencies (e.g., `devDependencies`, `[dev]` extras, `test` scope); only production deps are scanned for CVEs in the release gate.

## P3 — Post-launch / backlog (track, revisit after launch; never blocks)

- [ ] SLSA Level 3 provenance: hermetic, isolated builds with additional supply-chain controls.
- [ ] VEX (Vulnerability Exploitability eXchange) documents created for disputed or not-applicable CVEs to reduce false-positive noise in SCA reports.
- [ ] Software Composition Analysis results published to a centralised dependency dashboard (e.g., Dependency-Track) for portfolio-level visibility.
- [ ] Quarterly dependency audit scheduled to review abandoned packages and evaluate alternatives proactively.

## How to use

**When:** Run this checklist before merging any PR that adds/upgrades dependencies, before every release, and as part of the monthly security review.

**Who:** `security-auditor` agent (`.claude/agents/quality/security-auditor.md`) leads; `devops-engineer` maintains CI integration; `technical-lead` approves exceptions.

**Command:** `/audit-security` (`.claude/commands/audit-security.md`) triggers this checklist automatically. P0 items block merge/deploy; P1 items generate tracked issues; P2–P3 are backlog.

**Tools:** Snyk, OWASP Dependency-Check, `npm audit`/`pip-audit`/`cargo audit`, Trivy, Grype, CycloneDX CLI, `slsa-github-generator`, `cosign`, Dependency-Track.

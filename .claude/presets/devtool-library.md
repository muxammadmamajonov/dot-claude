# Developer Tool / Library Preset

## Project type
A reusable software artifact published for consumption by other developers — not an end-user application. Variants: open-source library (npm/PyPI/crates.io/Maven), framework or meta-framework, SDK for a platform or API, CLI companion tool, code generator or scaffolder, linter/formatter/static-analysis plugin, build-system plugin (webpack/Vite/Rollup/Gradle), testing utility or fixture library, language runtime extension, or developer-facing API client.

## Typical use cases
- API client SDKs (wrapping a REST, GraphQL, or gRPC service for a target language)
- UI component libraries distributed as npm packages
- Framework plugins and middleware (authentication adapters, logging integrations)
- Code generators and scaffolding CLIs (project starters, boilerplate generators)
- Linting rule sets, formatters, or static-analysis plugins
- Testing utilities (fixtures, mocks, custom matchers, test helpers)
- Build-tool plugins (Vite plugins, webpack loaders, Rollup plugins, Gradle tasks)
- Infrastructure SDKs (IaC helpers, cloud provider wrappers, deployment utilities)

## Required discovery questions
1. What programming language(s) and runtime(s) must be supported? What is the minimum supported version of each (e.g. Node 18+, Python 3.10+, Rust 1.75+)?
2. What package registries will this be published to (npm, PyPI, crates.io, Maven Central, GitHub Packages)? Is the package open-source, source-available, or private/internal-only?
3. Who is the primary consumer — application developers, framework authors, or both? How sophisticated are they, and what DX expectations do they bring?
4. What is the API surface design philosophy — minimal and composable, batteries-included, or opinionated convention over configuration? Are there prior-art libraries that define expectations in this space?
5. Does the library have any runtime side effects (global state, monkey-patching, process lifecycle hooks)? How must it behave when multiple versions coexist in the same dependency tree (singleton problem)?
6. What are the bundle-size, startup-latency, or memory-footprint constraints? Will consumers use it in browser bundles, edge runtimes (Cloudflare Workers, Deno Deploy), or resource-constrained environments?
7. Is a TypeScript type definition (`.d.ts`) layer required, or will the library be authored in TypeScript and ship compiled JS + types together?
8. What is the versioning and breaking-change policy — semver strictly, deprecation windows, LTS branches? Who are the downstream consumers that a breaking change would affect?
9. Does the library need to handle authentication or secrets on behalf of the caller, and if so, how are credentials passed (constructor injection, environment variables, platform keychains)?
10. What is the maintenance and governance model — solo maintainer, small open-source team, company-backed OSS, or fully internal? Who approves releases and who handles security disclosures?

## Recommended agents

### Core
- `.claude/agents/core/orchestrator.md` — API surface governance, release sequencing
- `.claude/agents/core/solution-architect.md` — public API design, extension points, versioning strategy
- `.claude/agents/core/technical-lead.md` — internal architecture, module boundaries, build toolchain
- `.claude/agents/core/documentation-writer.md` — API reference, guides, migration docs, changelog

### Engineering
- `.claude/agents/engineering/backend-engineer.md` — core logic, runtime compatibility, error model
- `.claude/agents/engineering/api-architect.md` — public interface contracts, backward-compatibility rules
- `.claude/agents/engineering/release-engineer.md` — CI/CD pipeline, registry publishing, binary signing, changelogs
- `.claude/agents/engineering/frontend-engineer.md` — browser bundle builds, ESM/CJS dual output (when applicable)

### Quality
- `.claude/agents/quality/qa-engineer.md` — cross-runtime and cross-version test matrix, consumer integration tests
- `.claude/agents/quality/test-automation-engineer.md` — test pyramid, golden-file tests, mutation testing
- `.claude/agents/quality/security-auditor.md` — dependency audit, secrets-handling review, supply-chain security
- `.claude/agents/quality/performance-engineer.md` — bundle size regression, startup latency benchmarks, memory profiling

### Design
- `.claude/agents/design/ui-ux-designer.md` — DX design: error message quality, API ergonomics, documentation UX (when UI component library)

## Recommended skills
- `.claude/skills/api-design/SKILL.md` — public interface conventions, error types, extensibility patterns
- `.claude/skills/testing/SKILL.md` — unit, integration, snapshot/golden-file, consumer-driven contract tests
- `.claude/skills/security/SKILL.md` — dependency CVE scanning, secrets-handling patterns, supply-chain integrity
- `.claude/skills/performance/SKILL.md` — bundle analysis, tree-shaking verification, benchmark harness
- `.claude/skills/devops/SKILL.md` — CI matrix (OS × runtime version), registry publishing automation, provenance attestation
- `.claude/skills/documentation/SKILL.md` — API reference generation (TypeDoc/JSDoc/rustdoc), changelog conventions, migration guides
- `.claude/skills/backend/SKILL.md` — runtime compatibility shims, ESM/CJS interop, platform-specific adapters

## Recommended stack options

| Stack | Rationale |
|---|---|
| **TypeScript + tsup + Vitest + Changesets** | Gold standard for npm libraries; tsup produces ESM + CJS + `.d.ts` from one config; Vitest is fast and browser-compatible; Changesets automates versioned changelogs and releases. See `.claude/stack-matrix/web.md` |
| **Rust (cargo) + criterion benchmarks + cargo-release** | Best for performance-critical libraries, WASM targets, or system-level tools; memory safety prevents entire classes of CVEs; cargo ecosystem is excellent |
| **Python + uv/hatch + pytest + twine** | Natural choice for ML/data/scientific libraries; pyproject.toml-first; uv for fast installs; pytest plugins ecosystem; Hatch for packaging |
| **Go (module) + goreleaser + testify** | Ideal for infrastructure or cloud-tooling libraries; static binaries; clean module system; goreleaser handles multi-platform release artifacts |

Reference `.claude/stack-matrix/backend.md` for runtime tradeoffs; `.claude/stack-matrix/testing.md` for test framework comparisons.

## Required checklists
- `.claude/checklists/security.md` — dependency CVEs, secrets never in source, supply-chain signing, SECURITY.md
- `.claude/checklists/qa.md` — cross-version matrix, type correctness, backward-compatibility, golden-file tests
- `.claude/checklists/performance.md` — bundle size budget, startup benchmark, memory baseline, tree-shaking verified
- `.claude/checklists/production.md` — package metadata complete, license declared, README install + quickstart
- `.claude/checklists/launch.md` — registry publish verified, tag signed, release notes written, deprecation of prior alpha/beta tags

## MVP scope pattern

**In MVP**
- Minimal viable public API covering the core use case only — resist scope creep
- TypeScript types (or equivalent type system) shipped from day one
- README with install, quickstart, and at least three real-world usage examples
- `CHANGELOG.md` and semver tag starting at `0.1.0` or `1.0.0` with explicit stability promise
- CI matrix: all supported language/runtime versions × at least two OS (Linux + macOS)
- Unit tests at ≥ 80 % line coverage on public API paths
- `SECURITY.md` with a responsible-disclosure email address
- Published to target registry with correct license, homepage, and repository links in package metadata

**Deferred to v2**
- Plugin or extension system (design the core before adding extensibility)
- Multiple transport or backend adapters (start with one first-class implementation)
- Browser + Node dual builds (start with the primary target runtime)
- Internationalized error messages
- Interactive CLI companion (if the library is the primary artifact)
- Benchmarking dashboard / public perf tracking
- Contributor guide and first-issue labelling (once v1 API is stable)
- LTS branch policy (defer until there are real downstream dependents)

## Production risks

| Risk | Severity | Mitigation |
|---|---|---|
| Breaking public API in a minor or patch release | P0 | Semver contract enforced in CI (`api-extractor` for TS, `cargo-semver-checks` for Rust); deprecation warnings before removal; never remove in same release as deprecation |
| Malicious code injected via compromised maintainer account or dependency | P0 | Require MFA + scoped publish tokens on registry accounts; lock direct dependency versions; `npm audit` / `cargo audit` / `pip audit` in CI; publish provenance attestation (SLSA) |
| Secrets or credentials embedded in published package (`.env`, key material) | P0 | `.npmignore` / `files` allowlist in package.json restricts what is published; CI publishes from clean checkout; dry-run publish step outputs manifest for review |
| Singleton / global state conflict when multiple library versions coexist in the same process | P0 | Avoid module-level mutable globals; use Symbol or WeakMap keyed singletons; document peer-dependency version constraints |
| Bundle size regression making the package unusable in browser or edge environments | P1 | Size-limit or bundlesize check in CI with a hard budget per export; tree-shaking smoke test verifying unused code is eliminated |
| Missing or incorrect type definitions shipping in release | P1 | `tsd` or `expect-type` tests run in CI on the compiled output — not the source — to catch type regressions |
| Uncaught errors or unhandled promise rejections propagating to consumer | P1 | All async paths wrapped with typed error classes; no bare `throw new Error('string')` in public API; errors carry `code`, `message`, and optionally `cause` |
| No way for consumers to report security vulnerabilities privately | P1 | `SECURITY.md` at repo root; GitHub private security advisory or equivalent enabled |
| Documentation out of sync with implementation after refactors | P2 | API reference generated from source (TypeDoc/rustdoc/pydoc); broken-link checker on docs site in CI |
| Deprecated version still widely pinned — consumers never upgrade | P2 | Publish deprecation notice on registry; announce in README; emit runtime warning after N months |

## Launch requirements
- Package published to target registry; `npm install` / `pip install` / `cargo add` confirmed on a fresh machine with no local cache
- Package metadata verified: name, version, description, license (SPDX), homepage, repository, keywords, `main`/`module`/`exports` fields correct
- README contains: install command, minimal working example, link to full API reference, supported runtime versions, license badge
- `CHANGELOG.md` contains the v1.0.0 (or initial public) entry with summary of what is included
- `SECURITY.md` present with responsible-disclosure process
- CI matrix green across all declared supported runtime/OS combinations
- Bundle size within declared budget; tree-shaking verified
- No high or critical CVEs in dependency tree at publish time (`npm audit --audit-level=high`)
- API surface snapshot committed so future regressions are caught automatically
- At least one integration test runs against the published package artifact (not local source) to confirm the package is consumable as shipped

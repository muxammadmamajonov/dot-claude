# Monorepo & Multi-Service Orchestration — one flow, many packages

This layer adapts the universal 9-stage flow to a repo containing **more than one independently
classifiable package or service**. It does not replace `.claude/orchestration/routing-matrix.md` — each
package still gets classified and routed through it (or the web/mobile/desktop layer if that's its
type); this file is the extra step that decides *which* packages are in scope for a given task and how
their gates combine without re-auditing the whole repo on every change.

## Topology detection (first step)

Signals this layer applies (any one is enough; more strengthens the call):
- Workspace tooling config present: `pnpm-workspace.yaml`, `turbo.json`, `nx.json`, `lerna.json`,
  `rush.json`, an npm/yarn `"workspaces"` field, a Cargo `[workspace]` table, `go.work`, a Bazel
  `WORKSPACE`/`MODULE.bazel` with multiple `BUILD.bazel` targets, or a `.sln` referencing multiple
  project directories.
- More than one independent manifest (`package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`,
  `*.csproj`, `build.gradle`) under different top-level directories — not just a root manifest plus one app.
- Conventional top-level directories (`apps/`, `packages/`, `services/`, `libs/`, `modules/`) each holding
  an independently buildable unit.
- Multiple independently deployable services in one repo (separate Dockerfiles/deploy configs per directory).

If none apply, this layer is irrelevant — use the normal single-project flow.

## Operating modes (orchestrator picks per task)

- **per-package** (default) — scope the task to one package/service; classify and route it exactly like
  a standalone project via `.claude/orchestration/routing-matrix.md`, using only that package's own
  manifest/framework signals. A sibling package's stack must never leak into this classification.
- **shared-infra change** — a change to root tooling (CI config, shared lint/build config, the root
  lockfile, a shared internal library). Route to root-level concerns (below) and use the dependency graph
  to find every downstream package that needs re-verification, without pulling each one's full team into
  the active set just because it exists.
- **cross-package feature** — one feature spans multiple packages (e.g. a type change in
  `packages/api-types` consumed by `apps/web` and `apps/mobile`). Classify each touched package, union
  their active teams, but run the shared-infra gates once, not once per package.
- **full-repo audit** — pre-release or periodic. Every package runs its own gates; root-level gates
  (dependencies, release-rollback) run once for the whole repo, not per package.

## Package classification (extends `/route`)

For each affected package, run `.claude/skills/project-classification/SKILL.md` scoped strictly to that
package's own subtree and manifest. Record one classification per package at
`docs/state/packages/<package-name>/project-type.md`, and roll up a repo-level summary at
`docs/state/monorepo.md` listing every package, its type, and its risk tier.

## Root vs package-scoped concerns

| Concern | Scope | Owner |
|---|---|---|
| CI/CD pipeline, root lint/format config | Root, once | `.claude/agents/engineering/devops-engineer.md` |
| Dependency/SCA scanning, SBOM | Root if a shared lockfile; per-package if each has its own | `.claude/agents/quality/security-auditor.md` |
| Shared internal library (e.g. `packages/ui`, `packages/api-types`) | Has its own classification (often `devtool-library`) **and** is a dependency of others | that package's owner, plus notify dependents |
| Framework code, business logic, tests, UI | Per-package | that package's stack engineer (web/mobile/backend/game/desktop) |
| Security/QA/performance/accessibility audits | Per-package for the audit itself; root once for supply-chain | `.claude/agents/quality/*` per package |
| Release/versioning | Per-package if independently versioned (changesets/semantic-release per package), else one root-level version | `.claude/agents/engineering/release-engineer.md` |

## Dependency graph & blast radius

Before scoping an active team, read the workspace's dependency graph (workspace-protocol references,
`nx graph` / `turbo run --dry` output, Cargo workspace members, Go module graph) to find what depends on
what. A change to a **leaf package** (nothing depends on it) needs only that package's own gates. A
change to a package with **N dependents** needs that package's own gates plus a *scoped* re-verification
of each dependent — rebuild and run its existing test suite — not a full re-classification or full audit
unless the dependent's own code also changed. Auditing every package in a 40-package monorepo because one
shared util changed violates the minimal-active-team principle
(`.claude/agents/core/orchestrator.md` — *Selection algorithm*); record the actual blast radius instead.

## Gate aggregation — shipping the monorepo

The launch gate for a monorepo change is the **union** of every touched package's own gates (per
`.claude/orchestration/routing-matrix.md` or the web/mobile/desktop layer) plus the root-level gates
(`.claude/checklists/dependencies.md`, `.claude/checklists/release-rollback.md`) run once. A package
untouched by the change, with no path from it in the dependency graph, does not need to re-pass its
gates — record which packages were judged in-scope and why in the routing decision so this stays
auditable rather than assumed.

## State layout

- `docs/state/monorepo.md` — repo-level summary: every package, its type/risk tier, its position in the
  dependency graph.
- `docs/state/packages/<name>/project-type.md`, `docs/state/packages/<name>/active-team.md` — per-package,
  mirroring the single-project state files.
- `docs/state/assumptions.md` stays one repo-level register; tag each entry with the package(s) it applies to.

## Commands that drive this

`.claude/commands/route.md` (topology detection is Step 0; loops per-package when a monorepo is
detected), `.claude/commands/onboard.md` (codebase-mapper run once per package plus a root summary),
the type-specific audits (`/web-audit`, `/mobile-audit`, `/desktop-audit`, or a backend project's
`/audit-security`) invoked per affected package, and `.claude/commands/plan-scale.md` for cross-package
capacity planning.

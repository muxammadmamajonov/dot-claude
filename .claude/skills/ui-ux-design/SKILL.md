---
name: ui-ux-design
description: Use when designing or revising what users (human or machine) interact with — information architecture, user/data flows, screens or command surfaces, and a reusable design-system baseline. Triggers after specs exist and before UI build phases, or whenever a new surface (web page, mobile screen, CLI command, API shape, dashboard, device UI) is introduced.
---

# UI / UX & Interaction Design

## When to use
- A spec or feature is approved and a human-facing or machine-facing surface must be designed before build.
- You are adding a new screen, view, command, endpoint shape, notification, or device interaction.
- Usability, accessibility, or consistency problems are reported and a redesign is needed.
- The project lacks a shared design baseline (tokens, components, interaction patterns) and drift is appearing.

"UI" here is broad: GUI screens, CLI/TUI command surfaces, conversational/agent turns, API request/response ergonomics, dashboards, and embedded/IoT displays all have an interaction layer worth designing.

## Workflow
1. **Restate the job-to-be-done.** From the spec, write one sentence per primary user (or consuming system) describing the outcome they need. Reference the founder interview and `.claude/templates/product-spec.md`. If a primary user is unclear, ask the user — do not invent personas.
2. **Map information architecture.** List the top-level entities, their relationships, and how a user navigates between them. For non-GUI projects this is the command/resource hierarchy or the object model an API exposes. Produce a tree or sitemap.
3. **Design the critical flows.** For each top-3 task, write the happy path as numbered steps, then enumerate the empty, loading, error, partial-permission, and offline states. A flow is not done until every state is named.
4. **Sketch screens / surfaces low-fidelity first.** Lay out each surface as labeled regions (header, primary action, content, secondary). Decide the single primary action per surface. Keep it text/wireframe level — do not pick colors or pixel values yet.
5. **Establish the design-system baseline.** Define tokens once: spacing scale, type scale, color roles (not raw hex scattered everywhere), radius, elevation, motion durations. Define core components (button, input, list, card, dialog, toast, empty-state) with their states. Record this in `.claude/templates/architecture.md` or a dedicated design-system doc.
6. **Specify interaction & accessibility rules.** Keyboard order, focus management, hit-target sizes, contrast ratios, error-recovery, copy tone. For CLI: flag conventions, `--help` output, exit codes, machine-readable output mode. For APIs: consistent naming, pagination, error envelope.
7. **Validate cheaply.** Walk each flow against the spec's acceptance criteria. Run a heuristic pass (see Standards). If feasible, do a 3–5 person hallway test or a quick task walkthrough before committing to build.
8. **Hand off.** Produce the artifact described in Output format, link it from the spec, and flag the build phases that implement it.

## Standards
- **Do** design the unhappy paths (empty, error, loading, no-permission, slow-network) for every flow — they are the bulk of real usage.
- **Do** define one primary action per surface; demote everything else visually or structurally.
- **Do** centralize design decisions as tokens/components so changes propagate; never hardcode the same spacing/color in twenty places.
- **Do** meet WCAG 2.2 AA as the default bar: 4.5:1 text contrast, 24px min target spacing, visible focus, no information by color alone. See `.claude/checklists/accessibility.md`.
- **Do** write real interface copy (labels, errors, empty states) — copy is design, not a fill-in-later task.
- **Do** design responsively/adaptively: small + large viewport for GUI, narrow + wide terminal for CLI, varying payloads for APIs.
- **Do-not** start visual polish (color, shadow, animation) before IA and flows are validated.
- **Do-not** introduce a new component when an existing one fits; extend the system instead.
- **Do-not** rely on hover-only or color-only affordances, or ship modals that trap focus or lose keyboard users.
- **Do-not** assume a web app — keep patterns translatable to whatever surface the project actually uses.

## Common mistakes to avoid
- Designing only the success state and discovering error/empty/loading gaps during build.
- "Mystery meat" navigation: unlabeled icons, ambiguous primary actions, hidden destructive actions with no confirmation.
- Inventing personas or requirements not in the spec instead of asking the user one business-critical question.
- Token sprawl: a "spacing system" that has 14 ad-hoc values, or colors copied as hex everywhere.
- Inaccessible defaults: low contrast, tiny tap targets, focus that disappears, forms without labels.
- Over-designing low-traffic surfaces while under-specifying the daily-driver flow.
- Treating CLI/API/agent surfaces as "not UX" — they have the same need for clarity, consistency, and good error messages.

## Output format
A design package (one document or folder) containing: (1) IA tree/sitemap, (2) the top flows with all states enumerated, (3) low-fidelity wireframes/region maps per surface, (4) the design-system baseline (tokens + core components with states), (5) interaction & accessibility rules, (6) real interface copy. Use `.claude/templates/architecture.md` for the system-level structure and link the package from the feature spec (`.claude/templates/product-spec.md`). Keep it diff-friendly (markdown + simple diagrams) so it lives in the repo and stays current.

## Related checklists
- `.claude/checklists/accessibility.md`
- `.claude/checklists/qa.md`
- `.claude/checklists/security.md`

## Related agents
- `.claude/agents/core/orchestrator.md`
- `.claude/agents/design/ui-ux-designer.md`
- `.claude/agents/core/business-analyst.md`

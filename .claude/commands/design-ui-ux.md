---
description: Define information architecture, key flows, screen-level wireframes, design-system tokens, and accessibility baseline
argument-hint: [feature or surface name]
---

# /design-ui-ux

## Purpose
Produce a complete UI/UX design brief for a feature or product surface: information architecture, user flows, screen-level wireframes (text-based), a design-system token set, component inventory, and an accessibility baseline — before any implementation begins.

## When to use
- After `/classify` and `/interview-founder` have confirmed the product type and user goals
- Before `/build-prototype` or `/implement-feature`
- When redesigning an existing surface or adding a major new user-facing area
- When a design system does not yet exist and tokens need to be established
- When the argument is omitted, scope to the entire product MVP

## Workflow

**Step 1 — Load context** (orchestrator: `.claude/agents/core/orchestrator.md`)
- Read `docs/specs/product.md`, `docs/specs/architecture.md`, and any existing design-system token files
- Identify project type (web, mobile native, desktop, CLI, embedded dashboard, etc.) — UI/UX approach differs per type
- List known user personas, goals, and jobs-to-be-done from the spec

**Step 2 — Information architecture**
- Map all screens / surfaces / views for the given scope into a hierarchy table:
  | Surface | Parent | Entry point | Primary action |
- Identify navigation model: tabs, sidebar, breadcrumb, wizard steps, command palette, etc.
- For non-visual products (CLI, API, voice): map command/intent hierarchy and key interaction states instead

**Step 3 — User flow diagrams (text)**
- Write numbered step-by-step flows for every critical path (happy path + 2 failure paths per flow)
- Format: `[Actor] → [Trigger] → [Screen/State] → [Action] → [Next Screen/State]`
- Mark branch points and error states explicitly

**STOP — business-critical decision #1**
Present the IA and flows to the user. Ask:
1. Are all user goals and personas correctly represented?
2. Are there flows or edge cases missing?
3. Are there brand / platform / accessibility constraints not yet captured?
Do not proceed until the user confirms or provides corrections.

**Step 4 — Screen-level wireframes**
- Produce ASCII / structured text wireframes for every distinct screen and state identified in Step 2–3
- Each wireframe must include: layout regions, key components (buttons, inputs, lists, cards), hierarchy of information, empty/loading/error states
- For CLI: show prompt structure, output format, and error messages
- For APIs: show request/response shapes and error envelopes as wireframe equivalents

**Step 5 — Design-system tokens**
Define or extend the project token set in `docs/specs/design-tokens.md`:
- **Color**: primary, secondary, background, surface, border, error, warning, success, text (all variants)
- **Typography**: font families, scale (xs → 4xl), weight, line-height
- **Spacing**: base unit, scale (4, 8, 12, 16, 24, 32, 48, 64)
- **Radius & elevation**: border-radius values, shadow levels
- **Motion**: duration tokens (fast 100ms, normal 200ms, slow 400ms), easing curves
- For non-web projects map tokens to the platform equivalent (iOS HIG, Material Design, terminal color codes, etc.)

**Step 6 — Component inventory**
List every UI component required for this scope:
| Component | Variants | States | Tokens used | Notes |
Include: atomic (button, input, icon) + molecular (card, form row) + organism (nav, data table, modal).

**Step 7 — Accessibility baseline**
- Target standard: WCAG 2.2 AA minimum (or platform equivalent: iOS accessibility, ARIA, terminal screen-reader)
- For each component in Step 6, list: keyboard/focus behavior, ARIA role/label, contrast ratio requirement, touch-target minimum
- Flag any flows with timing, motion, or cognitive-load risks

**Step 8 — Write outputs**
- Write `docs/specs/ui-ux-brief.md` with all artefacts from Steps 1–7
- Update or create `docs/specs/design-tokens.md`
- Update `docs/specs/product.md` if new flows change scope

**STOP — business-critical decision #2**
Present the full brief to the user. Ask:
1. Do the wireframes match the intended experience?
2. Are the design tokens consistent with brand requirements?
3. Any component or accessibility requirement to add/remove before build?

## Agents used
- `.claude/agents/core/orchestrator.md` — coordinates steps
- `.claude/agents/design/ui-ux-designer.md` — IA, flows, wireframes (if available, otherwise orchestrator handles)

## Skills used
- `.claude/skills/ui-ux-design/SKILL.md` (if present)
- `.claude/checklists/accessibility.md`

## Expected outputs
| File | Status |
|------|--------|
| `docs/specs/ui-ux-brief.md` | created / updated |
| `docs/specs/design-tokens.md` | created / updated |
| `docs/specs/product.md` | updated (if scope changed) |

## Stop conditions
- No product spec or architecture spec exists — run `/classify` and `/interview-founder` first
- User rejects IA or flows in decision #1 — revise before continuing
- Platform type is ambiguous (cannot determine rendering target) — ask before Step 4

## Final report format
```
## UI/UX Design Brief — [scope name]

### Surfaces defined: N
### Flows documented: N (happy paths) + N (failure paths)
### Wireframes: N screens / states
### Design tokens: N defined | N updated
### Components: N (N atomic, N molecular, N organism)
### Accessibility: WCAG 2.2 AA | N flags to review

### Files written
- docs/specs/ui-ux-brief.md
- docs/specs/design-tokens.md

### Open decisions
- [any unresolved items from stop conditions]

### Next step
Run /build-prototype or /implement-feature [feature name]
```

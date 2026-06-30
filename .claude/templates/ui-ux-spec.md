# UI/UX Specification

**What:** Defines information architecture, user flows, screen inventory, component states, design tokens, and accessibility requirements.
**Who fills it in:** Product designer + product manager, reviewed by engineering lead.
**When:** After the project brief and architecture doc are complete; before any production UI is built.

---

## 1. Product Context

> What problem does this UI solve, and for whom? What is the primary job-to-be-done for the main user persona?

- Primary persona: `<Role, e.g. "Operations manager at a mid-market logistics company">`
- Top 3 tasks they must complete: `<task 1>`, `<task 2>`, `<task 3>`
- Device/environment: `<web desktop | native iOS | native Android | TV | kiosk | embedded display>`
- Usage pattern: `<frequent/daily vs. occasional vs. one-time onboarding>`

---

## 2. Information Architecture

> List every major section of the product as a tree. Include hidden/settings pages.

```
<AppName>
├── Auth
│   ├── Sign In
│   ├── Sign Up
│   └── Forgot Password
├── <Main Section 1>
│   ├── <List View>
│   └── <Detail View>
├── <Main Section 2>
│   ├── <Dashboard>
│   └── <Sub-page>
├── Settings
│   ├── Profile
│   ├── Notifications
│   └── Billing
└── Error / Empty States
```

---

## 3. Navigation Model

> Describe how users move between sections. Choose one primary pattern and note any secondary patterns.

| Dimension | Choice | Notes |
|-----------|--------|-------|
| Primary nav pattern | `<tabs | sidebar | drawer | hub-and-spoke | wizard>` | `<rationale>` |
| Deep-link support | `<yes / no>` | `<URL scheme or universal links>` |
| Back navigation | `<browser back / explicit back button / breadcrumb>` | |
| Auth-gated routes | `<list routes that require login>` | Redirect to `<sign-in URL>` |
| Role-based access | `<admin sees X, viewer sees Y>` | |

---

## 4. Key User Flows

> For each critical flow, list the steps and the happy-path decision points. Use numbered steps.

### Flow 1: `<e.g. New User Onboarding>`

1. User lands on `<entry point>`
2. `<Step 2 action>`
3. System responds with `<outcome>`
4. User arrives at `<destination screen>`

**Error path:** If `<failure condition>`, show `<error screen/toast>` and offer `<recovery action>`.

---

### Flow 2: `<e.g. Core Task Completion>`

1. User navigates to `<screen>`
2. `<Step 2 action>`
3. Confirmation: `<modal | inline | email>`

**Empty state:** When no data exists, show `<illustration + CTA copy>`.

---

### Flow 3: `<e.g. Settings / Billing / Account Management>`

*(Add as many flows as the product requires.)*

---

## 5. Screen Inventory

> One row per distinct screen or significant modal. Link to wireframe/Figma if available.

| Screen ID | Name | Route / Deep-link | Auth Required | Design Link |
|-----------|------|-------------------|---------------|-------------|
| S-01 | `<Sign In>` | `/login` | No | `<Figma URL>` |
| S-02 | `<Dashboard>` | `/dashboard` | Yes | `<Figma URL>` |
| S-03 | `<Item Detail>` | `/items/:id` | Yes | `<Figma URL>` |
| S-04 | `<Settings – Profile>` | `/settings/profile` | Yes | `<Figma URL>` |
| S-05 | `<Empty State>` | n/a | — | `<Figma URL>` |

---

## 6. Component States Catalogue

> For each reusable interactive component, enumerate all states that engineering must implement.

### `<Button>`
- Default, Hover, Focused, Active/Pressed, Disabled, Loading/Spinner

### `<Input Field>`
- Empty, Filled, Focused, Error (with message), Disabled, Read-only

### `<Data Table / List>`
- Loading skeleton, Populated, Empty, Error, Sorted (ASC/DESC), Row selected, Row expanded

### `<<ComponentName>>`
- `<list states>`

> Add a component row for every element that has more than one visual state.

---

## 7. Design Tokens

> Seed values that engineering will implement in code (CSS variables, design-system theme, etc.).

### Color

| Token | Light value | Dark value | Usage |
|-------|-------------|------------|-------|
| `color-primary` | `#<hex>` | `#<hex>` | CTA buttons, active nav |
| `color-secondary` | `#<hex>` | `#<hex>` | Secondary actions |
| `color-surface` | `#<hex>` | `#<hex>` | Card / panel backgrounds |
| `color-error` | `#D32F2F` | `#EF9A9A` | Validation errors |
| `color-success` | `#2E7D32` | `#A5D6A7` | Confirmations |
| `color-text-primary` | `#<hex>` | `#<hex>` | Body copy |
| `color-text-muted` | `#<hex>` | `#<hex>` | Labels, captions |

### Typography

| Token | Value | Usage |
|-------|-------|-------|
| `font-family-base` | `<"Inter", sans-serif>` | Body text |
| `font-family-mono` | `<"JetBrains Mono", monospace>` | Code, IDs |
| `font-size-xs` | `12px` | Labels |
| `font-size-sm` | `14px` | Body small |
| `font-size-base` | `16px` | Body |
| `font-size-lg` | `20px` | Section headings |
| `font-size-xl` | `24px` | Page headings |
| `font-weight-regular` | `400` | |
| `font-weight-medium` | `500` | Emphasis |
| `font-weight-bold` | `700` | Headings |

### Spacing & Radius

| Token | Value |
|-------|-------|
| `space-1` | `4px` |
| `space-2` | `8px` |
| `space-3` | `12px` |
| `space-4` | `16px` |
| `space-6` | `24px` |
| `space-8` | `32px` |
| `radius-sm` | `4px` |
| `radius-md` | `8px` |
| `radius-lg` | `16px` |
| `radius-full` | `9999px` |

### Motion

| Token | Value | Usage |
|-------|-------|-------|
| `duration-fast` | `100ms` | Hover states |
| `duration-base` | `200ms` | Modals, drawers |
| `duration-slow` | `400ms` | Page transitions |
| `easing-standard` | `cubic-bezier(0.4,0,0.2,1)` | Most animations |
| `easing-enter` | `cubic-bezier(0,0,0.2,1)` | Elements entering |
| `easing-exit` | `cubic-bezier(0.4,0,1,1)` | Elements leaving |

---

## 8. Responsive & Adaptive Breakpoints

> Define breakpoints and describe what changes at each.

| Breakpoint | Range | Layout change |
|------------|-------|---------------|
| `xs` | `< 480px` | Single column, bottom tab bar |
| `sm` | `480–767px` | Single column, top nav |
| `md` | `768–1023px` | Two-column, collapsible sidebar |
| `lg` | `1024–1279px` | Fixed sidebar, main content |
| `xl` | `≥ 1280px` | Wide layout, max-width `<1440px>` |

---

## 9. Accessibility Requirements

> Minimum compliance level: **WCAG 2.1 AA** (or higher if regulated industry).

| Requirement | Target | Notes |
|-------------|--------|-------|
| Color contrast (text) | ≥ 4.5:1 | Use `color-text-primary` on `color-surface` |
| Color contrast (large text / UI) | ≥ 3:1 | Buttons, icons |
| Keyboard navigation | Full tab order | All interactive elements reachable |
| Focus indicator | Visible 3px outline | `color-primary` at 3:1 contrast |
| Screen reader labels | All images, icons | `alt` text or `aria-label` |
| Form error identification | Text + icon (not color alone) | |
| Motion / animation | Respect `prefers-reduced-motion` | Disable or reduce transitions |
| Touch target size | ≥ 44×44px | Mobile interactive elements |
| Language attribute | `<html lang="<en>">` | |

---

## 10. Internationalization (i18n) Considerations

> Note if the product must support multiple languages, RTL, or locale-specific formatting.

- Supported locales at launch: `<en-US>` / `<add others>`
- RTL support required: `<yes / no>` — target languages: `<Arabic, Hebrew>`
- Date format: `<ISO 8601 | locale-aware>`
- Number/currency format: `<locale-aware via Intl API>`
- String storage: `<JSON locale files | i18next | gettext>`
- Text expansion allowance: `+40%` over English string lengths for UI containers

---

## 11. Open Decisions

> Track unresolved design questions. Remove items when resolved.

| # | Question | Owner | Target date |
|---|----------|-------|-------------|
| 1 | `<e.g. Should the dashboard default to weekly or monthly view?>` | `<Designer>` | `<YYYY-MM-DD>` |
| 2 | `<e.g. Do we need an in-app notification center or email-only?>` | `<PM>` | `<YYYY-MM-DD>` |

---

## 12. Related Documents

- Project brief: `.claude/templates/project-brief.md`
- Architecture: `.claude/templates/architecture.md`
- Mobile spec (if applicable): `.claude/templates/mobile-spec.md`
- Security model: `.claude/templates/security-model.md`
- Accessibility checklist: `.claude/checklists/accessibility.md`

# UI/UX Checklist

Passing this gate proves the interface is usable, consistent, accessible, and production-ready: real users can complete core tasks without confusion, error states are handled gracefully, the design system is applied correctly, and the product communicates clearly in every state. Items are severity-tagged P0/P1/P2/P3.

## P0 — Blockers (must pass before any user-facing release)

- [ ] Every interactive element — button, link, form field, modal trigger, dropdown — is reachable and fully operable via keyboard alone; no mouse-only or touch-only interactions exist.
- [ ] Every primary task flow (sign-up, onboarding, core action, checkout, settings change) has been walked through end-to-end by at least one person who did not build it; all blocking confusion or dead-ends are resolved.
- [ ] Loading, empty, and error states are explicitly designed and implemented for every data-driven view: no blank white screens, no raw error stack traces, no unhandled promise rejections visible to users.
- [ ] Form validation errors are displayed inline adjacent to the offending field immediately on submit (or on blur for async checks); error messages are in plain language and include specific guidance on how to fix the issue — not generic "Invalid input."
- [ ] Destructive or irreversible actions (delete, archive, unsubscribe, wipe, publish to production, send to all users) require an explicit confirmation step with clear language describing the consequence; single-click activation is forbidden.
- [ ] Color is never the sole differentiator for states, categories, or data series; every color-coded element is also labeled with text, an icon, or a pattern (WCAG 1.4.1).
- [ ] Text contrast ratio meets WCAG 2.2 AA minimums: ≥ 4.5:1 for body text, ≥ 3:1 for large text (≥ 18 pt / 14 pt bold) and UI component boundaries.
- [ ] The product is fully usable at every declared breakpoint (mobile, tablet, desktop, wide); no critical content is hidden, cropped, overlapping, or horizontally scrollable on a single-column layout at any supported viewport size.
- [ ] All images, icons, and non-text UI elements have descriptive `alt` text or `aria-label`; decorative elements are explicitly hidden from the accessibility tree.
- [ ] No content flashes more than 3 times per second; auto-playing media can be paused by the user.

## P1 — Important (fix before broad rollout)

- [ ] Navigation hierarchy is consistent across the entire product: the same action is always found in the same location; back-navigation or breadcrumbs are present whenever the user is more than one level deep.
- [ ] Page titles, section headings, CTA labels, and tooltip copy are written in plain language targeted at the actual end-user persona; no internal jargon, debug identifiers, or developer-facing strings appear in the UI.
- [ ] Focus management is correct after every async state change: modal open moves focus into the dialog; modal close returns focus to the trigger; route transitions move focus to the page heading or main landmark; dynamic content insertion announces via live region.
- [ ] Touch targets on mobile are ≥ 44 × 44 CSS px (Apple HIG) / 48 × 48 dp (Material Design); adjacent interactive targets have ≥ 8 dp of non-interactive space between them.
- [ ] Skeleton screens or shimmer loaders appear within 150 ms for any data load that may exceed 300 ms; operations longer than 2 s display a determinate progress indicator or estimated time; operations that can be cancelled provide a cancel action.
- [ ] Design system tokens (color, typography scale, spacing, radius, shadow, motion) are applied consistently throughout; no undocumented one-off inline overrides exist in production components.
- [ ] Internationalization (i18n) hooks are in place even if only one locale ships: all user-facing strings are externalized to a translation file, layout accommodates ≥ 30 % text expansion (German, Finnish), date/number/currency formats use locale-aware formatters, and RTL support is either implemented or formally deferred in a decision record.
- [ ] Session timeout and authentication errors result in a graceful redirect to the login page with the user's original destination URL preserved as a `next` or `redirect` parameter; on re-auth the user lands at the correct page.
- [ ] Error pages (404, 403, 500, network failure) return the correct HTTP status code, display a human-readable explanation, and provide a clear recovery path (link to homepage, retry button, or support contact).
- [ ] Onboarding or first-run experience introduces the minimum required context for the user to complete their first core action; it does not front-load every feature or require completing a tutorial before accessing the product.
- [ ] All form fields have visible placeholder examples or helper text where the expected format is not obvious; password fields have a show/hide toggle.

## P2 — Hardening / nice-to-have

- [ ] `prefers-reduced-motion` is respected globally; animations and auto-playing media disable or replace with instant transitions when the user has reduced-motion enabled at the OS level.
- [ ] `prefers-color-scheme: dark` is supported or formally deferred; no hard-coded hex values that produce invisible text or unreadable contrast in dark mode.
- [ ] Usability testing conducted with ≥ 3 participants from the target persona; session recordings reviewed; top friction points triaged and addressed or deferred with rationale.
- [ ] Microcopy and error messages reviewed for tone consistency with the product's voice and brand guidelines; error messages are empathetic, never blame the user, and suggest a next step.
- [ ] Analytics events are instrumented on every primary CTA, form submission, error view, and modal interaction; event names follow a consistent taxonomy so UX decisions can be made from real usage data post-launch.
- [ ] Print stylesheet or `@media print` CSS defined for any view users are likely to print (invoices, reports, tickets, confirmation pages); no navigation chrome or ads appear in print output.
- [ ] Keyboard shortcut conflicts with OS and browser defaults are avoided; any custom shortcuts are discoverable via an in-product help overlay and are reassignable or disableable.

## P3 — Post-launch / backlog (track and revisit after launch; never blocks shipping)

- [ ] Session recordings and funnel analytics (from the events instrumented at P2) are reviewed 4–8 weeks post-launch; top drop-off points and rage-click clusters are triaged into the next design iteration cycle.
- [ ] Usability testing with the target persona is conducted on the live product (not a prototype) once a meaningful user base exists; findings are compared against the pre-launch P2 usability test results to measure improvement and surface regressions.
- [ ] `prefers-color-scheme: dark` support deferred at P2 is implemented and audited for contrast compliance before the next major feature release, using real usage telemetry to confirm dark-mode adoption warrants prioritisation.
- [ ] Print stylesheets deferred at P2 for likely-to-print views (invoices, reports, confirmations) are implemented and tested across the two most common browsers used by the actual user base.
- [ ] Keyboard shortcuts added post-launch are audited against an updated list of OS and browser defaults for the platform versions in use; any conflict found is resolved and the help overlay is updated to reflect the current shortcut set.

## How to use

**Stage:** gate 6 (Audit) for every feature before merge; full checklist at gate 8 (Launch readiness). Partial checks (P0 items) should be verified during stage 5 (Build) per slice.

**Agent:** `.claude/agents/design/ui-ux-designer.md` and `.claude/agents/design/product-designer.md` own design review; `.claude/agents/quality/qa-engineer.md` owns functional validation; `.claude/agents/quality/accessibility-auditor.md` owns the accessibility subset.

**Skill:** `.claude/skills/ui-ux-design/SKILL.md` for design patterns; `.claude/skills/testing/SKILL.md` for usability-test scripts.

**Commands:** `review-feature` runs this checklist per feature; `audit-production` includes the full pass before launch.

**Process:** step through in order — (1) keyboard and focus walkthrough, (2) screen-reader pass on primary flows, (3) all-breakpoint resize test, (4) empty/loading/error state review, (5) copy and label audit. Mark each item `[x]` when verified or `[-]` when waived with written rationale and reviewer sign-off. P0 failures are launch blockers; record any waiver in `.claude/templates/decision-record.md`.

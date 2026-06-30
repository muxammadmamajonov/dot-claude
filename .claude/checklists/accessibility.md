# Accessibility Checklist

Passing this gate proves the product meets WCAG 2.2 AA conformance and is independently operable by users of keyboards, screen readers, switch devices, and alternative input methods across every supported platform (web, mobile, desktop, CLI/TUI, voice). Severity tiers: P0=blocker, P1=important (fix shortly after launch), P2=hardening, P3=post-launch / backlog (track and revisit; never blocks shipping).

## P0 — Blockers (must pass before proceeding / launch)

- [ ] Every interactive control — buttons, links, form fields, sliders, toggles, custom widgets — is reachable and fully operable via keyboard alone; no interaction requires a pointer device.
- [ ] Focus order follows the logical reading/flow order of the page or screen; Tab sequence never skips over content the user must interact with.
- [ ] Focus is never permanently trapped in a component unless it is a modal/dialog that explicitly provides an accessible close action (Esc key + visible close button).
- [ ] A visible, high-contrast focus indicator appears on every focused element; the default browser/platform outline is not suppressed without a custom replacement that meets ≥ 3:1 contrast against adjacent colors.
- [ ] Every non-text element — images, icons, illustrations, charts, video thumbnails — has a meaningful `alt` attribute, `aria-label`, or `aria-labelledby`; purely decorative elements are explicitly hidden from the accessibility tree (`alt=""` / `aria-hidden="true"`).
- [ ] Color is never the sole means of conveying information: error states, status badges, chart series, and data differences are always paired with text labels, icons, or patterns, not color alone.
- [ ] Text contrast ratio meets WCAG 2.2 AA minimums: ≥ 4.5:1 for body text, ≥ 3:1 for large text (≥ 18 pt regular or ≥ 14 pt bold), ≥ 3:1 for UI component boundaries and graphical objects.
- [ ] Every `<input>`, `<select>`, and `<textarea>` element (or platform equivalent) has an explicit, programmatically associated label; required fields are marked as required in the accessibility tree (`aria-required="true"` or `required`); validation errors identify the field by name and describe how to fix the error.
- [ ] No content flashes more than 3 times per second; no full-screen or large-area strobing effects exist (WCAG 2.3.1 — seizure threshold).
- [ ] Page or screen language is declared so assistive technologies use the correct pronunciation engine (`lang` attribute on HTML root, or platform locale setting); inline language changes use `lang` on the affected element.
- [ ] Timed sessions warn users at least 20 seconds before expiry and offer extension or the ability to disable the timer (WCAG 2.2.1); auto-refreshing content can be paused, stopped, or extended.
- [ ] Audio or video that plays automatically for more than 3 seconds has a mechanism to pause, stop, or mute it reachable by keyboard without requiring interaction with other content first.

## P1 — Important (fix before scaling / shortly after launch)

- [ ] Automated scan with axe-core, Playwright-axe, or Pa11y returns zero critical and zero serious violations on every primary user flow and every page template; scan is integrated into CI and the build fails on new violations.
- [ ] Screen-reader testing completed manually on at least one major reader per target platform: NVDA + Chrome or JAWS + Chrome (Windows web), VoiceOver + Safari (macOS/iOS), TalkBack + Chrome (Android); all primary task flows narrate correctly without visual reference.
- [ ] Skip-navigation link ("Skip to main content") is the first focusable element on every web page with repeated header/navigation; it is visible on focus.
- [ ] Page structure uses semantic landmarks: `<main>`, `<nav>` (one per distinct navigation), `<header>`, `<footer>`, `<aside>`, `<section aria-labelledby>` for web; equivalent platform primitives (UIAccessibilityContainer, Android ViewGroup roles) for native apps.
- [ ] Heading hierarchy is logical: one `<h1>` per page, no skipped levels; headings describe sections and are not used for visual styling alone.
- [ ] Modals and dialogs move keyboard focus into the dialog on open; trap Tab within the dialog while open; return focus to the triggering element on close (or a logical equivalent).
- [ ] Toasts, live notifications, and status updates are exposed to assistive technology via `role="alert"`, `role="status"`, or `aria-live` (web), or platform notification APIs (iOS UIAccessibilityPostNotification, Android AccessibilityEvent).
- [ ] Touch targets on mobile are ≥ 44 × 44 CSS/logical px per platform HIG (Apple) and ≥ 48 × 48 dp (Material); spacing between adjacent targets ≥ 8 dp; WCAG 2.5.8 target-size minimum honored.
- [ ] Content remains fully usable when zoomed to 200% browser/OS text size with no loss of content, no horizontal scrolling on single-column layouts, and no clipped or overlapping text.
- [ ] Data tables include `<caption>` or `aria-label`, `<th scope="col|row">` headers, and `<thead>`/`<tbody>` grouping; complex pivot tables provide row and column header associations via `id`/`headers`.
- [ ] Drag-and-drop interactions have a keyboard alternative (e.g., cut/paste, arrow-key reordering, explicit "move" action) per WCAG 2.5.7.

## P2 — Hardening / nice-to-have

- [ ] WCAG 2.2 AAA targets reviewed and either met or explicitly deferred with documented rationale (contrast ≥ 7:1, sign-language video alternatives, extended audio descriptions).
- [ ] Accessibility conformance statement (VPAT / ACR or EN 301 549 equivalent) drafted, reviewed by accessibility counsel, and published at a stable URL.
- [ ] `prefers-reduced-motion` CSS media query (or platform equivalent) is respected; all non-essential animations, auto-play carousels, parallax, and transitions disable or simplify to instant state changes.
- [ ] Windows High Contrast mode and macOS Increase Contrast tested; no invisible borders, text, or focus indicators; no images that carry meaning fail to render under forced-colors.
- [ ] Custom keyboard shortcuts are discoverable (documented in-product help), do not conflict with OS or browser defaults, and are reassignable or disableable (WCAG 2.1.4).
- [ ] PDF and downloadable documents exported with tagged structure: logical heading order, reading-order tagging, alt text on images, table headers, accessible column/row order; validated with Adobe Acrobat Accessibility Checker or PAC 2024.
- [ ] User testing conducted with at least two participants who rely on assistive technology; findings triaged and high-severity issues added to the backlog.
- [ ] `prefers-color-scheme: dark` and high-contrast system themes render correctly without hard-coded colors that bypass the theme; all text and icons remain legible.

## P3 — Post-launch / backlog (track and revisit after launch; never blocks shipping)

- [ ] Automated accessibility regression suite is expanded to cover every page template and every interactive component in the design system, not just primary task flows; new violations introduced by any PR are caught in CI before merge.
- [ ] Formal user testing with at least four participants who rely on assistive technology (screen reader, switch access, voice control, and magnification) is conducted per major release cycle; severity-ranked findings feed directly into the product backlog with assigned owners.
- [ ] Published accessibility conformance report (VPAT or ACR) is updated annually and versioned alongside release notes; any outstanding known exceptions are listed with remediation target dates.
- [ ] `prefers-reduced-motion`, `prefers-color-scheme`, and `prefers-contrast` are each covered by automated visual regression snapshots so future CSS changes cannot silently break users who rely on these system preferences.
- [ ] Accessibility debt register is maintained: each open P1/P2 item has a severity rating, affected user-population estimate, estimated fix effort, and a target sprint; the register is reviewed in every sprint planning session.

## How to use

**Stage:** gate 6 (Audit) and gate 8 (Launch readiness). Also run incrementally during stage 5 (Build) per feature.

**Agent:** `.claude/agents/quality/accessibility-auditor.md` owns this gate. Cross-reference `.claude/agents/design/accessibility-designer.md` for remediation design patterns.

**Skill:** `.claude/skills/testing/SKILL.md` (automated scan steps) and `.claude/skills/ui-ux-design/SKILL.md` (accessible interaction patterns).

**Commands:** `audit-production` triggers the full run; `review-feature` should include a quick axe scan before merge.

**Process:** run in this order — (1) automated axe/Pa11y CI scan on all routes, (2) manual keyboard walkthrough of every primary task flow, (3) screen-reader session on the same flows, (4) mobile touch-target audit, (5) zoom and text-size check. Mark each item `[x]` when verified or `[-]` when formally waived with written rationale. P0 items are launch blockers; waivers require explicit sign-off recorded in `.claude/templates/decision-record.md`.

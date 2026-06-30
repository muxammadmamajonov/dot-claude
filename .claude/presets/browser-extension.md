# Browser Extension (MV3) Preset

## Project type
Software package installed into a web browser via the Chrome Web Store, Firefox Add-ons, Edge Add-ons, or Safari Web Extension. Variants: page-enhancement extension (content script), new-tab replacement, devtools panel extension, browser action popup, background service worker with side panel, or cross-browser extension targeting multiple stores simultaneously. All new Chromium-based extensions must use Manifest V3 (MV3); Firefox uses MV2 or a MV3 subset.

## Typical use cases
- Productivity enhancers (tab managers, reading modes, note-takers, focus timers)
- Page automation and scraping (form fillers, price trackers, coupon finders)
- Security and privacy tools (ad blockers, tracker blockers, password helpers)
- Developer tools (API inspectors, accessibility auditors, DOM visualisers)
- AI assistant overlays injecting AI capabilities into existing web pages
- B2B tools embedded into SaaS workflows (CRM sidebar, email assistants)

## Required discovery questions
1. Which browsers must be supported at launch — Chrome/Chromium only, or also Firefox, Edge, Safari? Firefox and Safari require separate porting effort for MV3.
2. What is the primary interaction model — popup (toolbar button), side panel, new-tab page, content script overlay, or devtools panel?
3. Does the extension need to read or modify page content (content script)? On all URLs or only specific hostnames (reduces permission scope)?
4. Does the extension require persistent background state, or is a stateless service worker acceptable? (MV3 service workers terminate after ~30 s idle.)
5. Does the extension communicate with a remote backend? Is the backend owned by this project or a third-party API?
6. What authentication is required — OAuth PKCE via `chrome.identity`, sync-ed credentials, or no auth?
7. What data does the extension persist — `chrome.storage.local` (device-only), `chrome.storage.sync` (across devices), or remote backend?
8. Are there enterprise deployment requirements — Group Policy, managed storage, force-install via MDM?
9. Does the extension need to run on `file://` URLs, incognito windows, or inside iframes?
10. What is the update strategy — Chrome Web Store auto-update only, or also sideloaded / self-hosted update XML for enterprise?

## Recommended agents

### Core
- `.claude/agents/core/orchestrator.md` — MV3 constraint tracking, store submission coordination
- `.claude/agents/core/solution-architect.md` — service worker lifecycle design, message passing topology
- `.claude/agents/core/project-manager.md` — phased feature delivery around store review timelines

### Engineering
- `.claude/agents/engineering/frontend-engineer.md` — manifest, service worker, content scripts, message routing
- `.claude/agents/engineering/frontend-engineer.md` — popup / side panel / options page UI
- `.claude/agents/engineering/backend-engineer.md` — companion backend API (if applicable)
- `.claude/agents/engineering/backend-engineer.md` — `chrome.identity` OAuth PKCE, token refresh in service worker

### Quality
- `.claude/agents/quality/qa-engineer.md` — cross-browser matrix, content script injection edge cases
- `.claude/agents/quality/security-auditor.md` — CSP, message validation, XSS via DOM injection
- `.claude/agents/quality/performance-engineer.md` — service worker wake-up latency, memory in content scripts

### Domain
- `.claude/agents/engineering/release-engineer.md` — Web Store listing, privacy policy, permission justification
- `.claude/agents/quality/qa-engineer.md` — WebExtensions polyfill, Firefox-specific deviations

## Recommended skills
- `.claude/skills/browser-extension/SKILL.md` — MV3 patterns, message passing, service worker persistence workarounds
- `.claude/skills/web/SKILL.md` — popup/panel UI, shadow DOM for content scripts
- `.claude/skills/security/SKILL.md` — `chrome.identity`, PKCE, token storage in `chrome.storage`
- `.claude/skills/security/SKILL.md` — CSP for extensions, input sanitisation, `world: ISOLATED` content scripts
- `.claude/skills/testing/SKILL.md` — Puppeteer / Playwright extension testing, unit testing with jest-webextension-mock
- `.claude/skills/api-design/SKILL.md` — message protocol between popup ↔ service worker ↔ content script

## Recommended stack options

| Stack | Rationale |
|---|---|
| **WXT (Web Extension Tools) + React + TypeScript** | Purpose-built MV3 scaffold; HMR in dev; built-in cross-browser polyfill; TypeScript-first. See `.claude/stack-matrix/web.md` |
| **Plasmo + React + TypeScript** | Excellent DX for Chrome/Firefox; CSUI for content-script UI; built-in storage and messaging abstractions |
| **Vanilla TypeScript (custom webpack/vite config)** | Maximum control; best when extension is large and framework overhead matters; requires more manual wiring |
| **Vue 3 + Vite Plugin Web Extension** | Good option when team is Vue-primary; lightweight; similar tooling support to React options |

Reference `.claude/stack-matrix/web.md` for JS framework tradeoffs; MV3 mandates no remote code execution, affecting CDN-loaded frameworks.

## Required checklists
- `.claude/checklists/security.md` — CSP, message source validation, DOM injection XSS, remote code execution prohibition
- `.claude/checklists/performance.md` — service worker wake latency, content script injection timing, memory budget
- `.claude/checklists/accessibility.md` — popup keyboard navigation, focus trapping in modal panels
- `.claude/checklists/launch.md` — store screenshots, privacy policy, permission justification narratives, review queue timing
- `.claude/checklists/mobile.md` — Chrome Web Store Program Policies, minimal permissions principle, sensitive permission justification

## MVP scope pattern

**In MVP**
- Manifest with minimum required permissions only (fewer permissions = faster review + higher user trust)
- Core feature in popup or content script
- `chrome.storage.local` for any persisted state
- Options page for user-configurable settings
- Error handling when extension cannot access a tab (CSP restrictions, PDF viewer, chrome:// pages)
- Privacy policy page (required for any data collection, even local)
- Working in incognito if the feature is privacy-relevant (test explicitly)

**Deferred to v2**
- Side panel (Chrome 114+ only — reduced browser coverage)
- `chrome.storage.sync` (adds cross-device complexity; quota limits)
- Enterprise managed storage (`chrome.storage.managed`)
- Devtools panel
- Firefox / Safari port
- Cross-browser automated CI matrix
- Keyboard command shortcuts (`chrome.commands`)

## Production risks

| Risk | Severity | Mitigation |
|---|---|---|
| XSS via DOM manipulation in content scripts | P0 | Never use `innerHTML` with page data; use `textContent`; sanitise with DOMPurify; use shadow DOM to isolate injected UI |
| Remote code execution (violates MV3 / store policy) | P0 | No `eval()`, `new Function()`, or dynamically fetched scripts; all logic must be bundled at load time |
| Overly broad host permissions triggering store rejection | P0 | Request `activeTab` instead of `<all_urls>` where possible; justify any broad permissions in store listing |
| Message injection from malicious page to service worker | P0 | Always verify `sender.origin` and `sender.tab` in `onMessage` listeners; never trust message content without validation |
| Sensitive data in `chrome.storage.sync` (syncs to Google servers) | P0 | Store credentials and PII only in `chrome.storage.local`; never in `sync` |
| Service worker terminated mid-operation (MV3) | P1 | Use `chrome.offscreen` documents or `chrome.alarms` to keep work alive; persist state to `storage` before long async ops |
| Extension update breaking active content scripts (no reload) | P1 | Handle `chrome.runtime.onInstalled` to refresh active tabs or gracefully degrade stale content scripts |
| Store review rejection for undeclared data usage | P1 | Privacy policy must cover all data collected; single-purpose description must match actual behaviour |
| Memory leak in long-lived content scripts on SPAs | P1 | Observe page lifecycle (`visibilitychange`, `beforeunload`); clean up observers and intervals |
| Extension silently failing on CSP-protected pages | P2 | Detect injection failure gracefully; log to service worker; surface a helpful UI state to user |

## Launch requirements
- Manifest declares only the minimum permissions; every sensitive permission (`tabs`, `<all_urls>`, `history`, `cookies`) has a written justification ready for store review
- Extension tested on Chromium, Chrome Stable, and (if cross-browser) Firefox latest
- Content scripts tested on pages with strict CSP to ensure graceful degradation
- Privacy policy published at a stable URL and linked in store listing and options page
- Service worker wake-up tested: popup and alarms function after 30+ s of idle
- All `chrome.storage` reads wrapped in error handlers (storage can be unavailable in incognito/guest)
- Store listing complete: icon (128 px), screenshots (1280×800), description, support email
- No hardcoded API keys or secrets in the bundled extension (minified code is inspectable)
- Automated Playwright extension test covering the happy-path user flow runs in CI

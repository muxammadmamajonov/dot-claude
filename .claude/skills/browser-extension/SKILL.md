---
name: browser-extension
description: >
  Activate when the project is a browser extension (Chrome, Firefox, Edge, Safari Web Extension).
  Triggers on: manifest.json with "manifest_version", keywords like "content script",
  "background service worker", "popup", "web_accessible_resources", or Chrome Web Store / AMO submission.
---

# Browser Extension Development

## When to use
- New extension scaffold from scratch (MV3)
- Adding a content script, background worker, popup, options page, or side panel to an existing extension
- Migrating a Manifest V2 extension to Manifest V3
- Preparing a submission for Chrome Web Store, Firefox AMO, or Edge Add-ons
- Debugging cross-browser permission or messaging issues

## Workflow

1. **Classify the extension type** — decide which surfaces are needed:
   | Surface | File | Purpose |
   |---------|------|---------|
   | Background | `background/service-worker.js` | Long-running logic, alarms, storage sync |
   | Content script | `content/index.js` | Injected into host pages; DOM access |
   | Popup | `popup/popup.html + popup.js` | Toolbar icon click UI (ephemeral) |
   | Options page | `options/options.html` | Persistent settings UI |
   | Side panel | `sidepanel/panel.html` | Chrome 114+ persistent side panel |
   | DevTools panel | `devtools/devtools.html` | Page inspector integration |

2. **Write `manifest.json` (MV3 only)** — required fields:
   ```json
   {
     "manifest_version": 3,
     "name": "…",
     "version": "1.0.0",
     "description": "…",
     "permissions": [],
     "host_permissions": [],
     "background": { "service_worker": "background/service-worker.js" },
     "action": { "default_popup": "popup/popup.html" },
     "content_scripts": [],
     "web_accessible_resources": []
   }
   ```
   Request the minimum permission set; justify every entry in a comment block above the manifest.

3. **Implement messaging architecture** — choose ONE pattern and stick to it:
   - **Short-lived**: `chrome.runtime.sendMessage` / `onMessage` — fire-and-forget between popup and background.
   - **Long-lived**: `chrome.runtime.connect` / `Port` — streaming data from content script to background.
   - Never call DOM APIs from the service worker; delegate to content scripts via `chrome.tabs.sendMessage`.

4. **Handle storage correctly**:
   - User preferences → `chrome.storage.sync` (≤100 KB, synced across devices).
   - Large / sensitive data → `chrome.storage.local` (≤10 MB).
   - Session state (cleared on browser close) → `chrome.storage.session` (MV3 only).
   - Always handle `chrome.runtime.lastError` after every storage call.

5. **Content-Security-Policy** — MV3 default CSP blocks `eval` and inline scripts. Serve all scripts from extension files; never inject `<script>` tags with inline code.

6. **Cross-browser compatibility**:
   - Use the `webextension-polyfill` package (`mozilla/webextension-polyfill`) to normalize `chrome.*` vs `browser.*` APIs.
   - Test in Chrome Canary, Firefox Nightly, and Edge Dev before release.
   - Firefox requires `browser_specific_settings.gecko.id` in manifest.

7. **Build pipeline**:
   - Bundle with Vite + `vite-plugin-web-extension` or webpack + `copy-webpack-plugin`.
   - Use separate entry points per surface; do not bundle them together.
   - Output a `dist/` folder; zip it with `web-ext build` for store submission.

8. **Security audit before submission** — run through `.claude/checklists/security.md` plus:
   - No `"<all_urls>"` unless unavoidable; prefer specific origins.
   - `content_security_policy` explicitly set; no `unsafe-eval`, no `unsafe-inline`.
   - All external API calls go through the background service worker, not content scripts.
   - Never store auth tokens in `localStorage` on the host page; use `chrome.storage.local`.

9. **Store submission checklist**:
   - 128×128 icon (PNG, no alpha border), 440×280 promotional tile.
   - Privacy policy URL if any `host_permissions` or personal data is collected.
   - Single-purpose declaration matches `"description"` exactly.
   - Chrome Web Store review typically takes 1–3 business days; plan accordingly.

10. **Version & update cycle** — bump `"version"` in manifest for every release; the browser auto-updates within 24 h. Use `chrome.runtime.onInstalled` to migrate storage schema on update.

## Standards

**Do:**
- Keep the service worker stateless — it can be killed at any time; persist everything to `chrome.storage`.
- Use `chrome.alarms` instead of `setInterval` in the background; alarms survive worker restarts.
- Declare `"content_scripts"` `"run_at": "document_idle"` unless you explicitly need `document_start`.
- Isolate business logic in plain `.js` modules importable by both popup and service worker.
- Write end-to-end tests with `puppeteer` + `puppeteer-extra-plugin-stealth` or `playwright` with extension loading.

**Do not:**
- Use `chrome.tabs.executeScript` for code injection — use declarative content scripts instead.
- Include `node_modules` in the extension zip.
- Persist JWTs or API keys in `chrome.storage.sync` (not encrypted at rest on all platforms).
- Request `"tabs"` permission just to get the current URL — use `"activeTab"` instead.
- Access cross-origin resources directly from content scripts — proxy through the background worker.

## Common mistakes to avoid

- **Service worker going idle**: MV3 service workers terminate after ~30 s of inactivity. Use `chrome.alarms` or an active `Port` connection to keep alive only when genuinely needed — not to fight the lifetime model.
- **`chrome.runtime.lastError` swallowing**: Every async `chrome.*` callback must check `chrome.runtime.lastError`; unchecked errors cause silent failures.
- **Popup script assuming DOM is ready**: Wrap popup logic in `DOMContentLoaded`; `popup.html` is destroyed on close — never cache popup DOM references in the background.
- **Missing `web_accessible_resources`**: Injected iframes or images from the extension package fail silently if not listed here.
- **Forgetting Firefox's strict CSP for AMO**: Firefox AMO review rejects any use of `eval` even if Chrome accepts it.
- **Version not bumped**: Auto-update only triggers if the version string increases; patch changes without a version bump never reach users.
- **Overly broad `host_permissions`**: Requesting `"<all_urls>"` triggers a manual Chrome Web Store review and lowers user trust score.

## Output format

A complete extension project looks like:

```
manifest.json
background/
  service-worker.js
content/
  index.js
  styles.css
popup/
  popup.html
  popup.js
options/
  options.html
  options.js
icons/
  16.png  48.png  128.png
_locales/en/messages.json
tests/
  e2e/
    extension.test.js
package.json
vite.config.js (or webpack.config.js)
```

Reference architecture template: `.claude/templates/architecture.md`

## Related checklists
- `.claude/checklists/security.md` — permission minimization, CSP, secret storage
- `.claude/checklists/launch.md` — store submission readiness

## Related agents
- `.claude/agents/engineering/` — feature implementation workflow
- `.claude/agents/quality/` — QA and testing strategy
- `.claude/agents/stack/web/` — web frontend patterns (popup/options UI)

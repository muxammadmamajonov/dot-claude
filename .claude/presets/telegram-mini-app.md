---
description: Preset for Telegram Mini Apps (TMA / WebApps) — a web app rendered inside Telegram via the WebApp SDK, paired with a bot backend. Use when the project is a Telegram Mini App, uses `@twa-dev/sdk` / `window.Telegram.WebApp`, validates `initData`, or ships inside a Telegram bot. Activate on "Telegram mini app", "TMA", "Telegram WebApp", "tg mini app", "bot web app".
---

# Preset — Telegram Mini App (TMA)

## When this preset applies
The product runs **inside Telegram** as a WebApp (Mini App): a web frontend launched from a bot/menu,
talking to a bot backend, using the Telegram WebApp SDK for identity, theme, and native controls. It is
**web technology** (HTML/CSS/JS/TS, usually React/Vue/Svelte/Vanilla) — so it reuses the full web layer
(`.claude/orchestration/web-routing-matrix.md`) plus the Telegram-specific concerns below. It is **not**
a native app; treat native-mobile rows as out of scope unless a companion native app exists.

## Recommended agents
- Frontend build: `.claude/agents/engineering/frontend-engineer.md` + the matched `.claude/agents/stack/web/*` engineer.
- Bot backend / API: `.claude/agents/engineering/backend-engineer.md` + `.claude/agents/engineering/api-architect.md`.
- UI/UX: `.claude/agents/design/ui-ux-designer.md` + `.claude/agents/design/mobile-ux-specialist.md` (it renders on phones; touch targets, safe areas, keyboard).
- Security: `.claude/agents/quality/security-auditor.md` + `.claude/agents/quality/auth-permission-reviewer.md` (initData validation is the crux).
- Real-time / payments / AI as needed: `realtime-engineer`, `payments-engineer`, `ai-ml-engineer`.

## Recommended skills
`.claude/skills/web/SKILL.md`, the matched framework skill (`react-next`/`vue-nuxt`/…), `.claude/skills/security/SKILL.md`, `.claude/skills/api-design/SKILL.md`, `.claude/skills/ui-ux-design/SKILL.md`. Prefer the installed `frontend-design` skill for visual polish.

## Recommended stack-matrix entries
`.claude/stack-matrix/web.md`, `.claude/stack-matrix/backend.md`, `.claude/stack-matrix/auth-identity.md`, `.claude/stack-matrix/realtime.md` (if live updates), `.claude/stack-matrix/payments.md` (if selling).

## Recommended checklists
`.claude/checklists/web-production.md`, `.claude/checklists/security.md`, `.claude/checklists/privacy-compliance.md`, `.claude/checklists/accessibility.md`, `.claude/checklists/performance.md`.

## Recommended templates
`.claude/templates/product-spec.md`, `.claude/templates/api-spec.md`, `.claude/templates/security-model.md`, `.claude/templates/threat-model.md`.

## Telegram-specific concerns (the part the generic web layer misses)
- **`initData` validation is mandatory and server-side.** Verify the HMAC-SHA-256 signature of `Telegram.WebApp.initData` against the bot token on the **backend** before trusting the user id. Never trust `initDataUnsafe` on the client for auth. Check `auth_date` freshness to block replay. This is the #1 TMA security mistake → treat a missing/al-client check as **P0**.
- **Identity model:** the Telegram user id from validated initData is the identity; issue your own session/JWT after validating. Don't roll a second password system unless the product needs accounts outside Telegram.
- **Theme & viewport:** honor `themeParams` (light/dark + accent) and `viewportStableHeight`; handle `expand()`, safe areas, and the on-screen keyboard. Use `BackButton`, `MainButton`, `HapticFeedback`, and `showPopup` instead of bespoke web equivalents.
- **Lifecycle:** call `ready()` once the UI is mounted; handle `viewportChanged`/`themeChanged`; persist state server-side or in `CloudStorage` (per-user) rather than relying on `localStorage`, which can be cleared in the in-app webview.
- **Payments:** use Telegram payments / Stars for digital goods where required; for external web payments follow the bot platform rules. Validate purchases server-side.
- **Bot backend:** webhook signature/secret verification, idempotent update handling, rate limiting; keep the bot token server-side only.
- **Performance:** the webview runs on phones — small bundle, fast first paint, image optimization; test on low-end Android.

## Discovery questions
- Is identity Telegram-only, or are there accounts/roles beyond Telegram?
- Does it sell anything (Telegram payments / Stars / external)? Any KYC/region constraints?
- Real-time needs (live updates, chat)? Offline expectations inside the webview?
- Which Telegram surfaces (inline button, menu button, attachment menu, full-screen)?

## Key risks
- **Trusting client `initDataUnsafe`** for auth → account takeover. Validate server-side. (P0)
- Bot token leaked to the client. (P0)
- Assuming desktop browser behavior — it's a constrained mobile webview (storage clearing, keyboard, back button).
- Skipping `auth_date`/replay checks; missing webhook verification on the bot side.

## Verification
Treat as a web project for gates (`/web-audit`, `/web-readiness`) **plus** an explicit initData-validation
and bot-webhook security check via `auth-permission-reviewer` + `security-auditor`. Done when initData is
validated server-side, the bot token never reaches the client, theme/viewport/back-button behave, and the
web production + security gates pass.

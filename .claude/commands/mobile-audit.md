---
description: Mode- and scope-driven mobile audit. Detects the platform (React Native, Expo, Flutter, native iOS, native Android, KMP, Ionic/Capacitor, PWA, Telegram Mini App) and routes to the right specialists for a chosen area — returning ranked, evidence-backed findings, never fabricated results. Use for "audit my mobile app", "React Native/Flutter/iOS/Android review", "is this store-ready", offline/security/performance/notification/IAP review.
argument-hint: <scope: react-native|expo|flutter|ios|android|kmp|pwa|telegram|offline|networking|notifications|payments|security|performance|accessibility|full> [--mode audit-only|fix-and-verify|production-hardening|app-store-readiness]
---

# /mobile-audit

## Purpose
One token-efficient entry point for auditing a mobile app. It detects the platform, activates only
the specialists the chosen **scope** needs (see `.claude/orchestration/mobile-routing-matrix.md`),
runs them against the mobile checklists, and returns a single ranked report — serving read-only
review, fix-and-verify, production-hardening, or app-store-readiness via the **mode**.

## When to use
- "Audit my mobile app" / "review the React Native / Flutter / iOS / Android code".
- Targeted: offline/sync, networking, security (MASVS), performance, notifications, payments/IAP, accessibility.
- Before a store submission ("is this store-ready?") → use `--mode app-store-readiness` or `/store-readiness`.

## Workflow
1. **Map & detect platform.** `.claude/agents/core/codebase-mapper.md` → `docs/state/codebase-map.md`; classify RN/Expo/Flutter/native/KMP/Ionic/PWA/Telegram via the routing matrix's detection table.
2. **Resolve scope → specialists** (routing matrix). Examples:
   - `react-native`/`expo`/`flutter`/`ios`/`android`/`kmp` → the matching `stack/mobile/*` engineer + `mobile-ux-specialist`; checklists `mobile`, `accessibility`.
   - `offline` → mobile-engineer + database-architect; checks: local store, sync, conflict resolution, migrations, cache invalidation.
   - `networking` → mobile-engineer + api-architect; checks: retry/timeout/cancel, offline queue, optimistic updates, reachability, pagination.
   - `security` → `quality/mobile-security-auditor` (MASVS) + auth-permission-reviewer; checklists `security`, `privacy-compliance`.
   - `performance` → performance-engineer + mobile-engineer; startup, jank/frame rate, memory, app/bundle size, list virtualization.
   - `accessibility` → accessibility-auditor + mobile-ux-specialist; VoiceOver/TalkBack, dynamic type, contrast, touch targets, focus order.
   - `notifications` → mobile-engineer + integration-engineer; FCM/APNs, channels/categories, deep-link, background handling, badges.
   - `payments` → payments-engineer + mobile-engineer; IAP/StoreKit/Play Billing, receipt validation, entitlements, store compliance.
   - `pwa` → web layer (`/web-audit`); `telegram` → web layer + `presets/telegram-mini-app` (initData validation, theme, viewport, back button).
   - `full` → run the platform + security + performance + accessibility scopes **concurrently**, then dedupe.
3. **Run gates** read-only against the checklist; mark each item pass/fail with `file:line` evidence. Run real commands (build, `flutter test`, `detox test`, etc.) or mark "unverified" — never fabricate.
4. **Apply mode.** `audit-only` stops. `fix-and-verify` fixes P0/P1 then rebuilds + reruns the relevant tests and re-audits. `production-hardening` drives `.claude/checklists/mobile-production.md`. `app-store-readiness` drives `.claude/checklists/app-store-readiness.md`.
5. **Reconcile, rank P0→P3, risk review, summary** (crash / store-rejection / regression risk; reversibility).

## Agents used
`core/codebase-mapper`, `core/orchestrator`, and the scope's specialists: `stack/mobile/*`,
`engineering/{mobile-engineer,mobile-release-engineer,mobile-e2e-engineer,payments-engineer}`,
`quality/{mobile-security-auditor,performance-engineer,accessibility-auditor,qa-engineer}`,
`design/mobile-ux-specialist`. `core/code-reviewer` verifies diffs in fix-and-verify.

## Skills used
`.claude/skills/mobile/SKILL.md`, plus scope: `react-native`, `flutter`, `native-ios`, `native-android`, `security`, `performance`, `testing`, `payments`. Prefer the installed `vercel-react-native-skills` for RN idioms.

## Expected outputs
| Output | Path |
|---|---|
| Repo map (platform detected) | `docs/state/codebase-map.md` |
| Audit report (ranked P0–P3) | `docs/reports/mobile-audit-<scope>-<date>.md` |
| Fixes (fix-and-verify) | code diff + test results |
| Risk records | `docs/decisions/` |

## Stop conditions
- No mobile project detected → suggest `/route` (it may be a web/PWA → `/web-audit`).
- Build/tests can't run (no Xcode/Android SDK/simulator) → report which, mark items unverified, never fake a pass.
- A P0 (hardcoded secret, insecure storage of tokens, missing cert validation, store-blocking issue) → surface immediately.

## Final report format
```
## /mobile-audit — <scope> (<mode>)
Platform: <RN|Expo|Flutter|iOS|Android|KMP|…>  |  Scope: <…>  |  Mode: <…>
### Findings (N): P0 <n> · P1 <n> · P2 <n> · P3 <n>
- [P0] <title> — <file:line> — evidence: <…> — fix: <…>
### Fixed & verified (fix-and-verify): <list + how proven (command + result)>
### Risk review: <crash / store-rejection / regression ; reversibility>
### Verdict: <ship / fix-first / blocked>  ·  Next: <command, e.g. /store-readiness>
```

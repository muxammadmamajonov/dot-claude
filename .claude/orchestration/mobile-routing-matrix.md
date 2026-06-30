# Mobile Engineering Routing Matrix — the elite mobile team, assembled per task

The orchestrator's mobile routing layer. Detects the mobile platform/framework, activates the
**minimal** specialist set, picks an operating **mode**, and runs the right verification loop.
Complements `.claude/orchestration/routing-matrix.md` (universal) and
`.claude/orchestration/web-routing-matrix.md` (web; also covers PWA & Telegram Mini Apps, which are
web tech). Activate only what the task needs — never load all mobile agents at once.

## Platform detection (first step)
Run `.claude/agents/core/codebase-mapper.md`; classify the mobile target from signals:

| Signal | Target → primary specialist |
|---|---|
| `package.json` + `react-native` (no `expo`) | React Native → `stack/mobile/react-native-engineer` |
| `app.json`/`app.config.*` + `expo` | Expo → `stack/mobile/expo-engineer` |
| `pubspec.yaml` | Flutter → `stack/mobile/flutter-engineer` |
| `*.xcodeproj`/`*.swift`/`Package.swift` (no RN/Flutter) | Native iOS → `stack/mobile/native-ios-swift-engineer` |
| `build.gradle(.kts)` + `AndroidManifest.xml` (no RN/Flutter) | Native Android → `stack/mobile/native-android-kotlin-engineer` |
| `*.kt` shared module + `androidMain/iosMain` | KMP → `stack/mobile/kotlin-multiplatform-engineer` |
| `capacitor.config.*`/`ionic.config.json` | Ionic/Capacitor → `stack/mobile/ionic-capacitor-engineer` |
| Telegram WebApp SDK / `web_app` usage | Telegram Mini App → preset `presets/telegram-mini-app` + web layer |
| manifest + service worker, installable | PWA → web-routing-matrix (frontend-engineer) |
| **Mixed** (web dashboard + mobile app + backend) | union the relevant rows; keep web and mobile teams separate per surface |

## Operating modes (orchestrator picks ONE)
audit-only · fix-and-verify · production-hardening · ui-ux-polish · security-review (MASVS) ·
performance-review · release-readiness · **app-store-readiness** · documentation. State the mode up front.

## Task → team (mobile)
| Mobile task | Lead | Support | Skills | Checklists |
|---|---|---|---|---|
| Map / classify | `core/codebase-mapper` | — | discovery, project-classification | — |
| App architecture | `core/solution-architect` | `engineering/mobile-engineer` | architecture, mobile | mobile, architecture |
| RN / Expo build | `stack/mobile/{react-native,expo}-engineer` | mobile-ux-specialist | react-native, mobile | mobile, accessibility |
| Flutter build | `stack/mobile/flutter-engineer` | mobile-ux-specialist | flutter, mobile | mobile, accessibility |
| Native iOS | `stack/mobile/native-ios-swift-engineer` | mobile-ux-specialist | native-ios | mobile, accessibility |
| Native Android | `stack/mobile/native-android-kotlin-engineer` | mobile-ux-specialist | native-android | mobile, accessibility |
| KMP shared logic | `stack/mobile/kotlin-multiplatform-engineer` | native iOS/Android eng | native-ios, native-android | mobile |
| Mobile UI/UX & design system | `design/mobile-ux-specialist` + `design/design-system-architect` | accessibility-designer | ui-ux-design + installed `frontend-design` | accessibility, mobile |
| Mobile accessibility (VoiceOver/TalkBack) | `quality/accessibility-auditor` | mobile-ux-specialist | ui-ux-design | accessibility |
| Offline / sync / storage | `engineering/mobile-engineer` | database-architect | mobile, data-modeling | mobile, data-model |
| API / networking (retry, offline queue) | `engineering/mobile-engineer` | api-architect, integration-engineer | api-design, realtime | api, backend |
| Auth + mobile security (MASVS) | `quality/mobile-security-auditor` | auth-permission-reviewer, security-auditor | security | security, privacy-compliance |
| Permissions / device APIs | `engineering/mobile-engineer` | mobile-security-auditor | mobile | mobile, privacy-compliance |
| Push notifications | `engineering/mobile-engineer` (+ integration-engineer) | — | mobile, messaging-queues | mobile |
| Payments / IAP | `engineering/payments-engineer` | mobile-engineer | payments | mobile, privacy-compliance |
| Performance (startup, jank, app size) | `quality/performance-engineer` | mobile-engineer | performance | performance |
| QA / tests | `quality/qa-engineer` + `quality/test-automation-engineer` | — | testing | qa |
| Mobile E2E (device) | `engineering/mobile-e2e-engineer` | qa-engineer | testing | qa |
| CI/CD, signing, store submit | `engineering/mobile-release-engineer` | devops-engineer | devops | release-rollback, app-store-readiness |
| Store readiness | `engineering/mobile-release-engineer` + `quality/production-readiness-auditor` | privacy-compliance-auditor | production-readiness | app-store-readiness, mobile-production |
| Observability (crash/ANR/RUM) | `quality/reliability-engineer` | mobile-engineer | observability | observability, incident-response |
| Privacy / store compliance | `quality/privacy-compliance-auditor` | mobile-release-engineer | security | privacy-compliance, app-store-readiness |
| On-device / mobile AI | `engineering/ai-ml-engineer` | mobile-engineer | ai-ml | ai-ml, security |
| Bug fix / refactor | `engineering/{bug-fix,refactoring}-specialist` | the framework specialist | testing, architecture | qa |

## High-value external skills (via /find-skills)
- **`vercel-react-native-skills`** (vercel-labs, ~154k installs, likely installed) — prefer for RN/Expo idioms.
- **`frontend-design`** (anthropics, ~600k) — mobile UI/visual polish.
- Confirmed real needs we cover natively (community skills were thin): MASVS security (`mobile-security-auditor`), Maestro/Detox E2E (`mobile-e2e-engineer`), Telegram Mini Apps (`presets/telegram-mini-app`).

## Verification loops (fix-and-verify / hardening / release / app-store)
change → prove (build the app; run unit/widget + the relevant device/E2E tests for real; never fabricate)
→ re-audit the changed area with its checklist → risk review (crash/regression/store-rejection risk; reversible?)
→ final summary. `core/code-reviewer` checks diffs before done.

## Commands
`/mobile-audit <scope> [--mode]`, `/store-readiness` (App Store + Google Play), plus universal
`/route`, `/audit-security`, `/audit-performance`, `/fix-bugs`, `/refactor-safely`, `/create-tests`,
`/prepare-launch`, `/commit-ready`.

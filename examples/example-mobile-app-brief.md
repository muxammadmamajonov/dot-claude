# Example Project Brief — "Streak" (Consumer Mobile App)

> A worked example showing how the Project OS classifies and scopes a cross-platform mobile app. Not a real product — a realistic illustration of the `/start-project` → discovery → classification → stack → MVP flow.

## One-line idea
A habit-tracking mobile app that helps people build daily routines with streaks, reminders, and gentle social accountability.

## Classification result
- **Project type:** Mobile app (cross-platform, iOS + Android)
- **Preset:** [mobile-app](../.claude/presets/mobile-app.md)
- **Cross-cutting concerns:** offline-first (logging works with no signal), push notifications (reminders), payments (subscription / freemium), analytics & funnels, privacy (personal behavioral data).
- **Domain experts pulled in:** none heavy; light consult with [social-platform-domain-expert](../.claude/agents/domain/social-platform-domain-expert.md) for the accountability feed.

## Founder discovery answers
- **Problem:** People start habits but quit by week two; existing apps feel like spreadsheets or guilt machines.
- **Target users:** 22–40, already use a fitness/journaling app, want lightweight structure — not gamified noise.
- **Value proposition:** The fastest way to log a habit (one tap from the lock screen) plus a small circle of friends who see your streak.
- **Constraints:** Solo founder + one contract designer; $15k budget; 10-week runway to TestFlight beta; must work offline (gym basements, subways).
- **Success metrics:** D7 retention ≥ 35%; ≥ 3 habits logged/user/week; free→paid conversion ≥ 4% by week 4.
- **Key risks:** Notification fatigue → churn; thin offline-sync edge cases; App Store subscription review.
- **Budget / timeline:** $15k; beta in 10 weeks, public launch in 16.

## Recommended stack (with rationale)
- **Client:** Flutter — one codebase for iOS + Android, strong offline + local DB story, fits solo budget. See [.claude/stack-matrix/mobile.md](../.claude/stack-matrix/mobile.md).
- **Local store:** SQLite (drift) for offline-first logging; sync queue to backend.
- **Backend:** Supabase (Postgres + Auth + Realtime) — minimal ops, RLS for the friend feed, generous free tier. See [.claude/stack-matrix/database.md](../.claude/stack-matrix/database.md).
- **Payments:** RevenueCat over App Store / Play billing (handles receipts + entitlements). See [.claude/stack-matrix/payments.md](../.claude/stack-matrix/payments.md).
- **Push:** Firebase Cloud Messaging. **Analytics:** PostHog.

## MVP scope
**In:** create habit, one-tap log (incl. home-screen widget), streak counter, local reminders, offline logging + sync, email/Apple/Google sign-in, add up to 5 friends + see their streaks, single paid tier (unlimited habits + history).
**Deferred:** Android widget polish, habit templates marketplace, web app, teams/challenges, Apple Health import, localization.

## First 3 safe phases
1. **Walking skeleton** — log a habit offline, persist to SQLite, sync to Supabase when online, see the streak update. Proves the riskiest path (offline→sync). → [/build-prototype](../.claude/commands/build-prototype.md)
2. **Reminders + auth** — local notifications, sign-in, account-scoped data with RLS. → [/implement-feature](../.claude/commands/implement-feature.md)
3. **Friends feed + paywall** — read-only streak feed, RevenueCat paywall, then run [/audit-security](../.claude/commands/audit-security.md) + [accessibility checklist](../.claude/checklists/accessibility.md).

---
**Next command to run:** [/start-project](../.claude/commands/start-project.md) (it will confirm this classification, then route to [/interview-founder](../.claude/commands/interview-founder.md) and [/create-specs](../.claude/commands/create-specs.md)).

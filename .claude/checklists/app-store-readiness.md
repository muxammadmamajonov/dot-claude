# App Store & Google Play Readiness Checklist

The submission gate for shipping to the **Apple App Store** and **Google Play**. Pairs with
`.claude/checklists/mobile-production.md` (app quality) — this one covers store policy, metadata,
signing, and review survival. Severity: **P0** blocker (rejection/cannot submit) · **P1** important ·
**P2** hardening · **P3** backlog. Skip the store you're not shipping to.

## P0 — Blockers (submission will fail or be rejected)

### Both stores
- [ ] **Privacy policy URL** live and accurate; reachable from the app and the store listing.
- [ ] **Account deletion** available in-app (and a path to delete server data) if the app has accounts — required by both stores.
- [ ] **Data collection disclosure complete & truthful**: Apple **Privacy Nutrition Labels** and Google **Data safety** form match what the app + SDKs actually collect (analytics, ads, crash, location).
- [ ] **Permissions justified**: each requested permission is used; Apple purpose strings present; no permissions the feature set doesn't need (a top rejection/removal cause).
- [ ] **No secrets in the binary**; third-party SDKs reviewed for policy compliance (ads/tracking SDKs disclosed).
- [ ] **Login**: if any third-party/social login is offered, required equivalents are met (e.g. an alternative that meets store policy); demo account / credentials provided to reviewers if login-gated.
- [ ] **Payments use the right rails**: digital goods/subscriptions go through **Apple IAP / Google Play Billing** (not an external processor) where store policy requires; physical goods/services use external payment correctly.

### Apple App Store
- [ ] Valid **distribution signing** (provisioning profile + distribution cert); correct bundle id; app builds an uploadable archive.
- [ ] **App Tracking Transparency** prompt implemented if the app tracks users across apps/sites; `NSUserTrackingUsageDescription` present.
- [ ] No private APIs, no hidden/placeholder features; app is functional & complete (no "beta"/"demo" in production); minimum iOS target sane.
- [ ] Required screenshots for current device sizes; app icon (no alpha); export-compliance answered.

### Google Play
- [ ] **App signing** via Play App Signing; **target API level** meets Google's current minimum; 64-bit + **AAB** (not APK) upload.
- [ ] Content rating questionnaire completed; **Data safety** section submitted; foreground-service & sensitive-permission (location/SMS/etc.) declarations justified.
- [ ] Store listing complete (title, short/full description, feature graphic, screenshots) with no policy-violating claims.

## P1 — Important (before or right after launch)

- [ ] **Staged/phased rollout** configured (Play staged rollout / App Store phased release); ability to halt.
- [ ] **Crash-free rate** acceptable on internal/beta track (TestFlight / Play internal testing) before production.
- [ ] Release notes written; version & build number incremented and unique.
- [ ] Deep links / universal links / app links verified (associated-domains / `assetlinks.json` / AASA file served correctly).
- [ ] Reviewer notes explain any non-obvious flows; demo content seeded so review can exercise the app.
- [ ] Age rating / content rating matches actual content; restricted content gated.

## P2 — Hardening

- [ ] Localized store metadata & screenshots for target markets; localized in-app strings.
- [ ] Pre-launch report (Play) reviewed; TestFlight feedback triaged.
- [ ] App size within cellular-download limits; on-demand resources / asset packs where large.
- [ ] Subscription management, restore-purchases, and grace-period/billing-retry handling verified in sandbox.

## P3 — Post-launch / backlog (track; never blocks)

- [ ] Store A/B testing of listing assets; ASO (keywords, conversion) review.
- [ ] In-app review prompt at a sensible moment; ratings monitoring.
- [ ] Automated store submission via Fastlane/EAS Submit wired into CI for the next release.

## How to use

**When:** before every store submission and major release. **Who:** `mobile-release-engineer` leads;
`privacy-compliance-auditor` owns the privacy/data-safety items; `production-readiness-auditor`
confirms quality via `.claude/checklists/mobile-production.md`. **Command:** `/store-readiness` runs this
checklist and emits a go/no-go. P0 blocks submission; P1 → fix before/just-after launch; P2–P3 → backlog.
Verify against the **current** Apple App Store Review Guidelines and Google Play policies (they change) —
mark an item passed only with real evidence (a screenshot of the form, a successful upload, a TestFlight build).

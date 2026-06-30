# Google Play Submission — reference

Step-by-step for shipping an Android app to Google Play (native, React Native, Expo, or Flutter).
Read this for the `app-store-readiness` mode or `/store-readiness --store google`. Gate with
`.claude/checklists/app-store-readiness.md` first; verify against the **current** Google Play policies
and target-API requirements (they change yearly). Never commit keystores or service-account keys —
reference them from CI.

## 1. App & signing setup
- Create the app in **Play Console**; set package name (immutable once published).
- Enable **Play App Signing**: you upload with an **upload key**; Google holds the app signing key.
  Generate and **back up the upload keystore** — losing it requires a key reset.
- Service account: create a Google Cloud service account, grant it Play Console release permissions,
  download the **JSON key** (referenced via `GOOGLE_PLAY_SERVICE_ACCOUNT_JSON`, git-ignored).

## 2. Build artifact
- Ship an **Android App Bundle (.aab)**, not an APK. Enable 64-bit; shrink with **R8/ProGuard**.
- Meet the **current minimum target API level** (Google raises it each year; below it = cannot submit).
- Set versionCode (must increase every upload) and versionName.

## 3. Build & upload
- **Fastlane:** `gradle(task: 'bundleRelease')` then `upload_to_play_store(track: 'internal')`. See the
  scaffolded `fastlane/Fastfile` (`android_beta`, `android_release` with staged `rollout`).
- **Expo EAS:** `eas build -p android --profile production` then `eas submit -p android`.
- Tracks: **internal → closed (alpha/beta) → production**. Promote upward after validation.

## 4. Required declarations & compliance (top rejection causes)
- **Data safety** form must match what the app + SDKs collect/share (the Android analog of Apple's
  privacy labels); inaccuracy = enforcement.
- **Privacy policy URL** live; **account deletion** path (in-app + a web URL to request deletion).
- **Permissions & APIs:** justify sensitive permissions; foreground-service types declared; restricted
  permissions (SMS/Call Log, All files access, background location) need a declaration + valid use case.
- **Content rating** questionnaire completed; target audience set (COPPA/Families policy if kids).
- **Payments:** digital goods use **Google Play Billing**; physical goods use external payment per policy.
- Store listing: title, short/full description, feature graphic, screenshots — no misleading claims.

## 5. Beta → rollout → halt
- Validate on the **internal/closed** track; review the **pre-launch report** (Google runs your app on
  real devices and flags crashes/accessibility/security).
- Production via **staged rollout** (start ~10%); increase gradually. **Halt rollout** in Play Console if
  ANR/crash rate rises; ship a hotfix (a new versionCode) — Play has no "unpublish a version" beyond halt.

## 6. Common rejections to pre-empt
Inaccurate Data safety; below target API; APK instead of AAB; undeclared restricted permissions; missing
account deletion; deceptive listing; non-Play-Billing for digital goods; broken functionality found by the
pre-launch report. Run `/store-readiness` to catch these first.

## Validation
Done when: a signed `.aab` reaches the internal track, Data safety + permissions declarations are accurate,
target API + account deletion are satisfied, the pre-launch report is clean, and the readiness checklist's
Google P0 items pass — each with real evidence (a successful upload, the submitted form), never assumed.

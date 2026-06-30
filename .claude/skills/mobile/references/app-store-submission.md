# Apple App Store Submission — reference

Step-by-step for shipping an iOS app to the App Store (native, React Native, Expo, or Flutter).
Read this when running the `app-store-readiness` mode or `/store-readiness --store apple`. Gate with
`.claude/checklists/app-store-readiness.md` first; verify against the **current** App Store Review
Guidelines (they change). Never commit signing assets or credentials — reference them from CI.

## 1. Identifiers & capabilities
- Register the **bundle id** in the Apple Developer portal; enable only the capabilities the app uses
  (Push, Sign in with Apple, Associated Domains, IAP, …). Unused entitlements cause review questions.
- Create the app record in **App Store Connect** (name, primary language, SKU).

## 2. Signing
- Prefer **App Store Connect API key** (`.p8` + key id + issuer id) over Apple ID password for CI.
- Manage certificates/profiles with **fastlane match** (encrypted git repo) or Xcode automatic signing.
  Back up the distribution certificate's private key — losing it blocks future uploads.
- Distribution method: `app-store`. Build a signed archive (IPA).

## 3. Build & upload
- **Fastlane:** `build_app(export_method: 'app-store')` then `upload_to_testflight` (beta) or
  `deliver` (store). See the scaffolded `fastlane/Fastfile` (`ios_beta`, `ios_release`).
- **Expo EAS:** `eas build -p ios --profile production` then `eas submit -p ios`.
- **Transporter / Xcode Organizer** also work for manual uploads.

## 4. Required metadata & compliance (top rejection causes)
- **Privacy Nutrition Labels** in App Store Connect must match what the app + every SDK collects
  (analytics, ads, crash, location). Truthfulness is enforced.
- **Privacy policy URL** live and reachable.
- **App Tracking Transparency:** if you track across apps/sites, implement the ATT prompt and add
  `NSUserTrackingUsageDescription`. Using tracking SDKs without ATT = rejection.
- **Purpose strings** (`NS*UsageDescription`) for every sensitive permission; request permissions only
  when needed, with rationale.
- **Account deletion** in-app if the app has accounts.
- **Payments:** digital goods/subscriptions must use **StoreKit IAP**; external payments only for
  physical goods/services per policy.
- Screenshots for current device sizes; app icon without alpha; export-compliance answered.

## 5. Beta → review → release
- Distribute via **TestFlight** (internal/external) and confirm a healthy crash-free rate first.
- Provide **demo account credentials** and reviewer notes for any login-gated or non-obvious flow.
- Submit for review; on approval use **phased release** (7-day automatic ramp) so you can pause if
  crash rate spikes.

## 6. Common rejections to pre-empt
Incomplete/placeholder features; broken links; requesting permissions never used; mismatched privacy
labels; missing account deletion; non-StoreKit payments for digital goods; using private APIs;
guideline 4.3 "spam/duplicate" for thin apps. Run `/store-readiness` to catch these before Apple does.

## Validation
Done when: a signed build reaches TestFlight, privacy labels + ATT + purpose strings are accurate,
account deletion exists, demo creds are attached, and the readiness checklist's Apple P0 items pass —
each with real evidence (a successful upload, the submitted form), never assumed.

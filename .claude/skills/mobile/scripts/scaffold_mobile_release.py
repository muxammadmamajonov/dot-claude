#!/usr/bin/env python3
"""scaffold_mobile_release.py — generate starter mobile release config.

Writes Fastlane and/or EAS config plus a signing `.env.example` (PLACEHOLDERS ONLY)
and a RELEASE.md runbook into a target project, so `mobile-release-engineer` starts
from a correct skeleton instead of hand-rolling one. Pure standard library, no network,
no secrets. Idempotent: never overwrites an existing file unless `--force`.

Usage:
    python3 scaffold_mobile_release.py --platform <expo|rn|flutter|ios|android> [DIR] [--force]

- expo            → eas.json (build+submit profiles) + .env.example + RELEASE.md
- rn|flutter|ios|android → fastlane/Fastfile + fastlane/Appfile + .env.example + RELEASE.md
  (Fastfile includes ios and/or android lanes as appropriate)

SAFETY: emits only placeholder env var NAMES; never real keys. Signing assets
(keystores, certs, App Store/Play credentials) must be supplied via your CI secret
store and referenced by these env vars — never committed.
"""
import os, sys, argparse

EAS_JSON = """{
  "cli": { "version": ">= 5.0.0" },
  "build": {
    "development": { "developmentClient": true, "distribution": "internal" },
    "preview": { "distribution": "internal" },
    "production": { "autoIncrement": true }
  },
  "submit": {
    "production": {
      "ios": {
        "appleId": "$EXPO_APPLE_ID",
        "ascAppId": "$EXPO_ASC_APP_ID",
        "appleTeamId": "$EXPO_APPLE_TEAM_ID"
      },
      "android": {
        "serviceAccountKeyPath": "$GOOGLE_PLAY_SERVICE_ACCOUNT_JSON",
        "track": "internal"
      }
    }
  }
}
"""

FASTFILE_IOS = """  desc "Build and upload iOS to TestFlight"
  lane :ios_beta do
    setup_ci if ENV['CI']
    # match(type: 'appstore', readonly: is_ci)  # if using fastlane match for signing
    build_app(scheme: ENV['IOS_SCHEME'] || 'App', export_method: 'app-store')
    upload_to_testflight(skip_waiting_for_build_processing: true)
  end

  desc "Release iOS to the App Store (review)"
  lane :ios_release do
    build_app(scheme: ENV['IOS_SCHEME'] || 'App', export_method: 'app-store')
    deliver(submit_for_review: false, force: true, precheck_include_in_app_purchases: false)
  end
"""

FASTFILE_ANDROID = """  desc "Build and upload Android to Play internal track"
  lane :android_beta do
    gradle(task: 'clean bundleRelease')
    upload_to_play_store(track: 'internal', aab: ENV['ANDROID_AAB_PATH'] || 'app/build/outputs/bundle/release/app-release.aab')
  end

  desc "Promote Android to production (staged rollout)"
  lane :android_release do
    upload_to_play_store(track: 'production', rollout: '0.1',
      aab: ENV['ANDROID_AAB_PATH'] || 'app/build/outputs/bundle/release/app-release.aab')
  end
"""

APPFILE_IOS = "app_identifier(ENV['IOS_BUNDLE_ID'])\napple_id(ENV['APPLE_ID'])\nteam_id(ENV['APPLE_TEAM_ID'])\n"
APPFILE_ANDROID = "package_name(ENV['ANDROID_PACKAGE_NAME'])\njson_key_file(ENV['GOOGLE_PLAY_SERVICE_ACCOUNT_JSON'])\n"

ENV_EXAMPLE = """# Mobile release — signing & store credentials (PLACEHOLDERS — fill via your CI secret store, never commit real values)
# iOS / App Store
APPLE_ID=you@example.com
APPLE_TEAM_ID=XXXXXXXXXX
IOS_BUNDLE_ID=com.example.app
IOS_SCHEME=App
# App Store Connect API key (preferred over Apple ID password)
ASC_KEY_ID=
ASC_ISSUER_ID=
ASC_KEY_P8_PATH=
# Android / Google Play
ANDROID_PACKAGE_NAME=com.example.app
GOOGLE_PLAY_SERVICE_ACCOUNT_JSON=./play-service-account.json   # path provided by CI secret; file itself is git-ignored
ANDROID_KEYSTORE_PATH=
ANDROID_KEYSTORE_PASSWORD=
ANDROID_KEY_ALIAS=
ANDROID_KEY_PASSWORD=
# Expo EAS (if using EAS Submit)
EXPO_APPLE_ID=
EXPO_ASC_APP_ID=
EXPO_APPLE_TEAM_ID=
"""

RELEASE_MD = """# Mobile Release Runbook (generated starter — edit for your project)

> Secrets come from the CI secret store and are referenced by the vars in `.env.example`.
> Back up your Android keystore and iOS signing assets — losing them blocks all future updates.

## Pre-release gate
- Run the OS gates first: `/mobile-audit full` then `/store-readiness --store both`.
- Bump marketing version + build number; write release notes.

## Build & beta
- **Expo:** `eas build --profile production --platform all` → `eas submit --profile production --platform <ios|android>`
- **Fastlane iOS:** `bundle exec fastlane ios_beta` (TestFlight)
- **Fastlane Android:** `bundle exec fastlane android_beta` (Play internal track)

## Production rollout (staged) & halt
- iOS: submit for review (`ios_release`), then release in App Store Connect with **phased release**.
- Android: `android_release` starts at 10% (`rollout: '0.1'`); increase gradually; **halt** in Play Console if crash-free rate drops.
- Hotfix: JS-only fixes may go via OTA (Expo Updates / CodePush-style); native/permission/SDK changes require a new store build.

## After release
- Watch crash-free users/sessions (Crashlytics/Sentry) and ANR/OOM for the first hours.
- Tag the release in git; record any waived store-readiness item as a risk in `docs/decisions/`.
"""

def write(path, content, force):
    if os.path.exists(path) and not force:
        return ("skip", path)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    open(path, "w", encoding="utf-8").write(content)
    return ("write", path)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--platform", required=True, choices=["expo", "rn", "flutter", "ios", "android"])
    ap.add_argument("dir", nargs="?", default=".")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    root = os.path.abspath(a.dir)
    results = []

    if a.platform == "expo":
        results.append(write(os.path.join(root, "eas.json"), EAS_JSON, a.force))
    else:
        # ios and android lanes both included for rn/flutter; single platform for ios/android
        ios = a.platform in ("rn", "flutter", "ios")
        android = a.platform in ("rn", "flutter", "android")
        fastfile = "default_platform(:ios)\n\nplatform :ios do\n" + (FASTFILE_IOS if ios else "") + "end\n"
        fastfile += "\nplatform :android do\n" + (FASTFILE_ANDROID if android else "") + "end\n" if android else ""
        appfile = (APPFILE_IOS if ios else "") + (("\n" + APPFILE_ANDROID) if android else "")
        results.append(write(os.path.join(root, "fastlane", "Fastfile"), fastfile, a.force))
        results.append(write(os.path.join(root, "fastlane", "Appfile"), appfile, a.force))

    results.append(write(os.path.join(root, ".env.example"), ENV_EXAMPLE, a.force))
    results.append(write(os.path.join(root, "RELEASE.md"), RELEASE_MD, a.force))

    print(f"# Mobile release scaffold ({a.platform}) → {root}\n")
    for action, path in results:
        mark = "created" if action == "write" else "skipped (exists; --force to overwrite)"
        print(f"  {mark}: {os.path.relpath(path, root)}")
    print("\nNext: fill .env.example via your CI secret store (never commit real values), "
          "add `play-service-account.json` / keystores to .gitignore, then run the lanes in RELEASE.md.\n"
          "Gate first with /store-readiness. See app-store-submission.md / google-play-submission.md references.")

if __name__ == "__main__":
    main()

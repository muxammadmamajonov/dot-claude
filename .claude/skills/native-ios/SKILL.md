---
name: native-ios
description: >
  Activate when building, reviewing, or debugging a native iOS application
  using Swift and SwiftUI (or UIKit where required). Covers app architecture,
  SwiftUI data flow, Swift concurrency, Core Data / SwiftData, App Store
  submission, and security hardening. Trigger on any task involving Swift
  source files, Xcode project settings, Info.plist, entitlements, or
  iOS-specific frameworks.
---

# Native iOS (Swift / SwiftUI) Skill

## When to use

- Creating or modifying SwiftUI views, view models, or UIKit view controllers
- Designing data flow with `@State`, `@StateObject`, `@EnvironmentObject`, or the Observation framework
- Integrating system frameworks (Core Location, HealthKit, StoreKit 2, ARKit, etc.)
- Configuring Xcode project settings, signing, capabilities, or schemes
- Diagnosing hangs, memory leaks, or excessive CPU in Instruments
- Preparing an app for App Store review and submission

## Workflow

1. **Confirm minimum deployment target and Swift version** — check `IPHONEOS_DEPLOYMENT_TARGET` and `SWIFT_VERSION` in the `.xcconfig` or project settings. New APIs must be guarded with `@available(iOS X, *)`.
2. **Architecture decision** (align with team before coding):
   - **SwiftUI + Observable / MVVM**: `@Observable` view models (iOS 17+) or `ObservableObject` + `@StateObject` (iOS 14+); one `@Observable` class per screen
   - **TCA (The Composable Architecture)**: use for complex multi-screen state with explicit side-effect control
   - **UIKit + Coordinators**: only for brownfield additions or when SwiftUI's capabilities are insufficient for the target OS
3. **SwiftUI view structure**:
   - Keep `View` bodies thin — extract sub-views into separate `View` structs when a body exceeds ~30 lines
   - Pass only the data a subview needs; avoid threading `@EnvironmentObject` through more than two levels
   - Use `@ViewBuilder` for conditional branching inside reusable components
4. **Swift concurrency**:
   - Mark all UI updates on `@MainActor`; annotate view models with `@MainActor` at the class level
   - Use `async/await` for network and disk I/O; use `Task { }` to bridge to the async world from synchronous contexts
   - Cancel tasks in `onDisappear` or `deinit` via `task.cancel()` or SwiftUI's `.task` modifier (auto-cancelled on disappear)
5. **Data persistence**:
   - Simple key-value: `UserDefaults` (non-sensitive) or `Keychain` (sensitive tokens/passwords via `Security` framework or `KeychainAccess` package)
   - Relational: `SwiftData` (iOS 17+) or `Core Data` with `NSPersistentCloudKitContainer` for CloudKit sync
   - Network cache: `URLCache` with appropriate cache policies; `NSCache` for in-memory object caching
6. **Networking**:
   - Use `URLSession` with `async/await`; wrap in a typed `APIClient` struct
   - Validate SSL pinning for high-security apps via `URLSessionDelegate`
   - Never store raw API responses; decode into typed `Codable` models immediately
7. **Instruments pass before release**:
   - Leaks instrument: look for retain cycles (common with closures capturing `self` strongly)
   - Time Profiler: identify hangs >250 ms on the main thread
   - Memory Graph Debugger in Xcode: catch strong reference cycles in SwiftUI view model graphs
8. **App Store preparation**:
   - Privacy manifest (`PrivacyInfo.xcprivacy`) required for all apps; list all API categories used
   - App Tracking Transparency: request with `ATTrackingManager.requestTrackingAuthorization` before any ad SDK init
   - Review `Info.plist` usage description strings for every permission; Apple rejects vague strings
   - Archive with `Product → Archive`; validate and distribute via Xcode Organizer or `altool` / `notarytool`

## Standards

| Area | Do | Do not |
|---|---|---|
| Concurrency | `async/await` + structured concurrency (`TaskGroup`) | `DispatchQueue.global().async` in new Swift code |
| Memory | Use `[weak self]` in closures that outlive the calling scope | Capture `self` strongly in stored closures or `NotificationCenter` observers |
| SwiftUI state | `@State` for local view state; `@StateObject` / `@Observable` for view models | `@ObservedObject` for an object the view itself owns (causes re-creation bugs) |
| Keychain | Store tokens/passwords in Keychain with `kSecAttrAccessibleWhenUnlockedThisDeviceOnly` | Store secrets in `UserDefaults` or plist files |
| Permissions | Request at the moment of use with a pre-alert explaining the benefit | Request all permissions in `applicationDidFinishLaunching` |
| Error handling | Throw typed errors (`enum AppError: Error`); surface to user via `.alert(error:)` | `try!` or swallowing errors silently |
| Localization | All user-facing strings via `String(localized:)` or `LocalizedStringKey` | Hardcoded English strings in SwiftUI `Text` views |

## Common mistakes to avoid

- **Retain cycles in `@escaping` closures** — closures stored as properties (timer callbacks, notification observers, Combine sinks) commonly capture `self` strongly. Use `[weak self]` and guard-unwrap.
- **Modifying `@State` or publishing from a background thread** — SwiftUI state must be mutated on the main actor. Use `await MainActor.run { }` or `@MainActor` annotation.
- **`@StateObject` vs `@ObservedObject` confusion** — `@StateObject` creates and owns the object (use in the view that initialises it); `@ObservedObject` observes an externally-provided object.
- **Missing `@available` guards** — using iOS 17 APIs without `@available(iOS 17, *)` causes crashes on older devices at runtime, not compile time, unless `IPHONEOS_DEPLOYMENT_TARGET` is set correctly.
- **Storing large data in `UserDefaults`** — `UserDefaults` is loaded entirely into memory on app launch; store only lightweight preferences, never images or binary blobs.
- **Not unregistering `NotificationCenter` observers** (pre-iOS 11 pattern) — in modern Swift, `addObserver(forName:)` returns a token that must be retained and passed to `removeObserver` or the block fires after dealloc.
- **Skipping the privacy manifest** — App Store Connect rejects submissions that use required reason APIs (file timestamps, user defaults, etc.) without a corresponding entry in `PrivacyInfo.xcprivacy`.

## Output format

Typical feature deliverable structure:

```
Sources/
  Features/
    <Feature>/
      <Feature>View.swift          # SwiftUI view; thin, delegates to VM
      <Feature>ViewModel.swift     # @Observable or ObservableObject; @MainActor
      <Feature>Model.swift         # Codable data model
  Core/
    Networking/
      APIClient.swift              # URLSession wrapper; typed request/response
    Persistence/
      PersistenceController.swift  # SwiftData/Core Data stack
    Keychain/
      KeychainService.swift        # Typed Keychain read/write
Tests/
  <Feature>ViewModelTests.swift
  <Feature>APIClientTests.swift
```

## Related checklists

- `.claude/checklists/security.md`
- `.claude/checklists/performance.md`
- `.claude/checklists/accessibility.md`
- `.claude/checklists/production.md`

## Related agents

- `.claude/agents/engineering/mobile-engineer.md`
- `.claude/agents/design/mobile-ux-specialist.md`
- `.claude/agents/quality/performance-engineer.md`
- `.claude/agents/quality/security-auditor.md`
- `.claude/agents/quality/accessibility-auditor.md`

---
name: flutter
description: >
  Activate when building, reviewing, or debugging a Flutter application.
  Covers Dart, widget architecture, state management, navigation, platform
  channels, performance, and multi-platform deployment (iOS, Android, web,
  desktop). Trigger on any task involving Flutter widgets, pubspec.yaml,
  Dart code, or platform-specific integration.
---

# Flutter Skill

## When to use

- Creating or modifying Flutter screens, widgets, or navigation flows
- Choosing a state management approach (Riverpod, Bloc, Provider, GetX)
- Integrating platform channels for native iOS/Android APIs
- Configuring `pubspec.yaml`, flavors, or build variants
- Diagnosing jank, excessive rebuilds, or memory leaks
- Setting up CI builds for iOS, Android, web, or desktop targets

## Workflow

1. **Confirm Flutter channel and target platforms** — check `flutter --version` and which platforms are enabled in `pubspec.yaml`. Use stable channel for production; beta only if a specific fix is needed.
2. **Plan widget tree before coding**:
   - Identify which parts of the UI are stateless (pure display) vs. stateful (user interaction, async data)
   - Keep `StatelessWidget` the default; only use `StatefulWidget` when local ephemeral state is genuinely needed
   - Prefer `const` constructors everywhere possible — they short-circuit the rebuild cycle
3. **Choose state management** (confirm with team; do not switch mid-project):
   - **Riverpod** (recommended default): `AsyncNotifierProvider` for async data, `NotifierProvider` for sync state; co-locate provider declarations near the feature
   - **Bloc**: `Cubit` for simple state, `Bloc` for event-driven flows; one Bloc per feature/screen
   - **Provider**: acceptable for smaller apps; avoid nested `ChangeNotifierProvider` chains
4. **Navigation**: use `go_router` for declarative, deep-link-aware routing. Define all routes in a single `router.dart`; avoid `Navigator.of(context).push` calls scattered through the widget tree.
5. **Data layer**:
   - HTTP: `dio` or `http` package; wrap in a typed repository class
   - Local storage: `drift` (SQL) for structured data, `hive` / `isar` for simple key-value/object stores
   - Never call network or DB code inside `build()`
6. **Async in widgets**: use `FutureBuilder` / `StreamBuilder` only for one-off display; for anything the user can refresh or that changes over time, use a state management provider that holds the async state.
7. **Platform channels**: define the method channel in a dedicated service class; keep channel names namespaced (`com.example.app/channelName`); implement both iOS (Swift) and Android (Kotlin) sides before writing the Dart wrapper.
8. **Performance pass** before each release:
   - Run `flutter run --profile` on a real device; open DevTools → Performance
   - Identify widgets rebuilding unnecessarily with the Widget Rebuild tracker
   - Use `RepaintBoundary` around independently animated sections
   - Ensure all `Image` widgets use `cacheWidth`/`cacheHeight` or `ResizeImage`
9. **Build and sign**:
   - iOS: manage certificates and provisioning in Xcode or Fastlane; never commit `.p12` or `ExportOptions.plist` with embedded secrets
   - Android: store keystore outside the repo; reference via `key.properties` (git-ignored)
   - Use flavors (`--flavor`) for dev/staging/prod; map to separate Firebase projects if applicable

## Standards

| Area | Do | Do not |
|---|---|---|
| Widgets | Prefer `const` constructors; extract repeated sub-trees into named widgets | Build deeply nested anonymous closures inside `build()` |
| State | Hold state in providers/blocs; pass only what a widget needs via constructor | Store app state in `BuildContext` extensions or global variables |
| Keys | Use `ValueKey` / `ObjectKey` on list items; `GlobalKey` only when required (form, navigator) | Assign `GlobalKey` to every widget "just in case" |
| Async | Handle loading, error, and empty states explicitly | Use `.then()` chains inside `build()`; ignore `AsyncError` |
| Theming | Define all colors, text styles, and spacing in `ThemeData`; reference via `Theme.of(context)` | Hardcode hex colors or font sizes in widget files |
| Testing | Unit-test all business logic; widget-test critical flows; integration-test happy paths on CI | Skip tests because "Flutter UI is hard to test" |
| Secrets | Load API keys from `--dart-define` or a git-ignored `.env` read at build time | Embed secrets in `lib/` source files |

## Common mistakes to avoid

- **`setState` on a disposed widget** — always check `mounted` before calling `setState` after an `await`.
- **Rebuilding expensive widgets on every parent rebuild** — lift the expensive widget out, wrap in `const`, or use `Selector`/`Consumer` scoped to the exact state slice it needs.
- **`BuildContext` across async gaps** — after any `await`, the context may be invalid. Store what you need before the await, or check `mounted`.
- **`pubspec.yaml` asset paths with trailing slash not listing all files** — Flutter does not glob recursively; each subfolder must be listed, or files will be missing in release builds.
- **Platform channel calls on the main isolate for heavy work** — offload to a background `Isolate` or use `compute()`; blocking the main isolate causes dropped frames.
- **Not handling deep links in go_router on both platforms** — iOS requires `CFBundleURLTypes` in `Info.plist`; Android requires intent filters in `AndroidManifest.xml`. Test both.
- **Forgetting `flutter pub run build_runner build` after model changes** — generated files (`*.g.dart`, `*.freezed.dart`) go stale silently.

## Output format

Typical feature deliverable structure:

```
lib/
  features/
    <feature>/
      data/
        <feature>_repository.dart   # Network/DB calls; returns typed models
        <feature>_model.dart        # Freezed or plain Dart model + fromJson/toJson
      domain/
        <feature>_state.dart        # State class (Freezed union or sealed class)
      presentation/
        <feature>_screen.dart       # Root screen widget; provides BLoC/Riverpod scope
        widgets/
          <feature>_card.dart       # Extracted sub-widgets; prefer const
  core/
    router/
      router.dart                   # All go_router route definitions
    theme/
      app_theme.dart
test/
  features/
    <feature>/
      <feature>_repository_test.dart
      <feature>_screen_test.dart
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

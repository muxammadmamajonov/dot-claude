---
name: react-native
description: >
  Activate when building, reviewing, or debugging a React Native application
  (bare workflow or Expo). Covers component architecture, navigation, state
  management, native modules, performance, and store submission for iOS and
  Android. Trigger on any task involving React Native components, Metro bundler,
  Expo config plugins, or native bridge code.
---

# React Native Skill

## When to use

- Creating or modifying React Native screens, components, or navigation stacks
- Choosing between bare React Native and Expo managed/bare workflow
- Integrating native modules (camera, biometrics, BLE, push notifications)
- Diagnosing bridge overhead, JS thread jank, or memory pressure
- Configuring Metro, Babel, or Expo app.json / app.config.ts
- Preparing an app for App Store and Google Play submission

## Workflow

1. **Confirm workflow**: Expo managed workflow (no native code edited), Expo bare workflow (has `ios/` and `android/` folders), or plain React Native CLI. Each has different upgrade and native module strategies.
2. **Project bootstrap**:
   - Expo: `npx create-expo-app --template` — pick a TypeScript template
   - Bare RN: `npx @react-native-community/cli init ProjectName --template react-native-template-typescript`
   - Never bootstrap with JavaScript-only template for a new project; TypeScript from day one
3. **Navigation**: use React Navigation v6+ (`@react-navigation/native`). Define a typed root navigator in `src/navigation/RootNavigator.tsx`; export `RootStackParamList` for end-to-end type safety on `navigation.navigate()`.
4. **State management**:
   - Server/async state: `@tanstack/react-query` with a typed `queryClient`
   - Local UI state: `useState` / `useReducer`
   - Global client state: Zustand (lightweight) or Redux Toolkit (when team size or audit requirements demand it)
5. **Styling**: use `StyleSheet.create` (parsed once at load) or NativeWind (Tailwind for RN). Avoid inline style objects in `render` — they are recreated every render and skip memoization.
6. **Native modules**:
   - Prefer a well-maintained community package (`react-native-camera`, `react-native-vision-camera`, etc.) over writing a custom native module
   - For Expo managed workflow: use an Expo config plugin; never eject just to add a single module
   - When writing a custom module: implement in Swift (iOS) and Kotlin (Android); expose via the New Architecture (`TurboModules`) if the project targets RN 0.73+
7. **Performance pass**:
   - Use `React.memo` on list item components; pass stable callbacks via `useCallback`
   - Use `FlashList` (`@shopify/flash-list`) instead of `FlatList` for long lists
   - Run the JS thread profiler in Flipper or React DevTools; target <16 ms per frame on mid-range Android
   - Enable Hermes engine on both platforms (default since RN 0.70)
8. **Push notifications**: use `expo-notifications` (managed) or `@notifee/react-native` (bare); configure APNs entitlements on iOS and FCM `google-services.json` on Android before writing any notification code
9. **Build and submit**:
   - Expo: use EAS Build (`eas build`) and EAS Submit (`eas submit`) with `eas.json` profiles for dev/staging/prod
   - Bare RN: Fastlane + Xcode Cloud / Gradle for signing; store keystores and certs in a secrets manager, never in the repo
   - Run `npx react-native doctor` and fix all warnings before cutting a release

## Standards

| Area | Do | Do not |
|---|---|---|
| Components | Functional components + hooks only; `React.memo` for pure list items | Class components in new code |
| Lists | `FlashList` with `estimatedItemSize`; keyExtractor returns stable IDs | `ScrollView` wrapping a `map()` for lists longer than ~20 items |
| Images | `expo-image` or `react-native-fast-image` for caching; explicit `width`/`height` | Raw `<Image>` from RN core for remote images (no caching) |
| Permissions | Request permissions at the moment of use with clear rationale strings | Request all permissions on app launch |
| Deep links | Configure universal links (iOS) and App Links (Android) in the same PR as the feature | Test deep links only on one platform |
| Secrets | `expo-constants` + EAS secrets, or `react-native-config` with `.env` git-ignored | Hardcode API keys in JS source |
| Testing | Unit: Jest + `@testing-library/react-native`; E2E: Detox or Maestro | Skip E2E because "it's slow to set up" |

## Common mistakes to avoid

- **`useEffect` with missing dependencies** — causes stale closures; run ESLint with `react-hooks/exhaustive-deps` and treat warnings as errors.
- **Calling `setState` on an unmounted component** — return a cleanup function from `useEffect` that cancels pending async work or sets a `cancelled` flag.
- **Over-using `useEffect` for derived state** — if a value can be computed from props/state synchronously, compute it in the render body or with `useMemo`; do not store it in state and sync it with an effect.
- **Bridge-heavy operations on the JS thread** — operations like image decoding, crypto, or JSON parsing of large payloads block the JS thread; offload to a `worklet` (Reanimated) or a native module.
- **Not testing on a real mid-range Android device** — iOS Simulator and high-end Android emulators mask performance issues that appear on real budget Android hardware.
- **Ignoring Metro cache after native changes** — after adding/removing native modules or changing `app.json`, clear Metro cache: `npx expo start --clear` or `npx react-native start --reset-cache`.
- **`android:allowBackup="true"` left as default** — backs up sensitive shared preferences to Google Drive. Set to `false` or implement a custom `BackupAgent`.

## Output format

Typical feature deliverable structure:

```
src/
  features/
    <feature>/
      screens/
        <Feature>Screen.tsx       # Root screen registered in navigator
      components/
        <Feature>Card.tsx         # Memoized sub-component
      hooks/
        use<Feature>.ts           # Data fetching + business logic
      api/
        <feature>Api.ts           # Typed fetch/axios calls
      types.ts                    # Feature-local TypeScript types
  navigation/
    RootNavigator.tsx             # Typed navigator + RootStackParamList
  store/
    <feature>Store.ts             # Zustand or RTK slice
__tests__/
  features/
    <feature>/
      <Feature>Screen.test.tsx
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

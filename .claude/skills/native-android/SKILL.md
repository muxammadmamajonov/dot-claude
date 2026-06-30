---
name: native-android
description: >
  Activate when building, reviewing, or debugging a native Android application
  using Kotlin and Jetpack Compose (or View system where required). Covers
  app architecture, Compose state management, Kotlin coroutines, Room/DataStore,
  Play Store submission, and security hardening. Trigger on any task involving
  Kotlin source files, Gradle build scripts, AndroidManifest.xml, or
  Android-specific Jetpack libraries.
---

# Native Android (Kotlin / Jetpack Compose) Skill

## When to use

- Creating or modifying Compose screens, composables, or ViewModels
- Designing unidirectional data flow with `StateFlow`, `SharedFlow`, or `LiveData`
- Integrating Jetpack libraries (Room, DataStore, WorkManager, CameraX, etc.)
- Configuring Gradle build scripts, product flavors, or signing configs
- Diagnosing ANRs, memory leaks (LeakCanary), or slow Compose recompositions
- Preparing an app for Google Play review and submission

## Workflow

1. **Confirm `minSdk` / `targetSdk` and Kotlin version** — check `app/build.gradle.kts`. New APIs must be guarded with `@RequiresApi(Build.VERSION_CODES.X)` or `if (Build.VERSION.SDK_INT >= ...)`.
2. **Architecture**: follow the official Android Architecture (MVVM + Repository) unless team has adopted MVI. Structure: UI layer (Compose) → ViewModel → Repository → Data sources.
3. **Compose UI structure**:
   - Each screen is a `@Composable` function that takes UI state and callbacks as parameters (no ViewModel reference inside composable except at the screen root)
   - Extract repeated sub-composables into separate functions; keep them stateless and testable
   - Use `remember` for object instances that survive recomposition; `rememberSaveable` for state that survives process death
4. **State and data flow**:
   - ViewModel exposes state as `StateFlow<UiState>` (sealed class or data class); screen collects with `collectAsStateWithLifecycle()`
   - One-shot events (navigation, toasts) via `Channel<UiEvent>` consumed with `LaunchedEffect`
   - Never expose mutable state; back each `MutableStateFlow` with a read-only `StateFlow` property
5. **Dependency injection**: use Hilt (`@HiltViewModel`, `@AndroidEntryPoint`). One module per feature or layer. Do not use `ServiceLocator` patterns or manual DI in new code.
6. **Coroutines**:
   - Launch coroutines from ViewModel using `viewModelScope`; from a Repository use `withContext(Dispatchers.IO)` for blocking I/O
   - Never use `GlobalScope`; never use `runBlocking` on the main thread
   - Collect `Flow` in the UI with `collectAsStateWithLifecycle` (lifecycle-aware, cancels on stop)
7. **Data persistence**:
   - Structured data: Room with typed DAOs; use `Flow<T>` return types for reactive queries
   - Preferences: `DataStore<Preferences>` (replaces `SharedPreferences`); never use `SharedPreferences` in new code
   - Sensitive data: Android `EncryptedSharedPreferences` or `Keystore`-backed encryption; never store tokens in plaintext
8. **Networking**: Retrofit + OkHttp + Kotlin serialization (`kotlinx.serialization`). Define one `ApiService` interface per backend domain. Use an OkHttp `Interceptor` for auth headers and logging (disable logging interceptor in release builds).
9. **Performance pass before release**:
   - Run Layout Inspector → Recomposition counts; eliminate unnecessary recompositions with `remember`, `derivedStateOf`, or `key()`
   - Use LeakCanary in debug builds; fix all leaks before shipping
   - Profile with Android Studio Profiler (CPU, Memory, Network); target cold start <500 ms on a mid-range device
10. **Play Store preparation**:
    - Set `targetSdk` to the current year's requirement; update annually
    - Fill `DATA_SAFETY` section in Play Console before submission
    - Sign the release AAB (not APK) with a Keystore stored outside the repo; use Play App Signing
    - Run `./gradlew lint` and fix all errors; treat warnings as errors in CI (`warningsAsErrors = true`)

## Standards

| Area | Do | Do not |
|---|---|---|
| Coroutines | `viewModelScope` / `lifecycleScope`; structured concurrency | `GlobalScope`; bare `Thread` or `AsyncTask` |
| Compose state | Hoist state up; pass callbacks down; keep composables stateless | Pass ViewModel directly into deep composables |
| DI | Hilt modules scoped correctly (`@Singleton`, `@ViewModelScoped`) | `companion object` holding static context references |
| Permissions | Request at first use with `ActivityResultContracts.RequestPermission`; show rationale before re-requesting | `requestPermissions` in `onCreate` for all permissions at once |
| Serialization | `kotlinx.serialization` with `@Serializable` data classes | Moshi with reflection (slow) in new code; raw `JSONObject` parsing |
| Security | Store secrets in `EncryptedSharedPreferences` or Keystore; enable ProGuard/R8 for release | Log tokens or PII; leave `android:debuggable="true"` in release manifest |
| Testing | Unit: JUnit5 + MockK + Turbine for flows; UI: Compose `ComposeTestRule` | Skip testing because "Android tests are slow" |

## Common mistakes to avoid

- **Context leaks** — passing `Activity` context into a singleton (Hilt `@Singleton` module, Repository, etc.) causes the Activity to be retained. Use `Application` context for singletons.
- **Blocking the main thread** — `Room` and `Retrofit` calls on `Dispatchers.Main` cause ANRs. Always use `withContext(Dispatchers.IO)` or mark DAO functions `suspend`.
- **Recomposition storms** — reading a `StateFlow` directly inside a composable without `collectAsStateWithLifecycle` triggers recomposition on every emission regardless of lifecycle. Always use the lifecycle-aware collector.
- **`derivedStateOf` misuse** — wrap computations in `derivedStateOf` only when the derived value changes less frequently than the inputs; otherwise it adds overhead for no benefit.
- **Hardcoded strings in Compose** — use `stringResource(R.string.key)` not hardcoded literals; all user-visible text must be in `strings.xml` for localization and accessibility.
- **Missing `<queries>` in AndroidManifest for Android 11+** — apps targeting API 30+ cannot see other installed apps without declaring intents in `<queries>`; omitting this silently breaks package-visibility checks.
- **Not disabling debug flags in release** — `StrictMode`, `LeakCanary`, logging interceptors, and `android:debuggable` must all be disabled or stripped in release builds. Gate them with `BuildConfig.DEBUG`.

## Output format

Typical feature deliverable structure:

```
app/src/main/java/com/example/app/
  feature/<feature>/
    ui/
      <Feature>Screen.kt          # Root @Composable; collects state from VM
      <Feature>ViewModel.kt       # @HiltViewModel; exposes StateFlow<UiState>
      <Feature>UiState.kt         # Sealed class or data class for screen state
      components/
        <Feature>Card.kt          # Stateless sub-composable
    data/
      <Feature>Repository.kt      # Interface + impl; injected via Hilt
      <Feature>Dao.kt             # Room DAO with suspend / Flow functions
      <Feature>ApiService.kt      # Retrofit interface
      <Feature>Dto.kt             # @Serializable network model
    domain/
      <Feature>Model.kt           # Domain model mapped from DTO
  core/
    network/
      ApiClient.kt                # OkHttp + Retrofit setup
    database/
      AppDatabase.kt              # Room database singleton
test/
  feature/<feature>/
    <Feature>ViewModelTest.kt
    <Feature>RepositoryTest.kt
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

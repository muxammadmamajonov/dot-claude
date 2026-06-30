---
name: unity
description: >
  Activate when building, reviewing, or debugging a Unity game or interactive
  application. Covers project structure, MonoBehaviour patterns, scriptable
  objects, rendering pipelines, performance profiling, asset management, and
  multi-platform build configuration. Trigger on any task involving C# scripts,
  Unity scenes, prefabs, the Asset Database, or Unity project settings.
---

# Unity Skill

## When to use

- Creating or modifying Unity scenes, prefabs, or C# MonoBehaviour scripts
- Choosing between URP, HDRP, or Built-in render pipeline
- Designing game systems (input, audio, UI, save/load, pooling)
- Profiling and fixing frame-rate drops, GC spikes, or memory pressure
- Setting up CI builds (Unity Build Automation / GitHub Actions) for multiple platforms
- Preparing a build for Steam, iOS App Store, Google Play, or console certification

## Workflow

1. **Confirm Unity version and render pipeline** — check `ProjectSettings/ProjectVersion.txt` and the active render pipeline asset. URP for mobile/cross-platform, HDRP for high-fidelity PC/console, Built-in only for legacy projects. Do not switch pipeline mid-project without a full asset migration plan.
2. **Project structure** — establish before adding content:
   ```
   Assets/
     _Project/           # All project-specific assets (underscore sorts first)
       Art/
       Audio/
       Prefabs/
       Scenes/
       Scripts/
       ScriptableObjects/
       Settings/
     ThirdParty/         # Package Store assets, unmodified
   Packages/             # Unity Package Manager entries (packages.json)
   ```
3. **Scene and prefab discipline**:
   - One scene per major gameplay state (MainMenu, Gameplay, Loading)
   - Use Additive scene loading for streaming large worlds
   - Nest prefabs rather than duplicating GameObjects; never duplicate a prefab's contents across scenes
   - Mark prefab variant overrides intentionally; unintended overrides break batch updates
4. **C# scripting patterns**:
   - Prefer `ScriptableObject` for shared configuration and game-wide events (Event Channel pattern) over singletons
   - Use the Service Locator or Zenject/VContainer for DI instead of `FindObjectOfType` in production code
   - Reserve `MonoBehaviour` for things that genuinely belong on a GameObject; move pure logic to plain C# classes
   - Cache component references in `Awake`; never call `GetComponent` inside `Update`
5. **Input**: use the new Input System (`com.unity.inputsystem`) with an `InputActionAsset`; generated C# wrapper class per action map. Avoid `Input.GetKey` in new code.
6. **Object pooling**: use `UnityEngine.Pool.ObjectPool<T>` (Unity 2021+) for bullets, VFX, and any frequently instantiated/destroyed objects. `Instantiate`/`Destroy` in `Update` at high frequency causes GC pressure.
7. **UI**: use UI Toolkit (USS + UXML) for complex runtime UI on supported platforms; use uGUI (Canvas) for world-space UI or when targeting older Unity versions. Never mix UI Toolkit runtime and uGUI in the same panel hierarchy.
8. **Audio**: use Unity's Audio Mixer with exposed parameters for dynamic mixing; load audio clips as `Streaming` for music and `DecompressOnLoad` only for short, frequently-played SFX.
9. **Profiling pass** (before each milestone):
   - Open Profiler (`Window → Analysis → Profiler`); record on a target device, not in Editor
   - Check CPU: identify `Update` / `FixedUpdate` hot paths; eliminate per-frame allocations shown in GC Alloc column
   - Check Memory: use Memory Profiler package; look for duplicate textures and leaked assets
   - Check Rendering: use Frame Debugger to identify overdraw and unnecessary draw calls; use GPU Instancing for repeated meshes
   - Target: ≥30 fps sustained on the minimum-spec device; <2 ms GC spikes per frame
10. **Build pipeline**:
    - Use Build Profiles (`BuildProfile` asset, Unity 6) or `BuildPlayerOptions` scripting for automated builds
    - Strip unused code: enable `Managed Stripping Level: High` with a `link.xml` to protect reflected types
    - IL2CPP is required for iOS and recommended for Android release; verify with Mono first in dev, IL2CPP before final QA
    - Never commit `Library/`, `Temp/`, `Logs/`, or `.DS_Store` — add to `.gitignore` before first commit

## Standards

| Area | Do | Do not |
|---|---|---|
| Scene references | Assign references in the Inspector via serialized fields | `GameObject.Find` or `FindObjectOfType` at runtime |
| Data | `ScriptableObject` for config, balancing data, and event channels | `static` fields for cross-object communication |
| Allocations | Pool reusable objects; use `StringBuilder` for string concatenation in hot paths | `new` in `Update`; string concatenation with `+` per frame |
| Physics | Use layer-based collision matrix to limit `Physics.FixedUpdate` work | `Physics.OverlapSphere` with no layer mask in a tight loop |
| Coroutines | Use for time-based sequences; cache `WaitForSeconds` instances | Start coroutines that are never stopped on a frequently-created object |
| Async | `UniTask` (or `Awaitable` in Unity 6) for async/await; never block main thread | `Thread.Sleep` or blocking I/O on main thread |
| Assets | Mark textures with correct compression per platform (ASTC for mobile) | Leave all textures at RGBA32 default for all platforms |

## Common mistakes to avoid

- **Serialized field left null in prefab** — Unity does not throw on null serialized references at edit time. Add `[SerializeField][NotNull]` validation or null-check in `Awake` with a clear error message.
- **Modifying `Transform` inside `FixedUpdate` without Rigidbody** — causes physics jitter. Use `Rigidbody.MovePosition`/`MoveRotation` or set `Transform` only in `Update` with `Time.deltaTime` scaling.
- **`Resources.Load` overuse** — `Resources` folder disables asset stripping and bloats build size. Use Addressables for runtime-loaded assets.
- **GC spikes from `foreach` on Unity collections** — `foreach` on `List<T>` is fine; `foreach` on `Dictionary<K,V>` or custom Unity collections allocates an enumerator. Use `for` loops or cache the enumerator.
- **Physics layer matrix not configured** — every layer collides with every other layer by default, which multiplies physics work. Configure the collision matrix in `Project Settings → Physics` before adding gameplay layers.
- **Scene not added to Build Settings** — `SceneManager.LoadScene("SceneName")` silently fails at runtime if the scene is not in the Build Settings list. Add scenes as part of the PR that creates them.
- **`DontDestroyOnLoad` proliferation** — creating multiple manager singletons with `DontDestroyOnLoad` leads to duplicate instances after scene reloads. Use a single `GameManager` or a DI container to control lifetime.

## Output format

Typical feature deliverable structure:

```
Assets/_Project/
  Scripts/
    <Feature>/
      <Feature>System.cs          # Core logic as plain C# class (no MonoBehaviour)
      <Feature>Controller.cs      # MonoBehaviour; thin, delegates to System
      <Feature>Config.cs          # ScriptableObject with [CreateAssetMenu]
      <Feature>Events.cs          # ScriptableObject event channels (raise/listen)
  Prefabs/
    <Feature>/
      <Feature>Prefab.prefab
  Scenes/
    <Feature>Scene.unity          # If a dedicated scene is required
  ScriptableObjects/
    <Feature>/
      <Feature>DefaultConfig.asset
Tests/
  EditMode/
    <Feature>SystemTests.cs       # NUnit tests for pure C# logic
  PlayMode/
    <Feature>IntegrationTests.cs  # Tests requiring MonoBehaviour/scene context
```

## Related checklists

- `.claude/checklists/performance.md`
- `.claude/checklists/security.md`
- `.claude/checklists/production.md`

## Related agents

- `.claude/agents/stack/game/unity-engineer.md`
- `.claude/agents/engineering/game-engineer.md`
- `.claude/agents/domain/gaming-domain-expert.md`
- `.claude/agents/design/game-ux-specialist.md`
- `.claude/agents/quality/performance-engineer.md`

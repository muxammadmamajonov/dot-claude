---
name: unreal
description: >
  Activate when building, debugging, or architecting games or real-time simulations
  with Unreal Engine 4 or 5 — C++ gameplay code, Blueprints, asset pipeline,
  performance, and shipping practices. Use whenever the work touches Unreal,
  `.uproject`/`.uasset` files, Actors/UCLASS/Gameplay Ability System, Blueprints,
  or keywords like "unreal", "ue4", "ue5", "blueprint" — even if the user just
  says "my game".
---

# Unreal Engine Development

## When to use
- Writing or reviewing Unreal C++ gameplay classes, components, or subsystems
- Designing or debugging Blueprint graphs
- Setting up asset import pipelines, LODs, or streaming
- Profiling and fixing CPU/GPU frame-time issues
- Configuring build targets, packaging, and platform-specific settings
- Integrating third-party plugins or Marketplace assets

## Workflow

1. **Classify the task** — gameplay logic, rendering, physics, UI (UMG), networking, build/package, or asset pipeline.
2. **Confirm UE version** — UE4 vs UE5 (Nanite, Lumen, PCG, Motion Matching differ significantly). Check `UE_VERSION` in `Build.cs` or the `.uproject` file.
3. **Choose the right abstraction layer**:
   - Pure game logic → C++ `AActor` / `UActorComponent` subclass.
   - Designer-facing behaviour → expose via `UPROPERTY(EditAnywhere, BlueprintReadWrite)` and `UFUNCTION(BlueprintCallable)`.
   - Prototype quickly → Blueprint; port hot paths to C++ once stable.
4. **Scaffold the class** using the UE editor wizard (`New C++ Class`) to get correct macros, module includes, and `UCLASS()`/`USTRUCT()` boilerplate auto-generated.
5. **Add headers conservatively** — include only what the `.cpp` needs; forward-declare in `.h`. Slow compile times are the biggest UE productivity killer.
6. **Implement and wire up**:
   - Override lifecycle hooks in the correct order: `PostInitializeComponents → BeginPlay → Tick → EndPlay`.
   - Register delegates with `AddDynamic` for Blueprint-compatible events.
7. **Test in PIE** (Play-In-Editor) before packaging. Use `stat unit`, `stat fps`, and the Session Frontend Profiler to catch regressions immediately.
8. **Profile with Unreal Insights** for CPU traces; **RenderDoc** or **Nvidia Nsight** for GPU.
9. **Package** via `Project → Package Project` (or `RunUAT BuildCookRun`) targeting the platform. Check log for cook errors before QA.
10. **Audit** against .claude/checklists/performance.md and .claude/checklists/security.md before shipping.

## Standards

### C++ conventions
- Every exposed UObject must have `GENERATED_BODY()` and a valid module in `Build.cs`.
- Use `TObjectPtr<>` (UE5) instead of raw `UObject*` pointers — enables GC tracking.
- Prefer `FName`/`FText`/`FString` for the correct semantic purpose: `FName` for identity, `FText` for UI, `FString` for manipulation.
- Mark read-only Blueprint references `BlueprintReadOnly`; expose mutators through explicit `UFUNCTION`.
- Keep `Tick()` bodies under 0.1 ms. Move anything heavier to async tasks, timers, or events.
- Log with `UE_LOG(LogYourCategory, Warning, TEXT("..."))` — never `printf`.

### Blueprints
- Blueprints own visual state and designer-tweakable data; C++ owns logic and performance-critical paths.
- Compile all Blueprints before packaging (`Editor → Blueprints → Compile All Blueprints`).
- Name events and variables explicitly — avoid default `NewVar_0` names.

### Asset pipeline
- Import source assets at full resolution; use LOD groups and Nanite (UE5) for runtime resolution.
- Texture sizes must be power-of-two; use `BC7` for colour, `BC5` for normal maps, `BC4` for greyscale.
- Redirect assets via `Asset Manager` instead of direct `StaticLoadObject` — supports async loading.

### Networking (multiplayer)
- Mark server-authoritative state `Replicated` and `UPROPERTY(ReplicatedUsing=OnRep_*)`.
- RPCs: Server (`_Implementation`), Client, NetMulticast — validate authority with `HasAuthority()`.
- Never trust client input; validate on the server before applying.

### Do not
- Do not call `LoadObject` / `StaticFindObject` at runtime in shipping builds — use Soft References and async load.
- Do not tick actors that don't need per-frame updates; disable with `PrimaryActorTick.bCanEverTick = false`.
- Do not use global `GEngine->AddOnScreenDebugMessage` in shipping; wrap in `#if !UE_BUILD_SHIPPING`.
- Do not commit intermediate `.uasset` binary conflicts — always re-save through the editor after a merge.

## Common mistakes to avoid

| Mistake | Fix |
|---|---|
| Holding `UObject*` in non-UObject classes without `UPROPERTY` | The GC will collect it mid-frame. Use `UPROPERTY` or `FWeakObjectPtr`. |
| Calling `BeginPlay` logic in the constructor | Constructors run in the editor on CDO; use `BeginPlay` for runtime init. |
| Hot-reloading C++ with live delegates bound | Can crash the editor; unbind delegates in `EndPlay` before reloading. |
| Streaming levels that stall the game thread | Always use async level loading (`LoadStreamLevel` with a delegate). |
| Packaging without cooking redirectors | Players see missing asset errors; run `Fix Up Redirectors` before cook. |
| Blueprint nativisation left enabled in UE4 | Produces brittle compiled code; disable unless specifically needed. |

## Output format

- New C++ class: `.h` and `.cpp` pair with full UE boilerplate, matching module includes in `Build.cs`.
- Blueprint guidance: numbered step-by-step with node names in `code` formatting.
- Profiling report: table of hotspots with ms budget vs. actual and one recommended fix each.
- Architecture decision: diagram description → rationale → trade-offs, referencing .claude/templates/architecture.md.

## Related checklists
- .claude/checklists/performance.md
- .claude/checklists/security.md
- .claude/checklists/qa.md

## Related agents
- .claude/agents/core/orchestrator.md
- .claude/agents/engineering/devops-engineer.md

---
name: game
description: >
  Activate when building, extending, or optimising a video game — any genre or
  platform (PC, console, mobile, browser). Covers game-loop design, scene/level
  architecture, asset pipeline, physics, audio, input, playtesting, performance
  budgets, and publishing. Applies to Unity, Unreal, Godot, Phaser, three.js/
  Babylon.js, libGDX, or custom engine projects. Do NOT activate for interactive
  data visualisations or simulations that are not games.
---

# Game Development Skill

## When to use

- Starting a new game project (prototype, vertical slice, full production)
- Designing or refactoring the core game loop, scene graph, or entity system
- Adding gameplay features: combat, inventory, AI, dialogue, procedural generation
- Fixing frame-rate drops, memory spikes, shader stalls, or input latency
- Setting up the asset pipeline (sprites, 3D meshes, audio, shaders)
- Preparing a build for Steam, itch.io, Epic, App Store, Google Play, or console cert

---

## Workflow

1. **Classify the project** — Read `docs/specs/product.md` and `.claude/stack-matrix/` to confirm engine, target platforms, genre, and monetisation model (premium, free-to-play, subscription). If missing, run founder-interview questions (see `.claude/agents/core/orchestrator.md`) before touching any code.

2. **Define the performance budget before any code** — Agree on targets for the weakest target device:
   | Budget item | Typical target |
   |---|---|
   | Frame time | ≤ 16.6 ms (60 fps) or ≤ 33.3 ms (30 fps) |
   | Draw calls | < 200 (mobile < 100) per frame |
   | GPU memory | < 512 MB (mobile < 200 MB) |
   | CPU game-logic | ≤ 4 ms per frame |
   | Load time | < 5 s cold start, < 2 s level transition |
   Write these into `docs/specs/tech.md`.

3. **Scaffold engine project** — Use the engine's official project wizard (Unity Hub, Godot project manager, Unreal Project Browser). Set version control to include only source assets; add engine-generated binaries and `Library/` to `.gitignore`.

4. **Design the game loop** — Separate responsibilities clearly:
   - **Input** → poll or event-buffer at the top of the frame
   - **Update** → advance simulation (physics, AI, timers) using `delta_time`; never use wall-clock time directly
   - **Render** → read state only; do not mutate game state in render code
   Scale all movement and animation by `delta_time` to stay frame-rate-independent.

5. **Implement the entity/component architecture** — Prefer the engine's built-in ECS or component model (Unity MonoBehaviour, Godot Node, Unreal Actor-Component). Avoid deep single-class inheritance trees; compose behaviours.

6. **Build scene/level structure**
   - One scene per logical state: MainMenu, Gameplay, Pause, GameOver
   - Sub-scenes/prefabs for reusable objects (enemies, pickups, UI panels)
   - Use asset bundles / addressables for levels larger than initial load budget

7. **Set up the asset pipeline**
   - Sprites: export at 2× and 4× densities; use texture atlases (> 4 sprites that appear together)
   - 3D meshes: target < 50 K triangles for environment props, < 10 K for background objects
   - Audio: OGG/Vorbis for music (streaming); WAV/PCM for short SFX (in-memory)
   - Shaders: author in the engine's shader graph first; optimise GLSL/HLSL by hand only when profiler demands it

8. **Implement save/load** — Serialise player state to a versioned format. Include a `save_version` integer; migrate old saves forward on load. Never break old save files silently.

9. **Playtest at each milestone** — Run structured sessions:
   - **Prototype**: does the core mechanic feel fun? Kill features that don't pass.
   - **Alpha**: is progression clear? Do first-time players know what to do?
   - **Beta**: are there game-breaking bugs? Is performance within budget on target hardware?
   Log all bugs in a tracker. Regression-test every fixed bug.

10. **Profile and optimise** — Only optimise when a profiler confirms a bottleneck:
    - CPU: batch physics casts, cache component references (don't `GetComponent` in `Update`)
    - GPU: reduce overdraw, use LODs, bake static lighting
    - Memory: pool frequently instantiated objects (bullets, particles, enemies); eliminate GC allocs in the hot path
    Reference `.claude/checklists/performance.md`.

11. **Prepare for release**
    - Strip all cheat codes, debug menus, and development overrides from release builds
    - Implement analytics (session length, level completion, crash reports) respecting platform privacy rules
    - For console: submit for platform certification (TRC/TCR/LotCheck) early; cert takes weeks
    - For Steam: configure store page, age ratings (ESRB/PEGI), and Steam Deck compatibility

---

## Standards

**Do**
- Use `delta_time` for every movement, animation, and timer. Never assume a fixed frame rate.
- Pool frequently created/destroyed objects (projectiles, particles) to eliminate per-frame GC pressure.
- Keep the gameplay simulation deterministic when network sync or replay is needed; separate RNG streams per system.
- Version-control your project settings files (ProjectSettings/, project.godot); they define platform targets, input maps, and physics layers.
- Separate magic numbers into named constants or data tables — never hardcode damage values, speeds, or cooldowns in code.

**Do not**
- Do physics or heavy computation in the render callback.
- Load assets synchronously during gameplay; use async loading with a progress indicator.
- Use the entity hierarchy for data queries (e.g., `GetComponentsInChildren` in Update) — it's O(n) over all descendants.
- Commit binary build artefacts (`.dll`, `.so`, editor caches) to version control.
- Expose developer cheats or God mode in release builds.

---

## Common mistakes to avoid

- **Frame-rate-dependent movement** — `transform.position += speed * Vector3.forward` without `* Time.deltaTime` makes the game faster on faster machines.
- **Monolithic game manager** — a single `GameManager` singleton that owns everything becomes unmaintainable; split into focused managers (AudioManager, SceneManager, SaveManager).
- **Z-fighting on co-planar geometry** — offset overlapping surfaces by at least 0.001 units, or use polygon offset in the shader.
- **Null-reference on scene load** — objects destroyed on scene transition leave dangling references; use weak references or events, and guard with null-checks.
- **Ignoring mobile thermal throttling** — sustained 60 fps causes CPU/GPU heat and device throttling; test a 20-minute play session on a physical device.
- **Audio source overload** — playing hundreds of overlapping one-shot sounds spikes CPU; pool AudioSource components and implement voice stealing.
- **Skipping localisation infrastructure** — retrofitting i18n into shipped text is expensive; use string keys and a localisation table from day one if international launch is planned.

---

## Output format

A production-ready game project should include:

```
/
├── Assets/ (Unity) | project.godot + scenes/ (Godot) | Content/ (Unreal)
│   ├── Scripts/ (or src/)    # Game logic, systems
│   ├── Scenes/               # Scene files per game state
│   ├── Prefabs/ (or scenes/) # Reusable entity templates
│   ├── Art/                  # Source and imported art assets
│   ├── Audio/                # Music, SFX
│   └── Data/                 # Scriptable objects, JSON data tables
├── Tests/                    # Edit-mode and play-mode unit tests
├── Builds/                   # Git-ignored build output
├── Docs/
│   ├── design.md             # Game design document (GDD) or link
│   └── art-pipeline.md       # Asset specs and export settings
└── README.md                 # How to open in editor, run tests, make a build
```

---

## Related checklists

- `.claude/checklists/performance.md`
- `.claude/checklists/qa.md`
- `.claude/checklists/production.md`
- `.claude/checklists/security.md`

## Related agents

- `.claude/agents/core/orchestrator.md`
- `.claude/agents/quality/performance-engineer.md`

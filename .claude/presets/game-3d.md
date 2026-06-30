# 3D Game Preset

## Project type

A game whose world and primary gameplay exist in three-dimensional space (X/Y/Z). Encompasses first-person shooters, third-person action/adventure, open-world RPGs, racing, flight simulators, VR/AR experiences, 3D platformers, strategy with 3D camera, and architectural/simulation visualisations with game mechanics. Target platforms include PC/Mac/Linux (Steam, Epic), consoles (PlayStation 5, Xbox Series, Nintendo Switch), mobile (iOS/Android), and VR headsets (Quest, SteamVR, PSVR). Assets are 3D meshes, rigs, animations, PBR materials, and environment art rather than flat sprites.

---

## Typical use cases

- First-person shooter or looter-shooter (Unreal Engine 5)
- Third-person action/adventure or soulslike (Unreal 5, Unity 6)
- Open-world RPG or survival (Unreal 5, Unity DOTS/Entities)
- 3D platformer or collect-a-thon (Unity, Godot 4)
- Racing / flight sim (Unreal, Unity)
- VR/AR immersive experience (Unreal XR, Unity XR Toolkit, WebXR)
- Mobile 3D game (Unity URP, Godot 4 Mobile)
- Architectural visualisation with interactive elements (Unreal, Unity)

---

## Required discovery questions

1. **Genre and core mechanic** — What is the player doing every 10 seconds in 3D space? (explore, shoot, drive, build, solve?) What single mechanic must feel best at launch?
2. **Target platform(s) and minimum spec** — PC (what GPU tier?), console (which generations?), mobile (which OS version and device class?), or VR (which headsets, standalone vs tethered)?
3. **World scale** — Is the world bounded (arena, level), open-world (streaming), or procedurally generated? Open-world requires a completely different streaming and LOD architecture.
4. **Multiplayer** — Single-player, split-screen, online co-op, or competitive? Online multiplayer significantly changes the scope; see `.claude/presets/multiplayer-game.md`.
5. **Monetisation model** — Premium, free-to-play with cosmetic IAP, season pass, subscription, or no commercial model?
6. **Art direction and performance envelope** — Photorealistic (Nanite/Lumen/ray-tracing) vs. stylised? The art direction sets the entire rendering budget and asset pipeline complexity.
7. **Engine preference and team experience** — Unreal 5 (C++/Blueprints), Unity 6 (C#/URP/HDRP), Godot 4 (GDScript/C#), or custom? Prior engine experience is decisive for 3D projects.
8. **Character and animation system** — Third-person character with full rig (IK, blend trees, motion matching)? Physics-based character controller? Vehicles? The animation system is a major standalone workstream.
9. **Team size and timeline** — 3D games at full production quality require 10–100× more asset time than 2D; is the scope realistic for the team and timeline?
10. **Console certification target** — Which platform partners, and is there a cert submission date? Console cert (TRC for PlayStation, TCR for Xbox, LotCheck for Nintendo) adds weeks to the schedule and has strict technical requirements.

---

## Recommended agents

**Core**
- `.claude/agents/core/orchestrator.md` — drives the 9-stage flow
- `.claude/agents/core/solution-architect.md` — rendering pipeline, LOD strategy, streaming, entity architecture
- `.claude/agents/core/product-manager.md` — GDD, vertical slice scope, milestone gating

**Engineering**
- `.claude/agents/engineering/game-engineer.md` — game loop, character controller, physics, AI, animation state machine
- `.claude/agents/quality/performance-engineer.md` — draw call budgets, LOD chains, shader optimisation, memory profiling
- `.claude/agents/engineering/backend-engineer.md` — if online features (leaderboards, cloud save, IAP validation, matchmaking)
- `.claude/agents/engineering/release-engineer.md` — build pipeline, console SDK integration, cert submission

**Quality**
- `.claude/agents/quality/qa-engineer.md` — playtest plans, regression, console-cert checklist
- `.claude/agents/quality/performance-engineer.md` — frame-time audit on weakest target; VR latency audit if applicable

**Design**
- `.claude/agents/design/game-ux-specialist.md` — 3D camera design, UI/HUD, accessibility (motion sickness for VR)
- `.claude/agents/design/accessibility-designer.md` — FOV sliders, subtitle/caption system, colourblind mode, motion sickness settings for VR

**Domain**
- `.claude/agents/domain/gaming-domain-expert.md` — economy, IAP, progression, anti-cheat, live-ops

---

## Recommended skills

- `.claude/skills/game/SKILL.md` — core game-loop, ECS, asset pipeline, playtesting, performance budget
- `.claude/skills/unity/SKILL.md` — Unity 6 project setup, URP/HDRP, Addressables, animation rigging (if Unity)
- `.claude/skills/unreal/SKILL.md` — Unreal 5 project setup, Nanite, Lumen, Blueprints, animation system (if Unreal)
- `.claude/skills/performance/SKILL.md` — GPU profiling, LOD, occlusion culling, draw-call batching, texture streaming
- `.claude/skills/testing/SKILL.md` — automated test harness for gameplay systems; VR motion-sickness regression tests
- `.claude/skills/security/SKILL.md` — anti-cheat server authority, IAP validation, cheat-resistant save

---

## Recommended stack options

| Stack | Rationale |
|---|---|
| **Unreal Engine 5 + C++/Blueprints** | Industry-standard for high-fidelity 3D; Nanite virtualized geometry + Lumen GI eliminate manual LOD/light-bake work for most PC/console targets; best for realistic art direction. |
| **Unity 6 + C# + URP/HDRP** | Largest asset store, strong mobile and XR support, flexible rendering; good for stylised 3D, mobile 3D, or cross-platform (PC + console + mobile from one project). |
| **Godot 4 + C#/GDScript** | Lightweight, open-source, fast iteration; suitable for indie 3D games with modest visual targets; lacks Unreal/Unity's built-in large-studio pipeline tooling. |
| **Unity 6 + DOTS/Entities + C#** | Needed when simulating thousands of entities (RTS, large-scale simulation, bullet-hell in 3D); ECS architecture is a hard requirement, not an afterthought. |

---

## Required checklists

- `.claude/checklists/performance.md` — frame time targets per platform (PC ≤ 16.6 ms @ 60 fps; console 60 or 30 fps target agreed; VR ≤ 11.1 ms @ 90 fps hard requirement)
- `.claude/checklists/qa.md` — vertical slice, alpha, beta, gold-master playtest gates
- `.claude/checklists/security.md` — server-authoritative game state for online, IAP receipt validation, anti-cheat integration
- `.claude/checklists/production.md` — crash reporting, console cert requirements, store metadata, age rating

---

## MVP scope pattern

**In the first cut (vertical slice)**
- One contained environment (~5–10 minutes of play) demonstrating the core 3D mechanic end-to-end
- Playable character with locomotion, camera, and primary action (shoot/jump/drive/interact) at target quality
- One complete enemy type or obstacle set with AI and feedback (hit reaction, death, spawn)
- Frame time within budget on weakest target device — not "usually fine", verified with profiler
- Main menu and basic pause/resume
- Local save for vertical-slice progress checkpoint

**Defer until post-vertical-slice**
- Full level count, open-world streaming (design the streaming system, stub it)
- Full animation polish (IK, facial, motion matching) — rough blend trees first
- Multiplayer layer (architect the server-authority model now, implement later)
- Cinematic cutscenes and narrative presentation
- Full audio mix and music system (placeholder SFX and music, final mix in beta)
- Localisation (string-key system from day one, translations deferred)
- Console certification submission (PC/dev-kit testing first; cert last mile)
- VR mode if primary target is flat-screen (prototype on flat, port to VR after core is stable)

---

## Production risks

| Risk | Priority | Mitigation |
|---|---|---|
| VR motion sickness from high render latency or frame drops | P0 for VR | Hard 90 fps lock (or 72/80 for Quest); fixed foveated rendering; no frame-rate-dependent movement |
| Scope creep on open-world ("we'll add more biomes") | P0 | Define world boundaries in GDD before any art production; locked scope gate at vertical-slice review |
| Asset pipeline bottleneck (art takes 80% of the time) | P0 | Define poly budgets, texture resolutions, and naming conventions before any art is made |
| Console certification failure (missing required features: subtitles, multiple save slots, online disconnect handling) | P0 | Read platform TRC/TCR/LotCheck checklists from day one; build cert requirements into the architecture |
| LOD and streaming gaps causing pop-in or hitches | P1 | Set LOD distances in tech spec; test streaming with simulated slow storage early |
| Character controller feel — bad-feeling movement kills 3D games | P1 | Playtest movement in isolation at prototype stage; never defer "feel" tuning to beta |
| Shader compilation stutter on PC (DX12/Vulkan PSO compilation) | P1 | Use shader warm-up / PSO caching; profile on mid-spec PC from week one |
| Memory pressure on consoles (fixed 16 GB shared CPU/GPU RAM) | P1 | Set per-system memory budgets in tech spec; track with memory profiler throughout production |
| Missing GDPR/COPPA compliance for analytics/ads | P0 if applicable | Confirm age rating and markets; implement consent flow before any telemetry is live |

---

## Launch requirements

- All items in `.claude/checklists/production.md` are green
- Frame time within budget on every target platform, verified with platform profiler (Unreal Insights, Unity Profiler, PIX/RGP for console)
- Zero P0/P1 bugs; all P2 triaged and accepted or deferred to patch
- Console: platform cert (TRC/TCR/LotCheck) submission completed and cert granted before launch date
- IAP end-to-end tested in sandbox on every target platform; server-side receipt validation confirmed
- Save/load cycle tested: save → crash-quit → relaunch → correct state on all platforms
- Age rating approved on all target storefronts (ESRB, PEGI, etc.)
- Privacy policy live; analytics opt-in implemented per GDPR/CCPA
- Crash reporting active and confirmed receiving events from cert/preview builds
- All debug menus, cheat codes, god modes, and developer overlays stripped from release build
- Subtitle/caption system functional (required for PEGI/ESRB compliance on most console platforms)
- Localisations QA-passed for all shipped languages
- At least one full playthrough of the shipped content by QA with zero P0 blockers found

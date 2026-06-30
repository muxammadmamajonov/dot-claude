# 2D Game Preset

## Project type

A game whose world and primary gameplay exist on a flat (X/Y) plane. Encompasses pixel-art platformers, top-down RPGs, shoot-em-ups, puzzle games, match-3, idle/clicker, visual novels, tower-defence, and card games. Target platforms include PC/Mac/Linux, mobile (iOS/Android), browser (WebGL), Nintendo Switch, PlayStation, and Xbox. Assets are sprites, tilemaps, and 2D physics shapes rather than 3D meshes.

---

## Typical use cases

- Pixel-art platformer or metroidvania (Unity/Godot)
- Top-down RPG or dungeon crawler
- Mobile casual/hyper-casual (Phaser, Unity Mobile, Godot)
- Puzzle or match-3 (portrait mobile first)
- Shoot-em-up / bullet-hell
- Visual novel / narrative adventure (Ren'Py, Unity, Godot)
- Tower defence or strategy
- Browser mini-game (Phaser 3, PixiJS)

---

## Required discovery questions

1. **Genre and core mechanic** — What does the player do every 10 seconds? (e.g. "jump over obstacles", "match tiles", "shoot enemies") What is the one mechanic that must feel great at launch?
2. **Target platform(s)** — PC/console, mobile portrait, mobile landscape, browser WebGL, or all? Mobile changes the entire input and performance model.
3. **Monetisation** — Premium one-time purchase, free-to-play with IAP/ads, subscription, or no monetisation (game jam / portfolio)?
4. **Target audience and age rating** — Casual vs. core; children under 13 (COPPA/GDPR-K)? This controls UI complexity, violence level, and store compliance.
5. **Multiplayer requirement** — Single-player only, local co-op, or online multiplayer? Online multiplayer requires a separate server layer — see `.claude/presets/multiplayer-game.md`.
6. **Art style and existing assets** — Pixel art, hand-drawn, vector, or licensed? Do assets exist or must they be created? What is the resolution/tile size?
7. **Engine preference** — Unity (C#), Godot 4 (GDScript/C#), Phaser 3 (TypeScript), or custom? Any prior engine lock-in?
8. **Team size and timeline** — Solo dev, small indie team, or studio? Hard launch deadline (e.g. game jam, holiday window, app store featuring)?
9. **Save and progression model** — What player data persists? Local save file, cloud save (Apple/Google/Steam Cloud), or server-side? How many save slots?
10. **Content volume at launch** — Approximate number of levels/stages/maps, enemy types, item types, and hours of gameplay expected in the first release?

---

## Recommended agents

**Core**
- `.claude/agents/core/orchestrator.md` — drives the 9-stage flow; never skip to coding
- `.claude/agents/core/solution-architect.md` — scene graph, ECS design, save system architecture
- `.claude/agents/core/product-manager.md` — game design document, feature prioritisation, milestone gating

**Engineering**
- `.claude/agents/engineering/game-engineer.md` — game loop, physics, input, entity systems
- `.claude/agents/engineering/frontend-engineer.md` — UI/HUD layer (especially browser/WebGL targets)
- `.claude/agents/engineering/backend-engineer.md` — if online features (leaderboards, cloud save, IAP validation) are needed
- `.claude/agents/engineering/release-engineer.md` — build pipeline, platform submission, CI/CD

**Quality**
- `.claude/agents/quality/qa-engineer.md` — playtest plans, regression test on every build
- `.claude/agents/quality/performance-engineer.md` — frame budget, draw call audits, memory profiling

**Design**
- `.claude/agents/design/game-ux-specialist.md` — UI/UX, onboarding flow, feel of controls
- `.claude/agents/design/accessibility-designer.md` — colour-blind modes, remappable controls, text sizing

**Domain**
- `.claude/agents/domain/gaming-domain-expert.md` — economy, IAP, progression, live-ops, leaderboards

---

## Recommended skills

- `.claude/skills/game/SKILL.md` — core game-loop, entity system, asset pipeline, playtesting workflow
- `.claude/skills/godot/SKILL.md` — Godot 4 scene/node model, GDScript patterns (if Godot)
- `.claude/skills/unity/SKILL.md` — Unity project setup, MonoBehaviour, Addressables, URP (if Unity)
- `.claude/skills/performance/SKILL.md` — draw call batching, texture atlases, object pooling, GC avoidance
- `.claude/skills/testing/SKILL.md` — automated play-mode tests, regression suites
- `.claude/skills/security/SKILL.md` — IAP receipt validation, cheat-resistant save files, anti-tamper

---

## Recommended stack options

| Stack | Rationale |
|---|---|
| **Godot 4 + GDScript/C#** | Open-source, excellent 2D tooling, small binary, strong mobile/desktop/browser export; best default for new indie 2D projects. See `.claude/stack-matrix/backend.md`. |
| **Unity 6 + C# + URP** | Largest asset marketplace, mature mobile pipeline, strong console cert track record; good when team has prior Unity experience or needs certified console release. |
| **Phaser 3 + TypeScript** | Pure browser/WebGL target; no install, instant play; best for web portals, casual games, or game-jam browser entries. |
| **Godot 4 + C# + Nakama** | Adds authoritative server layer when online multiplayer is needed later; same engine, adds real-time backend. See `.claude/presets/multiplayer-game.md`. |

---

## Required checklists

- `.claude/checklists/performance.md` — frame time ≤ 16.6 ms @ 60 fps on weakest target device; draw calls < 100 on mobile
- `.claude/checklists/qa.md` — playtest milestone gates (prototype fun, alpha clarity, beta bug-free)
- `.claude/checklists/security.md` — save-file tampering, IAP server-side validation, no cheat exposure in release builds
- `.claude/checklists/production.md` — crash reporting, analytics opt-in, app store metadata, age rating

---

## MVP scope pattern

**In the first cut (MVP)**
- One fully playable level or stage that demonstrates the core mechanic end-to-end
- Functional main menu, pause, and game-over screen
- Local save for player progress (one slot is enough)
- Stable 60 fps on the weakest target device, no loading hitches mid-level
- Basic sound effects and background music (placeholder quality acceptable)
- Crash-free on target platforms; submitted to internal TestFlight / Play Internal Testing

**Defer until post-MVP**
- Multiple worlds / level packs (add content, don't change systems)
- Online leaderboards and cloud save
- Achievements / trophies
- Localisation (design string-key i18n infrastructure from day one, fill other languages later)
- Accessibility options (colour-blind mode, text scale) — stub the settings page, implement after core is stable
- Full live-ops / event system
- Controller remapping (ship fixed layout first, make it remappable next)

---

## Production risks

| Risk | Priority | Mitigation |
|---|---|---|
| Frame-rate-dependent movement (no `delta_time`) | P0 | Enforce `delta_time` scaling in code review; write a lint check |
| IAP fraud — client-reported purchases not validated server-side | P0 | Server-side receipt validation against Apple/Google API before any grant; see `.claude/agents/domain/gaming-domain-expert.md` |
| Save-file corruption on crash mid-write | P0 | Write to a temp file, atomic rename; keep one backup slot |
| Performance cliff on low-end mobile (thermal throttle, GPU overdraw) | P1 | Profile on the oldest/cheapest device in scope; set draw-call and texture-memory budgets early |
| Localisation retrofit cost | P1 | Use string tables / i18n keys from day one even if only one language ships |
| Monolithic `GameManager` singleton | P1 | Decompose into focused managers at design time; enforce via architecture review |
| Platform certification rejection | P1 | Read store guidelines before building IAP/ads/privacy flows; submit cert checklist from `.claude/checklists/production.md` |
| Audio source overload (hundreds of simultaneous SFX) | P2 | Implement voice stealing and audio pooling before beta |
| Missing COPPA/GDPR-K compliance for under-13 audience | P0 if applicable | Confirm age rating target in discovery; disable analytics/ads for child-directed designation |

---

## Launch requirements

- All items in `.claude/checklists/production.md` are green
- Frame time ≤ 16.6 ms on weakest target device (measured, not estimated)
- Zero P0/P1 bugs open; all known P2 bugs triaged and accepted or deferred
- IAP flow end-to-end tested in sandbox on every target platform
- Save/load cycle verified: save → force-quit → relaunch → correct state
- Age rating submitted and approved (ESRB/PEGI/USK/IARC as required)
- Privacy policy URL live and linked in store listing (required by all major app stores)
- Crash reporting (Sentry, Firebase Crashlytics, or equivalent) active and confirmed receiving events
- Analytics opt-in/opt-out implemented per GDPR/CCPA requirements
- Store listing complete: screenshots in all required sizes, description, keywords, content descriptors
- Release build has all debug menus, cheat codes, and dev overlays stripped
- At least one successful TestFlight / Play Internal Testing / Steam Playtest run completed

# Game Checklist
Gate for game projects covering frame budget, asset pipeline, save integrity, and playtest signoff. Severity tiers: P0=blocker, P1=important (fix shortly after launch), P2=hardening, P3=post-launch/backlog.

## P0 — Blockers (must pass before build ships)

- [ ] **Frame budget met**: Target frame time (16.67 ms for 60 fps, 33.33 ms for 30 fps) is not exceeded in the most demanding scene under minimum-spec hardware; profiler confirms no frame spikes > 2× budget for more than 3 consecutive frames.
- [ ] **No progression blockers**: Every critical path (tutorial → first level → final level) is completable without softlock, crash, or infinite loop; verified by QA playthrough on a fresh save.
- [ ] **Save/load integrity**: Game saves at every intended checkpoint; reloading a save restores player position, inventory, stats, and quest flags with zero data loss; tested across at minimum 3 save slots.
- [ ] **Save corruption guard**: If a save file is corrupt or truncated, the game surfaces a recoverable error and does not crash; it does not silently overwrite the last good save.
- [ ] **No out-of-memory crash**: Peak VRAM and RAM usage stay below 80 % of minimum-spec limits across all levels; verified with instrumented build.
- [ ] **Audio sync**: No audio dropouts or desync vs. animation during cutscenes, dialogue, or combat events on minimum-spec hardware.
- [ ] **Input handling**: All intended control schemes (keyboard/mouse, gamepad, touch) are functional and rebindable where documented; no unmapped critical actions.
- [ ] **Platform certification requirements met**: Submission checklist items for target platform(s) (Steam, console, mobile stores) are all ticked; e.g., achievement API integration, age rating content compliance, icon/metadata assets present.
- [ ] **No missing or placeholder assets in release build**: All placeholder meshes, textures, audio clips, and strings have been replaced; build pipeline strips `_WIP` / `_placeholder` tagged assets.

## P1 — Important (fix before public release or shortly after)

- [ ] **Asset pipeline reproducible**: A clean checkout can produce a shippable build with a single command; asset cooking/baking steps are scripted and not reliant on local machine state.
- [ ] **LOD and culling verified**: Level-of-detail transitions are not visible as jarring pop-in under normal gameplay camera distances; frustum and occlusion culling are active.
- [ ] **Loading screen / async loading**: No level transition causes a hard freeze visible to the player for more than 2 seconds without a loading indicator.
- [ ] **Physics determinism (if applicable)**: Multiplayer or replay-dependent physics produce identical results across supported platforms; floating-point modes are locked.
- [ ] **Anti-cheat / integrity (online games)**: Server-authoritative logic prevents client-side stat manipulation; cheat detection is integrated and tested before first online session.
- [ ] **Accessibility baseline**: At minimum one colorblind mode, subtitle/caption option, and adjustable HUD scale are present and functional.
- [ ] **Localization completeness**: All in-game strings use the localization pipeline; no hardcoded English text appears in non-English builds; font supports all shipped character sets.
- [ ] **Crash reporting integration**: A crash reporter (e.g., Sentry, Backtrace, platform-native) is active in release builds and sends symbolicated stack traces to the team's dashboard.
- [ ] **Build size within store limits**: Final package size is within the allowed download/install limit for each target platform; large asset packs are delivered via DLC or streaming where needed.

## P2 — Hardening / nice-to-have

- [ ] **Texture streaming / memory pooling**: Dynamic texture streaming is tuned so VRAM does not spike on scene transitions; object pools are pre-warmed for frequently spawned entities.
- [ ] **Shader compilation stutter**: Shader variants are pre-compiled or async-compiled to eliminate first-frame stutter when new materials are encountered.
- [ ] **Automated regression tests**: A headless smoke-test build runs core gameplay loops (spawn, move, interact, save, load) and reports failures to CI within 10 minutes.
- [ ] **Analytics / telemetry hooked up**: Session start/end, level completion, and death/fail events are being collected (with consent where required) so post-launch balance data is available.
- [ ] **Player-reported bug funnel**: In-game feedback or bug-report shortcut exists in non-release builds; players can attach a screenshot and session log.
- [ ] **DRM / licence check non-intrusive**: DRM does not require persistent internet during offline play (where not intended); licence check failure shows a clear message instead of a silent crash.
- [ ] **Update / patch pipeline tested**: A delta patch from the previous build can be applied cleanly; version number and changelog are embedded in the build.

## P3 — Post-launch / backlog (track and revisit after launch; never blocks shipping)

- [ ] **Player-behavior telemetry reviewed for balance**: Heatmaps, death locations, item-usage rates, and level completion funnels are analyzed post-launch; findings feed into a documented balance patch schedule.
- [ ] **Mod support / user-generated content pipeline**: An official modding SDK or data-export format is designed, documented, and sandboxed so community content cannot execute arbitrary code or corrupt saves.
- [ ] **Speedrun and exploit catalogue maintained**: Known sequence breaks and out-of-bounds exploits are catalogued; the team decides for each whether to patch (casual experience) or preserve (competitive community value) and documents the rationale.
- [ ] **Cross-save / cloud-save expanded to all platforms**: Save data is synced across every supported platform via the platform's cloud-save API or a first-party backend; conflict resolution (newest-wins vs. manual merge) is specified and tested.
- [ ] **Post-launch content pipeline validated**: DLC, season-pass, and live-service content (new levels, skins, events) can be authored, cooked, and shipped as delta patches without a full-game reinstall; pipeline is smoke-tested on a canary build.
- [ ] **Community-reported exploit and soft-lock backlog triaged**: A public or internal tracker captures post-launch bug reports; severity is re-evaluated monthly and critical soft-locks are patched within a defined SLA.

## How to use

**When**: Run this checklist at the "release candidate" milestone, before any public build is distributed (alpha, beta, or launch).

**Who**: QA lead signs off P0, tech lead signs off P1, and the full team reviews P2 items before final submission.

**Command / agent**: Ask the agent `"Run .claude/checklists/game.md against the current build"` — it will execute automated checks (frame profiler, asset scan, save-file round-trip test) and flag items that need manual review. Manual items are assigned to the appropriate role in `.claude/agents/core/orchestrator.md`.

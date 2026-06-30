# Example Project Brief — "Deepforge" (2D Indie Game)

> A worked example showing how the Project OS classifies and scopes a single-player 2D game. Illustrative, not a real title.

## One-line idea
A 2D roguelike where you descend a procedurally generated mine, forging and upgrading weapons from ore you mine mid-run, with permadeath and meta-progression between runs.

## Classification result
- **Project type:** Game (2D, single-player, desktop-first)
- **Preset:** [game-2d](../.claude/presets/game-2d.md)
- **Cross-cutting concerns:** game-loop & frame budget, asset pipeline, save-file integrity (corruption = lost progress = refunds), deterministic procedural generation (seeded), controller + keyboard input, Steam release/achievements. **No** realtime multiplayer, **no** server backend in v1.
- **Specialists pulled in:** [game-engineer](../.claude/agents/engineering/game-engineer.md), [game-ux-specialist](../.claude/agents/design/game-ux-specialist.md), [gaming-domain-expert](../.claude/agents/domain/gaming-domain-expert.md) (progression/economy).

## Founder discovery answers
- **Problem (player):** Roguelike fans want fresh build variety; most games gate it behind grind. Crafting-during-run gives moment-to-moment agency.
- **Target users:** PC roguelike players (Hades / Dead Cells audience); play in 20–40 min sessions.
- **Value proposition:** Every run you literally build your weapon from what you find — no two runs play the same.
- **Constraints:** 2 devs (1 gameplay, 1 art) + freelance audio; 9-month part-time runway; ~$8k tools/asset budget; target Steam.
- **Success metrics:** Demo → wishlist conversion ≥ 8%; median session ≥ 20 min; "very positive" launch reviews; stable 60 FPS on a 5-year-old laptop.
- **Key risks:** Scope creep (content treadmill); procedural levels that feel samey or unfair; save corruption; performance with many on-screen entities.
- **Budget / timeline:** ~$8k; vertical-slice demo in 3 months, Early Access in 9.

## Recommended stack (with rationale)
- **Engine:** Godot 4 — free/open (no royalties on an indie budget), excellent 2D pipeline, GDScript for fast iteration with C# escape hatch for hot paths. See [.claude/stack-matrix/game.md](../.claude/stack-matrix/game.md).
- **Language:** GDScript for gameplay; C# only if profiling demands it.
- **Persistence:** local save files (JSON + checksum + atomic write + backup slot) — no DB, no cloud in v1.
- **Tooling:** Aseprite (art), Tiled (room templates feeding the generator), Git LFS for assets, GitHub Actions for export builds.
- **Distribution:** Steam (Steamworks for achievements/cloud saves).

## MVP / vertical-slice scope
**In:** one biome (3 room archetypes), seeded procedural layout, mining + 1 craftable weapon family with 3 upgrade paths, core combat loop, permadeath, one meta-upgrade, controller + keyboard, save/continue with integrity checks, 60 FPS target.
**Deferred:** additional biomes, bosses beyond the slice, audio polish, localization, Steam achievements, Deck verification, mod support.

## First 3 safe phases
1. **Walking skeleton** — player moves, mines an ore node, the loop spawns the next room from a seed, basic combat. Proves the game *feels* good and the generator is deterministic. → [/build-prototype](../.claude/commands/build-prototype.md)
2. **Crafting + progression** — turn ore into a weapon mid-run, one upgrade path, permadeath + one meta-upgrade. → [/implement-feature](../.claude/commands/implement-feature.md)
3. **Save integrity + perf pass** — atomic saves with checksum + backup, then [performance audit](../.claude/commands/audit-performance.md) against the 60 FPS budget and the [game checklist](../.claude/checklists/game.md) before the demo.

---
**Next command to run:** [/start-project](../.claude/commands/start-project.md) → it will confirm the game-2d preset and produce a [game-design-document](../.claude/templates/game-design-document.md) via [/create-specs](../.claude/commands/create-specs.md).

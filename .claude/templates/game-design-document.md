# Game Design Document (GDD)

**What:** The single source of truth for what the game is, how it plays, and how it grows. Covers design pillars, core loop, mechanics, progression, economy, and content plan.
**Who fills it in:** Game director + lead designer, reviewed by engineering and art leads.
**When:** Before any feature implementation. Update it when scope changes — treat this as a living document, not a contract.

---

## 1. Game Overview

> Answer the elevator-pitch questions in one paragraph each.

**Logline:** `<One sentence. "X meets Y in a world where Z." e.g. "A factory-builder where supply chains are turned into musical instruments.">`

**Genre:** `<e.g. Turn-based tactics RPG | Real-time strategy | Narrative puzzle | Roguelite platformer>`

**Platform(s):** `<PC (Steam) | iOS | Android | Nintendo Switch | PS5 | Xbox Series X | WebGL>`

**Target audience:**
- Age range: `<e.g. 16–35>`
- Player archetype (Bartle): `<Achiever / Explorer / Socializer / Killer — pick primary>`
- Comparable titles they play: `<Title A>`, `<Title B>`, `<Title C>`

**ESRB / PEGI rating target:** `<E | T | M | E10+>` — `<reason>`

**Monetization model:** `<Buy-to-play | Free-to-play + IAP | Subscription | Premium + DLC>`

---

## 2. Design Pillars

> 3–5 non-negotiable design values. Every feature must serve at least one pillar. Use these to say "no" to scope creep.

| # | Pillar | What it means in practice |
|---|--------|--------------------------|
| 1 | `<e.g. Every run tells a story>` | `<Procedural generation always produces memorable moments, not random noise>` |
| 2 | `<e.g. Mastery is visible>` | `<Players should feel measurably more skilled after 5 hours than after 1 hour>` |
| 3 | `<e.g. Accessible, not dumbed down>` | `<Easy to learn; tutorials never insult; depth revealed gradually>` |
| 4 | `<e.g. Respect player time>` | `<Sessions completeable in 20 min; no padded grinding; fast restart>` |
| 5 | `<optional>` | `<optional>` |

---

## 3. Core Loop

> Describe what the player does in a single session from launch to quit. Use a diagram or numbered sequence.

```
[Session Start]
      │
      ▼
 <Goal presented>  ──►  <Player acts>  ──►  <Feedback / reward>
      │                                           │
      └──── <New goal unlocked or loop repeats> ◄─┘
      │
      ▼
 <Session End / Save>
```

**Micro loop (seconds):** `<e.g. Aim → shoot → hit/miss feedback>`
**Meso loop (minutes):** `<e.g. Clear a room → loot → choose upgrade>`
**Macro loop (hours/sessions):** `<e.g. Complete a run → unlock meta-progression node → start next run stronger>`

---

## 4. Core Mechanics

> Define every mechanic players interact with. For each: what it is, how it works, win/lose conditions.

### 4.1 `<Mechanic Name — e.g. Combat>`

- **Description:** `<What the player does and perceives>`
- **Controls:** `<Input mapping per platform>`
- **Rules:** `<Numbered list of rules: damage formula, cooldowns, limits>`
- **Feel targets:** `<Snappy | Weight | Chaos — reference a comparable game moment>`
- **Failure state:** `<What happens when the player fails this mechanic>`

### 4.2 `<Mechanic Name — e.g. Crafting>`

- **Description:** `<>`
- **Recipe system:** `<fixed recipes | discovered | procedural>`
- **Resource inputs:** `<list resource types>`
- **Output types:** `<consumables | equipment | upgrades | cosmetics>`

### 4.3 `<Mechanic Name — e.g. Exploration>`

*(Add as many mechanic sections as needed.)*

---

## 5. Progression Systems

> How does the player grow? Separate character/world progression from meta-progression.

### 5.1 In-Session Progression

| Layer | Type | Examples |
|-------|------|---------|
| Character stats | `<Additive / multiplicative>` | HP, Attack, Speed |
| Abilities | `<Unlocked / chosen at milestone>` | `<Ability A>`, `<Ability B>` |
| Equipment slots | `<count>` | `<Weapon, Armor, Trinket>` |

### 5.2 Meta-Progression (Persists Between Sessions)

| System | Unlock trigger | What it unlocks |
|--------|----------------|-----------------|
| `<Skill tree>` | `<Earn XP>` | `<Passive bonuses>` |
| `<Character roster>` | `<Complete run with class>` | `<New playable character>` |
| `<Cosmetics>` | `<Achievement / purchase>` | `<Skins, emotes>` |

### 5.3 Difficulty Curve

> Describe how challenge increases. Include a rough level/hour map.

| Hour mark | Expected player state | Challenge adjustment |
|-----------|-----------------------|----------------------|
| 0–1 h | `<Learning controls>` | `<Tutorial, no fail states>` |
| 1–5 h | `<Comfortable with core loop>` | `<Introduce first elite enemies>` |
| 5–20 h | `<Building mastery>` | `<Full system interactions exposed>` |
| 20+ h | `<Endgame / NG+>` | `<Modifiers / challenge modes active>` |

---

## 6. Economy Design

> Define every resource, its sources, its sinks, and target scarcity.

### 6.1 Currency & Resources

| Resource | Type | Primary source | Primary sink | Scarcity target |
|----------|------|---------------|--------------|-----------------|
| `<Gold>` | Soft currency | `<Enemy drops>` | `<Shop purchases>` | `<Mild surplus — player always has something to buy>` |
| `<Gems>` | Hard currency | `<IAP / rare achievement>` | `<Premium cosmetics, energy>` | `<Scarce — deliberate spend>` |
| `<Crafting mats>` | Material | `<Exploration, recipes>` | `<Crafting>` | `<Moderate — drive exploration>` |

### 6.2 Shop / Store

- Shop resets: `<daily | per-run | never>`
- Price ranges: `<e.g. Common item 50–100 gold; Rare 200–500 gold>`
- IAP catalogue (if F2P):

| SKU | Price (USD) | Contents | Value vs. free path |
|-----|-------------|----------|---------------------|
| `<Starter Pack>` | `$1.99` | `<300 gems + cosmetic>` | `<2× value>` |
| `<Monthly Pass>` | `$4.99` | `<Daily gems for 30 days>` | `<4× value>` |

### 6.3 Economy Balance Rules

- Never sell power that is unobtainable via free play within `<X hours>`
- Maximum real-money advantage: `<time-save only | cosmetic only | define cap>`
- Inflation protection: `<price floors, resource caps at X>`

---

## 7. Game Modes

> List every mode the player can enter from the main menu.

| Mode | Description | Unique rules | Unlocked by |
|------|-------------|--------------|-------------|
| `<Story / Campaign>` | `<Linear narrative missions>` | `<No permadeath>` | `<Default>` |
| `<Endless / Roguelite>` | `<Procedural runs>` | `<Permadeath, meta unlocks>` | `<Complete chapter 1>` |
| `<PvP Arena>` | `<1v1 ranked>` | `<Balanced preset loadouts>` | `<Reach level 10>` |
| `<Co-op>` | `<2–4 player online>` | `<Shared health pool>` | `<Default>` |
| `<Daily Challenge>` | `<Fixed seed, global leaderboard>` | `<One attempt per day>` | `<Default>` |

---

## 8. Narrative & World

> Fill in only what engineering and art need to build the game. Full narrative bible lives separately.

- **Setting:** `<Genre, era, tone — e.g. "Near-future biopunk city, noir tone">`
- **Player character:** `<Defined protagonist | Player-created | Avatar>`
- **Central conflict:** `<One sentence>`
- **Factions / key NPCs:**

| Name | Role | Relationship to player |
|------|------|------------------------|
| `<Faction A>` | `<Antagonist>` | `<Hostile by default, can be allied>` |
| `<NPC Guide>` | `<Mentor>` | `<Unlocks abilities via dialogue>` |

- **Chapter/Act structure:** `<Number of acts>`, `<approximate content hours each>`

---

## 9. Art & Audio Direction

> Enough to align engineers and artists; detailed style guides live in the art bible.

| Dimension | Direction |
|-----------|-----------|
| Visual style | `<e.g. 2D pixel art, 16:9, 48×48 tile grid>` |
| Color palette mood | `<e.g. Muted darks with neon accent pops>` |
| Animation priority | `<e.g. Player jump arc, enemy death, projectile impact>` |
| Camera | `<e.g. Top-down orthographic | Side-scrolling | Third-person 3D>` |
| Audio style | `<e.g. Chiptune OST + punchy SFX, no voice acting at launch>` |
| Accessibility audio | `<Subtitles | Closed captions | Visual cues for audio events>` |

---

## 10. Technical Constraints

> Scope limits that must inform design choices.

| Constraint | Value | Impact on design |
|------------|-------|-----------------|
| Engine | `<Unity 2022 LTS | Unreal 5 | Godot 4 | custom>` | |
| Target frame rate | `<60fps | 30fps>` | `<Particle limits, simulation tick rate>` |
| Target devices | `<iOS 15+, Android 10+>` | `<Polygon budget, RAM cap>` |
| Max binary size | `<200 MB initial install>` | `<Asset streaming required>` |
| Offline support | `<Full | Partial (no PvP) | None>` | |
| Max concurrent enemies on screen | `<e.g. 50>` | `<AI budget>` |

---

## 11. Content Plan

> What ships at launch vs. what is post-launch. Prevents scope creep.

### Launch (v1.0)

- Story chapters: `<1–3>`
- Playable characters: `<e.g. 4>`
- Enemy types: `<e.g. 20>`
- Environments / biomes: `<e.g. 3>`
- Game modes: `<e.g. Story, Endless>`

### Post-Launch Roadmap

| Patch / DLC | Target window | Key addition |
|-------------|---------------|--------------|
| `<v1.1 Balance pass>` | `<4 weeks post-launch>` | `<Bug fixes, top community requests>` |
| `<DLC 1 — New Biome>` | `<3 months>` | `<New environment, 2 characters, story chapter>` |
| `<Season 2>` | `<6 months>` | `<PvP season, Battle Pass>` |

---

## 12. Metrics & Liveness

> How will you know if the game is healthy?

| Metric | Target (Day 7) | Target (Day 30) |
|--------|----------------|-----------------|
| Day-1 retention | `>50%` | — |
| Day-7 retention | — | `>20%` |
| Session length (median) | `>15 min` | `>20 min` |
| Sessions per DAU | `>2.0` | `>2.5` |
| ARPU (F2P) | — | `>$0.10` |
| Conversion to payer (F2P) | — | `>2%` |

---

## 13. Open Design Questions

| # | Question | Owner | Decision needed by |
|---|----------|-------|-------------------|
| 1 | `<e.g. Should death be permanent or optional per difficulty?>` | `<Game Director>` | `<YYYY-MM-DD>` |
| 2 | `<e.g. Offline co-op required at launch or DLC?>` | `<Producer>` | `<YYYY-MM-DD>` |

---

## 14. Related Documents

- Project brief: `.claude/templates/project-brief.md`
- Architecture: `.claude/templates/architecture.md`
- Performance plan: `.claude/templates/performance-plan.md`
- Security model (for online features, IAP): `.claude/templates/security-model.md`
- Testing strategy: `.claude/templates/testing-strategy.md`

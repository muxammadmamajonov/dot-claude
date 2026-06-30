# Game Engine Stack Matrix

Choose based on **genre and visual fidelity requirements**, **target platforms**, **team size and skills**, and **business model**. Unity and Unreal dominate commercial game development for different tiers — Unity for mid-fidelity cross-platform, Unreal for AAA and photorealistic work. Godot is the serious open-source contender for indie and mid-scale 2D/3D. Phaser serves browser-based 2D games. Roblox is a platform, not just an engine, with its own distribution and monetization. Custom engines are only justified when all others impose unacceptable constraints.

---

## Unity

- **When to use:** Mid-fidelity 3D or 2D games targeting multiple platforms (PC, console, mobile, VR/AR, WebGL); indie to mid-size studio productions; mobile games; XR applications; simulations and serious games.
- **When NOT to use:** AAA photorealistic open-world games where Unreal's rendering is a stronger fit; teams with no C# experience and unwilling to learn; projects where Unity's runtime fee model (post-2023 controversy) is a business risk.
- **Strengths:** Largest asset store ecosystem; best mobile platform support (iOS, Android, ad mediation, IAP integrations); strong VR/AR support (OpenXR, Meta, Apple Vision Pro); huge community and learning resources; C# is approachable; DOTS/ECS available for data-oriented performance; Unity Gaming Services (matchmaking, analytics, cloud save).
- **Weaknesses:** Runtime fee controversy damaged trust — licensing terms changed in 2023 and may change again; editor UI is dated; built-in render pipeline fragmentation (Built-in, URP, HDRP); IL2CPP build times are long; physics and animation systems are less mature than Unreal.
- **Team fit:** Indie developers; mobile game studios; mid-size teams (2–50 engineers); simulation and XR developers; teams comfortable with C#.
- **Scale fit:** Scales from solo projects to AA studio productions. AAA is possible (Hollow Knight, Cuphead, Pokémon GO) but requires significant engine expertise.
- **Production risks:** Licensing uncertainty; asset store assets of variable quality can introduce tech debt; render pipeline choice locks you in early; IL2CPP compilation failures on edge cases; Unity editor instability on large projects.

---

## Unreal Engine

- **When to use:** AAA and high-fidelity 3D games; cinematic experiences; virtual production; architectural visualization; games requiring Lumen (dynamic global illumination) or Nanite (virtualized geometry); console-first titles; teams with C++ expertise.
- **When NOT to use:** Mobile games (Unreal's mobile performance optimization is harder and build sizes are larger); 2D games (possible but not Unreal's strength); teams without C++ or Blueprint expertise; small indie teams on tight timelines.
- **Strengths:** Industry-leading rendering (Lumen, Nanite, Temporal Super Resolution); Blueprints visual scripting lets designers prototype without code; MetaHuman for realistic characters; Fab marketplace; Epic's extensive documentation and sample projects; 5% royalty only after $1M revenue (favorable for large projects); active AAA studio adoption.
- **Weaknesses:** Steep learning curve; C++ compile times are painful in large projects (mitigated by Unreal Build Tool and incremental builds); overkill for simple games; Blueprint visual scripting has performance limits; engine source is large and complex to modify; less ideal for mobile.
- **Team fit:** AA to AAA studios; teams with dedicated technical directors and engine programmers; virtual production companies; architectural viz studios; developers targeting high-end PC and console.
- **Scale fit:** No ceiling — Fortnite, Ark, and countless AAA titles. Scales to the largest productions in the industry.
- **Production risks:** Blueprint-heavy projects accumulate tech debt and performance problems; C++ build times slow iteration; console certification requirements need engine expertise; shader compilation stalls (PSO caching) affect players on first run; Epic roadmap changes can deprecate features teams depend on.

---

## Godot

- **When to use:** Indie games (2D and 3D); open-source-committed teams; projects where avoiding royalties or licensing fees is a hard requirement; developers who want a lightweight, hackable engine; game jam projects; teams wanting GDScript or C# flexibility.
- **When NOT to use:** AAA productions; mobile games that need advanced ad SDK integrations not yet available in Godot; teams needing the asset ecosystem depth of Unity; projects requiring Unreal-quality rendering (Godot 4's renderer is good but not Lumen-class).
- **Strengths:** Fully open-source (MIT license) — no royalties, no runtime fees, no licensing risk; Godot 4 brought major improvements (Vulkan renderer, improved 3D, better C# support, GDExtension); lightweight editor; node/scene system is intuitive; GDScript is Python-like and fast to learn; active indie community; self-hostable.
- **Weaknesses:** Smaller asset marketplace than Unity; fewer third-party SDK integrations (analytics, ads, IAP require more custom work); C# support is good but historically second-class to GDScript; 3D capabilities, while much improved in Godot 4, still trail Unity and Unreal for high-fidelity work; console export requires third-party publisher support.
- **Team fit:** Indie developers; game jam teams; studios that value open-source and want no licensing overhead; developers coming from Python-adjacent backgrounds (GDScript); educators.
- **Scale fit:** Excellent for 2D games at any scope. 3D games up to mid-fidelity AA level. Console ports require additional work.
- **Production risks:** Console export is not officially supported (requires third-party porting studios like W4Games); mobile SDK integrations need custom plugins; Godot 3 → 4 migration is non-trivial for existing projects; smaller talent pool than Unity.

---

## Phaser

- **When to use:** Browser-based 2D games; HTML5 games for web portals or ad networks; casual games embedded in web apps or marketing pages; developers who want to use JavaScript/TypeScript for games; rapid game prototypes.
- **When NOT to use:** 3D games (Phaser is 2D only); mobile apps distributed through app stores (web wrapper performance is poor for games); projects needing complex physics, networking, or AI systems; games requiring offline-first distribution.
- **Strengths:** Pure JavaScript/TypeScript — no new language to learn for web developers; runs in any browser without plugins; WebGL renderer with canvas fallback; active community and extensive documentation; lightweight and fast to prototype in; good physics integration (Matter.js, Arcade Physics); free and open-source.
- **Weaknesses:** 2D only; browser performance ceiling below native; no built-in multiplayer (needs third-party: Colyseus, Socket.io); no native app store distribution without wrapper (Cordova/Capacitor); smaller community than Unity/Godot; less suited to complex game architectures without disciplined structuring.
- **Team fit:** Web developers making their first game; teams building HTML5 games for ad networks or web portals; developers who want to avoid learning a new engine or language; educational game developers.
- **Scale fit:** Good for simple to medium complexity 2D games. Complex games with hundreds of entities or large tilemaps require careful optimization (object pooling, camera culling).
- **Production risks:** Browser API fragmentation (WebGL 2 support varies); mobile browser performance is inconsistent; audio API limitations in Safari; no offline distribution without wrapping; monetization via ads or IAP requires manual integration.

---

## Roblox

- **When to use:** Games targeting children and teens; UGC (user-generated content) platform games; developers who want built-in distribution, monetization (Robux), social features, and multiplayer without building infrastructure; educational coding projects using Lua.
- **When NOT to use:** Games targeting adults as the primary audience; projects needing custom engine rendering or physics beyond Roblox's sandbox; IP-sensitive projects (Roblox owns distribution and has content moderation constraints); developers who need to publish to app stores independently.
- **Strengths:** Built-in multiplayer infrastructure (no server management); instant distribution to 70M+ daily active users; Robux monetization system; built-in social graph; Lua scripting is approachable; free to develop; Roblox Studio is capable for the platform's constraints; strong youth market reach.
- **Weaknesses:** Platform lock-in — your game exists within Roblox, not as an independent product; Roblox takes a significant revenue share; content moderation can remove games without appeal; Lua is not transferable to other engines; graphics fidelity is limited by Roblox's renderer; adult/hardcore gaming audiences are not on the platform.
- **Team fit:** Developers targeting the youth market; educators; indie developers who want distribution without marketing budget; teams building social/casual experiences.
- **Scale fit:** Roblox handles infrastructure scaling automatically. The platform itself scales to millions of concurrent players. Your scale ceiling is Roblox's platform policies, not your engineering.
- **Production risks:** Complete platform dependency — policy changes, revenue share changes, or moderation decisions are out of your control; no path to independent distribution; Lua skills have limited portability; IP protection on Roblox is weak.

---

## Custom Engine

- **When to use:** Only when all existing engines impose unacceptable constraints for your specific use case — e.g., a novel rendering technique, a unique simulation domain (fluid dynamics at scale, custom physics for a specific sport or system), hardware targets where no engine has a port, or when the engine itself is the product (engine-as-SDK for other developers).
- **When NOT to use:** Any project that can be delivered with an existing engine. Custom engines are almost always slower to deliver, more expensive to maintain, and harder to staff than using an existing solution — even when existing engines seem "imperfect."
- **Strengths:** Total control over rendering pipeline, memory model, and feature set; no licensing fees or royalties; can be precisely optimized for one specific genre or hardware target; no unnecessary engine features bloating the build.
- **Weaknesses:** Massive upfront investment (years for a production-quality engine); you must build or integrate every system (audio, physics, input, serialization, asset pipeline, platform abstraction); hiring requires engineers who want to build engine infrastructure, not games; no community or asset marketplace; every platform certification must be done from scratch.
- **Team fit:** Large studios with dedicated engine teams (id Software, Valve, CDPR with REDengine); specialized simulation companies; hardware vendors building engine SDKs; research institutions.
- **Scale fit:** Unlimited — but the cost to reach "scalable" is orders of magnitude higher than using an existing engine.
- **Production risks:** Extreme schedule risk; key-person dependency on engine architects; platform SDK updates (console OS updates, new GPU driver requirements) require engine-team bandwidth; no community to absorb support burden.

---

## Comparison Table

| Engine         | Languages        | Dimensions | Target Platforms             | Rendering Quality | License/Cost         | Best For                              |
|----------------|------------------|------------|------------------------------|-------------------|----------------------|---------------------------------------|
| Unity          | C#               | 2D + 3D    | PC, mobile, console, VR/AR, web | Medium-High   | Free tier + royalty  | Mobile, indie, XR, mid-fidelity       |
| Unreal Engine  | C++ + Blueprints | 3D (+ 2D)  | PC, console, mobile, VR      | Highest           | Free + 5% after $1M  | AAA, cinematic, high-fidelity 3D      |
| Godot          | GDScript / C#    | 2D + 3D    | PC, mobile, web (console via 3rd party) | Medium | MIT (free)          | Indie, 2D, open-source committed      |
| Phaser         | JS / TS          | 2D only    | Browser, web                 | Low-Medium        | MIT (free)           | Browser games, HTML5, web devs        |
| Roblox         | Lua              | 3D         | Roblox platform (PC/mobile)  | Low-Medium        | Free dev, rev share  | Youth market, UGC, social games       |
| Custom Engine  | Any              | Any        | Any (must implement)         | Unlimited         | Engineering cost only | Specialized simulation, engine-as-product |

---

## Recommended Combinations

| Combination                                      | Why                                                                                              |
|--------------------------------------------------|--------------------------------------------------------------------------------------------------|
| Unity + URP + C# + Mirror (multiplayer)          | Best mobile game stack; URP balances performance and visuals; Mirror for self-hosted multiplayer |
| Unreal + C++ + Blueprints + EOS                  | AA/AAA PC and console games; EOS provides free cross-platform multiplayer and anti-cheat         |
| Godot 4 + GDScript + Nakama                      | Fully open-source indie stack; Nakama for self-hosted multiplayer; zero licensing cost           |
| Phaser 3 + TypeScript + Colyseus                 | Browser multiplayer games; Colyseus is purpose-built for Phaser + Node.js real-time servers     |
| Unity + DOTS/ECS + Burst + Jobs                  | Data-oriented architecture for large-scale simulations or strategy games with many entities      |
| Unreal + MetaHuman + Lumen + Nanite              | Cinematic or virtual production projects requiring photorealistic characters and environments    |

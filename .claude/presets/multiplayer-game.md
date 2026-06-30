# Multiplayer Game Preset

## Project type

A game with real-time or turn-based online multiplayer, requiring networked game state, authoritative server logic, and live operations. Encompasses competitive PvP (FPS, battle royale, MOBA, fighting), cooperative PvE, massively multiplayer online (MMO/MMORPG), social/party games, turn-based async multiplayer, and any game with persistent online features (leaderboards, guilds, seasons). Sits on top of a 2D or 3D game foundation — combine this preset with `.claude/presets/game-2d.md` or `.claude/presets/game-3d.md` as appropriate.

---

## Typical use cases

- Competitive FPS / battle royale (dedicated servers, client-side prediction)
- MOBA or RTS (deterministic lockstep simulation)
- Online co-op action/RPG (relay or dedicated server, session-based)
- MMO / persistent world (zone servers, sharding, stateful long sessions)
- Social / party game (lobby, relay, low-precision synchronisation)
- Mobile async multiplayer (turn-based, push notifications, no real-time session)
- Arcade / casual real-time with matchmaking (Nakama, PlayFab, custom backend)

---

## Required discovery questions

1. **Multiplayer model** — Real-time session-based (FPS, racing), deterministic lockstep (RTS, fighting), authoritative server with client prediction, relay/peer-relay, or async turn-based? This is the single most architectural decision.
2. **Concurrent users at launch vs. peak** — How many players per session? How many concurrent sessions at expected peak? This drives server fleet sizing and cost model.
3. **Tick rate and latency budget** — What is the maximum tolerable round-trip latency before gameplay breaks? (FPS: ~80 ms; RTS: ~200 ms; turn-based: seconds.) What tick rate (20/30/60/128 Hz)?
4. **Server authority model** — Who is the source of truth for game state? Full server authority (FPS, MMO) or trusted-client/relay (casual party game)? Anti-cheat requirements depend heavily on this.
5. **Matchmaking requirements** — Skill-based (ELO/MMR), region-based, party/squad assembly, quick-play queue, private lobbies? What is the acceptable queue-wait time before relaxing skill constraints?
6. **Persistent vs. session-only data** — What survives a session? Player stats, inventory, currency, progression, clans/guilds? Persistent data requires a proper backend database and migration strategy.
7. **Anti-cheat level** — Is this a competitive/ranked game where cheating is a community-trust issue, or a casual game where it matters less? Anti-cheat architecture is expensive to retrofit.
8. **Live-ops and seasons** — Will there be seasonal resets, battle passes, limited-time events, or frequent balance patches? Live-ops infrastructure must be designed before launch, not after.
9. **Platform and cross-play** — Which platforms, and is cross-play between them required? Cross-play requires platform-specific SDK integration and approval from each platform holder.
10. **Regulatory and content moderation** — Chat, voice, user-generated content? In-app purchases with real money? Child audience (COPPA)? Each adds significant compliance scope.

---

## Recommended agents

**Core**
- `.claude/agents/core/orchestrator.md` — drives the 9-stage flow; multiplayer projects must not skip spec stages
- `.claude/agents/core/solution-architect.md` — network topology, server authority model, session lifecycle, state sync design
- `.claude/agents/core/product-manager.md` — GDD, live-ops roadmap, season cadence planning

**Engineering**
- `.claude/agents/engineering/game-engineer.md` — client game loop, client-side prediction, rollback netcode, input serialisation
- `.claude/agents/engineering/realtime-engineer.md` — server authoritative loop, tick system, lag compensation, interest management
- `.claude/agents/engineering/backend-engineer.md` — matchmaking service, session management, player data, leaderboards, economy API
- `.claude/agents/engineering/infrastructure-engineer.md` — dedicated server fleet (Agones/GameLift/Hathora), auto-scaling, region routing, DDoS protection
- `.claude/agents/engineering/release-engineer.md` — live patch pipeline, hotfix process, feature flags, version compatibility

**Quality**
- `.claude/agents/quality/qa-engineer.md` — network-condition simulation tests, packet-loss scenarios, reconnect testing
- `.claude/agents/quality/performance-engineer.md` — server CPU per session, client frame time under network load, bandwidth usage

**Design**
- `.claude/agents/design/game-ux-specialist.md` — lobby UX, matchmaking feedback, disconnect/reconnect flows, spectator mode

**Domain**
- `.claude/agents/domain/gaming-domain-expert.md` — economy, IAP, anti-cheat, leaderboards, live-ops event system, ban pipeline

---

## Recommended skills

- `.claude/skills/game/SKILL.md` — core game loop, ECS, asset pipeline, playtest process
- `.claude/skills/security/SKILL.md` — server-authority model, receipt validation, DDoS mitigation, input validation
- `.claude/skills/performance/SKILL.md` — bandwidth profiling, server CPU profiling, client prediction tuning
- `.claude/skills/testing/SKILL.md` — network simulation tests, load tests, matchmaking queue simulation
- `.claude/skills/devops/SKILL.md` — dedicated server fleet CI/CD, canary deploys, rollback on live servers
- `.claude/skills/node-backend/SKILL.md` or `.claude/skills/go-backend/SKILL.md` — backend services for matchmaking, economy, leaderboards

---

## Recommended stack options

| Stack | Rationale |
|---|---|
| **Unreal/Unity + custom C++ game server + Agones on GKE** | Maximum control over server code; Agones handles fleet lifecycle, scaling, and health-checking on Kubernetes; best for competitive high-tick FPS/battle royale. |
| **Godot / Unity + Nakama (self-hosted or Heroic Cloud)** | Open-source real-time backend with matchmaking, leaderboards, social graph, and relay; lowest ops overhead for indie team; ideal for co-op and social games. |
| **Unity + PlayFab (Azure)** | Managed backend (matchmaking, economy, live-ops, multiplayer servers via MPS); strong integration with Xbox/Game Pass; good for mid-tier studios on Azure. |
| **Unity / Unreal + AWS GameLift + DynamoDB** | AWS-native dedicated server fleet management; suits teams already on AWS; GameLift Anywhere lets you test with local servers before cloud rollout. |

---

## Required checklists

- `.claude/checklists/performance.md` — client frame time under packet loss; server CPU per session; bandwidth per client; tick-rate stability
- `.claude/checklists/security.md` — server authority enforced for all game-state mutations; input validation on server; DDoS protection on session endpoints; IAP receipt validation
- `.claude/checklists/qa.md` — network-condition simulation (0% / 5% / 20% packet loss; 200 ms / 500 ms latency injection); reconnect; server crash recovery
- `.claude/checklists/production.md` — fleet auto-scaling tested to 2× expected peak; runbook for server outage; rollback procedure for bad live patch

---

## MVP scope pattern

**In the first cut (playable online slice)**
- One game mode, one map, minimum viable player count (e.g. 2-player co-op or 4v4 PvP)
- Server-authoritative game loop with client-side prediction for local responsiveness
- Basic matchmaking (quick-play queue, skill matching deferred to v2 unless core to design)
- Session lifecycle: lobby → countdown → game → end-of-match results → return to lobby
- Basic player data persistence (username, match history, basic stats)
- Disconnect handling: grace period to rejoin, graceful session end if host/server disconnects
- In-game text chat (even if voice is planned — voice is deferred)

**Defer until post-MVP**
- Ranked mode and MMR/ELO ladder (design the rating system now, expose it to players later)
- Anti-cheat integration (design the server-authority model now; EAC/VAC adds cert overhead)
- Battle pass and seasonal content (live-ops infrastructure designed, not populated)
- Cross-play (per-platform SDK integration deferred after core is stable)
- Voice chat (text chat first; voice adds moderation complexity)
- Spectator / replay system
- Guild / clan system
- Full content moderation pipeline (profanity filter, report queue, ban appeals)
- Full regional server coverage (launch in 1–2 regions, add regions by demand)

---

## Production risks

| Risk | Priority | Mitigation |
|---|---|---|
| Client-authoritative state — cheaters report "I killed them" to server | P0 | Server validates all game-state transitions; clients send inputs, not outcomes |
| No idempotency on item/currency grants — network retry double-grants rewards | P0 | Idempotency keys on every grant endpoint; deduplication at the economy service layer |
| DDoS on game server IP — session endpoints exposed | P0 | Route through relay/proxy; never expose dedicated server IP to clients until session is established; rate-limit matchmaking API |
| Session data lost on server crash — players lose progress | P0 | Checkpoint game state to durable store every N seconds (configurable); reconcile on reconnect |
| Fleet underprovisioned at launch spike | P0 | Load-test at 2× expected peak CCU; configure auto-scaling with pre-warm; have a "lobby queue" fallback |
| Desync in deterministic lockstep — clients diverge silently | P1 | Hash game state every N ticks; compare hashes between peers/server; disconnect and flag desynced clients |
| Packet loss causing rubber-banding — unacceptable at > 5% loss | P1 | Client-side prediction + server reconciliation; interpolation; tune dead-reckoning threshold |
| Virtual economy inflation — too many currency sources, not enough sinks | P1 | Model all sources and sinks before launch; see `.claude/agents/domain/gaming-domain-expert.md` |
| Ban without appeal — platform policy violation, community backlash | P1 | Automated detection → human review → appeal path; never auto-permanent-ban |
| Cross-play approval rejection by platform | P1 | Apply for cross-play approval early; Nintendo/Sony have separate approval processes |
| COPPA / child data exposure in chat or user profiles | P0 if applicable | Age gate or COPPA-mode: disable chat, disable social features, restrict data collection |

---

## Launch requirements

- All items in `.claude/checklists/production.md` are green
- Fleet auto-scaling successfully tested at 2× expected peak CCU with no session drops
- Reconnect tested: disconnect mid-session → rejoin within grace period → correct state restored
- Server crash tested: dedicated server process killed → new session allocated → players notified within 10 s
- Packet-loss simulation (5% and 20%) passes without desync or unacceptable rubber-banding
- Economy: all IAP end-to-end tested in sandbox; server-side receipt validation confirmed on every platform
- Anti-cheat: server-authority model verified; no client-reported position/health accepted as ground truth
- Matchmaking: queue tested at low population (< 50 concurrent); expansion policy confirmed to prevent infinite queues
- All P0/P1 bugs resolved; P2 triaged
- Runbook complete: how to patch a live server fleet, roll back a bad patch, and handle a DDoS
- Age rating approved on all target storefronts
- Privacy policy live; GDPR/CCPA consent flow active; COPPA compliance verified if applicable
- Platform cross-play approvals obtained (if cross-play is in scope)
- Monitoring active: server CPU, session count, queue time, reconnect rate, crash rate — all with alerting thresholds

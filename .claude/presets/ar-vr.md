# AR/VR/XR Preset

## Project type
An application or game built for extended-reality hardware where frame rate, latency, and user comfort are hard engineering constraints. Variants include:

- **Standalone VR app/game** — Meta Quest 3/3S, PICO 4; self-contained, GPU/thermal-limited
- **PC-tethered VR** — SteamVR (Valve Index, Vive), PlayStation VR2; higher fidelity, cable or Wi-Fi streaming
- **Mobile AR** — ARKit (iOS), ARCore (Android); camera passthrough, marker/surface/face tracking
- **Passthrough mixed reality** — Meta Quest MR, Apple Vision Pro; video-passthrough with anchored 3D objects
- **Spatial computing** — Apple Vision Pro visionOS; eye + hand input, no controllers, RealityKit
- **Enterprise AR** — HoloLens 2, Magic Leap 2; hands-free, industrial overlay on physical equipment
- **WebXR** — browser-based XR via WebXR Device API; broad reach, limited fidelity
- **Location-based / LBE** — theme-park / arcade installs; custom backpack PCs, arena tracking

## Typical use cases
- Immersive VR game with full locomotion and physics interactions
- AR product visualizer (furniture, clothing, automotive) in a retail mobile app
- Enterprise training simulation (warehouse ops, surgical procedure, equipment maintenance)
- Social VR space with multiplayer avatars and voice
- Architectural walkthrough / digital twin overlay
- WebXR marketing experience embedded in a webpage
- Physical therapy / rehabilitation application using motion tracking
- Museum or education app with spatial storytelling

## Required discovery questions
1. Which headsets and platforms are in scope for launch, and which are deferred (device matrix)?
2. What is the target render resolution and refresh rate per device — 72 Hz minimum / 90 Hz / 120 Hz?
3. Is locomotion free movement, teleportation, or seated/stationary? What comfort guardrails prevent motion sickness?
4. What interaction model is required — 6DoF controllers, hand tracking, gaze + pinch, voice, or gamepad?
5. Is there a multiplayer / social layer? If so, what are the latency and synchronization requirements?
6. What is the content strategy — user-generated, curated, procedurally generated, or streamed?
7. Are there age-gating or content-rating requirements (minors in VR, violent content, health disclaimers)?
8. What thermal and battery budget applies (standalone headsets throttle at ~5 W sustained GPU)?
9. Does the experience overlay the real world (passthrough/AR) requiring safety warnings or guardian-zone enforcement?
10. Is there accessibility scope — subtitles, colorblind modes, seated/stationary alternatives?

## Recommended agents

**Core:**
- `.claude/agents/core/product-manager.md`
- `.claude/agents/core/solution-architect.md`
- `.claude/agents/core/technical-lead.md`

**Engineering:**
- `.claude/agents/engineering/game-engineer.md`
- `.claude/agents/engineering/realtime-engineer.md`
- `.claude/agents/engineering/mobile-engineer.md` (for ARKit/ARCore/visionOS)
- `.claude/agents/engineering/backend-engineer.md` (multiplayer, content delivery)

**Quality:**
- `.claude/agents/quality/performance-engineer.md`
- `.claude/agents/quality/qa-engineer.md`
- `.claude/agents/quality/accessibility-auditor.md`
- `.claude/agents/quality/reliability-engineer.md`

**Design:**
- `.claude/agents/design/game-ux-specialist.md`
- `.claude/agents/design/mobile-ux-specialist.md` (AR variant)
- `.claude/agents/design/ui-ux-designer.md`

**Domain:**
- `.claude/agents/domain/ar-vr-domain-expert.md`
- `.claude/agents/domain/gaming-domain-expert.md`

## Recommended skills

- `.claude/skills/game/SKILL.md` — render loop, physics, asset pipeline
- `.claude/skills/performance/SKILL.md` — GPU profiling, draw-call budgets, foveation
- `.claude/skills/mobile/SKILL.md` — ARKit, ARCore, thermal management
- `.claude/skills/realtime/SKILL.md` — multiplayer state sync, interpolation
- `.claude/skills/ui-ux-design/SKILL.md` — spatial UI, diegetic interfaces
- `.claude/skills/backend/SKILL.md` — matchmaking, presence, content CDN
- `.claude/skills/testing/SKILL.md` — automated frame-time regression, simulator CI
- `.claude/skills/observability/SKILL.md` — in-headset telemetry, crash reporting

## Recommended stack options

| Option | Stack | Rationale |
|--------|-------|-----------|
| **Unity (cross-platform)** | Unity 6 + XR Interaction Toolkit + OpenXR + Photon/NGO | Broadest device support (Quest, SteamVR, ARCore, ARKit, HoloLens); largest asset ecosystem |
| **Unreal Engine (AAA fidelity)** | Unreal Engine 5 + OpenXR + EOS | Nanite/Lumen for PC-VR; best visual fidelity; Blueprints lower barrier; performance demands careful optimization on standalone |
| **Native visionOS** | SwiftUI + RealityKit + ARKit + Multipeer/CloudKit | Required for Apple Vision Pro spatial computing; fullest platform API access |
| **WebXR** | Three.js / Babylon.js + WebXR Device API + WebSocket | No install friction; works on Quest browser + ARCore WebXR; limited fidelity; good for marketing/demo |

See `.claude/stack-matrix/game.md`.

## Required checklists

- `.claude/checklists/performance.md` — frame-time budget per device; GPU/CPU split
- `.claude/checklists/game.md` — asset pipeline, input, save system
- `.claude/checklists/ui-ux.md` — comfort guidelines, reticle sizing, FOV
- `.claude/checklists/accessibility.md` — seated mode, subtitle support
- `.claude/checklists/mobile.md` (AR variant) — thermal, battery, camera permissions
- `.claude/checklists/security.md` — user data, spatial mapping data privacy
- `.claude/checklists/production.md`
- `.claude/checklists/launch.md`
- `.claude/checklists/privacy-compliance.md` — biometric and spatial data (BIPA, GDPR Art 9)
- `.claude/checklists/observability.md` — frame-time histograms, reprojection rate metrics

## MVP scope pattern

**In MVP:**
- Single target device (e.g., Meta Quest 3) at stable 72 Hz
- Core interaction loop fully playable (teleport or snap-turn locomotion for safety)
- Comfort guardrails: vignette on locomotion, guardian boundary respected, no sustained acceleration
- Basic spatial audio (positional cues)
- Crash reporting and frame-time telemetry
- Content rating / age-gate if required by store (Meta, Steam)
- Basic accessibility: recenter, seated mode, subtitle toggle

**Deferred:**
- Secondary device/platform ports
- Multiplayer / social presence
- Hand tracking (if controllers are primary)
- Progressive foveated rendering
- Cloud streaming version
- Haptic narrative scripting
- 120 Hz mode
- User-generated content pipeline

## Production risks

| Risk | Tag | Mitigation |
|------|-----|------------|
| Frame drops below 72 Hz causing nausea/disorientation | P0 | Lock render thread to frame budget; enable ASW/ATW reprojection as fallback; perf gate in CI |
| Motion-to-photon latency >20 ms causes sickness | P0 | Use platform-native reprojection; never block render thread with I/O; profile end-to-end latency per device |
| Passthrough safety: user walks into wall while in MR | P0 | Enforce guardian / boundary API; display proximity warning; minimum safe-play-area requirement in onboarding |
| Thermal throttling on standalone headset | P1 | Profile sustained 30-min session; adaptive quality scaler reduces resolution before throttle kicks in |
| Biometric / spatial mapping data leakage | P1 | Do not persist spatial mesh or eye-tracking data without explicit consent; comply with platform privacy APIs |
| Cybersickness from high-FOV locomotion | P1 | Comfort mode enabled by default; third-party comfort rating (Oculus CRC) |
| Controller input latency > 3 frames | P1 | Use platform input prediction APIs; test with profiler at 72/90/120 Hz |
| Age-inappropriate content reaching minors (VR) | P1 | Store age-gate; runtime parental-control API integration |
| Build size exceeding store limit (Meta: 4 GB APK) | P2 | Asset compression pipeline; streaming asset delivery for large worlds |
| Eye-tracking data used without BIPA/GDPR consent | P2 | Eye-tracking gated behind explicit consent; data not transmitted off-device without user action |
| Accessibility exclusion of users with vestibular disorders | P2 | Stationary / cockpit mode always available; comfort settings prominent in menu |

## Launch requirements

1. **Frame-time budget met on target device** — sustained 72 Hz (or target Hz) over 30-minute session under thermal load, verified by automated perf test.
2. **Comfort certification** — Oculus Comfort Rating (or equivalent) completed; comfort settings prominent at first launch.
3. **Guardian / boundary enforcement** — passthrough/MR builds respect platform guardian API; safety warning displayed.
4. **Privacy disclosure** — spatial mapping, eye-tracking, and voice data handling disclosed; platform privacy manifest complete.
5. **Age-gate implemented** — store metadata age rating submitted; runtime age-check if required.
6. **Accessibility minimum** — seated mode, subtitle/caption toggle, colorblind mode documented.
7. **Crash rate < 0.5%** on soak test (30-min session × 50 runs).
8. **Store submission assets complete** — screenshots, trailer captured at native resolution, content rating questionnaire.
9. **Legal review** — biometric data laws (BIPA, GDPR Art 9) cleared for all target markets.
10. **Thermal soak passed** — no performance cliff or safety shutdown during 45-minute sustained-play session.

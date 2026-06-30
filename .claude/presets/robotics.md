# Robotics Preset

## Project type
Software for autonomous or semi-autonomous physical systems where real-time control, functional safety, and fail-safe behavior are non-negotiable engineering requirements. Variants include:

- **Industrial robot arm** — pick-and-place, welding, assembly; ISO 10218-1/2 safety; collaborative (cobot) or caged
- **Mobile ground robot (AMR/AGV)** — warehouse logistics, last-mile delivery, outdoor field robots
- **Aerial vehicle (drone/UAV)** — autonomous flight, inspection, survey; FAA/EASA regulation
- **Surgical / medical robot** — IEC 62304, FDA 510(k)/De Novo; zero-tolerance failure
- **Service robot** — reception, cleaning, telepresence; mixed human-environment operation
- **Autonomous vehicle (AV)** — road-legal or campus-limited; ISO 26262 ASIL requirements
- **Underwater ROV** — inspection, maintenance; unreliable comms, no wireless E-stop
- **Space / extreme-environment** — radiation-hardened, long-latency uplink, no field service

## Typical use cases
- ROS 2 node graph controlling a 6-DOF arm with MoveIt 2 motion planning
- Fleet management server dispatching AMRs across a warehouse floor
- Drone inspection pipeline: autonomous waypoint flight, sensor data capture, defect ML model
- Digital twin simulation (Gazebo / Isaac Sim) for regression testing before hardware deployment
- OTA firmware update system for deployed robot fleet with rollback
- Safety monitoring daemon enforcing ISO 10218 collaborative-speed limits via force/torque sensing
- Edge-AI inference for object detection and semantic segmentation on robot compute (Jetson/RK3588)

## Required discovery questions
1. What is the operational design domain (ODD) — indoor/outdoor, structured/unstructured, human co-present or caged?
2. What are the real-time control frequency requirements (1 kHz servo loop? 100 Hz planning? 10 Hz perception)?
3. What functional-safety standard applies — ISO 10218, ISO 12100, ISO 26262 (AV), IEC 62304 (medical), DO-178C (aviation)?
4. What is the E-stop / fail-safe architecture — hardware interlocks, safety-rated PLC, or software-only?
5. What sensor suite is in scope — LiDAR, stereo camera, IMU, force/torque, GPS/RTK, encoders?
6. Is a simulation environment required for CI regression before hardware deployment?
7. What is the OTA update strategy for deployed fleet — phased rollout, rollback trigger, downtime window?
8. What are the latency and reliability constraints on the communication link (ROS 2 DDS, MQTT, 5G, radio)?
9. What edge compute platform is deployed on the robot (Jetson Orin, RK3588, x86 NUC, microcontroller)?
10. Are there export-control, regulatory, or certification requirements before commercial deployment?

## Recommended agents

**Core:**
- `.claude/agents/core/solution-architect.md`
- `.claude/agents/core/technical-lead.md`
- `.claude/agents/core/requirements-engineer.md`
- `.claude/agents/core/product-manager.md`

**Engineering:**
- `.claude/agents/engineering/realtime-engineer.md` — control loops, RT OS, DDS tuning
- `.claude/agents/engineering/backend-engineer.md` — fleet management, mission dispatch
- `.claude/agents/engineering/ai-ml-engineer.md` — perception, SLAM, behavior trees
- `.claude/agents/engineering/devops-engineer.md` — OTA, CI with sim, fleet monitoring
- `.claude/agents/engineering/cloud-architect.md` — telemetry ingestion, digital twin

**Quality:**
- `.claude/agents/quality/reliability-engineer.md`
- `.claude/agents/quality/security-auditor.md`
- `.claude/agents/quality/qa-engineer.md`
- `.claude/agents/quality/performance-engineer.md`
- `.claude/agents/quality/production-readiness-auditor.md`

**Domain:**
- `.claude/agents/domain/robotics-domain-expert.md`
- `.claude/agents/domain/iot-domain-expert.md`

## Recommended skills

- `.claude/skills/realtime/SKILL.md` — RT scheduling, DDS/ROS 2, control-loop latency
- `.claude/skills/iot-embedded/SKILL.md` — microcontroller firmware, hardware abstraction
- `.claude/skills/ai-ml/SKILL.md` — perception models, SLAM, edge inference
- `.claude/skills/backend/SKILL.md` — fleet management API, mission planner
- `.claude/skills/devops/SKILL.md` — CI with Gazebo/Isaac Sim, OTA pipeline
- `.claude/skills/security/SKILL.md` — network hardening, firmware signing, auth for remote ops
- `.claude/skills/observability/SKILL.md` — ROS 2 bag recording, telemetry, anomaly detection
- `.claude/skills/data-platform/SKILL.md` — sensor data lake, replay infrastructure
- `.claude/skills/testing/SKILL.md` — hardware-in-the-loop (HIL), sim regression, chaos tests

## Recommended stack options

| Option | Stack | Rationale |
|--------|-------|-----------|
| **ROS 2 + C++ (standard)** | ROS 2 Jazzy + C++17 + Nav2 + MoveIt 2 + Gazebo Harmonic | Industry standard; broadest hardware driver support; real-time capable with CycloneDDS or Zenoh |
| **ROS 2 + Python (rapid prototype)** | ROS 2 Jazzy + Python rclpy + Nav2 + Isaac Sim | Faster iteration; Python not suitable for hard-RT control nodes; good for perception/planning layer |
| **Rust robotics** | Zenoh + r2r (ROS 2 Rust) + Tokio async | Memory safety in safety-critical code; no GC pauses; growing ecosystem; fewer drivers than C++ |
| **Micro-ROS (MCU tier)** | micro-ROS + FreeRTOS/Zephyr + CAN/EtherCAT | For microcontrollers on actuators/sensors; bridges to ROS 2 agent via serial/UDP |

See `.claude/stack-matrix/backend.md` and `.claude/stack-matrix/cloud-devops.md`.

## Required checklists

- `.claude/checklists/production.md`
- `.claude/checklists/security.md` — firmware signing, remote-access hardening
- `.claude/checklists/performance.md` — control-loop jitter, worst-case execution time (WCET)
- `.claude/checklists/observability.md` — telemetry, ROS bag archival, alert pipelines
- `.claude/checklists/incident-response.md` — fleet recall, E-stop broadcast, field recovery
- `.claude/checklists/release-rollback.md` — OTA phased rollout, rollback on CRC/heartbeat failure
- `.claude/checklists/dependencies.md` — supply-chain for embedded libraries
- `.claude/checklists/privacy-compliance.md` — video/sensor data from human environments
- `.claude/checklists/devops.md` — sim CI, HIL CI, containerized build

## MVP scope pattern

**In MVP:**
- Single robot platform, single operational scenario
- Core control loop at target frequency with jitter budget met
- Hardware E-stop wired and software-monitored; kills motion within 100 ms of trigger
- Basic localization and navigation (Nav2 with pre-built map, or fixed workspace)
- Manual teleoperation mode as fallback to autonomous
- ROS 2 bag recording for post-incident replay
- OTA mechanism with signature verification and automatic rollback on heartbeat loss
- Basic obstacle avoidance (safety stop, not re-planning)
- Remote monitoring dashboard: battery, pose, mode, active faults

**Deferred:**
- Multi-robot coordination / fleet
- Semantic scene understanding
- Dynamic re-mapping (live SLAM in production)
- Manipulation with force control / compliant grasping
- Edge-AI model auto-update pipeline
- Regulatory certification submission
- High-availability fleet server (active-passive HA)
- International localization (multi-language HMI)

## Production risks

| Risk | Tag | Mitigation |
|------|-----|------------|
| E-stop failure: robot does not halt on trigger | P0 | Hardware-wired safety relay; safety-rated PLC (Cat 3 / PLd per ISO 13849); E-stop tested every deployment |
| Collision with person in collaborative zone | P0 | ISO 10218-2 speed/force limits enforced at firmware level; redundant presence sensing; workspace risk assessment documented |
| Control-loop overrun causing actuator fault | P0 | WCET analysis; RT scheduling with priority ceiling; watchdog timer reboots node on overrun |
| OTA bricked fleet (bad firmware, no rollback) | P0 | Cryptographically signed images; A/B partition rollback; heartbeat-based automatic rollback within 60 s |
| Sensor spoofing (LiDAR/GPS) causing unsafe navigation | P1 | Sensor fusion cross-validation; anomaly detection on sensor disagreement; safe-stop on persistent disagreement |
| Communication link loss during autonomous operation | P1 | Onboard autonomous safe-stop or hold-in-place policy; no cloud-dependent safety path |
| Cyber attack via robot network interface | P1 | DDS security (SROS 2); mTLS for fleet API; network segmentation; no public internet exposure |
| Privacy violation from camera/audio in human spaces | P1 | Data minimization; on-device processing preferred; explicit consent for any off-device transmission |
| Sim-to-real gap causes untested behavior in production | P1 | Standardized sim validation suite; staged deployment: sim → HIL → controlled site → production |
| Regulatory non-compliance at deployment | P1 | Risk assessment per ISO 12100 complete before site deployment; CE/UL marking checklist |
| Battery thermal runaway on mobile platform | P2 | BMS monitoring with shutdown at temperature threshold; fire-rated storage during charging |
| Fleet telemetry data volume overwhelming ingestion | P2 | Edge-side pre-aggregation; selective bag upload (anomaly-triggered); tiered storage |

## Launch requirements

1. **Functional safety documentation** — risk assessment (ISO 12100 / ISO 10218) complete and signed off before any human-co-present operation.
2. **E-stop verified** — wired hardware E-stop tested on target hardware: motion stops within 100 ms; test result logged and signed.
3. **WCET budget met** — control-loop worst-case execution time measured and within 80% of cycle budget on production hardware.
4. **OTA with rollback verified** — staged OTA to 5% of fleet; automatic rollback on heartbeat-loss confirmed working end-to-end.
5. **Sim regression suite green** — full Nav2/MoveIt scenario suite passes in CI on Gazebo/Isaac Sim before any hardware deploy.
6. **Cyber hardening complete** — SROS 2 / mTLS enabled; penetration test of fleet API; no open management ports on robot network interface.
7. **Privacy compliance confirmed** — camera/audio data handling reviewed against GDPR/CCPA for deployment region; consent mechanism implemented.
8. **Telemetry live** — real-time battery, mode, fault, and pose visible in operations dashboard; alerting configured for critical faults.
9. **Incident response runbook published** — fleet-wide E-stop broadcast procedure, field-recovery steps, and contact list documented.
10. **Site acceptance test (SAT) passed** — minimum 8-hour supervised autonomous run at production site with no P0/P1 faults recorded.

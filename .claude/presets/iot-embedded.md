# IoT / Embedded Preset

## Project type

Firmware, device fleet management, and cloud-connected IoT systems. Common variants:

- **MCU-only** — bare-metal or RTOS firmware with no cloud connection (ESP32, STM32, nRF52, RP2040).
- **Cloud-connected device** — device sends telemetry to a cloud backend; receives commands and OTA updates.
- **Edge + cloud** — local processing on a gateway (Raspberry Pi, Jetson, i.MX8), cloud for aggregation and dashboards.
- **Industrial IoT** — SCADA integration, Modbus/OPC-UA, deterministic control loops, safety certification (IEC 62443, IEC 61508).
- **Consumer IoT** — BLE/Wi-Fi products with mobile companion app; OTA via app store-style release train.
- **Fleet + digital twin** — manages thousands of heterogeneous devices; per-device state shadow and remote diagnostics.

## Typical use cases

- Smart home / building automation (lighting, HVAC, energy monitoring).
- Industrial machine monitoring, predictive maintenance, quality control vision.
- Asset tracking (GPS + cellular: LTE-M, NB-IoT).
- Agricultural sensors, environmental monitoring, water management.
- Medical wearables / remote patient monitoring.
- Automotive telematics and in-vehicle infotainment (CAN bus, AUTOSAR).
- Robotics firmware and actuator control.
- Retail shelf / cold-chain temperature logging.

## Required discovery questions

1. What is the target hardware? (MCU family, clock speed, RAM/flash budget, peripherals needed.) Is it custom silicon, a module, or off-the-shelf dev board?
2. What connectivity protocol is required on-device? (Wi-Fi, BLE, LoRaWAN, Zigbee, LTE-M/NB-IoT, Ethernet, CAN, RS-485.) Are you behind NAT or firewall?
3. What are the hard real-time requirements? Any safety-critical control loops where a missed deadline is a hazard?
4. What is the expected fleet size and growth trajectory? (10 prototypes, 10k production units, 1M devices in 3 years.)
5. How will firmware updates be delivered? (USB/JTAG only, BLE DFU, HTTPS OTA, cellular push.) What is the acceptable downtime window for an update?
6. What cloud platform and protocol does the system target? (MQTT/AMQP to AWS IoT Core, Azure IoT Hub, GCP IoT, self-hosted EMQX, or custom.)
7. What are the power constraints? (Mains-powered, USB, battery — capacity and expected lifetime, solar/energy-harvesting.)
8. Are there regulatory or certification requirements? (CE, FCC, UL, RoHS, ATEX, FDA 510(k), IEC 62443, FIPS 140-2.)
9. What data must the device store locally if connectivity is lost? What is the maximum acceptable data loss window?
10. Who manages the device fleet in production? (Engineering, Ops, customer's IT department.) Do they need a self-service dashboard?

## Recommended agents

**Core**
- `.claude/agents/core/orchestrator.md` — flow control and gate enforcement.
- `.claude/agents/core/solution-architect.md` — overall hardware/software/cloud architecture.
- `.claude/agents/core/requirements-engineer.md` — captures real-time and safety requirements.

**Engineering**
- `.claude/agents/domain/iot-domain-expert.md` — MCU-level firmware, RTOS task design, peripheral drivers.
- `.claude/agents/engineering/backend-engineer.md` — telemetry ingestion, command dispatch, device registry.
- `.claude/agents/engineering/devops-engineer.md` — CI/CD for firmware artifacts, OTA release train.

**Quality**
- `.claude/agents/quality/security-auditor.md` — secure boot, TLS mutual auth, credential storage, firmware signing.
- `.claude/agents/quality/qa-engineer.md` — HIL (hardware-in-the-loop) test planning, simulation harnesses.
- `.claude/agents/quality/production-readiness-auditor.md` — fleet monitoring, rollback gates, observability.
- `.claude/agents/quality/reliability-engineer.md` — watchdog design, OTA rollback, failure-mode analysis.

**Domain**
- `.claude/agents/domain/iot-domain-expert.md` — connectivity protocols, fleet patterns, OTA strategy.

## Recommended skills

- `.claude/skills/iot-embedded/SKILL.md` — firmware workflow, hardware tiers, OTA, edge processing.
- `.claude/skills/security/SKILL.md` — secure boot chain, TLS, credential rotation, firmware signing.
- `.claude/skills/backend/SKILL.md` — telemetry ingestion pipeline, device registry, time-series storage.
- `.claude/skills/devops/SKILL.md` — firmware CI, artifact signing, staged OTA release.
- `.claude/skills/data-platform/SKILL.md` — high-throughput telemetry ingest, time-series queries.
- `.claude/skills/production-readiness/SKILL.md` — fleet health dashboards, alert thresholds, runbooks.
- `.claude/skills/testing/SKILL.md` — unit tests for firmware logic, simulation/emulation strategies.
- `.claude/skills/docker-kubernetes/SKILL.md` — containerised backend services for cloud-side components.

## Recommended stack options

| Stack | Rationale |
|-------|-----------|
| **ESP-IDF / FreeRTOS + AWS IoT Core + TimescaleDB** | Best-in-class ESP32 SDK; AWS IoT Core handles MQTT at fleet scale with device shadows; TimescaleDB for time-series telemetry with SQL familiarity. See `.claude/stack-matrix/backend.md`. |
| **Zephyr RTOS + Azure IoT Hub + ADX / InfluxDB** | Zephyr's modular HAL supports nRF, STM32, NXP in one codebase; Azure IoT Hub integrates with Azure Data Explorer for analytics. |
| **Yocto Linux (MPU) + EMQX self-hosted + Grafana** | Full Linux on gateway-class hardware; EMQX MQTT broker on-prem for air-gapped or sovereignty requirements; Grafana for dashboards. |
| **Arduino / PlatformIO + Balena + InfluxDB Cloud** | Rapid prototyping for small teams; Balena.io manages container-based OTA on Linux devices; InfluxDB Cloud for time-series with free tier. |

## Required checklists

- `.claude/checklists/security.md` — augment with: secure boot verified, TLS client certs rotatable, no hardcoded credentials in firmware binary, firmware signature chain validated before boot.
- `.claude/checklists/production.md` — augment with: OTA rollback tested, fleet health metric baselines set, device registry reconciliation process documented.
- `.claude/checklists/qa.md` — augment with: HIL or emulation test coverage, watchdog reset path tested, offline buffering and reconnection tested.
- `.claude/checklists/performance.md` — augment with: RAM/flash budget verified under worst-case load, latency of control loop measured, telemetry throughput under peak fleet load stress-tested.

## MVP scope pattern

**In the first cut:**
- Single device type, one firmware target, one connectivity protocol.
- Device connects, authenticates with a server certificate, publishes telemetry (JSON or CBOR over MQTT/HTTPS), and receives a single command type.
- Minimal cloud backend: ingest endpoint, device registry table, time-series store, one dashboard showing last-known value per device.
- OTA stub: device checks for a new firmware version on boot; downloads and boots into it; rolls back on CRC failure.
- Secure provisioning: unique per-device credential injected at factory flash time (no hardcoded shared key).

**Deferred to later:**
- Multiple device types or hardware variants.
- Edge ML inference, local anomaly detection.
- Full fleet management UI (bulk commands, geofencing, segmented rollout).
- Digital twin / device shadow with historical replay.
- Advanced analytics (correlation, predictive maintenance models).
- Multi-region ingestion, global fleet routing.
- Third-party integrations (ERP, SCADA, BI tools).

## Production risks

| Risk | Priority | Notes |
|------|----------|-------|
| OTA brick: bad firmware locks out entire fleet | P0 | Dual-bank bootloader with CRC check + auto-rollback; staged rollout (1% → 10% → 100%); hardware watchdog as last resort. |
| Hardcoded credentials in firmware | P0 | Per-device certificate provisioned at manufacture; never a shared secret in binary. Enforce via `.claude/checklists/security.md`. |
| No rollback path for breaking protocol change | P0 | Version the MQTT topic schema and payload format from day one; maintain backward compatibility for N-1 firmware. |
| Unbounded telemetry volume overloading backend | P1 | Rate-limit ingestion per device; apply exponential backoff + jitter on reconnect; queue telemetry on-device during outage. |
| Secure boot not enabled on production hardware | P1 | Add secure boot to the factory flash script; verify in production smoke test before shipping units. |
| Battery drain from aggressive polling | P1 | Use interrupt-driven wakeup or MQTT keepalive tuning; measure current draw in deep-sleep and active state. |
| Missing offline buffering: data loss during outage | P1 | Device stores telemetry in flash ring buffer; flushes on reconnect with idempotent message IDs. |
| Regulatory certification missed pre-launch | P1 | Identify required certs (FCC, CE, etc.) in discovery; plan for 8–16 week certification lead time; do not ship without. |
| No monitoring of fleet-level firmware version spread | P2 | Track firmware version distribution in device registry; alert when >10% of fleet is on EOL firmware. |
| Memory leak in long-running RTOS tasks | P2 | Static memory allocation preferred on MCUs; heap usage tracked; soak test for 72h minimum. |

## Launch requirements

- Secure boot enabled and verified on production hardware units.
- Per-device unique credentials provisioned; no shared secret in firmware binary.
- OTA update tested end-to-end on representative hardware: update applied, CRC validated, rollback triggered on intentional corruption.
- Staged OTA rollout pipeline in place with automatic halt on error-rate spike.
- Telemetry pipeline load-tested at 2× expected peak fleet volume.
- Device registry shows real-time online/offline status for all devices.
- Alert firing on device silent (no telemetry for N minutes) and on OTA failure.
- Runbook for: recovering a bricked device, revoking a compromised device certificate, emergency fleet-wide firmware halt.
- All required regulatory certifications obtained.
- Legal/privacy review complete for any PII in telemetry (location, usage patterns).

---
name: iot-embedded
description: >
  Activate when the project involves IoT devices, embedded firmware, edge computing, telemetry
  ingestion, fleet management, or OTA updates. Triggers on: keywords like "firmware", "MCU",
  "RTOS", "MQTT", "Zigbee", "BLE", "LoRaWAN", "CAN bus", "sensor", "actuator", "OTA",
  "edge", "gateway", "fleet", "digital twin", "FreeRTOS", "Zephyr", "ESP32", "STM32",
  "Raspberry Pi", "AWS IoT", "Azure IoT Hub", "ThingsBoard".
---

# IoT & Embedded Systems Development

## When to use
- Writing or modifying device firmware (bare-metal or RTOS)
- Designing the telemetry pipeline from device to cloud
- Building device provisioning, fleet management, or OTA update flows
- Implementing edge processing to reduce cloud data volume
- Integrating device data into a backend service or digital twin
- Hardening device security (secure boot, TLS, credential management)
- Designing for constrained resources: RAM ≤ 256 KB, flash ≤ 1 MB, battery-powered

## Workflow

1. **Classify the hardware tier** — determines acceptable toolchain and patterns:
   | Tier | Examples | OS | Language |
   |------|----------|----|----------|
   | Microcontroller (MCU) | ESP32, STM32, nRF52 | Bare-metal / FreeRTOS / Zephyr | C, C++, Rust (embedded) |
   | Microprocessor (MPU) | Raspberry Pi, i.MX8 | Linux (Yocto, Buildroot) | C, Python, Rust |
   | Edge gateway | Jetson Nano, x86 SBC | Ubuntu, Debian | Any |
   | Cloud-connected module | SIM7080G, ESP-AT | AT commands | Script/config |

2. **Define the connectivity stack** — choose protocol based on range, bandwidth, and power:
   | Protocol | Range | Power | Bandwidth | Use case |
   |----------|-------|-------|-----------|----------|
   | BLE 5 | ~100 m | Ultra-low | Low | Short-range sensor, wearable |
   | Wi-Fi | ~50 m | Medium | High | Local gateway, camera |
   | Zigbee / Z-Wave | ~30 m mesh | Low | Low | Smart home mesh |
   | LoRaWAN | ~10 km | Ultra-low | Very low | Agriculture, utilities |
   | LTE-M / NB-IoT | Cellular | Low | Low | Remote tracking, meters |
   | MQTT over TLS | IP-based | Varies | Medium | Standard IoT messaging |

3. **Design the firmware architecture**:
   - Separate HAL (hardware abstraction layer), application logic, and communication stack into distinct modules.
   - On RTOS: assign tasks with explicit priorities; never block high-priority tasks with I2C/SPI polling.
   - Use a message queue between ISR (interrupt service routine) and application task — never call blocking functions from an ISR.
   - Define a watchdog timer; reset the device if the main loop stalls beyond `WDT_TIMEOUT_MS`.
   - Linker script must account for `.bss`, `.data`, `.rodata`, stack, and heap; leave ≥10% flash headroom.

4. **Telemetry pipeline design**:
   ```
   Sensor → MCU firmware → (edge filter/aggregate) → Gateway → MQTT/HTTPS → Broker/Ingestion → Time-series DB → API → Dashboard
   ```
   - Define telemetry schema upfront: `{ device_id, timestamp_utc, metric_name, value, unit, quality }`.
   - Apply edge filtering: send only when value changes by > threshold or at a fixed heartbeat interval (e.g., every 60 s).
   - Buffer telemetry locally (SPIFFS, LittleFS, SD card) when connectivity is lost; replay on reconnect with deduplication.
   - Use QoS 1 (at-least-once) for critical alerts; QoS 0 for high-frequency sensor data.

5. **Device provisioning & identity**:
   - Each device gets a unique X.509 certificate or pre-shared key (PSK) provisioned at manufacturing time.
   - Never hardcode Wi-Fi credentials or cloud endpoint URLs in firmware; use a provisioning flow (BLE pairing app, captive portal, factory NVS partition).
   - Store secrets in a hardware-backed secure element (ATECC608, ESP32 eFuse, TrustZone) — never in plaintext flash.
   - Implement device registration API: `POST /devices { serial_number, certificate_pem }` → returns `device_id` and cloud endpoint.

6. **OTA update flow**:
   a. Build and sign the firmware binary (RSA-2048 or Ed25519 signature).
   b. Upload signed binary to the update server (S3, Azure Blob, or dedicated OTA service).
   c. Device polls for updates at startup and on a schedule (e.g., every 6 h).
   d. Device verifies signature before writing to the update partition.
   e. Dual-bank (A/B) partitioning: write to inactive bank → reboot → verify → commit or rollback.
   f. Report OTA status (success/failure/version) to fleet management backend after reboot.
   g. Never brick: always keep a known-good rollback partition and a bootloader that cannot be OTA-updated without physical access.

7. **Edge computing**:
   - Run ML inference on-device only if the model fits in RAM after quantization (TFLite Micro, ONNX Runtime Mobile).
   - Pre-aggregate: compute mean/min/max/std over a 1-minute window on-device; send one message instead of 60.
   - Alert locally: trigger an actuator or alarm without cloud round-trip when latency matters (< 50 ms).
   - Synchronize edge clocks via NTP or GPS PPS; timestamp every reading at the source.

8. **Fleet management**:
   - Track per-device: firmware version, last-seen timestamp, connectivity status, battery level, error count.
   - Group devices by site, device type, firmware cohort.
   - Phased OTA rollout: deploy to 5% → monitor error rate for 24 h → 25% → 100%.
   - Remote diagnostics: device publishes a `$device/<id>/log` topic; ops team subscribes to pull logs without SSH.

9. **Security hardening**:
   - Enable secure boot (chain of trust from bootloader to application).
   - Disable JTAG and UART debug interfaces in production firmware builds.
   - Enforce TLS 1.2+ for all cloud communication; pin the CA certificate in firmware.
   - Rotate device credentials without physical access using a credential vending service.
   - Run a threat model against OWASP IoT Top 10 before production release.

10. **Testing strategy**:
    - **Unit tests**: run on host (PC) using a hardware stub/mock; no hardware required (e.g., Unity + CMock, Zephyr twister).
    - **Integration tests**: run on target hardware in CI using a hardware-in-the-loop (HIL) rig.
    - **Protocol tests**: verify MQTT message format, QoS behavior, reconnection logic with a local broker (Mosquitto).
    - **OTA tests**: test successful update, interrupted update mid-write, signature verification failure, rollback.
    - **Endurance tests**: run device for 72 h continuously; confirm no memory leak, watchdog trip, or crash.

## Standards

**Do:**
- Use fixed-width integer types (`uint8_t`, `int32_t`) — never `int` or `long` in firmware.
- Declare ISR variables as `volatile`; use atomic reads on MCUs without memory barriers.
- Zero-initialize all struct fields explicitly; rely on default zero-init only in `.bss`.
- Log firmware version, build timestamp, and chip ID to serial on boot.
- Use semantic versioning for firmware: `MAJOR.MINOR.PATCH`; bump MAJOR for breaking protocol changes.

**Do not:**
- Use `malloc`/`free` in firmware on resource-constrained MCUs — use static allocation pools.
- Perform blocking I/O in interrupt handlers.
- Ship firmware with debug logging enabled at VERBOSE level — costs flash and CPU.
- Use `strcpy` or `sprintf` without bounds checks; use `strncpy`, `snprintf`.
- Expose device management APIs without authentication even on a local network.
- `rm -rf` or wipe flash partitions containing provisioning data without explicit operator confirmation.

## Common mistakes to avoid

- **Stack overflow**: default FreeRTOS task stacks are small (256–1024 bytes). Profile stack high-water mark with `uxTaskGetStackHighWaterMark` in development.
- **Clock drift**: devices without NTP drift seconds per day; timestamps become meaningless after 24 h. Always sync on connect and re-sync periodically.
- **No offline buffering**: when MQTT connection drops, unsent data is lost. Implement a circular log buffer in NVS/flash.
- **Hardcoded endpoints**: firmware pointing to `dev.api.example.com` shipped to production. Use build-time configuration flags.
- **OTA without rollback**: a bad firmware update bricks thousands of devices. A/B partitioning is non-negotiable.
- **Floating-point on Cortex-M0**: M0 has no FPU; float operations compile to slow software routines. Use fixed-point arithmetic for sensor scaling.
- **Assuming reliable connectivity**: design every device as if connectivity is intermittent by default.

## Output format

A typical IoT project structure:

```
firmware/
  src/
    hal/              # Hardware abstraction (GPIO, SPI, I2C, UART)
    drivers/          # Peripheral drivers (sensor, modem, display)
    app/              # Application logic (state machine, business rules)
    comms/            # MQTT, HTTP, BLE stack integration
    ota/              # OTA update manager
    main.c / main.cpp
  include/
  test/
    unit/             # Host-side unit tests (Unity/CMock)
    integration/      # HIL tests
  CMakeLists.txt / platformio.ini / Makefile
  partitions.csv      # Partition table (ESP-IDF)
  sdkconfig           # RTOS/SDK config (tracked in Git)
cloud/
  ingestion/          # MQTT broker → time-series DB pipeline
  fleet/              # Device registry, OTA management API
  api/                # REST API for dashboards and apps
  provisioning/       # Device onboarding service
docs/
  telemetry-schema.yaml
  provisioning-flow.md
  ota-runbook.md
```

Reference architecture template: `.claude/templates/architecture.md`

## Related checklists
- `.claude/checklists/security.md` — secure boot, TLS, credential hygiene, OWASP IoT Top 10
- `.claude/checklists/performance.md` — RAM/flash budget, latency, power consumption
- `.claude/checklists/launch.md` — HIL test pass, OTA rollback verified, fleet monitoring live

## Related agents
- `.claude/agents/core/orchestrator.md` — overall project flow
- `.claude/agents/stack/backend/` — cloud backend receiving device telemetry
- `.claude/agents/stack/cloud/` — cloud infrastructure for fleet and ingestion
- `.claude/agents/quality/` — testing strategy including HIL and endurance tests

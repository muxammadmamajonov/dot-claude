# Realtime Stack Matrix

Choose by answering: (1) Is communication one-way (server→client) or bidirectional? (2) Is it peer-to-peer media/data, or client↔server messaging? (3) Do you need collaborative document state (CRDTs) or just event delivery? (4) What is the connection count and message volume at target scale? Most projects start with WebSocket or SSE and only need a managed service once operational complexity becomes a bottleneck. Add CRDT libraries only when you need conflict-free collaborative editing — they carry significant complexity overhead.

Key decision drivers: directionality, latency requirements, connection concurrency, infrastructure ownership vs. managed service cost, mobile/unreliable network behavior, and offline-first requirements.

---

## WebSocket

- **When to use:** Any bidirectional, low-latency communication over TCP — chat, live dashboards, multiplayer games, collaborative editing backends, trading UIs, live notifications where the client also sends events. The baseline choice for most realtime features.
- **When NOT to use:** When communication is server→client only (SSE is simpler and has automatic reconnect). When you don't control the network and firewalls may block upgrade headers (some enterprise proxies strip WebSocket). When the payload is media/audio/video (use WebRTC).
- **Strengths:** Full-duplex; works in every modern browser and runtime; low overhead per message after handshake; well-understood protocol (RFC 6455); easy to implement with `ws` (Node), `websockets` (Python), Gorilla (Go), or built-in browser `WebSocket`.
- **Weaknesses:** Stateful connections require sticky sessions or a pub/sub broker (Redis Pub/Sub, NATS) to fan out across multiple server instances; no built-in reconnect or message delivery guarantee (must implement yourself); HTTP/2 multiplexing doesn't apply (each WS is one TCP connection); mobile network changes (WiFi→LTE) drop the connection.
- **Team fit:** Any backend team. Complexity lives in the connection management and horizontal scaling layer.
- **Scale fit:** A single Node.js server handles ~10K–50K concurrent connections; scale out with a Redis Pub/Sub fan-out layer or a message broker. Above 100K concurrent connections, evaluate managed services.
- **Production risks:** Missing heartbeat/ping-pong → silent dead connections accumulate. No horizontal scale without a broker. Memory leaks if connection cleanup on disconnect is not handled. Proxy/load-balancer timeout misconfiguration (set idle timeout > heartbeat interval).

---

## SSE (Server-Sent Events)

- **When to use:** One-way server→client push: live feeds, progress tracking, LLM streaming responses, notification banners, status updates. Much simpler than WebSocket when the client doesn't need to send data back over the same channel.
- **When NOT to use:** Bidirectional communication (use WebSocket). Binary data streams (SSE is text/UTF-8). When you need more than ~6 concurrent SSE streams per browser origin (HTTP/1.1 browser limit; use HTTP/2 to remove this constraint).
- **Strengths:** Plain HTTP — works through all proxies, CDNs, and load balancers without special configuration; browser reconnects automatically with `Last-Event-ID`; trivial to implement on any HTTP server; no special protocol; streaming responses for LLM completions are the canonical use case today.
- **Weaknesses:** Unidirectional — client must use a separate HTTP request to send data; browser limit of 6 connections per origin on HTTP/1.1; not suitable for high-frequency bidirectional messaging; some older mobile browsers have limited support.
- **Team fit:** Any team. SSE is the lowest-complexity realtime option when directionality is server→client.
- **Scale fit:** Scales horizontally like any HTTP endpoint behind a load balancer; use `Transfer-Encoding: chunked` or HTTP/2 streaming. For fan-out (same event to many clients) still need a broker or pub/sub layer.
- **Production risks:** Nginx/reverse proxy buffering SSE responses (must set `X-Accel-Buffering: no`). Missing `retry:` field means clients use a short default reconnect interval. Long-lived SSE connections hold a server thread/connection on blocking servers (use async framework — FastAPI, Node, Go).

---

## WebRTC

- **When to use:** Peer-to-peer audio, video, or arbitrary data between browsers or native clients. Video conferencing, screen sharing, real-time gaming between peers, P2P file transfer, low-latency data channels.
- **When NOT to use:** Server-to-client notifications or pub/sub messaging — WebRTC is designed for peer communication, not server-push. Projects without a signaling server to handle offer/answer exchange. Teams that need a simple solution — WebRTC has a steep learning curve.
- **Strengths:** Sub-100ms latency for media; DTLS + SRTP encryption by default; browser-native (no plugin); data channels support arbitrary binary data; NAT traversal via STUN/TURN.
- **Weaknesses:** Requires a signaling server (any WebSocket or HTTP channel for SDP offer/answer exchange); TURN server needed for ~15–20% of connections that can't punch through NAT; complex API; SFU/MCU required for multi-party calls at scale (simple mesh breaks beyond ~4 participants); debugging is painful; spec and browser implementation quirks.
- **Team fit:** Specialist video/media engineers or teams willing to invest in learning curve. For managed video, use Daily.co, Agora, Livekit, or Twilio Video instead.
- **Scale fit:** P2P scales without server bandwidth (both sides send directly); multi-party requires an SFU server (Mediasoup, Janus, LiveKit) which scales via horizontal SFU clusters.
- **Production risks:** TURN server bandwidth costs spike in poor network conditions. ICE connection failures for users behind symmetric NAT without TURN. Browser codec negotiation failures. SDP mismatch bugs across browser versions.

---

## Pusher

- **When to use:** Teams that need managed WebSocket infrastructure quickly — rapid prototyping, early-stage products, or projects where the team lacks backend expertise to operate a WebSocket server. Also strong for presence channels (who is online) and client events.
- **When NOT to use:** Cost-sensitive projects at scale (Pusher pricing grows linearly with concurrent connections and messages); projects with very high message frequency (above ~10 msg/sec per channel gets expensive); apps that need to self-host for data residency.
- **Strengths:** Zero server infrastructure to manage; SDKs for every platform; presence channels (online user lists) built-in; client events (peer-to-peer via Pusher relay); generous free tier for prototyping; reliable delivery with reconnect handled by SDK.
- **Weaknesses:** Per-connection and per-message pricing becomes expensive above moderate scale; 100 KB message size limit; no message persistence/history by default; vendor lock-in (Pusher-specific SDK, channel naming conventions); limited to their infrastructure regions.
- **Team fit:** Frontend-heavy teams; startups moving fast; projects where realtime is a secondary feature.
- **Scale fit:** Works up to ~500 concurrent connections affordably; above that, evaluate Ably or self-hosted WebSocket.
- **Production risks:** Hitting message/connection rate limits unexpectedly; Pusher outage affecting your product (no self-host fallback); cost spike from a viral event.

---

## Ably

- **When to use:** Production-grade managed realtime messaging at scale — more powerful than Pusher with guaranteed message ordering, message history, presence, and a fiber-optic global edge network. Strong for IoT data streams, collaborative apps, and live sports/events.
- **When NOT to use:** Simple use cases where Pusher free tier or a self-hosted WebSocket is sufficient. Cost-sensitive projects at very high volume (evaluate self-hosted at that point).
- **Strengths:** Guaranteed message ordering; message persistence and history (replay on reconnect); presence; global edge network with <65ms latency; support for WebSocket, SSE, MQTT, and HTTP fallback; protocol-agnostic (can publish from any HTTP client); delta compression for bandwidth reduction; SLA-backed uptime.
- **Weaknesses:** More complex than Pusher; pricing is usage-based and can be significant at scale; still vendor lock-in; some advanced features (delta compression, firehose) are enterprise-tier.
- **Team fit:** Teams that want managed infrastructure without ops burden but need production reliability guarantees beyond Pusher.
- **Scale fit:** Designed for millions of concurrent connections; used for live sports scoring and trading platforms.
- **Production risks:** Vendor dependency for a core product feature; complex quota monitoring to avoid overage charges.

---

## Supabase Realtime

- **When to use:** Projects already using Supabase (PostgreSQL backend). Supabase Realtime provides Postgres change data capture (CDC) over WebSocket — clients subscribe to database table changes and receive row-level events. Also supports broadcast (arbitrary messages) and presence.
- **When NOT to use:** Projects not using Postgres/Supabase; use cases that need sub-10ms latency (CDC has processing delay); very high-frequency events where DB write-then-CDC is inefficient.
- **Strengths:** Zero additional infrastructure if you're on Supabase; row-level security (RLS) applies to realtime subscriptions (critical for multi-tenant apps); no separate pub/sub layer needed for data sync; broadcast and presence channels available; open-source and self-hostable.
- **Weaknesses:** Latency is higher than direct WebSocket (event travels: client write → Postgres WAL → Realtime server → subscriber); tightly coupled to Supabase/Postgres; connection limits depend on Supabase plan; not suitable as a general-purpose message bus.
- **Team fit:** Full-stack teams building on Supabase; especially good for apps with a live data dashboard or collaborative list/feed that mirrors database state.
- **Scale fit:** Supabase Pro/Team plans handle thousands of concurrent realtime connections; self-host for unlimited scale.
- **Production risks:** RLS misconfiguration exposing rows to wrong users via realtime. Realtime connection count limits on free/pro tier. WAL replication lag under heavy write load.

---

## PubNub

- **When to use:** IoT device telemetry, geolocation tracking, push notification delivery at global scale, and chat infrastructure. PubNub's global PoP network provides low-latency delivery across 175+ countries including regions where other providers have poor coverage.
- **When NOT to use:** Simple web-only applications where Pusher or Ably is cheaper and simpler. Cost-sensitive projects — PubNub's per-transaction pricing is expensive for high-frequency messaging.
- **Strengths:** 175+ PoPs globally; offline message storage and playback; push notification delivery (APNS, FCM) alongside in-app; presence; IoT SDK ecosystem including embedded C SDKs; Functions (serverless transforms on messages); very long message history retention options.
- **Weaknesses:** Per-transaction pricing model becomes very expensive for high-frequency data; older API design compared to Ably; documentation quality inconsistent; some SDKs are less maintained than others.
- **Team fit:** Teams with a global user base or IoT device fleet; mobile app teams that want one SDK for in-app realtime and push notifications.
- **Scale fit:** Designed for global-scale IoT and consumer apps; billions of messages per day on the platform.
- **Production risks:** Per-transaction cost spike from noisy devices or runaway clients. Message size limits (32KB). PubNub Functions cold-start latency if using serverless transforms.

---

## MQTT

- **When to use:** IoT and embedded systems where bandwidth and battery are constrained. MQTT is the standard protocol for device-to-cloud telemetry and command delivery. Use with a broker: Mosquitto (self-hosted), AWS IoT Core, HiveMQ, EMQX.
- **When NOT to use:** Browser-based applications (MQTT over plain TCP doesn't work in browsers — use MQTT over WebSocket, which is supported but adds overhead); applications with complex routing logic better suited to HTTP or WebSocket.
- **Strengths:** Tiny overhead (2-byte fixed header); QoS levels 0/1/2 for at-most-once, at-least-once, exactly-once delivery; retain messages (last known value for a topic); will messages (device disconnect notification); topic-based pub/sub with wildcard subscriptions; runs on microcontrollers (ESP32, Arduino).
- **Weaknesses:** No request/response pattern (must implement with reply topics); brokers need high-availability setup; security requires TLS + auth configuration (plain MQTT has no auth by default); not suitable for browser apps without WebSocket transport; topic design is an art — poor design causes operational pain.
- **Team fit:** Embedded/firmware engineers; IoT platform teams; backend engineers with messaging system experience.
- **Scale fit:** EMQX and HiveMQ handle 100M+ concurrent MQTT connections in cluster mode; AWS IoT Core scales infinitely (managed).
- **Production risks:** QoS 2 (exactly-once) has significant overhead — most IoT use cases use QoS 1 with idempotent consumers. Broker single point of failure without clustering. Topic namespace collisions in multi-tenant deployments.

---

## Yjs (CRDT)

- **When to use:** Real-time collaborative document editing where multiple users edit simultaneously and changes must merge without conflicts — collaborative text editors, whiteboards, spreadsheets, code editors. The leading JavaScript CRDT library; used by many editor frameworks (TipTap, Quill, CodeMirror, ProseMirror).
- **When NOT to use:** Simple notification or live-refresh use cases — CRDTs are significant complexity overhead for problems that pub/sub solves. Non-document data structures where conflict-free merging isn't needed.
- **Strengths:** Conflict-free merge of concurrent edits from any number of clients; works offline (edits accumulate locally and sync when reconnected); multiple network providers (y-websocket, y-webrtc, Liveblocks, PartyKit); supports shared types: Text, Array, Map, XmlFragment; small update diffs (only changed operations transmitted); awareness protocol for cursor/presence sharing.
- **Weaknesses:** Learning curve for CRDT mental model; persistence requires storing the full CRDT document (not just the latest state); document size grows with history (use snapshots + garbage collection); debugging concurrent merge issues is hard; server-side modification of a Yjs document requires the `yjs` npm package on the server.
- **Team fit:** Frontend engineers building editor or whiteboard features; teams with at least one engineer willing to own the CRDT persistence and sync layer.
- **Scale fit:** Scales per-document; y-websocket server is simple to horizontally scale with Redis persistence; for managed scale, use Liveblocks or PartyKit.
- **Production risks:** Document history growing unbounded without snapshot + GC strategy. y-websocket server losing in-memory state on restart without persistence. Forgetting to destroy `Y.Doc` instances causing memory leaks in server-side rendering.

---

## Automerge (CRDT)

- **When to use:** Alternative to Yjs when you need a Rust/WASM implementation with better performance for large documents, or when building non-JavaScript backends (Rust, Python via automerge-py). Also consider for structured data (JSON-like) rather than text-first collaboration.
- **When NOT to use:** Browser-only apps where Yjs has a more mature ecosystem of editor integrations and network providers. Small teams new to CRDTs — Yjs has more learning resources.
- **Strengths:** Rust core with WASM bindings (better performance than pure-JS Yjs for large documents); supports arbitrary JSON-like structures; excellent for local-first architectures; strong typing in TypeScript bindings; smaller wire format than Yjs for some workloads.
- **Weaknesses:** Smaller ecosystem than Yjs; fewer ready-made editor integrations; fewer managed sync providers; less mature network provider ecosystem; community is smaller.
- **Team fit:** Teams comfortable with Rust toolchains; projects needing high-performance CRDT processing; local-first architecture advocates.
- **Scale fit:** Same as Yjs — scales per-document with a sync server.
- **Production risks:** WASM bundle size adds to initial page load; fewer battle-tested production deployments than Yjs.

---

## Comparison Table

| Option | Direction | Managed | Self-host | Latency | Best for | Complexity |
|---|---|---|---|---|---|---|
| WebSocket | Bidirectional | No (DIY) | Yes | <10ms | Chat, games, dashboards | Medium |
| SSE | Server→Client | No (DIY) | Yes | <50ms | Feeds, LLM streams, notifications | Low |
| WebRTC | Peer-to-peer | Signaling needed | Yes | <100ms | Audio/video, P2P data | High |
| Pusher | Bidirectional | Yes | No | ~50ms | Prototyping, light use | Low |
| Ably | Bidirectional | Yes | No | <65ms | Production pub/sub at scale | Medium |
| Supabase Realtime | Bidirectional | Yes (Supabase) | Yes | 50–200ms | Postgres CDC, Supabase apps | Low |
| PubNub | Bidirectional | Yes | No | <100ms (global) | IoT, global push, mobile | Medium |
| MQTT | Bidirectional | Broker needed | Yes | <10ms | IoT, embedded, telemetry | Medium |
| Yjs (CRDT) | Bidirectional | Via provider | Yes | Sync-on-change | Collaborative editing | High |
| Automerge (CRDT) | Bidirectional | Via provider | Yes | Sync-on-change | Local-first, structured data | High |

---

## Recommended Combinations

- **Notifications + live dashboard (web app):** SSE for server→client push; plain HTTP POST for client→server actions — no WebSocket complexity needed.
- **Chat / multiplayer game:** WebSocket + Redis Pub/Sub for horizontal fan-out — `ws` library (Node) or Gorilla (Go); Redis channels bridge server instances.
- **Collaborative text editor:** Yjs + y-websocket server + PostgreSQL (store Yjs binary updates) — or replace y-websocket with Liveblocks/PartyKit for managed sync.
- **Video conferencing:** LiveKit (open-source SFU built on WebRTC) — handles signaling, TURN, and media routing; deploy on a single server or LiveKit Cloud.
- **IoT telemetry platform:** MQTT (EMQX cluster or AWS IoT Core) → message broker (Kafka or AWS Kinesis) → processing pipeline → WebSocket or SSE for browser dashboards.
- **Supabase-backed app with live data:** Supabase Realtime (CDC) for database-driven UI updates + Supabase broadcast for ephemeral events (typing indicators, cursor positions).
- **Global mobile app with push:** PubNub — single SDK handles in-app realtime and APNS/FCM push notification fallback when app is backgrounded.
- **Prototype → production managed:** Start with Pusher; migrate to Ably or self-hosted WebSocket once you hit Pusher's cost/feature ceiling — keep provider abstracted behind a `RealtimeService` interface.

Cross-reference: `.claude/stack-matrix/backend.md` for the application server that hosts WebSocket connections, `.claude/checklists/security.md` for authentication on WebSocket upgrade requests and MQTT broker access control.

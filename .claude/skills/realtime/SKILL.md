---
name: realtime
description: >
  Activate for any real-time, live-update, or push-notification design task.
  Triggers: WebSocket, SSE (Server-Sent Events), WebRTC, long polling, presence,
  live cursors, chat, notifications, collaborative editing, live dashboards,
  Ably, Pusher, Supabase Realtime, Socket.IO, GraphQL subscriptions, signaling server,
  pub/sub fan-out, backpressure in streaming, reconnection strategy.
---

# Realtime Communication

## When to use
- Push events from server to clients without polling (live feeds, notifications)
- Bidirectional communication (chat, collaborative tools, multiplayer)
- Presence tracking (who is online, typing indicators, live cursors)
- Live dashboards with sub-second data refresh
- Peer-to-peer media (WebRTC audio/video, data channels)
- Scaling a WebSocket server beyond a single process
- Choosing between WebSocket, SSE, and managed services

## Workflow

1. **Classify communication pattern** — Unidirectional server-to-client (SSE), bidirectional (WebSocket), peer-to-peer media (WebRTC), or all three?
2. **Select transport** — Use decision matrix in Standards.
3. **Design channel/room model** — Namespace → room → subscriber. Define channel naming convention (`{entity}:{id}`, e.g. `document:abc123`).
4. **Design message envelope** — `{ event, data, id, timestamp }`. Unique `id` per event enables client-side deduplication and `Last-Event-ID` replay (SSE).
5. **Implement server** — Choose framework/platform. Implement auth middleware (validate JWT before upgrading connection). Emit events to channel on DB/queue change.
6. **Implement client** — Reconnection with exponential backoff (base 1 s, max 30 s, jitter ±20%). Heartbeat/ping-pong detection (detect silent drops). Reconcile missed events on reconnect using last received event ID or cursor.
7. **Presence** — Server maintains ephemeral presence store (Redis SETEX with TTL; refresh on heartbeat). Broadcast enter/leave diffs, not full roster, to avoid fan-out storms at scale.
8. **Scale horizontally** — WebSocket servers are stateful. Use Redis Pub/Sub (or Redis Streams) as message bus between nodes. Or use managed service to offload fan-out.
9. **Backpressure** — Per-connection send buffer limit. Slow client detection: if buffer exceeds threshold, drop or disconnect; log and alert. Never block event loop waiting for slow client.
10. **Observability** — Track: connected clients (gauge), messages sent/received (counters), connection duration histogram, reconnect rate, per-room subscriber count. Alert on reconnect rate spike (network instability) or message queue depth.
11. **Security** — Auth on upgrade (not on first message). Rate-limit per connection (token bucket). Validate channel names server-side before allowing subscription. Sanitize all inbound data. TLS/WSS mandatory.
12. **Test** — Unit-test event handlers with mock socket. Load-test with `k6` WebSocket API (`k6/ws`) or `artillery` (`@artillery/plugin-expect`). Chaos: abrupt disconnect, slow consumer, duplicate delivery.

## Standards

### Transport decision matrix

| Pattern | Best choice | Avoid |
|---|---|---|
| Server → client one-way (feeds, notifications) | **SSE** (native browser EventSource, automatic reconnect) | WebSocket (bidirectional overhead) |
| Bidirectional, low-latency (<100 ms) | **WebSocket** (RFC 6455) | SSE, long-polling |
| Bidirectional, batteries-included | **Socket.IO 4.x** (WS + HTTP fallback + rooms) | Raw WS when rooms/namespaces needed |
| Peer-to-peer media (audio/video/data) | **WebRTC** + signaling server | WebSocket (too high latency for media) |
| Fully managed, global edge, presence built-in | **Ably** or **Pusher Channels** | Self-hosted at early stage |
| Postgres-native, Supabase project | **Supabase Realtime** (Phoenix Channels) | External broker |
| GraphQL API | **GraphQL subscriptions** over WS (`graphql-ws` library) | Polling |
| Mobile push (not in-app) | **FCM** / **APNs** via server-side SDK | WebSocket (background-killed) |

Examples shown in JS/Node; the same patterns apply across platforms — equivalents (mobile, Go, Python, etc.) follow the Standards table.

### WebSocket server (Node.js, `ws` library v8+)
```typescript
import { WebSocketServer, WebSocket } from 'ws';
import { createClient } from 'redis';

const wss = new WebSocketServer({ port: 8080 });
const pub = createClient(); // publish
const sub = pub.duplicate();  // subscribe

await sub.connect();
await pub.connect();

// Subscribe to Redis channel for fan-out across nodes
await sub.subscribe('events', (message) => {
  const payload = JSON.parse(message);
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN && client.room === payload.room) {
      client.send(message);
    }
  });
});

wss.on('connection', (ws, req) => {
  const token = authenticate(req); // validate JWT; close if invalid
  if (!token) { ws.close(1008, 'Unauthorized'); return; }

  ws.isAlive = true;
  ws.on('pong', () => { ws.isAlive = true; });
  ws.on('message', (raw) => handleMessage(ws, raw));
});

// Heartbeat every 30s — detect silent disconnects
const hb = setInterval(() => {
  wss.clients.forEach((ws) => {
    if (!ws.isAlive) { ws.terminate(); return; }
    ws.isAlive = false;
    ws.ping();
  });
}, 30_000);
wss.on('close', () => clearInterval(hb));
```

### SSE (Server-Sent Events)
```typescript
// Express SSE endpoint
app.get('/events', (req, res) => {
  const token = verifyBearer(req.headers.authorization);
  if (!token) { res.status(401).end(); return; }

  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('X-Accel-Buffering', 'no'); // disable nginx buffering
  res.flushHeaders();

  const lastId = req.headers['last-event-id'];
  // Replay missed events since lastId from DB/cache here

  const sendEvent = (data: object, id: string) =>
    res.write(`id: ${id}\ndata: ${JSON.stringify(data)}\n\n`);

  const unsub = emitter.on('event', sendEvent);
  req.on('close', () => unsub());
});
```
- Client-side: native `EventSource` auto-reconnects using `Last-Event-ID`.
- SSE is HTTP/1.1; browser limit of 6 connections per domain — use HTTP/2 to remove limit.
- SSE does NOT work with HTTP/1.1 behind proxies that buffer responses; set `X-Accel-Buffering: no`.

### Socket.IO 4.x patterns
- Use namespaces for top-level separation (e.g. `/chat`, `/notifications`).
- Use rooms within a namespace for per-entity channels.
- Adapter: `@socket.io/redis-adapter` for multi-node with Redis Pub/Sub.
- Sticky sessions required only when using HTTP long-polling fallback (set `transport: ['websocket']` to skip).
- `socket.io-msgpack-parser` for binary efficiency on high-throughput channels.

### Managed services

**Ably**
- Channels: `ably.channels.get('room:id')` — attach, publish, subscribe.
- Presence: `channel.presence.enter(clientData)`, `channel.presence.get()`.
- History: `channel.history({ limit: 100 })` for catch-up on reconnect.
- Push notifications: Ably Push (FCM/APNs gateway) from same API.

**Pusher Channels**
- Public / private (requires auth endpoint) / presence (auth + member data).
- Server SDK: `pusher.trigger('channel', 'event', data)`.
- Client: `pusher.subscribe('channel').bind('event', handler)`.
- Limit: 100 concurrent connections on free tier; 10k on paid.

**Supabase Realtime**
```typescript
const channel = supabase
  .channel('room:abc')
  .on('postgres_changes', { event: '*', schema: 'public', table: 'messages' },
      (payload) => console.log(payload))
  .on('presence', { event: 'sync' }, () => {
    const state = channel.presenceState();
  })
  .subscribe();
```
- Postgres Changes: row-level CDC pushed to clients (filter by `filter: 'room_id=eq.abc'`).
- Row-Level Security must be enabled; Realtime respects RLS policies.
- Presence uses in-memory CRDT; not persisted across restarts.

### Presence design
- **Ephemeral store**: Redis `HSET presence:{room} {userId} {json}` + `EXPIRE` TTL (30–60 s).
- **Heartbeat**: client sends ping every 15 s; server resets TTL on receive.
- **Fan-out events**: `presence.join` / `presence.leave` diffs only — never broadcast full roster on every heartbeat.
- **Large rooms** (>10k members): do not track individual presence; use counters instead.

### WebRTC signaling
- Signaling (SDP offer/answer + ICE candidates) via WebSocket or Ably/Pusher.
- STUN: use Google's `stun:stun.l.google.com:19302` for dev; deploy own STUN for prod (coturn).
- TURN: mandatory for corporate firewalls; deploy coturn or use Twilio TURN (BYOC pricing).
- ICE restart: handle `iceConnectionState === 'failed'` with `restartIce()`.

### Client reconnection pattern
```typescript
function connect(url: string, backoff = 1000) {
  const ws = new WebSocket(url);
  ws.addEventListener('open', () => { backoff = 1000; });
  ws.addEventListener('close', () => {
    const jitter = Math.random() * 0.4 * backoff;
    setTimeout(() => connect(url, Math.min(backoff * 2, 30_000)), backoff + jitter);
  });
  ws.addEventListener('message', handleMessage);
  return ws;
}
```
- On reconnect, send `{ lastEventId }` in first message or as query param to get missed events.
- Never reconnect faster than 1 s to avoid thundering herd.

### Scaling fan-out
| Subscribers | Architecture |
|---|---|
| <1 000 | Single process; in-memory event emitter |
| 1 000–100 000 | Multiple WS nodes + Redis Pub/Sub adapter |
| >100 000 | Managed service (Ably / Pusher / Fanout.io) or custom Elixir/Phoenix (Phoenix PubSub scales to millions) |

- Redis Pub/Sub delivers to all nodes; each node filters to connected clients.
- For very high fan-out (same event → millions): use Kafka + dedicated push service tier.

## Common mistakes to avoid

- **No heartbeat** — TCP connections silently drop through NAT/proxies; without ping-pong, zombie connections accumulate and events are lost.
- **Reconnecting immediately without backoff** — thundering herd crushes server on restart.
- **Broadcasting full presence roster on every heartbeat** — O(n²) fan-out; at 1k users this becomes 1M messages/heartbeat.
- **No auth on WebSocket upgrade** — only token in URL query param (logged in access logs); use `Authorization` header in upgrade HTTP request or first message validation.
- **Buffering response in nginx** — SSE and WebSocket streams are broken by default proxy buffering; always set `proxy_buffering off` and `proxy_read_timeout 3600s`.
- **Single WebSocket server without Redis adapter** — scale-out fails; messages from Node A never reach clients connected to Node B.
- **Sending JSON as string inside JSON** — double-serialization; always send `JSON.stringify(payload)` directly.
- **Not handling `ws.readyState` before send** — crashes on `CLOSING`/`CLOSED` socket.
- **Storing ephemeral presence in primary DB** — high write amplification; use Redis with TTL.

## Output format

Produce artifacts in `docs/realtime/` using `.claude/templates/architecture.md` adapted for realtime:
- `transport-decision.md` — chosen transport(s) with rationale
- `channel-schema.md` — channel naming, event taxonomy, message envelope spec
- `presence-design.md` — presence store, heartbeat interval, fan-out strategy
- `scaling-plan.md` — concurrent connection estimate, Redis adapter or managed service config
- Code snippets (server + client) inline as fenced code blocks matching project language

## Related checklists
- `.claude/checklists/architecture.md`
- `.claude/checklists/performance.md`
- `.claude/checklists/security.md`
- `.claude/checklists/backend.md`

## Related agents
- `.claude/agents/engineering/realtime-engineer.md`
- `.claude/agents/engineering/backend-engineer.md`
- `.claude/agents/engineering/frontend-engineer.md`
- `.claude/agents/engineering/mobile-engineer.md`
- `.claude/agents/quality/performance-engineer.md`
- `.claude/agents/quality/reliability-engineer.md`
- `.claude/agents/core/solution-architect.md`

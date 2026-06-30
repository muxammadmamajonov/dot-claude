---
name: messaging-queues
description: >
  Activate for any async messaging, event-driven architecture, or queue design task.
  Triggers: Kafka, RabbitMQ, SQS, SNS, NATS, Google Pub/Sub, Azure Service Bus,
  outbox pattern, DLQ, consumer groups, delivery semantics, backpressure, idempotency,
  message ordering, event sourcing setup, broker selection.
---

# Async Messaging & Queues

## When to use
- Decoupling producers from consumers across service boundaries
- Guaranteeing at-least-once or exactly-once delivery
- Fan-out to multiple consumers (pub/sub)
- Rate-limiting downstream services (backpressure)
- Durable event log / event sourcing (Kafka)
- Job queues for background processing (SQS, RabbitMQ)
- Ordered processing of domain events

## Workflow

1. **Clarify delivery contract** — Ask: ordered or unordered? at-least-once or exactly-once? max latency? consumer count? message size p99? retention needed?
2. **Select broker** — Use the decision matrix in Standards below.
3. **Design topic/queue schema** — Name conventions, partition count (Kafka), routing keys (RabbitMQ), FIFO vs standard (SQS).
4. **Define message envelope** — Header fields (event-type, correlation-id, causation-id, schema-version, produced-at ISO-8601). Payload in JSON or Avro/Protobuf.
5. **Implement producer** — Transactional outbox if DB write + publish must be atomic. Otherwise wrap in try/catch with structured logging of failure.
6. **Implement consumer** — Idempotency key stored in DB or Redis before processing. Ack only after successful processing + side-effects committed.
7. **Configure DLQ** — Dead-letter after N retries (3–5). Alert on DLQ depth > 0. DLQ messages must retain original headers + failure reason.
8. **Backpressure** — Consumer-side: bounded prefetch/max in-flight (RabbitMQ `prefetch_count`, Kafka `max.poll.records`). Producer-side: circuit breaker or local queue with shed policy.
9. **Schema evolution** — Backward/forward-compatible changes only (add optional fields, never remove or rename). Register schemas in Confluent Schema Registry or AWS Glue Schema Registry.
10. **Observability** — Emit consumer lag, processing latency, error rate, DLQ depth. Kafka: use `kafka_consumer_group_lag` via JMX/MSK metrics. SQS: `ApproximateNumberOfMessagesNotVisible`, `ApproximateAgeOfOldestMessage`.
11. **Security** — mTLS or SASL/SCRAM for Kafka. IAM policies scoping producer/consumer per topic for SQS/SNS. Encryption at rest (KMS). No secrets in message payloads.
12. **Test** — Unit-test handlers with in-memory stub. Integration-test with Testcontainers (kafka container `confluentinc/cp-kafka:7.x`, localstack for SQS). Chaos: kill broker mid-test, assert idempotent re-delivery.

## Standards

### Broker selection matrix

| Requirement | Best choice | Avoid |
|---|---|---|
| Durable ordered log, replay, high throughput (>50k msg/s) | **Kafka** (MSK or self-hosted) | RabbitMQ (no log replay) |
| Simple job queue, SaaS, no ops overhead | **SQS Standard** or **SQS FIFO** | Kafka (overkill) |
| Complex routing (topic exchanges, fanout, per-message TTL) | **RabbitMQ** | SQS |
| Sub-millisecond latency, request-reply, lightweight IoT | **NATS JetStream** | Kafka |
| GCP-native | **Cloud Pub/Sub** | — |
| Azure-native | **Azure Service Bus** (queues/topics) or **Event Hubs** (Kafka-compat) | — |
| Exactly-once without outbox | **Kafka transactions** (`transactional.id`) | SQS (no exactly-once) |

### Kafka specifics (versions 3.x)
- Partition count: start at `max_consumers_expected × 2`, never decrease.
- Replication factor: 3 in prod, `min.insync.replicas=2`.
- Producer: `acks=all`, `enable.idempotence=true`, `compression.type=lz4`.
- Consumer: `enable.auto.commit=false`; commit only after processing + downstream acks.
- Exactly-once: `isolation.level=read_committed`, use Kafka Streams or explicit transactions.
- Retention: set per topic (`retention.ms`, `retention.bytes`); default 7 days for audit topics.
- Monitoring: Cruise Control for rebalancing; Kafka UI or Redpanda Console for dev.

### SQS specifics
- Standard queue for throughput; FIFO queue (300 TPS, or 3000 with batching) for ordering.
- `VisibilityTimeout` ≥ 6× max processing time to prevent double-delivery.
- `ReceiveMessageWaitTimeSeconds=20` (long polling) to cut cost.
- Batch receive (`MaxNumberOfMessages=10`) in consumers.
- DLQ: set `maxReceiveCount=3`; redrive policy referencing DLQ ARN.
- Large messages (>256 KB): use SQS Extended Client Library with S3.

### RabbitMQ specifics (versions 3.12+)
- Use quorum queues (not classic mirrored) for HA.
- `prefetch_count` per channel, not per connection.
- Publisher confirms: `channel.confirm_select()` + wait for ack before returning success to caller.
- Dead-lettering: set `x-dead-letter-exchange` + `x-dead-letter-routing-key` on queue declaration.
- Use stream queues (3.9+) for log-like replay semantics.

### Outbox pattern (transactional outbox)
Use when: producer must atomically write to DB and enqueue a message.
1. Write domain record + outbox record in same DB transaction.
2. Polling relay (or Debezium CDC) reads outbox table, publishes to broker, marks sent.
3. Consumer deduplicates via `message_id` in processed-events table (upsert on conflict do nothing).
- Debezium connectors: `debezium/debezium-connector-postgres:2.x` for Postgres → Kafka.
- Polling relay: query `WHERE published_at IS NULL ORDER BY created_at LIMIT 100` every 500 ms.

### Idempotency
- Every consumer maintains an `idempotency_key → processed_at` store (Postgres unique index or Redis SET NX with TTL).
- Key = `message_id` from broker header (UUID v4 set by producer). Never use payload fields as key.
- Window: keep keys for `max(retention_period, visibility_timeout × max_retries)`.

### Ordering guarantees
- Kafka: order guaranteed within partition; use message key = aggregate ID.
- SQS FIFO: order within `MessageGroupId`; set group = aggregate ID.
- RabbitMQ: single consumer per queue for strict order (no competing consumers).
- Never assume cross-partition/cross-queue ordering.

## Common mistakes to avoid

- **Auto-commit before processing** — loses messages on consumer crash; always commit after.
- **No DLQ** — poison messages block the queue forever.
- **Visibility timeout too short** (SQS) — causes duplicate delivery under load.
- **Single partition** (Kafka) — no parallelism; impossible to scale later without disruption.
- **Putting secrets in message body** — messages are often logged; use references instead.
- **Synchronous HTTP in consumer** — creates tight coupling; use async or circuit breaker.
- **Ignoring consumer lag** — queue depth spike is the earliest signal of a downstream incident.
- **Breaking schema changes** — removing/renaming fields breaks consumers silently; use schema registry + compatibility checks in CI.
- **Unbounded retries without backoff** — cascades into broker saturation; use exponential backoff with jitter (base 100 ms, max 30 s).

## Output format

Produce artifacts in `docs/architecture/messaging/` using template `.claude/templates/architecture.md` adapted for the messaging context:
- `broker-decision.md` — rationale for broker choice
- `topic-schema.md` — topic/queue names, partition counts, retention, routing keys
- `message-envelope.md` — field definitions with types and required/optional
- `consumer-playbook.md` — idempotency strategy, DLQ handling, retry policy, observability
- Code scaffolds (producer + consumer) inline in the message-envelope doc as code blocks

## Related checklists
- `.claude/checklists/architecture.md`
- `.claude/checklists/security.md`
- `.claude/checklists/observability.md`
- `.claude/checklists/backend.md`

## Related agents
- `.claude/agents/engineering/backend-engineer.md`
- `.claude/agents/engineering/data-engineer.md`
- `.claude/agents/engineering/realtime-engineer.md`
- `.claude/agents/engineering/integration-engineer.md`
- `.claude/agents/quality/reliability-engineer.md`
- `.claude/agents/core/solution-architect.md`

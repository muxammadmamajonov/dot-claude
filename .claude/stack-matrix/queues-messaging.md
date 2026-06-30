# Queues & Messaging Stack Matrix

Choose based on three axes: **delivery guarantees** (at-most-once vs. at-least-once vs. exactly-once), **throughput/ordering** requirements, and **operational complexity** your team can absorb. A startup with no Kafka ops expertise should not run Kafka; a fintech with strict ordering and replay needs probably should.

Key drivers: message volume, ordering requirements, fan-out topology, replay/audit needs, managed vs. self-hosted preference, vendor lock-in tolerance.

---

## Kafka

**When to use**
- High-throughput event streaming (>100 k msg/s per topic realistic)
- Log compaction, durable replay, rewind-to-offset use cases (audit trails, event sourcing)
- Multiple independent consumer groups reading the same stream at different offsets
- Real-time analytics pipelines and CDC (Change Data Capture) from databases

**When NOT to use**
- Simple task queues with low volume — massive operational overhead for modest needs
- Teams with no Kafka/JVM/ZooKeeper (or KRaft) expertise
- Sub-5-second latency spikes are unacceptable without careful tuning
- Need native request-reply or per-message TTL without custom wrappers

**Strengths**
- Immutable, partitioned, replicated log — messages persist after consumption; replayable
- Horizontal scale: add partitions/brokers without downtime
- Rich ecosystem: Kafka Streams, ksqlDB, Kafka Connect (300+ connectors), Schema Registry
- Exactly-once semantics available with idempotent producers + transactional API

**Weaknesses**
- Operational complexity: ZooKeeper (legacy) or KRaft, broker sizing, partition rebalancing
- No native priority queues; ordering guaranteed only within a partition
- Small-message overhead — efficient at >1 KB payloads; tiny messages waste bandwidth
- Managed options (Confluent Cloud, MSK) add cost quickly at scale

**Team fit**
- Platform/data engineering teams; companies with dedicated infra engineers
- Poor fit for product teams that just need a background job queue

**Scale fit**
- Proven at petabyte-scale (LinkedIn, Uber). Overkill for <10 k msg/s unless replay matters.

**Risks**
- Under-provisioned disk fills fast; consumer lag causes silent data loss if retention expires
- KRaft migration from ZooKeeper has edge cases in older Kafka versions

---

## RabbitMQ

**When to use**
- Complex routing: topic exchanges, fanout, direct, headers-based routing in one system
- Task queues with worker pools, priority queues, dead-letter queues (DLQ)
- RPC / request-reply patterns
- Moderate throughput (<50 k msg/s) with flexible routing logic

**When NOT to use**
- Need long-term message replay/audit — RabbitMQ deletes messages after acknowledgment
- Very high throughput without clustering expertise
- Need Kafka-style consumer groups reading at independent offsets

**Strengths**
- Rich routing via exchanges (topic, fanout, direct, headers)
- Per-message TTL, priority queues, DLQ native
- Mature: 15+ years, battle-tested AMQP 0-9-1 and newer AMQP 1.0
- Good management UI; easy local dev with Docker

**Weaknesses**
- Messages deleted post-consumption — no replay
- Cluster setup (mirrored queues → quorum queues) adds operational burden
- Throughput tops out earlier than Kafka under sustained load
- Not ideal for event-driven architectures needing fan-out to many consumers simultaneously

**Team fit**
- Backend teams comfortable with AMQP; microservices routing scenarios
- Language-agnostic: excellent client libraries for Python, Ruby, .NET, Java, Go

**Scale fit**
- Sweet spot: 1 k–50 k msg/s. Scales with sharding plugins and quorum queues but less elegantly than Kafka.

**Risks**
- Classic mirrored queues deprecated; migrate to quorum queues for HA
- Memory pressure can crash brokers if consumers fall behind without flow control

---

## AWS SQS / SNS

**When to use**
- AWS-native workloads; want fully managed with zero broker ops
- Simple fan-out: SNS topic → multiple SQS queues (pub/sub + worker pool)
- Lambda triggers, ECS task consumers — tight AWS integration
- Standard queues (at-least-once) or FIFO queues (exactly-once, 3 k msg/s)

**When NOT to use**
- Need message replay after consumption
- Multi-cloud or on-prem — SQS/SNS is AWS-only
- FIFO throughput cap (3 k msg/s with batching, 300 without) is a bottleneck
- Need complex routing logic beyond SNS filter policies

**Strengths**
- Zero ops: no brokers, scaling, or patching
- Near-infinite scale for Standard queues; cost-effective at low-to-mid volume
- Deep AWS integrations: Lambda, EventBridge, Step Functions, S3 notifications
- SNS fan-out to HTTP/S, email, SMS, Lambda, SQS simultaneously

**Weaknesses**
- Standard queues: at-least-once delivery, occasional out-of-order — idempotency required
- FIFO: strict 300/3 k msg/s limits; can be a hard ceiling
- No replay, no consumer groups at independent offsets
- Long-polling adds latency; visibility timeout misconfigurations cause duplicate processing

**Team fit**
- Any team already on AWS; great default for task queues and event fan-out
- Minimal learning curve; Terraform/CDK support excellent

**Scale fit**
- Standard: effectively unlimited. FIFO: 3 k msg/s hard cap without sharding.

**Risks**
- Vendor lock-in; migrating off SQS is non-trivial
- Hidden costs: number of requests (not just messages); large payloads need S3 pointer pattern

---

## Google Pub/Sub

**When to use**
- GCP-native workloads; managed streaming at scale
- Global fan-out with push (HTTP webhook) or pull subscribers
- Bigquery subscriptions, Dataflow integration for stream processing
- Need dead-letter topics and ordering keys natively

**When NOT to use**
- AWS/Azure shops — cross-cloud latency and operational complexity
- Need Kafka-level replay (Pub/Sub message retention max 31 days, not a log)
- Sub-10 ms latency requirements

**Strengths**
- Fully managed; auto-scales to millions of msg/s
- At-least-once with ordering keys for per-key ordering guarantees
- Native BigQuery subscriptions, Dataflow templates, Cloud Functions triggers
- Global topic: publishers and subscribers in any region without separate clusters

**Weaknesses**
- At-least-once only; exactly-once requires deduplication on consumer side
- Pricing per message volume can exceed Kafka self-hosted at very high throughput
- Less flexible routing than RabbitMQ or Kafka consumer group patterns

**Team fit**
- GCP data engineering teams; organizations using Dataflow, BigQuery, GKE

**Scale fit**
- Handles millions of msg/s globally; excellent for bursty unpredictable loads

**Risks**
- GCP lock-in; message ordering only guaranteed per ordering key, not globally
- Retention limit (31 days) means not a true event log

---

## NATS

**When to use**
- Ultra-low latency (<1 ms) messaging; IoT, gaming, edge computing
- Lightweight microservice communication replacing gRPC for fire-and-forget
- JetStream (NATS persistence layer) for durable pub/sub, KV store, object store in one
- Multi-cloud or on-prem with minimal footprint (single binary, 20 MB binary)

**When NOT to use**
- Need Kafka-level replay across very long retention windows at petabyte scale
- Team unfamiliar with NATS subject hierarchy and wildcard subscription model
- Enterprise support SLA requirements without commercial vendor backing

**Strengths**
- Extreme performance: 10–20 M msg/s on modest hardware
- JetStream adds persistence, consumer acks, exactly-once delivery
- Simple deployment: single Go binary; cluster with leaf nodes for geo-distribution
- Subject-based addressing with wildcards (foo.> , foo.*) — flexible routing

**Weaknesses**
- JetStream persistence less battle-tested at Kafka scale
- Smaller ecosystem than Kafka/RabbitMQ; fewer connectors
- At-most-once delivery in core NATS (no persistence); JetStream required for durability

**Team fit**
- Platform teams building high-performance microservices or IoT backends
- Go, Rust, C shops where binary footprint and latency matter

**Scale fit**
- Core NATS: extreme throughput; JetStream: up to hundreds of millions of messages/day comfortably

**Risks**
- JetStream cluster split-brain scenarios require careful Raft quorum sizing
- Community smaller than Kafka; fewer enterprise patterns documented

---

## Redis Streams

**When to use**
- Already running Redis; need a simple durable queue without adding a new system
- Consumer groups with ack semantics layered on top of Redis
- Low-to-medium throughput (<1 M msg/s) with sub-millisecond latency
- Ephemeral task queues where replay matters for recent messages only

**When NOT to use**
- Long-term message retention — Redis memory cost makes multi-day/multi-week retention expensive
- Kafka-scale throughput or multi-TB event logs
- Need Kafka-style topic partitioning across brokers

**Strengths**
- Zero additional infrastructure if Redis is already present
- Consumer groups, XACK, XPENDING — proper at-least-once semantics
- Very low latency; XADD O(1) append
- Trim policies (MAXLEN) keep memory bounded

**Weaknesses**
- Memory-backed: retaining large volumes of messages is costly
- No built-in topic partitioning across nodes (can shard keys but manual)
- Cluster mode complicates multi-shard stream consumption
- No schema registry or ecosystem comparable to Kafka

**Team fit**
- Teams already invested in Redis (caching, sessions) who need light queuing
- Python/Node shops using Bull, Celery, or Sidekiq patterns wanting Redis consistency

**Scale fit**
- Up to ~500 k msg/s; beyond that, dedicated broker (Kafka/NATS) recommended

**Risks**
- AOF/RDB persistence configuration mistakes risk data loss on restart
- MAXLEN trimming silently drops old messages if consumers fall behind

---

## Azure Service Bus

**When to use**
- Azure-native workloads; enterprise messaging with sessions, transactions, DLQ
- Message sessions for per-entity ordered delivery (e.g., per-customer order processing)
- Hybrid on-prem/cloud via Azure Relay
- .NET / Microsoft ecosystem shops

**When NOT to use**
- Non-Azure cloud; significant migration overhead
- Need Kafka-scale throughput — Service Bus Premium tops ~1 M msg/s with careful partitioning
- Need long-term event log replay

**Strengths**
- Fully managed; geo-disaster recovery, geo-replication built in
- Sessions: per-session FIFO guarantees (strong ordering for stateful workflows)
- Dead-letter queues, message deferral, scheduled messages, duplicate detection native
- AMQP 1.0 support; integrates with Logic Apps, Azure Functions, Event Grid

**Weaknesses**
- Azure lock-in; AMQP client required (no lightweight HTTP polling like SQS)
- Premium tier required for >256 KB messages and VNet integration — cost jumps
- Not a streaming log; messages deleted after consumption

**Team fit**
- .NET/Azure enterprise teams; organizations using Azure Logic Apps, Durable Functions
- SAP, Dynamics, BizTalk integration scenarios

**Scale fit**
- Standard: modest loads. Premium: up to 1 M msg/s with partitioned entities.

**Risks**
- Namespace-level quota limits can surprise at scale; plan capacity in advance
- Pricing model (operations + storage) obscures cost at high message rates

---

## Comparison Table

| Criterion | Kafka | RabbitMQ | AWS SQS/SNS | Google Pub/Sub | NATS | Redis Streams | Azure Service Bus |
|---|---|---|---|---|---|---|---|
| **Delivery guarantee** | Exactly-once (configured) | At-least-once | At-least-once (Standard) / EO (FIFO) | At-least-once | At-most-once (core) / At-least-once (JetStream) | At-least-once | At-least-once |
| **Message replay** | Yes (configurable retention) | No | No | Limited (31 days) | Yes (JetStream) | Limited (memory-bounded) | No |
| **Max throughput** | Millions/s | ~50 k/s | Unlimited (Standard) / 3 k/s (FIFO) | Millions/s | 10–20 M/s (core) | ~500 k/s | ~1 M/s (Premium) |
| **Latency** | Low (ms) | Very low (ms) | Low-medium (ms–s) | Low (ms) | Ultra-low (<1 ms) | Ultra-low (<1 ms) | Low (ms) |
| **Ops complexity** | High | Medium | None (managed) | None (managed) | Low | Low (if Redis exists) | None (managed) |
| **Routing flexibility** | Medium (partition key) | High (exchanges) | Low (SNS filters) | Low (filter attrs) | High (subject wildcards) | Low | High (sessions, rules) |
| **Ordering** | Per-partition | Per-queue | FIFO queues | Per ordering-key | Per-subject (JetStream) | Per-stream | Per-session |
| **Cloud lock-in** | None | None | AWS | GCP | None | None | Azure |
| **Message retention** | Configurable (days–forever) | Until consumed | Up to 14 days | Up to 31 days | Configurable (JetStream) | Memory-bounded | Up to 14 days |
| **Ecosystem** | Huge (Connect, Streams, ksqlDB) | Good (AMQP, management UI) | AWS-native | GCP-native | Growing | Redis ecosystem | Azure-native |
| **Cost model** | Self-hosted or Confluent/MSK | Self-hosted or CloudAMQP | Per-request | Per-message | Self-hosted or Synadia | Included in Redis | Per-operation |

---

## Recommended Combinations

| Combination | Why |
|---|---|
| **Kafka + Kafka Connect + ksqlDB** | Full streaming platform: ingest from databases/APIs, stream process, sink to data warehouse — all in one ecosystem. |
| **SQS (Standard) + SNS + Lambda** | Serverless fan-out on AWS: zero ops, auto-scale, pay-per-use. Default choice for AWS shops without replay needs. |
| **RabbitMQ + Celery (Python) / Sidekiq (Ruby)** | Classic task queue for web apps: rich routing, DLQ, priority lanes; well-documented worker patterns. |
| **NATS JetStream + Go microservices** | Low-latency, lightweight service mesh alternative; single binary replaces both queue and KV store. |
| **Kafka + SQS** | Kafka for event log/stream processing; SQS as a buffer for downstream services that can't keep up with Kafka throughput. |
| **Redis Streams + existing Redis stack** | Simplest upgrade path: add durable queuing to a Redis-first architecture without deploying new infrastructure. |
| **Google Pub/Sub + Dataflow + BigQuery** | GCP native streaming analytics pipeline: ingest events, process with Dataflow, land in BigQuery for BI. |
| **Azure Service Bus + Azure Functions + Logic Apps** | Azure enterprise automation: workflow orchestration, scheduled messages, hybrid on-prem integration via Relay. |

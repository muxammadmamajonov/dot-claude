# Cost Model

**What this is:** A structured model of infrastructure and operational costs — covering cost drivers, per-environment estimates, unit economics, the scaling cost curve, and optimization levers. Used to forecast spend, set budget alerts, and guide architectural trade-offs.

**Who fills this:** DevOps/cloud architect + backend lead, reviewed by engineering manager and finance. Refresh quarterly or when traffic/usage changes >30%.

---

## 0. Document Metadata

| Field | Value |
|---|---|
| Project | `<project-name>` |
| Version | `<v1.0>` |
| Prepared by | `<name, role>` |
| Date | `<YYYY-MM-DD>` |
| Currency | `<USD>` |
| Billing period | `<Monthly>` |
| Cloud provider(s) | `<AWS / GCP / Azure / multi-cloud>` |

---

## 1. Cost Drivers

> What causes the bill to grow? List every resource category that appears on your invoice.

| Category | Service / Resource | Driver (what makes it scale) | Notes |
|---|---|---|---|
| Compute | `<ECS Fargate / EC2 / GKE nodes>` | `<Request volume, CPU/mem per pod, instance hours>` | `<Auto-scales; min 2 tasks>` |
| Serverless | `<Lambda / Cloud Run>` | `<Invocations × GB-seconds>` | `<Cold-start risk at low traffic>` |
| Database | `<RDS PostgreSQL / Aurora / PlanetScale>` | `<Instance size, storage GB, IOPS, backup retention>` | `<Multi-AZ doubles instance cost>` |
| Cache | `<ElastiCache Redis>` | `<Node size × node count>` | `<Reduces DB read load>` |
| Storage | `<S3 / GCS>` | `<GB stored + GET/PUT requests + egress>` | `<Lifecycle rules move to IA after 30 days>` |
| CDN | `<CloudFront / Fastly>` | `<Egress GB + requests>` | `<Cache-hit rate directly reduces origin cost>` |
| Networking | `<Data transfer, NAT Gateway, VPN>` | `<Egress bytes, AZ cross-traffic>` | `<NAT Gateway often underestimated>` |
| Queues / Messaging | `<SQS / Kafka MSK / Pub/Sub>` | `<Messages published + delivered + retained bytes>` | |
| Search | `<OpenSearch / Elasticsearch>` | `<Node size × node count, storage>` | |
| Observability | `<Datadog / Grafana Cloud / CloudWatch>` | `<Hosts, log volume GB/day, metrics, APM traces>` | `<Log retention policy critical>` |
| LLM / AI APIs | `<OpenAI / Anthropic / Bedrock>` | `<Input tokens + output tokens per request>` | `<Cache prompts where possible>` |
| Email / SMS | `<SendGrid / Twilio>` | `<Emails sent, SMS segments>` | |
| Auth | `<Auth0 / Cognito>` | `<Monthly active users (MAUs)>` | `<Auth0 pricing jumps at MAU tiers>` |
| Support / tooling | `<PagerDuty, GitHub, CI runners>` | `<Seats, build minutes>` | |

---

## 2. Per-Environment Cost Estimate

> Estimate monthly spend per environment. Dev/staging should be aggressively sized down.

### 2.1 Production

| Resource | Size / Config | Qty | Unit Cost/mo | Monthly Cost |
|---|---|---|---|---|
| `<ECS Fargate — app>` | `<0.5 vCPU, 1 GB RAM>` | `<4 tasks avg>` | `<~$14/task>` | `<~$56>` |
| `<RDS PostgreSQL>` | `<db.t4g.medium, Multi-AZ>` | `<1>` | `<~$140>` | `<~$140>` |
| `<ElastiCache Redis>` | `<cache.t3.small>` | `<1>` | `<~$25>` | `<~$25>` |
| `<S3 storage>` | `<500 GB + 10M GET>` | `<1>` | `<~$15>` | `<~$15>` |
| `<CloudFront>` | `<500 GB egress>` | `<1>` | `<~$42>` | `<~$42>` |
| `<NAT Gateway>` | `<100 GB processed>` | `<2 AZ>` | `<~$45>` | `<~$90>` |
| `<Datadog>` | `<Pro, 5 hosts>` | `<1>` | `<~$75/host>` | `<~$375>` |
| **Production total** | | | | **`<~$743/mo>`** |

### 2.2 Staging

| Resource | Size / Config | Monthly Cost |
|---|---|---|
| `<ECS Fargate — app>` | `<1 task, 0.25 vCPU>` | `<~$7>` |
| `<RDS PostgreSQL>` | `<db.t4g.micro, Single-AZ>` | `<~$18>` |
| `<ElastiCache Redis>` | `<cache.t3.micro>` | `<~$12>` |
| **Staging total** | | **`<~$55/mo>`** |

### 2.3 Development

> Use ephemeral environments; tear down nightly.

| Resource | Approach | Monthly Cost |
|---|---|---|
| `<App>` | `<Local Docker Compose or ephemeral ECS task>` | `<~$10>` |
| `<DB>` | `<Local Postgres or shared t4g.micro>` | `<~$9>` |
| **Dev total** | | **`<~$20/mo>`** |

### 2.4 Summary

| Environment | Monthly Cost | Annual Estimate |
|---|---|---|
| Production | `<$743>` | `<$8,916>` |
| Staging | `<$55>` | `<$660>` |
| Development | `<$20>` | `<$240>` |
| **Total** | **`<$818>`** | **`<$9,816>`** |

---

## 3. Unit Economics

> Express costs in terms that connect to business value.

| Metric | Formula | Current Value |
|---|---|---|
| Cost per active user / month | `<Total infra cost / MAU>` | `<$0.82 @ 1,000 MAU>` |
| Cost per API request | `<Total infra cost / monthly requests>` | `<$0.0008 @ 1M req/mo>` |
| Cost per transaction (if applicable) | `<Total infra cost / transactions>` | `<$0.041 @ 20K tx/mo>` |
| Cost per GB stored | `<Storage cost / GB>` | `<$0.023/GB>` |
| Infrastructure as % of revenue | `<Infra cost / MRR>` | `<8% @ $10K MRR>` |

> **Target range:** Infrastructure typically 5–20% of revenue for SaaS at scale. Track monthly and alert if trending above 25%.

---

## 4. Scaling Cost Curve

> How does cost grow as the system scales? Identify where costs are linear, step-function, or sub-linear.

| Scale Point | Monthly Traffic / Users | Projected Cost | Key Step-Function Events |
|---|---|---|---|
| Current | `<1,000 MAU, 1M req/mo>` | `<$743>` | — |
| 5× | `<5,000 MAU, 5M req/mo>` | `<~$1,600>` | `<RDS upgrade to db.t4g.large; +2 Fargate tasks>` |
| 10× | `<10,000 MAU, 10M req/mo>` | `<~$2,800>` | `<Read replica for DB; Redis cluster mode>` |
| 50× | `<50,000 MAU, 50M req/mo>` | `<~$9,200>` | `<Aurora switch; Datadog enterprise tier; dedicated NAT per AZ>` |
| 100× | `<100,000 MAU, 100M req/mo>` | `<~$16,000>` | `<Multi-region; Aurora Global; CDN reserved capacity>` |

> **Sub-linear levers:** Reserved instance commitments (1-year = ~30% off), Savings Plans, S3 Intelligent Tiering, CDN cache optimization.
> **Super-linear risks:** NAT Gateway egress, Datadog log volume, LLM token spend at scale, cross-AZ data transfer.

---

## 5. Cost Optimization Levers

> Actionable ways to reduce spend, ranked by effort vs. impact.

| Lever | Potential Saving | Effort | Priority | Owner |
|---|---|---|---|---|
| `<Purchase 1-year Reserved Instances for DB + cache>` | `<~30% on committed resources>` | Low | High | `<DevOps>` |
| `<Enable S3 Intelligent Tiering>` | `<~40% on infrequently accessed objects>` | Low | High | `<DevOps>` |
| `<Increase CloudFront cache TTL from 60s to 300s>` | `<~20% on origin requests + egress>` | Low | High | `<Backend>` |
| `<Right-size Fargate tasks after profiling>` | `<~20% compute>` | Medium | High | `<SRE>` |
| `<Datadog log retention 15d → 7d for debug logs>` | `<~$80/mo>` | Low | Medium | `<SRE>` |
| `<Implement LLM prompt caching (Anthropic / OpenAI)>` | `<50–90% on repeated prompt prefixes>` | Medium | High | `<AI/ML team>` |
| `<Move nightly jobs to Fargate Spot / Preemptible VMs>` | `<~70% on batch compute>` | Medium | Medium | `<Backend>` |
| `<Enforce per-team cost tags; chargeback model>` | `<Drives accountability, 10–20% reduction>` | Medium | Medium | `<FinOps>` |
| `<Replace NAT Gateway with VPC endpoint for S3/DynamoDB>` | `<~$40/mo per AZ>` | Low | Medium | `<DevOps>` |
| `<Evaluate Aurora Serverless v2 for staging>` | `<~$90/mo>` | Low | Medium | `<DevOps>` |

---

## 6. Budget Alerts & Governance

> How spend is monitored and who is accountable.

| Alert | Threshold | Channel | Action |
|---|---|---|---|
| Monthly forecast > budget | `<110% of monthly budget>` | `<Slack #finops + email to EM>` | `<Review in weekly standup>` |
| Daily spend spike | `<>150% of 7-day average daily spend>` | `<PagerDuty P3>` | `<Identify runaway resource>` |
| Single service > 40% of bill | `<Any one service >40%>` | `<Email to DevOps lead>` | `<Investigate and optimize>` |
| Unused resources | `<Resources with 0 traffic for 14 days>` | `<Weekly Slack digest>` | `<Terminate or decommission>` |

### 6.1 Tagging Policy

All resources must be tagged with:

| Tag Key | Example Value | Purpose |
|---|---|---|
| `environment` | `production` | Separate prod vs. non-prod |
| `team` | `platform` | Chargeback |
| `service` | `api-gateway` | Per-service cost attribution |
| `cost-center` | `engineering` | Finance reporting |

### 6.2 Monthly FinOps Review

- **Meeting:** `<First Monday of each month, 30 min>`
- **Attendees:** `<DevOps lead, EM, Finance rep>`
- **Agenda:** actual vs. forecast, top cost drivers, optimization actions, next-month budget
- **Tool:** `<AWS Cost Explorer / GCP Cost Dashboard / Infracost in CI>`

---

## 7. Assumptions & Risks

> What could make this model wrong?

| Assumption | If Wrong | Risk Level |
|---|---|---|
| `<Traffic grows linearly with users>` | `<Viral event → 100× spike overnight>` | High |
| `<LLM usage stays at current ratio per request>` | `<Feature expansion increases token usage 5×>` | High |
| `<Data egress stays within CDN cache>` | `<Cache invalidation bug floods origin>` | Medium |
| `<Reserved Instance discount applied>` | `<Commitment not made before quarter end>` | Medium |
| `<Log volume stays stable>` | `<New verbose logging in feature X>` | Low |

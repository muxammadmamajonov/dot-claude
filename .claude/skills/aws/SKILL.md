---
name: aws
description: >
  Activate for any AWS architecture, IAM design, cost analysis, or infrastructure work.
  Triggers: EC2, ECS, EKS, Lambda, S3, RDS, Aurora, DynamoDB, SQS, SNS, VPC, CloudFormation,
  CDK, Terraform on AWS, IAM, well-architected review, AWS cost optimization, or any
  "deploy to AWS" request.
---

# AWS

## When to use
- Designing or reviewing AWS architectures
- Writing IAM policies (least-privilege analysis)
- Choosing compute: EC2 vs ECS vs EKS vs Lambda vs App Runner vs Fargate
- Configuring VPC, subnets, security groups, NACLs, Transit Gateway
- Setting up S3 buckets (access control, lifecycle, replication, event triggers)
- Selecting and configuring RDS/Aurora, ElastiCache, DynamoDB
- Designing messaging (SQS, SNS, EventBridge, Kinesis)
- Cost analysis and Well-Architected review
- CDK / CloudFormation / Terraform IaC authoring

## Workflow

1. **Classify the workload:** web API, batch/ETL, event-driven, stateful service, ML inference, or static content. Each has a different primary compute and storage choice.

2. **IAM first — model permissions before building:**
   - One IAM role per service/workload; never share roles across unrelated services.
   - Start with `deny *`, add only the actions and resources the service needs.
   - Use resource-based policies (S3 bucket policy, Lambda resource policy) to further restrict cross-account.
   - Use IAM Access Analyzer to validate policies and detect overly broad conditions.
   - Never use `*` as the resource ARN in `Allow` statements unless unavoidable (e.g., `logs:CreateLogGroup`).
   - Prefer AWS managed policies as a starting point; customize with inline policies for tighter scope.
   - Use permission boundaries on developer-created roles to prevent privilege escalation.
   - Use AWS Organizations SCPs at the account/OU level to enforce global guardrails.
   - Rotate access keys; prefer IAM roles + STS AssumeRole over long-lived credentials everywhere.

3. **VPC design:**
   - Default: 3 AZ, 3 tiers: public (ALB, NAT GW), private-app (compute), private-data (RDS, ElastiCache).
   - Never put databases in public subnets.
   - Use VPC Endpoints (Gateway for S3/DynamoDB, Interface for everything else) to keep traffic off the public internet and reduce data transfer costs.
   - Security groups: stateful, layer-7 rule as narrow as possible (port + source SG, not CIDR).
   - NACLs: stateless, use only for broad subnet-level deny rules.
   - Flow Logs: enable on all VPCs for security and cost debugging.

4. **Compute selection:**
   - **Lambda:** event-driven, < 15 min, bursty, stateless. Use Provisioned Concurrency for latency-sensitive paths. Keep packages < 50 MB (use Lambda Layers or container images for large deps). Set memory to tune CPU proportionally.
   - **ECS Fargate:** containerized services without cluster management. Good for APIs, workers, sidecars. Use task-level IAM roles.
   - **ECS on EC2 / EKS:** when you need GPU, specific instance types, or fine-grained cluster control.
   - **EC2:** stateful workloads, licensed software, or bare-metal needs. Use Auto Scaling Groups + Launch Templates. Prefer Graviton3 (arm64) for ~20% better price-performance.
   - **App Runner:** simplest path for containerized web API with zero cluster ops.
   - Use Spot Instances for batch/CI/stateless workers (up to 90% cost saving); always handle `SIGTERM` gracefully.

5. **Storage:**
   - **S3:** block public access at account level by default; use bucket policies + OAC for CloudFront. Enable versioning + MFA delete on critical buckets. Set lifecycle rules: transition to S3-IA at 30 days, Glacier at 90 days for cold data.
   - **RDS/Aurora:** enable Multi-AZ for production. Use Aurora Serverless v2 for variable load (scales from 0.5 ACU). Enable Performance Insights and Enhanced Monitoring. Store credentials in Secrets Manager, rotate automatically. Use RDS Proxy for Lambda → RDS connections (avoids connection exhaustion).
   - **DynamoDB:** on-demand capacity for unpredictable workloads; provisioned + Auto Scaling for steady-state. Enable point-in-time recovery. Use DynamoDB Streams + Lambda for event-driven patterns. Design for single-table where possible to minimize round-trips.
   - **EFS:** shared POSIX filesystem for ECS/EKS workloads needing shared mutable storage.

6. **Messaging / eventing:**
   - **SQS Standard:** at-least-once, best-effort order. Good for worker queues. Set `VisibilityTimeout` ≥ 6× function timeout. Enable DLQ.
   - **SQS FIFO:** exactly-once, strict order within message group. Throughput: 3,000 msg/s with batching.
   - **SNS:** fan-out to multiple SQS queues, Lambda, HTTP endpoints, email. Use message filtering to route.
   - **EventBridge:** preferred for cross-service / cross-account event routing. Supports schema registry. Use event buses + rules with targets.
   - **Kinesis Data Streams:** ordered, replay-capable streaming. Use when you need exactly-once processing order at high throughput.
   - **MSK (Kafka):** when you need Kafka compatibility or migration from on-prem Kafka.

7. **Cost controls (Well-Architected Cost pillar):**
   - Enable AWS Cost Explorer, set budgets with alerts via AWS Budgets.
   - Tag all resources (`env`, `team`, `service`, `cost-center`) and enable Cost Allocation Tags.
   - Use Compute Optimizer recommendations for right-sizing EC2, Lambda, ECS.
   - Purchase Savings Plans (Compute or EC2) for baseline steady-state workloads (1- or 3-year).
   - Delete unattached EBS volumes, idle load balancers, unused NAT Gateways (charged per AZ/hour).
   - Use S3 Intelligent-Tiering for data with unknown access patterns.
   - Architect to minimize data transfer: keep compute and data in same AZ; use VPC Endpoints.

8. **Well-Architected review (5 pillars):**
   - Operational Excellence: IaC for all resources, runbooks, automated deployment pipelines.
   - Security: encryption at rest (KMS) and in transit (TLS 1.2+), least-privilege IAM, GuardDuty, Security Hub.
   - Reliability: Multi-AZ, health checks, Auto Scaling, Circuit Breaker pattern, chaos engineering.
   - Performance Efficiency: right-sizing, caching (ElastiCache, CloudFront), async decoupling.
   - Cost Optimization: reserved capacity, Spot, right-sizing, lifecycle policies, waste elimination.

9. **IaC (CDK recommended):**
   - Use AWS CDK (TypeScript) for greenfield; CloudFormation YAML for legacy/migration.
   - Organize CDK apps: one Stack per deployment unit; use `cdk.Stage` for multi-account pipelines.
   - Use `cdk synth` + `cfn-nag` / `checkov` in CI before deploy.
   - Tag stacks with `cdk.Tags.of(app).add(key, value)`.
   - Use CDK Pipelines (`CodePipeline`) for self-mutating deployment pipelines.

## Standards

**Do:**
- Enable CloudTrail (all regions, management + data events on sensitive S3/KMS) from day one.
- Enable AWS Config with conformance packs (e.g., `AWS-Best-Practices`) for continuous compliance.
- Use KMS Customer Managed Keys (CMK) for data classification requirements; use AWS managed keys for general purpose.
- Enable GuardDuty, Security Hub, and Inspector on all accounts.
- Store all secrets in Secrets Manager (not Parameter Store `/plain`, not env vars).
- Use ALB over CLB/NLB for HTTP/S workloads; NLB only for TCP/TLS passthrough or extreme throughput.
- Enable access logging on all ALBs and S3 buckets.
- Pin Lambda runtime versions; subscribe to runtime deprecation notifications.

**Do not:**
- Grant `AdministratorAccess` to application roles.
- Put long-lived access keys in code or environment variables on compute (use IMDSv2 instance metadata or task roles).
- Use `0.0.0.0/0` in security group ingress rules except for internet-facing ALB port 443.
- Disable IMDSv2 on EC2 instances (it blocks SSRF credential theft attacks).
- Use `us-east-1` as the sole region for multi-region SLAs without explicit fallback.
- Store state in Lambda `/tmp` beyond a single invocation.
- Rely on EC2 instance IP addresses in security group rules — use SG-to-SG references.

## Common mistakes to avoid

- **IAM `*` resource on S3 actions:** `s3:PutObject` on `*` grants write to every bucket in the account. Always scope to `arn:aws:s3:::bucket-name/*`.
- **Missing DLQ on SQS/Lambda:** failed messages silently disappear after `maxReceiveCount` retries.
- **Single-AZ RDS without read replica:** one AZ outage takes down the database with no failover.
- **Lambda hitting RDS directly without RDS Proxy:** under load, Lambda spawns hundreds of connections, exhausting the RDS connection pool.
- **NAT Gateway per AZ not accounted for:** each AZ needs its own NAT GW for HA, tripling the fixed cost (~$32/AZ/month).
- **Forgetting S3 data transfer costs:** egress to internet is ~$0.09/GB; architect CloudFront in front of S3 for public assets.
- **Using CloudWatch basic metrics only:** EC2 memory and disk metrics require the CloudWatch Agent — not enabled by default.

## Output format

- Architecture decisions → `docs/decisions/aws-<topic>-<date>.md` (use `.claude/templates/decision-record.md`)
- Infrastructure diagrams → `docs/specs/architecture.md` (use `.claude/templates/architecture.md`)
- IAM policies → inline in `docs/specs/security-model.md` (use `.claude/templates/security-model.md`)
- Cost model → `docs/specs/cost-model.md` (use `.claude/templates/cost-model.md`)
- Runbooks → `docs/runbooks/<service>.md` (use `.claude/templates/runbook.md`)

## Related checklists
- `.claude/checklists/architecture.md`
- `.claude/checklists/security.md`
- `.claude/checklists/devops.md`
- `.claude/checklists/production.md`
- `.claude/checklists/cost.md`
- `.claude/checklists/observability.md`

## Related agents
- `.claude/agents/core/solution-architect.md`
- `.claude/agents/engineering/cloud-architect.md`
- `.claude/agents/engineering/infrastructure-engineer.md`
- `.claude/agents/engineering/devops-engineer.md`
- `.claude/agents/quality/security-auditor.md`
- `.claude/agents/quality/production-readiness-auditor.md`

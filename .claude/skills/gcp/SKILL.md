---
name: gcp
description: >
  Activate for any Google Cloud Platform architecture, IAM, deployment, data, or cost work.
  Triggers: GCP, Google Cloud, GKE, Cloud Run, Cloud Functions, BigQuery, Cloud SQL, Spanner,
  Pub/Sub, Cloud Storage, Firestore, Vertex AI, Artifact Registry, Terraform on GCP, or
  "deploy to Google Cloud".
---

# GCP (Google Cloud Platform)

## When to use
- Designing or reviewing GCP architectures
- IAM / Workload Identity design (least-privilege on GCP)
- Choosing compute: GCE vs GKE vs Cloud Run vs Cloud Functions vs App Engine
- BigQuery schema, partitioning, clustering, and cost control
- Cloud SQL / Spanner / Firestore / Bigtable selection and configuration
- Pub/Sub and Eventarc event-driven patterns
- Cloud Storage bucket design, IAM, lifecycle
- CI/CD with Cloud Build, Artifact Registry, Cloud Deploy
- Cost optimization and budget alerts
- Terraform / Deployment Manager IaC

## Workflow

1. **Classify workload type:** web serving, batch/analytics, streaming, ML training/inference, or data warehousing. Each drives a different primary GCP service combination.

2. **IAM — resource hierarchy first:**
   - GCP hierarchy: Organization → Folder → Project → Resource. Grant permissions at the lowest level possible.
   - Use folders to separate environments (prod, staging, dev) and business units.
   - Prefer predefined roles over basic roles (`Owner`/`Editor`/`Viewer`). Use custom roles for fine-grained needs.
   - Use Workload Identity for GKE pods and Cloud Run services — eliminates service account key files.
   - Service account keys are a security antipattern; avoid outside of local dev tooling.
   - Enable IAM Recommender and apply recommendations regularly.
   - Use VPC Service Controls for sensitive data projects (prevent data exfiltration).
   - Enable Organization Policy constraints: `compute.requireOsLogin`, `compute.vmExternalIpAccess`, `iam.disableServiceAccountKeyCreation`.

3. **Networking:**
   - Use Shared VPC for multi-project environments; one host project owns the network, service projects attach.
   - Cloud NAT for private GKE nodes / Cloud Run to reach the internet outbound without public IPs.
   - Private Google Access: GCE instances in private subnets can reach Google APIs without external IP.
   - Use Private Service Connect or VPC peering for managed service connectivity (Cloud SQL, Memorystore).
   - Cloud Armor: WAF and DDoS protection at the Global Load Balancer layer.
   - Use Google-managed SSL certificates on HTTPS load balancers.

4. **Compute selection:**
   - **Cloud Run:** preferred for stateless HTTP services and event-driven containers. Scales to zero. Supports Knative. Use min-instances to avoid cold starts. Supports gRPC and WebSockets (Cloud Run v2).
   - **GKE Autopilot:** managed Kubernetes without node management. Best for complex microservices needing K8s semantics. Workload Identity is default.
   - **GKE Standard:** when you need specific node machine types, GPU nodes, or fine-grained node management.
   - **Cloud Functions (2nd gen):** event-driven functions backed by Cloud Run. Use for lightweight Pub/Sub consumers, HTTP triggers, Eventarc events.
   - **Compute Engine (GCE):** VMs for stateful workloads, licensed software, custom kernels. Prefer N2D (AMD) or C3 (Intel) over N1 for price-performance. T2A (Arm/Ampere) for ~30% cost saving on compatible workloads.
   - **Batch:** managed job scheduling for HPC/ML batch workloads without GKE overhead.

5. **BigQuery — analytics and data warehouse:**
   - Partition tables by date/timestamp (`PARTITION BY DATE(_PARTITIONTIME)` or a column); required for tables > 1 TB.
   - Cluster on columns used in `WHERE` and `JOIN` (up to 4 columns) — reduces bytes scanned on top of partitioning.
   - Never use `SELECT *` in production queries; explicitly project columns to reduce scanned bytes.
   - Use `INFORMATION_SCHEMA.JOBS_BY_PROJECT` to audit query costs.
   - Use BigQuery Reservations (slot commitments) for predictable high-volume workloads; on-demand for bursty/ad-hoc.
   - Authorized views and row-level security for multi-tenant data sharing without copying datasets.
   - Prefer `MERGE` over `DELETE + INSERT` for upserts; reduces slot consumption.
   - Use BigQuery Omni for querying data in AWS S3 or Azure ADLS without moving it.
   - External tables (BigLake) for querying Parquet/CSV in Cloud Storage without ingestion cost.

6. **Cloud SQL / Spanner / Firestore:**
   - **Cloud SQL (PostgreSQL/MySQL):** managed relational DB. Enable HA (high availability with standby) for production. Use private IP + VPC peering. Set `max_connections` per instance size.
   - **Spanner:** globally distributed, horizontally scalable relational DB. Use when you need > 2 TB, global writes, or 99.999% SLA. Costly; size compute capacity in processing units.
   - **Firestore:** serverless document DB, native mobile/web SDK, offline sync. Good for user-facing apps, configuration, low-latency lookups. Not a replacement for BigQuery.
   - **Bigtable:** wide-column NoSQL for time-series, telemetry, and low-latency high-throughput workloads (>1 TB, millions of ops/s).

7. **Pub/Sub and Eventarc:**
   - Pub/Sub: at-least-once delivery. Set `ackDeadline` ≥ processing time + buffer. Always set a dead-letter topic.
   - Use push subscriptions for Cloud Run / Cloud Functions (HTTP endpoint receives messages); pull for batch workers.
   - Eventarc: routes events from GCP services (Cloud Storage, Audit Logs, Pub/Sub) to Cloud Run, Cloud Functions, GKE targets. Prefer over manual Pub/Sub plumbing for GCP service triggers.
   - Use Pub/Sub Lite for very high throughput at lower cost (zonal, no replication by default).

8. **Cloud Storage:**
   - Enable uniform bucket-level access (disables ACLs); manage access only through IAM.
   - Block public access by default; use signed URLs for time-limited public access.
   - Lifecycle rules: transition to Nearline (30 days), Coldline (90 days), Archive (365 days) for cost reduction.
   - Use CMEK (Cloud KMS) for regulated data. Default encryption is Google-managed.
   - Enable Object Versioning on critical buckets; set lifecycle to clean old versions.
   - Use signed URLs or Cloud CDN with a backend bucket for static asset serving.

9. **Cost controls:**
   - Set budget alerts at 50%, 90%, 100% of monthly budget with email + Pub/Sub notification.
   - Use committed use discounts (CUDs) for sustained GCE/GKE/Cloud SQL workloads (1- or 3-year).
   - BigQuery: use cost controls (`maximumBytesBilled`) in jobs; prefer slot reservations over on-demand for > 100 TB/month.
   - Enable Cloud Recommender for idle resources, right-sizing, and IAM over-provisioning.
   - Delete unused persistent disks, static IPs, and Cloud NAT rules (billed when unattached).
   - Use Cloud Storage nearline/coldline/archive for cold data vs Standard tier.

10. **IaC (Terraform recommended):**
    - Use `google` and `google-beta` Terraform providers. Pin provider versions.
    - Organize: one root module per environment, shared modules for reusable components (VPC, GKE cluster, Cloud SQL).
    - Use Workload Identity Federation in CI/CD (GitHub Actions, GitLab) instead of service account keys.
    - Use `terraform plan` artifact in CI; require human approval for `apply` in prod.
    - Store state in Cloud Storage backend with bucket versioning + locking via Cloud Storage.

## Standards

**Do:**
- Enable Cloud Audit Logs (Admin Activity + Data Access) on all projects.
- Enable Security Command Center (SCC) Premium for threat detection and compliance.
- Use Cloud Armor for all internet-facing HTTPS load balancers.
- Enable Binary Authorization on GKE to enforce signed container images.
- Use Artifact Registry (not Container Registry, which is deprecated) for container and package storage.
- Enable VPC Flow Logs on all subnets for network visibility.
- Tag all resources with `environment`, `team`, `service` labels for cost attribution.

**Do not:**
- Create service account keys for GKE workloads — use Workload Identity.
- Grant `roles/owner` or `roles/editor` to service accounts.
- Use `allUsers` or `allAuthenticatedUsers` on sensitive Cloud Storage buckets.
- Put Cloud SQL instances with public IP without Authorized Networks or Cloud SQL Auth Proxy.
- Use App Engine Standard for new projects (prefer Cloud Run for portability).
- Query BigQuery without partition filters on large partitioned tables (full scan costs).
- Expose GKE master endpoint publicly without authorized networks or private cluster.

## Common mistakes to avoid

- **Missing partition filter in BigQuery:** query against a 10 TB table without `WHERE _PARTITIONDATE = ...` scans all data — can cost hundreds of dollars per query.
- **Service account key files committed to source control:** rotate immediately, audit with Secret Scanner.
- **GKE nodes with public IPs:** use private cluster with Cloud NAT; public IPs are a direct attack surface.
- **Over-provisioning Spanner:** each processing unit is billed whether used or not; start small and monitor CPU utilization (target < 65% for regional, < 45% for multi-regional).
- **Cloud Run cold starts at scale:** set `min-instances: 1` for latency-sensitive services (costs ~$10/month for 1 vCPU instance).
- **Forgetting Cloud CDN for Cloud Run/GCS public content:** without CDN, egress charges accumulate at ~$0.12/GB.
- **Using default compute service account with Editor role:** the default SA has too many permissions; create dedicated SAs per service.

## Output format

- Architecture decisions → `docs/decisions/gcp-<topic>-<date>.md` (use `.claude/templates/decision-record.md`)
- Infrastructure specs → `docs/specs/architecture.md` (use `.claude/templates/architecture.md`)
- BigQuery schema → `docs/data-model/bigquery-<dataset>.md` (use `.claude/templates/data-model.md`)
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
- `.claude/agents/engineering/data-engineer.md`
- `.claude/agents/engineering/devops-engineer.md`
- `.claude/agents/quality/security-auditor.md`
- `.claude/agents/quality/production-readiness-auditor.md`

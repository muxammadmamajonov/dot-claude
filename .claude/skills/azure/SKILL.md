---
name: azure
description: >
  Activate for any Microsoft Azure architecture, RBAC/Entra ID, AKS, App Service, Functions,
  Azure SQL, Cosmos DB, storage, Service Bus, or cost work. Triggers: Azure, AKS, Azure
  Functions, App Service, Azure SQL, Cosmos DB, Service Bus, Blob Storage, Entra ID, ARM,
  Bicep, Terraform on Azure, or "deploy to Azure".
---

# Azure

## When to use
- Designing or reviewing Azure architectures
- Entra ID (formerly Azure AD) and RBAC design
- Choosing compute: AKS vs App Service vs Azure Functions vs Container Apps vs VMs
- Azure SQL / Cosmos DB / Table Storage / Blob Storage selection and configuration
- Service Bus, Event Grid, Event Hubs messaging design
- Virtual Network, NSG, Private Endpoints, Azure Firewall networking
- Azure Monitor, Application Insights, Log Analytics observability
- Cost analysis, reservations, Azure Well-Architected review
- Bicep / ARM / Terraform IaC authoring

## Workflow

1. **Classify workload:** web API, microservices, batch, event-driven, data analytics, or ML. Map to Azure landing zone pattern (Corp/Online/Sandbox management group).

2. **Entra ID + RBAC first:**
   - Use managed identities (system-assigned or user-assigned) for all Azure compute — no credentials in code.
   - Assign built-in RBAC roles at the lowest scope (resource > resource group > subscription > management group).
   - Prefer `Contributor` + specific data-plane roles over `Owner`; never grant `Owner` to applications.
   - Use custom roles only when built-in roles are too permissive.
   - Conditional Access policies: require MFA for all users; block legacy authentication protocols.
   - Use Privileged Identity Management (PIM) for JIT elevation of privileged roles (Global Admin, Subscription Owner).
   - Use Microsoft Entra Workload Identities (federated credentials) for CI/CD (GitHub Actions OIDC) — no SP secrets.
   - Enable Entra ID Identity Protection for risk-based sign-in policies.

3. **Virtual Network design:**
   - Hub-and-spoke topology: hub VNet (Azure Firewall, VPN/ExpressRoute GW, Bastion) + spoke VNets per workload/environment.
   - Use Azure Virtual WAN for large-scale or multi-region hub-and-spoke with SD-WAN requirements.
   - Private Endpoints for all PaaS services (Storage, SQL, Cosmos, Service Bus, Key Vault) — eliminates public internet exposure.
   - NSGs: apply at subnet level as baseline; apply to NIC only for exception rules. Use Application Security Groups to avoid IP-based rules.
   - Azure Firewall (Standard or Premium) for centralized outbound filtering and threat intelligence.
   - Azure DDoS Protection Standard on hub VNet for production.
   - Use Azure Bastion for admin access to VMs — no public RDP/SSH endpoints.

4. **Compute selection:**
   - **Azure Container Apps:** serverless Kubernetes-based platform. Best for microservices, background workers, event-driven workloads. Scales to zero. Built-in Dapr and KEDA support.
   - **Azure Functions:** event-triggered serverless compute. Prefer isolated process model (dotnet-isolated, Node.js v4). Use Durable Functions for orchestration and fan-out patterns.
   - **App Service (Web Apps):** managed PaaS for HTTP workloads. Use P-series (Premium v3) for production (includes zone redundancy, better cold start). Enable deployment slots for blue/green.
   - **AKS (Azure Kubernetes Service):** when you need full Kubernetes control, GPU nodes, or complex multi-container orchestration. Enable Workload Identity, OIDC Issuer, and Azure CNI. Use node pools (system + user separated).
   - **Azure Batch:** HPC and large-scale parallel job processing.
   - **VMs:** lift-and-shift or licensed software. Use Virtual Machine Scale Sets with Spot instances for batch/stateless workers.

5. **Storage:**
   - **Blob Storage:** object storage. Use Standard LRS for dev, GRS/ZRS for production. Immutable storage (WORM) for compliance. Enable soft delete + versioning on production accounts. Access tiers: Hot (frequent), Cool (30-day min), Cold (90-day min), Archive (180-day min).
   - **Azure SQL:** fully managed SQL Server PaaS. Use General Purpose or Business Critical tier. Enable zone-redundant HA. Use Elastic Pools for multi-tenant SaaS. Enable Advanced Threat Protection + Transparent Data Encryption.
   - **Cosmos DB:** globally distributed NoSQL. Choose API carefully: NoSQL (recommended for new projects), MongoDB (migration), Cassandra, Gremlin (graph). Enable multi-region writes only if needed (increases RU cost). Use serverless capacity for dev/test, provisioned + autoscale for production. Always set a partition key with high cardinality.
   - **Azure Cache for Redis:** Premium tier for persistence, clustering, and VNet injection. Standard for HA without clustering.
   - **Azure Files / NetApp Files:** shared file storage for lift-and-shift or HPC.

6. **Messaging (Service Bus, Event Grid, Event Hubs):**
   - **Service Bus Queues:** reliable message queuing, at-least-once, FIFO within sessions, dead-letter queue built-in. Use Premium tier for VNet integration and message sizes > 256 KB.
   - **Service Bus Topics:** publish-subscribe with multiple subscriptions and filter rules. Replace fan-out patterns that would need multiple queues.
   - **Event Grid:** event routing from Azure services to handlers (Functions, Logic Apps, Webhooks). Push model, at-least-once, low latency. Use for resource lifecycle events (Blob created, Resource state changed).
   - **Event Hubs:** high-throughput event streaming (Kafka-compatible). Use for telemetry, log ingestion, streaming analytics. Partition count is fixed post-creation — plan capacity upfront. Enable Capture to Blob/ADLS for durable replay.
   - Default choice: Service Bus for commands/tasks (need reliability, ordering, DLQ); Event Grid for events (state changes); Event Hubs for streaming/telemetry.

7. **Observability:**
   - Enable Application Insights for all web apps and Functions (auto-instrumented via connection string).
   - Send all diagnostic logs and metrics to a central Log Analytics workspace.
   - Use Azure Monitor alerts with Action Groups (email, SMS, webhook, Azure Function) for threshold and anomaly alerts.
   - Enable Azure Monitor Baseline Alerts (AMBA) for platform-level alerts (VM CPU, SQL DTU, Storage availability).
   - Use Workbooks for custom dashboards instead of legacy Azure dashboards.
   - Retain Log Analytics data ≥ 90 days for operational needs; archive to Storage Account for compliance.

8. **Cost controls:**
   - Use Azure Reservations (1- or 3-year) for compute (VMs, App Service, AKS nodes, SQL, Cosmos).
   - Azure Hybrid Benefit: apply existing Windows Server and SQL Server licenses to Azure VMs and SQL.
   - Dev/Test subscription pricing for non-production workloads (requires Visual Studio subscriptions).
   - Set budgets and alerts in Microsoft Cost Management (50%, 90%, 100% threshold).
   - Use Azure Advisor cost recommendations; prioritize right-sizing and reservation recommendations.
   - Tag all resources with `environment`, `team`, `service`, `cost-center` — required for cost allocation reports.
   - Delete orphaned disks, unused Public IP addresses, empty resource groups.

9. **IaC (Bicep recommended for Azure-native):**
   - Bicep compiles to ARM; supports `@description`, modules, and parameter files. Use `az bicep build` to validate.
   - Organize: one main.bicep per environment, shared modules in `/modules/` (vnet, aks-cluster, sql-server).
   - Use parameter files per environment (`parameters/prod.json`, `parameters/dev.json`).
   - Use Azure Deployment Environments or Azure Developer CLI (`azd`) for developer self-service.
   - Terraform: use `azurerm` provider (v3.x+); store state in Azure Storage backend with state locking.
   - Run `az deployment what-if` (Bicep) or `terraform plan` before applying changes.
   - Use Microsoft Defender for DevOps (GitHub/ADO) to scan IaC for misconfigurations.

## Standards

**Do:**
- Enable Microsoft Defender for Cloud (all plans) on all subscriptions.
- Enable Defender for Containers on AKS clusters.
- Use Azure Key Vault for all secrets, certificates, and keys; enable soft-delete + purge protection.
- Enable Private Endpoints for all PaaS services in production — disable public network access.
- Use zone-redundant SKUs (ZRS storage, Business Critical SQL, Premium Service Bus) for production SLAs.
- Enable Transparent Data Encryption (TDE) with CMK for regulated data in SQL/Cosmos.
- Use Azure Policy to enforce organizational standards at scale (e.g., require tags, enforce allowed locations, require TLS).

**Do not:**
- Use Service Principal secrets (client secret) for CI/CD; use federated credentials (OIDC) instead.
- Grant `Contributor` at subscription scope to application identities.
- Expose Azure SQL or Cosmos DB public endpoints in production — use Private Endpoints.
- Use LRS storage for production data that cannot be re-created.
- Use App Service Consumption plan (v1) for latency-sensitive workloads; use Premium v3 (Ep1+) for Functions.
- Store connection strings or secrets in App Service application settings in plain text — reference Key Vault secrets via `@Microsoft.KeyVault(...)`.
- Use the Azure portal for production changes — all changes must go through IaC + CI/CD pipeline.

## Common mistakes to avoid

- **Missing managed identity — using Service Principal secrets:** SP client secrets expire and are a credential leak risk. Migrate to managed identity or federated credentials.
- **Cosmos DB partition key chosen incorrectly:** a low-cardinality partition key (e.g., `status: "active"`) causes hot partitions. Choose a high-cardinality key aligned with query patterns.
- **AKS with kubenet networking:** kubenet lacks UDR and Private Link support; use Azure CNI or Azure CNI Overlay for production.
- **Not enabling zone redundancy on App Service:** Standard and below tiers have no zone redundancy; Production SLAs require Premium v3.
- **Event Hubs partition count too low:** once created, cannot be increased (except via migration). Plan for peak throughput at design time (1 partition = ~1 MB/s).
- **Log Analytics workspace per resource instead of centralized:** siloed observability, high cost from redundant retention. Centralize all logs into one workspace per region.
- **Forgetting Cosmos DB RU provisioning:** default 400 RU/s is often insufficient for production; enable autoscale (10× burst) and monitor `NormalizedRUConsumption`.

## Output format

- Architecture decisions → `docs/decisions/azure-<topic>-<date>.md` (use `.claude/templates/decision-record.md`)
- Infrastructure specs → `docs/specs/architecture.md` (use `.claude/templates/architecture.md`)
- Security model → `docs/specs/security-model.md` (use `.claude/templates/security-model.md`)
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

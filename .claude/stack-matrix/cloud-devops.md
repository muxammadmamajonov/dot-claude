# Cloud & DevOps Stack Matrix

Choose your cloud and DevOps toolchain by answering: (1) Are you cloud-agnostic or already invested in one provider's ecosystem? (2) Do you need managed compute, or will you run containers/VMs directly? (3) How much operational overhead can your team absorb? Small teams should lean on PaaS and managed services; larger teams can justify Kubernetes and Terraform.

Key decision drivers: team size, existing cloud spend/commitments, compliance/data-residency requirements, deployment frequency, budget for managed services vs. self-managed infra, and long-term vendor lock-in risk.

---

## AWS

- **When to use:** Default choice for most production systems. Broadest service catalog, deepest ecosystem, most available engineers, strongest compliance certifications (HIPAA, SOC2, FedRAMP, PCI).
- **When NOT to use:** Teams already standardized on Google Cloud (ML/data workloads) or Azure (Microsoft-shop enterprises); projects requiring specific services only available on other clouds.
- **Strengths:** Largest global region footprint, most mature managed services (RDS, EKS, Lambda, SQS, S3), dominant in enterprise and startup ecosystems, best documentation and community support.
- **Weaknesses:** Console complexity is overwhelming; IAM is powerful but notoriously confusing; pricing is opaque; vendor lock-in is real (Lambda, DynamoDB, SQS are AWS-proprietary).
- **Team fit:** Any team. AWS skills are the most transferable. Largest hiring pool.
- **Scale fit:** Petabyte scale, global PoPs, multi-region active-active. Used by the largest internet companies.
- **Production risks:** IAM misconfiguration exposing resources; S3 bucket public access; unexpected egress costs; Lambda cold starts in latency-sensitive paths; region-specific service unavailability.

---

## GCP (Google Cloud Platform)

- **When to use:** Data/ML-heavy workloads (BigQuery, Vertex AI, TPUs), Kubernetes-native teams (GKE is the gold standard), companies already using Google Workspace, gaming backends (Agones).
- **When NOT to use:** General-purpose cloud if the team lacks GCP familiarity; projects where AWS talent pool or compliance certifications matter most.
- **Strengths:** BigQuery is best-in-class serverless analytics; GKE is the most mature managed Kubernetes; Vertex AI and TPU access for ML; strong networking (private global fiber backbone).
- **Weaknesses:** Smaller service catalog than AWS; fewer regions than AWS; Google's history of killing products creates enterprise trust issues; support tiers are expensive.
- **Team fit:** Data engineering and ML teams, Kubernetes specialists, Google-ecosystem companies.
- **Scale fit:** Petabyte analytics with BigQuery, global Kubernetes with GKE. Google-grade infrastructure.
- **Production risks:** GCP project quota limits hitting unexpectedly; BigQuery on-demand pricing surprises; GKE upgrades breaking workloads; networking VPC peering complexity.

---

## Azure

- **When to use:** Microsoft-stack enterprises (.NET, Active Directory, Office 365, Teams), regulated industries with Microsoft compliance requirements, companies with existing Microsoft EA agreements.
- **When NOT to use:** Startups without Microsoft tooling commitment; teams preferring open-source-first ecosystems; ML/data workloads (GCP/AWS are stronger here).
- **Strengths:** Best Active Directory/Entra integration, strong .NET support, hybrid cloud (Azure Arc), GitHub Actions native CI/CD, OpenAI partnership (Azure OpenAI Service).
- **Weaknesses:** Historically slower to release features vs. AWS; documentation quality inconsistent; pricing can be higher for comparable compute; UI complexity rivals AWS.
- **Team fit:** .NET/Microsoft shops, enterprise IT teams, companies using Microsoft 365 heavily.
- **Scale fit:** Enterprise-grade global scale, especially for hybrid (on-prem + cloud) workloads.
- **Production risks:** Azure AD conditional access misconfigurations; unexpected bandwidth costs; ARM template complexity; resource group permission sprawl.

---

## Cloudflare

- **When to use:** Edge compute (Workers), CDN, DDoS protection, DNS, R2 storage (S3-compatible, zero egress), bot management, API gateway at edge, globally distributed apps with latency requirements.
- **When NOT to use:** Primary compute for stateful, CPU-heavy workloads; teams needing full Linux environments; complex database-backed services (use as the edge layer, not the only layer).
- **Strengths:** 300+ PoPs globally, Workers run at edge with sub-millisecond cold start, R2 eliminates egress costs, D1 (SQLite at edge), KV and Durable Objects for state, generous free tier.
- **Weaknesses:** Workers have CPU time limits and no long-running processes; ecosystem smaller than AWS; Durable Objects global consistency has learning curve; vendor-specific APIs.
- **Team fit:** Frontend-leaning full-stack teams, teams building edge-first APIs, teams using Next.js/Remix deployed to edge.
- **Scale fit:** Global CDN scales infinitely. Workers handle millions of requests per second. D1/Durable Objects have limits for heavy stateful workloads.
- **Production risks:** CPU time limits killing long computations; KV eventual consistency causing stale reads; Workers bundle size limits; D1 in beta — not production-hardened for all workloads.

---

## Vercel

- **When to use:** Next.js, Nuxt, SvelteKit, Astro, or any modern frontend framework deployment. Best-in-class developer experience for frontend + serverless functions. Preview deployments per PR.
- **When NOT to use:** Pure backend APIs, long-running services, stateful workloads, cost-sensitive projects at scale (Vercel pricing is premium), teams needing full infrastructure control.
- **Strengths:** Zero-config deploys from Git, automatic preview URLs per branch, edge network (Vercel Edge Network), edge functions, image optimization, analytics built-in, first-class Next.js support.
- **Weaknesses:** Expensive at scale (serverless function invocations add up); function execution time limits; no persistent disk; limited to frontend + serverless paradigm; vendor lock-in risk.
- **Team fit:** Frontend and full-stack JS/TS teams, especially Next.js shops. Non-ideal for backend-heavy teams.
- **Scale fit:** Handles traffic spikes automatically. Costs become significant at high function invocation volume.
- **Production risks:** Unexpected bill spikes from function invocations; cold starts on infrequently used serverless functions; log retention limits; no WebSocket support in edge functions.

---

## Netlify

- **When to use:** Static sites, Jamstack architectures, sites with mostly CDN-served content + serverless functions, teams wanting Vercel-alternative with slightly more generous free tier.
- **When NOT to use:** Complex server-side rendering at scale, heavy serverless function workloads, teams needing advanced edge compute (use Cloudflare or Vercel Edge).
- **Strengths:** Excellent static site hosting, form handling built in, identity/auth service, split testing, deploy previews, Netlify Functions (Lambda under the hood), git-based workflows.
- **Weaknesses:** Function cold starts; less capable than Vercel for SSR-heavy Next.js; smaller ecosystem than Vercel; bandwidth limits on free/starter tiers.
- **Team fit:** Marketing teams, content sites, documentation sites, small-to-medium Jamstack projects.
- **Scale fit:** CDN scales well. Compute-heavy function workloads should move to dedicated backends.
- **Production risks:** Function timeout limits; bandwidth overage billing; deploy cache invalidation issues on large sites; limited observability compared to full cloud providers.

---

## Fly.io / Render

- **When to use:** Running containerized applications without Kubernetes complexity. Long-running servers, WebSockets, background workers, databases — anything that doesn't fit the serverless model.
- **When NOT to use:** Projects requiring the full AWS/GCP service catalog, compliance-heavy enterprise workloads, teams already invested in Kubernetes.
- **Strengths (Fly.io):** Deploy Docker containers globally near users, persistent volumes, private networking, Machines API for auto-scaling, competitive pricing vs. Heroku/Railway. Render is simpler but less flexible.
- **Weaknesses:** Smaller ecosystem than major clouds; fewer managed services; support response times vary; Fly.io has had reliability incidents; less enterprise trust than AWS/GCP/Azure.
- **Team fit:** Small-to-mid teams tired of serverless constraints. Good Heroku replacement. Backend API teams.
- **Scale fit:** Medium scale. Not designed for hyperscale workloads. Good for 0–100 RPS range, manageable to higher with care.
- **Production risks:** Fly.io volume reliability; cold VM startup latency; limited observability tooling vs. major clouds; egress pricing adds up.

---

## Docker + Kubernetes

- **When to use:** Large teams with complex microservices, teams needing workload portability across clouds, sophisticated autoscaling/rollout requirements, GPU workloads, on-premise deployments.
- **When NOT to use:** Small teams, early-stage startups, simple applications — operational complexity is enormous. If you can use a managed PaaS, do so.
- **Strengths:** Full control over infrastructure, workload portability, declarative configuration, rich ecosystem (Helm, Argo, Flux, Istio), supported by all major clouds (EKS, GKE, AKS).
- **Weaknesses:** High operational overhead (cluster upgrades, node management, networking complexity); steep learning curve; security hardening is non-trivial; overkill for most early-stage projects.
- **Team fit:** Platform/DevOps engineering teams, large organizations, companies with dedicated SRE capacity.
- **Scale fit:** Designed for large-scale workloads. Cluster autoscaler + HPA handle millions of requests.
- **Production risks:** Misconfigured RBAC; node pool exhaustion; etcd corruption; image pull failures blocking rollouts; PodDisruptionBudgets not set causing downtime during maintenance.

---

## Terraform / Pulumi

- **When to use:** Any team managing cloud infrastructure that will change over time. Infrastructure as Code is non-negotiable for teams beyond the hobby stage. Terraform is the default; Pulumi for teams preferring real languages over HCL.
- **When NOT to use:** Personal experiments, short-lived demos — but even then, getting into IaC habits early pays off. Never for one-click console operations on production without IaC.
- **Strengths (Terraform):** Declarative HCL, plan/apply workflow, state management, 3000+ providers, massive community, Terraform Cloud for remote state and collaboration.
- **Strengths (Pulumi):** TypeScript/Python/Go/C# — real programming languages, testable, loops and conditionals without HCL workarounds, same resource model as Terraform.
- **Weaknesses:** State file corruption risk; provider version drift; HCL complexity at scale (Terraform); Pulumi smaller community than Terraform.
- **Team fit:** All infrastructure teams. Terraform for ops-background teams; Pulumi for developer-background teams.
- **Scale fit:** Manages infrastructure of any size. Works on all major clouds.
- **Production risks:** State lock deadlocks; applying without plan review; destroying resources accidentally; secrets in state files; drift from manual console changes.

---

## GitHub Actions / GitLab CI

- **When to use:** CI/CD for any project. GitHub Actions is the default for GitHub-hosted repos. GitLab CI for self-hosted GitLab or teams preferring tighter SCM-CI integration.
- **When NOT to use:** Extremely complex multi-repo CI workflows requiring advanced orchestration (consider Jenkins, Buildkite, or Tekton); teams with strict self-hosted security requirements that preclude cloud runners.
- **Strengths (GitHub Actions):** Deep GitHub integration (PR checks, environments, secrets), large Actions marketplace, matrix builds, reusable workflows, free for public repos.
- **Strengths (GitLab CI):** YAML-based pipelines, DAG pipeline support, integrated container registry, excellent for monorepos, first-class self-hosted runners.
- **Weaknesses:** GitHub Actions YAML can become deeply complex; hosted runner minutes cost money at scale; secrets management is basic vs. Vault; GitLab CI YAML syntax is verbose.
- **Team fit:** All teams. GitHub Actions for GitHub users; GitLab CI for GitLab users. Circle CI and Buildkite are valid alternatives for large teams.
- **Scale fit:** Hosted runners auto-scale. Self-hosted runners for cost control at high volume.
- **Production risks:** Secrets exposed via `echo` or log output; missing branch protection allowing CI bypass; supply chain attacks via untrusted third-party Actions; runner exhaustion at peak times.

---

## Comparison Table

| Tool | Type | Ops Complexity | Vendor Lock-in | Cost at Scale | Best Fit |
|---|---|---|---|---|---|
| AWS | Full cloud | High | High | Variable | Any production system |
| GCP | Full cloud | High | Medium-High | Variable | ML/data, Kubernetes |
| Azure | Full cloud | High | High | Variable | Microsoft enterprises |
| Cloudflare | Edge/CDN/compute | Low | Medium | Low-Medium | Edge APIs, CDN, DDoS |
| Vercel | PaaS (frontend) | Very Low | High | High | Next.js, frontend SSR |
| Netlify | PaaS (static) | Very Low | Medium | Low-Medium | Jamstack, static sites |
| Fly.io/Render | PaaS (containers) | Low | Medium | Medium | Simple container apps |
| Docker + K8s | Self-managed | Very High | Low | Medium-High | Large microservices |
| Terraform/Pulumi | IaC | Medium | Low | Low (tooling) | All infra management |
| GH Actions/GitLab CI | CI/CD | Low-Medium | Medium | Low-Medium | All CI/CD pipelines |

---

## Recommended Combinations

- **AWS + Terraform + GitHub Actions** — Most common production stack. Terraform manages AWS resources, GitHub Actions deploys. Battle-tested and well-documented.
- **GCP + GKE + Terraform + GitHub Actions** — ML/data teams: GKE for services, BigQuery for analytics, Terraform for IaC. Strong ML toolchain.
- **Vercel + Supabase + Cloudflare (DNS/WAF)** — Fastest full-stack JS delivery: Vercel for frontend, Supabase for backend, Cloudflare for DNS, DDoS, and caching.
- **Fly.io + Terraform + GitHub Actions** — Simpler container workloads without Kubernetes overhead. Good Heroku replacement.
- **AWS + EKS + Terraform + ArgoCD** — GitOps pattern: Terraform provisions EKS, ArgoCD syncs Kubernetes manifests from Git. Suitable for platform teams.
- **Cloudflare Workers + R2 + D1** — Edge-first serverless: Workers compute, R2 storage (no egress), D1 SQLite. Zero-egress cost architecture.
- **Azure + AKS + Pulumi + GitLab CI** — Microsoft shops: Azure for compute/AD/OpenAI, AKS for Kubernetes, Pulumi (C#/.NET) for IaC, GitLab for SCM+CI.
- **AWS Lambda + API Gateway + DynamoDB + Terraform** — Pure serverless: no servers to manage, scales to zero, minimal ops. Terraform manages all resources.

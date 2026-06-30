# Secrets Management Stack Matrix

Secrets — API keys, database credentials, tokens, private keys, certificates — are a **hard constraint** in this system. Per `CLAUDE.md` §8, secrets must never be committed, printed, logged, or transmitted; they live in env/secret managers and are referenced, never revealed. This matrix exists to choose **where** secrets are stored and **how** they reach the workload, not whether to protect them. Choose by answering: (1) Where do workloads run — one cloud, multi-cloud, Kubernetes, or local/CI? (2) Do you need **static** secrets (stored values you rotate) or **dynamic** secrets (generated on demand, short-lived, auto-expiring)? (3) How important is rotation, audit logging, and lease/revocation? (4) Build-vs-buy and operational budget — running Vault yourself is real work; a cloud manager is a managed line item (a §6 decision).

Key decision drivers: workload location and identity model, static vs. dynamic secret needs, rotation and revocation, audit/compliance requirements, encryption-at-rest and KMS integration, GitOps compatibility, and operational overhead.

---

## Comparison Table

| Tool | Hosting | Static | Dynamic | Rotation | K8s fit | Lock-in | Best for |
|---|---|---|---|---|---|---|---|
| HashiCorp Vault | Self-host / HCP | Yes | Yes (DB, cloud, PKI) | Strong (leases) | Strong (agent/CSI) | Low (portable) | Multi-cloud, dynamic secrets, PKI |
| AWS Secrets Manager | AWS managed | Yes | Limited (RDS rotation) | Built-in (Lambda) | Via CSI/IRSA | High (AWS) | AWS-native workloads |
| GCP Secret Manager | GCP managed | Yes | No | Manual/scheduled | Via CSI/Workload Identity | High (GCP) | GCP-native workloads |
| Azure Key Vault | Azure managed | Yes | No | Built-in events | Via CSI | High (Azure) | Azure-native, certs/keys |
| SOPS | File-based (Git) | Yes | No | Manual | Decrypt in pipeline | Low | GitOps encrypted-in-repo |
| Doppler | SaaS | Yes | No | Manual/integration | Operator/sync | Medium | Multi-env sync, DX-first teams |
| Infisical | SaaS / self-host | Yes | Some (dynamic add-on) | Manual/scheduled | Operator/CSI | Low (open source) | Open-source self-host alt |
| Cloud KMS (envelope) | Managed | (keys, not secrets) | — | Key rotation | Via SDK | High (per cloud) | Encrypting the secrets themselves |

---

## HashiCorp Vault

- **When to use:** Multi-cloud or hybrid environments; when you need **dynamic secrets** (short-lived database credentials, cloud IAM creds, SSH certs generated per request) and a built-in PKI/certificate authority; strong lease/revocation and detailed audit are required.
- **When NOT to use:** A small team fully inside one cloud that only needs static secrets — a managed cloud manager is far less to operate. Self-hosting Vault HA (storage backend, unseal/auto-unseal, upgrades) is a real commitment.
- **Strengths:** Dynamic secrets with automatic expiry shrink the blast radius of any leak; pluggable secret engines (databases, AWS/GCP/Azure, PKI, Transit encryption-as-a-service); rich policy and identity (AppRole, Kubernetes auth, OIDC); thorough audit log; HCP Vault offers a managed tier.
- **Weaknesses:** Operational complexity (unseal, storage, HA, upgrades); steep learning curve; self-hosted means you own its uptime — and an unavailable Vault can mean an undeployable app.
- **Risks:** Sealed/unavailable Vault blocking deploys; root-token mishandling; over-broad policies; forgetting that Transit/PKI keys themselves need a backup/rotation plan.

---

## AWS / GCP / Azure secret managers

- **When to use:** Workloads that live entirely in one cloud. Lean on native workload identity (AWS IAM roles / IRSA, GCP Workload Identity, Azure Managed Identity) so apps fetch secrets with **no bootstrap secret at all**. AWS Secrets Manager for managed RDS rotation; Azure Key Vault when you also manage certificates and keys; GCP Secret Manager for simple, cheap versioned secrets.
- **When NOT to use:** Multi-cloud (you would run three different APIs); when you need rich dynamic secrets across many backends (Vault is stronger); GitOps-encrypted-in-repo workflows (use SOPS).
- **Strengths:** Zero ops; tight IAM integration and audit (CloudTrail / Cloud Audit Logs / Azure Monitor); encryption at rest via the cloud KMS; AWS/Azure offer built-in rotation hooks; versioning and fine-grained access policies.
- **Weaknesses:** Vendor lock-in (APIs and access models are not portable); dynamic-secret support is limited compared to Vault; per-secret/per-API-call cost adds up at scale.
- **Risks:** Over-permissive IAM granting broad `GetSecretValue`; cross-account/region access gaps; assuming rotation is automatic when it must be wired up (especially GCP, which has no built-in rotation execution).

---

## SOPS (Secrets OPerationS)

- **When to use:** GitOps workflows where you want secrets **encrypted in the repository** next to the config they belong to, decrypted only at deploy time. Pairs naturally with a cloud KMS, age, or PGP as the encryption key, and with Argo CD / Flux.
- **When NOT to use:** When you need runtime secret fetching, dynamic secrets, lease/revocation, or central audit of secret *access* (SOPS audits commits, not reads). High-churn secrets that rotate frequently are painful in Git.
- **Strengths:** Secrets version with code; no separate secret store to run; decryption keys held in KMS/age so the repo alone is useless to an attacker; great for declarative, reproducible infra.
- **Weaknesses:** Rotation is a manual re-encrypt-and-commit; access control is repo + KMS-key access, not per-secret; no concept of leases or dynamic generation.
- **Risks:** Committing the *decrypted* file by mistake; an over-shared KMS key effectively unlocking everything; encrypting the values but leaking key *names* and structure in the clear (often acceptable, but be deliberate).

---

## Doppler / Infisical

- **When to use:** Developer-experience-first teams that want one place to define secrets and **sync** them to many environments and targets (local `.env` injection, CI, cloud managers, Kubernetes) without copy-paste. Infisical when you want an open-source, self-hostable option; Doppler for a polished managed SaaS.
- **When NOT to use:** When introducing a third-party SaaS into the secret path is itself a compliance concern (evaluate the trust boundary); when a cloud-native manager already covers your single-cloud needs with less surface area.
- **Strengths:** Excellent multi-environment sync and injection (`doppler run`, Infisical CLI/operator); branching/versioning of secret sets; integrations with most platforms and CI; reduces `.env` sprawl; Infisical is open source and self-hostable to keep secrets in your boundary.
- **Weaknesses:** Adds a vendor to the critical path; dynamic-secret support is limited (Infisical has a growing dynamic feature, Doppler is mostly static); pricing scales with usage/seats.
- **Risks:** A service-token leak exposing a whole project's secrets; over-broad sync pushing prod secrets into low-trust environments; reliance on the SaaS being available at deploy time.

---

## Cloud KMS (envelope encryption)

- **When to use:** Not a secret *store* but the **key** that protects secrets. Use a managed KMS (AWS KMS, GCP Cloud KMS, Azure Key Vault keys) for envelope encryption — encrypt data keys with a KMS master key — and as the decryption key behind SOPS, Vault auto-unseal, or application-level field encryption.
- **When NOT to use:** As the place you store many small string secrets directly (use a secret manager); KMS is for cryptographic key custody, not credential storage.
- **Strengths:** Hardware-backed key custody (HSM-grade); automatic master-key rotation; fine-grained IAM on key usage; full audit of every encrypt/decrypt; never exposes raw key material.
- **Weaknesses:** Per-operation cost and latency; you still need something to manage the secrets themselves; cross-cloud key portability is poor.
- **Risks:** Deleting/disabling a key that still protects live data (often irreversible — schedule deletions); over-broad `kms:Decrypt` grants; region pinning of keys complicating DR.

---

## Static vs. dynamic secrets

- **Static secrets:** A stored value (a DB password, an API key) you read, use, and rotate periodically. Simplest and universally supported. The leak window is "until you notice and rotate," so rotation cadence matters.
- **Dynamic secrets:** Generated on demand with a short TTL and automatically revoked at lease end (Vault's database/cloud/SSH engines). A leaked dynamic credential is useless minutes later, dramatically shrinking blast radius. Prefer dynamic for high-value backends (databases, cloud IAM) when your store supports it.

---

## Rotation

- **Automate it.** Manual rotation is rarely done and silently rots. AWS Secrets Manager (rotation Lambdas) and Azure Key Vault (rotation + event notifications) automate it natively; Vault dynamic secrets sidestep rotation entirely by being short-lived.
- **Version, then cut over.** Rotation should publish a new version while the old still works, then flip consumers — never break live workloads mid-rotation.
- **Rotate on exposure.** Any suspected leak triggers immediate rotation — and per §8, the leak is recorded as an incident, never quietly papered over.

---

## Kubernetes: sealed-secrets and CSI

- **Sealed Secrets (Bitnami):** Encrypt a Secret into a `SealedSecret` CRD safe to commit to Git; an in-cluster controller decrypts it to a real Secret at apply time. Good fit for GitOps when you want encrypted-in-repo without external fetch at runtime.
- **External Secrets Operator / Secrets Store CSI Driver:** Sync or mount secrets from Vault/AWS/GCP/Azure into pods at runtime, so the secret of record stays in the external manager and is never committed. Preferred when a central manager already exists.
- **Never** rely on plain Kubernetes `Secret` objects as the security boundary — they are base64, not encrypted, unless etcd encryption-at-rest and RBAC are configured. Treat raw Secrets as a delivery mechanism, not a vault.

---

## Recommended combinations

- **AWS-only workloads:** AWS Secrets Manager + IRSA (no bootstrap secret) + KMS-backed encryption + Secrets Store CSI Driver for pods. Native rotation for RDS; least moving parts.
- **Multi-cloud / dynamic secrets:** HashiCorp Vault (HCP or self-hosted HA) with database + cloud + PKI engines, Kubernetes auth for workload identity, and KMS auto-unseal. Maximum control and shortest-lived credentials.
- **GitOps (Argo CD / Flux):** SOPS + cloud KMS (or age) for encrypted-in-repo config, or Sealed Secrets for the same with an in-cluster controller. Secrets version with the manifests that use them.
- **DX-first startup, many environments:** Doppler or self-hosted Infisical as the source of truth, syncing into CI and the cloud-native manager; keep prod isolated behind separate tokens.
- **Encryption substrate everywhere:** A managed cloud KMS underneath whichever store you pick — backing SOPS decryption, Vault auto-unseal, and application-level field encryption — so raw key material never leaves the HSM boundary.

Cross-reference: `CLAUDE.md` §8 (secrets are a hard constraint — never commit, print, or transmit; reference, never reveal), `.claude/checklists/security.md` (secret-scanning and access-control review), and `.claude/hooks/` (`secret-scan` blocks commits containing secrets) for mechanical enforcement.

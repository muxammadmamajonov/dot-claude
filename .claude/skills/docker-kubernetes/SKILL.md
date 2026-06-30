---
name: docker-kubernetes
description: >
  Activate when the project needs to containerize services with Docker, write
  Compose files for local development, or deploy to Kubernetes (k8s, k3s, EKS,
  GKE, AKS). Also activate when writing Dockerfiles, Helm charts, Kubernetes
  manifests, CI/CD pipelines that build/push images, or when diagnosing
  container runtime issues, CrashLoopBackOff, OOMKilled, or image pull errors.
---

# Docker & Kubernetes Skill

## When to use

- Writing or optimizing Dockerfiles for any language/runtime (Node, Python, Go, Java, Rust, …)
- Composing multi-service local development environments with `docker compose`
- Writing Kubernetes Deployment, Service, ConfigMap, Secret, Ingress, HPA, and PodDisruptionBudget manifests
- Designing Helm charts for reusable, environment-parameterized deployments
- Setting up CI/CD pipelines that build, tag, scan, and push images to a registry
- Diagnosing `CrashLoopBackOff`, `OOMKilled`, `ImagePullBackOff`, pending pods, or resource quota violations
- Hardening containers for production (non-root user, read-only filesystem, seccomp, network policies)

---

## Workflow

### Docker

1. **Start from a minimal, pinned base image** — use official images with an exact version tag (e.g. `node:22.4-alpine3.20`), never `latest`.
2. **Layer order matters for cache efficiency** — copy dependency manifests first, install dependencies, then copy source code. This keeps the expensive install layer cached when only source files change.
3. **Use multi-stage builds** — one stage to compile/build, a second minimal stage to ship. The final image should contain only the runtime artifact and its direct OS dependencies.
4. **Set a non-root user** — add `RUN addgroup -S app && adduser -S app -G app` and `USER app` before the final `CMD`.
5. **Write a `.dockerignore`** — exclude `.git`, `node_modules`, `dist`, `.env*`, test files, and any secrets.
6. **Use `COPY --chown=app:app`** instead of a separate `RUN chown` to avoid creating an extra layer.
7. **Scan the image** — run `docker scout cves <image>` or `trivy image <image>` in CI before pushing.
8. **Publish a health check** — `HEALTHCHECK CMD curl -f http://localhost:8080/health || exit 1`.

### Kubernetes

1. **Namespace everything** — never deploy application workloads to `default`; create per-environment namespaces (`app-prod`, `app-staging`).
2. **Set resource requests and limits on every container** — without requests, the scheduler cannot bin-pack correctly; without limits, a runaway process can evict neighbours.
3. **Use Deployments, not bare Pods** — Deployments provide rolling updates, rollback, and self-healing.
4. **Configure liveness and readiness probes** — readiness gates traffic; liveness restarts a stuck container. Do not share the same endpoint for both.
5. **Use ConfigMaps for non-secret config; Secrets for credentials** — mount as environment variables or volume files; never bake secrets into the image.
6. **Set `replicas: 2` minimum for production** and add a PodDisruptionBudget (`minAvailable: 1`) to survive node maintenance.
7. **Use HorizontalPodAutoscaler** tied to CPU/memory or custom metrics for variable-load services.
8. **Apply NetworkPolicies** — default-deny all ingress/egress within a namespace, then explicitly allow only required paths.
9. **Roll out with `kubectl rollout`** — use `--record` is deprecated; instead annotate with `kubectl annotate deployment/<name> kubernetes.io/change-cause="<reason>"`.
10. **Drain and verify before deleting nodes** — `kubectl drain <node> --ignore-daemonsets --delete-emptydir-data`.

---

## Standards

### Do
- Pin base image digests (`FROM node:22.4-alpine3.20@sha256:<digest>`) in production Dockerfiles for reproducible builds.
- Use `ENTRYPOINT ["executable"]` + `CMD ["arg1"]` (exec form, not shell form) to ensure signals propagate correctly to PID 1.
- Label images with `org.opencontainers.image.*` labels (source, revision, created) for traceability.
- Store Kubernetes manifests in version control alongside application code (`deploy/k8s/` or a separate gitops repo).
- Use Helm `values.yaml` for environment-specific overrides; keep secrets out of `values.yaml` — inject via `helm upgrade --set-string` from CI secrets or an external secrets operator.
- Set `imagePullPolicy: Always` for mutable tags in development; use `IfNotPresent` with immutable SHA-tagged images in production.

### Do not
- Do not run containers as root in production.
- Do not use `CMD` with shell form (`CMD npm start`) — signals like SIGTERM are not forwarded to the Node process.
- Do not embed `.env` files or credentials in Docker images at any build stage.
- Do not use `docker run` with `--privileged` unless the workload explicitly requires it (e.g., a container runtime within a container).
- Do not `kubectl apply -f -` directly to production without a review step; use a GitOps controller (Argo CD, Flux) or a manual approval gate in CI.
- Do not set CPU limits below what the runtime's JIT or GC needs — Java/Node cold starts spike CPU and will be throttled into extreme slowness.
- Do not store state in a Deployment pod's local filesystem — use PersistentVolumeClaims or external storage for anything that must survive a pod restart.

---

## Common mistakes to avoid

| Mistake | Consequence | Fix |
|---|---|---|
| `FROM node:latest` | Non-reproducible builds; surprise breaking changes | Pin to `node:22.4-alpine3.20` |
| Copying `node_modules` into the image before `npm ci` | Installs host OS binaries into Linux container | `.dockerignore` excludes `node_modules`; install inside the build stage |
| No `USER` directive | Process runs as root; container escape has host impact | Add non-root user in Dockerfile |
| No resource `requests`/`limits` in k8s | Scheduler over-provisions nodes; OOMKilled under load | Always set both in every container spec |
| `CrashLoopBackOff` on startup | Missing env var, wrong entrypoint, or failing health check | `kubectl logs <pod> --previous` + `kubectl describe pod <pod>` |
| Readiness probe on a slow-starting service | Pod killed before it finishes init | Set `initialDelaySeconds` ≥ worst-case startup time |
| Storing secrets in ConfigMap | Secrets readable by anyone with ConfigMap list access | Use `kind: Secret` + seal with Sealed Secrets or External Secrets Operator |
| `imagePullPolicy: Always` with a SHA-tagged image in prod | Unnecessary registry round-trips on every pod start | Use `IfNotPresent` when images are tagged with immutable SHAs |

---

## Output format

Minimal production Dockerfile (Node example):
```dockerfile
# syntax=docker/dockerfile:1
FROM node:22.4-alpine3.20 AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

FROM node:22.4-alpine3.20 AS runner
RUN addgroup -S app && adduser -S app -G app
WORKDIR /app
COPY --from=deps --chown=app:app /app/node_modules ./node_modules
COPY --chown=app:app . .
USER app
EXPOSE 8080
HEALTHCHECK CMD wget -qO- http://localhost:8080/health || exit 1
ENTRYPOINT ["node"]
CMD ["dist/server.js"]
```

Kubernetes Deployment snippet:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  namespace: app-prod
spec:
  replicas: 2
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
      containers:
        - name: api
          image: registry.example.com/api:sha256-abc123
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 20
          envFrom:
            - configMapRef:
                name: api-config
          env:
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: api-secrets
                  key: db_password
```

---

## Related checklists
- `.claude/checklists/devops.md`
- `.claude/checklists/security.md`
- `.claude/checklists/launch.md`
- `.claude/checklists/performance.md`

## Related agents
- `.claude/agents/engineering/infrastructure-engineer.md`
- `.claude/agents/engineering/backend-engineer.md`
- `.claude/agents/quality/security-auditor.md`
- `.claude/agents/core/orchestrator.md`

# Feature Flags Stack Matrix

Feature flags decouple **deploy** from **release**: code ships dark, then a flag turns it on for some or all users without a redeploy. They enable gradual rollout, instant kill-switches, A/B experiments, entitlement gating, and trunk-based development. They also create **flag debt** — every flag is a permanent branch in your control flow until someone removes it. Choose by answering: (1) Do you need a managed platform with targeting and experimentation, or a lightweight open-source toggle service? (2) **Build-time** config (baked into the build, fast and simple, redeploy to change) or **runtime** flags (evaluated live, changeable instantly)? (3) Do flags drive real experiments (need statistics) or just operational rollout/kill-switches? (4) Self-host vs. SaaS, and how much do you care about vendor lock-in — mitigated by the **OpenFeature** standard.

Key decision drivers: targeting sophistication, experimentation/stats needs, evaluation latency (edge vs. server vs. client), self-host vs. SaaS, audit/governance, and lock-in tolerance.

---

## Comparison Table

| Tool | Hosting | Targeting | Experimentation | OpenFeature | Lock-in | Best for |
|---|---|---|---|---|---|---|
| LaunchDarkly | SaaS (managed) | Excellent | Add-on / strong | Provider | High | Enterprise rollout + governance |
| Unleash | Self-host / SaaS | Good | Basic (via add-ons) | Provider | Low (OSS) | Self-hosted, privacy-sensitive |
| Flagsmith | Self-host / SaaS | Good | Basic A/B | Provider | Low (OSS) | OSS with remote config |
| Statsig | SaaS | Good | Best-in-class stats | Provider | Medium | Experimentation-led teams |
| GrowthBook | Self-host / SaaS | Good | Strong (warehouse-native) | Provider | Low (OSS) | Warehouse-native experiments |
| OpenFeature | Spec / SDK | (delegated) | (delegated) | The standard | None | Vendor-neutral abstraction |

---

## LaunchDarkly

- **When to use:** Enterprise teams that need sophisticated targeting (by user attribute, segment, percentage), strong governance (approvals, audit log, role-based access), and reliable global flag delivery. The most mature managed platform.
- **When NOT to use:** Cost-sensitive small teams or projects that need only a handful of toggles; organisations that cannot send evaluation context to a third-party SaaS for data-residency reasons (consider self-hosted Unleash/Flagsmith).
- **Strengths:** Best-in-class targeting and segmentation; instant flag changes via a streaming SDK; robust SDKs across every platform (server, client, edge, mobile); approval workflows, audit, and flag governance; experimentation add-on.
- **Weaknesses:** Expensive and priced by seats/MAUs; SaaS-only (your evaluation context leaves your boundary unless using server-side eval); can become a single vendor you are deeply coupled to (mitigate with OpenFeature).
- **Risks:** Flag-change blast radius without approvals enabled; SDK initialisation failures needing safe defaults; cost surprises as MAU grows.

---

## Unleash

- **When to use:** Teams that want a proven **open-source, self-hostable** flag service to keep evaluation data inside their own infrastructure, with a clean activation-strategy model (gradual rollout, by-segment, by-host).
- **When NOT to use:** When you need turnkey, statistically-rigorous experimentation out of the box (Statsig/GrowthBook are stronger); when you do not want to operate the service (a managed SaaS tier exists but then you weigh cost vs. cloud managers).
- **Strengths:** Mature OSS with a strong activation-strategy abstraction; self-host for full data control; good SDK coverage; commercial Unleash tier adds enterprise governance; OpenFeature provider available.
- **Weaknesses:** Experimentation/analytics are basic without add-ons; you operate and scale the server yourself when self-hosting; UI/governance less polished than LaunchDarkly.
- **Risks:** Self-hosted availability becoming a release dependency; client-side SDKs exposing flag config if misconfigured; rollout strategy mistakes affecting the wrong cohort.

---

## Flagsmith

- **When to use:** Teams wanting an open-source platform that combines **feature flags with remote config** (typed values, not just on/off), self-hostable, with multi-environment support and per-identity overrides.
- **When NOT to use:** Heavy experimentation programmes needing deep statistics; ultra-low-latency edge evaluation at massive scale without extra caching.
- **Strengths:** Flags + remote config in one tool; open source and self-hostable; clean per-environment and per-identity targeting; OpenFeature provider; reasonable managed tier.
- **Weaknesses:** Smaller ecosystem than LaunchDarkly; experimentation is basic; advanced targeting less granular than the market leader.
- **Risks:** Identity/trait sprawl complicating targeting; relying on client-side evaluation for sensitive gates; self-host scaling under high SDK poll volume.

---

## Statsig

- **When to use:** Product teams whose primary goal is **experimentation** — A/B/n tests with trustworthy statistics (CUPED, sequential testing, guardrail metrics) — where flags and experiments are one workflow. Strong when product decisions are data-driven.
- **When NOT to use:** When you only need operational toggles/kill-switches (simpler tools suffice); strict self-hosting requirements (Statsig is SaaS, though it offers a warehouse-native mode).
- **Strengths:** Rigorous, fast experimentation analytics; generous free tier; flags, experiments, and metrics unified; warehouse-native option to compute results on your own data warehouse; OpenFeature provider.
- **Weaknesses:** SaaS-centric; experimentation depth is overkill if you just need toggles; learning curve for the statistical features.
- **Risks:** Misreading underpowered experiments; metric/event instrumentation gaps invalidating results; coupling product analytics to a single vendor.

---

## GrowthBook

- **When to use:** Teams that want **open-source, warehouse-native experimentation** — GrowthBook reads results straight from your data warehouse (Snowflake/BigQuery/etc.) so experiment data never leaves your stack — plus feature flags with a self-hostable backend.
- **When NOT to use:** When you have no data warehouse to compute experiment results against; when you need the polish and global SDK delivery network of a large managed vendor.
- **Strengths:** Warehouse-native (your data stays put); open source and self-hostable; solid stats engine (Bayesian and frequentist); flags + experiments together; OpenFeature provider.
- **Weaknesses:** Requires a warehouse and event pipeline to be useful for experiments; you operate it when self-hosting; SDK edge-delivery less turnkey than SaaS leaders.
- **Risks:** Garbage-in metrics from a weak event pipeline; warehouse query cost for frequent result recomputation; self-host scaling.

---

## OpenFeature (the standard)

- **When to use:** **Always consider it as the abstraction layer**, whatever backend you pick. OpenFeature is a CNCF vendor-neutral API/SDK spec for flag evaluation; you code against its interface and plug in a *provider* (LaunchDarkly, Unleash, Flagsmith, Statsig, GrowthBook, or a custom one).
- **When NOT to use:** Trivial projects with one or two build-time toggles where any abstraction is overkill.
- **Strengths:** Decouples application code from the vendor, so swapping providers does not mean rewriting evaluation calls; consistent flag-evaluation API across languages; hooks for logging/telemetry; growing provider ecosystem.
- **Weaknesses:** It is an interface, not a backend — you still choose and run/buy a provider; advanced vendor-specific features may not be fully exposed through the standard API.
- **Risks:** Leaning on provider-specific escape hatches that re-introduce lock-in; assuming the abstraction removes the need for safe-default handling (it does not).

---

## Kill-switches

A kill-switch is a flag whose only job is to disable a feature instantly when it misbehaves in production — no redeploy, no rollback of code. Make them **runtime**, default-safe (a failure to evaluate must fail to *off*/safe), and fast to flip. Every risky new feature should ship behind one. Kill-switches are an operational safety control and pair directly with rollback (`.claude/checklists/release-rollback.md`).

---

## Gradual rollout

Release to 1% → 5% → 25% → 100%, watching error rates and key metrics at each step; halt or roll back via the flag if a stage regresses. Target by stable bucketing (hash of user ID) so a user's experience does not flicker between requests. Combine with canary deploys: the flag controls *who* sees the feature, the deploy controls *where* the code runs.

---

## Flag debt

Every flag is a permanent fork in control flow and a testing-matrix multiplier (N flags → up to 2^N code paths). Untracked, flags accumulate until no one knows which are safe to remove. Discipline:

- Give each flag an **owner**, a **purpose**, and an **expiry/cleanup date** at creation.
- Distinguish **transient** flags (rollout/experiment — delete after the decision) from **permanent** flags (entitlement/ops kill-switches — keep, but document).
- Schedule stale-flag cleanup; treat a flag whose decision is made but code path lingers as debt to pay down.
- Never let a half-removed flag leave a dead branch — removal means deleting the branch, not just defaulting it.

---

## Build-time vs. runtime config

- **Build-time (compile/env config):** Baked into the artifact; changing it requires a rebuild/redeploy. Fastest at runtime, zero external dependency, no eval latency — but no instant kill-switch and no per-user targeting. Good for static, environment-level switches.
- **Runtime flags:** Evaluated live against a flag service/SDK; changeable in seconds without deploy; support targeting, gradual rollout, and kill-switches — at the cost of an SDK dependency, evaluation latency, and the need for **safe defaults** when the service is unreachable. Required for anything you must be able to turn off in production immediately.

---

## Recommended combinations

- **Vendor-neutral default:** OpenFeature SDK + your chosen provider (LaunchDarkly, Unleash, Flagsmith, Statsig, or GrowthBook). Code once against the standard; swap backends without touching evaluation calls.
- **Enterprise rollout + governance:** LaunchDarkly (behind OpenFeature) with approval workflows, audit log, and kill-switches for every risky feature.
- **Privacy-sensitive / self-hosted:** Unleash or Flagsmith self-hosted, keeping evaluation context inside your infrastructure; OpenFeature on top for portability.
- **Experimentation-led product:** Statsig (SaaS) or GrowthBook (warehouse-native, self-host) for flags + rigorous A/B stats in one workflow; pipe events from your analytics stack.
- **Operational safety baseline:** Even with build-time config for static settings, add a small runtime kill-switch layer (any provider) so every production feature can be disabled instantly without a deploy.

Cross-reference: `.claude/checklists/release-rollback.md` (kill-switches and gradual rollout as rollback mechanisms), `.claude/stack-matrix/analytics.md` (event pipeline feeding experimentation), and `CLAUDE.md` §5.9 / §9 (reversible-by-default — a flag-gated feature is reversible by flipping the flag).

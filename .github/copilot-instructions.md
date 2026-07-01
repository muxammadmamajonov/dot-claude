<!-- DO NOT EDIT — generated from .claude/ by .claude/scripts/generate_adapters.py. Edit .claude/ and re-run. -->

# Copilot instructions — Universal .claude AI Project OS

This repository uses the **Universal .claude AI Project Operating System**. The authoritative rules are in
`.claude/CLAUDE.md` (the constitution) with the cross-tool entry point in `AGENTS.md` — follow them.

## Operating rules
- 9-stage flow: classify → interview → select → spec → build (small safe phases) → audit (security/QA/performance/accessibility) → readiness → launch → continue. Coding is stage 5; understand first. Pick the team via .claude/orchestration/routing-matrix.md.
- Safety spine (always): read before write; least privilege & least blast radius; never expose secrets (reference, never reveal); human-in-the-loop for anything irreversible; headless/scheduled runs are read/review-only by default; never assume an MCP server exists; document the why. Full rules: .claude/CLAUDE.md §8.
- Specs precede code. Write small, safe, reversible changes. Record assumptions and decisions under `docs/`.
- Quality gates are non-optional: security, QA, performance, accessibility (`.claude/checklists/*`, tagged P0–P3).

## How to use the system here
- Pick the team/checklists for a task via `.claude/orchestration/routing-matrix.md` (and the web/mobile/desktop layers).
- Apply `.claude/skills/<name>/SKILL.md` as procedures; treat `.claude/agents/*` as role briefs and
  `.claude/commands/*` as runnable workflows (reproduce their steps with Copilot).
- Never fabricate test results — run the real command or say it's unverified.

Available skills: ai-ml, analytics, api-design, architecture, aws, azure, backend, blockchain, browser-extension, cli, clickhouse, cloudflare, data-modeling, data-platform, desktop, devops, discovery, docker-kubernetes, documentation, dotnet, firebase, flutter, game, gcp, go-backend, godot, headless-automation, iot-embedded, java-spring, mcp-integration, memory-management, messaging-queues, mobile, mongodb, mysql, native-android, native-ios, node-backend, observability, payments, performance, php-laravel, postgres, production-readiness, project-classification, python-backend, react-native, react-next, realtime, redis, requirements-engineering, routine-authoring, ruby-rails, rust-backend, search, security, stack-selection, supabase, terminal-operations, testing, ui-ux-design, unity, unreal, vue-nuxt, web.

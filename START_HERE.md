# Start Here — 5-Minute Quickstart

This is a reusable `.claude/` system that turns Claude Code into a careful, senior project team for **any** software project — web, mobile, desktop, game, backend/API, CLI, AI agent, data platform, and more. You bring the idea and the business decisions; the system handles the classify → understand → spec → build → audit → launch flow safely, asking you only when something truly matters.

It's for builders of any skill level — you don't need to be technical to start. The golden rule: **it never jumps straight to coding.** It understands what you're building first, writes a plan you approve, then builds in small, safe steps.

---

## The fastest path (3 steps)

1. **Copy `.claude/` into your project.** Drop the entire `.claude/` folder into your project's root (alongside `package.json`, `README`, your source, etc.). Starting from scratch? Make an empty folder and paste `.claude/` inside.

2. **Open Claude Code in that folder.**
   ```
   cd path/to/your-project
   claude
   ```
   It automatically reads `.claude/`, so it already knows the rules of this system.

3. **Run the front-door command:**
   ```
   /start-project        # new project — classify + interview, then guide you through
   /brainstorm-project   # idea still fuzzy? shape it first, then /start-project
   /continue-work        # existing codebase — resume at the right stage
   ```

That's it. Answer the questions in plain language and let the system drive.

---

## The 9-stage flow (copy-pasteable)

The whole journey as a command sequence. The orchestrator runs most of these for you, but you can drive each step yourself:

```
/start-project         # 1–2  Classify the project + interview you on what matters
/route                 # 3    Assemble the minimal team of agents for this project
/create-specs          # 4    Write the product + technical specs (you approve them)
/design-architecture   # 4    Define components, data flow, and the security model
/implement-feature     # 5    Build in small, safe phases
                       #      (/build-prototype first, for the walking skeleton)
/audit-security        # 6    Security gate (also covers QA + accessibility)
/audit-production      # 7    Readiness: backups, monitoring, rollback, runbooks
/prepare-launch        # 8    Build and execute the staged launch plan
/continue-work         # 9    After launch — next features, same safe loop
```

Need performance too? Add `/audit-performance` in the audit stage.

---

## What happens

- **Classify** — the system detects what kind of product you're building, so questions and the plan are tailored to *your* project.
- **Understand** — a short interview covering only **business-critical** decisions (who it's for, what success looks like, hard requirements, deal-breakers). It decides the technical plumbing itself and writes every assumption down for you to review.
- **Spec** — a written plan you approve *before* any code is written. Nothing gets built until you say "looks good."
- **Build in safe phases** — it starts with a "walking skeleton" (the thinnest end-to-end version where your one core journey actually works), then layers on features one small, reversible slice at a time.
- **Audit** — security, QA, performance, and accessibility gates run against checklists, ranked by importance.
- **Launch** — a go-live readiness review (backups, monitoring, rollback) and a staged plan you sign off on.

If a plan or build ever looks wrong, just say so in plain words — the system adjusts and can step back. Your specs and progress are saved as files, so you can pause and pick up anytime.

---

## Going further

- **README.md** — what this system is and the big picture.
- **PROJECT_OS.md** — the full architecture: agents, skills, presets, checklists, and how the 9-stage flow fits together.
- **SECURITY.md** — the safety model and how the always-on guards work.
- **`.claude/docs/`** — deeper guides on the operating capabilities (terminal, memory, commands, skills, MCP, subagents, hooks, headless, routines). Start with `CLAUDE_CODE_OPERATING_MODEL.md`, then dip into `MCP_STRATEGY.md`, `MEMORY_STRATEGY.md`, `SUBAGENT_ORCHESTRATION.md`, `HEADLESS_AND_ROUTINES.md`, and `HOOKS_SAFETY_MODEL.md` as needed.

You don't need any of these to ship your first prototype.

---

**Safe by default.** The system refuses destructive or irreversible actions (deleting data, force-pushing, dropping databases) without your explicit approval, and it never exposes secrets — it references them, never reveals them. When in doubt, ask "is this safe and reversible?"

Start at step 1, take it one step at a time, and let the system do the heavy lifting while you make the calls that matter.

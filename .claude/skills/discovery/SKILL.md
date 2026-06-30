---
name: discovery
description: Run founder/business discovery at the very start of any new project (or a major new module) before any specs or code exist. Activate when the user wants to "start a project", "scope an idea", "kick off discovery", or when requirements are vague and business context is missing. Produces the discovery-answers artifact that every later phase depends on.
---

# Discovery (Founder & Business Interview)

## When to use
- A new project is being initiated and there is no written business context, or context is thin/contradictory.
- A major new product line, module, or pivot needs its own business framing.
- Before classification, requirements, architecture, or any build work — discovery feeds all of them.
- Skip only when a complete, signed-off discovery artifact already exists; if so, review and update it instead.

## Workflow
1. **Set the frame (1 message).** Tell the user you will ask a focused set of business questions, that you will record assumptions where they cannot answer, and that nothing will be built until specs are approved. Reference the safe flow in `.claude/agents/core/orchestrator.md`.
2. **Interview in rounds, not one giant dump.** Ask 3–6 questions per round, grouped by theme. Wait for answers before the next round. Cover, in order:
   - **Problem & outcome** — What problem, for whom, and what does success look like in 6–12 months? What happens if nothing is built?
   - **Users & stakeholders** — Primary users, secondary users, buyers vs. users, internal operators, regulators.
   - **Value & business model** — How does this create or capture value (revenue, savings, compliance, strategic)? Free/paid/internal?
   - **Scope & MVP** — Must-have vs. nice-to-have for the first usable release. What is explicitly out of scope for v1?
   - **Constraints** — Budget ceiling, hard deadline, team size/skills, mandated stack, existing systems to integrate, hosting/region limits.
   - **Compliance & data** — Personal data, payments, health, financial, children's data, jurisdictions (GDPR, HIPAA, PCI-DSS, SOC 2, etc.).
   - **Risk & failure modes** — What must never happen (data loss, downtime, mis-payment, safety)? Who is harmed if it fails?
   - **Existing assets** — Current code, brand, designs, data, contracts, prior attempts.
   - **Success metrics** — Quantified targets (users, latency, conversion, uptime, cost per unit).
3. **Probe for the business-critical decisions only.** Do not ask the user about implementation details they don't care about; record those as assumptions instead. Escalate to the user only when a choice changes cost, legal exposure, timeline, or core scope.
4. **Record everything as you go** into `.claude/templates/discovery-answers.md` (copy the template into the project's working docs, e.g. `docs/discovery.md`). Fill every field; mark unknowns explicitly as `ASSUMPTION:` or `OPEN QUESTION:` with an owner.
5. **Reflect back a summary.** Restate the problem, target users, MVP scope, top 3 constraints, and top 3 risks in your own words. Ask the user to confirm or correct. Resolve contradictions before proceeding.
6. **Lock and hand off.** Mark the artifact `Status: confirmed` with date and version. Hand off to `.claude/skills/project-classification/SKILL.md` for typing, then `.claude/skills/requirements-engineering/SKILL.md`.

## Standards
- **Do** ask open questions first ("walk me through…"), then closed questions to pin down specifics.
- **Do** quantify everything you can: turn "fast" into a number, "secure" into named standards, "soon" into a date.
- **Do** separate facts (stated by user), assumptions (your inference), and decisions (agreed choices) visually in the artifact.
- **Do** keep business framing technology-agnostic — no stack talk in discovery.
- **Do not** propose architectures, frameworks, or schemas here; that is later work.
- **Do not** invent data the user can confirm — ask. Invent only where the user is unavailable, and label it.
- **Do not** proceed to specs while a contradiction or a business-critical OPEN QUESTION is unresolved.

## Common mistakes to avoid
- Treating every project as a web app and asking web-only questions (skips mobile/CLI/embedded/agent realities).
- Asking 30 questions at once — the user disengages and answers shallowly.
- Letting "we'll figure it out later" hide a compliance or payments requirement that reshapes the whole project.
- Capturing answers only in chat; if it is not in the artifact, it is lost.
- Confusing the buyer's goals with the end user's goals when they differ.
- Skipping the "what must never happen" question — it is the seed of the security and QA checklists.

## Output format
A completed `.claude/templates/discovery-answers.md` saved into the project (e.g. `docs/discovery.md`), with: project one-liner, problem statement, target users/personas, value/business model, MVP scope and explicit non-goals, constraints table, compliance/data-sensitivity flags, risk register seed, success metrics, and a clearly separated Facts / Assumptions / Decisions / Open Questions structure. Header carries `Status`, `Owner`, `Date`, `Version`.

## Related checklists
- `.claude/checklists/discovery.md`
- `.claude/checklists/security.md` (data-sensitivity flags feed this)
- `.claude/checklists/production.md`

## Related agents
- `.claude/agents/core/orchestrator.md`
- `.claude/agents/core/business-analyst.md`
- `.claude/agents/core/product-manager.md`

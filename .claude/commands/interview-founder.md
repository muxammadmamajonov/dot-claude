---
description: Run founder/business discovery and record answers as structured context
argument-hint: [optional focus area, e.g. "monetisation" or "compliance"]
---

# /interview-founder

## Purpose
Conduct a structured discovery conversation with the founder or product owner. Extract the problem statement, target users, value proposition, constraints, success metrics, risks, budget, and timeline. Record everything in a canonical discovery document so all subsequent agents work from the same ground truth.

## When to use
- As Phase 2 of `/start-project`, immediately after `/classify-project`.
- Standalone when returning to a project after a scope change.
- When onboarding a new agent onto an existing project that lacks a discovery record.

## Workflow

### Step 1 — Load context
1. Read `docs/state/project-type.md` if it exists. Extract the primary type and any compliance/cross-cutting concerns — these shape which questions to ask.
2. Check whether `docs/context/discovery-answers.md` already exists. If it does, load it and present the existing answers before asking new questions. Ask: "These are the answers we recorded previously. Would you like to update any of them, or continue from where we left off?"

### Step 2 — Core interview (ask all; wait for answer before next)
Ask each question sequentially. Do not batch them — one question at a time so the user can think.

**Block A — Problem & value**
- Q1: "What specific problem does this solve? Who suffers from it today and how?"
- Q2: "Why hasn't this been solved well already? What is the key insight that makes your approach different?"
- Q3: "Who are the primary users? Describe them concretely — role, industry, technical level, device, location."
- Q4: "What does success look like for a user in their first week? Their first month?"

**Block B — Business model & constraints**
- Q5: "How does the project make money, or what value does it deliver to the organisation funding it?"
- Q6: "Are there any hard technology, vendor, or legal constraints we cannot violate? (existing infra, approved vendor lists, data residency laws, regulated industry standards)"
- Q7: "What is the approximate budget and team size available for the build phase?"
- Q8: "What is the target launch date, and are there external deadlines (regulatory filing, contract, event) that are immovable?"

**Block C — Metrics & risks**
- Q9: "What are the three most important metrics that will tell you the project is working? Give a target value for each."
- Q10: "What are the two or three things most likely to kill this project? What would trigger you to stop?"
- Q11: "Who are the main stakeholders who must approve the launch? What are their approval criteria?"

**Block D — Type-specific questions** (ask only the block matching the primary type from project-type.md)

| Primary type | Additional questions |
|-------------|---------------------|
| WEB / MOB / DSK | "What browsers, OS versions, or device form factors must be supported? What is the acceptable load time on a median connection?" |
| API | "Who are the API consumers? Internal teams, third-party developers, or both? What SLA (uptime, latency p99) is required?" |
| AGT | "What LLM providers are approved? What is the acceptable cost per conversation? How will hallucinations be detected and handled?" |
| BLK | "Which chain(s)? Mainnet launch or testnet first? Who audits the contracts?" |
| SAS | "How many tenants at launch? What is the tenant isolation model — shared DB, schema-per-tenant, or DB-per-tenant?" |
| FIN | "Which regulatory frameworks apply (PSD2, FinCEN, MiCA)? Is there an existing compliance team or external counsel?" |
| IOT / EMB | "What hardware platform and RTOS? What are the memory and flash constraints? How are firmware updates delivered?" |
| DAT | "What are the source systems? What is the acceptable data freshness (realtime, hourly, daily)? Who are the data consumers?" |

### Step 3 — Clarify and confirm
3. After all questions are answered, read back a condensed summary of the key decisions.
4. **STOP.** Ask: "Does this summary accurately capture your vision? Any corrections or additions before we lock in the discovery record?"
5. Incorporate any corrections.

### Step 4 — Write output
6. Write `docs/context/discovery-answers.md` using the template at `.claude/templates/discovery-answers.md`. Include:
   - All answers verbatim (lightly formatted).
   - A `[DECISION NEEDED]` marker for any question the user deferred or answered ambiguously.
   - A `Constraints` section listing all hard constraints extracted from Block B.
   - A `Metrics` section with the three KPIs and their targets.
   - A `Risks` section with the kill-switch conditions.
7. Do NOT write any spec, stack, or architecture files at this stage — discovery is input only.

## Agents used
None — this command runs inline as a conversation.

## Skills used
None at this phase. Compliance flags identified here are passed forward to `.claude/skills/security/SKILL.md` during spec creation.

## Expected outputs
| Path | Description |
|------|-------------|
| `docs/context/discovery-answers.md` | Structured discovery record with all answers, constraints, KPIs, and risks |

## Stop conditions
- Fewer than 8 of the 11 core questions are answered — do not write the output file; note which are missing and ask the user to complete them.
- A critical constraint (legal, regulatory, data-residency) is identified but the user cannot confirm details — add a `[DECISION NEEDED: legal review required]` marker and flag it in the final report.
- The user says the project is already built and only needs documentation — switch to audit mode: read existing code and infer answers where possible, then confirm with the user.

## Final report format
```
## /interview-founder — Discovery Complete

**Problem:** <one sentence>
**Primary users:** <description>
**Business model:** <one sentence>
**Hard constraints:** <list>
**KPIs:**
  1. <metric> → target: <value>
  2. <metric> → target: <value>
  3. <metric> → target: <value>
**Top risks:** <list>
**Launch deadline:** <date or "not fixed">
**Open decisions:** <count and list of [DECISION NEEDED] markers>

**Output:** docs/context/discovery-answers.md
**Next step:** /create-specs
```

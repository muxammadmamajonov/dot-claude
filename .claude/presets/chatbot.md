# Chatbot / Conversational Assistant Preset

## Project type

A **conversational assistant** that holds a multi-turn dialogue with a human across one or more channels to answer questions, complete tasks, or route the user to the right place. This covers customer-support bots, FAQ/help assistants, lead-qualification bots, internal-helpdesk assistants, booking/order assistants, and voice/IVR assistants. The bot may be rule/intent-driven, retrieval-augmented (RAG over a knowledge base), LLM-driven, or a hybrid — but its defining trait is **turn-taking conversation with a person**.

This is **distinct from `ai-agent-system`** (`.claude/presets/ai-agent-system.md`). An agent system is autonomous: it plans, calls tools, and acts toward a goal with limited human turns. A chatbot is **human-in-the-loop by design** — every turn is a reply to a person, and the hardest problems are conversational (intent, slots, escalation, transcript handling, latency), not autonomous planning. A chatbot may *call* an agent or tools under the hood, but its contract is the conversation. It is also distinct from `ml-training` (which trains the underlying models) — a chatbot typically *consumes* hosted or pre-trained models.

---

## Typical use cases

- Customer-support assistant on a website widget that deflects tickets and escalates the rest
- WhatsApp / SMS / Messenger bot for order status, bookings, or FAQs
- Slack / Teams internal assistant (IT helpdesk, HR questions, runbook lookup)
- Voice / IVR assistant that handles intent capture before routing to a human agent
- Lead-qualification bot that asks scripted questions and hands warm leads to sales
- RAG-backed product assistant grounded in docs, with citations and a human fallback

---

## Required discovery questions

1. **Channels** — Which channels at launch: web widget, WhatsApp/SMS, Slack/Teams, Messenger, voice/IVR? Each has different latency, formatting, auth, and message-length constraints, and channel choice is largely irreversible once users adopt it.
2. **Scope of conversation** — Is the bot narrow (FAQ/support over a known knowledge base) or open-ended? A narrow, grounded scope is dramatically safer and cheaper than open-ended chat.
3. **Knowledge source** — What does the bot answer from: a fixed FAQ, RAG over documents, live system data via API, or a model's general knowledge? This drives grounding and hallucination risk.
4. **Escalation to human** — When and how does a conversation hand off to a person (live agent, ticket, callback)? What is the SLA for that handoff? Every serious bot needs a clean human exit.
5. **Identity and auth** — Does the bot need to authenticate the user before sharing account-specific information? Sharing personal data with an unverified user is a privacy breach.
6. **Transcript retention and PII** — How long are conversation transcripts kept, where, and who can read them? Do users share personal/payment/health data mid-conversation? This is a §6 business-critical / privacy decision.
7. **Latency budget** — What is the acceptable response time per turn (chat tolerates ~1–3 s; voice needs sub-second to feel natural)? This constrains model choice and retrieval depth.
8. **Tone, persona, and brand** — What voice should the bot have, and what must it never say? Brand/tone is a §6 business-critical decision.
9. **Languages** — Which languages must be supported at launch, and is automatic language detection required?
10. **Failure behaviour** — What does the bot do when it does not know, is unsure, or the backend is down — apologise, escalate, or fall back to a menu? Define the safe default before launch.

---

## Recommended agents

**Core**
- `.claude/agents/core/orchestrator.md` — drives the flow; conversation design and escalation policy must be specced before bot code
- `.claude/agents/core/solution-architect.md` — channel adapters, dialogue/state design, grounding pipeline, handoff topology

**Engineering**
- `.claude/agents/engineering/ai-ml-engineer.md` — model selection, prompt/intent design, RAG grounding, guardrails, latency/cost management (primary builder)
- `.claude/agents/engineering/integration-engineer.md` — channel integrations (WhatsApp/Slack/Twilio/web), CRM/helpdesk handoff, webhooks
- `.claude/agents/engineering/backend-engineer.md` — conversation state store, transcript persistence, session management, auth

**Quality**
- `.claude/agents/quality/qa-engineer.md` — conversation test sets, intent/slot coverage, escalation-path testing, golden-dialogue regression
- `.claude/agents/quality/privacy-compliance-auditor.md` — transcript retention, PII handling, consent, right-to-erasure
- `.claude/agents/quality/accessibility-auditor.md` — chat UI / voice accessibility (screen readers, captions, keyboard, voice clarity)

**Domain**
- `.claude/agents/domain/ai-agent-domain-expert.md` — conversation-loop design, grounding, guardrails, and tool-use when the bot calls backend actions

---

## Recommended skills

- `.claude/skills/ai-ml/SKILL.md` — model selection, prompt design, RAG grounding, guardrails, conversational evaluation, cost/latency management
- `.claude/skills/api-design/SKILL.md` — channel webhook contracts, handoff APIs, backend action endpoints the bot invokes
- `.claude/skills/security/SKILL.md` — auth before disclosing account data, prompt-injection defence, transcript access control
- `.claude/skills/observability/SKILL.md` — per-turn latency, deflection/escalation rate, fallback rate, conversation analytics
- `.claude/skills/testing/SKILL.md` — golden-conversation tests, intent/slot regression, escalation-path coverage

---

## Recommended stack-matrix entries

- `.claude/stack-matrix/ai-ml.md` — model and RAG/embedding choices for the conversational core
- `.claude/stack-matrix/realtime.md` — for streaming responses, websockets in the web widget, and voice transport
- `.claude/stack-matrix/search.md` — for the retrieval layer when the bot is RAG-grounded over a knowledge base
- `.claude/stack-matrix/backend.md` — for the conversation-state and transcript-persistence service

---

## Required checklists

- `.claude/checklists/ai-ml.md` — grounding, hallucination/guardrail checks, conversational eval gate, prompt-injection resistance, model-output safety
- `.claude/checklists/privacy-compliance.md` — transcript retention period, PII handling and redaction, consent capture, right-to-erasure, lawful basis
- `.claude/checklists/security.md` — auth before account-data disclosure, prompt-injection defence, channel webhook signature verification
- `.claude/checklists/accessibility.md` — chat/voice interface accessibility for the human surface

---

## MVP scope pattern

**In the first cut**
- One channel end-to-end (usually the web widget) with multi-turn context retained within a session
- A narrow, grounded scope: answer from a fixed FAQ or RAG over a defined knowledge base, with citations where possible
- A clear "I don't know" path and a working **escalation to human** (ticket or live handoff) — the bot must never trap the user
- Transcript persistence with a documented retention period and access control from day one
- A guardrail layer: refuse out-of-scope and unsafe requests; resist obvious prompt injection
- Per-turn latency within the target budget; a graceful message when the backend is slow or down

**Defer until post-MVP**
- Additional channels (add one at a time; each is its own adapter and test surface)
- Voice/IVR if launching on text first (voice adds transport, latency, and barge-in complexity)
- Multi-language beyond the launch language (add detection + translation once the core flow is stable)
- Deep tool-calling / transactional actions (start by answering and routing; add "do things on the user's behalf" once auth and guardrails are proven)
- Personalisation from CRM history
- Proactive/outbound messaging (start reactive; outbound has consent and compliance weight)

---

## Key risks

| Risk | Priority | Mitigation |
|---|---|---|
| **Account data disclosed to an unverified user** | P0 | Authenticate before sharing any personal/account data; never trust a self-claimed identity in the conversation |
| **PII in transcripts stored or logged unsafely** | P0 | Define retention up front; redact PII in logs; access-control transcripts; support erasure (`.claude/checklists/privacy-compliance.md`) |
| **Hallucinated answers presented as fact** | P0 | Ground answers in retrieval with citations; constrain scope; the bot says "I don't know" and escalates rather than inventing |
| **Prompt injection via user input or retrieved docs** | P0 | Treat all conversation and retrieved content as untrusted; separate instructions from data; never let input change tool permissions |
| **No human escalation — user gets stuck in a loop** | P1 | A guaranteed handoff path on every flow; detect repeated failure/frustration and escalate automatically |
| **Latency makes the bot feel broken** | P1 | Stream responses; cap retrieval depth; set per-turn budget; show typing/processing state; pick a model that meets the budget |
| **Tone/brand violations or unsafe content** | P1 | Persona + safety guardrails in the system prompt; output moderation; documented "never say" list reviewed against brand |
| **Cost runaway from long contexts or high volume** | P1 | Trim context windows; cache common answers; monitor cost per conversation; rate-limit abusive sessions |
| **Channel webhook spoofing** | P1 | Verify webhook signatures (Twilio/Slack/Meta) on every inbound message |

---

## Launch requirements

- All items in `.claude/checklists/ai-ml.md` and `.claude/checklists/privacy-compliance.md` are green
- Escalation to human works and meets its SLA; tested from a stuck/frustrated conversation
- Grounding verified: a golden set of questions returns correct, cited answers; out-of-scope questions are declined, not hallucinated
- Auth gate verified: the bot will not reveal account-specific data without verifying identity
- Transcript retention live: documented period, redaction of PII in logs, access control, and an erasure procedure
- Guardrails verified: prompt-injection attempts and unsafe requests are refused; channel webhooks verify signatures
- Latency within budget on the launch channel under representative load; graceful degradation when the backend is unavailable
- Conversation analytics live: deflection rate, escalation rate, fallback ("I don't know") rate, and per-turn latency dashboards
- Persona/tone reviewed against brand; the "never say" list is enforced by guardrails and tested
- A decision record (`.claude/templates/decision-record.md`) captures scope, knowledge source, retention period, and escalation policy

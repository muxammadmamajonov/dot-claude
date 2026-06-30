# Discovery Checklist
Passing this gate proves the founder interview is complete, the problem and user are understood with precision, and every downstream decision has a solid foundation — no speculation, no implicit assumptions. Items are severity-tagged P0/P1/P2/P3.

## P0 — Blockers (must pass before proceeding to requirements)

- [ ] Problem statement is one concrete sentence naming the pain, who feels it, and what they do today instead — no vague "improve X" or "help businesses with Y" language.
- [ ] Primary user persona is documented with: role, stated goal, specific daily friction, current workaround, and what "success today" looks like for them.
- [ ] At least one secondary persona (admin, operator, third-party integrator, or machine) is identified, even if their needs are deferred to a later phase.
- [ ] Success definition for v1 is measurable and agreed with the founder: a specific action a specific user can complete end-to-end without help (e.g., "a landlord can list a property and receive a verified tenant inquiry within 24 hours").
- [ ] Business model is documented: how the product earns or saves money (subscription, per-transaction fee, internal productivity, marketplace take-rate, licensing, advertising, or data). "TBD" is not accepted.
- [ ] Core workflow is traced step-by-step from the trigger event to the value moment — not described abstractly. Every manual step, decision point, and handoff is named.
- [ ] At least two existing alternatives or competitors are named with a one-line note on why users would switch (pricing, missing feature, trust, geography, compliance gap, or speed).
- [ ] Non-negotiable constraints are captured and classified: legal (GDPR, HIPAA, PCI-DSS, local data-residency), platform (iOS/Android/web only), geography (single country vs. multi-region), offline capability, language/locale, accessibility mandate (WCAG 2.2 AA, ADA, EN 301 549), or hardware dependency.
- [ ] Project type is confirmed and locked from: web app, mobile app, desktop app, game (2D/3D/multiplayer), backend API, CLI tool, browser extension, AI agent system, data platform, automation tool, IoT/embedded, blockchain app, SaaS, ecommerce, marketplace, fintech, CRM, ERP, helpdesk, social platform, media streaming, or custom. This gates preset selection in `../presets/` and stack guidance in `../stack-matrix/`.
- [ ] Out-of-scope list for v1 is written and agreed — at minimum five things that are explicitly deferred. This prevents scope creep from implicit assumptions during build.
- [ ] Scope boundary for v1 is written and agreed — the exact list of what is IN scope, not just "core features." Ambiguous items are explicitly resolved.
- [ ] Interview transcript or discovery-answers document is saved to `docs/discovery/` using `../templates/discovery-answers.md` as the template.

## P1 — Important (needed before architecture decisions)

- [ ] Stakeholder map is complete: every decision-maker, veto holder, and sign-off authority is named with their specific domain of control (infra spend, legal/compliance, brand, security policy, budget).
- [ ] Data sensitivity is rated for each data category the system will store: public / internal / confidential / regulated (PII, PHI, PCI, financial). Breach impact (reputational, regulatory fine, legal liability) is estimated.
- [ ] Scale expectations are stated as orders of magnitude for: users at launch, at 6 months, and at 18 months; peak concurrent sessions; data volume growth rate (rows/day or GB/month). Rough estimates accepted; "unknown" is not.
- [ ] Third-party integration dependencies are named with: API name, auth method, rate limits, pricing tier, SLA/uptime, and what happens if the integration is unavailable at launch.
- [ ] Team capability snapshot captures technology gaps that must be avoided or bridged: languages not known, ops skills absent, domain knowledge missing (financial regulations, medical data handling, etc.).
- [ ] Budget ceiling and hard launch deadline are documented so the MVP scope is realistically sized against available runway. If funded, runway to next milestone or break-even is noted.
- [ ] Offline / degraded-mode behavior is decided: must the product work with no internet? with intermittent connectivity? with read-only access during outages? Answer affects architecture fundamentally.

## P2 — Hardening / nice-to-have

- [ ] Assumptions log is started (`docs/state/assumptions.md` from `../templates/assumptions-log.md`) with at least the three highest-uncertainty assumptions noted, each with a confidence level and a validation plan.
- [ ] Exit and handoff scenario is considered: will this product be transferred to another team, acquired, white-labeled, or open-sourced? This affects documentation and abstraction choices.
- [ ] Monetization runway is recorded: if the product is funded, the date by which it must reach a revenue or usage milestone is documented so technical trade-offs reflect real time pressure.
- [ ] Regulatory roadmap beyond v1 is noted: any compliance certifications (SOC 2, ISO 27001, HIPAA BAA, PCI-DSS Level 1) that will be required within 12 months should be flagged now, as they affect architecture decisions made today.

## P3 — Post-launch / backlog (track and revisit after launch; never blocks shipping)

- [ ] Discovery answers document is reviewed against actual v1 usage data (6–12 weeks post-launch) to validate or invalidate the primary persona's stated pain, workaround, and success definition.
- [ ] Competitor landscape is re-surveyed after launch: new entrants, pricing changes, or feature gaps that emerged since the original discovery session are documented and assessed for strategic impact.
- [ ] Secondary personas deferred at discovery are formally re-evaluated with real user telemetry to determine whether their needs justify a phase-2 scope expansion.
- [ ] Regulatory roadmap items flagged at discovery (SOC 2, HIPAA BAA, PCI-DSS Level 1, ISO 27001) are assigned owners, timelines, and budget estimates now that v1 is live and the compliance surface is concrete.
- [ ] Out-of-scope list from v1 is revisited; items with high user demand (evidenced by support tickets, feature requests, or usage gaps) are promoted to the next planning cycle with priority rationale.

## How to use
Run during the **classify → interview** phase, driven by `../agents/core/orchestrator.md` delegating to `../agents/core/business-analyst.md`. The business analyst interviews the founder using `../commands/interview-founder.md` and fills these items. Reference `../skills/discovery/SKILL.md` for interview technique. No requirements work, architecture, or code begins until all P0 items pass. Re-run if the business model, primary persona, project type, or core workflow changes materially. Reviewer marks each item `[x]` when satisfied or `[-]` when explicitly waived with a written reason and risk note.

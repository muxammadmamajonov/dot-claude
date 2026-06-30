# Edtech Preset

## Project type

Software products that deliver, manage, or enhance educational experiences for learners, instructors, or institutions. Common variants:

- **Learning Management System (LMS)** — course authoring, enrollment, progress tracking, grades, certificates; B2B sold to schools, universities, or corporates.
- **Online course marketplace** — instructor-created video courses sold to individual learners; Udemy/Coursera model; royalty and payout engine for instructors.
- **Adaptive / personalized learning** — AI-driven content sequencing that adjusts to learner mastery; spaced repetition; K-12 or professional certification focus.
- **Tutoring / live session platform** — 1:1 or small-group live sessions; tutor marketplace with scheduling, video, and payment.
- **K-12 / higher-ed institutional platform** — integrates with SIS (Student Information System), rostering via Clever/ClassLink, LTI 1.3 integration into existing LMS.
- **Corporate learning / L&D platform** — onboarding, compliance training, skills development; SCORM/xAPI content playback; HRIS integration.
- **Coding bootcamp / skills platform** — interactive coding environments (sandboxes), project submissions, automated grading, cohort management.
- **Gamified learning / EdGame** — game mechanics driving learning outcomes; narrative-driven or puzzle-based; often K-12 or language learning.
- **Assessment and proctoring platform** — question banks, adaptive testing, online proctoring (AI or human), psychometric reporting.

## Typical use cases

- University deploys an LMS for 20,000 students with LTI integrations into Zoom and Turnitin.
- Individual creator sells self-paced video courses with quizzes and completion certificates.
- Language-learning app with daily streaks, spaced-repetition vocabulary, and AI pronunciation feedback.
- Corporate compliance training platform with SCORM playback and completion reporting to HR.
- K-12 school district deploys a coding curriculum with in-browser sandboxes and teacher dashboards.
- Tutoring marketplace where parents book verified tutors for live video sessions paid per hour.
- Adaptive math platform that serves practice problems calibrated to each student's current mastery level.

## Required discovery questions

1. Who are the primary learners — age group, technical sophistication, device access (desktop, tablet, mobile, low-bandwidth)? Are they individual consumers (B2C) or institution-enrolled (B2B)?
2. What content formats are in scope at launch? (Video, text/articles, interactive exercises, SCORM/xAPI packages, live video sessions, coding sandboxes, assessments.) Who creates the content — the platform, instructors, or institutions?
3. What does the learner progress model look like? (Linear course completion, mastery-based unlocking, cohort-based deadlines, self-paced open access, adaptive sequencing.) How are completions and grades defined and certified?
4. Are there institutional integration requirements? (LTI 1.3 / LTI Advantage for LMS embedding, Clever/ClassLink for K-12 rostering, SCORM 1.2/2004 or xAPI for content interoperability, SIS sync for enrollment and grades.)
5. What are the child privacy obligations? (COPPA for under-13 US users, FERPA for US student educational records, GDPR-K / UK Age-Appropriate Design Code, PIPEDA for Canada.) Do parental consent flows apply?
6. What is the monetisation model? (Subscription per learner/institution, per-seat B2B licence, course purchase, instructor revenue share, freemium with paid certificates, government/grant-funded free access.)
7. What accessibility standard must the product meet, and for which jurisdictions? (WCAG 2.1 AA minimum; Section 508 if selling to US federal agencies or public schools; EN 301 549 for EU public sector.) Are captions and transcripts required for all video content?
8. What are the peak concurrency requirements? (Exam season / cohort start day can spike to 10–50× baseline; live session platforms need WebRTC media server capacity planning.)
9. What assessment integrity controls are needed? (Time-limited exams, question randomisation, plagiarism detection, online proctoring, locked-browser mode.) What happens when a learner loses connectivity mid-exam?
10. What reporting and analytics does the institution or instructor need? (Completion rates, time-on-task, quiz scores, cohort comparisons, xAPI/LRS reporting, CSV/API export for accreditation evidence.)

## Recommended agents

**Core**
- `.claude/agents/core/orchestrator.md` — flow control and gate enforcement.
- `.claude/agents/core/product-manager.md` — learner journey design, content model, monetisation scope.
- `.claude/agents/core/solution-architect.md` — LTI/SCORM integration architecture, content delivery, progress data model.
- `.claude/agents/core/requirements-engineer.md` — FERPA/COPPA compliance requirements, accessibility acceptance criteria.

**Engineering**
- `.claude/agents/engineering/backend-engineer.md` — enrollment engine, progress tracking, certificate generation, payment/payout, xAPI LRS.
- `.claude/agents/engineering/frontend-engineer.md` — course player (video, SCORM, interactive), learner dashboard, instructor studio.
- `.claude/agents/engineering/mobile-engineer.md` — offline content download, mobile player, push notification reminders.
- `.claude/agents/engineering/realtime-engineer.md` — live class video (WebRTC), collaborative whiteboard, real-time quiz/poll, chat.
- `.claude/agents/engineering/devops-engineer.md` — CDN for video delivery, elastic scaling for exam peaks, CI/CD.
- `.claude/agents/engineering/ai-ml-engineer.md` — adaptive sequencing, spaced repetition engine, AI writing/pronunciation feedback.

**Quality**
- `.claude/agents/quality/accessibility-auditor.md` — WCAG 2.1 AA; captions and transcripts; keyboard navigation of course player and assessments.
- `.claude/agents/quality/security-auditor.md` — FERPA data protection, COPPA safeguards, LTI authentication security, assessment integrity.
- `.claude/agents/quality/privacy-compliance-auditor.md` — COPPA parental consent, FERPA data-sharing restrictions, GDPR for EU learners.
- `.claude/agents/quality/qa-engineer.md` — SCORM conformance, LTI launch flows, progress-tracking edge cases, concurrent exam load.
- `.claude/agents/quality/performance-engineer.md` — video streaming latency, peak concurrency for exams, adaptive content response time.

**Domain**
- `.claude/agents/domain/edtech-domain-expert.md` — LTI 1.3, SCORM/xAPI, FERPA/COPPA, spaced repetition, learning outcome taxonomy, accreditation evidence.

## Recommended skills

- `.claude/skills/backend/SKILL.md` — enrollment state machine, progress aggregation, certificate issuance, xAPI statement storage.
- `.claude/skills/web/SKILL.md` — SCORM/xAPI runtime API, video player (HLS adaptive bitrate), interactive exercise rendering.
- `.claude/skills/mobile/SKILL.md` — offline content caching, background sync of progress, push-notification learning reminders.
- `.claude/skills/security/SKILL.md` — LTI 1.3 OIDC launch validation, FERPA access controls, child-safe data handling.
- `.claude/skills/data-modeling/SKILL.md` — learner progress schema, xAPI statement schema, course/content hierarchy model.
- `.claude/skills/performance/SKILL.md` — adaptive bitrate video delivery, CDN edge caching, concurrent exam load testing.
- `.claude/skills/testing/SKILL.md` — SCORM conformance suite, LTI launch test harness, accessibility automated scanning.
- `.claude/skills/devops/SKILL.md` — auto-scaling for exam peaks, video transcoding pipeline, feature flag rollout for content experiments.

## Recommended stack options

| Stack | Rationale |
|-------|-----------|
| **Next.js + Node.js (NestJS) + PostgreSQL + AWS CloudFront + Mux** | Full-stack TypeScript; Mux handles video encoding, storage, and HLS delivery with built-in analytics; Postgres stores progress and enrollment; CloudFront scales to exam-day traffic spikes. See `.claude/stack-matrix/web.md`, `.claude/stack-matrix/backend.md`. |
| **React + Django (Python) + PostgreSQL + Celery + Cloudflare R2** | Python backend suits ML-heavy adaptive learning; Django has mature LMS libraries (Open edX ancestry); Celery for async certificate generation and progress aggregation; R2 for cost-effective video storage. See `.claude/stack-matrix/backend.md`. |
| **React Native + Node.js + PostgreSQL + AWS** | Mobile-first language or skills learning app requiring offline support; React Native shares business logic across iOS and Android; background sync sends xAPI statements when connectivity resumes. See `.claude/stack-matrix/mobile.md`. |
| **Open edX (Tutor deployment) + custom plugins** | Industry-standard open-source LMS with built-in SCORM, LTI, and xAPI; best when the product needs LMS baseline features fast and budget allows platform customisation rather than greenfield build. See `.claude/stack-matrix/backend.md`. |

## Required checklists

- `.claude/checklists/accessibility.md` — extend with: all video content has accurate captions and a transcript; course player is fully keyboard-operable; SCORM content accessibility is verified (or noted as a third-party responsibility); timed assessments have a pause/extend mechanism for learners with accommodations.
- `.claude/checklists/security.md` — extend with: LTI 1.3 launch signature verified; FERPA-protected records accessible only to the enrolled student and authorised educators; under-13 accounts have verifiable parental consent before any data collection; no student PII in third-party analytics SDKs without DPA.
- `.claude/checklists/qa.md` — extend with: SCORM 1.2 and 2004 conformance tested against ADL test suite; xAPI statements validated against profile; progress correctly restored after mid-session disconnect; certificate generation idempotent (duplicate completion event does not issue duplicate certificate).
- `.claude/checklists/performance.md` — extend with: video player reaches first-frame within 3 seconds on a 10 Mbps connection; concurrent exam peak load tested (10× normal daily users); adaptive bitrate switches gracefully at 3 Mbps and 1 Mbps; CDN cache-hit ratio > 90 % for static course assets.

## MVP scope pattern

**In the first cut:**
- One content type delivered end-to-end: either self-paced video course or live session — not both.
- Linear enrollment → content delivery → completion tracking → certificate flow.
- Learner and instructor roles; admin panel for content management and enrollment reports.
- Single payment method (Stripe Checkout) for direct course purchase or subscription.
- Progress auto-saved every 30 seconds and on page close; restore on re-entry.
- Basic completion certificate (PDF) generated on course finish; verifiable via a public URL.
- WCAG 2.1 AA from launch: captions on all video, keyboard navigation on player and quiz.
- Child-safe mode (COPPA) if any under-13 users are possible: no behavioural tracking, parental consent gate, no social features.

**Deferred to later:**
- LTI 1.3 integration (high complexity; required for institutional sales — prioritise when first school/enterprise deal is in progress).
- SCORM/xAPI playback (needed for corporate L&D; add after B2B channel is validated).
- Adaptive sequencing and spaced-repetition engine (significant ML investment; validate with fixed curriculum first).
- Live proctoring (requires legal review and third-party partnership; defer until exam-integrity is a commercial requirement).
- Multi-instructor marketplace with revenue share (complex payout logic; launch with a single-creator model first).
- Mobile offline download (important for low-bandwidth markets; deliver after web product is stable).
- xAPI Learning Record Store (enterprise analytics feature; validate need before building).
- Cohort and cohort-paced scheduling (needed for bootcamp model; add when cohort GTM is confirmed).

## Production risks

| Risk | Priority | Notes |
|------|----------|-------|
| COPPA violation: collecting data from under-13 users without verifiable parental consent | P0 | Age gate with parental consent flow before any account creation if product may reach under-13; no third-party tracking for child accounts; legal review of COPPA notice before launch. |
| FERPA violation: student educational records exposed to unauthorised parties | P0 | Enrollment-scoped access control; no student data in third-party analytics without signed DPA; data-sharing only with school officials with legitimate educational interest. |
| LTI 1.3 authentication bypass — attacker launches as arbitrary user | P0 | Validate nonce, iss, aud, exp, and deployment ID on every LTI launch; never trust client-provided user identity without verified JWT. |
| Video content accessible without authentication — paid content piracy and revenue loss | P0 | Signed URLs with short expiry on every video segment; CDN access policy enforces token; no permanent public video URLs. |
| Progress data lost on mid-session crash — learner loses hours of work | P1 | Auto-save progress every 30 seconds; write-ahead buffer in localStorage; reconcile with server on reconnect; test with simulated network drop. |
| SCORM package crashes player — learner unable to complete compliance course | P1 | Sandbox SCORM execution; catch unhandled JS errors in SCORM iframe; fallback to direct content view; test each SCORM package before publishing. |
| Exam peak concurrency causes timeout — students unable to submit during final exam | P1 | Load test at 10× daily concurrent users before any scheduled exam; auto-scale policy tested; queue-based submission with client-side retry and deadline extension fallback. |
| Certificate issued without completed course requirements — accreditation risk | P1 | Certificate generation gated on server-side completion assertion (not client-reported); audit log of every certificate issue; revocation mechanism exists. |
| Inaccessible video player locks out learners with disabilities | P1 | Automated accessibility scan on player component; manual test with screen reader (NVDA/VoiceOver) before launch; captions on 100 % of video before any institutional sale. |
| Instructor payout calculation error — overpayment or underpayment | P2 | Revenue-share calculation has unit tests with boundary values; payout report reconciles against Stripe Connect transfer log; instructor-facing payout history shows itemised breakdown. |

## Launch requirements

- All video content has accurate captions and a text transcript before the product is publicly accessible.
- Course player passes keyboard-navigation test on all critical actions (play/pause, seek, quiz submission, next lesson).
- COPPA age gate and parental consent flow implemented and tested if any under-13 users are possible.
- FERPA access controls verified: automated test confirms Student A cannot retrieve Student B's progress or grades.
- Progress auto-save and restore tested: session interrupted at mid-lesson restores to within 30 seconds of the last saved position.
- Certificate generation tested for idempotency: triggering completion twice issues exactly one certificate.
- Stripe payment and payout flows tested in test mode including failed card, refund, and instructor payout.
- Video delivery tested at 1 Mbps (adaptive bitrate degrades gracefully) and on mobile Safari and Chrome.
- Peak load test completed: platform handles expected launch-day concurrency without timeout or data loss.
- Error monitoring active; alerts fire on course-player error rate spike or payment failure threshold.
- Privacy policy and COPPA notice (if applicable) reviewed by legal counsel and live before launch.

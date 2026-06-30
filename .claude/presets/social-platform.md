# Social Platform Preset

## Project type

Social networking platform with user-generated content, social graphs, feeds, and moderation. Users create profiles, post content, follow or connect with others, and consume algorithmically or chronologically ordered feeds. Variants differ primarily in content type and graph topology.

Common variants:
- **Interest-based social network** — posts, follows, topic communities (Twitter/X, Mastodon style)
- **Visual-first platform** — photo/video posts, stories, reels (Instagram/TikTok style)
- **Professional network** — profile-as-résumé, endorsements, job posts (LinkedIn style)
- **Community / forum platform** — threaded discussion, upvotes, sub-communities (Reddit style)
- **Private social / close-friends** — small-group sharing, ephemeral content
- **Creator platform** — subscription content, tipping, paywalled posts (Substack/Patreon hybrid)
- **Federated / decentralised social** — ActivityPub or Nostr protocol, multiple instances

---

## Typical use cases

- Profile creation and discovery: bio, avatar, handle, links, follow/connect actions
- Content creation: text posts, images, videos, polls, links with open-graph previews
- Feed rendering: home feed (followed accounts), discovery/explore feed, profile feed
- Social interactions: likes, reactions, comments, shares/reposts, quote-posts
- Notifications: real-time alerts for mentions, replies, follows, reactions
- Direct messaging between connected users
- Search: full-text post search, people search, hashtag/topic pages
- Content moderation: report flow, automated pre-screening, moderator review queue, appeals
- Creator monetisation: subscriptions, tipping, ad revenue share, paywalled posts

---

## Required discovery questions

1. **What is the core content type?** (text, image, video, audio, mixed) — determines storage, transcoding pipeline, CDN strategy, and feed-ranking complexity.
2. **What is the social graph model?** (directed follow = asymmetric; mutual friend = symmetric; community membership; or all three) — graph model shapes every feed, notification, and permission query.
3. **Who can see content by default, and what privacy controls exist?** (public, followers-only, close-friends, paid subscribers, unlisted, private) — visibility logic permeates every read path.
4. **Is real-time interaction required?** (live notifications, presence indicators, live streaming, real-time comments) — real-time adds significant infrastructure complexity.
5. **What scale is expected at launch vs. 12 months?** (DAU, posts/day, feed reads/second) — the architectural gap between 1 k and 100 k DAU in feed design is massive; fan-out strategy must be chosen early.
6. **What moderation obligations apply?** (DSA in EU, CSAM detection mandatory everywhere, local illegal-content removal laws, age verification requirements) — non-compliance is a legal P0, not a feature.
7. **Is there a creator economy / monetisation layer?** (subscriptions, tips, ads) — adds payment processing, tax/VAT handling, payout flows, and revenue-share accounting.
8. **Does the platform target or permit access by minors?** (COPPA in US, age-appropriate design codes in UK/EU) — tightens data collection, advertising rules, and content controls substantially.
9. **Is federation or interoperability required?** (ActivityPub, AT Protocol, open API) — federated architectures have fundamentally different data models and trust boundaries.
10. **What are the authentication and identity requirements?** (email/password, social login, phone number, pseudonymous, device-only) — determines account recovery, ban-evasion prevention, and sybil resistance.

---

## Recommended agents

### Core
- `.claude/agents/core/orchestrator.md`
- `.claude/agents/core/solution-architect.md`
- `.claude/agents/core/requirements-engineer.md`
- `.claude/agents/core/product-manager.md`
- `.claude/agents/core/business-analyst.md`

### Engineering
- `.claude/agents/engineering/backend-engineer.md`
- `.claude/agents/engineering/frontend-engineer.md`
- `.claude/agents/engineering/realtime-engineer.md`
- `.claude/agents/engineering/database-architect.md`
- `.claude/agents/engineering/search-engineer.md`
- `.claude/agents/engineering/data-engineer.md`
- `.claude/agents/engineering/api-architect.md`
- `.claude/agents/engineering/mobile-engineer.md` *(if mobile app)*

### Quality
- `.claude/agents/quality/security-auditor.md`
- `.claude/agents/quality/privacy-compliance-auditor.md`
- `.claude/agents/quality/qa-engineer.md`
- `.claude/agents/quality/performance-engineer.md`
- `.claude/agents/quality/reliability-engineer.md`
- `.claude/agents/quality/accessibility-auditor.md`
- `.claude/agents/quality/production-readiness-auditor.md`

### Design
- `.claude/agents/design/ui-ux-designer.md`
- `.claude/agents/design/product-designer.md`
- `.claude/agents/design/accessibility-designer.md`
- `.claude/agents/design/mobile-ux-specialist.md` *(if mobile app)*

### Domain
- `.claude/agents/domain/social-platform-domain-expert.md`
- `.claude/agents/domain/media-streaming-domain-expert.md` *(if video/audio content)*

### Stack
- `.claude/agents/stack/backend/node-nest-fastify-engineer.md` or `.claude/agents/stack/backend/go-engineer.md`
- `.claude/agents/stack/web/react-next-engineer.md`
- `.claude/agents/stack/database/postgres-engineer.md`

---

## Recommended skills

- `.claude/skills/data-modeling/SKILL.md` — social graph (user → follow → user), posts, reactions, feed cursor pagination schema
- `.claude/skills/backend/SKILL.md` — fan-out-on-write vs. fan-out-on-read feed strategy, notification pipeline
- `.claude/skills/redis/SKILL.md` — feed cache (sorted sets), presence indicators, rate limiting, pub/sub for real-time events
- `.claude/skills/postgres/SKILL.md` — graph traversal queries, full-text post search, timeline cursor pagination
- `.claude/skills/api-design/SKILL.md` — cursor-based pagination API design, GraphQL vs REST for social graph trade-offs
- `.claude/skills/security/SKILL.md` — account takeover protection, rate limiting on auth endpoints, CSAM hash-matching integration
- `.claude/skills/performance/SKILL.md` — feed p99 latency targets, image/video CDN, hot-post fan-out storm mitigation
- `.claude/skills/testing/SKILL.md` — feed correctness tests, moderation workflow tests, notification delivery tests
- `.claude/skills/production-readiness/SKILL.md`
- `.claude/skills/requirements-engineering/SKILL.md`

---

## Recommended stack options

| Stack | Rationale |
|---|---|
| **Node/Fastify + PostgreSQL + Redis + React/Next.js** | High-concurrency WebSocket connections for notifications; Redis sorted sets for timeline caches; Postgres adjacency-list graph at moderate scale. See `.claude/stack-matrix/backend.md`. |
| **Go + PostgreSQL + Redis + React** | Goroutines handle massive concurrent feed reads and WebSocket connections cheaply; suited for platforms expecting rapid user growth. See `.claude/stack-matrix/backend.md`. |
| **Python/Django + PostgreSQL + Celery + React** | Faster iteration for modest scale (<50 k DAU); Celery handles async fan-out and notification dispatch; good for community/forum variants. See `.claude/stack-matrix/backend.md`. |
| **Node/NestJS + PostgreSQL + Redis + React Native** *(mobile-first)* | Shared TypeScript types between API and React Native app; NestJS WebSockets for real-time; best when mobile is the primary surface. |

---

## Required checklists

- `.claude/checklists/security.md` — emphasize: CSAM detection mandatory before enabling image/video uploads, account takeover protection (rate-limit login, MFA), report-abuse prevention, visibility filter enforced at query layer
- `.claude/checklists/qa.md` — feed ordering correctness, notification delivery, moderation action audit trail, block/mute coverage across all feed paths
- `.claude/checklists/performance.md` — home feed render <300 ms p95; fan-out must not block post creation API response; image CDN delivery <2 s
- `.claude/checklists/accessibility.md` — feed infinite scroll accessible via keyboard; image alt text enforced or prompted at upload; video captions required
- `.claude/checklists/production.md`
- `.claude/checklists/launch.md`

---

## MVP scope pattern

**In the first cut:**
- User registration, login, profile (avatar, bio, handle)
- Directed follow graph (follow / unfollow / block / mute)
- Text post creation; single-image post
- Chronological home feed (posts from followed accounts, cursor-paginated)
- Profile feed (all posts by a user)
- Like and comment on posts
- Mention (@handle) with notification
- In-app notification centre (polling acceptable at MVP)
- Content reporting: user flags post → moderation queue
- Basic moderation queue: moderator reviews, removes or dismisses

**Deferred to later iterations:**
- Algorithmic / ranked feed
- Video and audio post types with transcoding pipeline
- Stories / ephemeral content
- Direct messaging
- Hashtags and topic pages
- Real-time push notifications (WebSocket)
- Discovery / explore feed
- Creator monetisation (subscriptions, tips, paywalled posts)
- Native mobile apps
- CSAM automated detection (required before scaling UGC to public — plan integration early)
- Federation / ActivityPub
- Advanced moderation: AI-assisted detection, appeals workflow, transparency reports
- Ads system

---

## Production risks

| Risk | Severity | Mitigation |
|---|---|---|
| CSAM uploaded or distributed on platform | **P0** | Integrate PhotoDNA or Microsoft CSAM hash-matching before any public image/video upload goes live; NCMEC reporting pipeline in place; legal review of obligations per jurisdiction before launch |
| Illegal content triggers regulatory enforcement | **P0** | DSA / local law compliance review before EU launch; content reporting SLA defined; emergency takedown procedure in runbook |
| Fan-out storm: viral post write-amplification degrades database | **P0** | Cap fan-out-on-write at N followers (e.g. 10 k); above threshold use fan-out-on-read with celebrity feed merge; load test at 10× expected peak before launch |
| Account takeover via credential stuffing | **P0** | Rate-limit login attempts per IP and per account; breached-password check (HaveIBeenPwned API); MFA option; device fingerprint anomaly alert |
| Feed query missing visibility filter (public vs. followers-only post returned to non-follower) | **P0** | Enforce visibility predicate at ORM/query layer, not application layer; automated test: followers-only post must return 403 to non-follower API call |
| Notification storm on viral post overwhelms delivery pipeline | **P1** | Aggregate notifications ("X and 47 others liked your post"); queue with back-pressure; per-recipient delivery rate limit |
| Moderation queue backlog leaves harmful content live for hours | **P1** | Automated pre-screening for known-bad hashes and high-severity keywords; priority triage by report count; SLA alert when oldest unreviewed item exceeds threshold |
| Hot-row contention on like/reaction counter at viral scale | **P1** | Approximate counter in Redis (INCR); periodic async flush to DB; never SELECT FOR UPDATE on a counter row |
| GDPR erasure cannot be fulfilled because deleted user's posts are entangled with others' replies | **P2** | Soft-delete posts; replace author attribution with "deleted user" tombstone; erasure does not cascade-delete replies authored by others |
| Search index lags significantly behind post creation | **P2** | Async index pipeline with lag metric; surface "results may be slightly delayed" warning in UI when lag >30 s |

---

## Launch requirements

- [ ] CSAM hash-matching integration active and tested before any public image/video upload is enabled
- [ ] Content reporting flow tested end-to-end: report → queue → action → reporter notification
- [ ] Visibility filter verified by automated test: followers-only post returns 403 to non-follower
- [ ] Fan-out load test passed at 2× expected launch DAU without DB saturation
- [ ] Login rate limiting and credential-stuffing protection active and verified
- [ ] Block and mute actions confirmed to suppress content across all feed and notification paths
- [ ] GDPR erasure tested: user deletion anonymises posts, removes PII, erasure logged
- [ ] Image upload limits and malicious file type rejection verified
- [ ] Notification aggregation confirmed: single viral post does not spam recipient's notification inbox
- [ ] Performance baseline: home feed p95 <300 ms at expected user count
- [ ] Accessibility: keyboard navigation through feed, image alt text prompt at upload, screen reader smoke test
- [ ] Moderation runbook written: escalation path, emergency takedown procedure, transparency report template
- [ ] Security checklist `.claude/checklists/security.md` fully green

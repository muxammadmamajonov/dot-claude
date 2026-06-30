# Media Streaming Platform Preset

## Project type

Platform that ingests, stores, processes, and delivers audio or video content to end users at scale. Covers on-demand (VOD) and live streaming. Variants differ by content type, rights model, and delivery architecture.

Common variants:
- **VOD platform** — uploaded video library, playback on demand (YouTube / Vimeo style)
- **Live streaming platform** — real-time broadcast ingestion and delivery (Twitch / live sports style)
- **Audio streaming** — podcast hosting, music streaming, audiobook delivery
- **SVOD / TVOD** — subscription or pay-per-view with DRM, content entitlements, geo-restrictions
- **Internal media hub** — enterprise video hosting for training, town halls, async comms
- **UGC + creator platform** — user uploads with monetisation (ad revenue, subscriptions, tips)
- **Broadcast / OTT** — linear channel simulation, EPG, catch-up TV

---

## Typical use cases

- Content ingest: upload raw media → transcode to adaptive bitrate (ABR) renditions → store on CDN
- Live ingest: RTMP/SRT stream from encoder → segment into HLS/DASH → distribute to viewers
- Adaptive bitrate playback: player selects quality tier based on available bandwidth
- Content catalogue: metadata management (title, description, tags, thumbnails, chapters, subtitles)
- Entitlement management: free tier, subscription check, pay-per-view token, geo-block enforcement
- DRM: Widevine, FairPlay, PlayReady key exchange with licence server
- Search and discovery: full-text search, genre/tag browse, recommendations
- Social layer: comments, reactions, watch parties, clip sharing
- Analytics: play events, buffering ratio, quality switches, completion rate, concurrent viewers
- Monetisation: pre/mid/post-roll ads (VAST/VMAP), subscription billing, creator payouts

---

## Required discovery questions

1. **Is this VOD, live streaming, or both?** — live streaming requires a real-time ingest pipeline (RTMP/SRT → segmenter) that is architecturally separate from VOD transcoding; building both at once is high risk.
2. **Who creates content — the platform operator, invited creators, or the general public?** — UGC platforms need upload abuse prevention, automated content moderation, and copyright detection (Content ID style); operator-only upload is far simpler.
3. **What is the expected peak concurrent viewer count and library size?** — drives CDN strategy, origin server sizing, and whether to build on a managed video platform (Mux, Cloudflare Stream, AWS MediaConvert) or custom transcode pipeline.
4. **Is DRM required, and if so which ecosystems?** (Widevine for Android/Chrome, FairPlay for Apple, PlayReady for Windows/Xbox) — DRM triples the playback integration complexity and requires a licence server.
5. **What geo-restrictions or content licensing territories apply?** — per-content geo-block must be enforced at both the CDN edge and the entitlement API; licensing metadata must be stored per territory.
6. **What is the monetisation model?** (AVOD with ads, SVOD subscriptions, TVOD pay-per-view, hybrid, creator revenue share) — each has distinct billing, entitlement, and reporting requirements.
7. **What accessibility requirements apply?** (closed captions mandatory under ADA/WCAG for video content; audio description tracks; accessible player controls) — captions pipeline must be planned from the start.
8. **What compliance obligations apply?** (COPPA if minors can access; GDPR on watch-history and behavioural data; CSAM detection if UGC video is permitted; local broadcast regulation for OTT).
9. **Must the platform own the transcode and storage infrastructure, or can it use a managed video API?** — managed services (Mux, AWS MediaConvert + S3 + CloudFront) reduce build time by months but add per-minute costs and vendor dependency.
10. **What player targets must be supported?** (web browser, iOS, Android, Smart TV / Fire TV / Roku, game consoles, desktop app) — each player surface needs a tested HLS/DASH + DRM integration.

---

## Recommended agents

### Core
- `.claude/agents/core/orchestrator.md`
- `.claude/agents/core/solution-architect.md`
- `.claude/agents/core/requirements-engineer.md`
- `.claude/agents/core/product-manager.md`
- `.claude/agents/core/technical-lead.md`

### Engineering
- `.claude/agents/engineering/backend-engineer.md`
- `.claude/agents/engineering/frontend-engineer.md`
- `.claude/agents/engineering/data-engineer.md`
- `.claude/agents/engineering/api-architect.md`
- `.claude/agents/engineering/realtime-engineer.md`
- `.claude/agents/engineering/cloud-architect.md`
- `.claude/agents/engineering/infrastructure-engineer.md`
- `.claude/agents/engineering/mobile-engineer.md` *(if mobile apps required)*

### Quality
- `.claude/agents/quality/performance-engineer.md`
- `.claude/agents/quality/security-auditor.md`
- `.claude/agents/quality/privacy-compliance-auditor.md`
- `.claude/agents/quality/qa-engineer.md`
- `.claude/agents/quality/reliability-engineer.md`
- `.claude/agents/quality/accessibility-auditor.md`
- `.claude/agents/quality/production-readiness-auditor.md`

### Design
- `.claude/agents/design/ui-ux-designer.md`
- `.claude/agents/design/accessibility-designer.md`

### Domain
- `.claude/agents/domain/media-streaming-domain-expert.md`

### Stack
- `.claude/agents/stack/backend/node-nest-fastify-engineer.md` or `.claude/agents/stack/backend/go-engineer.md`
- `.claude/agents/stack/web/react-next-engineer.md`
- `.claude/agents/stack/database/postgres-engineer.md`
- `.claude/agents/stack/cloud/aws-engineer.md` *(if AWS-based)*

---

## Recommended skills

- `.claude/skills/backend/SKILL.md` — signed URL generation, entitlement checks, webhook handling from transcode service
- `.claude/skills/data-modeling/SKILL.md` — content catalogue, entitlement, playback session, analytics event schema
- `.claude/skills/api-design/SKILL.md` — video API contracts (upload URLs, playback tokens, webhook ingest)
- `.claude/skills/devops/SKILL.md` — CDN configuration, origin shield, transcode pipeline orchestration
- `.claude/skills/redis/SKILL.md` — concurrent viewer counting, playback session tokens, rate limiting upload requests
- `.claude/skills/postgres/SKILL.md` — content metadata queries, entitlement lookups, analytics aggregation
- `.claude/skills/security/SKILL.md` — signed URLs with expiry, DRM licence request validation, hotlink protection
- `.claude/skills/performance/SKILL.md` — CDN hit ratio, TTFB for first segment, buffering ratio targets
- `.claude/skills/testing/SKILL.md` — playback integration tests, entitlement boundary tests, transcode output validation
- `.claude/skills/production-readiness/SKILL.md`

---

## Recommended stack options

| Stack | Rationale |
|---|---|
| **Node/Fastify + PostgreSQL + Redis + React + Managed Video API (Mux or Cloudflare Stream)** | Fastest path to working adaptive-bitrate delivery; offloads transcode, storage, and CDN to the vendor; build entitlement, catalogue, and UI on top. See `.claude/stack-matrix/backend.md`. |
| **Go + PostgreSQL + Redis + React + AWS (MediaConvert + S3 + CloudFront)** | Full control over transcode pipeline; Go suits high-concurrency upload ingestion and segment signing; AWS ecosystem integrates DRM (AWS Elemental) and analytics (Kinesis). See `.claude/stack-matrix/backend.md`. |
| **Python/FastAPI + PostgreSQL + Celery + React + FFmpeg (self-hosted transcode)** | Most cost-effective for low-to-medium volume with in-house devops capacity; Celery manages transcode job queue; FFmpeg produces HLS output; suitable for internal enterprise media hub. See `.claude/stack-matrix/backend.md`. |
| **Node/NestJS + PostgreSQL + Redis + React Native (mobile-first) + Mux** | When mobile is the primary viewing surface and time-to-market is the constraint; Mux handles all media complexity; React Native shares logic with web. |

---

## Required checklists

- `.claude/checklists/security.md` — emphasize: signed playback URLs with short TTL, DRM licence server authentication, upload abuse prevention, hotlink protection at CDN, CSAM scanning on UGC video
- `.claude/checklists/qa.md` — transcode output validation (all renditions playable), entitlement boundary tests (subscriber vs. guest), geo-block enforcement test
- `.claude/checklists/performance.md` — TTFB for first segment <1 s on reference connection; buffering ratio <0.5%; CDN cache hit ratio >95% for popular content; concurrent viewer scale test
- `.claude/checklists/accessibility.md` — closed captions present and synchronised for all video content; accessible player controls (keyboard, screen reader); captions toggle in player UI
- `.claude/checklists/production.md`
- `.claude/checklists/launch.md`

---

## MVP scope pattern

**In the first cut:**
- Content upload: operator or invited creator uploads video file → transcode to 3 ABR renditions (360p / 720p / 1080p) → store on CDN
- HLS playback in browser with adaptive bitrate player (Video.js or HLS.js)
- Content catalogue: title, description, thumbnail, tags, duration
- Public and unlisted visibility modes (no paywall for MVP)
- Basic search by title and tag
- Captions: upload SRT/VTT file, burn-in or side-car delivery
- Basic play event tracking (play started, play ended, duration watched)
- Simple admin panel: upload, publish, unpublish, view play counts

**Deferred to later iterations:**
- Live streaming ingest (RTMP/SRT)
- DRM (Widevine / FairPlay / PlayReady)
- Subscription / pay-per-view entitlement
- Geo-restrictions
- Ad insertion (VAST / VMAP)
- Creator monetisation and payouts
- Recommendations engine
- Auto-generated captions (speech-to-text)
- Comments and social layer
- Smart TV / set-top box apps
- Native mobile apps
- Advanced analytics (funnel, retention, quality-of-experience dashboard)
- Content ID / copyright fingerprinting for UGC
- Multi-CDN failover

---

## Production risks

| Risk | Severity | Mitigation |
|---|---|---|
| Signed playback URL leaked or reused → content piracy | **P0** | Short TTL (15 min) on signed URLs; bind URL to user agent or IP range; invalidate on logout; DRM for premium content |
| Transcode job silently fails → broken playback or missing renditions | **P0** | Webhook from transcode service on success/failure; post-transcode validation job checks all expected renditions are playable; alert on failure |
| Entitlement bypass: non-subscriber accesses paywalled content | **P0** | Entitlement check in licence server (not just frontend); signed URL generation gated on entitlement; pentest paywall boundary before launch |
| CSAM uploaded via UGC video ingest | **P0** | Hash-match scan (PhotoDNA or equivalent) on ingest before any public availability; NCMEC reporting pipeline; legal counsel review before enabling UGC |
| CDN origin overloaded during viral content spike | **P0** | Origin shield / tiered CDN caching; never serve segments direct from origin to end users; auto-scale origin or use managed CDN with high egress limit |
| High buffering ratio at launch destroys retention | **P1** | Load test CDN configuration before launch; confirm ABR ladder matches expected user bandwidth distribution; monitor buffering ratio in real time on launch day |
| Geo-block enforcement gap at CDN edge | **P1** | Enforce geo-check at both CDN (WAF rule) and API (entitlement token); test with VPN from blocked territory before launch |
| Storage costs exceed budget due to multiple rendition copies | **P1** | Lifecycle policy: delete raw upload after transcode confirmed; archive low-view content to cold storage; track storage cost per video |
| Closed captions missing or out of sync | **P1** | Captions are an accessibility legal requirement for public video in many jurisdictions; validate sync on all content before publish; gated publish if captions absent |
| Analytics event loss during spike | **P2** | Buffer play events client-side in batches; send to ingest queue (not directly to DB); tolerate up to 1% event loss — log but do not block playback |

---

## Launch requirements

- [ ] All transcode renditions validated as playable (automated) for every piece of launch content
- [ ] Signed URL expiry confirmed: expired URL returns 403 at CDN
- [ ] Entitlement boundary tested: guest cannot access subscriber-only content via direct URL manipulation
- [ ] CDN load test: 500 concurrent viewers on popular content without origin saturation
- [ ] Closed captions present, synchronised, and toggleable for all launch videos
- [ ] Transcode failure alert fires and is routed to on-call within 5 min
- [ ] Storage lifecycle policy active: raw upload deleted after successful transcode
- [ ] Play event pipeline confirmed delivering to analytics store without data loss under load
- [ ] Accessible player controls: keyboard play/pause/seek/caption-toggle, screen reader labels
- [ ] GDPR data deletion tested: watch history and play events removed on user erasure request
- [ ] CDN cache hit ratio >95% for pre-populated popular content
- [ ] Runbook written: transcode failure recovery, CDN purge procedure, content emergency takedown
- [ ] Security checklist `.claude/checklists/security.md` fully green

# Auth & Identity Stack Matrix

Choose based on four axes: **build vs. buy tolerance** (rolling your own is a security liability, but vendors lock you in), **deployment model** (SaaS-only vs. self-hostable), **target user type** (B2C consumers vs. B2B enterprise vs. internal employees), and **enterprise feature needs** (SSO/SAML, SCIM, audit logs, MFA enforcement). Auth is infrastructure — get it wrong and you get breached; get it over-engineered and you spend a quarter on login.

Key drivers: B2C vs. B2B, enterprise SSO requirement, self-host vs. managed, data residency, MAU pricing sensitivity, existing stack (AWS/Firebase/Supabase), and long-term vendor dependency risk.

---

## Auth0 (Okta)

**When to use**
- Need the broadest protocol and social provider support on day one (200+ social connections)
- Enterprise B2B with SAML/SSO requirements; Auth0 handles IdP integration out of the box
- Complex authentication flows: step-up auth, adaptive MFA, attack protection, anomaly detection
- Need extensive customization: Auth0 Actions (Node.js hooks), custom login pages, custom claims

**When NOT to use**
- Cost-sensitive at scale: Auth0 MAU pricing becomes significant beyond 10 k MAUs on paid plans
- Simple projects where 80% of Auth0's feature surface goes unused
- Teams wanting self-hostable or data-residency-first solution — Auth0 is SaaS only
- Organizations already deep in Okta Workforce — Auth0 (Consumer Identity) vs. Okta (Workforce) distinction causes confusion post-acquisition

**Strengths**
- Widest feature surface: MFA, passwordless, passkeys, breached password detection, bot detection
- Enterprise Identity: SAML 2.0, WS-Fed, OIDC, SCIM provisioning, audit logs
- Auth0 Actions: JavaScript hooks for token enrichment, pre/post registration, MFA policy
- Universal Login: customizable, hosted login page with consistent security
- Organizations: B2B multi-tenant with per-org connections (SSO per customer)

**Weaknesses**
- Pricing: $240/month for 1 k MAUs (Professional); enterprise SSO adds significant cost per connection
- Vendor lock-in: Actions and custom claims are Auth0-specific; migration is non-trivial
- Management API rate limits can bite during high-volume user imports or bulk operations
- Post-Okta acquisition, product direction and support quality perception is mixed

**Team fit**
- B2B SaaS with enterprise customers requiring SSO; consumer apps needing social login + MFA
- Teams that want auth done without building anything

**Scale fit**
- Used by Fortune 500s; handles billions of logins/month. Cost, not scale, is the limiting factor.

**Risks**
- Okta suffered a major breach in 2023 — third-party vendor risk is real
- MAU pricing can 10x as a consumer app grows; model costs early
- Lock-in through Actions and proprietary management API patterns

---

## Clerk

**When to use**
- React/Next.js/Remix frontends wanting drop-in `<SignIn />`, `<UserButton />` components
- B2C or early-B2B SaaS wanting beautiful auth UI with zero frontend implementation
- Need passkeys, social OAuth, email magic links, SMS OTP with modern UX out of the box
- Multi-tenant B2B: Clerk Organizations handles workspace/tenant isolation natively

**When NOT to use**
- Non-JavaScript backends or non-React frontends — Clerk SDKs are JS/TS first
- Need SAML/SSO for enterprise customers (available on Enterprise plan, expensive)
- Self-hosting or data residency requirements — Clerk is SaaS-only
- Very high MAU scale on paid plans — pricing is per-MAU and compounds quickly

**Strengths**
- Best developer experience in the category: components render in minutes, sessions just work
- First-class Next.js App Router and RSC support; middleware-based route protection
- Clerk Organizations: multi-tenant with roles, invitations, per-org settings out of the box
- Webhooks for all auth events; JWT templates for custom claims
- Passkeys, MFA, device tracking built in without configuration

**Weaknesses**
- SaaS only; data lives on Clerk's infrastructure
- SAML SSO is Enterprise plan only (~$1 k+/month); not practical for early-stage B2B
- Mobile SDK maturity (iOS/Android native) lags behind web SDKs
- Less flexible for non-standard auth flows vs. Auth0's Action hooks

**Team fit**
- Next.js/React-first teams shipping fast; B2C apps, indie hackers, early-stage B2B SaaS
- Frontend engineers who want auth to feel like a UI component, not infrastructure

**Scale fit**
- Proven at mid-scale SaaS; MAU pricing model means costs grow linearly with users

**Risks**
- Clerk is VC-backed startup — platform risk vs. Auth0/Cognito/Firebase
- SaaS lock-in: moving off Clerk requires re-implementing auth flows and migrating sessions
- SAML pricing wall hits hard when first enterprise customer requests SSO

---

## AWS Cognito

**When to use**
- AWS-native workloads; want auth that integrates natively with API Gateway, ALB, AppSync, Lambda
- Need user pools (username/password, social) + identity pools (federated IAM credentials for AWS resources) in one service
- Cost-sensitive at very high MAU: Cognito is cheap ($0.0055/MAU after 50 k free MAUs)
- Mobile apps using AWS Amplify: Cognito is the default auth layer

**When NOT to use**
- Need polished, customizable login UI — Cognito's Hosted UI is basic and famously hard to style
- Complex B2B enterprise SSO scenarios — SAML works but configuration is painful compared to Auth0
- Teams not committed to AWS — Cognito outside AWS is awkward
- Custom auth flows beyond what Lambda triggers support — triggers are powerful but debug-unfriendly

**Strengths**
- Price: 50 k free MAUs/month; $0.0055/MAU after — dramatically cheaper than Auth0/Clerk at scale
- AWS integration: IAM role federation for direct S3/DynamoDB/etc. access from mobile clients
- OIDC compliant; integrates with API Gateway authorizers and ALB natively
- Lambda triggers: Pre-authentication, Post-confirmation, Custom message, Define auth challenge — extensible
- SAML 2.0 and OIDC IdP federation supported

**Weaknesses**
- Developer experience is poor: Amplify SDK has breaking changes; raw Cognito API is verbose
- Hosted UI customization is CSS-only; branded login requires custom UI or Amplify UI components
- User pool limits (e.g., 25 MFA configurations per user pool type) can surprise
- No native multi-tenancy / organizations — must be architected manually (separate user pools or custom attributes)
- Migration away from Cognito is painful: passwords are hashed with Cognito's scheme; migration Lambda trigger required

**Team fit**
- AWS-committed teams building mobile apps with Amplify; serverless API backends
- Cost-sensitive scale-ups already invested in AWS IAM patterns

**Scale fit**
- Designed for millions of MAUs; AWS manages scale. Cheap at high volume.

**Risks**
- Hosted UI limitations force custom UI — doubles implementation work
- Lock-in: Cognito password hashes are not exportable; migration requires custom Lambda + user re-authentication
- Amplify SDK churn has burned many teams; evaluate direct SDK vs. Amplify carefully

---

## Firebase Auth

**When to use**
- Mobile-first apps (iOS, Android, Flutter) in the Google ecosystem
- Google Play / Firebase ecosystem already in use (Firestore, Cloud Functions, FCM)
- Need anonymous auth, phone number auth, or game sign-in (Game Center, Play Games)
- Rapid prototyping: Firebase Auth with Firestore security rules is the fastest path to a secured backend

**When NOT to use**
- Non-Google cloud; Firebase lock-in is significant
- Enterprise B2B requiring SAML/SSO — Firebase Auth does not support SAML
- Need custom token claims beyond Firebase's limited custom claims (max 1 KB)
- Applications requiring row-level security on a relational database — Firestore rules are NoSQL-centric

**Strengths**
- Free up to 10 k/month phone auth verifications; social auth and email/password are free
- Native SDKs: best-in-class iOS, Android, Flutter, React Native integration
- Anonymous auth: convert anonymous users to permanent accounts without friction
- Google account sign-in with one tap; GameCenter/Play Games for gaming apps
- Tight Firestore security rules integration: auth UID directly in database rules

**Weaknesses**
- No SAML, no enterprise SSO — hard ceiling for B2B use cases
- Custom claims limited to 1 KB; complex RBAC requires workarounds (Firestore lookup on every request)
- Data on Google servers; GDPR and data residency concerns
- Admin SDK for user management is less feature-rich than Auth0 Management API
- No native organizations/multi-tenancy beyond Firebase multi-tenancy (paid, complex)

**Team fit**
- Mobile app developers; Google ecosystem shops; gaming apps
- Teams using Firestore who want auth to "just work" with security rules

**Scale fit**
- Scales to millions of users without ops; Google manages infrastructure

**Risks**
- Google has a history of deprecating Firebase features; platform continuity risk
- Phone auth SMS costs at scale; verify pricing before going viral
- Migrating off Firebase Auth requires password export workaround (no direct export)

---

## Supabase Auth

**When to use**
- Already using Supabase (PostgreSQL + Realtime + Storage); want auth in the same platform
- Need Row Level Security (RLS) on PostgreSQL tied directly to auth.uid()
- Self-hostable: open source, runs on your infrastructure
- Email/password, magic links, social OAuth, phone OTP — all built in and free on Supabase Cloud

**When NOT to use**
- Need SAML/enterprise SSO — Supabase Auth does not support SAML natively
- Not using PostgreSQL — Supabase Auth's RLS integration is Postgres-specific
- Need advanced MFA enforcement, adaptive auth, or anomaly detection out of the box
- Complex multi-tenant B2B organizations with per-org SSO requirements

**Strengths**
- Deep PostgreSQL integration: auth.uid() available in RLS policies, joins, triggers
- Self-hostable under Apache 2.0 license — full data ownership
- Free tier includes auth; no per-MAU pricing on Supabase Cloud
- Social providers, magic links, phone OTP, PKCE flow — all standard
- Supabase Auth Admin API for server-side user management
- Anonymous sign-ins for progressive profiling

**Weaknesses**
- No SAML/enterprise SSO — significant B2B limitation
- Session management less sophisticated than Auth0 (no risk-based step-up MFA)
- Organizations/multi-tenancy requires manual implementation (no built-in concept)
- MFA limited to TOTP; no SMS-based MFA natively
- Self-hosting requires managing the full Supabase stack (Postgres, PostgREST, GoTrue, Realtime)

**Team fit**
- Full-stack teams using Supabase as their primary backend
- Privacy-conscious teams wanting open-source, self-hostable auth

**Scale fit**
- Supabase Cloud handles millions of MAUs; self-hosted scales with your Postgres infrastructure

**Risks**
- Supabase is VC-backed; self-host as hedge against pricing changes
- GoTrue (auth service) is less battle-tested at extreme scale than Auth0/Cognito

---

## Keycloak

**When to use**
- Enterprise or regulated environments requiring self-hosted, on-prem identity provider
- Need SAML 2.0, OIDC, WS-Fed, Kerberos, LDAP/Active Directory integration in one system
- Internal workforce identity: employee SSO across internal applications
- Government, healthcare, financial services with data sovereignty requirements
- Need to act as a central IdP that other services (OIDC clients) authenticate against

**When NOT to use**
- Small teams or startups without dedicated DevOps capacity — Keycloak requires serious ops
- Consumer-facing auth where login UX customization is critical (Keycloak themes are hard to customize cleanly)
- Low-latency auth requirements — Keycloak's Java/WildFly/Quarkus stack adds startup latency
- Cloud-first teams who don't want to run JVM infrastructure

**Strengths**
- Most complete open-source IAM: SAML, OIDC, OAuth 2.0, SCIM, LDAP, Kerberos, WebAuthn
- Self-hosted: full data sovereignty; runs on-prem, in private cloud, or Kubernetes
- Admin console: manage realms, clients, user federation, identity brokering in a UI
- User federation: sync from LDAP/AD with custom attribute mapping
- Fine-grained authorization policies with resource servers

**Weaknesses**
- Operational complexity: clustering, database (PostgreSQL), session replication, upgrades
- Java/Quarkus: significant memory footprint; cold start latency in containerized environments
- Theme customization (Freemarker templates) is arcane; modern React-based login pages require significant work
- Community support is primary channel; Red Hat SSO (paid) for enterprise support

**Team fit**
- Platform/infrastructure teams at enterprises; regulated industries (finance, healthcare, government)
- Organizations with existing LDAP/Active Directory infrastructure

**Scale fit**
- Battle-tested at enterprise scale; proper cluster sizing required for high-availability

**Risks**
- Upgrade process between major versions (e.g., 20 → 25) has breaking changes requiring migration scripts
- Under-provisioned clusters suffer session replication lag under load
- Keycloak's admin API and event system are powerful but poorly documented

---

## WorkOS

**When to use**
- B2B SaaS selling to enterprise customers who require SSO (SAML/OIDC) per customer
- Need SCIM user provisioning/deprovisioning for enterprise IT departments
- Want enterprise features (SSO, Directory Sync, Audit Logs, Magic Auth) as a thin API layer over your existing auth
- Moving upmarket: adding enterprise features to an existing auth system without replacing it

**When NOT to use**
- Consumer (B2C) auth — WorkOS is purpose-built for B2B enterprise use cases
- Teams needing a complete auth system including user registration, password reset, social login as primary (WorkOS AuthKit does this but it's secondary to the enterprise story)
- Cost-sensitive: WorkOS pricing per SSO connection adds up at many enterprise customers
- Need self-hosting or data residency (WorkOS is SaaS only)

**Strengths**
- Fastest path to enterprise SSO: SAML, OIDC, Google Workspace, Okta, Azure AD out of the box
- SCIM: automated user provisioning and deprovisioning synced from enterprise IdPs
- Audit Log: structured, queryable audit trail API for compliance (SOC 2, ISO 27001)
- Admin Portal: embeddable SSO configuration UI your enterprise customers self-configure
- AuthKit: complete user authentication UI (magic links, social, MFA) if starting from scratch

**Weaknesses**
- Priced per SSO connection ($125–$400/month per connection depending on plan) — adds up with many customers
- Not suited for consumer auth or applications where most users aren't enterprise employees
- SaaS only; no self-hosting
- Newer entrant: ecosystem and community smaller than Auth0

**Team fit**
- B2B SaaS teams moving upmarket; sales-led growth companies adding enterprise tier
- Engineering teams that don't want to implement SAML themselves (nobody does)

**Scale fit**
- Scales to thousands of SSO connections; pricing scales with customer count

**Risks**
- Per-connection pricing model can be a blocker at high enterprise customer count
- Platform dependency for a critical feature (enterprise SSO) — evaluate long-term commitment

---

## Roll-Your-Own (OIDC / OAuth 2.0)

**When to use**
- Platform products that ARE an identity provider (SaaS offering OAuth apps, developer platforms)
- Full control over auth flows, token structure, storage, and security policies is a hard requirement
- Existing mature user database that cannot be migrated to a vendor
- Teams with deep security expertise building for regulated industries with custom compliance needs

**When NOT to use**
- Almost every other scenario — rolling auth is the highest-risk, highest-cost option for most teams
- Startups: auth is not your competitive advantage; use a vendor
- Teams without a dedicated security engineer — JWT, PKCE, token rotation, session fixation, CSRF are all real attack surfaces
- Need enterprise SSO/SAML quickly — implementing SAML correctly takes months

**Strengths**
- Complete control: token claims, session management, storage, rotation policy, MFA triggers
- No per-MAU pricing; costs are infra, not vendor fees
- Can be tailored to unique compliance, audit, or workflow requirements
- No vendor lock-in; portable to any stack

**Weaknesses**
- Security liability: sessions, CSRF, timing attacks, JWT algorithm confusion, PKCE — all must be implemented correctly
- Time to first login: weeks to months vs. hours with a vendor
- Ongoing maintenance: OAuth spec evolution, security patches, library updates, CVE monitoring
- SAML implementation is notoriously complex; most teams underestimate it

**Team fit**
- Platform/identity engineering teams with dedicated security expertise
- Companies building auth-as-a-product (e.g., Clerk, Auth0 themselves)

**Scale fit**
- Unlimited — you own the infrastructure

**Risks**
- Security vulnerabilities from implementation errors are the primary risk; the blast radius is catastrophic
- Regulatory compliance (SOC 2, HIPAA) requires audit logs, session management, and MFA that must all be hand-built

---

## Comparison Table

| Criterion | Auth0 | Clerk | Cognito | Firebase Auth | Supabase Auth | Keycloak | WorkOS | Roll-Your-Own |
|---|---|---|---|---|---|---|---|---|
| **Primary use case** | B2B/B2C enterprise | B2C/B2B SaaS (JS) | AWS mobile/web | Mobile (Google) | Supabase stack | Enterprise self-hosted | B2B enterprise SSO | Platform/special |
| **Self-hostable** | No | No | No | No | Yes | Yes | No | Yes |
| **SAML/Enterprise SSO** | Yes | Enterprise plan | Yes (complex) | No | No | Yes | Yes (core feature) | Custom |
| **Social OAuth** | 200+ providers | ~20 providers | Limited | Google + others | ~20 providers | Via brokering | Via existing auth | Custom |
| **Multi-tenant / Orgs** | Organizations | Organizations | Manual | Multi-tenancy (paid) | Manual | Realms | Directory Sync | Custom |
| **SCIM provisioning** | Yes | No | No | No | No | Yes | Yes | Custom |
| **MFA** | Many factors | TOTP, SMS | TOTP, SMS | TOTP, SMS | TOTP | TOTP, WebAuthn | TOTP | Custom |
| **Passkeys / WebAuthn** | Yes | Yes | No | No | No | Yes | No | Custom |
| **Session replay / anomaly** | Yes | Basic | Basic | No | No | Basic | No | Custom |
| **Pricing model** | MAU | MAU | MAU (cheap) | Free / per verification | MAU (free tier) | Free (self-host) | Per SSO connection | Infra cost |
| **DX / time to hello-world** | Hours | Minutes | Days | Hours | Hours | Days–weeks | Hours | Weeks–months |
| **Data ownership** | Vendor | Vendor | AWS | Google | Full (self-host) | Full | Vendor | Full |
| **License** | Proprietary SaaS | Proprietary SaaS | AWS service | Google service | Apache 2.0 | Apache 2.0 | Proprietary SaaS | Your choice |
| **Best for** | Enterprise B2B SaaS | JS/React product teams | AWS-native apps | Mobile/Google apps | Supabase full-stack | On-prem enterprise | Adding SSO to B2B | Platform builders |

---

## Recommended Combinations

| Combination | Why |
|---|---|
| **Clerk + Next.js App Router** | Fastest B2C/early-B2B SaaS auth: components, middleware, and RSC support work out of the box in minutes. |
| **Auth0 + WorkOS** | Auth0 handles consumer + regular business users; WorkOS handles per-enterprise SAML connections — clean separation of concerns. |
| **Supabase Auth + Supabase (Postgres + RLS)** | Unified backend: auth UID drives row-level security policies directly on Postgres tables; no extra auth hop. |
| **Cognito + AWS Amplify + API Gateway** | AWS-native mobile app: Amplify SDK, Cognito User Pool, API Gateway Cognito Authorizer — all first-party integrations. |
| **Firebase Auth + Firestore** | Mobile app rapid prototype: auth UID in Firestore security rules; no backend code for basic CRUD access control. |
| **Keycloak + LDAP/AD federation** | Enterprise intranet: sync employees from Active Directory, issue OIDC tokens to internal apps via single Keycloak realm. |
| **WorkOS + existing JWT auth** | Additive enterprise layer: keep current auth for regular users; WorkOS SSO for enterprise customers only — minimal migration. |
| **Auth0 Organizations + Stripe + Supabase** | B2B SaaS full stack: Auth0 handles per-org SSO, Stripe handles billing, Supabase handles data — each best-in-class in its lane. |

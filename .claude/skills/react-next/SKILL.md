---
name: react-next
description: >
  Activate when building, reviewing, or debugging a React + Next.js application.
  Covers App Router, Pages Router, rendering strategies, data fetching, state
  management, performance, and deployment. Trigger on any task that touches
  Next.js config, React components, or SSR/SSG/ISR decisions.
---

# React + Next.js Skill

**Scope: Next.js/React specifics. Generic web concerns → `.claude/skills/web/SKILL.md`.**

## When to use

- Creating or modifying Next.js pages, layouts, or API routes
- Choosing between SSR, SSG, ISR, or CSR for a given route
- Setting up data fetching with Server Components, `getStaticProps`, `getServerSideProps`, or React Query
- Configuring `next.config.js`, middleware, or image optimization
- Resolving hydration errors, layout shift, or bundle size regressions
- Integrating auth (NextAuth / Auth.js), i18n, or Edge runtime

## Workflow

1. **Confirm router strategy** — ask the owner whether the project uses App Router (`app/`) or Pages Router (`pages/`). Do not mix patterns in the same codebase.
2. **Classify rendering need per route**:
   - Purely static content → SSG (`generateStaticParams` / `getStaticProps`)
   - Data changes on every request → SSR (Server Component or `getServerSideProps`)
   - Revalidate on a schedule → ISR (`revalidate` option on `fetch` or `revalidate` export)
   - User-specific, post-login content → CSR inside a Client Component behind a loading boundary
3. **Scaffold the route**:
   - App Router: create `app/<segment>/page.tsx` + optional `layout.tsx`, `loading.tsx`, `error.tsx`, `not-found.tsx`
   - Pages Router: create `pages/<segment>.tsx`, separate `_app.tsx` / `_document.tsx` only when necessary
4. **Data fetching**:
   - Server Components: `await fetch(url, { next: { revalidate: N } })` directly in the component body
   - Client Components: `useSWR` or `@tanstack/react-query` with a thin `fetch` wrapper; never call a DB directly
   - Mutations: use Server Actions (`"use server"`) for form submissions; avoid round-trip API routes for simple mutations
5. **State management**:
   - Local UI state: `useState` / `useReducer`
   - Shared ephemeral state: React Context or Zustand (keep stores small and co-located)
   - Server-authoritative state: rely on revalidation (`revalidatePath`, `revalidateTag`) rather than client cache invalidation
6. **Styling**:
   - Prefer CSS Modules or Tailwind CSS; avoid global style side-effects in component files
   - Use `next/font` for web fonts to eliminate layout shift
7. **Images and media**: always use `next/image`; set explicit `width`/`height` or `fill` + `sizes`; never use raw `<img>` for user-facing content
8. **Bundle audit**: run `ANALYZE=true next build` (with `@next/bundle-analyzer`) before merging features that add new dependencies
9. **Deploy target check**: confirm Vercel, Docker (standalone output), or static export (`output: 'export'`). Edge runtime has no Node.js APIs — validate before using `runtime = 'edge'`.

## Standards

| Area | Do | Do not |
|---|---|---|
| Components | Prefer Server Components; add `"use client"` only when you need browser APIs or hooks | Mark every component `"use client"` by default |
| Data fetching | Co-locate fetch inside the component that needs it | Prop-drill data through many layers to avoid "extra fetches" |
| Env vars | Public vars → `NEXT_PUBLIC_*`; secrets stay server-side only | Import `process.env.SECRET` inside a Client Component |
| Dynamic routes | Use `generateStaticParams` for known slugs | Leave high-traffic pages fully dynamic when they could be static |
| Error handling | Add `error.tsx` boundaries per segment; log to observability service | Let unhandled promise rejections crash the route silently |
| Types | Use TypeScript strict mode; type all `params` and `searchParams` | Use `any` for Next.js page props |
| Metadata | Export `metadata` or `generateMetadata` from every public page | Set `<title>` inside `<head>` in JSX |

## Common mistakes to avoid

- **Mixing App Router and Pages Router** in the same route segment — they cannot coexist under the same path.
- **Calling `cookies()` or `headers()` in a cached Server Component** — this opts the component into dynamic rendering silently. Wrap in a dedicated Server Action or route handler.
- **Large Client Component boundaries** — importing a heavy chart library inside a component that only needs one hook forces the entire library into the client bundle. Split the hook into a tiny Client Component wrapper.
- **Missing `key` on list items or wrong key (index)** — causes React reconciliation bugs; use stable IDs.
- **Uncaught waterfall fetches** — sequential `await fetch` calls in a Server Component that could run in parallel. Use `Promise.all`.
- **`useRouter().push` in Server Components** — `useRouter` is a client hook; use `redirect()` from `next/navigation` on the server.
- **Forgetting to invalidate cache after mutation** — Server Actions must call `revalidatePath()` or `revalidateTag()` or the UI will show stale data.
- **Storing secrets in `next.config.js` `env` block** — they get bundled into the client. Use `.env.local` and server-side access only.

## Output format

Typical deliverables for a Next.js feature:

```
app/
  <feature>/
    page.tsx          # Server Component, data fetching at top
    layout.tsx        # Shared chrome (nav, breadcrumb)
    loading.tsx       # Suspense fallback UI
    error.tsx         # Error boundary with reset button
    _components/      # Private components (not routable)
      FeatureCard.tsx
    actions.ts        # Server Actions ("use server")
components/           # Shared Client Components
lib/
  <feature>.ts        # Pure data-access or business logic
```

Each file should include: TypeScript types for all props and return values, explicit revalidation strategy comment at the top of data-fetching files, and a brief JSDoc on exported functions.

## Related checklists

- `.claude/checklists/security.md`
- `.claude/checklists/performance.md`
- `.claude/checklists/accessibility.md`
- `.claude/checklists/production.md`

## Related agents

- `.claude/agents/stack/web/react-next-engineer.md`
- `.claude/agents/engineering/frontend-engineer.md`
- `.claude/agents/engineering/fullstack-engineer.md`
- `.claude/agents/quality/performance-engineer.md`
- `.claude/agents/quality/accessibility-auditor.md`
- `.claude/agents/quality/security-auditor.md`

---
name: vue-nuxt
description: >
  Activate when building, reviewing, or debugging a Vue + Nuxt application.
  Covers Nuxt 3 / Vue 3 Composition API, rendering modes, auto-imports,
  server routes, Nitro engine, state management with Pinia, and deployment.
  Trigger on any task touching Nuxt config, Vue components, or SSR/SSG decisions.
---

# Vue + Nuxt Skill

## When to use

- Creating or modifying Nuxt pages, layouts, components, or server routes
- Choosing between SSR, SSG, ISR (SWR in Nuxt), or SPA mode per route
- Setting up data fetching with `useFetch`, `useAsyncData`, or `$fetch`
- Configuring `nuxt.config.ts`, Nitro presets, modules, or middleware
- Integrating Pinia stores, i18n (`@nuxtjs/i18n`), or auth (`nuxt-auth-utils`)
- Resolving hydration mismatches, FOUC, or build-time type errors

## Workflow

1. **Confirm Nuxt version** — Nuxt 3 (Vue 3, Composition API) is the baseline. Do not mix Options API pages with Composition API composables without explicit justification.
2. **Classify rendering per route** using `routeRules` in `nuxt.config.ts`:
   - Static content → `{ prerender: true }`
   - Dynamic, revalidated on a schedule → `{ swr: 3600 }` (stale-while-revalidate seconds)
   - Always-fresh server-rendered → `{ ssr: true }`
   - Client-only (auth-gated dashboards) → `{ ssr: false }` or wrap with `<ClientOnly>`
3. **Scaffold the feature**:
   - Page: `pages/<segment>.vue` (auto-registered via file-system routing)
   - Layout: `layouts/<name>.vue`, applied with `definePageMeta({ layout: '<name>' })`
   - Components: `components/` (auto-imported, no explicit `import` needed)
   - Composables: `composables/use<Name>.ts` (auto-imported)
   - Server routes: `server/api/<endpoint>.ts` using `defineEventHandler`
4. **Data fetching**:
   - Inside `<script setup>` on a page: `const { data, error } = await useFetch('/api/endpoint', { key: 'unique-key' })`
   - For complex transforms: `useAsyncData('key', () => $fetch('/api/endpoint'))`
   - Client-only after mount: `onMounted` + `$fetch` or a reactive `watch`
   - Server routes: `$fetch` within `defineEventHandler`; use `readBody`, `getQuery`, `getCookie` from `h3`
5. **State management**:
   - Local reactive state: `ref` / `reactive` / `computed` in `<script setup>`
   - Shared cross-component state: Pinia store in `stores/<name>.ts`; use `storeToRefs` to destructure without losing reactivity
   - Server-to-client state: `useState('key', () => defaultValue)` for SSR-safe shared state
6. **Styling**: Scoped `<style scoped>` per component, or Tailwind CSS. Use `@nuxtjs/color-mode` for dark mode; avoid direct `document` access in SSR context.
7. **Auto-import awareness**: components, composables, and utils in their conventional folders are auto-imported. Do not re-import them manually — it creates duplicate module instances.
8. **Bundle audit**: run `nuxi analyze` before merging; watch for unintended client-bundle growth from server-only modules.
9. **Deployment**: set the correct Nitro preset (`vercel`, `netlify`, `node-server`, `static`) in `nuxt.config.ts`. The `static` preset disables server routes entirely.

## Standards

| Area | Do | Do not |
|---|---|---|
| Reactivity | Use `ref`/`computed` for primitives, `reactive` for objects; unwrap with `.value` consistently | Mix Options API `data()` with Composition API `setup()` in the same component |
| Fetching | Pass a unique `key` to every `useFetch` / `useAsyncData` call | Omit `key` — it causes duplicate requests and cache collisions |
| Server routes | Keep business logic in `server/services/`; handler files only parse input and call services | Put DB queries directly inside `defineEventHandler` |
| Secrets | Access `useRuntimeConfig().mySecret` only in server context | Expose secrets in `runtimeConfig.public` |
| Pinia stores | Define with `defineStore` using the Setup Store syntax; export typed refs | Use the Options Store syntax when the team has agreed on Setup syntax |
| Plugins | Register one concern per plugin file in `plugins/`; use `provide` / `inject` for DI | Do DOM manipulation in plugins without `import.meta.client` guard |
| Types | Run `nuxi typecheck`; all composable return types should be explicit | Rely solely on Nuxt's auto-generated `.nuxt/types` without checking |

## Common mistakes to avoid

- **Accessing `window` or `document` at module top-level** — Nuxt SSR runs on Node.js; guard with `import.meta.client` or `onMounted`.
- **Missing `key` on `useFetch`** — Nuxt deduplicates fetches by key; omitting it or reusing a key across unrelated calls serves stale data to the wrong component.
- **Mutating Pinia state outside an action** — breaks Vue DevTools tracking and can cause SSR state leakage between requests (each SSR request must have its own store instance via `defineStore` + Pinia's auto-injection).
- **Using `<ClientOnly>` as a hydration escape hatch** — it hides SSR/CSR mismatches instead of fixing them. Fix the root cause (usually a `Date.now()` or `Math.random()` call differing between server and client).
- **Importing a heavy library into a composable used on every page** — use dynamic `import()` inside the function body, or move it to a Nitro server route.
- **`routeRules` set to `{ prerender: true }` on a route with user-specific content** — prerenders one user's data for all users.
- **Forgetting `server: false` on Nitro plugins that use Node-only APIs** — causes build failures on edge runtimes.

## Output format

Typical deliverables for a Nuxt feature:

```
pages/
  <feature>/
    index.vue           # Page component with definePageMeta + useFetch
    [id].vue            # Dynamic segment
components/
  <Feature>/
    Card.vue            # Auto-imported, scoped styles
composables/
  use<Feature>.ts       # Reusable data + logic
stores/
  <feature>.ts          # Pinia store (Setup Store syntax)
server/
  api/
    <feature>/
      index.get.ts      # GET handler
      index.post.ts     # POST handler
  services/
    <feature>.ts        # Business logic, DB calls
```

Each Vue SFC includes `<script setup lang="ts">` with explicit prop types via `defineProps<{...}>()` and emits via `defineEmits<{...}>()`.

## Related checklists

- `.claude/checklists/security.md`
- `.claude/checklists/performance.md`
- `.claude/checklists/accessibility.md`
- `.claude/checklists/production.md`

## Related agents

- `.claude/agents/stack/web/vue-nuxt-engineer.md`
- `.claude/agents/engineering/frontend-engineer.md`
- `.claude/agents/engineering/fullstack-engineer.md`
- `.claude/agents/quality/performance-engineer.md`
- `.claude/agents/quality/security-auditor.md`

# Tech Stack

Opinionated. Use this unless the user's existing codebase makes it impossible. The "why" matters more than the version numbers — if something has moved on by the time you read this, keep the reasoning and pick the modern equivalent.

| Layer | Choice | Why |
|---|---|---|
| Framework | **Next.js 16 (App Router) + React 19 + TypeScript** | App Router gives you route-level loading/error boundaries and server components for free. React 19's compiler means fewer memo hand-offs. |
| Styling | **Tailwind CSS v4** | The Oxide engine is fast; native container queries replace a whole category of JS. Tokens live in CSS variables — easy theming. |
| Components | **shadcn/ui (Radix primitives)** | You own the code. Radix handles keyboard + a11y correctly, which is the whole reason we can promise "keyboard navigation works". |
| Server state | **TanStack Query v5** | Caching, refetch-on-focus, optimistic updates, invalidation. The canonical answer for "data from an API". |
| Server caching | **Next.js `use cache`** | Pair with TanStack Query — server caches the fetch, client caches the query. |
| Tables | **TanStack Table v8** | Headless. Filter / sort / paginate / select / column visibility all built in. Do not hand-roll. |
| Charts | **Recharts** (default) or **ECharts** (heavy data) | Recharts for normal business dashboards — declarative, small, good defaults. ECharts when the user says "real-time", "streaming", "millions of rows", or "financial tick data". |
| Forms | **React Hook Form + Zod** | Same Zod schema validates client and server actions. One source of truth for shape. |
| ORM | **Drizzle** | Edge-ready, lighter than Prisma, plays well with serverless. |
| Auth | **Clerk** or **Auth.js v5** | Clerk if the user wants RBAC + user management in an hour. Auth.js if they want self-hosted and full control. |
| AI | **Vercel AI SDK** | Only if the dashboard includes LLM features. Streaming, tool calling, UI state for AI — don't reinvent. |
| Rate limiting | **Upstash Redis** | Especially for AI endpoints. Cheap, edge-compatible. |

## Deviations worth making

- **Existing Vite/CRA app** → stay in Vite. Swap Next-specific bits (App Router, server components) for React Router + client-only fetching. Everything else (Tailwind, shadcn, TanStack, Zod, RHF) still applies.
- **No Supabase / different backend** → swap Drizzle for whatever the backend uses. The UI layer doesn't change.
- **User already has a component library** → use theirs. Do not introduce shadcn alongside another system. Consistency beats preference.

## Deviations not worth making

- Don't swap TanStack Query for SWR / Redux / Zustand for server data. You'll rebuild TanStack Query badly.
- Don't hand-roll tables. Ever.
- Don't use a chart library that doesn't render axes and gridlines by default. The chart minimums are not optional.

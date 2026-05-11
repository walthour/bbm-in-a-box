# Architecture

The point of this file is to make scaffolding decisions boring and consistent. Read it before you run `create-next-app`.

## File structure

```
app/
├── (dashboard)/
│   ├── layout.tsx          # Persistent sidebar + top bar, wraps all dashboard routes
│   ├── page.tsx            # Overview — the landing screen
│   ├── loading.tsx         # Route-level skeleton
│   ├── error.tsx           # Route-level error boundary
│   └── [entity]/
│       ├── page.tsx        # Entity list (table)
│       └── [id]/page.tsx   # Entity detail
├── api/                    # Route handlers only if you need them; prefer Server Actions
└── layout.tsx              # Root: providers (TanStack Query, Theme, Toaster)
components/
├── ui/                     # shadcn primitives (don't edit lightly)
├── layout/                 # Sidebar, TopBar, PageHeader
├── data/                   # KpiCard, DataTable, LineChart, BarChart
└── forms/                  # Reusable form fields
lib/
├── mock/                   # Phase 1 fixtures + fake query fns (entities.ts, queries.ts)
├── db/                     # Phase 2: Drizzle schema + client
├── queries/                # TanStack Query keys + query/mutation fns
├── schemas/                # Zod schemas (one source of truth for shapes)
└── utils.ts
```

## Server vs client components — the rule

- **Default to server components.** They ship less JS and can fetch directly.
- **Add `"use client"` only when you need:** state, effects, event handlers, browser APIs, TanStack Query hooks, or Radix interactive primitives.
- **Pattern:** server component fetches initial data and passes it into a client component that hydrates TanStack Query with `initialData`. Best of both worlds — fast first paint, client-side cache after.

## Route boundaries

Every route that fetches data gets a `loading.tsx` (skeleton) and an `error.tsx` (recoverable). Don't skip these — they are the perceived-performance win.

## Providers

Root `layout.tsx` wraps children in:
1. `QueryClientProvider` (TanStack Query)
2. `ThemeProvider` (next-themes, if dark mode)
3. `Toaster` (shadcn sonner)

One `QueryClient` per request on the server, one singleton on the client. Use the standard Next.js + TanStack pattern — don't invent.

## Phase 1 mock query layer

Write `lib/queries/entities.ts` with functions like `fetchUsers()`, `createUser()`. In Phase 1 these read/write `lib/mock/`. In Phase 2 they hit Supabase via Drizzle. **Component code never changes between phases.** That is the whole point of the abstraction.

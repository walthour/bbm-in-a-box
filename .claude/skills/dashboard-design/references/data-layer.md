# Data Layer (Phase 1 Mock → Phase 2 Supabase)

The key idea: components never know whether data is mock or real. The swap happens in one place.

## Phase 1 — mock query layer

In `lib/mock/` put typed fixtures (e.g., `users.ts`, `orders.ts`) and a tiny delay helper to simulate latency. In `lib/queries/` define query/mutation functions that read from those fixtures:

```ts
// lib/queries/users.ts (Phase 1)
import { users } from "@/lib/mock/users";
import { sleep } from "@/lib/mock/utils";

export async function fetchUsers() {
  await sleep(300);           // simulate network so skeletons appear
  return users;
}

export async function createUser(input: NewUser) {
  await sleep(400);
  const user = { id: crypto.randomUUID(), ...input };
  users.push(user);
  return user;
}
```

Components consume these via TanStack Query:

```ts
useQuery({ queryKey: ["users"], queryFn: fetchUsers });
```

## Phase 2 — Supabase swap

In Phase 2 the same file is rewritten to hit Drizzle + Supabase. **No component changes. No query-key changes.**

```ts
// lib/queries/users.ts (Phase 2)
import { db } from "@/lib/db";
import { usersTable } from "@/lib/db/schema";

export async function fetchUsers() {
  return db.select().from(usersTable);
}
```

That's the whole migration. If you find yourself changing component code in Phase 2, the Phase 1 abstraction was wrong — fix it there.

## Caching rules (TanStack Query)

- **staleTime**: 30s default for most queries. Longer (5m) for slowly-changing metadata. 0 for real-time feeds.
- **refetchOnWindowFocus**: `true` — users coming back to a tab expect fresh data.
- **refetchOnMount**: default; rely on staleTime.
- **Invalidate on mutation**: after `createUser`, invalidate `["users"]`. Use predicates for broader invalidation sparingly.
- **Query keys**: stable array shapes. `["users", { page, filter }]` not `["users-page-" + page]`.

## Refresh strategy — choose deliberately

- **Polling** (`refetchInterval`) — simple and fine for most dashboards. Use 30s-5m depending on data freshness needs.
- **Realtime / websocket** — only if the user asked for it, or the data changes constantly (chats, live feeds). Supabase Realtime channels + `queryClient.setQueryData` on event.
- **Manual refresh** — a refresh button in the page header. Always provide this as an escape hatch even when polling is on.

## Supabase specifics (Phase 2)

- Use Drizzle's `postgres-js` or `node-postgres` driver pointed at Supabase's connection string. Pooler URL for serverless.
- RLS **on** for every table. Do not rely on UI filtering for security.
- Auth: match the choice in `tech-stack.md`. If using Supabase Auth, issue a server-side client per request. If using Clerk, pass the Clerk user id into RLS policies.
- Secrets live in `.env.local` — never import them into client components. If you see a `process.env.SUPABASE_SERVICE_ROLE_KEY` in a file with `"use client"`, that's a bug.
- Server Actions are the preferred mutation path in App Router. They give you the Zod schema reuse for free.

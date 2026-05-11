---
name: dashboard-design
description: Build production-grade data dashboard web apps that are calm, clear, fast, and data-first. Use this skill WHENEVER the user mentions building a dashboard, admin panel, analytics view, KPI page, internal tool, metrics UI, data visualization app, reporting interface, or anything resembling a "tool to view data" — even if they don't say the word "dashboard". Also use when redesigning, cleaning up, or upgrading an existing dashboard. This skill drives the entire build (scaffold, components, states, interactions) using an opinionated stack and a senior-bar design philosophy. Phase 1 is design/scaffold with mock data; Phase 2 (optional) wires it to Supabase.
---

# Dashboard Design

Your job is to **build** dashboards, not describe them. This skill gives you an opinionated stack, a senior-level design philosophy, and a workflow that produces dashboards which feel calm, trustworthy, and fast.

## Philosophy

Three rules. Re-read them whenever you're making a design choice:

1. **This is a tool, not a marketing page.** No oversized hero banners, no decorative gradients, no "delight" that competes with data.
2. **The UI should disappear; the data is the hero.** Navigation frames content, it does not compete with it. Accents reinforce hierarchy, not decorate.
3. **Trust is built through feedback.** Every interaction must acknowledge intent immediately, show outcome clearly, and behave consistently. Optimistic updates, skeletons, toasts — always.

If an element doesn't help the user scan, decide, or act, remove it.

## Two-phase workflow

Dashboards usually have two distinct stages. Do Phase 1 first and stop. Only proceed to Phase 2 when the user confirms the design is right and tells you to wire up data.

### Phase 1 — Design & scaffold (mock data)

The goal of this phase is a fully navigable, pixel-tight dashboard running on typed mock data. No database. No auth. This lets the user evaluate the design without worrying about integration.

1. **Clarify intent.** Ask (briefly):
   - Who uses this and what decision are they making?
   - What is the single most important insight on the landing screen?
   - What are the 3–7 data entities? (e.g., Users, Orders, Campaigns)
   - Roughly how many rows/metrics — small (<1k) or large/streaming?
2. **Scaffold.** `create-next-app` with TypeScript, Tailwind v4, App Router. Install `shadcn/ui`, TanStack Query, TanStack Table, Zod, React Hook Form, Recharts (switch to ECharts if the user said "large/streaming"). Set up `/app/(dashboard)/layout.tsx` with a persistent, quiet left sidebar.
3. **Generate typed mock data.** Put realistic fixtures in `lib/mock/` with Zod schemas. The UI reads from a fake query client — the same TanStack Query calls that will later hit Supabase. This is critical: the swap in Phase 2 must be a one-line change.
4. **Build the Overview page** with these required deliverables:
   - KPI cards (4 max, one dominant insight first)
   - A TanStack Table with filter, sort, pagination, row selection, and a contextual bulk-action toolbar
   - One line chart + one bar chart (axes, labels, tooltips, gridlines — always)
   - A create/edit flow using a Radix Dialog, React Hook Form, Zod validation, and an optimistic update
5. **Implement every state** for every data region: loading (skeleton), empty (with CTA), error (recoverable with retry), success (toast). Users should never wonder "did that work?"
6. **Run the audits** in `references/ui-hierarchy.md` and `references/interaction-trust.md` against the result. Fix what fails.
7. **Run the quality gate** (below). If it doesn't pass, iterate before handing off.

**Stop here.** Show the user. Do not touch Supabase until they confirm.

### Phase 2 — Wire to data source (on request)

Only when the user says "connect it" or similar. Read `references/data-layer.md`. Replace the mock query functions with real ones. Keep the exact same shapes so no component code changes. Handle auth, RBAC server-side, and the security defaults in `references/security.md`.

## Required stack

Defined in `references/tech-stack.md`. Deviate only if the user explicitly asks, or if a requirement makes it impossible (e.g., they already have a Vite app). Summary: **Next.js 16 App Router, React 19, TypeScript, Tailwind v4, shadcn/ui, TanStack Query v5, TanStack Table v8, Recharts (or ECharts for heavy data), Zod + React Hook Form, Drizzle ORM, Clerk or Auth.js v5.**

## State separation (non-negotiable)

- **Server state** → TanStack Query. Single source of truth for any data that came from an API.
- **UI state** → local component state (`useState`). Modals open/closed, hover, expanded rows.
- **Form state** → React Hook Form.

Never duplicate server data into component state. Never store UI state in the query cache.

## Quality gate

Before declaring Phase 1 done, verify all of these. If any fail, fix before handing off:

- [ ] A new user understands the page in **under 10 seconds**
- [ ] The most important insight is visually dominant on first glance
- [ ] The sidebar is quiet — lower contrast than content, no competing focal point
- [ ] Only **one** accent color used for primary actions/active states
- [ ] Every table has filter + sort + pagination + bulk actions
- [ ] Every chart has axes, labels, values, gridlines, and hover tooltips
- [ ] Every data region has loading, empty, error, and success states implemented
- [ ] Every mutation is optimistic with rollback on failure
- [ ] Keyboard navigation works (Radix primitives give this for free — verify, don't assume)
- [ ] No decorative elements that don't improve understanding

## Reference files — read when relevant

- `references/tech-stack.md` — the stack, versions, and the "why this not that" reasoning. Read at the start of Phase 1.
- `references/architecture.md` — App Router layout, server vs client components, route boundaries, file structure. Read before scaffolding.
- `references/ui-hierarchy.md` — focus, sidebar audit, navigation discipline, color restraint. Read before building the layout and again as an audit pass.
- `references/interaction-trust.md` — modals vs popovers, optimistic updates, all four states, feedback patterns. Read before building interactive elements and again as an audit pass.
- `references/tables-and-charts.md` — TanStack Table patterns, Recharts vs ECharts decision, chart minimum requirements. Read when implementing tables or charts.
- `references/data-layer.md` — data entities, caching rules, refresh strategy, and the Phase 2 Supabase wiring pattern. Read in Phase 2 (or when designing the mock query layer in Phase 1 so the swap is painless).
- `references/security.md` — server-side RBAC, Zod validation, OWASP defaults, rate limiting, audit logging. Read in Phase 2.

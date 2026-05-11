# Interaction, Feedback & Trust

Read before you wire up interactive elements. Read again as an audit pass.

## Core principle

**Trust is built through clear intent, immediate feedback, and consistent behavior.** After any action a user should think: "the system understood me, responded clearly, and will behave the same way next time." If any of those three is shaky, the trust is broken.

## Intent before action

For every interactive element, the user should know three things *before* they click:
1. **What will happen.** Labels are verbs ("Delete 3 rows" beats "Delete").
2. **When it will happen.** Instant? Confirmation required? Async with a toast later?
3. **Whether it can be undone.** If no — say so and require a second step.

If an action is ambiguous, surprising, or irreversible without warning — it's a bug. Fix it.

## Modals vs popovers vs inline

Pick by intent, not by convenience. Misuse is the most common interaction bug in dashboards.

| Use | When |
|---|---|
| **Dialog (modal)** | Blocking decisions, destructive actions, multi-step forms, high-commitment tasks. Interrupts the user — justify the interruption. |
| **Popover** | Quick filters, display options, small non-blocking actions. Low risk, easy to dismiss. |
| **Inline edit** | Single-field quick edits (rename, toggle). No ceremony. |
| **Drawer / Sheet** | Longer detail views or multi-field edits that benefit from staying next to the list. |

Wrong fit = broken trust. A modal for toggling a filter feels heavy. A popover for deleting a user feels reckless.

## Filters, sorting, bulk actions

- **Active state visible.** A filter chip, a highlighted sort arrow — the user should never wonder if a filter is on.
- **Result scope obvious.** "Showing 12 of 240" — always.
- **Bulk actions appear contextually.** The toolbar reveals itself when rows are selected; it disappears on deselect. Don't permanently reserve space for bulk-action buttons.
- **Destructive bulk actions require confirmation** with explicit count: "Delete 12 users? This cannot be undone."
- **Success and failure both get feedback.** Toast on success, toast + inline error on failure.

## Optimistic updates

Every common mutation updates the UI immediately and rolls back on failure. Use TanStack Query's `onMutate` / `onError` pattern or React's `useOptimistic`. The rule: **if the action will succeed 95%+ of the time, do it optimistically.** Destructive actions are the exception — they should confirm first, then execute with normal loading state.

## The four states (for every data region)

Every component that displays fetched data must handle all four. No exceptions — this is where dashboards most commonly feel broken.

1. **Loading** — skeleton that matches the eventual layout. Not a spinner in the middle of a box. The shape should look like the real thing so nothing jumps.
2. **Empty** — a clear explanation of why it's empty and a CTA to fix it ("No users yet. Invite your first.").
3. **Error** — explain what went wrong (briefly, no stack traces), explain what the user can do ("Retry" button), never blame them.
4. **Success** — data rendered. Mutations get a toast confirming the outcome.

## Feedback rules

- **Acknowledge input immediately.** The button shows a loading state the moment it's clicked. Not after the network response.
- **Toasts confirm outcomes, not actions.** "User created" not "Creating user…".
- **Don't stack toasts.** Collapse related ones. Autodismiss success in 3–4s; errors stay until dismissed.
- **Errors explain + recover.** Always pair a what with a next-step.

## Speed & consistency

- Interactions feel fast → optimistic updates + skeletons.
- Similar actions behave the same → if deleting a user requires confirmation, deleting a project does too.
- No "uncertain" UI → never leave the user staring at a button wondering if it did anything.

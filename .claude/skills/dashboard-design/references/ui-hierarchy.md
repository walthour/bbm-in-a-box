# UI Hierarchy, Focus & Navigation

Read this before you build the layout. Then read it again as an audit pass when Phase 1 is "done" — you'll catch things the first pass missed.

## Core principle

**The UI should point toward the data, not compete with it.** If you're adding something that draws the eye away from the numbers, stop.

## Primary focus

Every screen supports one most-important decision or insight. Identify it before you place anything.

- That element is visually dominant on first glance (size, contrast, position — upper-left or upper-center).
- Everything else clearly supports or defers to it.
- There is never more than one dominant focal point per screen.

**Test:** squint at the screen. What do you see first? If it's not the thing that matters most, rework the hierarchy.

## Sidebar audit

Sidebars are where dashboards most often go wrong. They get loud, they get cluttered, they start competing with the content.

- **Purpose.** Every sidebar must have one clear purpose: global navigation, local navigation, utilities, or context. If you can't name it in one word, it shouldn't exist.
- **Visual weight.** Lower contrast than content. Lighter type. Muted icons. The sidebar frames the content — it is not the content.
- **Item priority.** If an item isn't used weekly, it probably belongs in a submenu or settings. Group related items. Enforce hierarchy.
- **Active state.** Subtle. A soft background or a left border indicator. Never a loud accent block that pulls the eye away from the main content.
- **Discoverability vs noise.** If something needs constant visibility, justify why. Otherwise, collapse or progressively disclose.

## Navigation discipline

- **Separate global from local.** Global nav (top-level routes) lives in the sidebar. Local nav (tabs within a page) lives inline with the page content. Do not mix.
- Nav exists to orient, not to decorate. No icons larger than they need to be. No marketing copy in nav items.

## Color & tokens

- **Neutral base, one accent.** The dashboard is mostly grays/whites (or grays/blacks in dark mode). A single accent color reinforces primary actions, active states, and the one dominant chart element. Nothing else.
- **System colors are for state only.** `red` = error/destructive. `green` = success. `amber` = warning. Never use these decoratively. Never use color as the *only* signal — pair with icon or label (a11y).
- **Contrast.** WCAG AA minimum. If you can't read it at a glance, it doesn't belong.
- **Tokens live in CSS variables** (Tailwind v4 makes this easy). Theming = changing variables, not hunting hex codes.

## Visual restraint

- Kill decorative elements that don't improve understanding. Drop shadows, gradient borders, illustrative icons on every card — all suspect.
- De-emphasize secondary info via scale, contrast, and spacing — not color.
- Whitespace is a feature. Crowded dashboards feel anxious.

## The 3-second test

At a 3-second glance, a user should know:
1. What matters most on this screen
2. Where to look next
3. What action or insight comes next

If the answer to any of those is unclear, the hierarchy is broken. Fix it before shipping.

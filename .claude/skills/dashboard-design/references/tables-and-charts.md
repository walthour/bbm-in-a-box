# Tables & Charts

Tables and charts are where dashboards earn their keep. Do these well and the rest of the work shows.

## Tables — always TanStack Table v8

Never hand-roll. TanStack Table is headless, so you pair it with shadcn table primitives for styling and own the result.

Required features on every table:

- **Search / filter** — a top-level text search plus column filters for categorical fields.
- **Sort** — click any column header. Show current sort direction clearly but subtly.
- **Pagination** — client-side for <1k rows, server-side above that. Show "12 of 240".
- **Row selection** — checkboxes in the first column. Selecting any row reveals a contextual toolbar with bulk actions. Toolbar disappears when deselected.
- **Column visibility** — a popover to show/hide columns. Persist preference to localStorage.
- **Responsive columns** — hide less-critical columns below narrow widths. Don't let the table overflow its container.
- **Empty, loading, error states** — match the rest of the app.

Row click opens a detail view (drawer or route). Don't make users hunt for "view". Inline edits use a popover or inline field — not a modal.

## Charts — functional, not flashy

Use **Recharts** by default. Switch to **ECharts** only if the user said "real-time", "streaming", "tick data", or "millions of points".

Only two chart types on the Overview page: **line** and **bar**. Pie charts, radial gauges, and fancy radars all lose to a bar chart in a dashboard context. If the user asks for something exotic, push back unless they have a real reason.

### Non-negotiable chart requirements

Every chart ships with:

- **Axes** — labeled, with units ("USD", "%", "sessions")
- **Gridlines** — light, so values are scannable
- **Value labels or a clear scale** — users should be able to read approximate numbers without hovering
- **Hover tooltips** — exact values, formatted, with context (date + category)
- **Legend** — only if there are 2+ series
- **Empty state** — "No data for this range" with a way to widen the range
- **Loading state** — skeleton in the chart's shape, not a spinner

### Color in charts

- Use the **single accent** for the primary series.
- Use neutral grays for comparison series (previous period, benchmark).
- Never use red/green to distinguish arbitrary series — those are reserved for state (up/down, good/bad).
- Colorblind-safe. Never rely on color alone — use dash patterns or labels.

### Chart sizing

- Charts need room to breathe. A 200px-tall line chart on a dashboard looks starved.
- Aspect ratio: roughly 16:9 or wider for line charts; shorter and denser for sparklines.
- Don't cram 6 charts onto one screen. Two to four, max.

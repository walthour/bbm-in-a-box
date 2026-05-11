# Memory Map

Index of what lives where. **Memory holds operator state about the workspace or a project** — decisions, current strategy, sessions, ideas, project kickoffs. Business assets live under `active/`. Claude-CLI config lives under `.claude/`.

## Where `memory/` exists

Memory subtrees can exist at three levels:

- **Workspace `memory/`** (this folder) — operator state for the workspace as a whole. The workspace is a container, not a project, so it has no `project-brief.md`.
- **Container `memory/`** — parent folders that hold many projects can also have their own `memory/` for cross-cutting state that doesn't fit inside any single child. Example: `active/clients/memory/` would track patterns across all clients ("Shopify migrations keep tripping on X"). Containers have no `project-brief.md` either.
- **Project `memory/`** — each project folder carries its own `memory/` plus `project-brief.md` (the frozen kickoff). A folder qualifies as a "project" when it could plausibly stand alone as its own little workspace — client engagements, individual apps, CRM prospects, individual website projects.

Skills (`.claude/skills/{slug}/`) do NOT get `memory/` — they're libraries of capability, not engagements with accumulating state.

## Folders inside `memory/`

| Folder | What goes there | File shape |
|---|---|---|
| `decisions/` | Point-in-time choices that won't be revisited | File-per-entry, dated, full frontmatter |
| `sessions/` | Wrap-up summaries of long Claude Code sessions | File-per-entry, dated, full frontmatter |
| `meetings/` | Distilled notes from human conversations / Fathom calls — *client + agency levels only, not workspace* | File-per-entry, dated, full frontmatter |
| `ideas/` | Proposals for future projects that don't have a folder yet | Single file per idea. Promote to `project-brief.md` when the project's folder is scaffolded |
| `current/` | Mutable single-file state | Single files, overwrite or append-and-prune |

Project folders also have:

| File | What it tracks | Pattern |
|---|---|---|
| `project-brief.md` | The frozen kickoff for that specific project | Single file, written once at scope-freeze, edited only if scope changes |

## Single files in `current/`

| File | What it tracks | Pattern |
|---|---|---|
| `current-strategy.md` | What I'm working on right now and how I'm approaching it | Overwrite — snapshot, not a log |
| `next-actions.md` | Punch list of things to do | Append + prune when done |
| `bugs-and-risks.md` | Open issues, watch-outs, things to monitor | Append + prune when resolved |

## Frontmatter for `decisions/`, `sessions/`, and `meetings/`

```yaml
---
id: DEC-2026-01-15-pricing-change            # {TYPE}-{ISO-DATE}-{slug}
type: decision                                # decision | session | meeting
date: 2026-01-15                              # ISO-8601 only — no "January 2026"
client: null                                  # slug only ("acme-co"), or null for cross-cutting
tags: [pricing, packaging]
status: active                                # active | superseded | rejected
related: []                                   # other entry IDs (graph edges)
---
```

`meetings/` entries add `participants: [...]` and an optional `fathom_url:` field. Body holds distilled highlights (decisions, action items, anything directional) — never a transcript dump.

**Strict shapes matter.** `id`, `client`, `type`, `date`, `status` are designed to become Postgres-indexed filter columns when RAG ships. Slugs not free text, ISO dates not "January 2026", closed enums.

## Where things go (lookup table)

| Situation | Where |
|---|---|
| "Always do X / never do Y" rule | `CLAUDE.md` (workspace) or client `CLAUDE.md` |
| Path-specific rule (only fires for one folder) | `.claude/rules/{topic}.md` with `paths:` frontmatter |
| Made a choice, won't revisit | `memory/decisions/YYYY-MM-DD-slug.md` |
| What I'm working on right now | `memory/current/current-strategy.md` |
| Punch-list item | `memory/current/next-actions.md` |
| Open issue, risk, watch-out | `memory/current/bugs-and-risks.md` |
| Wrap-up of long session | `memory/sessions/YYYY-MM-DD-slug.md` |
| Distilled notes from a human meeting | `memory/meetings/YYYY-MM-DD-slug.md` (client level only) |
| Idea / proposal for a not-yet-scaffolded project | `memory/ideas/{slug}.md` |
| Frozen kickoff for an existing project folder | That project folder's `memory/project-brief.md` |
| Client-specific anything | The client's own `memory/` subtree (same shape) |

## Per-project memory

Every project folder gets its own `memory/` with this shape:

```
{project-folder}/
└── memory/
    ├── project-brief.md       # frozen kickoff for this project
    ├── decisions/             # project-specific decisions
    ├── sessions/              # session wrap-ups within this project's scope
    ├── meetings/              # distilled notes from human meetings (client level only)
    └── current/
        ├── current-strategy.md
        ├── next-actions.md
        └── bugs-and-risks.md
```

When working in a project folder, only that project's `memory/` is in Claude's natural reach. Sibling projects are invisible until you `cd` into them.

## Per-container memory

Containers like `active/clients/` and `active/crm/` can have their own `memory/` for *cross-cutting* state — observations, decisions, or patterns that span multiple children. Shape is the same as workspace memory (no `project-brief.md`).

If state is specific to *one* child, put it in that child's `memory/` instead.

## Lifecycle of an idea → project

1. **Idea phase:** write to `memory/ideas/{slug}.md`. May be informal — scope, motivation, sketch.
2. **Approval:** decide to do it. Pick a permanent folder location.
3. **Promotion:** scaffold the project folder with its own `memory/` subtree, move the idea file in as `project-brief.md`, edit it to "freeze" the scope.
4. **Project runs:** decisions, sessions, current state accumulate in the project's own `memory/`.

## RAG-readiness (future)

The frontmatter conventions here are designed so a future ingestion pipeline (e.g. Supabase pgvector + embeddings + hybrid search) can use `id`, `client`, `type`, `date`, `status` as **filter columns** rather than embed them as text. No RAG stack is being chosen now. The structure is ready when you are.

---
description: Wrap up the current conversation as a session record, and surface any other memory entries (decisions, ideas, project briefs, mutable state) that should be written or updated.
---

Wrap up the current conversation as a session record, and **surface any other memory entries that should be written or updated as a result of what happened**. A session file alone is not enough — decisions, ideas, and current state often need to live in their own places per the memory model in `memory/MAP.md`.

If the user passed a slug as `$ARGUMENTS`, use it as the session slug; otherwise infer one from the conversation.

## Step 1 — Determine scope

Decide whether this session is **workspace-level** or **project-scoped**:

- **Workspace-level** if the work touched multiple projects, the workspace structure itself, bundled skills, cross-cutting conventions, or operator memory at the workspace root. Save to `memory/sessions/`.
- **Project-scoped** if the work was clearly inside a single project's context (a client engagement, a CRM prospect, an app, an individual website project). Save to `{project-folder}/memory/sessions/`.

Note: "project" is broader than "client." A CRM prospect's work is project-scoped. So is work focused on a single app or a single website build.

If unclear, ask the user: "Save this to workspace memory or to {project}'s memory?" and wait.

## Step 2 — Survey the session

Before writing anything, scan what happened in this conversation and surface candidates for each of these. Don't write them yet — just identify.

For each category, the question to ask:

| Category | Question | If yes, lands in |
|---|---|---|
| **Decisions** | Did the user (or you, with their approval) commit to a choice that will govern future work? Not just "today we did X" but "going forward we do X." | `memory/decisions/YYYY-MM-DD-{slug}.md` |
| **Ideas** | Did a proposal surface for a future project that doesn't have a folder yet? (e.g., "we should build a tool that does X") | `memory/ideas/{slug}.md` |
| **Project briefs** | Did we scaffold a new project folder this session, with a clear initial scope? | That project folder's `memory/project-brief.md` |
| **Current strategy** | Did the workspace or a project's "what I'm working on" snapshot change? Did something ship? | `memory/current/current-strategy.md` (workspace) or `{project}/memory/current/current-strategy.md` |
| **Next actions** | Did new punch-list items emerge? Or did existing ones get completed? | `current/next-actions.md` at the right level |
| **Bugs & risks** | Did a watch-out or open issue surface? Or get resolved? | `current/bugs-and-risks.md` at the right level |

Heuristics for the judgment calls:

- **Decision vs. routine action.** A decision is forward-looking ("we'll standardize on X"). Routine completion of a task ("today we shipped Y") is not a decision unless it implies a new rule.
- **Idea vs. next action.** An idea is "we might do X someday in a new folder." A next action is "we should X this week." If the project doesn't exist yet, it's an idea.
- **Material enough for its own file?** A decision warrants its own file when it would change how a future-you (or an LLM in RAG) acts. If a stranger reading the codebase would derive the rule from the code itself, it's probably not material enough for its own decision file.

**Tell the user what you found before writing.** Example: "I found 2 decisions worth recording, 1 idea, and updates to current-strategy + next-actions. Proceed?"

## Step 3 — Choose the slug and filename

If the user passed a slug via `$ARGUMENTS`: use that (lowercase, hyphenated, ≤6 words).

If no argument: infer from the conversation. 2–4 words capturing the essence. Lowercase, hyphenated, no dates.

Examples: `workspace-restructure`, `klaviyo-deliverability-debug`, `pricing-decision`, `memory-model-refinement`.

Filename format: `{YYYY-MM-DD}-{slug}.md`.

Full path:
- Workspace: `memory/sessions/{YYYY-MM-DD}-{slug}.md`
- Project: `{project-folder}/memory/sessions/{YYYY-MM-DD}-{slug}.md`

## Step 4 — Write the decision files (if any)

For each material decision identified in Step 2:

- **If a decision file already exists** for this choice, don't duplicate. Note the existing `id` so the session can link to it in its `related:` frontmatter.
- **If not yet recorded**, write a separate file at `memory/decisions/{YYYY-MM-DD}-{slug}.md` (workspace) or `{project}/memory/decisions/{YYYY-MM-DD}-{slug}.md`.

Frontmatter:

```yaml
---
id: DEC-{YYYY-MM-DD}-{slug}
type: decision
date: {YYYY-MM-DD}
client: {client-slug or null}
tags: [closed enums — see memory/MAP.md]
status: active
related: [other entry IDs as graph edges]
---
```

Body sections (use what's relevant):

```markdown
# {Decision title — plain English}

## What changed
## Why
## What was rejected (alternatives considered)
## What didn't change
## Open follow-ups
```

The decision's `id` will appear in the session's `related:` frontmatter so they cross-link.

## Step 5 — Write the idea files (if any)

For each surfaced proposal that doesn't have a folder yet, write `memory/ideas/{slug}.md`. Frontmatter is optional / light:

```yaml
---
date: {YYYY-MM-DD}
---
```

After the frontmatter, capture:

- What it is (one line)
- Motivation / problem it solves
- Rough scope sketch
- Open questions
- When it'd graduate to a project (i.e., what's the trigger to scaffold its folder?)

## Step 6 — Write the project-brief.md (if a new project was scaffolded)

Only if Step 2 surfaced a new project folder this session. Write `{project-folder}/memory/project-brief.md`. The body covers what the project is, scope / definition of done, key constraints, and initial decisions baked in. Single file, written once, edited only if scope changes.

## Step 7 — Write the session file

Frontmatter:

```yaml
---
id: SES-{YYYY-MM-DD}-{slug}
type: session
date: {YYYY-MM-DD}
client: {client-slug or null}
tags: [up to 5 — what this touched]
status: active
related: [IDs of decisions/ideas/briefs from Steps 4-6, plus any pre-existing entries touched]
---
```

Body (skip sections that don't apply):

```markdown
# {Session title — what we did, in plain English}

## Context
One paragraph: why this session happened, what the starting state was.

## What we did
Bullet list of concrete things accomplished. Reference files created or significantly changed.

## Decisions made
- Link to each new decision file from Step 4 (by ID + path)
- For decisions in-flight but not yet recorded as separate files, note them and explain why (e.g., "still iterating, will record once frozen")

## Ideas surfaced
- Link to each new idea file from Step 5

## Open questions / next steps
What's unresolved. Cross-reference `current/next-actions.md` if items were added there.

## Watch-outs
Anything the future-reader should know that's not obvious from the diffs.

## Files changed
Compact list — paths only.
```

## Step 8 — Update mutable state (deliberate, not optional)

This step is **not optional** — actually check each of these and update if relevant. If genuinely nothing to add for a given file, say so explicitly.

**Every time you edit a `current/*` file (current-strategy.md, next-actions.md, or bugs-and-risks.md), update the `<!-- last-touched: -->` HTML comment at the top of the file.** If the file doesn't have one yet, add it as the first line:

```html
<!-- last-touched: {YYYY-MM-DD} -->
```

If it already exists, replace it. This makes "when was this last refreshed" visible at a glance.

For the **scope level you're saving to** (workspace OR project — same level as the session file):

- `current/current-strategy.md` — append to "Recently shipped" if work shipped; update "In progress" sections if state changed; refresh the `*Last updated:*` date.
- `current/next-actions.md` — append new items; mark or prune completed items.
- `current/bugs-and-risks.md` — add new watch-outs; move resolved items to "Resolved (recent)" with a date.

For **cross-cutting effects** (work that touched other projects' state):
- Update those projects' `current/*.md` files too. E.g., if a workspace-level decision affects a specific client, touch that client's `memory/current/current-strategy.md`.

Show the user each file you're about to update with a one-line summary before applying.

## Step 9 — Confirm

Tell the user:
- Where the session file was saved (full path)
- What other files you created (decisions, ideas, briefs) with their paths
- What mutable files you updated, with one-line summaries
- A 1–2 sentence summary of the session itself

Keep this terse — they want to know what landed, not re-read the session.

---

## Quick reference: which file does this go in?

```
A point-in-time choice that will govern future work        → decisions/{slug}.md
A proposal for a future project (no folder yet)            → ideas/{slug}.md
The frozen kickoff of an existing project folder           → that project's project-brief.md
What I'm working on right now (snapshot)                   → current/current-strategy.md
A new punch-list item                                      → current/next-actions.md
An open issue or watch-out                                 → current/bugs-and-risks.md
A wrap-up of this conversation                             → sessions/{date}-{slug}.md
```

If a session would have produced more than one of these in the past but you only wrote a session file, you missed information. The session file is the entry point — but it should link out to where the durable knowledge lives.

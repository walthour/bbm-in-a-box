# Your Business Command Center

An AI-powered workspace for running and growing your business with Claude Code. Holds your brand profile, client work (if you do client work), apps and websites you build, skills Claude can use, and a persistent memory system that lets Claude pick up where you left off across sessions.

## Structure

```
/                     # Root — keep clean. Never store scripts, data, or temp files here.
├── CLAUDE.md         # This file — workspace operating manual
├── GEMINI.md         # Gemini instructions (mirrors this)
├── BRAND.md          # Your brand profile — voice, audience, products, visuals
├── ONBOARDING.md     # One-time setup script (move to .tmp after running)
├── README.md         # Public README for the repo
├── .env              # API keys and environment variables (you create this)
├── .tmp/             # Scratch space for temporary files
├── memory/           # Operator memory — see memory/MAP.md
│   ├── MAP.md
│   ├── current/      # Mutable: current-strategy.md, next-actions.md, bugs-and-risks.md
│   ├── decisions/    # Point-in-time choices (dated, file-per-entry)
│   ├── sessions/     # Wrap-ups of long Claude Code sessions
│   └── ideas/        # Proposals for future projects
├── .claude/          # Claude-CLI configuration
│   ├── skills/       # Bundled skills (auto-loaded by Claude)
│   ├── rules/        # Modular path-scoped rules
│   ├── agents/       # Agent coordination patterns
│   ├── commands/     # Slash commands
│   └── mcp-servers/  # Local MCP server source
├── docs/             # Plans and design specs
│   ├── plans/        # Implementation plans
│   └── specs/        # Design specs
└── active/           # All business content
    ├── clients/      # Client engagements (one folder per client)
    ├── crm/          # Prospects / sales pipeline (pre-client)
    ├── apps/         # Standalone applications you build
    └── websites/     # Web builds, landing pages, research
```

**Rule: Never pollute root.** All files go in `active/`, `memory/`, `.claude/`, or `docs/` subdirectories.

## Brand Context

`BRAND.md` at the workspace root is the **single source of truth** for everything brand-related — voice, audience, products, visual identity, messaging. **Always reference `BRAND.md` when creating any business content** — emails, landing pages, social posts, ads, scripts.

If you do client work, each client folder has its own `BRAND.md` and `CLAUDE.md` that take precedence when working in that client's context.

## Memory system

Memory is how Claude remembers what's going on between sessions. It lives in three places:

- **Workspace `memory/`** (this folder) — operator state for the workspace as a whole.
- **Container `memory/`** — folders like `active/clients/` can have their own `memory/` for cross-cutting state across many children.
- **Project `memory/`** — each individual project folder (client, app, website) carries its own `memory/` plus `project-brief.md` (the frozen kickoff).

**Key files inside `memory/current/`:**

- `current-strategy.md` — what you're working on right now and how you're approaching it (snapshot, not a log)
- `next-actions.md` — punch list
- `bugs-and-risks.md` — open issues and watch-outs

**Other folders:**

- `decisions/` — point-in-time choices you won't revisit (dated, file-per-entry with frontmatter)
- `sessions/` — wrap-ups of long Claude Code sessions
- `ideas/` — proposals for projects that don't have folders yet. When promoted, the idea file moves into the new project folder as `project-brief.md`.

See [`memory/MAP.md`](memory/MAP.md) for full conventions, frontmatter shape, and the lifecycle of an idea → project.

### Rule: never scaffold a project folder without explicit approval

When a session produces a scope-of-work or brief for something that *could* become a new project, **default to writing it as an idea** at `memory/ideas/{slug}.md`. Do **not** create `active/{...}/projects/{slug}/` or any project folder structure unless the user has explicitly said "create a project for this" or equivalent. Ask first.

## Working with APIs & Services

When connecting to APIs or services, ALWAYS check existing `.env` files, config files, and existing scripts/code for credentials and patterns BEFORE asking the user or guessing at endpoints.

## Clients (optional)

If you do client work, each client folder mirrors the workspace structure. When working on a client, `cd` into their folder — it's self-contained.

```
{client_slug}/
├── BRAND.md            # Single source of truth — audience, products, voice, visual identity
├── CLAUDE.md           # Agent instructions, integration IDs, key file paths
├── memory/             # Per-client operator state (mirrors workspace memory/ + project-brief.md)
│   ├── MAP.md
│   ├── project-brief.md   # Frozen kickoff for this engagement
│   ├── decisions/, sessions/, meetings/
│   └── current/        # current-strategy.md, next-actions.md, bugs-and-risks.md
├── .claude/
│   └── skills/         # Client-specific skills only
├── active/
│   ├── research/       # Research deliverables
│   ├── copywriting/    # Avatars, sales pages, copy
│   ├── content/        # Scripts, drafts, content pieces
│   ├── projects/       # Project-scoped work
│   ├── ads/            # Ad creatives
│   └── websites/       # Web builds
├── assets/             # Visual assets (logos, images, design tokens)
├── credentials/        # secrets.env
└── .tmp/
```

- **`BRAND.md`** — read this when creating content for the client
- **`CLAUDE.md`** — read this when operating in the client's systems (CRMs, deploys, integrations)
- Client-specific skills go in the client's `.claude/skills/`, not the workspace root

### Rule: client-first lookup

**Whenever the user references a client by name, your FIRST action is to read that client's `CLAUDE.md` and `BRAND.md` before doing anything else.** Account IDs, integration links, and key file paths live there. If you discover an ID/integration that isn't recorded there, add it to the client's `CLAUDE.md` so future sessions don't have to search again.

## CRM (prospects)

`active/crm/` holds prospect data BEFORE someone becomes a client — discovery calls, proposals, research on people who haven't signed yet. Each prospect gets a folder. When they convert, migrate the folder from `active/crm/` to `active/clients/`.

## Skills

Skills live in `.claude/skills/`. Each skill has a `SKILL.md` that Claude loads automatically when relevant. See `.claude/skills/README.md` for the full list of bundled skills.

**Check existing skills before creating new ones.** Drop a folder with `SKILL.md` into `.claude/skills/` and Claude picks it up automatically.

Scripts in skills are invoked from the workspace root:

```bash
python3 .claude/skills/{skill-name}/scripts/main.py [args]
```

All scripts use `load_dotenv()` to load from the root `.env`.

## Rules

`.claude/rules/` holds modular, path-scoped instructions that only fire when working in matching folders. Each rule has frontmatter declaring its `paths:` glob. Use this for instructions that only apply to one part of the workspace (e.g. deploy rules for a specific app folder) without bloating this main CLAUDE.md.

## Deployment

If pushing code to Vercel-connected GitHub repos, make sure your Git user email matches the account connected to Vercel so auto-deployments trigger correctly.

## Quality Checks

After completing a batch task (e.g., writing scripts 1-14, generating metadata for multiple items), audit ALL outputs for consistency and quality — do not stop checking after the first few.

# Your Business Command Center

This workspace is your AI-powered hub for running and growing your business with Claude Code.

## Brand Context

All brand and business information lives in `BRAND.md` at the workspace root. Always reference this file when creating any business content — emails, landing pages, social posts, ads, or anything client-facing.

## Structure

```
/                       # Root — config and reference only
├── CLAUDE.md           # Workspace instructions (this file)
├── BRAND.md            # Brand profile (source of truth for all content)
├── GEMINI.md           # Gemini instructions
├── .env                # API keys and environment variables
├── .tmp/               # Scratch space for temporary files
├── .claude/
│   └── skills/         # Installed skills (auto-loaded by Claude)
└── active/
    ├── clients/        # Client projects and assets
    ├── content/        # Content drafts, scripts, copy
    └── websites/       # Web builds and landing pages
```

### Client Folder Structure

Each client folder mirrors this workspace structure:

```
{client_slug}/
├── BRAND.md            # Brand profile — single source of truth for content
├── CLAUDE.md           # Agent instructions + integration config
├── .claude/
│   ├── skills/         # Client-specific skills
│   └── learnings.md    # Accumulated learnings and constraints
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

## Rules

- **Do not pollute root.** All working files go in `active/` or `.tmp/`.
- **Check existing skills before creating new ones.** Look in `.claude/skills/` first.
- **Always reference BRAND.md** when creating any business content.

## Skills

Skills live in `.claude/skills/`. Each skill has a `SKILL.md` that Claude loads automatically when the skill is triggered. See the README for a list of included skills.

## Environment

API keys and credentials are stored in `.env` at the root. Scripts load this file automatically. Never commit `.env` to version control.

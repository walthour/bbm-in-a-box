# Your Business Command Center

This workspace is your AI-powered hub for running and growing your business with Claude Code.

## Brand Context

All brand and business information lives in `active/BRAND.md`. Always reference this file when creating any business content — emails, landing pages, social posts, ads, or anything client-facing.

## Structure

```
/                       # Root — keep clean
├── CLAUDE.md           # Workspace instructions (this file)
├── GEMINI.md           # Gemini instructions
├── .env                # API keys and environment variables
├── .tmp/               # Scratch space for temporary files
├── .claude/
│   └── skills/         # Installed skills (auto-loaded by Claude)
└── active/
    ├── BRAND.md        # Your brand profile (source of truth)
    ├── clients/        # Client projects and assets
    ├── content/        # Content drafts, scripts, copy
    └── websites/       # Web builds and landing pages
```

## Rules

- **Do not pollute root.** All working files go in `active/` or `.tmp/`.
- **Check existing skills before creating new ones.** Look in `.claude/skills/` first.
- **Always reference BRAND.md** when creating any business content.

## Skills

Skills live in `.claude/skills/`. Each skill has a `SKILL.md` that Claude loads automatically when the skill is triggered. See the README for a list of included skills.

## Environment

API keys and credentials are stored in `.env` at the root. Scripts load this file automatically. Never commit `.env` to version control.

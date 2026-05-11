# Your Business Command Center — Gemini

An AI-powered workspace for running and growing your business. This file mirrors `CLAUDE.md` for Gemini CLI users.

## Structure

```
/                     # Root — keep clean
├── CLAUDE.md         # Claude Code instructions
├── GEMINI.md         # Gemini instructions (this file)
├── BRAND.md          # Brand profile (source of truth for all content)
├── .env              # API keys and environment variables
├── .tmp/             # Scratch space for temporary files
├── memory/           # Operator memory (see memory/MAP.md)
├── .claude/          # Claude config — skills, rules, agents, commands, mcp-servers
├── docs/             # Plans and design specs
└── active/           # All business content
    ├── clients/      # Client engagements
    ├── crm/          # Prospects / sales pipeline
    ├── apps/         # Standalone applications
    └── websites/     # Web builds, landing pages, research
```

## Rules

- **Do not pollute root.** All files go in `active/`, `memory/`, `.claude/`, or `docs/` subdirectories.
- **Always reference `BRAND.md`** when creating any business content (emails, landing pages, social posts, ads).
- **Always check `.env` first** for API keys before asking the user.
- **Never scaffold a project folder without explicit approval.** Default to writing scoping documents to `memory/ideas/{slug}.md`. Ask before creating new project folders.
- **Client-first lookup:** when a client is referenced by name, read that client's `CLAUDE.md` and `BRAND.md` first before searching elsewhere.

## Memory

Operator state lives in `memory/` — current strategy, next actions, bugs/risks, decisions, sessions, ideas. See `memory/MAP.md` for the full map. Memory subtrees also exist at the container level (e.g. `active/clients/memory/`) and per-project (each client/app/website folder has its own `memory/`).

## Skills

Skills are bundled capabilities in `.claude/skills/`. Each has a `SKILL.md`. See `.claude/skills/README.md` for the full list.

## Environment

API keys live in `.env` at the root. Scripts load this file automatically. Never commit `.env` to version control.

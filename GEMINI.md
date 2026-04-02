# Your Business Command Center — Gemini

This workspace is your AI-powered hub for running and growing your business.

## Brand Context

All brand and business information lives in `active/BRAND.md`. Always reference this file when creating any business content.

## Structure

```
/                       # Root — keep clean
├── CLAUDE.md           # Claude Code instructions
├── GEMINI.md           # Gemini instructions (this file)
├── .env                # API keys and environment variables
├── .tmp/               # Scratch space for temporary files
├── skills/             # Installed skills
├── .claude/            # Claude internal config
└── active/
    ├── BRAND.md        # Your brand profile (source of truth)
    ├── clients/        # Client projects and assets
    ├── content/        # Content drafts, scripts, copy
    └── websites/       # Web builds and landing pages
```

## Rules

- Do not pollute root. All working files go in `active/` or `.tmp/`.
- Always reference `active/BRAND.md` when creating any business content.
- API keys are in `.env` at the root.

# Clients

One folder per client engagement. Each folder is self-contained — `cd` into it and Claude treats it like its own workspace.

## Folder shape

```
{client_slug}/
├── BRAND.md            # Audience, products, voice, visual identity — source of truth
├── CLAUDE.md           # Agent instructions, integration IDs, key file paths
├── memory/
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

## Slug convention

Use `lowercase_snake_case` or `lowercase-hyphenated`. Pick one and stay consistent. If you handle a lot of clients and want stable two-letter prefixes for sorting (`ac_acme_co`, `bc_big_corp`), establish that early.

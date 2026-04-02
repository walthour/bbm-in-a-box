# BBM in a Box

An AI-powered workspace template for running your business with [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Clone this repo, answer a few onboarding questions, and you have a fully configured command center for writing emails, building landing pages, researching your market, and more.

Built by [Antigravity](https://antigravity.co) as part of the [Brand Building Machine](https://bbm.co) ecosystem.

---

## What's Inside

```
/                       # Root — keep clean
├── CLAUDE.md           # Claude Code workspace instructions
├── GEMINI.md           # Gemini workspace instructions
├── ONBOARDING.md       # Interactive setup script (runs once)
├── .env                # API keys (you create this)
├── .tmp/               # Scratch space
├── .claude/
│   └── skills/         # Installed skills (auto-loaded by Claude)
└── active/
    ├── BRAND.md        # Your brand profile (filled during onboarding)
    ├── clients/        # Client projects and assets
    ├── content/        # Content drafts, scripts, copy
    └── websites/       # Web builds and landing pages
```

---

## Quick Start

1. Clone this repo
2. Open the folder in Claude Code
3. Tell Claude: "Run the onboarding" or paste the contents of `ONBOARDING.md`
4. Answer the setup questions (one at a time — it only takes a few minutes)
5. Start working. Ask Claude to write emails, research your audience, build a landing page, or anything else your business needs.

---

## Included Skills

Skills are pre-built workflows that Claude loads automatically when relevant. They live in `.claude/skills/`.

| Skill | What It Does |
|-------|--------------|
| `email-sequences` | Write high-converting email sequences using direct-response copywriting frameworks. Covers lead magnet delivery, welcome/nurture, sales conversion, and educational email courses. |
| `deep-researching` | Conduct comprehensive audience and market research using multiple AI APIs, then synthesize findings into reports and copywriting briefs. |
| `lead-magnet-creator` | Create high-converting lead magnets, opt-in freebies, checklists, and downloadable resources. |
| `website-copywriting-creation` | Create new high-converting landing page copy from scratch, from wireframing to final delivery. |
| `website-copywriting-analysis` | Analyze existing landing pages and sales copy to reverse-engineer their structure and effectiveness. |
| `brainstorming` | Structured exploration of ideas, requirements, and design before implementation. |
| `planning` | Create detailed, step-by-step implementation plans from specs or requirements. |
| `brand-identity` | Source of truth for brand guidelines, design tokens, and voice/tone. |
| `ui-ux-pro-max` | UI/UX design intelligence with style presets, palettes, font pairings, and layout patterns. |

### Optional Skills (Require Additional Setup)

Some skills require external API keys or services:

| Skill | Requirement |
|-------|-------------|
| `optional/scrape-instagram` | Apify API key |
| `optional/scrape-tiktok` | Apify API key |
| `optional/scrape-youtube` | Apify API key |
| `deep-researching` | API keys for Perplexity, Gemini, and/or other research providers |

Add any required keys to your `.env` file.

---

## How Skills Work

Each skill follows a standard format:

- `SKILL.md` — Instructions and frameworks loaded into context when the skill triggers
- `references/` — Supporting docs loaded on demand (keeps the main file lean)
- No external dependencies, no hardcoded paths

Skills activate automatically based on what you ask Claude to do. You can also browse available skills by asking Claude: "What skills do I have?"

---

## Adding Your Own Skills

Drop any skill folder into `.claude/skills/` with a `SKILL.md` file. Claude will pick it up automatically. Each skill should:

- Work without any specific folder structure assumptions
- Ask the user for any required inputs conversationally
- Include a clear description of what it does

---

## What BBM Is

[Brand Building Machine](https://bbm.co) is an AI-first growth ecosystem for small business owners. BBM in a Box is the open-source companion — the same workflows and tools we use with clients, packaged for anyone to run independently with Claude Code.

---

## License

MIT

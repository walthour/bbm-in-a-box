# BBM in a Box

An AI-powered workspace template for running your business with [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Clone this repo, answer a few onboarding questions, and you have a fully configured command center for writing emails, building landing pages, researching your market, tracking decisions across sessions, and more.

Built by [Brand Building Machine](https://bbm.co) and shipped as an open-source companion to our agency workflows.

---

## What's Inside

```
/                       # Root — keep clean
├── CLAUDE.md           # Claude Code workspace instructions
├── GEMINI.md           # Gemini workspace instructions
├── BRAND.md            # Your brand profile (filled during onboarding)
├── ONBOARDING.md       # Interactive setup script (runs once)
├── README.md           # This file
├── .env                # API keys (you create this)
├── .tmp/               # Scratch space
├── memory/             # Operator memory — what Claude remembers between sessions
│   ├── MAP.md          #   conventions for the memory model
│   ├── current/        #   current-strategy, next-actions, bugs-and-risks
│   ├── decisions/      #   point-in-time choices (dated)
│   ├── sessions/       #   wrap-ups of long sessions
│   └── ideas/          #   proposals for future projects
├── .claude/
│   ├── skills/         #   bundled skills (auto-loaded by Claude)
│   ├── rules/          #   path-scoped instructions
│   ├── agents/         #   sub-agent definitions
│   ├── commands/       #   custom slash commands
│   └── mcp-servers/    #   local MCP server source
├── docs/
│   ├── plans/          #   implementation plans
│   └── specs/          #   design specs
└── active/
    ├── clients/        # Client engagements
    ├── crm/            # Prospects / sales pipeline (pre-client)
    ├── apps/           # Standalone applications you build
    └── websites/       # Web builds, landing pages, research
```

---

## Quick Start

Open **[`ONBOARDING.md`](ONBOARDING.md)** and follow it. It walks you through everything — installing the macOS prerequisites in Terminal (about 30 minutes, mostly waiting), then setting up the workspace inside Claude Code Desktop with one master prompt.

When you're done with onboarding, your workspace is ready. Start asking Claude to write emails, research your audience, build a landing page, set up client folders, or anything else your business needs.

---

## Required Skill Library: Superpowers

This workspace uses the **Superpowers** skill library (brainstorming, planning, executing plans, debugging, TDD, code review). Superpowers is installed automatically during onboarding by copying its `skills/` folder into your workspace's `.claude/skills/` directory — no plugin marketplace required.

Superpowers is built by Jesse Vincent ([@obra](https://github.com/obra)): https://github.com/obra/superpowers

---

## The Memory System

The most important upgrade over a plain Claude Code workspace: **persistent memory**. Claude doesn't naturally remember anything between sessions, so this workspace gives it a structured place to write down:

- **What you're working on right now** (`memory/current/current-strategy.md`)
- **Your punch list** (`memory/current/next-actions.md`)
- **Open issues and risks** (`memory/current/bugs-and-risks.md`)
- **Point-in-time decisions** that won't be revisited (`memory/decisions/YYYY-MM-DD-slug.md`)
- **Session wrap-ups** so the next session can pick up cold (`memory/sessions/`)
- **Ideas** for future projects that don't exist yet (`memory/ideas/`)

Each client, app, or project folder gets its own `memory/` subtree too. See [`memory/MAP.md`](memory/MAP.md) for the full conventions.

---

## Included Skills

Skills are pre-built workflows that Claude loads automatically when relevant. They live in `.claude/skills/`.

| Skill | What It Does |
|-------|--------------|
| `dashboard-design` | Build production-grade data dashboard web apps that are calm, clear, fast, and data-first. |
| `email-sequences` | Write high-converting email sequences using direct-response copywriting frameworks. |
| `lead-magnet-creator` | Create high-converting lead magnets, opt-in freebies, checklists, and downloadable resources. |
| `scroll-stop-prompter` | Generate AI image/video prompts for scroll-stopping content — clean shot, exploded view, transition video. |
| `publish-website` | End-to-end workflow for publishing a web project live — pushes to GitHub and deploys to Vercel in one flow. |
| `ui-ux-pro-max` | UI/UX design intelligence with style presets, palettes, font pairings, charts, and layout patterns. |
| `website-copywriting-analysis` | Analyze existing landing pages and sales copy to reverse-engineer their structure and effectiveness. |
| `website-copywriting-creation` | Create new high-converting landing page copy from scratch, from wireframing to final delivery. |

> Brainstorming, planning, debugging, TDD, code review, and other process skills come from the **Superpowers plugin** (see [Required Plugin](#required-plugin-superpowers) above), not bundled here.

---

## How Skills Work

Each skill follows a standard format:

- `SKILL.md` — Instructions and frameworks loaded into context when the skill triggers
- `references/` — Supporting docs loaded on demand (keeps the main file lean)
- `scripts/` — Optional Python helpers
- No external dependencies, no hardcoded paths

Skills activate automatically based on what you ask Claude to do. You can also browse available skills by asking Claude: "What skills do I have?"

---

## Adding Your Own Skills

Drop any skill folder into `.claude/skills/` with a `SKILL.md` file. Claude will pick it up automatically. Each skill should:

- Work without specific folder structure assumptions
- Ask the user for any required inputs conversationally
- Include a clear `description:` in its frontmatter so Claude knows when to trigger it

---

## What's Different About This Workspace

Most Claude Code workspaces are scratch directories — useful in the moment, useless next week. This template adds three things on top:

1. **Memory** — a structured place for Claude to record decisions, current strategy, and session wrap-ups so the next session can pick up cold.
2. **Modular rules** — path-scoped instructions in `.claude/rules/` that only fire when working in matching folders, so your top-level `CLAUDE.md` stays lean.
3. **A multi-level structure** — workspace, container (e.g. `active/clients/`), and project (e.g. one specific client). Each level gets its own memory and config, so context stays local to the work.

---

## What BBM Is

[Brand Building Machine](https://bbm.co) is an AI-first growth ecosystem for small business owners. BBM in a Box is the open-source companion — the same workflows and tools we use with clients, packaged for anyone to run independently with Claude Code.

---

## License

MIT

# Skills Directory

Bundled, reusable capabilities Claude loads automatically when relevant. Each skill is a self-contained folder with a `SKILL.md` (instructions + frontmatter), optional `scripts/`, and optional `references/`.

## Bundled skills

| Skill | Description |
|-------|-------------|
| `brand-identity/` | Source of truth for brand guidelines, design tokens, and voice/tone. |
| `brainstorming/` | Structured exploration of ideas, requirements, and design before implementation. |
| `planning/` | Create detailed, step-by-step implementation plans from specs or requirements. |
| `dashboard-design/` | Build production-grade data dashboard web apps that are calm, clear, fast, and data-first. |
| `deep-researching/` | Comprehensive audience and market research synthesized into reports and copywriting briefs. |
| `email-sequences/` | Write high-converting email sequences using direct-response copywriting frameworks. |
| `lead-magnet-creator/` | Create high-converting lead magnets, opt-in freebies, checklists, and downloadable resources. |
| `scroll-stop-prompter/` | Generate AI image/video prompts for scroll-stopping content. |
| `tech-github-sync/` | Safe sync for any shared Git repository. Stages untracked files before destructive ops. |
| `tech-publish-to-github-vercel/` | End-to-end workflow for pushing a web project to GitHub and deploying live on Vercel. |
| `ui-ux-pro-max/` | UI/UX design intelligence: styles, palettes, font pairings, charts, layout patterns. |
| `website-copywriting-analysis/` | Analyze existing landing pages and sales copy to reverse-engineer structure and effectiveness. |
| `website-copywriting-creation/` | Create new high-converting landing page copy from scratch. |

### Optional skills (require API keys)

| Skill | Requirement |
|-------|-------------|
| `optional/scrape-instagram/` | Apify API key |
| `optional/scrape-tiktok/` | Apify API key |
| `optional/scrape-youtube/` | Apify API key |

Add required keys to your workspace `.env` file.

## Adding your own skill

Drop a folder with `SKILL.md` into `.claude/skills/`. Claude picks it up automatically on the next session.

Minimum `SKILL.md`:

```markdown
---
name: my-skill
description: One-line description Claude uses to decide when to invoke this skill.
---

# My Skill

Instructions for what to do when this skill triggers.
```

## How skills trigger

Claude loads each skill's frontmatter `description` at session start and invokes the skill when the user's request matches. The richer and more specific the description, the more reliably the skill triggers.

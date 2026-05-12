# Skills Directory

Bundled, reusable capabilities Claude loads automatically when relevant. Each skill is a self-contained folder with a `SKILL.md` (instructions + frontmatter), optional `scripts/`, and optional `references/`.

## Bundled skills

| Skill | Description |
|-------|-------------|
| `dashboard-design/` | Build production-grade data dashboard web apps that are calm, clear, fast, and data-first. |
| `email-sequences/` | Write high-converting email sequences using direct-response copywriting frameworks. |
| `lead-magnet-creator/` | Create high-converting lead magnets, opt-in freebies, checklists, and downloadable resources. |
| `publish-website/` | End-to-end workflow for publishing a web project live — pushes to GitHub and deploys to Vercel in one flow. |
| `scroll-stop-prompter/` | Generate AI image/video prompts for scroll-stopping content. |
| `ui-ux-pro-max/` | UI/UX design intelligence: styles, palettes, font pairings, charts, layout patterns. |
| `website-copywriting-analysis/` | Analyze existing landing pages and sales copy to reverse-engineer structure and effectiveness. |
| `website-copywriting-creation/` | Create new high-converting landing page copy from scratch. |

> Brainstorming, planning, executing plans, debugging, TDD, code review, and other process skills come from the **Superpowers plugin** — see the root README for install instructions.

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

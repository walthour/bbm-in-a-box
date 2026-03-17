# BBM in a Box

Standalone, shareable skills and agents built by Antigravity for the Brand Building Machine (BBM) ecosystem — and for anyone using Claude Code who wants battle-tested workflows.

Every asset here is designed to work **out of the box** in any environment. No proprietary folder structure, no internal dependencies. Just drop a skill into your Claude setup and go.

---

## What's Inside

### Skills

| Skill | What It Does |
|-------|-------------|
| `skills/email-sequences` | Write high-converting email sequences using direct-response copywriting frameworks. Covers lead magnet delivery, welcome/nurture, sales conversion, and educational email courses (EEC). |

---

## How to Use a Skill

Skills are designed for [Claude Code](https://claude.ai/code) with the Superpowers plugin installed.

1. Copy the skill folder into your Claude skills directory (typically `~/.claude/skills/` or wherever your setup points)
2. The skill will auto-load and trigger when relevant
3. Claude will ask you for any context it needs — no special folder structure required

---

## How Skills Are Built

Each skill follows the Superpowers skill format:
- `SKILL.md` — Instructions and frameworks loaded into context when the skill triggers
- `references/` — Supporting docs loaded on demand (keeps the main file lean)
- No external dependencies, no hardcoded paths

---

## What BBM Is

[Brand Building Machine](https://bbm.co) is an AI-first growth ecosystem for small business owners. BBM in a Box is the open-source complement — the workflows and tools we actually use, packaged for anyone to run.

---

## Contributing

Each skill or agent added here should:
- Work without any specific folder structure or environment assumptions
- Ask the user for any required inputs conversationally
- Include a clear description of what it does and when to use it
- Have no fabricated content (placeholders clearly marked)

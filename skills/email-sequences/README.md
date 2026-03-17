# Email Sequences Skill for Claude Code

Write high-converting email sequences using proven direct-response frameworks — directly inside Claude Code.

This skill covers 4 flow types:
- **Lead Magnet Delivery** — 2 emails, deliver the freebie and build trust
- **Welcome / Nurture** — 5 emails, build relationship before the pitch
- **Sales Conversion** — 6 emails, present offer, handle objections, drive action
- **Educational Email Course (EEC)** — 6 emails, daily education that builds authority

---

## Installation

### Option 1: Install via Claude Code (recommended)

```bash
# From your project root or home directory
gh repo clone walthour/email-sequences ~/.claude/skills/email-sequences
```

Or if you prefer a specific skills directory:

```bash
gh repo clone walthour/email-sequences /path/to/your/skills/email-sequences
```

### Option 2: Download ZIP

1. Click **Code → Download ZIP** on this page
2. Unzip and place the `email-sequences` folder in your Claude skills directory

### Where is my skills directory?

Claude Code looks for skills in the path configured in your Superpowers settings. Common locations:
- `~/.claude/skills/`
- Wherever your `superpowers` plugin points (check your `.superpowers/` config)

---

## How It Works

Once installed, Claude will automatically use this skill when you ask to write emails. No setup needed — Claude will ask you for the details it needs.

**Example prompts that trigger it:**
- "Write a welcome sequence for my coaching business"
- "I need a 5-day email course on home maintenance for homeowners"
- "Create a sales email sequence for my new online course"
- "Write a lead magnet delivery flow for my free checklist"

Claude will ask you upfront for what it needs: your audience, what you're selling, any client success stories, who signs the emails, etc.

---

## What's Inside

```
email-sequences/
├── SKILL.md                    # Main skill instructions (loaded when triggered)
└── references/
    ├── lead-magnet.md          # Lead magnet delivery flow (2 emails)
    ├── welcome-nurture.md      # Welcome/nurture flow (5 emails)
    ├── sales-conversion.md     # Sales conversion flow (6 emails)
    └── eec.md                  # Educational email course (6 emails)
```

---

## Core Principles Baked In

- **Never fabricate** — testimonials, case studies, and stats must be real; placeholders are clearly marked
- **Customer is the hero** — the brand is the guide, not the star
- **1 email = 1 idea** — no overloading
- **Value before ask** — nurture earns the right to pitch
- **4th-grade reading level** — simple, direct, mobile-friendly

---

## Part of BBM in a Box

This skill is part of [BBM in a Box](https://github.com/walthour/bbm-in-a-box) — a collection of standalone AI workflows for business owners built by [Antigravity](https://antigravity.agency).

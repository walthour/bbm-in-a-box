# Rules

Modular, path-scoped instructions that only fire when Claude is working in matching folders. Use this instead of bloating the workspace `CLAUDE.md` with rules that only apply to one part of the workspace.

## Shape

Each rule is a single Markdown file with frontmatter declaring its scope:

```markdown
---
paths:
  - "active/apps/my-app/**"
  - "active/apps/my-app/*.html"
---

# Rule title

Rule contents here. Claude will load this automatically when working in any matching path.
```

Rules without `paths:` frontmatter are always loaded (treat those carefully — they live in your top-level `CLAUDE.md`'s blast radius).

## Examples of good rules

- **Deploy rules** for a specific app — env var names, deploy command, gotchas
- **Account safety rules** for a third-party API — never run X without confirmation, always use account Y
- **Style rules** for a specific content folder — voice, formatting, banned words
- **Schema rules** for a specific data folder — required frontmatter shape, naming conventions

## What does NOT belong here

- Universal rules → those go in the workspace `CLAUDE.md`
- One-off notes from a single session → those go in `memory/`
- Decisions you might revisit → `memory/decisions/`

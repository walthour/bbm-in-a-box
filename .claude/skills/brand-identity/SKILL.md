---
name: brand-identity
description: Provides the single source of truth for brand guidelines, design tokens, technology choices, and voice/tone. Use this skill whenever generating UI components, styling applications, writing copy, or creating user-facing assets to ensure brand consistency.
---

# Brand Identity & Guidelines

**Scope:** Brand-Specific Design & Copy Constraints

This skill defines the core constraints for visual design and technical implementation. It is designed to be **Context Aware** -- you must identify the active brand/client and use their specific assets.

## 1. Identify the Brand

Before proceeding, check if brand assets exist in the project. Common locations:
- `brand/` or `assets/` directory in the project root
- A client-specific folder if working in a multi-client setup

If no brand assets are found, ask the user to provide them or use the templates in this skill as a starting point.

## 2. Load Brand Resources

### For Visual Design & UI Styling
Look for a **design tokens** file (JSON or similar):
- `brand/design-tokens.json`
- `assets/design-tokens.json`

If none exists, use the template at `templates/design-tokens.json` as a starting point and ask the user to fill in their brand colors, fonts, and spacing.

### For Copywriting & Content Generation
Look for a **voice/tone** guide:
- `brand/voice-tone.md`
- `assets/voice-tone.md`

If none exists, use the template at `templates/voice-tone.md` and ask the user to define their brand personality.

## 3. Technology Standards
Unless overridden by a specific project requirement, use the defaults defined in:
- **[`resources/tech-stack.md`](resources/tech-stack.md)**

These can be customized per project -- the file serves as a sensible starting point.

---
name: website-copywriting-creation
description: Creates new high-converting landing page copy from scratch, from wireframing to final copy.
---

# Website Copywriting Creation

End-to-end creation of landing page copy: **Wireframe --> Generate --> Deliver**.

## When to Use This Skill
- You want to "write copy" for a new page
- You need a "wireframe" or "outline" for a sales page
- You want to "generate" full text for a landing page

## Workflow

### 1. Wireframe (Structure First)

Create the skeleton of a new page using proven templates.

```bash
# List available templates
python3 website-copywriting-creation/scripts/wireframe.py --list

# Direct mode with template
python3 website-copywriting-creation/scripts/wireframe.py --template 3 --goal "Sales Page"

# Interactive mode (prompts for selection)
python3 website-copywriting-creation/scripts/wireframe.py
```
**Output**: `.tmp/wireframe.md`

### 2. Generate (Fill the Blocks)

Generate persuasive copy for the wireframe using Claude.

```bash
python3 website-copywriting-creation/scripts/generate.py .tmp/wireframe.md \
  --audience "Target Audience" \
  --offer "My Offer" \
  --tone "Professional yet conversational"
```
**Output**: `.tmp/landing_page_copy.md`

### 3. Deliver

The final copy is saved as a markdown file. You can then:
- Copy it into your CMS or page builder
- Export it to Google Docs manually
- Share it with your designer or developer

## Instructions
- Always start with a wireframe to ensure structural soundness.
- Use `generate.py` to fill the wireframe with persuasive copy.
- **CRITICAL**: Verify all generated copy against `resources/core_principles.md`, specifically the "Design for Scan-ability" section.

## Scripts Reference

| Script | Purpose | Key Args |
|--------|---------|----------|
| `wireframe.py` | Template-based page skeleton | `--template 1-5`, `--goal`, `--list`, `--output` |
| `generate.py` | LLM-powered copy generation | `wireframe` (positional), `--audience`, `--offer`, `--tone`, `--output` |

### Available Templates

| # | Template | Best For |
|---|----------|----------|
| 1 | Short Warm Offer Page | Email/retargeting, warm traffic, low-friction offers |
| 2 | Direct-to-Product Ecom | Cold ads, single product campaigns |
| 3 | Long-Form Sales Page | High-ticket, complex offers, cold traffic |
| 4 | Lead-Gen Services | Services, medical, B2B, form fills |
| 5 | Pre-Sell Advertorial | Education before sale, overcoming skepticism |

## Requirements

The `generate.py` script requires an `ANTHROPIC_API_KEY` environment variable. Set it in a `.env` file in your project root:
```bash
ANTHROPIC_API_KEY=sk-ant-...
```

Required Python packages:
```bash
pip install anthropic python-dotenv
```

> **Note:** `wireframe.py` has no API dependencies -- it works purely from local templates.

## Output Format

| Step | Output File | Contents |
|------|-------------|----------|
| Wireframe | `.tmp/wireframe.md` | Structured page outline with sections |
| Generate | `.tmp/landing_page_copy.md` | Full persuasive copy in markdown |

## Resources
- [Scripts](scripts/)
- [Templates](resources/templates/)
- [Core Principles](resources/core_principles.md)

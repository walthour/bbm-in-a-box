---
name: deep-researching
description: Conducts comprehensive audience and market research across 5 research chapters using a single research tool (Perplexity, Claude web search, or any available search-capable AI). Synthesizes findings into a full report, copywriting brief, and executive summary. Use when user mentions audience research, market research, deep research, or competitive analysis.
---

# Deep Audience Research

## When to Use This Skill

- User requests audience or market research
- User wants to understand a target demographic
- User needs competitive landscape analysis
- User asks for a copywriting brief or executive summary based on research

## Prerequisites

You need ONE research tool that can search the web. Any of these will work:

| Tool | How to Access |
|------|---------------|
| **Perplexity MCP** (recommended) | `perplexity_research` or `perplexity_search` via MCP |
| **Claude web search** | Built-in `WebSearch` tool |
| **Firecrawl** | `firecrawl_search` via MCP |
| **Manual** | User pastes research from any source |

If no search tool is available, the user can run each chapter prompt manually in Perplexity (perplexity.ai), ChatGPT with browsing, or any search-capable AI, then paste the results back for synthesis.

## Required Inputs

**Audience Brief** -- a text description (can be a file or pasted directly) containing:
- Who the audience is (demographics, psychographics)
- What product/service is being offered
- Any known competitors or market context
- Geographic focus (if applicable)

## Workflow

### Phase 1: Research (5 Chapters)

Run each chapter sequentially. For each chapter, use your research tool with the chapter prompt from `references/` combined with the audience brief.

The 5 research chapters are:

| # | Chapter | Reference File | Focus |
|---|---------|----------------|-------|
| 1 | Audience Psychology | `references/01_audience_psychology.md` | Pains, desires, obstacles, voice of customer |
| 2 | Competitor Landscape | `references/02_competitor_landscape.md` | Direct competitors, positioning, market gaps |
| 3 | Market Trends | `references/03_market_trends.md` | Cultural shifts, economic factors, timing |
| 4 | Content Strategy | `references/04_content_strategy.md` | Platform hierarchy, influencers, hooks |
| 5 | Paid Acquisition & Funnel | `references/05_paid_acquisition_funnel.md` | Messaging framework, funnel architecture, ad creative |

**How to run each chapter:**

1. Read the chapter prompt from `references/`
2. Combine it with the audience brief
3. Send to your research tool
4. Save the output (hold in context or write to a scratch file)

**Example using Perplexity MCP:**
```
For each chapter:
  1. Read references/0X_chapter_name.md
  2. Call perplexity_research with: "[chapter prompt] + [audience brief]"
  3. Store the result
```

**Example using manual approach:**
```
For each chapter:
  1. Read references/0X_chapter_name.md
  2. Paste the prompt + audience brief into Perplexity/ChatGPT
  3. Copy the results back
```

Each chapter should produce 4-8 pages of research. Save all outputs before moving to synthesis.

### Phase 2: Synthesis

Once all 5 chapters are complete, synthesize them into a single report. Use the synthesis instructions in `references/synthesis_instructions.md`.

**Produce three deliverables (in order):**

#### 1. Full Strategic Report (20-30 pages)
Structure:
- High-Level Audience Summary (1-2 paragraphs at top)
- Chapter 1: Audience Psychology & Voice of Customer
- Chapter 2: Competitive Landscape
- Chapter 3: Market Trends & Cultural Shifts
- Chapter 4: Content Strategy
- Chapter 5: Paid Acquisition & Funnel Strategy

#### 2. Copywriting Brief (5-8 pages)
Extract from the full report:
- Pains with voice-of-customer language
- Desires (emotional, social, practical)
- Objections and how to handle them
- Messaging angles ranked by impact
- Words/phrases to use and avoid
- Hook library (7-10 hooks with rationale)

#### 3. Executive Summary (4-6 pages)
Distill the full report into:
- Market opportunity overview
- Key insights (bulleted, scannable)
- Prioritized actions (what to do first, second, third)
- Quick-reference competitor table

### Phase 3: Delivery

Save all outputs to the client folder:
```
active/clients/{slug}/research/
  full_report.md
  copywriting_brief.md
  executive_summary.md
```

## Quality Requirements

Every deliverable must be:
- **Complete** -- no placeholders like `[Example...]`, `[Insert...]`, `[Competitor Name]`
- **Sourced** -- real URLs, real competitor names, real statistics
- **Pattern-based** -- insights organized by patterns, not raw data dumps
- **Actionable** -- every section provides clear direction, not just information
- **Production-ready** -- can be delivered to a client without further editing

## Synthesis Rules

When combining research from multiple chapters:
- **Remove duplicates** -- if the same insight appears in multiple chapters, combine into one strong statement
- **Flag conflicts** -- if sources disagree, note it with a warning (e.g., "Note: conflicting data -- Source A found X, while Source B found Y")
- **Prioritize quality over quantity** -- one strong insight beats three repetitive ones
- **Use real examples** -- competitor names, actual influencer handles, specific statistics
- **No meta-commentary** -- never say "the reader needs to research X" or "more data is needed"

## Edge Cases & Tips

- **No search tool available**: User can run prompts manually in perplexity.ai or ChatGPT with browsing, then paste results for synthesis
- **Thin results on a chapter**: Note the gap, work with what you have, remove empty sections rather than filling with generic advice
- **Local vs. national business**: The prompts adapt -- local businesses get local competitor analysis and regional cultural context; national/online businesses get broader market analysis
- **B2B vs. B2C**: The prompts adapt -- adjust platform recommendations, review sources, and language accordingly

## References

All chapter prompts and synthesis instructions are in the `references/` folder:

| File | Purpose |
|------|---------|
| `01_audience_psychology.md` | Chapter 1 research prompt |
| `02_competitor_landscape.md` | Chapter 2 research prompt |
| `03_market_trends.md` | Chapter 3 research prompt |
| `04_content_strategy.md` | Chapter 4 research prompt |
| `05_paid_acquisition_funnel.md` | Chapter 5 research prompt |
| `synthesis_instructions.md` | How to combine chapters into final deliverables |

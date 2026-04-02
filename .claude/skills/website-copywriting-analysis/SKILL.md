---
name: website-copywriting-analysis
description: Analyzes existing landing pages and sales copy to reverse-engineer their structure and effectiveness.
---

# Website Copywriting Analysis

This skill specializes in auditing and analyzing existing website copy.

## When to Use This Skill
- You want to "audit" or "analyze" a URL
- You need to reverse-engineer a successful competitor's page
- You need to understand the structure of an existing page before rewriting it

## Workflow

1.  **Analyze URL**: Scrape and parse a URL to extract its copy and structural blocks.
    ```bash
    python3 website-copywriting-analysis/scripts/analyze.py <url>
    # Optional flags: --output <path> --json <path>
    ```

2.  **Review Output**:
    - The script generates a markdown wireframe and a JSON analysis file.
    - Check the wireframe for the structural breakdown (Hero, Problem, Solution, etc.).
    - Check the JSON for metadata (headings count, CTAs found, etc.).

## Instructions
- **Input**: A valid URL (http/https).
- **Output**: 
    - Markdown file with structural analysis and wireframe.
    - JSON file with quantitative data.
- **Constraints**: 
    - Respects `robots.txt` where possible (though standard scraping libraries are used).
    - Best for static content; heavily dynamic JS-rendered sites might need a browser-based approach.

## Requirements

The script requires `requests` and `beautifulsoup4`:
```bash
pip install requests beautifulsoup4
```

## Resources
- [Scripts](scripts/)
- [Core Principles](resources/core_principles.md)

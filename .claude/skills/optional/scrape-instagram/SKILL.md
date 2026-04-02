---
name: scrape-instagram
description: Scrape Instagram profiles for posts, Reels, and carousels with optional transcription. Requires Apify API token.
---

# scrape-instagram

Scrapes Instagram profiles (posts, Reels, carousels) via Apify, with optional transcription powered by Gemini Flash. Supports local markdown output for quick research or JSON for further processing.

## Requirements

| Requirement | Purpose |
|:---|:---|
| `APIFY_API_TOKEN` | Required -- powers the Instagram scraping |
| `GEMINI_API_KEY` | Optional -- for video transcription and image description |
| `yt-dlp` binary | Optional -- for downloading video audio (needed for transcription) |
| Python packages | `apify-client`, `google-genai`, `python-dotenv` |

Set your API tokens in a `.env` file:
```bash
APIFY_API_TOKEN=apify_xxx
GEMINI_API_KEY=xxx          # Optional, for transcription
```

Install dependencies:
```bash
pip install apify-client google-genai python-dotenv
```

## Usage

```bash
# Quick summary of recent posts
python3 optional/scrape-instagram/scripts/scrape.py \
  --profiles "https://www.instagram.com/hormozi/" \
  --since 30d --output summary

# Save to local markdown
python3 optional/scrape-instagram/scripts/scrape.py \
  --profiles "https://www.instagram.com/hormozi/" \
  --since 30d --max-results 20 --output local

# Full JSON output
python3 optional/scrape-instagram/scripts/scrape.py \
  --profiles "https://www.instagram.com/hormozi/" \
  --since 7d --output json

# Skip transcription for faster scraping
python3 optional/scrape-instagram/scripts/scrape.py \
  --profiles "https://www.instagram.com/hormozi/" \
  --since 7d --no-transcribe --output local
```

## CLI Flags

| Flag | Default | Description |
|:---|:---|:---|
| `--profiles` | (required) | Comma-separated Instagram profile URLs |
| `--since` | `30d` | Time window: `7d`, `30d`, `2w`, `3m`, or `YYYY-MM-DD` |
| `--max-results` | `20` | Max posts per profile |
| `--output` | `summary` | `summary`, `json`, or `local` |
| `--output-dir` | `reports/` | Directory for `local` output |
| `--no-transcribe` | false | Skip transcription entirely |

## Output Modes

- **summary** -- Quick table in stdout with post titles, dates, metrics
- **json** -- Full JSON array printed to stdout
- **local** -- Structured markdown file saved to `reports/` with captions, metrics, and transcripts

## Note

This is an optional skill that requires paid API access (Apify). The scripts in this folder need to be adapted to your specific setup -- the original versions depend on agency-specific infrastructure (Supabase tables, internal client slugs) that has been removed from this template.

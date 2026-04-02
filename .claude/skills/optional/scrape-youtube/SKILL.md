---
name: scrape-youtube
description: Scrape YouTube channels for videos with transcripts. Requires Apify API token.
---

# scrape-youtube

Scrape YouTube channel videos, extract metadata and transcripts, and output as JSON, summary, or save to a database.

## Features

- Scrape videos from any YouTube channel URL
- Extract: title, thumbnail, description, engagement metrics
- Fetch transcripts via built-in YouTube captions
- Flexible time windows: relative (24h, 7d, 30d) or absolute dates
- Multiple output modes: JSON, summary, or database storage

## Requirements

This skill requires external API access:

| Requirement | Purpose |
|:---|:---|
| `APIFY_API_TOKEN` | Required -- powers the YouTube scraping |
| Python packages | `apify-client`, `python-dotenv` |
| Database (optional) | Only needed if you want persistent storage |

Set your API token in a `.env` file:
```bash
APIFY_API_TOKEN=apify_xxx
```

Install dependencies:
```bash
pip install apify-client python-dotenv
```

## Usage

```bash
# Basic: scrape channel from last 24 hours
python3 optional/scrape-youtube/scripts/scrape.py \
    --channels "https://youtube.com/@simonw" \
    --since 24h

# With transcripts
python3 optional/scrape-youtube/scripts/scrape.py \
    --channels "https://youtube.com/@simonw,https://youtube.com/@anthropic" \
    --since 7d \
    --transcribe

# Output as JSON
python3 optional/scrape-youtube/scripts/scrape.py \
    --channels "https://youtube.com/@simonw" \
    --since 24h \
    --output json

# Summary only (no save)
python3 optional/scrape-youtube/scripts/scrape.py \
    --channels "https://youtube.com/@simonw" \
    --since 24h \
    --output summary
```

## CLI Options

| Flag | Required | Description |
|------|----------|-------------|
| `--channels` | Yes | Comma-separated YouTube channel URLs |
| `--since` | Yes | Time window: `24h`, `7d`, `30d`, `1m`, or `YYYY-MM-DD` |
| `--transcribe` | No | Fetch transcripts for each video |
| `--max-per-channel` | No | Max videos per channel (default: 20) |
| `--output` | No | `json` (default), or `summary` |

## Costs

- **Apify YouTube scraper**: ~$0.50 per 1,000 videos
- **Apify transcript scraper**: ~$0.10 per video

## Note

This is an optional skill that requires paid API access (Apify). The scripts in this folder need to be adapted to your specific storage setup if you want to persist data beyond JSON output.

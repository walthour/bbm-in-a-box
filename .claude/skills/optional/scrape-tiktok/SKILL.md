---
name: scrape-tiktok
description: Scrape TikTok videos, transcripts, and metrics. Requires Apify API token.
---

# scrape-tiktok

Scrape TikTok profiles for video metadata, engagement metrics, and optional transcription via Whisper.

## Requirements

| Requirement | Purpose |
|:---|:---|
| `APIFY_API_TOKEN` | Required -- powers the TikTok scraping via `apidojo/tiktok-scraper` |
| `OPENAI_API_KEY` | Optional -- for transcription via Whisper |
| `ffmpeg` | Optional -- needed for audio extraction before transcription |
| Python packages | `apify-client`, `openai`, `python-dotenv` |

Set your API tokens in a `.env` file:
```bash
APIFY_API_TOKEN=apify_xxx
OPENAI_API_KEY=sk-xxx       # Optional, for transcription
```

Install dependencies:
```bash
pip install apify-client openai python-dotenv
```

## Usage

```bash
# Basic JSON output
python3 optional/scrape-tiktok/scripts/scrape.py \
  --profiles "nicksaraev" \
  --since 7d --output json

# Summary view
python3 optional/scrape-tiktok/scripts/scrape.py \
  --profiles "willsmith" \
  --since 30d --output summary

# With transcription (requires ffmpeg + OpenAI key)
python3 optional/scrape-tiktok/scripts/scrape.py \
  --profiles "khaby.lame" \
  --transcribe --output json
```

## Data Fields

Each scraped video includes:
- `content_id` -- The TikTok Video ID
- `url` -- Direct link to the video
- `title` / `content_text` -- Video description
- `author_name` -- Creator username
- `published_at` -- Upload date
- `view_count`, `like_count`, `comment_count`, `share_count` -- Engagement metrics
- `transcript` -- Whisper transcription (if `--transcribe` is used)
- `has_transcript` -- Boolean indicating if transcription succeeded

## Note

This is an optional skill that requires paid API access (Apify). The scripts in this folder need to be adapted to your specific setup -- the original versions depend on agency-specific infrastructure (Supabase tables, internal helper modules) that has been removed from this template.

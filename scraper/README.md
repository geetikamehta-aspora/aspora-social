# aspora_scraper

Python 3.12 package. No Playwright, no browser automation — see
`/Users/apple/.claude/plans/cheerful-sleeping-sun.md` Section 5 for why.

YouTube ingestion lives in a Supabase Edge Function
(`/supabase/functions/youtube-ingest/`), not here — this package is only the
manual-upload parsing pipeline (Instagram screenshots, LinkedIn/X/YouTube
CSV/XLSX/PDF exports), which needs Python's library ecosystem
(pandas/pdfplumber/OpenAI) that Deno Edge Functions don't have.

## Setup

```sh
cd scraper
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env  # fill in secrets
```

## Entry points

- `python -m aspora_scraper.ingest.process_upload` — parse all pending manual uploads.
- `python -m aspora_scraper.ingest.process_upload --upload-id <id>` — parse one upload.
- `python -m aspora_scraper.ingest.check_staleness` — daily "no upload received" nudge.

## Package layout

```
normalize/schema.py      # NormalizedAccountSnapshot / NormalizedPost — the contract every source satisfies
instagram_graph/         # OPTIONAL — placeholder only; implement as an Edge Function (like YouTube), not here, once Meta Graph API access is confirmed
ingest/                  # manual-upload parsing (csv/xlsx/pdf/image) for Instagram/LinkedIn/X + YouTube's supplementary CSV
storage/supabase_client.py  # the ONLY module holding the service-role key
alerts/notifier.py       # Slack
```

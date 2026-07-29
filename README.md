# Aspora Leadership Social Dashboard

Tracks social performance for three brands — **Aspora**, **NRI Shala**, and
**Aspora Malayalam** — across Instagram, LinkedIn, X, and YouTube. Full
design rationale lives in `/Users/apple/.claude/plans/cheerful-sleeping-sun.md`;
this README is the practical "how it fits together and how to stand it up"
reference, including decisions made after that plan was approved.

## Architecture at a glance

- **YouTube**: official Data API v3, pulled automatically by a **Supabase
  Edge Function** (`/supabase/functions/youtube-ingest/`) on a `pg_cron`
  schedule (3x/day). Zero ToS/ban risk — no browser automation anywhere in
  this project.
- **Instagram / LinkedIn / X** (+ YouTube's supplementary CSV): no
  automation against these accounts. An admin uploads a report — a
  screenshot, CSV/XLSX export, or PDF — through the dashboard
  (`/settings/uploads`). The file itself is relayed through a small Next.js
  route into **Google Drive** (via the Apps Script bridge in `/gas/`), and a
  scheduled GitHub Actions job (`/scraper`, Python) parses it into the same
  normalized schema. CSV/XLSX auto-promote to a fast one-click review;
  PDF/screenshots always require full manual review before anything is
  trusted.
- **Database**: Supabase Postgres is the single source of truth (`/sql/`).
- **Auth**: Firebase Authentication (Google sign-in only) resolves identity;
  authorization (is this email allowed in, admin or viewer) is a plain
  client-side Supabase query right after login (`web/lib/auth/use-auth.tsx`).
  There's no Supabase Third-Party Auth registration, no custom claims, no
  session cookies, and — deliberately — **no RLS enforcement by identity**:
  every browser request uses the anon key, so Postgres can't tell users
  apart. RLS is permissive on purpose (see `sql/003_rls.sql`'s header
  comment); the app's own UI is what hides admin actions from viewers, not
  the database. This trade-off was chosen explicitly over a heavier
  backend-proxy alternative — simple to reason about, matches a pattern
  already proven elsewhere, and the realistic threat model for an internal
  dashboard is "random person finds the URL," not "a determined user with
  devtools."
- **Frontend**: Next.js 15 App Router, deployed via Firebase App Hosting.

## Repo layout

```
/sql                Supabase schema migrations, RLS, views, pg_cron setup — apply in order, see sql/README.md
/supabase/functions  Edge Functions (youtube-ingest)
/scraper             Python 3.12 — manual-upload parsing pipeline (no Playwright)
/gas                 Google Apps Script — Drive-upload bridge, see gas/README.md
/web                 Next.js 15 dashboard
/.github/workflows   process-uploads.yml (15-min poll), staleness-check.yml (daily), deploy-frontend.yml (CI gate)
```

## Setup order

1. **Supabase**: create the project (or use the existing one), apply
   `/sql/*.sql` in order (`sql/README.md`), add the service-role key to Vault.
2. **`youtube-ingest` Edge Function**: deploy, set its secrets, run
   `sql/008_youtube_cron.sql` to schedule it (`supabase/functions/youtube-ingest/README.md`).
3. **Drive-upload bridge**: paste `gas/Code.gs` into the Apps Script project,
   set Script Properties, deploy as a Web App (`gas/README.md`).
4. **`/web`**: `npm install`, fill in `.env` (already has real
   Supabase/Firebase values — nothing else needed for auth), `npm run dev`.
5. **`/scraper`**: `pip install -e ".[dev]"`, fill in `.env`, used by the
   GitHub Actions upload-parsing workflows (add the same secrets to the repo).
6. Fill in the `TODO_SET_HANDLE` placeholders in `sql/004_seed.sql` with real
   handles/channel IDs before relying on YouTube ingestion.

## What's not built yet

- `ai_insights` generation is gated on `OPENAI_API_KEY`, which hasn't been
  added yet — schema and UI shell exist, the generation job doesn't run
  without it (also needed for the screenshot vision parser).
- Instagram Graph API as an alternative to screenshot upload — contingent on
  confirming Meta Business Suite / Developer App access per brand
  (`scraper/aspora_scraper/instagram_graph/runner.py`).
- Multi-account fan-out for `applies_to='all_accounts'` uploads — the
  approve-to-`historical_metrics` step currently requires a single resolved
  `platform_account_id`; a combined multi-account report needs to be split
  into per-account uploads for now.
- `reports` generation, per-platform deep-dive pages, and full CRUD for
  `configurations`/`platform_accounts` in Settings are stubbed/read-only.

# youtube-ingest

Supabase Edge Function. Pulls YouTube Data API v3 stats for every
`platform_accounts` row where `platform='youtube'` and
`ingestion_method='automated_api'`, normalizes, and writes
`historical_metrics`/`posts`/`ingestion_runs`. Scheduled 3x/day via pg_cron
(`sql/008_youtube_cron.sql`) instead of GitHub Actions — see the project's
main plan for why (everything YouTube-related stays inside Supabase, no
external secrets needed for this piece).

## Deploy

```sh
supabase functions deploy youtube-ingest
supabase secrets set YOUTUBE_API_KEY=<your key>
supabase secrets set SLACK_WEBHOOK_URL=<your webhook>
```

`SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` are injected automatically by
the Edge Functions runtime — don't set them manually.

## Test manually

```sh
curl -X POST https://<project-ref>.supabase.co/functions/v1/youtube-ingest \
  -H "Authorization: Bearer <service-role-key>"
```

## Schedule

After deploying, run `sql/008_youtube_cron.sql` (with `<PROJECT_REF>` filled
in, and the service-role key stored in Vault first) to wire up the 3x/day
cron via pg_cron + pg_net.

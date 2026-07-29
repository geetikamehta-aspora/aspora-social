-- Schedules the youtube-ingest Edge Function 3x/day via pg_cron + pg_net.
-- Deploy the function FIRST (supabase functions deploy youtube-ingest) and
-- set its secrets (YOUTUBE_API_KEY, SLACK_WEBHOOK_URL) before running this.
--
-- The service-role key must be in Vault (Dashboard -> Project Settings ->
-- Vault -> add secret named 'service_role_key') rather than hardcoded here —
-- this file gets committed to git.

create extension if not exists pg_cron;
create extension if not exists pg_net;

-- Replace <PROJECT_REF> with your actual Supabase project ref.
select cron.schedule(
  'youtube-ingest-morning',
  '0 6 * * *',
  $$
  select net.http_post(
    url := 'https://<PROJECT_REF>.supabase.co/functions/v1/youtube-ingest',
    headers := jsonb_build_object(
      'Authorization', 'Bearer ' || (select decrypted_secret from vault.decrypted_secrets where name = 'service_role_key'),
      'Content-Type', 'application/json'
    )
  );
  $$
);

select cron.schedule(
  'youtube-ingest-afternoon',
  '0 12 * * *',
  $$
  select net.http_post(
    url := 'https://<PROJECT_REF>.supabase.co/functions/v1/youtube-ingest',
    headers := jsonb_build_object(
      'Authorization', 'Bearer ' || (select decrypted_secret from vault.decrypted_secrets where name = 'service_role_key'),
      'Content-Type', 'application/json'
    )
  );
  $$
);

select cron.schedule(
  'youtube-ingest-evening',
  '0 18 * * *',
  $$
  select net.http_post(
    url := 'https://<PROJECT_REF>.supabase.co/functions/v1/youtube-ingest',
    headers := jsonb_build_object(
      'Authorization', 'Bearer ' || (select decrypted_secret from vault.decrypted_secrets where name = 'service_role_key'),
      'Content-Type', 'application/json'
    )
  );
  $$
);

-- To inspect scheduled jobs: select * from cron.job;
-- To unschedule: select cron.unschedule('youtube-ingest-morning');

-- Row Level Security — permissive by design.
--
-- Auth model: Firebase Auth resolves identity; authorization (is this email
-- allowed in, what role) is decided entirely in app code (see
-- web/lib/auth/use-auth.tsx's resolveProfile). There is no Supabase
-- Third-Party-Auth-for-Firebase registration, no custom claims, no session
-- cookies — every browser request presents only the anon key, so Postgres
-- has no way to tell one signed-in user apart from another. Given that,
-- RLS is kept enabled (so this is an explicit, documented "yes, open"
-- rather than a silently-missing check) but permissive on every table the
-- app touches — the app's own UI is what hides admin actions from viewers,
-- not the database. Same trade-off as most Firebase-Auth-plus-a-permissive-
-- backend apps: the real threat model here is "random person stumbles onto
-- the URL," not "a determined user with devtools."
--
-- service_role (the Python upload-parsing job, the youtube-ingest Edge
-- Function) bypasses RLS entirely regardless of any policy here, as always.

alter table public.users enable row level security;
create policy anon_all on public.users for all to public using (true) with check (true);

alter table public.invited_users enable row level security;
create policy anon_all on public.invited_users for all to public using (true) with check (true);

alter table public.brands enable row level security;
create policy anon_all on public.brands for all to public using (true) with check (true);

alter table public.platform_accounts enable row level security;
create policy anon_all on public.platform_accounts for all to public using (true) with check (true);

alter table public.historical_metrics enable row level security;
create policy anon_all on public.historical_metrics for all to public using (true) with check (true);

alter table public.posts enable row level security;
create policy anon_all on public.posts for all to public using (true) with check (true);

alter table public.reports enable row level security;
create policy anon_all on public.reports for all to public using (true) with check (true);

alter table public.ai_insights enable row level security;
create policy anon_all on public.ai_insights for all to public using (true) with check (true);

alter table public.configurations enable row level security;
create policy anon_all on public.configurations for all to public using (true) with check (true);

alter table public.file_uploads enable row level security;
create policy anon_all on public.file_uploads for all to public using (true) with check (true);

alter table public.ingestion_runs enable row level security;
create policy anon_all on public.ingestion_runs for all to public using (true) with check (true);

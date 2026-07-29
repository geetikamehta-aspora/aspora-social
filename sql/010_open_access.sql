-- Full switch to the "Firebase-only auth" pattern: Firebase Auth resolves
-- identity; authorization (is this email allowed, what role) is decided
-- entirely in app code (see web/lib/auth/use-auth.tsx's resolveProfile).
-- There is no more Supabase Third-Party-Auth-for-Firebase registration, no
-- custom claims, no session cookies — every browser request now presents
-- only the anon key, so Postgres/RLS has no way to distinguish one user
-- from another. Accept that and stop pretending otherwise: RLS becomes
-- permissive, and the app's own UI (not the database) is what hides admin
-- actions from viewers. Same trade-off as the reference project this
-- mirrors ("the DB itself doesn't enforce who's a student").
--
-- Run this against the live project (which already has 001-006+008+009
-- applied). Fresh installs get this directly via the rewritten
-- 003_rls.sql instead.

-- Drop every policy that depended on requesting_role()/requesting_firebase_uid().
drop policy if exists users_select on public.users;
drop policy if exists users_insert_self on public.users;
drop policy if exists users_update on public.users;
drop trigger if exists trg_enforce_user_role_immutable on public.users;
drop function if exists public.enforce_user_role_immutable();

drop policy if exists brands_select on public.brands;
drop policy if exists brands_admin_write on public.brands;

drop policy if exists historical_metrics_select on public.historical_metrics;
drop policy if exists historical_metrics_admin_write on public.historical_metrics;
drop policy if exists historical_metrics_admin_update on public.historical_metrics;

drop policy if exists posts_select on public.posts;
drop policy if exists posts_admin_write on public.posts;
drop policy if exists posts_admin_update on public.posts;

drop policy if exists reports_select on public.reports;
drop policy if exists reports_admin_write on public.reports;

drop policy if exists ai_insights_select on public.ai_insights;
drop policy if exists ai_insights_admin_write on public.ai_insights;

drop policy if exists file_uploads_admin_all on public.file_uploads;
drop policy if exists configurations_admin_all on public.configurations;
drop policy if exists platform_accounts_admin_all on public.platform_accounts;
drop policy if exists ingestion_runs_admin_select on public.ingestion_runs;
drop policy if exists invited_users_admin_all on public.invited_users;

drop function if exists public.requesting_role();
drop function if exists public.requesting_firebase_uid();

-- Permissive policy per table — RLS stays enabled (so it's an explicit,
-- documented "yes, open" rather than silently disabled), but every table
-- the app touches is now readable/writable by anyone holding the anon key,
-- same as the app itself. service_role (the scraper / Edge Function) is
-- unaffected either way, as always.
create policy anon_all on public.users for all to public using (true) with check (true);
create policy anon_all on public.invited_users for all to public using (true) with check (true);
create policy anon_all on public.brands for all to public using (true) with check (true);
create policy anon_all on public.platform_accounts for all to public using (true) with check (true);
create policy anon_all on public.historical_metrics for all to public using (true) with check (true);
create policy anon_all on public.posts for all to public using (true) with check (true);
create policy anon_all on public.reports for all to public using (true) with check (true);
create policy anon_all on public.ai_insights for all to public using (true) with check (true);
create policy anon_all on public.configurations for all to public using (true) with check (true);
create policy anon_all on public.file_uploads for all to public using (true) with check (true);
create policy anon_all on public.ingestion_runs for all to public using (true) with check (true);

-- `platform_accounts` itself is admin-only in RLS (003_rls.sql), but every
-- authenticated user (viewer included) needs to see "which accounts are
-- tracked" and their staleness for the dashboard's staleness badges (plan
-- Section 4). Expose a sanitized view instead of relaxing the base table.
create view public.platform_accounts_public as
select
  id,
  brand_id,
  platform,
  handle,
  ingestion_method,
  last_ingested_at,
  last_ingest_status
from public.platform_accounts
where is_active = true;

grant select on public.platform_accounts_public to authenticated;

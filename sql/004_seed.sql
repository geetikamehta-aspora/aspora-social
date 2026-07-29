-- Seed the three real brands and their known platform coverage (plan Section 2).
-- Handles are placeholders — replace 'TODO_SET_HANDLE' with the real @handle /
-- channel ID / company slug for each account before running ingestion.

insert into public.brands (name, slug) values
  ('Aspora', 'aspora'),
  ('NRI Shala', 'nri-shala'),
  ('Aspora Malayalam', 'aspora-malayalam');

-- Aspora: instagram, linkedin, x (all manual_upload) + youtube (automated_api)
insert into public.platform_accounts (brand_id, platform, handle, ingestion_method)
select id, 'instagram', 'TODO_SET_HANDLE', 'manual_upload' from public.brands where slug = 'aspora'
union all
select id, 'linkedin', 'TODO_SET_HANDLE', 'manual_upload' from public.brands where slug = 'aspora'
union all
select id, 'x', 'TODO_SET_HANDLE', 'manual_upload' from public.brands where slug = 'aspora'
union all
select id, 'youtube', 'TODO_SET_HANDLE', 'automated_api' from public.brands where slug = 'aspora';

-- NRI Shala: instagram (manual_upload) + youtube (automated_api)
insert into public.platform_accounts (brand_id, platform, handle, ingestion_method)
select id, 'instagram', 'TODO_SET_HANDLE', 'manual_upload' from public.brands where slug = 'nri-shala'
union all
select id, 'youtube', 'TODO_SET_HANDLE', 'automated_api' from public.brands where slug = 'nri-shala';

-- Aspora Malayalam: instagram (manual_upload) + youtube (automated_api)
insert into public.platform_accounts (brand_id, platform, handle, ingestion_method)
select id, 'instagram', 'TODO_SET_HANDLE', 'manual_upload' from public.brands where slug = 'aspora-malayalam'
union all
select id, 'youtube', 'TODO_SET_HANDLE', 'automated_api' from public.brands where slug = 'aspora-malayalam';

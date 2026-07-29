-- Core schema. See /Users/apple/.claude/plans/cheerful-sleeping-sun.md Section 2 for design rationale.

-- ============================================================================
-- users
-- ============================================================================
-- id is the raw Firebase UID (text), not a generated uuid, so RLS policies can
-- compare it directly against auth.jwt()->>'sub' without a lookup table.
create table public.users (
  id            text primary key,
  email         text not null unique,
  display_name  text,
  photo_url     text,
  role          text not null default 'viewer' check (role in ('admin', 'viewer')),
  is_active     boolean not null default true,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);

-- ============================================================================
-- invited_users — pre-authorization by email, added from /settings/users.
-- Firebase UIDs don't exist until someone actually signs in with Google, so
-- this is the only way to grant a role (in particular, admin) to someone who
-- hasn't logged in yet. Consumed (deleted) the moment that email's first
-- `users` row is created — see the trigger in 003_rls.sql.
-- ============================================================================
create table public.invited_users (
  id            uuid primary key default gen_random_uuid(),
  email         text not null unique,
  display_name  text,
  role          text not null default 'viewer' check (role in ('admin', 'viewer')),
  invited_by    text references public.users(id),
  created_at    timestamptz not null default now()
);

-- ============================================================================
-- brands
-- ============================================================================
create table public.brands (
  id          uuid primary key default gen_random_uuid(),
  name        text not null,
  slug        text not null unique,
  logo_url    text,
  is_active   boolean not null default true,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);

-- ============================================================================
-- platform_accounts
-- ============================================================================
create table public.platform_accounts (
  id                  uuid primary key default gen_random_uuid(),
  brand_id            uuid not null references public.brands(id) on delete cascade,
  platform            text not null check (platform in ('instagram', 'linkedin', 'x', 'youtube')),
  handle              text not null,
  external_id         text,
  -- 'automated_api': YouTube always; Instagram once Meta Graph API access is confirmed for this account.
  -- 'manual_upload': everything else, today.
  ingestion_method    text not null default 'manual_upload' check (ingestion_method in ('automated_api', 'manual_upload')),
  profile_url         text,
  is_active           boolean not null default true,
  last_ingested_at    timestamptz,
  last_ingest_status  text check (last_ingest_status in ('success', 'partial', 'failed')),
  last_ingest_error   text,
  created_at          timestamptz not null default now(),
  updated_at          timestamptz not null default now(),
  unique (brand_id, platform)
);

-- ============================================================================
-- ingestion_runs — bookkeeping for automated-API pulls (YouTube today, Instagram Graph API later)
-- ============================================================================
create table public.ingestion_runs (
  id             uuid primary key default gen_random_uuid(),
  platform       text not null check (platform in ('instagram', 'linkedin', 'x', 'youtube')),
  triggered_by   text not null check (triggered_by in ('schedule', 'manual', 'retry')),
  started_at     timestamptz not null,
  finished_at    timestamptz,
  status         text not null default 'running' check (status in ('running', 'success', 'partial_failure', 'failure')),
  github_run_id  text,
  summary        jsonb,
  created_at     timestamptz not null default now()
);

-- ============================================================================
-- file_uploads — every manually-uploaded report, and the review queue
-- ============================================================================
create table public.file_uploads (
  id                    uuid primary key default gen_random_uuid(),
  brand_id              uuid not null references public.brands(id) on delete cascade,
  platform              text not null check (platform in ('instagram', 'linkedin', 'x', 'youtube')),
  platform_account_id   uuid references public.platform_accounts(id) on delete set null,
  applies_to            text not null default 'single_account' check (applies_to in ('single_account', 'all_accounts')),
  period_start          date not null,
  period_end            date not null,
  -- Files live in Google Drive, not Supabase Storage — a Drive-upload
  -- Apps Script bridge (see /gas/) saves the file into a shared folder, sets
  -- link-sharing to "anyone with the link", and returns these two values.
  -- drive_file_id is what the Python parser fetches by; drive_view_url is
  -- shown in the review-queue UI so a reviewer can open the source file.
  drive_file_id         text not null,
  drive_view_url        text not null,
  file_type             text not null check (file_type in ('csv', 'xlsx', 'pdf', 'image')),
  status                text not null default 'pending' check (status in ('pending', 'processing', 'awaiting_review', 'approved', 'failed')),
  extracted_preview     jsonb,
  column_mapping        jsonb,
  confidence             text check (confidence in ('high', 'low')),
  reviewed_by            text references public.users(id),
  reviewed_at             timestamptz,
  error_message           text,
  uploaded_by             text not null references public.users(id),
  created_at              timestamptz not null default now(),
  updated_at              timestamptz not null default now(),
  check (
    (applies_to = 'single_account' and platform_account_id is not null)
    or (applies_to = 'all_accounts' and platform_account_id is null)
  )
);

-- ============================================================================
-- posts — latest known state of each post, upserted every ingestion event
-- ============================================================================
create table public.posts (
  id                    uuid primary key default gen_random_uuid(),
  platform_account_id   uuid not null references public.platform_accounts(id) on delete cascade,
  platform              text not null check (platform in ('instagram', 'linkedin', 'x', 'youtube')),
  platform_post_id      text not null,
  post_type             text check (post_type in ('image', 'video', 'reel', 'carousel', 'text', 'article', 'short', 'livestream', 'poll', 'other')),
  permalink             text,
  caption               text,
  media_urls            jsonb,
  posted_at             timestamptz,
  first_seen_at         timestamptz not null default now(),
  last_seen_at          timestamptz not null default now(),

  likes                 bigint default 0,
  comments              bigint default 0,
  shares                bigint default 0,
  saves                 bigint default 0,
  impressions           bigint,
  video_views           bigint,
  engagement_rate       numeric(10, 4),

  source                text not null check (source in ('automated_api', 'manual_upload')),
  file_upload_id        uuid references public.file_uploads(id) on delete set null,

  raw_latest            jsonb not null,
  created_at            timestamptz not null default now(),
  updated_at            timestamptz not null default now(),
  unique (platform_account_id, platform_post_id)
);

create index idx_posts_account_posted_at on public.posts (platform_account_id, posted_at desc);
create index idx_posts_engagement on public.posts (platform, engagement_rate desc);

-- ============================================================================
-- historical_metrics — append-only account-level snapshots
-- ============================================================================
create table public.historical_metrics (
  id                    bigint generated always as identity primary key,
  platform_account_id   uuid not null references public.platform_accounts(id) on delete cascade,
  brand_id              uuid not null references public.brands(id) on delete cascade,
  platform              text not null check (platform in ('instagram', 'linkedin', 'x', 'youtube')),
  source                text not null check (source in ('automated_api', 'manual_upload')),
  run_id                uuid references public.ingestion_runs(id) on delete set null,
  file_upload_id        uuid references public.file_uploads(id) on delete set null,
  scraped_at            timestamptz not null,

  followers_count       bigint,
  following_count       bigint,
  posts_count           bigint,
  impressions_total     bigint,
  likes_total           bigint,
  comments_total        bigint,
  shares_total          bigint,
  saves_total           bigint,
  video_views_total     bigint,
  engagement_rate       numeric(10, 4),
  follower_delta        bigint,

  raw_payload           jsonb not null,
  created_at            timestamptz not null default now(),

  check (
    (source = 'automated_api' and run_id is not null and file_upload_id is null)
    or (source = 'manual_upload' and file_upload_id is not null and run_id is null)
  )
);

create index idx_hist_metrics_account_time on public.historical_metrics (platform_account_id, scraped_at desc);
create index idx_hist_metrics_brand_time on public.historical_metrics (brand_id, scraped_at desc);

-- ============================================================================
-- reports
-- ============================================================================
create table public.reports (
  id             uuid primary key default gen_random_uuid(),
  brand_id       uuid not null references public.brands(id) on delete cascade,
  title          text not null,
  report_type    text not null check (report_type in ('daily', 'weekly', 'monthly', 'custom', 'ad_hoc')),
  period_start   date not null,
  period_end     date not null,
  status         text not null default 'draft' check (status in ('draft', 'generated', 'published')),
  generated_by   text references public.users(id),
  data_snapshot  jsonb,
  ai_summary     text,
  created_at     timestamptz not null default now(),
  updated_at     timestamptz not null default now()
);

-- ============================================================================
-- ai_insights
-- ============================================================================
create table public.ai_insights (
  id                  uuid primary key default gen_random_uuid(),
  brand_id            uuid not null references public.brands(id) on delete cascade,
  platform            text check (platform in ('instagram', 'linkedin', 'x', 'youtube', 'all')),
  scope               text not null check (scope in ('daily', 'weekly', 'monthly', 'run', 'report')),
  period_start        date,
  period_end          date,
  related_run_id      uuid references public.ingestion_runs(id) on delete set null,
  related_report_id   uuid references public.reports(id) on delete set null,

  input_metrics_ref   jsonb not null,
  model               text not null,
  prompt_version      text not null,
  summary             text not null,
  highlights          jsonb,
  recommendations     jsonb,
  raw_response        jsonb,
  tokens_used         integer,
  cost_usd            numeric(10, 4),

  created_at          timestamptz not null default now()
);

create index idx_ai_insights_brand_scope_period on public.ai_insights (brand_id, scope, period_end desc);

-- ============================================================================
-- configurations
-- ============================================================================
create table public.configurations (
  id           uuid primary key default gen_random_uuid(),
  key          text not null unique,
  value        jsonb not null,
  description  text,
  updated_by   text references public.users(id),
  updated_at   timestamptz not null default now(),
  created_at   timestamptz not null default now()
);

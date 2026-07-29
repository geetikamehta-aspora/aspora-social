-- RPC used by the dashboard's Recharts time-series views (plan Section 4),
-- so the browser never has to pull raw historical_metrics rows for wide date
-- ranges. Still RLS-protected — callers hit this via supabase.rpc(...) under
-- their own session, and the underlying table's RLS policies still apply.
create or replace function public.get_daily_metrics(
  p_brand_id uuid,
  p_platform text,
  p_from date,
  p_to date
)
returns table (
  day date,
  followers_count bigint,
  follower_delta bigint,
  engagement_rate numeric,
  posts_count bigint,
  video_views_total bigint
)
language sql
stable
as $$
  select
    date(scraped_at) as day,
    -- last snapshot of the day wins if there were multiple ingestion events
    (array_agg(followers_count order by scraped_at desc))[1] as followers_count,
    (array_agg(follower_delta order by scraped_at desc))[1] as follower_delta,
    (array_agg(engagement_rate order by scraped_at desc))[1] as engagement_rate,
    (array_agg(posts_count order by scraped_at desc))[1] as posts_count,
    (array_agg(video_views_total order by scraped_at desc))[1] as video_views_total
  from public.historical_metrics
  where brand_id = p_brand_id
    and platform = p_platform
    and scraped_at >= p_from
    and scraped_at < (p_to + 1)
  group by date(scraped_at)
  order by day;
$$;

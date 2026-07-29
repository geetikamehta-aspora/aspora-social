// YouTube Data API v3 ingestion — the one platform that stays fully
// automated (official API, API-key auth, zero ToS/ban risk). Runs as a
// Supabase Edge Function on a pg_cron schedule (see sql/008_youtube_cron.sql)
// rather than GitHub Actions, so everything stays inside Supabase and the
// service-role key never needs to leave it.
//
// Deploy: supabase functions deploy youtube-ingest
// Secrets: supabase secrets set YOUTUBE_API_KEY=... SLACK_WEBHOOK_URL=...
// (SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY are injected automatically.)

import { createClient } from "npm:@supabase/supabase-js@2";

import { notifyIngestionFailure } from "../_shared/alerts.ts";
import {
  computeEngagementRate,
  type NormalizedAccountSnapshot,
  type NormalizedPost,
} from "../_shared/normalize.ts";

const MAX_RECENT_VIDEOS = 50;
const YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3";

function getSupabaseClient() {
  return createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  );
}

async function youtubeGet(path: string, params: Record<string, string>) {
  const apiKey = Deno.env.get("YOUTUBE_API_KEY")!;
  const url = new URL(`${YOUTUBE_API_BASE}/${path}`);
  for (const [k, v] of Object.entries(params)) url.searchParams.set(k, v);
  url.searchParams.set("key", apiKey);

  const res = await fetch(url.toString());
  if (!res.ok) {
    throw new Error(`YouTube API ${path} failed: ${res.status} ${await res.text()}`);
  }
  return await res.json();
}

function mapChannelSnapshot(channel: any): NormalizedAccountSnapshot {
  const stats = channel.statistics ?? {};
  return {
    platform: "youtube",
    scrapedAt: new Date().toISOString(),
    followersCount: stats.subscriberCount ? Number(stats.subscriberCount) : null,
    followingCount: null,
    postsCount: stats.videoCount ? Number(stats.videoCount) : null,
    impressionsTotal: null,
    likesTotal: null,
    commentsTotal: null,
    sharesTotal: null,
    savesTotal: null,
    videoViewsTotal: stats.viewCount ? Number(stats.viewCount) : null,
    engagementRate: null,
    rawPayload: channel,
  };
}

function mapVideoPost(video: any): NormalizedPost {
  const stats = video.statistics ?? {};
  const snippet = video.snippet ?? {};
  const likes = stats.likeCount ? Number(stats.likeCount) : 0;
  const comments = stats.commentCount ? Number(stats.commentCount) : 0;
  const views = stats.viewCount ? Number(stats.viewCount) : null;

  return {
    platform: "youtube",
    platformPostId: video.id,
    postType: "video",
    permalink: `https://www.youtube.com/watch?v=${video.id}`,
    caption: snippet.title ?? null,
    postedAt: snippet.publishedAt ?? null,
    likes,
    comments,
    shares: 0,
    saves: 0,
    impressions: null,
    videoViews: views,
    engagementRate: computeEngagementRate({ likes, comments, followers: views }),
    rawLatest: video,
  };
}

async function ingestAccount(supabase: ReturnType<typeof getSupabaseClient>, account: any, runId: string) {
  const channelId = account.external_id || account.handle;
  const channelResp = await youtubeGet("channels", {
    part: "statistics,snippet,contentDetails",
    id: channelId,
  });
  const channel = channelResp.items?.[0];
  if (!channel) throw new Error(`YouTube channel not found: ${channelId}`);

  const snapshot = mapChannelSnapshot(channel);

  const { data: previous } = await supabase
    .from("historical_metrics")
    .select("followers_count")
    .eq("platform_account_id", account.id)
    .order("scraped_at", { ascending: false })
    .limit(1);
  const prevFollowers = previous?.[0]?.followers_count ?? null;
  const followerDelta = snapshot.followersCount !== null && prevFollowers !== null
    ? snapshot.followersCount - prevFollowers
    : null;

  const { error: metricError } = await supabase.from("historical_metrics").insert({
    platform_account_id: account.id,
    brand_id: account.brand_id,
    platform: "youtube",
    source: "automated_api",
    run_id: runId,
    scraped_at: snapshot.scrapedAt,
    followers_count: snapshot.followersCount,
    following_count: snapshot.followingCount,
    posts_count: snapshot.postsCount,
    impressions_total: snapshot.impressionsTotal,
    likes_total: snapshot.likesTotal,
    comments_total: snapshot.commentsTotal,
    shares_total: snapshot.sharesTotal,
    saves_total: snapshot.savesTotal,
    video_views_total: snapshot.videoViewsTotal,
    engagement_rate: snapshot.engagementRate,
    follower_delta: followerDelta,
    raw_payload: snapshot.rawPayload,
  });
  if (metricError) throw metricError;

  const uploadsPlaylistId = channel.contentDetails?.relatedPlaylists?.uploads;
  let videoCount = 0;
  if (uploadsPlaylistId) {
    const playlistResp = await youtubeGet("playlistItems", {
      part: "contentDetails",
      playlistId: uploadsPlaylistId,
      maxResults: String(MAX_RECENT_VIDEOS),
    });
    const videoIds = (playlistResp.items ?? []).map((item: any) => item.contentDetails.videoId);

    if (videoIds.length > 0) {
      const videosResp = await youtubeGet("videos", {
        part: "statistics,snippet",
        id: videoIds.join(","),
      });
      for (const video of videosResp.items ?? []) {
        const post = mapVideoPost(video);
        const { error: postError } = await supabase.from("posts").upsert(
          {
            platform_account_id: account.id,
            platform: "youtube",
            platform_post_id: post.platformPostId,
            post_type: post.postType,
            permalink: post.permalink,
            caption: post.caption,
            posted_at: post.postedAt,
            likes: post.likes,
            comments: post.comments,
            shares: post.shares,
            saves: post.saves,
            impressions: post.impressions,
            video_views: post.videoViews,
            engagement_rate: post.engagementRate,
            source: "automated_api",
            raw_latest: post.rawLatest,
            last_seen_at: new Date().toISOString(),
          },
          { onConflict: "platform_account_id,platform_post_id" },
        );
        if (postError) throw postError;
        videoCount++;
      }
    }
  }

  return { status: "success", videosIngested: videoCount };
}

Deno.serve(async (_req) => {
  const supabase = getSupabaseClient();
  const startedAt = new Date().toISOString();

  const { data: run, error: runInsertError } = await supabase
    .from("ingestion_runs")
    .insert({ platform: "youtube", triggered_by: "schedule", started_at: startedAt, status: "running" })
    .select("id")
    .single();
  if (runInsertError || !run) {
    return new Response(JSON.stringify({ error: "Failed to create ingestion_runs row" }), { status: 500 });
  }

  const { data: accounts, error: accountsError } = await supabase
    .from("platform_accounts")
    .select("*")
    .eq("platform", "youtube")
    .eq("ingestion_method", "automated_api")
    .eq("is_active", true);
  if (accountsError) {
    return new Response(JSON.stringify({ error: accountsError.message }), { status: 500 });
  }

  const summary: Record<string, unknown> = {};
  let anySuccess = false;
  let anyFailure = false;

  for (const account of accounts ?? []) {
    try {
      const result = await ingestAccount(supabase, account, run.id);
      summary[account.handle] = result;
      anySuccess = true;
      await supabase
        .from("platform_accounts")
        .update({ last_ingest_status: "success", last_ingest_error: null, last_ingested_at: new Date().toISOString() })
        .eq("id", account.id);
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      summary[account.handle] = { status: "failed", error: message };
      anyFailure = true;
      await supabase
        .from("platform_accounts")
        .update({ last_ingest_status: "failed", last_ingest_error: message, last_ingested_at: new Date().toISOString() })
        .eq("id", account.id);
      await notifyIngestionFailure(`youtube (${account.handle})`, message);
    }
  }

  const status = anySuccess && !anyFailure ? "success" : anySuccess ? "partial_failure" : "failure";
  await supabase
    .from("ingestion_runs")
    .update({ status, finished_at: new Date().toISOString(), summary })
    .eq("id", run.id);

  return new Response(JSON.stringify({ status, summary }), {
    status: status === "failure" ? 500 : 200,
    headers: { "Content-Type": "application/json" },
  });
});

// The canonical contract every ingestion source must satisfy — TypeScript
// mirror of scraper/aspora_scraper/normalize/schema.py. Whether data came
// from this Edge Function's YouTube pull or the Python upload-parsing
// pipeline, it ends up shaped like this before being written to Supabase.

export type Platform = "instagram" | "linkedin" | "x" | "youtube";
export type Source = "automated_api" | "manual_upload";

export type NormalizedAccountSnapshot = {
  platform: Platform;
  scrapedAt: string; // ISO timestamp
  followersCount: number | null;
  followingCount: number | null;
  postsCount: number | null;
  impressionsTotal: number | null;
  likesTotal: number | null;
  commentsTotal: number | null;
  sharesTotal: number | null;
  savesTotal: number | null;
  videoViewsTotal: number | null;
  engagementRate: number | null;
  rawPayload: Record<string, unknown>;
};

export type NormalizedPost = {
  platform: Platform;
  platformPostId: string;
  postType: string | null;
  permalink: string | null;
  caption: string | null;
  postedAt: string | null;
  likes: number;
  comments: number;
  shares: number;
  saves: number;
  impressions: number | null;
  videoViews: number | null;
  engagementRate: number | null;
  rawLatest: Record<string, unknown>;
};

export function computeEngagementRate(
  { likes = 0, comments = 0, shares = 0, saves = 0, followers }: {
    likes?: number;
    comments?: number;
    shares?: number;
    saves?: number;
    followers: number | null;
  },
): number | null {
  if (!followers) return null;
  return (likes + comments + shares + saves) / followers;
}

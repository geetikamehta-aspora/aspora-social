import { useQuery } from "@tanstack/react-query";

import { supabase } from "@/lib/supabase/client";

export type DailyMetric = {
  day: string;
  followers_count: number | null;
  follower_delta: number | null;
  engagement_rate: number | null;
  posts_count: number | null;
  video_views_total: number | null;
};

/**
 * Wraps the get_daily_metrics RPC (sql/005_rpc.sql) so wide date ranges never
 * pull raw historical_metrics rows into the browser. Still RLS-protected —
 * this runs under the caller's own session via supabase.rpc().
 */
export function useDailyMetrics(brandId: string | undefined, platform: string, from: string, to: string) {
  return useQuery({
    queryKey: ["daily-metrics", brandId, platform, from, to],
    enabled: !!brandId,
    queryFn: async (): Promise<DailyMetric[]> => {
      const { data, error } = await supabase.rpc("get_daily_metrics", {
        p_brand_id: brandId,
        p_platform: platform,
        p_from: from,
        p_to: to,
      });
      if (error) throw error;
      return data;
    },
  });
}

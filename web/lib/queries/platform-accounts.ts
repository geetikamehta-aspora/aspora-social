import { useQuery } from "@tanstack/react-query";

import { supabase } from "@/lib/supabase/client";

export type PlatformAccount = {
  id: string;
  brand_id: string;
  platform: "instagram" | "linkedin" | "x" | "youtube";
  handle: string;
  ingestion_method: "automated_api" | "manual_upload";
  last_ingested_at: string | null;
  last_ingest_status: "success" | "partial" | "failed" | null;
};

export function usePlatformAccounts(brandId: string | undefined) {
  return useQuery({
    queryKey: ["platform-accounts", brandId],
    enabled: !!brandId,
    queryFn: async (): Promise<PlatformAccount[]> => {
      // platform_accounts itself is admin-only in RLS; this sanitized view
      // (sql/006_views.sql) is what lets viewers see staleness too.
      const { data, error } = await supabase
        .from("platform_accounts_public")
        .select("id, brand_id, platform, handle, ingestion_method, last_ingested_at, last_ingest_status")
        .eq("brand_id", brandId)
        .order("platform");
      if (error) throw error;
      return data;
    },
  });
}

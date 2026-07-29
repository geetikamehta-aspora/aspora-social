import { useMutation, useQueryClient } from "@tanstack/react-query";

import { type FileUpload } from "@/lib/queries/uploads";
import { supabase } from "@/lib/supabase/client";

type CanonicalSnapshot = {
  followers_count: number | null;
  following_count: number | null;
  posts_count: number | null;
  impressions_total: number | null;
  likes_total: number | null;
  comments_total: number | null;
  shares_total: number | null;
  saves_total: number | null;
  video_views_total: number | null;
};

async function markApproved(uploadId: string, reviewerId: string) {
  const { error } = await supabase
    .from("file_uploads")
    .update({ status: "approved", reviewed_by: reviewerId, reviewed_at: new Date().toISOString() })
    .eq("id", uploadId);
  if (error) throw error;
}

/**
 * CSV/XLSX path (confidence='high'): one historical_metrics row per parsed
 * row. This is the "fast one-click confirm" case from plan Section 5/4 —
 * the click itself is what commits the already-deterministic parse.
 */
export function useApproveTabularUpload() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ upload, reviewerId }: { upload: FileUpload; reviewerId: string }) => {
      if (!upload.platform_account_id) {
        throw new Error(
          "This upload applies to all accounts — multi-account fan-out isn't wired up yet. " +
            "Split it into one upload per account, or resolve manually before approving."
        );
      }
      const rows = (upload.extracted_preview?.rows ?? []) as Array<
        CanonicalSnapshot & { date?: string }
      >;
      if (rows.length === 0) throw new Error("No rows to commit.");

      const inserts = rows.map((row) => ({
        platform_account_id: upload.platform_account_id,
        brand_id: upload.brand_id,
        platform: upload.platform,
        source: "manual_upload" as const,
        file_upload_id: upload.id,
        scraped_at: row.date ? new Date(row.date).toISOString() : `${upload.period_end}T00:00:00Z`,
        followers_count: row.followers_count ?? null,
        following_count: row.following_count ?? null,
        posts_count: row.posts_count ?? null,
        impressions_total: row.impressions_total ?? null,
        likes_total: row.likes_total ?? null,
        comments_total: row.comments_total ?? null,
        shares_total: row.shares_total ?? null,
        saves_total: row.saves_total ?? null,
        video_views_total: row.video_views_total ?? null,
        raw_payload: row,
      }));

      const { error } = await supabase.from("historical_metrics").insert(inserts);
      if (error) throw error;

      await markApproved(upload.id, reviewerId);
    },
    onSuccess: (_data, { upload }) => {
      queryClient.invalidateQueries({ queryKey: ["file-uploads"] });
      queryClient.invalidateQueries({ queryKey: ["file-upload", upload.id] });
      queryClient.invalidateQueries({ queryKey: ["daily-metrics"] });
    },
  });
}

/**
 * PDF/image path (confidence='low'): one historical_metrics row from
 * reviewer-edited values. The reviewer's typed-in numbers are the source of
 * truth here, not whatever the parser/vision model originally extracted —
 * `values` is deliberately a fresh form state, not extracted_preview itself.
 */
export function useApproveSnapshotUpload() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({
      upload,
      values,
      reviewerId,
    }: {
      upload: FileUpload;
      values: CanonicalSnapshot;
      reviewerId: string;
    }) => {
      if (!upload.platform_account_id) {
        throw new Error(
          "This upload applies to all accounts — multi-account fan-out isn't wired up yet. " +
            "Split it into one upload per account, or resolve manually before approving."
        );
      }

      const { error } = await supabase.from("historical_metrics").insert({
        platform_account_id: upload.platform_account_id,
        brand_id: upload.brand_id,
        platform: upload.platform,
        source: "manual_upload",
        file_upload_id: upload.id,
        scraped_at: `${upload.period_end}T00:00:00Z`,
        ...values,
        raw_payload: { ...values, extracted_preview: upload.extracted_preview },
      });
      if (error) throw error;

      await markApproved(upload.id, reviewerId);
    },
    onSuccess: (_data, { upload }) => {
      queryClient.invalidateQueries({ queryKey: ["file-uploads"] });
      queryClient.invalidateQueries({ queryKey: ["file-upload", upload.id] });
      queryClient.invalidateQueries({ queryKey: ["daily-metrics"] });
    },
  });
}

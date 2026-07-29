import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { supabase } from "@/lib/supabase/client";

export type FileUpload = {
  id: string;
  brand_id: string;
  platform: "instagram" | "linkedin" | "x" | "youtube";
  platform_account_id: string | null;
  applies_to: "single_account" | "all_accounts";
  period_start: string;
  period_end: string;
  drive_file_id: string;
  drive_view_url: string;
  file_type: "csv" | "xlsx" | "pdf" | "image";
  status: "pending" | "processing" | "awaiting_review" | "approved" | "failed";
  extracted_preview: Record<string, unknown> | null;
  column_mapping: Record<string, string> | null;
  confidence: "high" | "low" | null;
  error_message: string | null;
  created_at: string;
};

export function useFileUploads(brandId: string | undefined) {
  return useQuery({
    queryKey: ["file-uploads", brandId],
    enabled: !!brandId,
    queryFn: async (): Promise<FileUpload[]> => {
      const { data, error } = await supabase
        .from("file_uploads")
        .select("*")
        .eq("brand_id", brandId)
        .order("created_at", { ascending: false });
      if (error) throw error;
      return data;
    },
  });
}

export function useFileUpload(uploadId: string | undefined) {
  return useQuery({
    queryKey: ["file-upload", uploadId],
    enabled: !!uploadId,
    queryFn: async (): Promise<FileUpload> => {
      const { data, error } = await supabase
        .from("file_uploads")
        .select("*")
        .eq("id", uploadId)
        .single();
      if (error) throw error;
      return data;
    },
  });
}

function inferFileType(file: File): FileUpload["file_type"] {
  const ext = file.name.split(".").pop()?.toLowerCase();
  if (ext === "csv") return "csv";
  if (ext === "xlsx" || ext === "xls") return "xlsx";
  if (ext === "pdf") return "pdf";
  return "image";
}

export function useCreateUpload() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (input: {
      brandId: string;
      brandSlug: string;
      platform: FileUpload["platform"];
      platformAccountId: string | null;
      appliesTo: "single_account" | "all_accounts";
      periodStart: string;
      periodEnd: string;
      file: File;
      uploadedBy: string;
    }) => {
      const fileType = inferFileType(input.file);

      // Bytes go through the server (the only place that holds the GAS
      // shared secret) and land in Drive, not Supabase Storage, organized
      // as <root>/<period end date>/<platform>/<brand slug>/<filename>.
      const formData = new FormData();
      formData.append("file", input.file);
      formData.append(
        "pathParts",
        JSON.stringify([input.periodEnd, input.platform, input.brandSlug])
      );
      const driveResponse = await fetch("/api/uploads/drive", { method: "POST", body: formData });
      const driveResult = await driveResponse.json();
      if (!driveResponse.ok || driveResult.error) {
        throw new Error(driveResult.error ?? "Failed to upload file to Drive");
      }

      // The metadata row is still inserted directly from the browser under
      // the admin's own session (RLS-gated), matching the rest of the
      // dashboard's write pattern.
      const { error: insertError } = await supabase.from("file_uploads").insert({
        brand_id: input.brandId,
        platform: input.platform,
        platform_account_id: input.appliesTo === "single_account" ? input.platformAccountId : null,
        applies_to: input.appliesTo,
        period_start: input.periodStart,
        period_end: input.periodEnd,
        drive_file_id: driveResult.fileId,
        drive_view_url: driveResult.viewUrl,
        file_type: fileType,
        uploaded_by: input.uploadedBy,
      });
      if (insertError) throw insertError;
    },
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["file-uploads"] }),
  });
}

export function useRejectUpload() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, note }: { id: string; note: string }) => {
      const { error } = await supabase
        .from("file_uploads")
        .update({ status: "failed", error_message: note || "Rejected by reviewer" })
        .eq("id", id);
      if (error) throw error;
    },
    onSuccess: (_data, { id }) => {
      queryClient.invalidateQueries({ queryKey: ["file-uploads"] });
      queryClient.invalidateQueries({ queryKey: ["file-upload", id] });
    },
  });
}

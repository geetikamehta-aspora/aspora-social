"use client";

import { useParams, useRouter } from "next/navigation";
import { useState } from "react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuth } from "@/lib/auth/use-auth";
import { useApproveSnapshotUpload, useApproveTabularUpload } from "@/lib/queries/approve-upload";
import { useFileUpload, useRejectUpload } from "@/lib/queries/uploads";

const CANONICAL_FIELDS = [
  "followers_count",
  "following_count",
  "posts_count",
  "impressions_total",
  "likes_total",
  "comments_total",
  "shares_total",
  "saves_total",
  "video_views_total",
] as const;

type CanonicalKey = (typeof CANONICAL_FIELDS)[number];

function TabularReview({ uploadId }: { uploadId: string }) {
  const { user } = useAuth();
  const router = useRouter();
  const { data: upload } = useFileUpload(uploadId);
  const approve = useApproveTabularUpload();
  const reject = useRejectUpload();

  if (!upload) return null;
  const preview = upload.extracted_preview as {
    row_count?: number;
    column_mapping?: Record<string, string>;
    unmapped_columns?: string[];
  } | null;

  return (
    <div className="flex flex-col gap-4">
      <p className="text-sm">
        <strong>{preview?.row_count ?? 0}</strong> rows parsed from this {upload.file_type.toUpperCase()}.
      </p>
      <div>
        <p className="mb-1 text-sm font-medium">Column mapping used</p>
        <ul className="text-sm text-muted-foreground">
          {Object.entries(preview?.column_mapping ?? {}).map(([source, target]) => (
            <li key={source}>
              {source} → {target}
            </li>
          ))}
        </ul>
        {preview?.unmapped_columns && preview.unmapped_columns.length > 0 && (
          <p className="mt-2 text-xs text-amber-600">
            Ignored columns (not mapped): {preview.unmapped_columns.join(", ")}
          </p>
        )}
      </div>
      <div className="flex gap-2">
        <Button
          disabled={approve.isPending}
          onClick={async () => {
            if (!user) return;
            try {
              await approve.mutateAsync({ upload, reviewerId: user.uid });
              toast.success("Approved and committed to historical data.");
              router.push("/settings/uploads");
            } catch (err) {
              toast.error(err instanceof Error ? err.message : "Failed to approve");
            }
          }}
        >
          Looks right — Approve
        </Button>
        <Button
          variant="outline"
          onClick={async () => {
            await reject.mutateAsync({ id: upload.id, note: "Column mapping looked wrong" });
            router.push("/settings/uploads");
          }}
        >
          Reject
        </Button>
      </div>
    </div>
  );
}

function SnapshotReview({ uploadId }: { uploadId: string }) {
  const { user } = useAuth();
  const router = useRouter();
  const { data: upload } = useFileUpload(uploadId);
  const approve = useApproveSnapshotUpload();
  const reject = useRejectUpload();

  const extracted = (upload?.extracted_preview as { extracted?: Record<string, unknown> } | null)
    ?.extracted;

  const [values, setValues] = useState<Record<CanonicalKey, string>>(() => {
    const initial = {} as Record<CanonicalKey, string>;
    for (const field of CANONICAL_FIELDS) {
      const raw = extracted?.[field];
      initial[field] = raw === null || raw === undefined ? "" : String(raw);
    }
    return initial;
  });

  if (!upload) return null;

  return (
    <div className="flex flex-col gap-4">
      {upload.file_type === "pdf" && (
        <div>
          <p className="mb-1 text-sm font-medium">Raw extracted tables (reference only)</p>
          <pre className="max-h-64 overflow-auto rounded-md bg-muted p-3 text-xs">
            {JSON.stringify(upload.extracted_preview, null, 2)}
          </pre>
        </div>
      )}
      {upload.file_type === "image" && (
        <p className="text-sm text-muted-foreground">
          Values below were read from the screenshot by AI vision — verify against the source
          image before approving.
        </p>
      )}

      <div className="grid grid-cols-2 gap-3">
        {CANONICAL_FIELDS.map((field) => (
          <label key={field} className="text-sm">
            <span className="mb-1 block text-muted-foreground">{field}</span>
            <input
              type="number"
              className="h-9 w-full rounded-lg border border-border bg-background px-3"
              value={values[field]}
              onChange={(e) => setValues((v) => ({ ...v, [field]: e.target.value }))}
            />
          </label>
        ))}
      </div>

      <div className="flex gap-2">
        <Button
          disabled={approve.isPending}
          onClick={async () => {
            if (!user) return;
            const parsed = Object.fromEntries(
              CANONICAL_FIELDS.map((f) => [f, values[f] === "" ? null : Number(values[f])])
            ) as Record<CanonicalKey, number | null>;
            try {
              await approve.mutateAsync({ upload, values: parsed, reviewerId: user.uid });
              toast.success("Approved and committed to historical data.");
              router.push("/settings/uploads");
            } catch (err) {
              toast.error(err instanceof Error ? err.message : "Failed to approve");
            }
          }}
        >
          Approve
        </Button>
        <Button
          variant="outline"
          onClick={async () => {
            await reject.mutateAsync({ id: upload.id, note: "Extracted values looked wrong" });
            router.push("/settings/uploads");
          }}
        >
          Reject
        </Button>
      </div>
    </div>
  );
}

export default function UploadReviewPage() {
  const params = useParams<{ uploadId: string }>();
  const { data: upload, isLoading } = useFileUpload(params.uploadId);

  if (isLoading) return <p className="text-sm text-muted-foreground">Loading...</p>;
  if (!upload) return <p className="text-sm text-muted-foreground">Upload not found.</p>;

  return (
    <div className="flex flex-col gap-4">
      <h1 className="text-lg font-semibold capitalize">
        Review: {upload.platform} ({upload.file_type})
      </h1>
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <span>
              {upload.period_start} → {upload.period_end}
            </span>
            <a
              href={upload.drive_view_url}
              target="_blank"
              rel="noreferrer"
              className="text-xs font-normal underline"
            >
              View source file in Drive
            </a>
          </CardTitle>
        </CardHeader>
        <CardContent>
          {upload.confidence === "high" ? (
            <TabularReview uploadId={upload.id} />
          ) : (
            <SnapshotReview uploadId={upload.id} />
          )}
        </CardContent>
      </Card>
    </div>
  );
}

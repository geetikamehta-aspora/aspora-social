"use client";

import Link from "next/link";
import { useState } from "react";
import { toast } from "sonner";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { useAuth } from "@/lib/auth/use-auth";
import { useBrands } from "@/lib/queries/brands";
import { usePlatformAccounts } from "@/lib/queries/platform-accounts";
import { useCreateUpload, useFileUploads } from "@/lib/queries/uploads";

const PLATFORMS = ["instagram", "linkedin", "x", "youtube"] as const;

const STATUS_VARIANT = {
  pending: "default",
  processing: "default",
  awaiting_review: "warning",
  approved: "success",
  failed: "danger",
} as const;

export default function UploadsPage() {
  const { user } = useAuth();
  const { data: brands } = useBrands();
  const [brandId, setBrandId] = useState<string | undefined>(undefined);
  const activeBrandId = brandId ?? brands?.[0]?.id;
  const activeBrand = brands?.find((b) => b.id === activeBrandId);

  const [platform, setPlatform] = useState<(typeof PLATFORMS)[number]>("linkedin");
  const [appliesTo, setAppliesTo] = useState<"single_account" | "all_accounts">("single_account");
  const [platformAccountId, setPlatformAccountId] = useState<string>("");
  const [periodStart, setPeriodStart] = useState("");
  const [periodEnd, setPeriodEnd] = useState("");
  const [file, setFile] = useState<File | null>(null);

  const { data: accounts } = usePlatformAccounts(activeBrandId);
  const accountsForPlatform = accounts?.filter((a) => a.platform === platform) ?? [];

  const { data: uploads, isLoading } = useFileUploads(activeBrandId);
  const createUpload = useCreateUpload();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!activeBrandId || !activeBrand || !file || !user) return;
    if (appliesTo === "single_account" && !platformAccountId) {
      toast.error("Select an account, or choose 'applies to all accounts'.");
      return;
    }

    try {
      await createUpload.mutateAsync({
        brandId: activeBrandId,
        brandSlug: activeBrand.slug,
        platform,
        platformAccountId: appliesTo === "single_account" ? platformAccountId : null,
        appliesTo,
        periodStart,
        periodEnd,
        file,
        uploadedBy: user.uid,
      });
      toast.success("Uploaded — it'll be parsed within ~10-15 minutes.");
      setFile(null);
    } catch (err) {
      console.error(err);
      toast.error("Upload failed.");
    }
  }

  return (
    <div className="flex flex-col gap-6">
      <h1 className="text-lg font-semibold">Uploads</h1>

      <Card>
        <CardContent className="p-4">
          <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-3">
            <select
              className="h-9 rounded-lg border border-border bg-background px-3 text-sm"
              value={activeBrandId ?? ""}
              onChange={(e) => setBrandId(e.target.value)}
            >
              {brands?.map((b) => (
                <option key={b.id} value={b.id}>
                  {b.name}
                </option>
              ))}
            </select>

            <select
              className="h-9 rounded-lg border border-border bg-background px-3 text-sm capitalize"
              value={platform}
              onChange={(e) => setPlatform(e.target.value as (typeof PLATFORMS)[number])}
            >
              {PLATFORMS.map((p) => (
                <option key={p} value={p}>
                  {p}
                </option>
              ))}
            </select>

            <label className="col-span-2 flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={appliesTo === "all_accounts"}
                onChange={(e) => setAppliesTo(e.target.checked ? "all_accounts" : "single_account")}
              />
              This file covers all accounts on this platform
            </label>

            {appliesTo === "single_account" && (
              <select
                className="col-span-2 h-9 rounded-lg border border-border bg-background px-3 text-sm"
                value={platformAccountId}
                onChange={(e) => setPlatformAccountId(e.target.value)}
              >
                <option value="">Select account...</option>
                {accountsForPlatform.map((a) => (
                  <option key={a.id} value={a.id}>
                    @{a.handle}
                  </option>
                ))}
              </select>
            )}

            <input
              type="date"
              required
              className="h-9 rounded-lg border border-border bg-background px-3 text-sm"
              value={periodStart}
              onChange={(e) => setPeriodStart(e.target.value)}
            />
            <input
              type="date"
              required
              className="h-9 rounded-lg border border-border bg-background px-3 text-sm"
              value={periodEnd}
              onChange={(e) => setPeriodEnd(e.target.value)}
            />

            <input
              type="file"
              required
              accept=".csv,.xlsx,.xls,.pdf,image/*"
              className="col-span-2 text-sm"
              onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            />

            <Button type="submit" disabled={createUpload.isPending} className="col-span-2">
              {createUpload.isPending ? "Uploading..." : "Upload"}
            </Button>
          </form>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="p-0">
          {isLoading && <p className="p-4 text-sm text-muted-foreground">Loading...</p>}
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border text-left text-muted-foreground">
                <th className="p-3">Platform</th>
                <th className="p-3">Period</th>
                <th className="p-3">Type</th>
                <th className="p-3">Status</th>
                <th className="p-3" />
              </tr>
            </thead>
            <tbody>
              {uploads?.map((upload) => (
                <tr key={upload.id} className="border-b border-border last:border-0">
                  <td className="p-3 capitalize">{upload.platform}</td>
                  <td className="p-3">
                    {upload.period_start} → {upload.period_end}
                  </td>
                  <td className="p-3 uppercase">{upload.file_type}</td>
                  <td className="p-3">
                    <Badge variant={STATUS_VARIANT[upload.status]}>{upload.status}</Badge>
                  </td>
                  <td className="p-3">
                    {upload.status === "awaiting_review" && (
                      <Link href={`/settings/uploads/${upload.id}`} className="text-sm underline">
                        Review
                      </Link>
                    )}
                    {upload.status === "failed" && upload.error_message && (
                      <span className="text-xs text-red-600">{upload.error_message}</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </CardContent>
      </Card>
    </div>
  );
}

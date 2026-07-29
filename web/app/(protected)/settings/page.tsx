"use client";

import { StalenessBadge } from "@/components/staleness-badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useBrands } from "@/lib/queries/brands";
import { usePlatformAccounts } from "@/lib/queries/platform-accounts";

function BrandAccounts({ brandId, brandName }: { brandId: string; brandName: string }) {
  const { data: accounts } = usePlatformAccounts(brandId);
  return (
    <Card>
      <CardHeader>
        <CardTitle>{brandName}</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-2">
        {accounts?.map((account) => (
          <div key={account.id} className="flex items-center justify-between text-sm">
            <span className="capitalize">
              {account.platform} — @{account.handle}{" "}
              <span className="text-xs text-muted-foreground">
                ({account.ingestion_method === "automated_api" ? "automated" : "manual upload"})
              </span>
            </span>
            <StalenessBadge lastIngestedAt={account.last_ingested_at} />
          </div>
        ))}
        {accounts?.length === 0 && (
          <p className="text-sm text-muted-foreground">No platform accounts configured.</p>
        )}
      </CardContent>
    </Card>
  );
}

export default function SettingsPage() {
  const { data: brands, isLoading } = useBrands();

  return (
    <div className="flex flex-col gap-4">
      <h1 className="text-lg font-semibold">Settings</h1>
      {isLoading && <p className="text-sm text-muted-foreground">Loading...</p>}
      {brands?.map((brand) => (
        <BrandAccounts key={brand.id} brandId={brand.id} brandName={brand.name} />
      ))}
    </div>
  );
}

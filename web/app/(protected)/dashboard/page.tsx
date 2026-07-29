"use client";

import { useState } from "react";
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { BrandSelect } from "@/components/brand-select";
import { StalenessBadge } from "@/components/staleness-badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useBrands } from "@/lib/queries/brands";
import { useDailyMetrics } from "@/lib/queries/metrics";
import { usePlatformAccounts } from "@/lib/queries/platform-accounts";

function dateDaysAgo(days: number): string {
  const d = new Date();
  d.setDate(d.getDate() - days);
  return d.toISOString().slice(0, 10);
}

const TODAY = new Date().toISOString().slice(0, 10);
const THIRTY_DAYS_AGO = dateDaysAgo(30);

export default function DashboardPage() {
  const { data: brands, isLoading: brandsLoading } = useBrands();
  const [brandId, setBrandId] = useState<string | undefined>(undefined);
  const activeBrandId = brandId ?? brands?.[0]?.id;

  const { data: accounts, isLoading: accountsLoading } = usePlatformAccounts(activeBrandId);
  const { data: youtubeMetrics } = useDailyMetrics(activeBrandId, "youtube", THIRTY_DAYS_AGO, TODAY);

  if (brandsLoading) return <p className="text-sm text-muted-foreground">Loading...</p>;

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <h1 className="text-lg font-semibold">Dashboard</h1>
        {brands && (
          <BrandSelect brands={brands} value={activeBrandId} onChange={setBrandId} />
        )}
      </div>

      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        {accountsLoading && <p className="text-sm text-muted-foreground">Loading accounts...</p>}
        {accounts?.map((account) => (
          <Card key={account.id}>
            <CardHeader>
              <CardTitle className="flex items-center justify-between capitalize">
                {account.platform}
                <StalenessBadge lastIngestedAt={account.last_ingested_at} />
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">@{account.handle}</p>
              <p className="mt-1 text-xs text-muted-foreground/70">
                {account.ingestion_method === "automated_api" ? "Automated" : "Manual upload"}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>YouTube followers — last 30 days</CardTitle>
        </CardHeader>
        <CardContent className="h-72">
          {youtubeMetrics && youtubeMetrics.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={youtubeMetrics}>
                <CartesianGrid strokeDasharray="3 3" className="stroke-border" />
                <XAxis dataKey="day" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="followers_count"
                  stroke="hsl(var(--primary))"
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-sm text-muted-foreground">No data yet for this period.</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

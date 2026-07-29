"use client";

import { useAuth } from "@/lib/auth/use-auth";

/**
 * UI-level gating only — matches the chosen trade-off (see
 * sql/003_rls.sql's header comment): RLS is permissive, so this is the ONLY
 * thing stopping a viewer from reaching this section. Someone editing
 * requests directly (devtools/curl with the public anon key) can bypass
 * this — that's accepted, not a bug.
 */
export default function SettingsLayout({ children }: { children: React.ReactNode }) {
  const { profile } = useAuth();

  if (profile?.role !== "admin") {
    return (
      <div className="flex flex-col gap-2">
        <h1 className="text-lg font-semibold">403 — Admins only</h1>
        <p className="text-sm text-muted-foreground">This section is restricted to admins.</p>
      </div>
    );
  }

  return <>{children}</>;
}

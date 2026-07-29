"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";

import { AppShell } from "@/components/app-shell";
import { useAuth } from "@/lib/auth/use-auth";

/**
 * Client-side guard — there's no server-side session to check anymore (no
 * cookie, no Firebase Admin SDK). Firebase's own persisted session plus the
 * cached profile from use-auth.tsx is the only signal we have, which is why
 * this can only run as a client component. See sql/003_rls.sql's header
 * comment for the full reasoning behind this trade-off.
 */
export default function ProtectedLayout({ children }: { children: React.ReactNode }) {
  const { user, profile, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && (!user || !profile)) {
      router.replace("/login");
    }
  }, [loading, user, profile, router]);

  if (loading || !user || !profile) {
    return <div className="flex min-h-screen items-center justify-center text-sm text-muted-foreground">Loading…</div>;
  }

  return (
    <AppShell
      role={profile.role}
      user={{ email: user.email ?? "", displayName: profile.displayName, photoUrl: profile.photoUrl }}
    >
      {children}
    </AppShell>
  );
}

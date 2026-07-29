"use client";

import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";
import { useAuth } from "@/lib/auth/use-auth";

export function SignOutButton() {
  const { signOut } = useAuth();
  const router = useRouter();

  return (
    <Button
      variant="ghost"
      size="sm"
      onClick={async () => {
        await signOut();
        router.push("/login");
      }}
    >
      Sign out
    </Button>
  );
}

"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useState } from "react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuth } from "@/lib/auth/use-auth";

function LoginForm() {
  const { signInWithGoogle } = useAuth();
  const [pending, setPending] = useState(false);
  const router = useRouter();
  const searchParams = useSearchParams();

  async function handleSignIn() {
    setPending(true);
    try {
      await signInWithGoogle();
      router.push(searchParams.get("next") ?? "/dashboard");
    } catch (err) {
      console.error(err);
      toast.error(err instanceof Error ? err.message : "Sign-in failed. Please try again.");
    } finally {
      setPending(false);
    }
  }

  return (
    <Button className="w-full" onClick={handleSignIn} disabled={pending}>
      {pending ? "Signing in..." : "Sign in with Google"}
    </Button>
  );
}

export default function LoginPage() {
  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <Card className="w-full max-w-sm">
        <CardHeader className="items-center text-center">
          <CardTitle className="text-lg font-semibold text-foreground">
            Aspora Leadership Dashboard
          </CardTitle>
          <p className="text-sm text-muted-foreground">Sign in with your Aspora Google account</p>
        </CardHeader>
        <CardContent>
          {/* useSearchParams() requires a Suspense boundary during static
              prerendering — see https://nextjs.org/docs/messages/missing-suspense-with-csr-bailout */}
          <Suspense fallback={<Button className="w-full" disabled>Loading...</Button>}>
            <LoginForm />
          </Suspense>
        </CardContent>
      </Card>
    </div>
  );
}

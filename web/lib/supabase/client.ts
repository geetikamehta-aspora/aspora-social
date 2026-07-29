import { createClient } from "@supabase/supabase-js";

/**
 * Plain anon-key client — no Firebase token is attached. Supabase never
 * verifies Firebase identity (no Third-Party Auth registration); every
 * request here runs as the anon Postgres role. Authorization is entirely
 * app-layer (see lib/auth/use-auth.tsx's resolveProfile) and RLS is
 * permissive by design (see sql/003_rls.sql). Sending the Firebase ID token
 * as a bearer token here would make PostgREST try (and fail) to verify it
 * as a JWT — don't reintroduce that.
 */
export const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

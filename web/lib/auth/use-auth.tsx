"use client";

import {
  type User,
  onAuthStateChanged,
  signInWithPopup,
  signOut as firebaseSignOut,
} from "firebase/auth";
import { createContext, useContext, useEffect, useState } from "react";

import { auth, googleProvider } from "@/lib/firebase/client";
import { supabase } from "@/lib/supabase/client";

export type Profile = {
  role: "admin" | "viewer";
  displayName: string | null;
  photoUrl: string | null;
};

const CACHE_KEY = "aspora_profile_cache";

function cacheProfile(uid: string, profile: Profile) {
  localStorage.setItem(CACHE_KEY, JSON.stringify({ uid, profile }));
}

function readCachedProfile(uid: string): Profile | null {
  try {
    const raw = localStorage.getItem(CACHE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    return parsed.uid === uid ? parsed.profile : null;
  } catch {
    return null;
  }
}

function clearCachedProfile() {
  localStorage.removeItem(CACHE_KEY);
}

/**
 * The actual authorization gate — no RLS involved. Firebase Auth only ever
 * tells us "this is a real Google account with this email"; everything
 * about whether that email is allowed in, and what role it gets, lives
 * here. Returns null to mean "reject" (caller signs the Firebase session
 * back out).
 */
async function resolveProfile(fbUser: User): Promise<Profile | null> {
  const email = fbUser.email;
  if (!email) return null;

  const { data: existing } = await supabase
    .from("users")
    .select("role, display_name, photo_url")
    .eq("id", fbUser.uid)
    .maybeSingle();

  if (existing) {
    // Keep name/photo fresh from Google without ever touching role here —
    // role changes only ever happen via /settings/users.
    if (existing.display_name !== fbUser.displayName || existing.photo_url !== fbUser.photoURL) {
      await supabase
        .from("users")
        .update({ display_name: fbUser.displayName, photo_url: fbUser.photoURL })
        .eq("id", fbUser.uid);
    }
    return { role: existing.role, displayName: fbUser.displayName, photoUrl: fbUser.photoURL };
  }

  // First-ever login for this account. @aspora.com always gets in as a
  // viewer by default; anyone else needs a matching invited_users row
  // (added via /settings/users "Add user"). Either way, a pending
  // invitation's role/name wins over the default.
  const isAsporaDomain = email.endsWith("@aspora.com");
  const { data: invited } = await supabase
    .from("invited_users")
    .select("id, role, display_name")
    .eq("email", email)
    .maybeSingle();

  if (!isAsporaDomain && !invited) {
    return null; // not on the allowlist — reject
  }

  const role = invited?.role ?? "viewer";
  const displayName = fbUser.displayName ?? invited?.display_name ?? null;

  const { error: insertError } = await supabase.from("users").insert({
    id: fbUser.uid,
    email,
    display_name: displayName,
    photo_url: fbUser.photoURL,
    role,
  });
  if (insertError) throw insertError;

  if (invited) {
    await supabase.from("invited_users").delete().eq("id", invited.id);
  }

  return { role, displayName, photoUrl: fbUser.photoURL };
}

type AuthContextValue = {
  user: User | null;
  profile: Profile | null;
  loading: boolean;
  signInWithGoogle: () => Promise<void>;
  signOut: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [profile, setProfile] = useState<Profile | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Handles page reloads: Firebase restores its own persisted session,
    // this fires with that user, we hydrate instantly from cache then
    // re-validate against Supabase in the background — signing out if the
    // account's been removed since.
    return onAuthStateChanged(auth, async (fbUser) => {
      setUser(fbUser);

      if (!fbUser) {
        setProfile(null);
        clearCachedProfile();
        setLoading(false);
        return;
      }

      const cached = readCachedProfile(fbUser.uid);
      if (cached) setProfile(cached);
      setLoading(false);

      try {
        const resolved = await resolveProfile(fbUser);
        if (!resolved) {
          await firebaseSignOut(auth);
          setProfile(null);
          clearCachedProfile();
        } else {
          setProfile(resolved);
          cacheProfile(fbUser.uid, resolved);
        }
      } catch (err) {
        console.error("Failed to resolve profile", err);
      }
    });
  }, []);

  async function signInWithGoogle() {
    const credential = await signInWithPopup(auth, googleProvider);
    const resolved = await resolveProfile(credential.user);
    if (!resolved) {
      await firebaseSignOut(auth);
      throw new Error("This email isn't authorized. Ask an admin to add you in Settings > Users.");
    }
    setProfile(resolved);
    cacheProfile(credential.user.uid, resolved);
  }

  async function signOut() {
    await firebaseSignOut(auth);
    setProfile(null);
    clearCachedProfile();
  }

  return (
    <AuthContext.Provider value={{ user, profile, loading, signInWithGoogle, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
}

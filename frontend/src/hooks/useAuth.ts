import { useEffect, useState } from "react";
import type { Session, User } from "@supabase/supabase-js";
import { supabase } from "../lib/supabase";

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!supabase) {
      setLoading(false);
      return;
    }

    let mounted = true;

    supabase.auth
      .getSession()
      .then(({ data }) => {
        if (!mounted) return;
        setSession(data.session ?? null);
        setUser(data.session?.user ?? null);
        setLoading(false);
      })
      .catch(() => {
        // If auth backend is temporarily unreachable (e.g., TLS/cert/network issue),
        // gracefully fall back to guest mode and clear stale local auth cache.
        if (!mounted) return;
        try {
          const keys = Object.keys(window.localStorage);
          keys
            .filter((key) => key.startsWith("sb-") && key.endsWith("-auth-token"))
            .forEach((key) => window.localStorage.removeItem(key));
        } catch {
          // ignore storage errors
        }
        setSession(null);
        setUser(null);
        setLoading(false);
      });

    const { data } = supabase.auth.onAuthStateChange((_event, nextSession) => {
      setSession(nextSession ?? null);
      setUser(nextSession?.user ?? null);
      setLoading(false);
    });

    return () => {
      mounted = false;
      data.subscription.unsubscribe();
    };
  }, []);

  return {
    user,
    session,
    loading,
    isAuthenticated: Boolean(session?.access_token && user),
  };
}

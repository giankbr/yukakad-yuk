"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { AUTH_EVENT, clearSession, getRole, getToken, isTokenExpired } from "./api";

/** The stored token, or null when there is none or it has visibly expired (the stale one is dropped). */
function usableToken(): string | null {
  const stored = getToken();
  if (stored && isTokenExpired(stored)) {
    clearSession();
    return null;
  }
  return stored;
}

/** Picks up a replacement token (e.g. after a password change, or a re-login in another tab). */
function useTokenUpdates(ready: boolean, setToken: (token: string) => void) {
  useEffect(() => {
    if (!ready) return;
    const sync = () => {
      const next = getToken();
      if (next) setToken(next);
    };
    window.addEventListener(AUTH_EVENT, sync);
    window.addEventListener("storage", sync);
    return () => {
      window.removeEventListener(AUTH_EVENT, sync);
      window.removeEventListener("storage", sync);
    };
  }, [ready, setToken]);
}

function loginPath() {
  const here = `${window.location.pathname}${window.location.search}`;
  return `/auth/login?next=${encodeURIComponent(here)}`;
}

// Redirects to login if no token is present; otherwise returns the token
// once available. `ready` is false during the one-tick localStorage read so
// callers can show a loading state instead of flashing a redirect.
export function useAuthToken() {
  const [token, setToken] = useState<string | null>(null);
  const [ready, setReady] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const stored = usableToken();
    if (!stored) {
      router.push(loginPath());
      return;
    }
    // localStorage isn't available during SSR, so this can only run client-side.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setToken(stored);
    setReady(true);
  }, [router]);
  useTokenUpdates(ready, setToken);

  return { token, ready };
}

// Same as useAuthToken, but also requires the stored role to be "admin";
// non-admins are sent to their own dashboard instead of the login page,
// since they do have a valid session, just not one for this area.
export function useAdminAuth() {
  const [token, setToken] = useState<string | null>(null);
  const [ready, setReady] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const stored = usableToken();
    if (!stored) {
      router.push(loginPath());
      return;
    }
    if (getRole() !== "admin") {
      router.push("/dashboard");
      return;
    }
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setToken(stored);
    setReady(true);
  }, [router]);
  useTokenUpdates(ready, setToken);

  return { token, ready };
}

// Resolves a Next.js dynamic-segment params promise into a plain object,
// since client components can't `await` it directly.
export function useRouteParams<T extends Record<string, string>>(params: Promise<T>): T | null {
  const [value, setValue] = useState<T | null>(null);
  useEffect(() => {
    params.then(setValue);
  }, [params]);
  return value;
}

"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getRole, getToken } from "./api";

// Redirects to login if no token is present; otherwise returns the token
// once available. `ready` is false during the one-tick localStorage read so
// callers can show a loading state instead of flashing a redirect.
export function useAuthToken() {
  const [token, setToken] = useState<string | null>(null);
  const [ready, setReady] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const stored = getToken();
    if (!stored) {
      router.push("/auth/login");
      return;
    }
    // localStorage isn't available during SSR, so this can only run client-side.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setToken(stored);
    setReady(true);
  }, [router]);

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
    const stored = getToken();
    if (!stored) {
      router.push("/auth/login");
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

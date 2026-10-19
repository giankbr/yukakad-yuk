export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080";

// Storage keys keep the legacy "yukakad_" prefix so existing sessions stay signed in.
export const AUTH_KEYS = ["yukakad_token", "yukakad_role", "yukakad_name", "yukakad_email"] as const;
/** Fired on window (same tab) whenever the stored session or profile changes; other tabs get `storage`. */
export const AUTH_EVENT = "rawuh:auth";

function readStorage(key: string): string | null {
  if (typeof window === "undefined") return null;
  try {
    return window.localStorage.getItem(key);
  } catch {
    return null;
  }
}

function writeStorage(entries: Record<string, string>) {
  try {
    for (const [key, value] of Object.entries(entries)) window.localStorage.setItem(key, value);
  } catch {
    /* storage unavailable: the session just won't persist */
  }
}

function notifyAuthChange() {
  window.dispatchEvent(new Event(AUTH_EVENT));
}

export function getToken(): string | null {
  return readStorage("yukakad_token");
}

export function getRole(): string | null {
  return readStorage("yukakad_role");
}

export type SessionUser = { name?: string; email?: string; role?: string };

/** Stores the session from a login/register response (`{token, user}`). */
export function saveSession(token: string, user?: SessionUser | null) {
  if (typeof window === "undefined") return;
  writeStorage({
    yukakad_token: token,
    yukakad_role: user?.role ?? "user",
    yukakad_name: user?.name ?? "",
    yukakad_email: user?.email ?? "",
  });
  redirecting = false;
  notifyAuthChange();
}

/** Replaces only the token (e.g. the fresh one returned after a password change). */
export function saveToken(token: string) {
  if (typeof window === "undefined") return;
  writeStorage({ yukakad_token: token });
  notifyAuthChange();
}

/** Updates the cached display name/email shown in the dashboard shell. */
export function saveProfile(profile: { name?: string; email?: string }) {
  if (typeof window === "undefined") return;
  const entries: Record<string, string> = {};
  if (profile.name !== undefined) entries.yukakad_name = profile.name;
  if (profile.email !== undefined) entries.yukakad_email = profile.email;
  writeStorage(entries);
  notifyAuthChange();
}

/** Removes the session keys only (UI preferences such as the collapsed sidebar stay). */
export function clearSession() {
  if (typeof window === "undefined") return;
  try {
    for (const key of AUTH_KEYS) window.localStorage.removeItem(key);
  } catch {
    /* storage unavailable */
  }
  notifyAuthChange();
}

/**
 * True when the token is a signed `uid:email:role:exp.sig` token whose exp (unix seconds) has passed.
 * Opaque session tokens carry no client-readable expiry, so they are never treated as expired here.
 */
export function isTokenExpired(token: string, nowMs = Date.now()): boolean {
  const dot = token.lastIndexOf(".");
  if (dot <= 0) return false;
  const segments = token.slice(0, dot).split(":");
  if (segments.length !== 4 || !/^\d+$/.test(segments[3])) return false;
  return Number(segments[3]) * 1000 <= nowMs;
}

let redirecting = false;

/** Hard-navigates to the login page, remembering where the user was. Runs at most once per page load. */
export function redirectToLogin() {
  if (typeof window === "undefined" || redirecting) return;
  if (window.location.pathname.startsWith("/auth/")) return;
  redirecting = true;
  const here = `${window.location.pathname}${window.location.search}${window.location.hash}`;
  const target = new URL(`/auth/login?next=${encodeURIComponent(here)}`, window.location.origin);
  window.location.replace(target.toString());
}

export async function apiFetch(path: string, token: string, init: RequestInit = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      ...(init.body && !(init.body instanceof FormData) ? { "Content-Type": "application/json" } : {}),
      Authorization: `Bearer ${token}`,
      ...init.headers,
    },
  });
  // Expired or revoked session: drop it and log in again. /api/auth/* calls report their own 401s
  // (wrong current password, logout of an already-dead session).
  if (response.status === 401 && token && !path.startsWith("/api/auth/") && typeof window !== "undefined") {
    clearSession();
    redirectToLogin();
  }
  return response;
}

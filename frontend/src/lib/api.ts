export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080";

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem("yukakad_token");
}

export function getRole(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem("yukakad_role");
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
  return response;
}

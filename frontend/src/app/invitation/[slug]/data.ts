// Server-only data access for public invitations (/invitation/[slug]).
// Shared by the page and generateMetadata: React `cache()` dedupes within one request and the fetch
// cache (`revalidate: 30`) keeps published invitations from hammering the API when a link goes viral.
import { cache } from "react";
import { notFound } from "next/navigation";

const API_BASE = process.env.API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080";
const REVALIDATE_SECONDS = 30;

export type PublicInvitation = {
  slug?: string;
  title: string;
  template_id?: string;
  couple?: { bride_name?: string; groom_name?: string; bride_nickname?: string; groom_nickname?: string; bride_parents?: string; groom_parents?: string; bride_photo?: string; groom_photo?: string };
  event?: { title?: string; type?: string; venue?: string; date?: string; start_time?: string; end_time?: string; address?: string; maps_url?: string };
  events?: Array<{ title?: string; type?: string; date?: string; start_time?: string; end_time?: string; venue?: string; address?: string; maps_url?: string }>;
  sections?: string[];
  online_gift?: { active?: boolean; note?: string; min_amount?: number; max_amount?: number };
  wishlist_funds?: Record<string, number>;
};

export type PublicContent = {
  items?: Array<Record<string, string>>;
  theme?: string;
  music_url?: string;
  autoplay_music?: boolean;
  /** Extra sections from the dashboard (an object; older invitations still store the legacy `[]`). */
  sections_config?: unknown;
  opening_text?: string;
};

/** Thrown for 429/5xx/network failures so the route's error.tsx ("sedang ramai") renders instead of a 404. */
export class InvitationUnavailableError extends Error {
  constructor(public status: number | "network", detail?: string) {
    super(`Invitation API unavailable (${status})${detail ? `: ${detail}` : ""}`);
    this.name = "InvitationUnavailableError";
  }
}

function headers(previewToken?: string): Record<string, string> {
  const result: Record<string, string> = { Accept: "application/json" };
  if (previewToken) result["X-Preview-Token"] = previewToken;
  const internal = process.env.INTERNAL_API_SECRET;
  if (internal) result["X-Rawuh-Internal"] = internal;
  return result;
}

type FetchResult<T> = { ok: true; data: T } | { ok: false; status: number };

/**
 * GET a public endpoint. Published content is cached for 30 s (keyed by URL). Preview requests are
 * never cached so owners always see their latest edits and unpublished data never lands in the cache.
 */
async function getJSON<T>(path: string, previewToken?: string): Promise<FetchResult<T>> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE}${path}`, {
      headers: headers(previewToken),
      ...(previewToken ? { cache: "no-store" as const } : { next: { revalidate: REVALIDATE_SECONDS } }),
    });
  } catch (error) {
    throw new InvitationUnavailableError("network", error instanceof Error ? error.message : undefined);
  }
  if (response.status === 429 || response.status >= 500) throw new InvitationUnavailableError(response.status);
  if (!response.ok) return { ok: false, status: response.status };
  try {
    return { ok: true, data: (await response.json()) as T };
  } catch {
    throw new InvitationUnavailableError(response.status, "invalid JSON");
  }
}

const enc = encodeURIComponent;

/** The invitation itself. 404 (unknown/unpublished) → notFound(); transient failures throw. */
export const getInvitation = cache(async (slug: string, previewToken?: string): Promise<PublicInvitation> => {
  const result = await getJSON<PublicInvitation>(`/api/public/invitation/${enc(slug)}`, previewToken);
  if (!result.ok) notFound();
  return result.data;
});

/** A sub-resource (gallery, gifts, settings, stories). Missing (4xx) → empty; transient failures throw. */
export const getContent = cache(async (slug: string, resource: string, previewToken?: string): Promise<PublicContent> => {
  const result = await getJSON<PublicContent>(`/api/public/invitation/${enc(slug)}/${resource}`, previewToken);
  return result.ok ? result.data : {};
});

/** Personal link details (name + table) for `?guest=<token>`; null when the token is unknown or the lookup fails. */
export const getGuest = cache(async (slug: string, token: string, previewToken?: string): Promise<{ name?: string; table?: string } | null> => {
  try {
    // Per-guest lookups are not cached: they're one-off per token and the response is personal.
    const response = await fetch(`${API_BASE}/api/public/invitation/${enc(slug)}/guest?token=${enc(token)}`, { cache: "no-store", headers: headers(previewToken) });
    return response.ok ? await response.json() : null;
  } catch {
    return null;
  }
});

/** Preview token from `?preview=` (current) or the legacy `?preview_token=` link. Always sent as X-Preview-Token. */
export function previewTokenFrom(params: { preview?: string | string[]; preview_token?: string | string[] }) {
  const value = first(params.preview) || first(params.preview_token);
  return value?.trim() || undefined;
}

export function first(value: string | string[] | undefined) {
  return Array.isArray(value) ? value[0] : value;
}

/** Guest name from `?to=`: already URL-decoded by Next (`+`/`%20` → space); hyphens are kept as typed. */
export function guestNameFrom(value: string | string[] | undefined) {
  const name = first(value)?.replace(/\s+/g, " ").trim().slice(0, 80).trim();
  return name || undefined;
}

const DATE_RE = /^(\d{4})-(\d{2})-(\d{2})$/;
const TIME_RE = /^([01]\d|2[0-3]):[0-5]\d/;

function isCalendarDate(value: string) {
  const match = DATE_RE.exec(value);
  if (!match) return false;
  const [year, month, day] = [Number(match[1]), Number(match[2]), Number(match[3])];
  const date = new Date(Date.UTC(year, month - 1, day));
  return date.getUTCFullYear() === year && date.getUTCMonth() === month - 1 && date.getUTCDate() === day;
}

/**
 * "2026-12-12" + "11:00" → "2026-12-12T11:00:00+07:00" so countdowns and calendars use WIB.
 * Invalid dates → undefined (the page shows "Tanggal menyusul"); an invalid time falls back to 00:00.
 */
export function at(date?: string, start?: string): string | undefined {
  if (!date) return undefined;
  const value = date.trim();
  if (value.includes("T")) {
    // Already a full timestamp (older data): accept only a real calendar date with a parseable instant.
    return isCalendarDate(value.slice(0, 10)) && !Number.isNaN(new Date(value).getTime()) ? value : undefined;
  }
  if (!isCalendarDate(value)) return undefined;
  const time = start && TIME_RE.test(start) ? start.slice(0, 5) : "00:00";
  return `${value}T${time}:00+07:00`;
}

/** "11:00" + "14:00" → "11.00 – 14.00 WIB"; invalid times are dropped. */
export function timeRange(start?: string, end?: string) {
  if (!start || !TIME_RE.test(start)) return "";
  const fmt = (value: string) => value.slice(0, 5).replace(":", ".");
  return `${fmt(start)}${end && TIME_RE.test(end) ? ` – ${fmt(end)}` : ""} WIB`;
}

/** "Sabtu, 12 Desember 2026" in WIB, or undefined. */
export function longDateWIB(iso?: string) {
  if (!iso) return undefined;
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return undefined;
  return new Intl.DateTimeFormat("id-ID", { timeZone: "Asia/Jakarta", weekday: "long", day: "numeric", month: "long", year: "numeric" }).format(date);
}

/** Slug of the published invitation a verified custom domain points to; unknown → notFound(). */
export const getDomainSlug = cache(async (host: string): Promise<string> => {
  const result = await getJSON<{ slug?: string }>(`/api/public/domain/${enc(host)}`);
  if (!result.ok || !result.data.slug) notFound();
  return result.data.slug;
});

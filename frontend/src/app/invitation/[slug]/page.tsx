import type { GiftMethod, InvitationData, InvitationExtras } from "@/components/invitation/types";
import { FALLBACK_THEME, isTheme, loadTheme, themesWithOwnMusic } from "@/components/invitation/themes/registry";
import { InvitationProvider, MusicPlayer } from "@/components/invitation/themes/kit";
import { eventTypeLabel } from "@/lib/event-types";

const API_BASE = process.env.API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080";

type PublicInvitation = {
  slug?: string;
  title: string;
  template_id?: string;
  couple?: { bride_name?: string; groom_name?: string; bride_nickname?: string; groom_nickname?: string; bride_parents?: string; groom_parents?: string; bride_photo?: string; groom_photo?: string };
  event?: { title?: string; type?: string; venue?: string; date?: string; start_time?: string; end_time?: string; address?: string; maps_url?: string };
  events?: Array<{ title?: string; type?: string; date?: string; start_time?: string; end_time?: string; venue?: string; address?: string; maps_url?: string }>;
  sections?: string[];
};

type PublicContent = {
  items?: Array<Record<string, string>>;
  theme?: string;
  music_url?: string;
  autoplay_music?: boolean;
  /** Extra sections from the dashboard (an object; older invitations still store the legacy `[]`). */
  sections_config?: unknown;
  opening_text?: string;
};

function authHeaders(previewToken?: string): HeadersInit | undefined {
  return previewToken ? { Authorization: `Bearer ${previewToken}` } : undefined;
}

async function getInvitation(slug: string, previewToken?: string): Promise<PublicInvitation | null> {
  const response = await fetch(`${API_BASE}/api/public/invitation/${slug}`, { cache: "no-store", headers: authHeaders(previewToken) });
  if (!response.ok) return null;
  return response.json();
}

async function getContent(slug: string, resource: string, previewToken?: string): Promise<PublicContent> {
  const response = await fetch(`${API_BASE}/api/public/invitation/${slug}/${resource}`, { cache: "no-store", headers: authHeaders(previewToken) });
  if (!response.ok) return {};
  return response.json();
}

/** Personal link details (name + table) for `?guest=<token>`; null when the token is unknown. */
async function getGuest(slug: string, token: string, previewToken?: string): Promise<{ name?: string; table?: string } | null> {
  try {
    const response = await fetch(`${API_BASE}/api/public/invitation/${slug}/guest?token=${encodeURIComponent(token)}`, { cache: "no-store", headers: authHeaders(previewToken) });
    return response.ok ? response.json() : null;
  } catch {
    return null;
  }
}

export default async function PublicInvitationPage({
  params,
  searchParams,
}: {
  params: Promise<{ slug: string }>;
  searchParams: Promise<{ guest?: string; to?: string; preview_token?: string }>;
}) {
  const { slug } = await params;
  const { guest: guestToken, to: guestName, preview_token: previewToken } = await searchParams;

  const result = await getInvitation(slug, previewToken);
  if (!result) return <main className="invitation-not-found"><h1>Undangan ini belum bisa dibuka.</h1><p>Link mungkin belum dipublikasikan atau sudah tidak aktif.</p></main>;

  const [gallery, giftsResult, settings, stories, guest] = await Promise.all([
    getContent(slug, "gallery", previewToken),
    getContent(slug, "gifts", previewToken),
    getContent(slug, "settings", previewToken),
    getContent(slug, "stories", previewToken),
    guestToken ? getGuest(slug, guestToken, previewToken) : Promise.resolve(null),
  ]);
  const gifts = (giftsResult.items ?? []) as unknown as GiftMethod[];
  const firstStory = stories.items?.[0];

  // "2026-12-12" + "11:00" → "2026-12-12T11:00:00+07:00" so countdowns and calendars use WIB.
  const at = (date?: string, start?: string) => {
    if (!date) return undefined;
    if (date.includes("T")) return date;
    return `${date.slice(0, 10)}T${/^\d{2}:\d{2}/.test(start ?? "") ? start!.slice(0, 5) : "00:00"}:00+07:00`;
  };
  const time = (start?: string, end?: string) => (start ? `${start.slice(0, 5).replace(":", ".")}${end ? ` – ${end.slice(0, 5).replace(":", ".")}` : ""} WIB` : "");
  const mainDate = at(result.event?.date, result.event?.start_time) ?? "";
  const invitation: InvitationData = {
    couple: { bride: result.couple?.bride_name || "Mempelai Wanita", groom: result.couple?.groom_name || "Mempelai Pria", note: settings.opening_text?.trim() ?? "" },
    eventLabel: eventTypeLabel(result.event?.type),
    date: mainDate,
    place: result.event?.venue || "Lokasi menyusul",
    address: result.event?.address ?? "",
    mapsUrl: result.event?.maps_url,
    story: { title: firstStory?.title ?? "", body: firstStory?.content ?? "" },
    events: [{ name: result.event?.title || eventTypeLabel(result.event?.type), date: mainDate, time: time(result.event?.start_time, result.event?.end_time) || "Waktu menyusul", venue: result.event?.venue || "Lokasi menyusul", address: result.event?.address, mapsUrl: result.event?.maps_url }],
    gallery: gallery.items?.map((item) => item.image_url).filter(Boolean) ?? [],
    gifts,
    guestName: guestName ? guestName.replace(/-/g, " ") : guest?.name || undefined,
    guestTable: guest?.table || undefined,
  };

  // Every invitation renders with a Rawuh theme; missing/retired templates fall back to Linen Putih.
  const themeId = isTheme(result.template_id) ? result.template_id : FALLBACK_THEME;
  const { Theme } = await loadTheme(themeId);
  const couple = result.couple ?? {};
  const events = (result.events ?? []).filter(event => event.title || event.date).map(event => ({
    name: event.title ?? "Acara", date: at(event.date, event.start_time) ?? invitation.date, time: time(event.start_time, event.end_time) || "Waktu menyusul",
    venue: event.venue ?? invitation.place, address: event.address, mapsUrl: event.maps_url,
  }));
  const storyList = (stories.items ?? [])
    .map(item => ({ title: item.title ?? "", body: item.content ?? "", date: item.date, image: item.image_url }))
    .filter(item => item.title || item.body);
  const data: InvitationData = {
    ...invitation,
    couple: {
      ...invitation.couple,
      bride: couple.bride_nickname || invitation.couple.bride,
      groom: couple.groom_nickname || invitation.couple.groom,
      brideFull: couple.bride_name, groomFull: couple.groom_name,
      brideParents: couple.bride_parents, groomParents: couple.groom_parents,
      bridePhoto: couple.bride_photo, groomPhoto: couple.groom_photo,
    },
    events: events.length ? events : invitation.events,
    stories: storyList.length ? storyList : undefined,
    music: settings.music_url ? { url: settings.music_url, autoplay: Boolean(settings.autoplay_music) } : undefined,
    extras: settings.sections_config && typeof settings.sections_config === "object" && !Array.isArray(settings.sections_config)
      ? settings.sections_config as InvitationExtras : undefined,
  };
  return (
    <InvitationProvider data={data} slug={slug} guestToken={guestToken}>
      <Theme data={data} slug={slug} guestToken={guestToken} />
      {!themesWithOwnMusic.has(themeId) && <MusicPlayer music={data.music} />}
    </InvitationProvider>
  );
}

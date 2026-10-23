import type { Metadata } from "next";
import type { GiftMethod, InvitationData, InvitationExtras } from "@/components/invitation/types";
import { FALLBACK_THEME, isTheme, loadTheme } from "@/components/invitation/themes/registry";
import { InvitationProvider, MusicPlayer } from "@/components/invitation/themes/kit";
import { eventTypeLabel } from "@/lib/event-types";
import { at, first, getContent, getGuest, getInvitation, guestNameFrom, longDateWIB, previewTokenFrom, timeRange } from "./data";

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? "https://rawuh.id";
const DATE_PENDING = "Tanggal menyusul";

type SearchParams = { guest?: string | string[]; to?: string | string[]; preview?: string | string[]; preview_token?: string | string[]; amplop?: string | string[] };
type Props = { params: Promise<{ slug: string }>; searchParams: Promise<SearchParams> };

function absoluteUrl(value?: string) {
  if (!value) return undefined;
  try {
    return new URL(value, SITE_URL).toString();
  } catch {
    return undefined;
  }
}

export async function generateMetadata({ params, searchParams }: Props): Promise<Metadata> {
  const { slug } = await params;
  const previewToken = previewTokenFrom(await searchParams);
  // Same cached calls as the page (React cache + fetch cache): no extra API hits.
  const [result, gallery] = await Promise.all([getInvitation(slug, previewToken), getContent(slug, "gallery", previewToken)]);
  const couple = result.couple ?? {};
  const bride = couple.bride_nickname || couple.bride_name;
  const groom = couple.groom_nickname || couple.groom_name;
  const names = bride && groom ? `${bride} & ${groom}` : bride || groom || result.title || "Undangan";
  const title = `${names} — Undangan ${eventTypeLabel(result.event?.type)}`;
  const when = longDateWIB(at(result.event?.date, result.event?.start_time));
  const description = [when, result.event?.venue].filter(Boolean).join(" · ") || "Undangan digital dari Rawuh.";
  const image = absoluteUrl(gallery.items?.map(item => item.image_url).find(Boolean) || couple.bride_photo || couple.groom_photo);
  // No photo yet: fall back to the Rawuh card so WhatsApp still shows a large preview.
  const shareImage = image ?? "/rawuh/phone-kirana.webp";
  const images = [{ url: shareImage, alt: image ? names : "Undangan digital Rawuh" }];
  return {
    title,
    description,
    robots: { index: false, follow: false },
    alternates: { canonical: `/invitation/${encodeURIComponent(slug)}` },
    openGraph: { type: "website", title, description, url: `/invitation/${encodeURIComponent(slug)}`, siteName: "Rawuh", locale: "id_ID", images },
    twitter: { card: "summary_large_image", title, description, images: [shareImage] },
  };
}

export default async function PublicInvitationPage({ params, searchParams }: Props) {
  const { slug } = await params;
  const query = await searchParams;
  const previewToken = previewTokenFrom(query);
  const guestToken = first(query.guest)?.trim() || undefined;
  const guestName = guestNameFrom(query.to);
  const amplop = first(query.amplop);

  // Unknown/unpublished → notFound() (branded 404); API busy/down → throws → error.tsx.
  const result = await getInvitation(slug, previewToken);

  const [gallery, giftsResult, settings, stories, guest] = await Promise.all([
    getContent(slug, "gallery", previewToken),
    getContent(slug, "gifts", previewToken),
    getContent(slug, "settings", previewToken),
    getContent(slug, "stories", previewToken),
    guestToken ? getGuest(slug, guestToken, previewToken) : Promise.resolve(null),
  ]);
  const gifts = (giftsResult.items ?? []) as unknown as GiftMethod[];
  const firstStory = stories.items?.[0];

  const time = timeRange;
  // Invalid/missing dates render as "Tanggal menyusul" (kit's formatDate shows unparseable values as-is).
  const mainDate = at(result.event?.date, result.event?.start_time) ?? DATE_PENDING;
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
    guestName: guestName ?? (guest?.name || undefined),
    guestTable: guest?.table || undefined,
    onlineGift: result.online_gift?.active
      ? { note: result.online_gift.note, minAmount: result.online_gift.min_amount ?? 10000, maxAmount: result.online_gift.max_amount ?? 100000000 }
      : undefined,
    wishlistFunds: result.wishlist_funds ?? {},
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
    <InvitationProvider data={data} slug={slug} guestToken={guestToken} theme={themeId}>
      {/* Guests returning from the envelope payment skip the cover so they land on the thank-you note. */}
      <Theme data={data} slug={slug} guestToken={guestToken} skipCover={amplop === "selesai"} />
      {/* Hides itself when the theme renders its own music button. */}
      <MusicPlayer music={data.music} />
    </InvitationProvider>
  );
}

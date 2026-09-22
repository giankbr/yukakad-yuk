import { ClosingSection } from "@/components/invitation/ClosingSection";
import { CountdownSection } from "@/components/invitation/CountdownSection";
import { CoupleSection } from "@/components/invitation/CoupleSection";
import { CoverSection } from "@/components/invitation/CoverSection";
import { EventSection } from "@/components/invitation/EventSection";
import { GallerySection } from "@/components/invitation/GallerySection";
import { GiftSection } from "@/components/invitation/GiftSection";
import { LocationSection } from "@/components/invitation/LocationSection";
import { RSVPSection } from "@/components/invitation/RSVPSection";
import { StorySection } from "@/components/invitation/StorySection";
import { WishesSection } from "@/components/invitation/WishesSection";
import type { GiftMethod, InvitationData } from "@/components/invitation/types";

const API_BASE = process.env.API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080";

type PublicInvitation = {
  slug?: string;
  title: string;
  couple?: { bride_name?: string; groom_name?: string };
  event?: { title?: string; venue?: string; date?: string; maps_url?: string };
  sections?: string[];
};

type PublicContent = {
  items?: Array<Record<string, string>>;
  theme?: string;
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
  if (!result) return <main className="invitation-not-found"><h1>This invitation is taking a quiet moment.</h1><p>The link may be private or no longer available.</p></main>;

  const [gallery, giftsResult, settings, stories] = await Promise.all([
    getContent(slug, "gallery", previewToken),
    getContent(slug, "gifts", previewToken),
    getContent(slug, "settings", previewToken),
    getContent(slug, "stories", previewToken),
  ]);
  const gifts = (giftsResult.items ?? []) as unknown as GiftMethod[];
  const firstStory = stories.items?.[0];

  const invitation: InvitationData = {
    couple: { bride: result.couple?.bride_name ?? "Bride", groom: result.couple?.groom_name ?? "Groom", note: "A life made of ordinary days, shared carefully." },
    date: result.event?.date ?? "A day to remember",
    place: result.event?.venue ?? "Our chosen place",
    address: result.event?.title ?? "Details to follow",
    mapsUrl: result.event?.maps_url,
    story: { title: firstStory?.title ?? "The story continues here", body: firstStory?.content ?? "Thank you for being part of this chapter." },
    events: [{ name: result.event?.title ?? "Celebration", date: result.event?.date ?? "Soon", time: "Details to follow", venue: result.event?.venue ?? "Our chosen place" }],
    gallery: gallery.items?.map((item) => item.image_url).filter(Boolean) ?? [],
    gifts,
    guestName: guestName ? guestName.replace(/-/g, " ") : undefined,
  };

  const template = settings.theme === "adat" || settings.theme === "modern" || settings.theme === "motion" ? settings.theme : "editorial";
  return <main className={`invitation-page template-${template}`}>
    <CoverSection data={invitation} />
    <div className="invitation-body">
      <CountdownSection data={invitation} />
      <CoupleSection data={invitation} />
      <StorySection data={invitation} />
      <EventSection data={invitation} />
      <LocationSection data={invitation} />
      <GallerySection data={invitation} />
      <RSVPSection slug={slug} guestToken={guestToken} />
      <WishesSection slug={slug} guestToken={guestToken} />
      <GiftSection data={invitation} />
      <ClosingSection data={invitation} />
      <footer className="invitation-footer">With love, {invitation.couple.bride} &amp; {invitation.couple.groom}</footer>
    </div>
  </main>;
}

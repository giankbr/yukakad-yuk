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
import type { InvitationData } from "@/components/invitation/types";

const invitation: InvitationData = {
  couple: { bride: "Alya", groom: "Rizky", note: "We met in a room full of people and somehow left with a life full of small, shared rituals. This next chapter feels better with you in it." },
  date: "15 November 2026 · Yogyakarta",
  place: "Pendopo Ndalem Yudhaningratan",
  address: "Jl. Ibu Ruswo No. 35, Yogyakarta",
  mapsUrl: "https://maps.google.com/?q=Pendopo+Ndalem+Yudhaningratan",
  story: { title: "Mereka yang bertemu di waktu yang tepat", body: "Dari satu obrolan kecil, lalu menjadi banyak cerita. Kami belajar bahwa rumah bukan selalu sebuah tempat, kadang ia adalah seseorang yang membuat hari biasa terasa pulang." },
  events: [
    { name: "Akad nikah", date: "Sabtu, 15 November", time: "08.00 — 09.00", venue: "Pendopo utama" },
    { name: "Resepsi", date: "Sabtu, 15 November", time: "11.00 — 15.00", venue: "Pendopo utama" },
  ],
  gallery: [
    "https://images.unsplash.com/photo-1520854221256-17451cc331bf?auto=format&fit=crop&w=900&q=85",
    "https://images.unsplash.com/photo-1522673607200-164d1b6ce486?auto=format&fit=crop&w=900&q=85",
    "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=900&q=85",
  ],
  gifts: [
    { id: "demo-1", type: "bank", bank_name: "BCA", account_number: "1234567890", account_name: "Alya Prameswari" },
    { id: "demo-2", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "081234567890" },
  ],
};
const invitationSlug = "alya-rizky";

export default function InvitationDemoPage() {
  return <main className="invitation-page template-editorial">
    <CoverSection data={invitation} />
    <div className="invitation-body">
      <CountdownSection data={invitation} />
      <CoupleSection data={invitation} />
      <StorySection data={invitation} />
      <EventSection data={invitation} />
      <LocationSection data={invitation} />
      <GallerySection data={invitation} />
      <RSVPSection slug={invitationSlug} />
      <WishesSection slug={invitationSlug} />
      <GiftSection data={invitation} />
      <ClosingSection data={invitation} />
      <footer className="invitation-footer">With love, Alya &amp; Rizky · 2026</footer>
    </div>
  </main>;
}

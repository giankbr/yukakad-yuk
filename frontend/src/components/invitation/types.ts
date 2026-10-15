export type GiftMethod = {
  id: string;
  type: "bank" | "ewallet" | "qris" | "address";
  bank_name?: string;
  account_number?: string;
  account_name?: string;
  ewallet_provider?: string;
  ewallet_number?: string;
  qris_image_url?: string;
  address?: string;
};

export type InvitationData = {
  couple: {
    /** Short/nickname used in headlines, e.g. "Rina". */
    bride: string;
    groom: string;
    note: string;
    /** Full names with titles, e.g. "Rina Maharani, S.Ds." */
    brideFull?: string;
    groomFull?: string;
    /** e.g. "Putri dari Bpk. Ahmad & Ibu Siti" */
    brideParents?: string;
    groomParents?: string;
    bridePhoto?: string;
    groomPhoto?: string;
  };
  /** Event kind shown in headings, e.g. "Pernikahan". */
  eventLabel?: string;
  date: string;
  place: string;
  address: string;
  mapsUrl?: string;
  story: {
    title: string;
    body: string;
  };
  events: Array<{
    name: string;
    date: string;
    time: string;
    venue: string;
    address?: string;
    mapsUrl?: string;
  }>;
  /** Love story timeline (optional; themes fall back to `story`). */
  stories?: Array<{ title: string; body: string; date?: string; image?: string }>;
  gallery: string[];
  gifts: GiftMethod[];
  guestName?: string;
  /** Table/seat label of the guest who opened their personal link (e.g. "12", "VIP A"). */
  guestTable?: string;
  /** Background music uploaded from the dashboard (settings.music_url / autoplay_music). */
  music?: { url: string; autoplay?: boolean };
  /** Optional extra sections managed from the dashboard (stored in settings.sections_config). */
  extras?: InvitationExtras;
};

/** Every block is optional; a section renders only when its data is filled (and `enabled !== false`). */
export type InvitationExtras = {
  /** Opening verse/quote, e.g. QS Ar-Rum 21. */
  quote?: { enabled?: boolean; text: string; source?: string };
  /** Child profile for aqiqah / khitan / birthday invitations. */
  child?: { enabled?: boolean; name: string; nickname?: string; birthDate?: string; photo?: string; meaning?: string; parents?: string };
  /** "Simpan ke kalender" buttons under the events (on by default). */
  calendar?: { enabled?: boolean };
  livestream?: { enabled?: boolean; url: string; platform?: string; startsAt?: string; note?: string };
  dressCode?: { enabled?: boolean; note: string; colors?: string[] };
  /** Prewedding / teaser video (YouTube, Vimeo or a direct .mp4 link). */
  video?: { enabled?: boolean; url: string; title?: string };
  /** "Turut mengundang" family list. */
  family?: { enabled?: boolean; title?: string; names: string[] };
  /** Show the guest's personal check-in QR when the link carries ?guest=<token>. */
  guestPass?: { enabled?: boolean; note?: string };
  rundown?: { enabled?: boolean; items: Array<{ time: string; title: string; note?: string }> };
  travel?: { enabled?: boolean; note?: string; items: Array<{ name: string; detail?: string; url?: string }> };
  wishlist?: { enabled?: boolean; note?: string; items: WishlistItem[] };
  faq?: { enabled?: boolean; items: Array<{ q: string; a: string }> };
  /** Extra RSVP question about allergies / dietary needs. */
  rsvpDietary?: { enabled?: boolean; label?: string };
  /** After the event: "auto" switches once the last event date has passed. */
  thankYou?: { mode?: "auto" | "on" | "off"; message?: string };
};

export type WishlistItem = { id: string; name: string; url?: string; image?: string; price?: string; claimed_by?: string };

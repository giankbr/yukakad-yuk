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
  /** Background music uploaded from the dashboard (settings.music_url / autoplay_music). */
  music?: { url: string; autoplay?: boolean };
};

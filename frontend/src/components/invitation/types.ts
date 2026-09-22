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
    bride: string;
    groom: string;
    note: string;
  };
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
  }>;
  gallery: string[];
  gifts: GiftMethod[];
  guestName?: string;
};

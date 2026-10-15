// Editable copy for Tentang + legal pages: defaults, the shape admins save, and merge helpers.
// Pure data (no fetch) so both server pages and admin editors can import it.

import type { LegalDoc } from "./legal";

const filled = (value: unknown): value is string => typeof value === "string" && value.trim() !== "";
const text = (value: unknown, fallback: string) => (filled(value) ? value : fallback);
function list<T>(value: unknown, keep: (item: T) => boolean, fallback: T[]): T[] {
  const items = Array.isArray(value) ? (value as T[]).filter((item) => item && typeof item === "object" && keep(item)) : [];
  return items.length ? items : fallback;
}

// ---------------------------------------------------------------- Legal

export type TitledText = { title: string; text: string };
export type LegalContent = { updated?: string; intro?: string; summary?: TitledText[]; sections?: { title: string; body: string }[] };
export const legalSection = (slug: string) => (slug === "kebijakan-privasi" ? "privacy" : "terms");

/** Body blocks ↔ editable text: paragraphs are separated by a blank line, list items start with "- ". */
export function legalBodyToText(body: (string | string[])[]) {
  return body.map((block) => (Array.isArray(block) ? block.map((item) => `- ${item}`).join("\n") : block)).join("\n\n");
}

export function textToLegalBody(value: string): (string | string[])[] {
  return value
    .split(/\n\s*\n/)
    .map((block) => block.trim())
    .filter(Boolean)
    .map((block) => {
      const lines = block.split("\n").map((line) => line.trim()).filter(Boolean);
      return lines.every((line) => /^[-•*]\s+/.test(line)) ? lines.map((line) => line.replace(/^[-•*]\s+/, "")) : lines.join(" ");
    });
}

export function legalToContent(doc: LegalDoc): Required<LegalContent> {
  return {
    updated: doc.updated,
    intro: doc.intro,
    summary: doc.summary.map(([title, value]) => ({ title, text: value })),
    sections: doc.sections.map((section) => ({ title: section.title, body: legalBodyToText(section.body) })),
  };
}

const slugify = (value: string) => value.toLowerCase().normalize("NFKD").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 40) || "bagian";

export function mergeLegal(doc: LegalDoc, content: LegalContent): LegalDoc {
  const summary = list<TitledText>(content.summary, (item) => filled(item.title) && filled(item.text), []);
  const sections = list<{ title: string; body: string }>(content.sections, (item) => filled(item.title) && filled(item.body), []);
  const used = new Set<string>();
  return {
    ...doc,
    updated: text(content.updated, doc.updated),
    intro: text(content.intro, doc.intro),
    summary: summary.length ? summary.map((item) => [item.title, item.text] as [string, string]) : doc.summary,
    sections: sections.length
      ? sections.map((section) => {
          let id = slugify(section.title);
          while (used.has(id)) id += "-2";
          used.add(id);
          return { id, title: section.title.trim(), body: textToLegalBody(section.body) };
        })
      : doc.sections,
  };
}

// ---------------------------------------------------------------- Tentang

export type Stat = { value: string; label: string };
export type Milestone = { year: string; title: string; text: string };
export type TeamMember = { name: string; role: string; photo: string };
export type AboutContent = {
  title_lead: string;
  title_mono: string;
  lead: string;
  photo: string;
  stats: Stat[];
  story_title: string;
  story: string;
  quote: string;
  quote_by: string;
  principles: TitledText[];
  journey_title: string;
  milestones: Milestone[];
  team_title: string;
  open_roles: string;
  team: TeamMember[];
  address: string;
  email: string;
};

export const defaultAbout: AboutContent = {
  title_lead: "Rawuh artinya",
  title_mono: "“datang.”",
  lead: "Dalam bahasa Jawa, rawuh adalah cara paling sopan untuk menyebut kedatangan seseorang. Kami membangun Rawuh agar setiap tamu merasa diundang secara pribadi — bukan sekadar menerima link.",
  photo: "/rawuh/about-team.webp",
  stats: [
    { value: "2021", label: "berdiri di Yogyakarta" },
    { value: "120rb+", label: "acara dirayakan" },
    { value: "2,4 jt", label: "tamu diundang" },
    { value: "34", label: "provinsi terjangkau" },
  ],
  story_title: "Berawal dari undangan nikah kakak kami sendiri.",
  story: "Tahun 2021, pernikahan dibatasi 50 tamu. Kakak kami ingin keluarga di Medan, Makassar, dan Belanda tetap merasa hadir. Undangan digital yang ada saat itu terasa dingin — satu link yang sama untuk semua orang.\n\nJadi kami membuatnya sendiri: undangan dengan nama setiap tamu, peta yang benar-benar bisa dipakai, dan buku ucapan yang dibaca ulang bertahun-tahun kemudian. Teman-teman mulai minta dibuatkan. Lalu teman dari teman.",
  quote: "Teknologi boleh modern, tapi rasa diundangnya harus tetap seperti diantar langsung ke rumah.",
  quote_by: "Galih Prakoso, pendiri",
  principles: [
    { title: "Personal, bukan massal", text: "Setiap tamu pantas disapa dengan namanya." },
    { title: "Ramah untuk orang tua", text: "Kalau ibu kami bisa pakai, semua orang bisa." },
    { title: "Harga jujur", text: "Sekali bayar. Tanpa langganan, tanpa jebakan." },
    { title: "Lokal sepenuhnya", text: "Desainer, server, dan CS ada di Indonesia." },
  ],
  journey_title: "Dari satu undangan ke 120 ribu.",
  milestones: [
    { year: "2021", title: "Undangan pertama", text: "Dibuat untuk pernikahan kakak, 50 tamu." },
    { year: "2022", title: "Rawuh.id lahir", text: "10 tema pertama & fitur RSVP." },
    { year: "2023", title: "Amplop digital", text: "QRIS & e-wallet, 10rb acara." },
    { year: "2024", title: "QR Check-in", text: "Buku tamu tanpa antre di venue." },
    { year: "2026", title: "Video 3D", text: "120rb+ acara di 34 provinsi." },
  ],
  team_title: "24 orang, satu kantor di Jogja.",
  open_roles: "3 posisi terbuka — hubungi kami",
  team: [
    { name: "Galih Prakoso", role: "Pendiri & CEO", photo: "/rawuh/team-galih.webp" },
    { name: "Sekar Ayuningtyas", role: "Kepala Desain", photo: "/rawuh/team-sekar.webp" },
    { name: "Bagus Wicaksono", role: "Kepala Teknologi", photo: "/rawuh/team-bagus.webp" },
    { name: "Nadia Putri", role: "Customer Happiness", photo: "/rawuh/team-nadia.webp" },
  ],
  address: "Jl. Prawirotaman No. 12, Yogyakarta",
  email: "halo@rawuh.id",
};

/** Overlay saved edits on the defaults; empty strings and empty lists keep the default. `open_roles` may be cleared on purpose. */
export function mergeAbout(content: Partial<AboutContent>): AboutContent {
  const d = defaultAbout;
  return {
    title_lead: text(content.title_lead, d.title_lead),
    title_mono: text(content.title_mono, d.title_mono),
    lead: text(content.lead, d.lead),
    photo: text(content.photo, d.photo),
    stats: list<Stat>(content.stats, (s) => filled(s.value) && filled(s.label), d.stats),
    story_title: text(content.story_title, d.story_title),
    story: text(content.story, d.story),
    quote: typeof content.quote === "string" ? content.quote : d.quote,
    quote_by: typeof content.quote_by === "string" ? content.quote_by : d.quote_by,
    principles: list<TitledText>(content.principles, (p) => filled(p.title) && filled(p.text), d.principles),
    journey_title: text(content.journey_title, d.journey_title),
    milestones: list<Milestone>(content.milestones, (m) => filled(m.year) && filled(m.title), d.milestones),
    team_title: text(content.team_title, d.team_title),
    open_roles: typeof content.open_roles === "string" ? content.open_roles : d.open_roles,
    team: list<TeamMember>(content.team, (t) => filled(t.name), d.team),
    address: text(content.address, d.address),
    email: text(content.email, d.email),
  };
}

export const isRemoteImage = (src: string) => /^https?:\/\//.test(src);

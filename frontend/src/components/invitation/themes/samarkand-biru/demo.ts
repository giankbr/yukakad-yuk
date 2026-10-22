import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadhifa", groom: "Rayyan",
    brideFull: "Nadhifa Khairunnisa, S.Ars.", groomFull: "Rayyan Al-Farisi, M.T.",
    brideParents: "Putri pertama dari\nBapak Ir. H. Taufik Hidayat & Ibu Hj. Rina Marlina", groomParents: "Putra ketiga dari\nBapak Dr. H. Ahmad Faisal & Ibu Hj. Siti Mariam",
    bridePhoto: "/themes/img/a99.webp", groomPhoto: "/themes/img/r26.webp",
    note: "Seperti ubin yang disusun satu demi satu menjadi pola yang utuh, semoga Allah merangkai hidup kami dalam sakinah, mawaddah, wa rahmah.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-05-22T09:00:00+07:00",
  place: "Graha Sanusi Hardjadinata",
  address: "Jl. Dipati Ukur No. 35, Lebakgede, Coblong, Kota Bandung",
  stories: [
    { date: "2018", title: "Studio Arsitektur", body: "Kami satu studio di kampus. Nadhifa menggambar denah paling rapi, Rayyan selalu meminjam penggarisnya." },
    { date: "2025", title: "Biru Samarkand", body: "Dalam perjalanan studi arsitektur Islam ke Asia Tengah, di bawah kubah toska yang berusia ratusan tahun, Rayyan menyampaikan niat baiknya." },
    { date: "2026", title: "Lamaran", body: "Kedua keluarga bertemu di Bandung dan bersepakat dengan doa dan restu." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-22T09:00:00+07:00", time: "09.00 – 10.00 WIB", venue: "Masjid Pusdai Jawa Barat", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Cibeunying Kaler, Kota Bandung" },
    { name: "Resepsi", date: "2027-05-22T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Graha Sanusi Hardjadinata", address: "Jl. Dipati Ukur No. 35, Lebakgede, Coblong, Kota Bandung" },
  ],
  gallery: ["/themes/img/a43.webp", "/themes/img/r12.webp", "/themes/img/r10.webp", "/themes/img/a31.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7301 2233 44", account_name: "Nadhifa Khairunnisa" },
    { id: "demo-muamalat", type: "bank", bank_name: "Bank Muamalat", account_number: "1440 0567 89", account_name: "Rayyan Al-Farisi" },
  ],
  guestName: "Bapak Dr. Hendra Gunawan & Keluarga",
  guestTable: "Meja Firuza 4",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat (kebesaran Allah).", source: "QS. Az-Zariyat: 49" },
    rundown: { items: [
      { time: "11.00", title: "Kirab pengantin", note: "Diiringi nasyid" },
      { time: "11.30", title: "Doa & tausiyah singkat" },
      { time: "12.00", title: "Ramah tamah", note: "Jamuan & foto bersama" },
    ] },
    dressCode: { note: "Busana muslim dalam nuansa biru toska, biru lapis, dan putih gading.", colors: ["#182a6a", "#2b9fa3", "#1f4a9e", "#eee8d8"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Ir. H. Taufik Hidayat", "Kel. Besar Dr. H. Ahmad Faisal"] },
  },
});

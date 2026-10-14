import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Laksmi", groom: "Bayu",
    brideFull: "Laksmi Puspitasari, S.Psi.", groomFull: "Bayu Aji Nugroho, S.H.",
    brideParents: "Putri pertama dari\nBapak R. Soetomo & Ibu Sri Rahayu", groomParents: "Putra kedua dari\nBapak Haryanto & Ibu Endang Lestari",
    bridePhoto: "/themes/img/a47.webp", groomPhoto: "/themes/img/a48.webp",
  },
  eventLabel: "Pernikahan",
  date: "2026-07-05T08:00:00+07:00",
  place: "Pendhapa Ndalem Joyokusuman",
  address: "Jl. Gajahan No. 7, Pasar Kliwon, Surakarta",
  stories: [
    { date: "2018", title: "Bertemu", body: "Bertemu di pentas wayang orang Sriwedari. Laksmi penarinya, Bayu penonton yang tak bisa berkedip." },
    { date: "2020", title: "Berpacaran", body: "Setelah dua tahun berteman, keduanya sepakat melangkah bersama." },
    { date: "2025", title: "Lamaran", body: "Keluarga Bayu berkunjung ke rumah Laksmi membawa seserahan tradisional." },
  ],
  events: [
    { name: "Ijab Qobul", date: "2026-07-05T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Keraton Surakarta", address: "Jl. Masjid Besar, Kauman, Surakarta" },
    { name: "Upacara Panggih", date: "2026-07-05T10:00:00+07:00", time: "10.00 – 11.00 WIB", venue: "Pendhapa Ndalem Joyokusuman", address: "Jl. Gajahan No. 7, Pasar Kliwon, Surakarta" },
    { name: "Resepsi", date: "2026-07-05T19:00:00+07:00", time: "19.00 – 21.30 WIB", venue: "Pendhapa Ndalem Joyokusuman", address: "Jl. Gajahan No. 7, Pasar Kliwon, Surakarta" },
  ],
  gallery: ["/themes/img/a46.webp", "/themes/img/a49.webp", "/themes/img/a50.webp", "/themes/img/a47.webp", "/themes/img/a48.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0123 0100 4567 501", account_name: "Laksmi Puspitasari" },
    { id: "demo-kado", type: "address", address: "Jl. Slamet Riyadi No. 275, Sriwedari, Laweyan, Surakarta" },
  ],
  guestName: "Bapak Hendro Wibowo & Keluarga",
});

import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Vina", groom: "Aldo",
    brideFull: "Vina Larasati", groomFull: "Aldo Saputra",
    brideParents: "Putri Bapak Larto & Ibu Sumi", groomParents: "Putra Bapak Saputra & Ibu Endah",
    bridePhoto: "/themes/img/a107.webp", groomPhoto: "/themes/img/a106.webp",
  },
  eventLabel: "Pernikahan",
  date: "2026-08-08T08:00:00+07:00",
  place: "Jogja Expo Center",
  address: "Banguntapan, Yogyakarta",
  stories: [
    { title: "Warrior", date: "2019", body: "Bertemu di warnet: rebutan satu PC, akhirnya main berdua." },
    { title: "Epic", date: "2022", body: "Resmi jadi duo tetap. Sinyal boleh hilang, komitmen tidak." },
    { title: "Mythic", date: "2025", body: "Lamaran setelah menang match: cincin di dalam kotak diamond." },
  ],
  events: [
    { name: "Akad Nikah", date: "2026-08-08T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Masjid Gedhe Kauman, Yogyakarta" },
    { name: "Resepsi", date: "2026-08-08T19:00:00+07:00", time: "19.00 – 21.30 WIB", venue: "Jogja Expo Center, Banguntapan" },
  ],
  gallery: ["/themes/img/a108.webp", "/themes/img/a109.webp", "/themes/img/a110.webp"],
  gifts: [{ id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0808 2026 99", account_name: "Vina Larasati" }],
  guestName: "Bapak Eko Prasetyo & Keluarga",
});

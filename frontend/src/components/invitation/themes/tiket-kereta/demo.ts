import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Wulan", groom: "Seno",
    brideFull: "Wulan Pertiwi", groomFull: "Seno Aji",
    brideParents: "Putri Bapak Tiwi & Ibu Nani", groomParents: "Putra Bapak Aji & Ibu Warsini",
    bridePhoto: "/themes/img/r40.webp", groomPhoto: "/themes/img/r41.webp",
  },
  eventLabel: "Pernikahan",
  date: "2027-11-07T08:00:00+07:00",
  place: "Loko Coffee Hall",
  address: "eks Stasiun Tugu, Yogyakarta",
  stories: [
    { title: "St. Lajang", date: "2019", body: "Bertemu di gerbong 3, rebutan kursi 1A" },
    { title: "St. Jadian", date: "2021", body: "Resmi, PP Jogja–Solo tiap minggu" },
    { title: "St. Lamaran", date: "2026", body: "Seno berlutut di peron 1, disaksikan penumpang" },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-11-07T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Masjid Gedhe Kauman", address: "Yogyakarta" },
    { name: "Resepsi", date: "2027-11-07T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Loko Coffee Hall", address: "eks Stasiun Tugu" },
  ],
  gallery: ["/themes/img/r42.webp", "/themes/img/r43.webp", "/themes/img/r44.webp"],
  gifts: [{ id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0711 2027 88", account_name: "Wulan Pertiwi" }],
  guestName: "Ibu Endah Prasetyo & Keluarga",
});

import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Ratri", groom: "Danang",
    brideFull: "Ratri Anjani", groomFull: "Danang Saputro",
    brideParents: "Putri Bapak Anjar & Ibu Sulis", groomParents: "Putra Bapak Sapto & Ibu Darmi",
    bridePhoto: "/themes/img/r96.webp", groomPhoto: "/themes/img/r95.webp",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-24T08:00:00+07:00",
  place: "Graha Saba Buana",
  address: "Jl. Letjen Suprapto, Solo",
  stories: [
    { title: "St. Perkenalan", date: "2020", body: "Satu KA Jogja–Solo, Ratri pinjam charger." },
    { title: "St. Komitmen", date: "2023", body: "Resmi berpacaran di peron 3, hujan rintik." },
    { title: "St. Lamaran", date: "2026", body: "Danang berlutut persis saat kereta tiba." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-07-24T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Graha Saba Buana", address: "Jl. Letjen Suprapto, Solo" },
    { name: "Resepsi", date: "2027-07-24T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Graha Saba Buana", address: "Jl. Letjen Suprapto, Solo" },
  ],
  gallery: ["/themes/img/r98.webp", "/themes/img/r97.webp", "/themes/img/r99.webp"],
  gifts: [{ id: "demo-bank", type: "bank", bank_name: "BRI", account_number: "2407 2027 11", account_name: "Ratri Anjani" }],
  guestName: "Bapak Slamet Riyadi & Keluarga",
});

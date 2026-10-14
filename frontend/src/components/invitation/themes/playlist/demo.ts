import { makeDemo } from "../demo-base";

const day = "2027-07-24";
const venue = "Balai Kota Lama, Semarang";
const address = "Jl. Letjen Suprapto No. 31, Kota Lama, Semarang";

export const demo = makeDemo({
  couple: {
    bride: "Kania", groom: "Dimas",
    note: "Dua pendengar, satu frekuensi. Diputar tanpa henti sejak 2019.",
    brideFull: "Kania Rahma", groomFull: "Dimas Anggara",
    brideParents: "Putri Bapak Rahmat & Ibu Ida", groomParents: "Putra Bapak Tono & Ibu Yuli",
    bridePhoto: "/themes/img/a135.webp", groomPhoto: "/themes/img/a136.webp",
  },
  eventLabel: "Pernikahan",
  date: `${day}T08:00:00+07:00`,
  place: venue,
  address,
  stories: [
    { title: "Debut", date: "2019", body: "", image: "/themes/img/a137.webp" },
    { title: "Senja EP", date: "2022", body: "", image: "/themes/img/a139.webp" },
    { title: "Lamaran", date: "2026", body: "", image: "/themes/img/a138.webp" },
  ],
  events: [
    { name: "Akad Nikah", date: `${day}T08:00:00+07:00`, time: "08.00 – 09.30 WIB", venue, address },
    { name: "Pemberkatan Keluarga", date: `${day}T09:30:00+07:00`, time: "09.30 – 10.00 WIB", venue, address },
    { name: "Resepsi & Live Band", date: `${day}T18:30:00+07:00`, time: "18.30 – 21.30 WIB", venue, address },
  ],
  gallery: ["/themes/img/a134.webp", "/themes/img/a140.webp"],
  gifts: [{ id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "2407 2027 55", account_name: "Kania Rahma" }],
  guestName: "Bapak Agus Salim & Keluarga",
});

import { makeDemo } from "../demo-base";

const day = "2027-05-02";
const venue = "Graha Harmoni, Surabaya";
const address = "Jl. Mayjen Sungkono No. 25, Surabaya";

export const demo = makeDemo({
  couple: {
    bride: "Nada", groom: "Raga",
    note: "Dua suara, satu lagu untuk selamanya.",
    brideFull: "Nada Safira", groomFull: "Raga Aditama",
    brideParents: "Putri Bapak Pramudya & Ibu Astuti", groomParents: "Putra Bapak Wibowo & Ibu Sulastri",
    bridePhoto: "/themes/img/a127.webp", groomPhoto: "/themes/img/a126.webp",
  },
  eventLabel: "Pernikahan",
  date: `${day}T08:00:00+07:00`,
  place: venue,
  address,
  stories: [
    { title: "Debut", date: "2018", body: "Pertama bertemu di panggung akustik kampus.", image: "/themes/img/a129.webp" },
    { title: "Duet Pertama", date: "2021", body: "Resmi jadian setelah duet di acara sahabat.", image: "/themes/img/a130.webp" },
    { title: "Single: Lamaran", date: "2026", body: "Raga melamar di tengah konser kecil keluarga.", image: "/themes/img/a128.webp" },
  ],
  events: [
    { name: "Penjemputan Pengantin", date: `${day}T06:30:00+07:00`, time: "06.30 WIB", venue, address },
    { name: "Akad Nikah (Live)", date: `${day}T08:00:00+07:00`, time: "08.00 – 09.00 WIB", venue, address },
    { name: "Sungkeman (Akustik)", date: `${day}T09:30:00+07:00`, time: "09.30 WIB", venue, address },
    { name: "Resepsi — Orkestra Penuh", date: `${day}T11:00:00+07:00`, time: "11.00 – 13.00 WIB", venue, address },
    { name: "Lempar Bunga (Bonus Track)", date: `${day}T13:30:00+07:00`, time: "13.30 WIB", venue, address },
  ],
  gallery: ["/themes/img/a125.webp", "/themes/img/a131.webp", "/themes/img/a132.webp", "/themes/img/a133.webp"],
  gifts: [{ id: "demo-bni", type: "bank", bank_name: "BNI", account_number: "0205 2027 44", account_name: "Nada Safira" }],
  guestName: "Ibu Hesti Pramono & Keluarga",
});

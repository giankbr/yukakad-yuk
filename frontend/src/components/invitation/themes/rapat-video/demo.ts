import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Rani", groom: "Yudha",
    brideFull: "Rani Puspita, S.I.Kom.", groomFull: "Yudha Mahardika, S.T.",
    brideParents: "Putri Bapak Bagyo & Ibu Endang", groomParents: "Putra Bapak Mahar & Ibu Tuti",
    bridePhoto: "/themes/img/r68.webp", groomPhoto: "/themes/img/r71.webp",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-12T08:00:00+07:00",
  place: "Balai Rakyat Depok",
  address: "Jl. Margonda, Depok",
  stories: [
    { date: "2020", title: "Meeting pertama", body: "Rapat divisi gabungan. Kamera Rani mati, suaranya yang bikin penasaran." },
    { date: "2021", title: "Breakout room berdua", body: "Dipasangkan di breakout room. Lupa balik ke main room." },
    { date: "2026", title: "Share screen cincin", body: "Yudha share screen: slide terakhir berisi lamaran." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-12T08:00:00+07:00", time: "08.00", venue: "Masjid Baiturrahman", address: "Depok" },
    { name: "Resepsi", date: "2027-09-12T11:00:00+07:00", time: "11.00", venue: "Balai Rakyat Depok", address: "Jl. Margonda" },
  ],
  gallery: ["/themes/img/r31.webp", "/themes/img/r32.webp", "/themes/img/r30.webp"],
  gifts: [{ id: "demo-bni", type: "bank", bank_name: "BNI", account_number: "1209 2027 44", account_name: "Rani Puspita" }],
  guestName: "Ibu Marlina Dewi & Keluarga",
});

import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Sinta", groom: "Haris",
    brideFull: "Sinta Permatasari, S.Ak.", groomFull: "Haris Gunadi, S.Kom.",
    brideParents: "Putri Bapak Permadi & Ibu Asih", groomParents: "Putra Bapak Gun & Ibu Marni",
    bridePhoto: "/themes/img/r72.webp", groomPhoto: "/themes/img/r75.webp",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-18T08:00:00+07:00",
  place: "Balai Kartini Tangerang",
  address: "Jl. Sudirman No. 9",
  stories: [
    { date: "2019", title: "Perkenalan", body: "CC: teman kantor. Haris salah kirim email, malah kenalan." },
    { date: "2022", title: "Resmi", body: "Subject: WFH bareng selamanya? — Sinta: Approve." },
    { date: "2026", title: "Lamaran", body: "High priority! Haris melamar saat farewell kantor lama." },
  ],
  events: [
    { name: "Akad & Resepsi", date: "2027-07-18T08:00:00+07:00", time: "08.00 – 14.00 WIB", venue: "Balai Kartini Tangerang", address: "Jl. Sudirman No. 9" },
  ],
  gallery: ["/themes/img/r72.webp", "/themes/img/r75.webp", "/themes/img/r73.webp"],
  gifts: [{ id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1807 2027 31", account_name: "Sinta Permatasari" }],
  guestName: "Bapak Taufik Rahman & Keluarga",
});

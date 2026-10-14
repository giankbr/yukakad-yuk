import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Bella", groom: "Arga",
    brideFull: "Bella Pramesti", groomFull: "Arga Wijaya",
    brideParents: "Putri Bapak Pram & Ibu Made", groomParents: "Putra Bapak Wija & Ibu Komang",
    bridePhoto: "/themes/img/r107.webp", groomPhoto: "/themes/img/r106.webp",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-11T08:00:00+08:00",
  place: "AYANA Cliff Garden, Jimbaran",
  address: "Jimbaran, Bali",
  stories: [
    { title: "", date: "2019", body: "Open trip Nusa Penida — kenalan di speedboat, sama-sama mabuk laut." },
    { title: "", date: "2022", body: "Backpacking Jawa–Bali 14 hari. Pulang-pulang resmi pacaran." },
    { title: "", date: "2026", body: "Lamaran di Pinggan sunrise point, kabutnya tahu momen." },
  ],
  events: [
    { name: "Kumpul tamu", date: "2027-09-11T07:30:00+08:00", time: "07.30", venue: "Lobi AYANA · dresscode: earth tone" },
    { name: "Akad Nikah", date: "2027-09-11T08:00:00+08:00", time: "08.00", venue: "Cliff Chapel · momen sakral" },
    { name: "Sesi foto keluarga", date: "2027-09-11T10:00:00+08:00", time: "10.00", venue: "Taman tebing · senyum terbaikmu" },
    { name: "Resepsi sunset", date: "2027-09-11T17:00:00+08:00", time: "17.00", venue: "Cliff Garden · dinner & live music" },
  ],
  gallery: ["/themes/img/r105.webp", "/themes/img/r108.webp", "/themes/img/r110.webp", "/themes/img/r109.webp"],
  gifts: [{ id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "1109 2027 33", account_name: "Bella Pramesti" }],
  guestName: "Bapak Gede Mahendra & Keluarga",
});

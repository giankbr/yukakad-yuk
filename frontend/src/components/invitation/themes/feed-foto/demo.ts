import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Alika", groom: "Rio",
    brideFull: "Alika Dewi", groomFull: "Rio Saputra",
    brideParents: "Putri Bpk. Dewa & Ibu Mirah", groomParents: "Putra Bpk. Seno & Ibu Tatik",
  },
  eventLabel: "Menikah",
  date: "2027-03-07T08:00:00+08:00",
  place: "Villa Karang Putih",
  address: "Uluwatu, Bali",
  stories: [
    { title: "Kenalan", date: "2021", body: "Kenalan lewat mutual, saling like story dulu seminggu." },
    { title: "Hard launch", date: "2023", body: "Hard launch! Post foto berdua pertama, 1.200 likes." },
    { title: "Lamaran", date: "2026", body: "Rio lamaran di Uluwatu. Caption: finally, forever." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-03-07T08:00:00+08:00", time: "08.00 – 10.00 WITA", venue: "Villa Karang Putih", address: "Uluwatu" },
    { name: "Resepsi", date: "2027-03-07T16:00:00+08:00", time: "16.00 – 20.00 WITA", venue: "Sunset Lawn", address: "Uluwatu" },
  ],
  gallery: [
    "/themes/img/r10.webp", "/themes/img/r11.webp", "/themes/img/r9.webp",
    "/themes/img/r15.webp", "/themes/img/r13.webp", "/themes/img/r14.webp", "/themes/img/r16.webp", "/themes/img/r12.webp", "/themes/img/r17.webp",
  ],
  gifts: [{ id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0703 2027 22", account_name: "Alika Dewi" }],
  guestName: "Bapak Dharma Putra & Keluarga",
});

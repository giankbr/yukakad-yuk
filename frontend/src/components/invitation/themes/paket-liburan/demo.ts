import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Monica", groom: "Fikri",
    brideFull: "Monica Putri", groomFull: "Fikri Ramadhan",
    brideParents: "Putri Bapak Pur & Ibu Yayah", groomParents: "Putra Bapak Rama & Ibu Nenden",
    bridePhoto: "/themes/img/r100.webp", groomPhoto: "/themes/img/r101.webp",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-14T08:00:00+07:00",
  place: "The Tribrata",
  address: "Dharmawangsa, Jakarta",
  stories: [
    { title: "", date: "2019", body: "Berangkat — kenalan di open trip Bromo, satu jeep." },
    { title: "", date: "2021", body: "Check-in hubungan serius, sarapan janji manis." },
    { title: "", date: "2026", body: "Puncak tertinggi: lamaran di Bukit Teletubbies." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-14T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "The Tribrata", address: "Dharmawangsa, Jakarta" },
    { name: "Resepsi", date: "2027-08-14T11:30:00+07:00", time: "11.30 – 14.00 WIB", venue: "The Tribrata", address: "Dharmawangsa, Jakarta" },
  ],
  gallery: ["/themes/img/r102.webp", "/themes/img/r103.webp", "/themes/img/r104.webp"],
  gifts: [{ id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "1408 2027 22", account_name: "Monica Putri" }],
  guestName: "Ibu Yanti Kusuma & Keluarga",
});

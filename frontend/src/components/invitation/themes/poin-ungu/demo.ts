import { makeDemo } from "../demo-base";

// The design has empty photo slots; the demo fills them with stock photos from the shared theme library.
export const demo = makeDemo({
  couple: {
    bride: "Keisha", groom: "Putra",
    brideFull: "Keisha Amelia", groomFull: "Putra Wardana",
    brideParents: "Putri Bapak Doni & Ibu Siska", groomParents: "Putra Bapak Wawan & Ibu Nani",
    bridePhoto: "/themes/img/a19.webp", groomPhoto: "/themes/img/a20.webp",
  },
  eventLabel: "Pernikahan",
  date: "2027-05-22T08:00:00+07:00",
  place: "Atria Ballroom",
  address: "Gading Serpong, Tangerang",
  stories: [
    { title: "Kenalan di food court", date: "2019", body: "Berbagi meja di food court yang penuh, lalu berbagi cerita." },
    { title: "Jadian (double points!)", date: "2022", body: "Akhirnya resmi jadian." },
    { title: "Lamaran diterima", date: "2026", body: "Lamaran sederhana bersama dua keluarga." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-22T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Masjid Al-Azhar BSD", address: "BSD City, Tangerang" },
    { name: "Resepsi", date: "2027-05-22T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Atria Ballroom, Gading Serpong", address: "Gading Serpong, Tangerang" },
  ],
  gallery: ["/themes/img/a22.webp", "/themes/img/a23.webp", "/themes/img/a21.webp"],
  gifts: [{ id: "demo-ewallet", type: "ewallet", ewallet_provider: "dana", ewallet_number: "0812 2205 2027", account_name: "Keisha Amelia" }],
  guestName: "Ibu Maria Theresia & Keluarga",
});

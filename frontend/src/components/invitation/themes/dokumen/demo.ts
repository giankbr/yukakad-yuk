import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Tasya", groom: "Bram",
    note: "Dari rapat proyek kampus 2021 sampai halaman ini — semua terdokumentasi rapi.",
    brideFull: "Tasya Kirana", groomFull: "Bram Aditya",
    brideParents: "Putri Bapak Kirana & Ibu Ajeng", groomParents: "Putra Bapak Adit & Ibu Rukmini",
    bridePhoto: "/themes/img/r79.webp", groomPhoto: "/themes/img/r76.webp",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-08T08:00:00+07:00",
  place: "The Breeze, BSD City",
  address: "BSD City, Tangerang Selatan",
  stories: [
    { date: "2021", title: "Satu kelompok proyek kampus", body: "Tasya bikin timeline, Bram yang telat." },
    { date: "2023", title: "Resmi", body: "Status hubungan: in progress → committed." },
    { date: "2026", title: "Lamaran", body: "Task 'menikah' dipindah ke kolom Done." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-08T08:00:00+07:00", time: "08.00", venue: "Masjid Al-Hakim BSD", address: "BSD City, Tangerang Selatan" },
    { name: "Resepsi", date: "2027-08-08T11:00:00+07:00", time: "11.00", venue: "The Breeze, BSD City", address: "BSD City, Tangerang Selatan" },
  ],
  gallery: ["/themes/img/r66.webp", "/themes/img/r76.webp", "/themes/img/r74.webp", "/themes/img/r79.webp"],
  gifts: [{ id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0808 2027 21", account_name: "Tasya Kirana" }],
  guestName: "Bapak Yoga Pratista & Keluarga",
});

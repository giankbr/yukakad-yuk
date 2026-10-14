import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Fatimah", groom: "Yusuf",
    note: "“Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya.” — QS. Ar-Rum: 21",
    brideFull: "Fatimah Az-Zahra, S.Ag.", groomFull: "Muhammad Yusuf, Lc.",
    brideParents: "Putri dari Bapak H. Abdullah & Ibu Hj. Maryam", groomParents: "Putra dari Bapak H. Ibrahim & Ibu Hj. Aisyah",
  },
  eventLabel: "Pernikahan",
  date: "2026-09-20T08:00:00+07:00",
  place: "Masjid Agung Al-Azhar",
  address: "Jl. Sisingamangaraja, Kebayoran Baru, Jakarta",
  stories: [
    { title: "Perkenalan", date: "2024", body: "Dipertemukan melalui ustadzah pembimbing kajian pekanan." },
    { title: "Pertemuan Keluarga", date: "2025", body: "Pertemuan keluarga pertama, saling mengenal dengan adab." },
    { title: "Lamaran", date: "2025", body: "Yusuf melamar Fatimah di hadapan kedua keluarga." },
  ],
  events: [
    { name: "Akad Nikah", date: "2026-09-20T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Al-Azhar", address: "Jl. Sisingamangaraja, Kebayoran Baru, Jakarta" },
    { name: "Resepsi Pernikahan", date: "2026-09-20T10:00:00+07:00", time: "10.00 – 13.00 WIB", venue: "Aula Al-Azhar", address: "Jl. Sisingamangaraja, Kebayoran Baru, Jakarta" },
  ],
  gallery: ["/themes/img/a58.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7120 3344 5566", account_name: "Fatimah Az-Zahra" },
    { id: "demo-kado", type: "address", address: "Jl. Cipete Raya No. 45, Jakarta Selatan" },
  ],
  guestName: "Bapak H. Abdullah & Keluarga",
});

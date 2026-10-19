import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Khadijah", groom: "Hamzah",
    note: "Dua hati yang dipertemukan dalam taat, semoga dipersatukan hingga ke jannah-Nya.",
    brideFull: "Khadijah Nur Azizah, S.Pd.", groomFull: "Hamzah Al-Faruq, S.T.",
    brideParents: "Putri dari Bapak H. Ahmad Syarifuddin & Ibu Hj. Siti Rahmah",
    groomParents: "Putra dari Bapak H. Muhammad Ridwan & Ibu Hj. Nur Laila",
    bridePhoto: "/themes/img/a19.webp", groomPhoto: "/themes/img/a20.webp",
  },
  eventLabel: "Pernikahan",
  date: "2027-05-15T08:00:00+07:00",
  place: "Masjid Raya Al-Falah",
  address: "Jl. Darmo No. 137, Surabaya",
  stories: [
    { title: "Ta'aruf", date: "2025", body: "Diperkenalkan oleh guru mengaji kami, berbekal biodata dan niat yang lurus." },
    { title: "Khitbah", date: "Agustus 2026", body: "Hamzah bersama keluarga datang meminang Khadijah di rumah keluarga di Sidoarjo." },
    { title: "Menuju Akad", date: "Mei 2027", body: "Dengan izin Allah, kami memantapkan langkah menyempurnakan separuh agama." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-15T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Raya Al-Falah", address: "Jl. Darmo No. 137, Surabaya" },
    { name: "Walimatul 'Ursy", date: "2027-05-15T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Grand Darmo Suite", address: "Jl. Raya Darmo No. 68, Surabaya" },
  ],
  gallery: ["/themes/img/a118.webp", "/themes/img/a116.webp", "/themes/img/a85.webp", "/themes/img/a22.webp", "/themes/img/r65.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7123456789", account_name: "Khadijah Nur Azizah" },
    { id: "demo-ew", type: "ewallet", ewallet_provider: "dana", ewallet_number: "081234567890", account_name: "Hamzah Al-Faruq" },
    { id: "demo-kado", type: "address", address: "Jl. Kertajaya Indah No. 21, Surabaya 60116" },
  ],
  guestName: "Bapak Ustadz Fadlan & Keluarga",
});

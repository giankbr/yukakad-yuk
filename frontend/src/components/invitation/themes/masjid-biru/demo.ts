import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Zahra", groom: "Fikri",
    note: "Di bawah langit yang sama, kami memohon agar Allah menjadikan rumah kami tempat yang teduh untuk beribadah.",
    brideFull: "Zahra Salsabila Putri, S.Farm.", groomFull: "Muhammad Fikri Ramadhan, M.Kom.",
    brideParents: "Putri kedua dari Bapak Drs. H. Hasan Basri & Ibu Hj. Rosmawati",
    groomParents: "Putra sulung dari Bapak H. Zainal Abidin & Ibu Hj. Fauziah",
  },
  eventLabel: "Pernikahan",
  date: "2027-02-20T09:00:00+07:00",
  place: "Masjid Agung Sunda Kelapa",
  address: "Jl. Taman Sunda Kelapa No. 16, Menteng, Jakarta Pusat",
  stories: [
    { title: "Satu Shaf Kajian", date: "2023", body: "Kami sama-sama menjadi relawan kajian remaja masjid, saling mengenal dari kejauhan." },
    { title: "Istikharah", date: "2025", body: "Setelah ta'aruf yang didampingi keluarga, kami memohon petunjuk dan Allah memudahkan jalannya." },
    { title: "Lamaran", date: "Oktober 2026", body: "Keluarga Fikri datang bersilaturahmi dan meminang Zahra dengan penuh kehangatan." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-02-20T09:00:00+07:00", time: "09.00 – 10.00 WIB", venue: "Masjid Agung Sunda Kelapa", address: "Jl. Taman Sunda Kelapa No. 16, Menteng, Jakarta Pusat" },
    { name: "Resepsi", date: "2027-02-20T19:00:00+07:00", time: "19.00 – 21.30 WIB", venue: "Balai Kartini — Ruang Nusantara", address: "Jl. Gatot Subroto Kav. 37, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/a116.webp", "/themes/img/a118.webp", "/themes/img/a85.webp", "/themes/img/a22.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Bank Muamalat", account_number: "3010045678", account_name: "Zahra Salsabila Putri" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "081298765432", account_name: "Muhammad Fikri Ramadhan" },
  ],
  guestName: "Ibu Hj. Nurhayati & Keluarga",
  guestTable: "Meja Melati 3",
});

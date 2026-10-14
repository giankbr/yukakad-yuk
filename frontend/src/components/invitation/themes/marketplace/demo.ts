import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Rina", groom: "Bima",
    brideFull: "Rina Maharani, S.Ds.", groomFull: "Bima Prakoso, S.T.",
    brideParents: "Putri dari Bpk. Ahmad & Ibu Siti", groomParents: "Putra dari Bpk. Hadi & Ibu Ratna",
    bridePhoto: "/themes/img/a19.webp", groomPhoto: "/themes/img/a20.webp",
  },
  eventLabel: "Pernikahan",
  date: "2026-12-12T08:00:00+07:00",
  place: "Gedung Graha Sarana",
  address: "Jl. Gatot Subroto Kav. 12, Jakarta",
  stories: [
    { title: "Pesanan Diterima", date: "Mar 2019", body: "Pertama bertemu di kelas desain. Bima pinjam pensil, tidak pernah dikembalikan." },
    { title: "Diproses", date: "Agu 2020", body: "Mulai pacaran setelah satu tahun saling kirim playlist." },
    { title: "Dikemas", date: "Jun 2025", body: "Bima melamar di pantai Lombok saat matahari terbenam.", image: "/themes/img/a21.webp" },
  ],
  events: [
    { name: "Akad Nikah", date: "2026-12-12T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Masjid Agung Al-Azhar", address: "Jl. Sisingamangaraja, Kebayoran Baru" },
    { name: "Resepsi", date: "2026-12-12T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Graha Sarana", address: "Jl. Gatot Subroto Kav. 12, Jakarta" },
  ],
  gallery: ["/themes/img/a18.webp", "/themes/img/a22.webp", "/themes/img/a23.webp", "/themes/img/a25.webp", "/themes/img/a26.webp", "/themes/img/a24.webp"],
  gifts: [{ id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "123 456 7890", account_name: "Rina Maharani" }],
  guestName: "Bapak Budi Santoso & Keluarga",
});

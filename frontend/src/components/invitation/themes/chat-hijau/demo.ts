import { makeDemo } from "../demo-base";

const day = "2027-02-14";

export const demo = makeDemo({
  couple: {
    bride: "Fitri", groom: "Andra",
    note: "Setelah 6 tahun, akhirnya kami memutuskan untuk menikah!",
    brideFull: "Fitri Handayani, S.Pd.", groomFull: "Andra Wicaksono, S.T.",
    brideParents: "Putri Bapak Kumala & Ibu Sari", groomParents: "Putra Bapak Wicak & Ibu Endah",
    bridePhoto: "/themes/img/r3.webp", groomPhoto: "/themes/img/r4.webp",
  },
  eventLabel: "Pernikahan",
  date: `${day}T08:00:00+07:00`,
  place: "Gedung Papadaan",
  address: "Jl. A. Yani, Bekasi",
  stories: [
    { title: "", date: "2021", body: "Kenalan di grup KKN. Andra paling rajin bales chat" },
    { title: "", date: "2022", body: "Jadian! Ditembak via voice note 3 menit." },
    { title: "", date: "2026", body: "Andra datang ke rumah bawa keluarga. Lamaran diterima ✓" },
  ],
  events: [
    { name: "Akad Nikah", date: `${day}T08:00:00+07:00`, time: "08.00 – 10.00 WIB", venue: "Masjid Al-Barkah", address: "Bekasi" },
    { name: "Resepsi", date: `${day}T11:00:00+07:00`, time: "11.00 – 14.00 WIB", venue: "Gedung Papadaan", address: "Jl. A. Yani, Bekasi" },
  ],
  gallery: ["/themes/img/r0.webp", "/themes/img/r1.webp", "/themes/img/r6.webp", "/themes/img/r7.webp", "/themes/img/r5.webp", "/themes/img/r8.webp"],
  gifts: [{ id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "1402 2027 10", account_name: "Fitri H." }],
  guestName: "Ibu Ratih Kumala & Keluarga",
});

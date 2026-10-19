import { makeDemo } from "../demo-base";

const base = makeDemo();

export const demo = makeDemo({
  couple: {
    bride: "Yuliana", groom: "Markus",
    brideFull: "Yuliana Sampe Rante, S.Kep.", groomFull: "Markus Tandi Lolo, S.T.",
    brideParents: "Putri sulung dari\nBapak Yohanis Rante Allo & Ibu Debora Sampe Bua'",
    groomParents: "Putra ketiga dari\nBapak Daniel Tandi Lolo & Ibu Rahel Pasolang",
    note: "Dua rumpun tongkonan yang dipersatukan dalam kasih.",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-10T09:00:00+07:00",
  place: "Tongkonan Keluarga Rante Allo",
  address: "Lembang Nonongan, Sopai, Toraja Utara",
  stories: [
    { date: "2017", title: "Sama-sama Merantau", body: "Bertemu di persekutuan mahasiswa Toraja di Makassar. Yuliana pemandu pujian, Markus pemain gitarnya." },
    { date: "2021", title: "Pulang ke Rantepao", body: "Kembali ke kampung halaman, melayani bersama di jemaat dan sering menyusuri pematang di bawah Gunung Sesean." },
    { date: "2026", title: "Kunjungan Keluarga", body: "Keluarga besar Tandi Lolo datang ke tongkonan Rante Allo untuk menyampaikan maksud baik dan menetapkan hari." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-07-10T09:00:00+07:00", time: "10.00 – 11.30 WITA", venue: "Gereja Toraja Jemaat Rantepao", address: "Jl. Ahmad Yani, Rantepao, Toraja Utara" },
    { name: "Rampanan Kapa'", date: "2027-07-10T12:00:00+07:00", time: "13.00 – 15.00 WITA", venue: "Tongkonan Keluarga Rante Allo", address: "Lembang Nonongan, Sopai, Toraja Utara" },
    { name: "Resepsi", date: "2027-07-10T17:30:00+07:00", time: "18.30 – 21.00 WITA", venue: "Aula Serbaguna Rantepao", address: "Jl. Pongtiku, Rantepao, Toraja Utara" },
  ],
  gallery: ["/themes/img/a116.webp", "/themes/img/a22.webp", "/themes/img/r81.webp", "/themes/img/a33.webp", "/themes/img/r104.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0451 0100 2233 507", account_name: "Yuliana Sampe Rante" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "152 00 1234567 8", account_name: "Markus Tandi Lolo" },
    { id: "demo-kado", type: "address", address: "Jl. Pembangunan No. 8, Rantepao, Toraja Utara" },
  ],
  guestName: "Bapak Pdt. Samuel Pakan & Keluarga",
  extras: {
    ...base.extras,
    quote: { text: "Dan bilamana seorang dapat dialahkan, dua orang akan dapat bertahan. Tali tiga lembar tak mudah diputuskan.", source: "Pengkhotbah 4:12" },
    rundown: { items: [
      { time: "13.00", title: "Rombongan mempelai pria tiba", note: "Disambut keluarga di halaman tongkonan" },
      { time: "13.30", title: "Rampanan kapa'", note: "Dipimpin tetua adat & keluarga" },
      { time: "14.15", title: "Nasihat dan doa", note: "Oleh pendeta jemaat" },
      { time: "14.45", title: "Makan bersama", note: "Pa'piong & hidangan keluarga" },
    ] },
    dressCode: { note: "Busana bernuansa merah, hitam, atau kuning. Kain tenun Toraja sangat dipersilakan.", colors: ["#16110f", "#a3201b", "#e5a823", "#f3ece0"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-07-10T09:00:00+07:00" },
    family: { names: ["Kel. Besar Rante Allo", "Kel. Besar Tandi Lolo", "Keluarga Besar Tongkonan Pasolang", "Majelis Jemaat Rantepao"] },
    travel: { note: "Untuk tamu dari luar Toraja, berikut beberapa informasi perjalanan.", items: [
      { name: "Penginapan di Rantepao", detail: "Banyak pilihan di sekitar pusat kota, ± 15 menit ke tongkonan" },
      { name: "Dari Makassar", detail: "Bus malam ± 8 jam atau penerbangan ke Bandara Toraja" },
    ] },
    faq: { items: [
      { q: "Apakah tamu boleh hadir di rampanan kapa'?", a: "Boleh, tamu dipersilakan menyaksikan dari halaman tongkonan." },
      { q: "Bagaimana cuaca di Toraja?", a: "Malam hari cukup sejuk, sebaiknya membawa jaket atau selendang." },
    ] },
  },
});

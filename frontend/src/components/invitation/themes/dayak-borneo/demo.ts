import { makeDemo } from "../demo-base";

const base = makeDemo();

export const demo = makeDemo({
  couple: {
    bride: "Meiliana", groom: "Yosua",
    brideFull: "Meiliana Ambun, S.Hut.", groomFull: "Yosua Dandan Tingang, S.Kom.",
    brideParents: "Putri kedua dari\nBapak Yulius Ambun & Ibu Maria Itat",
    groomParents: "Putra sulung dari\nBapak Petrus Tingang & Ibu Ester Dinah",
    note: "Seperti enggang yang setia pada pasangannya seumur hidup.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-21T09:00:00+07:00",
  place: "Betang Adat Keluarga Ambun",
  address: "Jl. Tjilik Riwut Km. 7, Palangka Raya, Kalimantan Tengah",
  stories: [
    { date: "2018", title: "Bertemu di Hutan Kahayan", body: "Sama-sama relawan penanaman pohon di tepian Sungai Kahayan. Meiliana mencatat bibit, Yosua yang mengangkutnya." },
    { date: "2022", title: "Melangkah Bersama", body: "Lima tahun berteman, saling mendoakan, hingga yakin Tuhan menuntun ke arah yang sama." },
    { date: "2026", title: "Hakumbang Auh", body: "Keluarga Yosua datang menyampaikan maksud baik kepada keluarga Meiliana, disambut dengan sukacita." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-08-21T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Gereja Kalimantan Evangelis Jemaat Palangka", address: "Jl. Ahmad Yani, Palangka Raya" },
    { name: "Penganten Mandai", date: "2027-08-21T13:00:00+07:00", time: "13.00 – 15.00 WIB", venue: "Betang Adat Keluarga Ambun", address: "Jl. Tjilik Riwut Km. 7, Palangka Raya" },
    { name: "Resepsi", date: "2027-08-21T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Aula Jayang Tingang", address: "Jl. RTA Milono, Palangka Raya" },
  ],
  gallery: ["/themes/img/a30.webp", "/themes/img/r89.webp", "/themes/img/r11.webp", "/themes/img/r1.webp", "/themes/img/r16.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "Bank Kalteng", account_number: "0101 2345 6789", account_name: "Meiliana Ambun" },
    { id: "demo-ovo", type: "ewallet", ewallet_provider: "ovo", ewallet_number: "0811 5200 3344", account_name: "Yosua Dandan Tingang" },
  ],
  guestName: "Bapak Yohanes Ngabut & Keluarga",
  extras: {
    ...base.extras,
    quote: { text: "Dan di atas semuanya itu: kenakanlah kasih, sebagai pengikat yang mempersatukan dan menyempurnakan.", source: "Kolose 3:14" },
    rundown: { items: [
      { time: "13.00", title: "Lawang sakepeng", note: "Rombongan pengantin pria menembus gerbang adat" },
      { time: "13.30", title: "Penyambutan & dialog adat", note: "Kedua keluarga dipertemukan" },
      { time: "14.00", title: "Tampung tawar", note: "Doa dan restu para tetua" },
      { time: "14.30", title: "Makan bersama di betang" },
    ] },
    dressCode: { note: "Busana bernuansa hitam dengan aksen manik kuning, merah, atau tosca. Busana adat Dayak dipersilakan.", colors: ["#10221e", "#1f8a84", "#f0b429", "#c8322a"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-08-21T09:00:00+07:00" },
    family: { names: ["Kel. Besar Ambun", "Kel. Besar Tingang", "Keluarga Besar Betang Tumbang Rungan", "Persekutuan Pemuda GKE Palangka"] },
    travel: { note: "Untuk tamu dari luar kota, berikut beberapa pilihan terdekat.", items: [
      { name: "Bandara Tjilik Riwut", detail: "± 15 menit berkendara ke lokasi resepsi" },
      { name: "Penginapan di Jl. Imam Bonjol", detail: "Pusat kota, ± 10 menit ke gereja" },
    ] },
    faq: { items: [
      { q: "Apakah tamu boleh menyaksikan prosesi adat?", a: "Boleh, prosesi lawang sakepeng terbuka untuk seluruh tamu." },
      { q: "Apakah tersedia parkir?", a: "Tersedia parkir di halaman betang dan aula resepsi." },
    ] },
  },
});

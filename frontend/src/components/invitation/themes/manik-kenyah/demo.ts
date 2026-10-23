import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Ilun", groom: "Jalung",
    brideFull: "Yohana Ilun Lawing", groomFull: "Petrus Jalung Anyie",
    brideParents: "Putri dari Bapak Lawing Asang\n& Ibu Maria Ubung", groomParents: "Putra dari Bapak Anyie Njau\n& Ibu Lusia Bilung",
    note: "Seperti manik yang dironce satu per satu menjadi sulur yang utuh, kami dirangkai dalam kasih Tuhan, butir demi butir.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-14T09:00:00+08:00",
  place: "Lamin Adat Desa Setulang",
  address: "Desa Setulang, Kec. Malinau Selatan Hilir, Kabupaten Malinau, Kalimantan Utara",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "Agustus 2021", title: "Di Pesta Irau", body: "Ilun menari kancet di panggung Irau Malinau, Jalung memetik sape di belakangnya. Selesai tampil, kami tertawa karena salah hitung ketukan." },
    { date: "2023", title: "Menyusuri Sungai Malinau", body: "Jalung bekerja di Samarinda, Ilun mengajar di Malinau. Kami bertemu setiap libur, menumpang longboat ke kampung kakek dan nenek." },
    { date: "Desember 2026", title: "Peminangan", body: "Selepas ibadah Natal, keluarga Jalung datang membawa tanda pinangan. Para tetua lamin menyambut dengan restu." },
    { date: "Agustus 2027", title: "Hari Pemberkatan", body: "Kami diberkati di gereja, lalu dirayakan secara adat Kenyah di lamin bersama seluruh warga kampung." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-08-14T09:00:00+08:00", time: "09.00 – 11.00 WITA", venue: "Gereja GKII Jemaat Malinau Kota", address: "Jl. Pelita Kampung Baru, Malinau Kota, Kabupaten Malinau" },
    { name: "Pesta Adat Kenyah", date: "2027-08-14T15:00:00+08:00", time: "15.00 WITA – selesai", venue: "Lamin Adat Desa Setulang", address: "Desa Setulang, Kec. Malinau Selatan Hilir, Kabupaten Malinau" },
    { name: "Syukuran di Samarinda", date: "2027-08-21T18:30:00+08:00", time: "18.30 – 21.00 WITA", venue: "Aula Lamin Pemuda Samarinda", address: "Jl. Kesuma Bangsa No. 9, Sungai Pinang Luar, Samarinda" },
  ],
  gallery: ["/themes/img/a30.webp", "/themes/img/r89.webp", "/themes/img/r110.webp", "/themes/img/a26.webp"],
  gifts: [
    { id: "demo-bankaltimtara", type: "bank", bank_name: "Bankaltimtara", account_number: "0071 2027 0814", account_name: "Yohana Ilun Lawing" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0332 0108 5521 509", account_name: "Petrus Jalung Anyie" },
    { id: "demo-kado", type: "address", address: "Jl. Raja Pandita RT 04, Malinau Kota, Kabupaten Malinau, Kalimantan Utara 77554" },
  ],
  guestName: "Bapak Yosef Usat & Keluarga",
  guestTable: "Lamin 2",
  extras: {
    quote: { text: "Dan di atas semuanya itu: kenakanlah kasih, sebagai pengikat yang mempersatukan dan menyempurnakan.", source: "Kolose 3:14" },
    rundown: { items: [
      { time: "15.00", title: "Penyambutan rombongan di tangga lamin" },
      { time: "15.45", title: "Upacara adat dan nasihat para tetua" },
      { time: "17.30", title: "Makan bersama di ruang lamin" },
      { time: "19.00", title: "Tari kancet dan petikan sape" },
    ] },
    dressCode: { note: "Busana adat atau batik dipersilakan. Nuansa kuning, hitam, putih, dengan aksen merah atau biru.", colors: ["#e8b52a", "#16110e", "#efe8d8", "#b5322a", "#2b5ba8"] },
    rsvpDietary: {},
    family: { names: ["Keluarga Besar Lawing Asang", "Keluarga Besar Anyie Njau", "Warga Lamin Desa Setulang"] },
    travel: { note: "Untuk tamu dari Samarinda dan Tarakan.", items: [
      { name: "Penerbangan ke Malinau", detail: "Bandara Robert Atty Bessing, dari Tarakan sekitar 30 menit" },
      { name: "Antar-jemput ke Setulang", detail: "Mobil keluarga berangkat dari gereja pukul 13.30" },
    ] },
    faq: { items: [
      { q: "Apakah boleh membawa anak?", a: "Tentu. Lamin luas dan anak-anak sangat diterima." },
      { q: "Berapa jauh Setulang dari kota?", a: "Sekitar 40 menit dari Malinau Kota lewat jalan darat. Rombongan keluarga akan memandu." },
    ] },
  },
});

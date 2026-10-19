import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Sekar", groom: "Rangga",
    brideFull: "Sekar Ayu Kusumawardani, S.Pd.", groomFull: "Rangga Permana Sukmana, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Asep Saepudin & Ibu Hj. Nining Kurniasih", groomParents: "Putra pertama dari\nBapak Dedi Supriatna & Ibu Iis Rohaeti",
    bridePhoto: "/themes/img/a19.webp", groomPhoto: "/themes/img/a20.webp",
  },
  eventLabel: "Pernikahan",
  date: "2027-05-15T08:00:00+07:00",
  place: "Grha Sanusi Hardjadinata",
  address: "Jl. Dipati Ukur No. 35, Lebakgede, Coblong, Kota Bandung",
  stories: [
    { date: "2019", title: "Pendak Munggaran", body: "Bertemu di kampus Jatinangor saat sama-sama ikut UKM angklung. Rangga yang memainkan, Sekar yang bernyanyi." },
    { date: "2022", title: "Silih Pikanyaah", body: "Tiga tahun saling mendukung — dari skripsi hingga pekerjaan pertama di Bandung." },
    { date: "2026", title: "Neundeun Omong", body: "Keluarga Rangga datang ke Cianjur untuk melamar, disambut hangat keluarga besar Sekar." },
  ],
  events: [
    { name: "Siraman & Ngeuyeuk Seureuh", date: "2027-05-14T09:00:00+07:00", time: "09.00 – 12.00 WIB", venue: "Bumi Kulawarga Mempelai Istri", address: "Jl. Cihampelas No. 118, Coblong, Kota Bandung" },
    { name: "Akad Nikah", date: "2027-05-15T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Pusdai Jawa Barat", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Kota Bandung" },
    { name: "Upacara Adat Sawer & Nincak Endog", date: "2027-05-15T10:00:00+07:00", time: "10.00 – 10.45 WIB", venue: "Grha Sanusi Hardjadinata", address: "Jl. Dipati Ukur No. 35, Coblong, Kota Bandung" },
    { name: "Resepsi", date: "2027-05-15T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Grha Sanusi Hardjadinata", address: "Jl. Dipati Ukur No. 35, Coblong, Kota Bandung" },
  ],
  gallery: ["/themes/img/a22.webp", "/themes/img/a116.webp", "/themes/img/a64.webp", "/themes/img/a19.webp", "/themes/img/a20.webp", "/themes/img/a125.webp"],
  gifts: [
    { id: "demo-bjb", type: "bank", bank_name: "BJB", account_number: "0012 3456 7890 1", account_name: "Sekar Ayu Kusumawardani" },
    { id: "demo-dana", type: "ewallet", ewallet_provider: "dana", ewallet_number: "0812 2233 4455", account_name: "Rangga Permana" },
    { id: "demo-kado", type: "address", address: "Jl. Cihampelas No. 118, Coblong, Kota Bandung 40131" },
  ],
  guestName: "Bapak Ujang Suryana & Keluarga",
  guestTable: "7",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "10.00", title: "Sawer & nincak endog", note: "Upacara adat di pelaminan" },
      { time: "10.30", title: "Buka pintu & huap lingkung" },
      { time: "11.00", title: "Resepsi dibuka", note: "Diiringi degung & kacapi suling" },
    ] },
    dressCode: { note: "Nuansa hijau, emas, dan putih. Kebaya atau batik dipersilakan.", colors: ["#1d4a33", "#c9a54e", "#fffaf0", "#2f6b4c"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-05-15T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. H. Asep Saepudin", "Kel. Besar Bpk. Dedi Supriatna", "Wargi Paguyuban Pasundan Coblong", "Rekan Angklung Jatinangor"] },
    travel: { note: "Untuk tamu dari luar kota, berikut beberapa pilihan terdekat dari lokasi.", items: [
      { name: "Hotel di sekitar Dago", detail: "± 1,5 km dari gedung" },
      { name: "Parkir", detail: "Area parkir gedung & halaman kampus, ada petugas" },
    ] },
    faq: { items: [
      { q: "Boleh membawa anak?", a: "Tentu, putra-putri sangat diterima." },
      { q: "Apakah upacara adat terbuka untuk tamu?", a: "Ya, upacara sawer dan nincak endog dapat disaksikan seluruh tamu sebelum resepsi." },
    ] },
  },
});

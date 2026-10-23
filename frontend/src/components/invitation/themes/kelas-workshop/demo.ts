import { makeDemo } from "../demo-base";

const ART = "/themes/art/kelas-workshop";

export const demo = makeDemo({
  couple: {
    bride: "Mbak Laras", groom: "Studio Lempung",
    brideFull: "Larasati Wening Pangestu", groomFull: "Studio Lempung Kasongan",
    brideParents: "Perajin gerabah & pengajar kriya sejak 2014", groomParents: "Ruang kriya keramik kecil di Kasongan, Bantul",
    note: "Satu hari, lima kilo tanah liat, dan tangan yang boleh kotor. Pulang membawa mangkuk buatan sendiri.",
  },
  eventLabel: "Kelas Gerabah Pemula",
  date: "2027-03-13T09:00:00+07:00",
  place: "Studio Lempung Kasongan",
  address: "Jl. Kasongan No. 45, Bangunjiwo, Kasihan, Bantul, DI Yogyakarta",
  story: { title: "Silabus kelas", body: "" },
  stories: [
    { date: "Sesi 1 · 09.00", title: "Mengenal Tanah Liat", body: "Menguleni dan membuang udara dari tanah liat, mengenal kadar air, dan membuat mangkuk pijit pertama." },
    { date: "Sesi 2 · 10.15", title: "Teknik Pilin & Lempeng", body: "Membangun cangkir dari pilinan tanah dan piring kecil dari lempengan yang digiling rata." },
    { date: "Sesi 3 · 11.30", title: "Mencoba Meja Putar", body: "Memusatkan tanah di atas meja putar dan menarik dinding silinder. Gagal itu biasa, kami pandu pelan-pelan." },
    { date: "Sesi 4 · 13.30", title: "Hias, Toreh & Glasir", body: "Menoreh motif, memilih warna glasir, lalu menitipkan karya untuk dibakar di tungku studio." },
  ],
  events: [
    { name: "Kelas Gerabah Pemula", date: "2027-03-13T09:00:00+07:00", time: "09.00 – 15.00 WIB (istirahat makan siang 12.30)", venue: "Studio Lempung Kasongan", address: "Jl. Kasongan No. 45, Bangunjiwo, Kasihan, Bantul, DI Yogyakarta" },
    { name: "Ambil Hasil Bakaran", date: "2027-03-27T10:00:00+07:00", time: "10.00 – 16.00 WIB", venue: "Studio Lempung Kasongan", address: "Jl. Kasongan No. 45, Bangunjiwo, Kasihan, Bantul, DI Yogyakarta" },
  ],
  gallery: [`${ART}/rak.webp`, `${ART}/meja.webp`, `${ART}/celemek.webp`],
  gifts: [
    { id: "demo-kelas", type: "bank", bank_name: "BPD DIY", account_number: "0021 4455 6789", account_name: "Studio Lempung Kasongan" },
  ],
  guestName: "Kak Sinta Maharani",
  guestTable: "Meja Putar 3",
  extras: {
    quote: { text: "Tanah liat tidak pernah terburu-buru. Ia hanya meminta tangan yang sabar.", source: "Catatan di dinding Studio Lempung" },
    dressCode: { note: "Pakai baju yang boleh kotor dan kuku pendek. Celemek kami sediakan.", colors: ["#c46a3f", "#7f9c78", "#e2aa45", "#4f6d8f"] },
    guestPass: { note: "Tunjukkan kode ini di meja depan studio untuk mengambil celemek dan tanah liatmu." },
    rsvpDietary: { label: "Alergi makanan untuk makan siang? (opsional)" },
    faq: { items: [
      { q: "Belum pernah memegang tanah liat, boleh ikut?", a: "Justru kelas ini dibuat untuk pemula. Maksimal 10 peserta, jadi setiap orang mendapat pendampingan." },
      { q: "Kapan hasil karya bisa diambil?", a: "Karya dikeringkan dan dibakar dua kali, siap diambil dua minggu kemudian atau dikirim dengan ongkos kirim sendiri." },
      { q: "Bolehkah mengajak anak?", a: "Untuk usia 12 tahun ke atas dengan pendamping. Kelas anak tersedia setiap Minggu pagi." },
    ] },
  },
});

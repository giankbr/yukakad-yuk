import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadia", groom: "Faris",
    brideFull: "Nadia Salsabila Rahman, S.Ars.", groomFull: "Faris Ramadhan Alatas, S.T.",
    brideParents: "Putri pertama dari\nBapak H. Abdul Rahman & Ibu Hj. Siti Maryam", groomParents: "Putra kedua dari\nBapak Hasan Alatas & Ibu Fatimah Zahra",
    note: "Rumah yang kami impikan sederhana saja: dinding yang hangat, pintu yang selalu terbuka, dan lampu yang menyala untuk setiap tamu.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-05-22T09:00:00+07:00",
  place: "Rumah Tanah Liat Dago",
  address: "Jl. Dago Pakar Raya No. 27, Mekarsaluyu, Cimenyan, Kabupaten Bandung",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2020", title: "Studio Arsitektur", body: "Nadia merancang rumah, Faris menghitung strukturnya. Kami bertemu di proyek rumah tanah di lereng Dago." },
    { date: "2023", title: "Belajar Tadelakt", body: "Kami ikut kelas plester kapur tradisional bersama para pengrajin, dan diam-diam mulai merancang rumah kami sendiri." },
    { date: "2026", title: "Khitbah", body: "Dengan niat baik dan restu dua keluarga, Faris datang melamar pada bulan Syawal." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-22T09:00:00+07:00", time: "09.00 – 10.00 WIB", venue: "Masjid Pusdai Jawa Barat", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Cibeunying Kaler, Kota Bandung" },
    { name: "Walimah", date: "2027-05-22T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Rumah Tanah Liat Dago", address: "Jl. Dago Pakar Raya No. 27, Mekarsaluyu, Cimenyan, Kabupaten Bandung" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7123 4567 89", account_name: "Nadia Salsabila Rahman" },
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "3480 9911 22", account_name: "Faris Ramadhan Alatas" },
  ],
  guestName: "Ibu Hj. Khadijah & Keluarga",
  guestTable: "Meja Cedar 4",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu", note: "Teh mint dan kurma di serambi" },
      { time: "11.30", title: "Doa & tausiyah singkat" },
      { time: "12.00", title: "Jamuan walimah", note: "Area pria dan wanita terpisah" },
      { time: "13.30", title: "Ramah tamah keluarga" },
    ] },
    dressCode: { note: "Busana muslim warna tanah: tanah liat, pasir, zaitun, dan krem.", colors: ["#b87561", "#e8d2bd", "#7c7a5a", "#3e2214"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. H. Abdul Rahman", "Kel. Besar Bpk. Hasan Alatas"] },
    faq: { items: [
      { q: "Apakah area tamu pria dan wanita terpisah?", a: "Ya, jamuan walimah disiapkan di dua ruang yang terpisah dengan pintu masing-masing." },
      { q: "Apakah tersedia tempat salat?", a: "Mushola tersedia di sayap timur, lengkap dengan perlengkapan salat." },
    ] },
  },
});

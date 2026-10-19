import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Rahmat", groom: "Wulan",
    note: "Alhamdulillah, setelah bertahun-tahun menabung dan menanti, kami kini menempati rumah baru. Kami ingin mensyukurinya bersama orang-orang terdekat.",
    brideFull: "Rahmat Hidayat", groomFull: "Wulan Sari Kusumawati",
    brideParents: "beserta putra-putri, Kenzie & Alya",
  },
  eventLabel: "Tasyakuran Rumah Baru",
  date: "2027-02-07T16:00:00+07:00",
  place: "Rumah Baru Keluarga Rahmat",
  address: "Perumahan Griya Asri Blok C3 No. 12, Jl. Kaliurang Km 9, Ngaglik, Sleman, Yogyakarta",
  story: { title: "Cerita rumah ini", body: "" },
  stories: [
    { date: "2017", title: "Rumah kontrakan pertama", body: "Dua kamar sempit di Gang Mawar, tempat kami belajar menata hidup berdua." },
    { date: "2022", title: "Menabung sedikit demi sedikit", body: "Celengan bambu di atas lemari jadi saksi mimpi kecil: punya rumah sendiri." },
    { date: "2025", title: "Peletakan batu pertama", body: "Kenzie dan Alya ikut menanam pohon mangga di halaman depan." },
    { date: "2027", title: "Pintu yang terbuka", body: "Rumah ini kini siap menyambut keluarga, sahabat, dan tetangga baru." },
  ],
  events: [
    { name: "Pengajian & Doa Bersama", date: "2027-02-07T16:00:00+07:00", time: "16.00 WIB (ba'da Ashar)", venue: "Rumah Baru Keluarga Rahmat", address: "Perumahan Griya Asri Blok C3 No. 12, Ngaglik, Sleman" },
    { name: "Ramah Tamah & Makan Bersama", date: "2027-02-07T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Halaman & teras rumah", address: "Perumahan Griya Asri Blok C3 No. 12, Ngaglik, Sleman" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BSI", account_number: "7123 4567 89", account_name: "Wulan Sari Kusumawati" },
    { id: "demo-kado", type: "address", address: "Perumahan Griya Asri Blok C3 No. 12, Jl. Kaliurang Km 9, Ngaglik, Sleman, Yogyakarta 55581" },
  ],
  guestName: "Bapak Haryono & Keluarga",
  guestTable: "",
  extras: {
    rundown: { items: [
      { time: "16.00", title: "Pembukaan & sambutan tuan rumah" },
      { time: "16.20", title: "Pembacaan Yasin & tahlil", note: "Dipimpin Ustaz Muhammad Arif" },
      { time: "17.15", title: "Doa keberkahan rumah" },
      { time: "18.30", title: "Potong tumpeng & ramah tamah" },
    ] },
    dressCode: { note: "Busana muslim atau batik, nyaman untuk duduk lesehan.", colors: ["#43553f", "#b85c38", "#e9c7b2", "#f2ead9"] },
    guestPass: {},
    rsvpDietary: {},
    family: { title: "Turut berbahagia", names: ["Kel. Bpk. H. Sudarmo (Klaten)", "Kel. Bpk. Kusumo Wardoyo (Magelang)", "Warga RT 04 Griya Asri"] },
    travel: { note: "Patokan menuju rumah:", items: [
      { name: "Gerbang Griya Asri", detail: "± 200 m setelah SPBU Km 9, belok kanan" },
      { name: "Parkir", detail: "Lapangan blok C, tersedia petugas parkir" },
    ] },
    faq: { items: [
      { q: "Apakah acara terbuka untuk anak-anak?", a: "Tentu, anak-anak sangat diterima. Disediakan tikar di halaman." },
      { q: "Perlu membawa sesuatu?", a: "Cukup hadir dan doakan kami. Itu sudah lebih dari cukup." },
    ] },
  },
});

import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Keluarga Halim", groom: "",
    brideFull: "Opa Gunawan Halim & Oma Lily Tjandra",
    brideParents: "Bersama anak, menantu, dan cucu:\nKeluarga Steven Halim · Keluarga Yohana & Andreas Wibisono · Keluarga Kevin Halim",
    note: "Setahun penuh kita berpencar di banyak kota. Malam ini, mari pulang dan duduk di satu meja bundar.",
  },
  eventLabel: "Makan Malam Imlek Keluarga",
  date: "2027-02-05T18:00:00+07:00",
  place: "Kediaman Keluarga Halim",
  address: "Jl. Gang Pinggir No. 28, Kauman, Semarang Tengah, Kota Semarang",
  story: { title: "Tradisi Keluarga Kami", body: "" },
  stories: [
    { date: "1972", title: "Toko kecil di Gang Pinggir", body: "Opa dan Oma membuka toko kelontong di Pecinan Semarang. Makan malam Imlek pertama mereka hanya berdua, dengan semangkuk mi panjang umur." },
    { date: "1995", title: "Meja bundar pertama", body: "Anak-anak mulai berkeluarga. Meja bundar kayu jati dibeli supaya semua bisa duduk berhadapan dan saling mengambilkan lauk." },
    { date: "2027", title: "Tiga generasi, dua meja", body: "Tahun ini kita 28 orang. Cucu-cucu menyiapkan lampion, Oma tetap memasak bandeng presto dan mi panjang umur kesukaan semua." },
  ],
  events: [
    { name: "Makan Malam Reuni (Malam Tahun Baru)", date: "2027-02-05T18:00:00+07:00", time: "18.00 – 21.00 WIB", venue: "Kediaman Keluarga Halim", address: "Jl. Gang Pinggir No. 28, Kauman, Semarang Tengah, Kota Semarang" },
    { name: "Silaturahmi Hari Pertama Imlek", date: "2027-02-06T10:00:00+07:00", time: "10.00 – 13.00 WIB", venue: "Kediaman Keluarga Halim", address: "Jl. Gang Pinggir No. 28, Kauman, Semarang Tengah, Kota Semarang" },
  ],
  gallery: ["/themes/img/r74.webp", "/themes/img/r63.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "0094 1288 61", account_name: "Yohana Halim" },
  ],
  guestName: "Keluarga Om Hendra Wijaya",
  guestTable: "Meja Bundar 2",
  extras: {
    quote: { text: "家和万事兴 · Keluarga yang rukun membuat segala urusan berjalan lancar.", source: "Pepatah Tionghoa" },
    rundown: { items: [
      { time: "17.30", title: "Kedatangan & salam tahun baru", note: "Teh hangat dan kue keranjang" },
      { time: "18.00", title: "Makan malam reuni bersama", note: "Bandeng, mi panjang umur, dan sup ikan" },
      { time: "19.30", title: "Bagi angpao untuk anak-anak" },
      { time: "20.30", title: "Menyalakan lampion bersama di halaman" },
    ] },
    dressCode: { note: "Nuansa merah, emas, atau krem. Cheongsam dan baju koko dipersilakan.", colors: ["#c4161c", "#d8a640", "#f6eedd", "#f08a1c"] },
    guestPass: {},
    rsvpDietary: {},
    family: { title: "Yang berbahagia mengundang", names: ["Opa Gunawan & Oma Lily", "Keluarga Steven Halim", "Keluarga Yohana & Andreas Wibisono", "Keluarga Kevin Halim"] },
    faq: { items: [
      { q: "Perlukah membawa sesuatu?", a: "Cukup bawa diri dan keluarga. Bila ingin, sekeranjang jeruk mandarin selalu jadi kejutan manis untuk Oma." },
      { q: "Apakah ada tempat parkir?", a: "Parkir terbatas di Gang Pinggir; tersedia parkir umum di Jl. Wotgandul Timur, lima menit berjalan kaki." },
    ] },
  },
});

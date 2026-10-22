import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Simanjuntak", groom: "Wenas",
    brideFull: "Bapak Daniel Simanjuntak & Ibu Maria Lumbantobing",
    groomFull: "Bapak Yohanes Wenas & Ibu Ruth Pangemanan",
    brideParents: "Bersama Grace, Samuel & Natalia",
    groomParents: "Bersama Kevin & Michelle",
    note: "Mari pulang, duduk bersama, dan merayakan kasih yang lahir di malam kudus.",
  },
  eventLabel: "Perayaan Natal Keluarga",
  date: "2027-12-25T17:00:00+07:00",
  place: "Kediaman Keluarga Simanjuntak",
  address: "Jl. Pattimura No. 8, Kebun Bunga, Bandung Wetan, Kota Bandung",
  story: { title: "Tradisi Natal Kami", body: "" },
  stories: [
    { date: "1998", title: "Natal pertama bersama", body: "Dua keluarga bertetangga di Medan merayakan Natal di satu meja panjang. Sejak itu tak pernah terpisah." },
    { date: "2005", title: "Lapis legit Oma", body: "Resep Oma Wenas diturunkan ke anak dan cucu, dipanggang bersama setiap tanggal 23 Desember." },
    { date: "2027", title: "Tiga generasi, satu pohon", body: "Tahun ini cucu-cucu menghias pohon cemara bersama, lalu kita bernyanyi Malam Kudus sambil menyalakan lilin." },
  ],
  events: [
    { name: "Ibadah Natal Keluarga", date: "2027-12-25T17:00:00+07:00", time: "17.00 – 18.15 WIB", venue: "Kediaman Keluarga Simanjuntak", address: "Jl. Pattimura No. 8, Kebun Bunga, Bandung Wetan, Kota Bandung" },
    { name: "Makan Malam & Tukar Kado", date: "2027-12-25T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Taman Belakang Kediaman Simanjuntak", address: "Jl. Pattimura No. 8, Kebun Bunga, Bandung Wetan, Kota Bandung" },
  ],
  gallery: ["/themes/img/r72.webp", "/themes/img/r79.webp", "/themes/img/r61.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Mandiri", account_number: "1310 0177 2845", account_name: "Maria Lumbantobing" },
  ],
  guestName: "Keluarga Bapak Tobing",
  guestTable: "",
  extras: {
    quote: { text: "Kemuliaan bagi Allah di tempat yang mahatinggi dan damai sejahtera di bumi di antara manusia yang berkenan kepada-Nya.", source: "Lukas 2:14" },
    rundown: { items: [
      { time: "17.00", title: "Ibadah singkat & pembacaan kisah Natal" },
      { time: "17.45", title: "Menyalakan lilin & bernyanyi Malam Kudus" },
      { time: "18.30", title: "Makan malam bersama", note: "Arsik, saksang, dan klappertaart Oma" },
      { time: "20.00", title: "Tukar kado sederhana", note: "Kado bebas, maksimal Rp100.000" },
    ] },
    dressCode: { note: "Nuansa hangat Natal: merah, hijau cemara, atau krem.", colors: ["#b8322c", "#24573c", "#f1e4c4", "#c9a24e"] },
    guestPass: {},
    rsvpDietary: {},
    family: { title: "Yang berbahagia mengundang", names: ["Oma & Opa Wenas", "Keluarga Lumbantobing", "Keluarga Pangemanan"] },
    faq: { items: [
      { q: "Perlukah membawa kado?", a: "Untuk tukar kado, bawalah satu kado sederhana. Anak-anak akan mendapat bingkisan dari tuan rumah." },
      { q: "Apakah ada tempat parkir?", a: "Parkir tersedia di sepanjang Jl. Pattimura dan di halaman gereja seberang rumah." },
    ] },
  },
});

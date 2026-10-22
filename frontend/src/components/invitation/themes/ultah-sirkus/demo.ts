import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nayla", groom: "",
    brideFull: "Nayla Putri Maheswari",
    brideParents: "Putri pertama dari Bapak Reza Maheswara & Ibu Anindita Puspasari",
    note: "Tenda sudah berdiri dan lampu sudah menyala! Nayla genap lima tahun dan ingin merayakannya dengan pertunjukan kecil bersama teman-teman tersayang.",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-08-14T15:00:00+07:00",
  place: "Pendopo Taman Kenari",
  address: "Jl. Kenari Raya No. 8, Bintaro Jaya Sektor 9, Tangerang Selatan",
  story: { title: "Cerita Nayla", body: "" },
  stories: [
    { date: "2022", title: "Bintang kecil lahir", body: "Nayla lahir di suatu sore bulan Agustus, membawa tawa paling riuh ke rumah kami." },
    { date: "2024", title: "Penonton paling setia", body: "Setiap ada sulap atau badut di acara keluarga, Nayla selalu duduk paling depan sambil bertepuk tangan." },
    { date: "2026", title: "Masuk TK", body: "Hari pertama sekolah, Nayla langsung punya tiga sahabat dan pulang membawa gambar tenda sirkus." },
    { date: "2027", title: "Lima tahun!", body: "Sekarang Nayla suka menari, menghitung sampai seratus, dan bercita-cita jadi pesulap." },
  ],
  events: [
    { name: "Pertunjukan Ulang Tahun Nayla", date: "2027-08-14T15:00:00+07:00", time: "15.00 – 17.30 WIB", venue: "Pendopo Taman Kenari", address: "Jl. Kenari Raya No. 8, Bintaro Jaya Sektor 9, Tangerang Selatan" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Mandiri", account_number: "1270 0091 4425", account_name: "Anindita Puspasari" },
    { id: "demo-kado", type: "address", address: "Jl. Cempaka Putih Blok HD 3 No. 12, Bintaro Jaya Sektor 9, Tangerang Selatan 15229" },
  ],
  guestName: "Adik Raffa & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Nayla Putri Maheswari", nickname: "Nayla", birthDate: "2022-08-14T16:20:00+07:00", parents: "Putri pertama dari Bapak Reza Maheswara & Ibu Anindita Puspasari" },
    rundown: { items: [
      { time: "15.00", title: "Pintu tenda dibuka", note: "Tukar karcis dengan popcorn dan topi pesta" },
      { time: "15.30", title: "Pertunjukan sulap & balon", note: "Kak Dodi dan sahabat balonnya" },
      { time: "16.15", title: "Lomba lempar gelang & joget bersama" },
      { time: "16.45", title: "Tiup lilin, potong kue & bagi bingkisan" },
    ] },
    dressCode: { note: "Pakai baju paling ceria: garis-garis, polkadot, atau kostum sirkus favoritmu. Topi pesta kami sediakan!", colors: ["#d8402f", "#f2b134", "#2f8a92", "#fbf1dc"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Maheswara", "Opa & Oma Puspasari", "Kak Arsa (kakak sepupu Nayla)"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah paling seru. Kalau ingin memberi, ini yang sedang Nayla impikan.", items: [
      { id: "w1", name: "Set sulap anak", price: "± Rp120.000" },
      { id: "w2", name: "Buku cerita bergambar", price: "± Rp80.000", claimed_by: "Tante Mira" },
      { id: "w3", name: "Kostum pesulap kecil", price: "± Rp150.000" },
    ] },
    faq: { items: [
      { q: "Apakah orang tua ikut masuk?", a: "Tentu! Ada kursi penonton untuk Ayah & Bunda di belakang barisan anak-anak." },
      { q: "Ada area parkir?", a: "Parkir mobil tersedia di sepanjang Jl. Kenari Raya dan halaman pendopo." },
    ] },
  },
});

import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Zahra", groom: "",
    brideFull: "Zahra Aulia Ramadhani",
    brideParents: "Putri sulung dari Bapak Rizky Firmansyah & Ibu Anindya Putri",
    note: "Zahra sudah tujuh tahun! Ayo datang, naik pelangi, dan tiup lilin bersama Lulu si unicorn.",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-08-14T15:00:00+07:00",
  place: "Ruang Pesta Kebun Permen",
  address: "Jl. Bintaro Utama Sektor 3A No. 12, Pondok Aren, Tangerang Selatan",
  story: { title: "Cerita Zahra", body: "" },
  stories: [
    { date: "2020", title: "Bintang kecil lahir", body: "Zahra lahir di suatu sore bulan Agustus, saat hujan reda dan pelangi muncul di atas rumah." },
    { date: "2023", title: "Suka menggambar", body: "Setiap dinding dan kertas penuh gambar kuda bertanduk dengan rambut warna-warni." },
    { date: "2025", title: "Masuk TK", body: "Hari pertama sekolah Zahra membawa bekal berbentuk awan dan pulang dengan tiga teman baru." },
    { date: "2027", title: "Tujuh tahun!", body: "Sekarang Zahra sudah bisa membaca dongeng sendiri dan ingin jadi pelukis kalau besar nanti." },
  ],
  events: [
    { name: "Pesta Pelangi Zahra", date: "2027-08-14T15:00:00+07:00", time: "15.00 – 17.30 WIB", venue: "Ruang Pesta Kebun Permen", address: "Jl. Bintaro Utama Sektor 3A No. 12, Pondok Aren, Tangerang Selatan" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BSI", account_number: "7123 4567 89", account_name: "Anindya Putri" },
    { id: "demo-kado", type: "address", address: "Jl. Kenari Raya Blok F2 No. 8, Pondok Aren, Tangerang Selatan 15229" },
  ],
  guestName: "Adik Keisha & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Zahra Aulia Ramadhani", nickname: "Zahra", birthDate: "2020-08-14T16:20:00+07:00", parents: "Putri sulung dari Bapak Rizky Firmansyah & Ibu Anindya Putri" },
    rundown: { items: [
      { time: "15.00", title: "Datang & pakai bando tanduk", note: "Meja penyambutan di gerbang pelangi" },
      { time: "15.30", title: "Lukis wajah & mewarnai unicorn" },
      { time: "16.15", title: "Tiup lilin & potong kue awan", note: "Nyanyi bersama" },
      { time: "17.00", title: "Dongeng & bagi bingkisan" },
    ] },
    dressCode: { note: "Baju warna pastel: merah muda, ungu muda, biru langit, atau mint. Kostum unicorn dan peri sangat boleh!", colors: ["#f7a8c8", "#d4c1f5", "#b9dcff", "#bdeed8"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Firmansyah", "Eyang Kakung & Eyang Putri Hadi", "Adik Rafa (adik Zahra)"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terindah. Kalau ingin memberi, ini kesukaan Zahra.", items: [
      { id: "w1", name: "Set cat air & kuas anak", price: "± Rp95.000" },
      { id: "w2", name: "Buku dongeng bergambar", price: "± Rp70.000", claimed_by: "Tante Mira" },
      { id: "w3", name: "Boneka unicorn kecil", price: "± Rp120.000" },
    ] },
    faq: { items: [
      { q: "Apakah orang tua boleh menemani?", a: "Tentu! Ada sudut teh dan camilan untuk Ayah & Bunda." },
      { q: "Perlu membawa apa?", a: "Cukup bawa senyum. Bando tanduk dan cat wajah sudah kami siapkan." },
    ] },
  },
});

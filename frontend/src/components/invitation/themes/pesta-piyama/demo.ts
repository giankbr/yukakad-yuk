import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Aluna", groom: "",
    brideFull: "Aluna Kirana Wibowo",
    brideParents: "Putri pertama dari Bapak Arif Wibowo & Ibu Sekar Ayuningtyas",
    note: "Bawa piyama favorit dan bantal kecilmu! Kita bikin tenda selimut, nonton film, makan popcorn, dan bercerita sampai mengantuk.",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-03-20T17:00:00+07:00",
  place: "Rumah Keluarga Wibowo",
  address: "Jl. Cempaka Wangi III No. 14, Sektor 9, Bintaro, Tangerang Selatan",
  story: { title: "Cerita Aluna", body: "" },
  stories: [
    { date: "2019", title: "Bintang kecil lahir", body: "Aluna lahir di suatu malam bulan Maret, saat bulan sabit tampak tersenyum dari jendela." },
    { date: "2022", title: "Tenda selimut pertama", body: "Membangun tenda dari dua kursi makan dan selimut Eyang, lalu menolak tidur di kasur selama seminggu." },
    { date: "2025", title: "Pendongeng andal", body: "Mulai membacakan cerita untuk Momo si beruang setiap malam, lengkap dengan suara-suara lucu." },
    { date: "2027", title: "Delapan tahun!", body: "Sekarang ingin berbagi tenda, cerita, dan popcorn dengan teman-teman tersayang." },
  ],
  events: [
    { name: "Pesta Piyama", date: "2027-03-20T17:00:00+07:00", time: "17.00 – 21.00 WIB", venue: "Rumah Keluarga Wibowo", address: "Jl. Cempaka Wangi III No. 14, Sektor 9, Bintaro, Tangerang Selatan" },
    { name: "Sarapan Pancake & Penjemputan", date: "2027-03-21T07:30:00+07:00", time: "07.30 – 09.00 WIB", venue: "Rumah Keluarga Wibowo", address: "Jl. Cempaka Wangi III No. 14, Sektor 9, Bintaro, Tangerang Selatan" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "6280 3201 19", account_name: "Sekar Ayuningtyas" },
    { id: "demo-kado", type: "address", address: "Jl. Cempaka Wangi III No. 14, Sektor 9, Bintaro, Tangerang Selatan 15229" },
  ],
  guestName: "Adik Naira & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Aluna Kirana Wibowo", nickname: "Aluna", birthDate: "2019-03-20T21:10:00+07:00", parents: "Putri pertama dari Bapak Arif Wibowo & Ibu Sekar Ayuningtyas" },
    rundown: { items: [
      { time: "17.00", title: "Datang dengan piyama", note: "Bantal dan selimut kecil boleh dibawa" },
      { time: "17.30", title: "Membangun tenda selimut bersama" },
      { time: "18.30", title: "Makan malam & tiup lilin" },
      { time: "19.15", title: "Nonton film & popcorn", note: "Film animasi untuk semua umur" },
      { time: "20.30", title: "Dongeng senter sebelum tidur" },
    ] },
    dressCode: { note: "Piyama paling nyaman dan kaus kaki hangat. Boleh bawa boneka kesayangan!", colors: ["#22385a", "#8fd3c1", "#f08a74", "#ffd36e"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Eyang Kakung & Eyang Putri Wibowo", "Opa & Oma Hadisuwarno", "Tante Laras & Om Bima"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terbaik. Kalau ingin memberi, ini kesukaan Aluna.", items: [
      { id: "w1", name: "Lampu tidur proyektor bintang", price: "± Rp150.000" },
      { id: "w2", name: "Buku dongeng bergambar", price: "± Rp90.000", claimed_by: "Tante Laras" },
      { id: "w3", name: "Kantong tidur anak", price: "± Rp250.000" },
    ] },
    faq: { items: [
      { q: "Apakah anak-anak menginap?", a: "Ya, bagi yang diizinkan. Penjemputan esok paginya setelah sarapan pancake, pukul 07.30–09.00." },
      { q: "Bagaimana kalau anak belum siap menginap?", a: "Tidak apa-apa! Boleh dijemput pukul 21.00 setelah dongeng." },
      { q: "Perlu membawa apa?", a: "Piyama, sikat gigi, bantal kecil, dan boneka kesayangan. Kasur lipat sudah kami siapkan." },
    ] },
  },
});

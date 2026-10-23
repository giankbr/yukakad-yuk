import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Alesha", groom: "",
    brideFull: "Alesha Mutiara Putri",
    brideParents: "Putri pertama dari Bapak Fajar Nugroho & Ibu Larasati Dewi",
    note: "Alesha genap enam tahun! Ayo menyelam ke istana kerang, mencari mutiara, dan berpesta di bawah ombak.",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-06-12T15:00:00+07:00",
  place: "Kolam Renang Taman Laguna Biru",
  address: "Jl. Pantai Mutiara Blok F No. 3, Pluit, Penjaringan, Jakarta Utara",
  story: { title: "Cerita Alesha", body: "" },
  stories: [
    { date: "2021", title: "Mutiara kecil", body: "Alesha lahir di musim kemarau yang cerah. Ayah bilang tangisnya semerdu ombak di pagi hari." },
    { date: "2024", title: "Cipratan pertama", body: "Pertama kali ke pantai, Alesha tidak mau pulang. Ember kecilnya penuh kerang warna-warni." },
    { date: "2027", title: "Enam tahun!", body: "Sekarang Alesha sudah berani berenang tanpa pelampung dan ingin merayakannya bersama teman-teman di kolam." },
  ],
  events: [
    { name: "Pesta Istana Kerang Alesha", date: "2027-06-12T15:00:00+07:00", time: "15.00 – 17.30 WIB", venue: "Kolam Renang Taman Laguna Biru", address: "Jl. Pantai Mutiara Blok F No. 3, Pluit, Penjaringan, Jakarta Utara" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BNI", account_number: "0452 9917 63", account_name: "Larasati Dewi" },
    { id: "demo-kado", type: "address", address: "Jl. Muara Karang Raya Blok Z No. 21, Pluit, Jakarta Utara 14450" },
  ],
  guestName: "Adik Naira & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Alesha Mutiara Putri", nickname: "Alesha", birthDate: "2021-06-09T08:15:00+07:00", parents: "Putri pertama dari Bapak Fajar Nugroho & Ibu Larasati Dewi" },
    rundown: { items: [
      { time: "15.00", title: "Datang & pilih mahkota kerang", note: "Setiap anak menghias mahkotanya sendiri" },
      { time: "15.30", title: "Main air & berburu mutiara di kolam dangkal", note: "Didampingi kakak penjaga kolam" },
      { time: "16.30", title: "Ganti baju & dongeng istana laut" },
      { time: "17.00", title: "Tiup lilin, potong kue & bagi bingkisan" },
    ] },
    dressCode: { note: "Bawa baju renang dan handuk. Warna laut pastel paling cocok!", colors: ["#86d6c6", "#b9a3ea", "#f6a68f", "#fbf5ef"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Nugroho", "Eyang Dewi"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terindah. Kalau ingin memberi, ini yang sedang Alesha impikan.", items: [
      { id: "w1", name: "Kacamata renang anak", price: "± Rp90.000" },
      { id: "w2", name: "Buku dongeng laut bergambar", price: "± Rp85.000", claimed_by: "Tante Mira" },
      { id: "w3", name: "Set manik-manik kerang", price: "± Rp120.000" },
    ] },
    faq: { items: [
      { q: "Apakah anak perlu bisa berenang?", a: "Tidak perlu. Permainan di kolam dangkal setinggi lutut dan selalu didampingi penjaga." },
      { q: "Apakah orang tua boleh menemani?", a: "Tentu, tersedia tempat duduk teduh di tepi kolam." },
    ] },
  },
});

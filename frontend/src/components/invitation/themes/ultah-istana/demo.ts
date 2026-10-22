import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Alya", groom: "",
    brideFull: "Alya Putri Maharani",
    brideParents: "Putri pertama dari Bapak Dimas Prasetyo & Ibu Rara Anggraini",
    note: "Pintu istana sudah dibuka, kue sudah dihias, dan Putri Alya menunggu teman-temannya di taman bunga!",
  },
  eventLabel: "Ulang Tahun",
  date: "2027-04-17T15:00:00+07:00",
  place: "Taman Dongeng Kids Party House",
  address: "Jl. Raya Darmo Permai III No. 9, Pradahkalikendal, Dukuhpakis, Surabaya",
  story: { title: "", body: "" },
  stories: [
    { date: "2021", title: "Sang putri lahir", body: "Alya lahir di musim bunga tabebuya, saat jalanan Surabaya dipenuhi kelopak merah muda." },
    { date: "2024", title: "Penjaga taman kecil", body: "Setiap pagi Alya menyiram pot-pot bunga Ibu dan menamai semuanya satu per satu." },
    { date: "2027", title: "Enam tahun!", body: "Sekarang Alya sudah bisa membaca dongeng sendiri dan bercita-cita membangun istana bunga." },
  ],
  events: [
    { name: "Pesta Istana Alya", date: "2027-04-17T15:00:00+07:00", time: "15.00 – 17.30 WIB", venue: "Taman Dongeng Kids Party House", address: "Jl. Raya Darmo Permai III No. 9, Pradahkalikendal, Dukuhpakis, Surabaya" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0882 4410 27", account_name: "Rara Anggraini" },
    { id: "demo-kado", type: "address", address: "Jl. Bukit Darmo Golf Blok K-12, Dukuhpakis, Surabaya 60226" },
  ],
  guestName: "Kak Nayla & Keluarga",
  guestTable: "",
  extras: {
    child: { name: "Alya Putri Maharani", nickname: "Alya", birthDate: "2021-04-17T09:10:00+07:00", parents: "Putri pertama dari Bapak Dimas Prasetyo & Ibu Rara Anggraini" },
    rundown: { items: [
      { time: "15.00", title: "Masuk gerbang istana", note: "Ambil mahkota & tongkat bunga" },
      { time: "15.30", title: "Dongeng & tebak-tebakan" },
      { time: "16.15", title: "Tiup lilin & potong kue istana", note: "Nyanyi bersama" },
      { time: "17.00", title: "Berburu harta karun di taman" },
    ] },
    dressCode: { note: "Baju pesta warna pastel: merah muda, lilac, kuning mentega, atau mint. Kostum putri, ksatria, dan peri bunga sangat boleh!", colors: ["#f4b6c9", "#d7c3f0", "#fbe39a", "#bfe4d2"] },
    guestPass: {},
    rsvpDietary: { label: "Ada alergi makanan pada anak? (opsional)" },
    family: { title: "Turut mengundang", names: ["Kakek & Nenek Prasetyo", "Opa & Oma Anggraini", "Adik Bima (adik Alya)"] },
    wishlist: { note: "Kehadiran teman-teman sudah jadi hadiah terindah. Kalau ingin memberi, ini kesukaan Alya.", items: [
      { id: "w1", name: "Buku dongeng bergambar", price: "± Rp75.000" },
      { id: "w2", name: "Set menanam bunga anak", price: "± Rp90.000", claimed_by: "Tante Sasa" },
      { id: "w3", name: "Kostum peri bunga", price: "± Rp150.000" },
    ] },
    faq: { items: [
      { q: "Apakah orang tua boleh menemani?", a: "Tentu! Ada paviliun teh dan camilan untuk Ayah & Bunda." },
      { q: "Perlu membawa kostum?", a: "Boleh, tapi mahkota dan tongkat bunga sudah kami siapkan di gerbang." },
    ] },
  },
});

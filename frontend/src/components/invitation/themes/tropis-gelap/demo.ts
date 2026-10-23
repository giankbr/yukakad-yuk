import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kirana", groom: "Damar",
    brideFull: "Kirana Larasati Wiyono", groomFull: "Damar Adiputra Sembiring",
    brideParents: "Putri dari\nBapak Hendra Wiyono & Ibu Maya Susanti", groomParents: "Putra dari\nBapak Robert Sembiring & Ibu Lina Tarigan",
    bridePhoto: "/themes/img/a83.webp", groomPhoto: "/themes/img/a84.webp",
    note: "Seperti hutan setelah hujan: tenang, rimbun, dan selalu tumbuh.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-21T16:00:00+08:00",
  place: "Taman Rimba Sayan",
  address: "Jl. Raya Sayan No. 18, Kedewatan, Ubud, Gianyar, Bali",
  stories: [
    { date: "2020", title: "Di Bawah Hujan Tropis", body: "Kami berteduh di kedai yang sama saat hujan deras di Ubud, lalu mengobrol sampai kedai hampir tutup." },
    { date: "2023", title: "Tumbuh Bersama", body: "Merawat kebun kecil di balkon: monstera, pisang hias, dan janji-janji yang pelan-pelan berakar." },
    { date: "2027", title: "Hari yang Kami Tanam", body: "Di tengah kebun yang rimbun, kami mengikat janji di hadapan keluarga dan sahabat." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-08-21T16:00:00+08:00", time: "16.00 – 17.00 WITA", venue: "Taman Rimba Sayan", address: "Jl. Raya Sayan No. 18, Kedewatan, Ubud, Gianyar, Bali" },
    { name: "Jamuan Malam", date: "2027-08-21T18:30:00+08:00", time: "18.30 – 22.00 WITA", venue: "Paviliun Daun, Taman Rimba Sayan", address: "Jl. Raya Sayan No. 18, Kedewatan, Ubud, Gianyar, Bali" },
  ],
  gallery: ["/themes/img/a85.webp", "/themes/img/a86.webp", "/themes/img/a83.webp", "/themes/img/a84.webp", "/themes/img/a87.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "5210 8876 31", account_name: "Kirana Larasati Wiyono" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1370 0098 2214", account_name: "Damar Adiputra Sembiring" },
    { id: "demo-kado", type: "address", address: "Jl. Bisma No. 7, Ubud, Gianyar, Bali 80571" },
  ],
  guestName: "Bapak Antonius Gunawan & Keluarga",
  guestTable: "Meja Monstera 3",
  extras: {
    quote: { text: "Dua orang lebih baik daripada seorang diri; kalau yang satu jatuh, yang lain mengangkatnya.", source: "Kebijaksanaan lama" },
    rundown: { items: [
      { time: "16.00", title: "Upacara pernikahan", note: "Di bawah naungan pohon trembesi" },
      { time: "17.15", title: "Ramah tamah senja" },
      { time: "18.30", title: "Jamuan malam", note: "Paviliun Daun" },
      { time: "20.00", title: "Dansa pertama" },
    ] },
    dressCode: { note: "Formal malam. Hijau tua, hitam, dan sentuhan jingga atau merah dipersilakan.", colors: ["#0f2a1e", "#0b100d", "#ef8a2c", "#c8202a"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-08-21T16:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Hendra Wiyono", "Kel. Besar Bpk. Robert Sembiring"] },
    travel: { note: "Untuk tamu dari luar Bali, berikut pilihan dekat lokasi.", items: [
      { name: "Penginapan di Sayan & Kedewatan", detail: "± 5 menit dari lokasi · banyak vila kecil" },
      { name: "Shuttle tamu", detail: "Dari Pasar Ubud pukul 15.00 dan 15.30 WITA" },
    ] },
    faq: { items: [
      { q: "Acaranya di luar ruangan?", a: "Upacara di taman terbuka, jamuan malam di paviliun beratap. Bawa selendang tipis untuk udara malam." },
      { q: "Boleh membawa anak?", a: "Tentu, anak-anak sangat diterima." },
    ] },
  },
});

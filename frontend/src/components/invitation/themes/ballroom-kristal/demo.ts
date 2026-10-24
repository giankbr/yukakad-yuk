import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Vivian", groom: "Raymond",
    brideFull: "Vivian Angelina Hartanto, B.Arch.", groomFull: "Raymond Christopher Wijaya, M.B.A.",
    brideParents: "Putri dari\nBapak Hendra Hartanto & Ibu Lily Setiawati", groomParents: "Putra dari\nBapak Antonius Wijaya & Ibu Maria Susanti",
    bridePhoto: "/themes/img/a77.webp", groomPhoto: "/themes/img/a76.webp",
    note: "Di bawah cahaya lampu kristal, kami ingin merayakan awal yang baru bersama orang-orang terkasih.",
  },
  eventLabel: "Pernikahan",
  date: "2027-10-16T10:00:00+07:00",
  place: "Grand Crystal Ballroom, The Aurelia",
  address: "Jl. Mayjen Sungkono No. 120, Dukuh Pakis, Surabaya",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2018", title: "Pesta Dansa Kampus", body: "Raymond menginjak kaki Vivian di lantai dansa malam perpisahan angkatan. Permintaan maafnya berlanjut jadi secangkir kopi." },
    { date: "2023", title: "Jarak & Kepulangan", body: "Dua tahun berbeda kota, ratusan panggilan video, dan satu tiket pulang yang tidak pernah ditukar lagi." },
    { date: "2026", title: "Sebuah Pertanyaan", body: "Di bawah lampu gantung rumah keluarga, Raymond berlutut. Jawabannya, tentu saja, iya." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-10-16T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "Kapel Santa Cecilia", address: "Jl. Raya Darmo Permai Selatan No. 2, Pradah Kalikendal, Surabaya" },
    { name: "Resepsi Malam", date: "2027-10-16T18:30:00+07:00", time: "18.30 – 21.30 WIB", venue: "Grand Crystal Ballroom, The Aurelia", address: "Jl. Mayjen Sungkono No. 120, Dukuh Pakis, Surabaya" },
  ],
  gallery: ["/themes/img/a131.webp", "/themes/img/a77.webp", "/themes/img/a76.webp", "/themes/img/a122.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "088 123 4567", account_name: "Vivian Angelina Hartanto" },
    { id: "demo-kado", type: "address", address: "Jl. Raya Darmo Harapan IV No. 18, Sukomanunggal, Surabaya 60187" },
  ],
  guestName: "Bapak Stefanus Gunawan & Partner",
  guestTable: "Meja 12",
  extras: {
    rundown: { items: [
      { time: "18.30", title: "Resepsi dibuka", note: "Welcome drink & musik kamar" },
      { time: "19.15", title: "Grand entrance & first dance" },
      { time: "19.45", title: "Jamuan makan malam", note: "Hidangan lima menu" },
      { time: "21.00", title: "Pemotongan kue & dansa bersama" },
    ] },
    dressCode: { note: "Black tie optional. Nuansa sampanye, gading, dan emas.", colors: ["#e8d6b5", "#faf5ec", "#b8914a", "#3a2c22"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Hendra Hartanto", "Kel. Besar Antonius Wijaya"] },
    faq: { items: [
      { q: "Apakah ada area parkir?", a: "Tersedia valet dan parkir basement The Aurelia untuk tamu undangan." },
      { q: "Sampai jam berapa acaranya?", a: "Resepsi berlangsung hingga pukul 21.30 WIB, dilanjutkan dansa bersama." },
    ] },
  },
});

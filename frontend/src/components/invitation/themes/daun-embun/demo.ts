import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Salsabila", groom: "Fathan",
    brideFull: "Salsabila Nurul Fitri, S.Si.", groomFull: "Fathan Ar-Rasyid, S.Hut.",
    brideParents: "Putri kedua dari\nBapak Ir. H. Endang Suherman & Ibu Hj. Nia Kurniasih", groomParents: "Putra sulung dari\nBapak H. Rahmat Hidayat & Ibu Dewi Sartika",
    note: "Seperti embun yang jatuh pelan di ujung daun setiap pagi, semoga rumah kami selalu disegarkan oleh syukur dan doa yang tak pernah kering.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-03-13T08:00:00+07:00",
  place: "Masjid Raya Bogor",
  address: "Jl. Raya Pajajaran No. 10, Bantarjati, Bogor Utara, Kota Bogor",
  stories: [
    { date: "2022", title: "Satu Kebun Raya", body: "Kami bertemu sebagai relawan pendataan tanaman di Kebun Raya Bogor; ia mencatat pakis, aku memotret daun calathea." },
    { date: "2025", title: "Ta'aruf", body: "Lewat guru ngaji keluarga, kami bertukar biodata dan berproses dengan pendampingan kedua orang tua." },
    { date: "November 2026", title: "Khitbah", body: "Keluarga Fathan datang ke Bantarjati di pagi yang gerimis. Lamaran diterima dengan haru dan teh hangat." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-03-13T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Raya Bogor", address: "Jl. Raya Pajajaran No. 10, Bantarjati, Bogor Utara, Kota Bogor" },
    { name: "Walimatul 'Ursy", date: "2027-03-13T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Kemuning Gading", address: "Jl. Pangrango No. 34, Babakan, Bogor Tengah, Kota Bogor" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7211 0458 3390", account_name: "Salsabila Nurul Fitri" },
    { id: "demo-bjb", type: "bank", bank_name: "BJB Syariah", account_number: "0076 1123 8801", account_name: "Fathan Ar-Rasyid" },
    { id: "demo-kado", type: "address", address: "Jl. Bangbarung Raya No. 21, Bantarjati, Bogor Utara, Kota Bogor 16153", account_name: "Keluarga H. Endang Suherman" },
  ],
  guestName: "Ibu Hj. Aisyah Rahmawati & Keluarga",
  guestTable: "Meja Pakis 3",
  extras: {
    quote: { text: "Dan Dialah yang menurunkan air dari langit, lalu Kami tumbuhkan dengan air itu segala macam tumbuh-tumbuhan.", source: "QS. Al-An'am: 99" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "09.00", title: "Tausiyah pernikahan" },
      { time: "11.00", title: "Walimah dibuka", note: "Area tamu putra & putri terpisah" },
      { time: "13.30", title: "Doa penutup" },
    ] },
    dressCode: { note: "Busana muslim santun bernuansa pagi: hijau daun, putih embun, dan sage lembut.", colors: ["#f4f8f1", "#a9cf9a", "#3f7f52", "#1f4a36"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Endang Suherman", "Kel. Besar H. Rahmat Hidayat"] },
    faq: { items: [
      { q: "Apakah area tamu putra dan putri dipisah?", a: "Ya, walimah menggunakan ruang terpisah dengan tirai hijau untuk tamu putra dan putri." },
      { q: "Apakah ada tempat salat?", a: "Tersedia musala dan tempat wudu di sayap timur gedung." },
    ] },
  },
});

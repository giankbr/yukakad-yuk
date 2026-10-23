import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Salsabila", groom: "Fathan",
    brideFull: "Salsabila Khairunnisa, S.Farm.", groomFull: "Muhammad Fathan Al-Ghifari, S.Kom.",
    brideParents: "Putri kedua dari\nBapak H. Ahmad Zainuddin & Ibu Hj. Nurul Hidayah", groomParents: "Putra pertama dari\nBapak Ir. Rahmat Hidayat & Ibu Siti Maryam",
    note: "Seperti mawar putih yang tumbuh perlahan di taman, kami belajar bahwa cinta yang diridai Allah tumbuh dengan sabar dan dirawat dengan doa.",
  },
  eventLabel: "Pernikahan",
  date: "2027-05-22T08:00:00+07:00",
  place: "Gedung Wanita Kencana Bogor",
  address: "Jl. Raya Pajajaran No. 88, Bantarjati, Bogor Utara, Kota Bogor",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2023", title: "Satu Majelis", body: "Kami sama-sama menjadi relawan kajian remaja di masjid kampus, tanpa banyak bicara, hanya saling menghormati dari kejauhan." },
    { date: "Ramadan 2026", title: "Ta'aruf", body: "Melalui perantara guru ngaji kami, biodata bertukar dan istikharah dilakukan. Hati kami sama-sama dimantapkan." },
    { date: "Desember 2026", title: "Khitbah", body: "Keluarga Fathan datang bersilaturahmi ke Bogor membawa niat baik, disambut hangat oleh keluarga besar Salsabila." },
    { date: "Mei 2027", title: "Akad", body: "Insyaallah kami menyempurnakan separuh agama, memohon doa restu agar menjadi keluarga sakinah, mawaddah, warahmah." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-22T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Raya Al-Musyawarah", address: "Jl. Raya Pajajaran No. 10, Baranangsiang, Bogor Timur, Kota Bogor" },
    { name: "Walimatul 'Ursy", date: "2027-05-22T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Wanita Kencana Bogor", address: "Jl. Raya Pajajaran No. 88, Bantarjati, Bogor Utara, Kota Bogor" },
  ],
  gallery: ["/themes/img/a26.webp", "/themes/img/a99.webp", "/themes/img/r44.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7134 2205 27", account_name: "Salsabila Khairunnisa" },
    { id: "demo-muamalat", type: "bank", bank_name: "Muamalat", account_number: "3310 0452 18", account_name: "Muhammad Fathan Al-Ghifari" },
    { id: "demo-kado", type: "address", address: "Jl. Kenari II No. 7, Tegallega, Bogor Tengah, Kota Bogor 16129" },
  ],
  guestName: "Ibu Hj. Aminah Fauziah & Keluarga",
  guestTable: "Meja Melati 3",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat kebesaran Allah.", source: "QS. Adz-Dzariyat: 49" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu", note: "Area tamu putra dan putri dipisah dengan tabir bunga" },
      { time: "11.20", title: "Tilawah & tausiyah singkat" },
      { time: "12.00", title: "Jamuan & ramah tamah" },
      { time: "13.30", title: "Doa penutup" },
    ] },
    dressCode: { note: "Busana muslim yang santun. Nuansa putih gading, krem, dan hijau tua dipersilakan.", colors: ["#f8f4ea", "#e9e1cd", "#2f5a40", "#17301f"] },
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Ahmad Zainuddin", "Kel. Besar Ir. Rahmat Hidayat"] },
  },
});

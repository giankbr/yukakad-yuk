import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Lintang", groom: "",
    brideFull: "Btari Lintang Ayuningtyas",
    brideParents: "Putri pertama dari Bapak Dimas Wicaksono & Ibu Rahayu Ningsih",
    note: "3,2 kg · 49 cm · pukul 05.42 WIB",
  },
  eventLabel: "Syukuran Kelahiran",
  date: "2027-02-13T10:00:00+07:00",
  place: "Kediaman Keluarga Wicaksono",
  address: "Perum Griya Asri Blok C-14, Jl. Kaliurang Km 9, Ngaglik, Sleman, Yogyakarta",
  story: { title: "Menanti Lintang", body: "" },
  stories: [
    { date: "Mei 2026", title: "Kabar bahagia", body: "Dua garis kecil di pagi hari yang membuat Ayah dan Ibu menangis bahagia di dapur." },
    { date: "September 2026", title: "Tendangan pertama", body: "Terasa saat Ayah sedang membacakan dongeng. Sejak itu dongengnya tidak pernah absen." },
    { date: "9 Januari 2027", title: "Halo, Lintang!", body: "Lahir saat fajar, ketika bintang terakhir masih terlihat di langit Kaliurang." },
  ],
  events: [
    { name: "Syukuran & Doa Bersama", date: "2027-02-13T10:00:00+07:00", time: "10.00 – 13.00 WIB", venue: "Kediaman Keluarga Wicaksono", address: "Perum Griya Asri Blok C-14, Jl. Kaliurang Km 9, Ngaglik, Sleman, Yogyakarta" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BRI", account_number: "0029 0110 4387 503", account_name: "Rahayu Ningsih" },
    { id: "demo-kado", type: "address", address: "Perum Griya Asri Blok C-14, Jl. Kaliurang Km 9, Ngaglik, Sleman, Yogyakarta 55581" },
  ],
  guestName: "Ibu Sulastri & Keluarga",
  guestTable: "",
  extras: {
    child: {
      name: "Btari Lintang Ayuningtyas", nickname: "Lintang", birthDate: "2027-01-09T05:42:00+07:00",
      parents: "Putri pertama dari Bapak Dimas Wicaksono & Ibu Rahayu Ningsih",
      meaning: "Btari berarti putri yang dimuliakan, Lintang berarti bintang, dan Ayuningtyas berarti hati yang indah. Semoga ia menjadi bintang kecil yang menerangi keluarga dengan hati yang lembut.",
    },
    rundown: { items: [
      { time: "10.00", title: "Penyambutan tamu", note: "Teh hangat & jajan pasar" },
      { time: "10.30", title: "Doa bersama untuk Lintang" },
      { time: "11.15", title: "Kenalan dengan Lintang", note: "Bergiliran, mohon cuci tangan dulu" },
      { time: "11.45", title: "Makan siang bersama" },
    ] },
    dressCode: { note: "Nuansa lembut: hijau sage, krem, atau kuning mentega.", colors: ["#9fb592", "#f7f1e1", "#f3d98b", "#efc3b4"] },
    guestPass: {},
    rsvpDietary: {},
    family: { title: "Turut berbahagia", names: ["Eyang Kakung & Eyang Putri Wicaksono", "Kakek & Nenek Ningsih", "Keluarga Besar Trah Atmodiharjo"] },
    wishlist: { note: "Doa Bapak/Ibu sudah lebih dari cukup. Bila berkenan, ini beberapa kebutuhan Lintang.", items: [
      { id: "w1", name: "Gendongan bayi (ukuran newborn)", price: "± Rp350.000" },
      { id: "w2", name: "Set popok kain & bedong", price: "± Rp180.000", claimed_by: "Tante Wulan" },
      { id: "w3", name: "Buku kain untuk bayi", price: "± Rp95.000" },
    ] },
    faq: { items: [
      { q: "Bolehkah menggendong Lintang?", a: "Boleh, bergantian dan setelah mencuci tangan. Mohon tidak datang bila sedang flu." },
      { q: "Apakah ada tempat parkir?", a: "Mobil dapat parkir di lapangan perumahan, sekitar 50 meter dari rumah." },
    ] },
  },
});

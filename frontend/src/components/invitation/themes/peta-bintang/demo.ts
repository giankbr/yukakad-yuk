import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Alya", groom: "Raditya",
    brideFull: "Alya Paramitha Santoso, S.Si.", groomFull: "Raditya Pratama Wijaya, M.T.",
    brideParents: "Putri kedua dari\nBapak Hendra Santoso & Ibu Maria Lestari", groomParents: "Putra pertama dari\nBapak Antonius Wijaya & Ibu Rosalina Dewi",
    bridePhoto: "/themes/img/r107.webp", groomPhoto: "/themes/img/r106.webp",
    note: "Di bawah langit yang sama, kami belajar membaca arah pulang: satu sama lain.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-07T19:30:00+07:00",
  place: "Pendapa Langit Menoreh",
  address: "Jl. Nanggulan–Mendut Km 6, Kembang, Nanggulan, Kulon Progo, DI Yogyakarta",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "Juli 2019", title: "Malam di Penanjakan", body: "Dua rombongan pengamat bintang berbagi satu teleskop di Bromo. Alya menunjuk Skorpio, Radit malah sibuk memotret Alya." },
    { date: "2021 – 2024", title: "Bandung – Jakarta", body: "Jarak dua kota kami isi dengan telepon tiap malam dan aplikasi peta langit yang sama, supaya selalu melihat bintang yang sama." },
    { date: "Agustus 2026", title: "Di Bawah Bima Sakti", body: "Di Pantai Wediombo, tepat saat galaksi melintang di atas kepala, Radit bertanya dan Alya menjawab ya." },
  ],
  events: [
    { name: "Upacara Janji Suci", date: "2027-08-07T16:00:00+07:00", time: "16.00 – 17.30 WIB", venue: "Taman Bukit Langit Menoreh", address: "Jl. Nanggulan–Mendut Km 6, Kembang, Nanggulan, Kulon Progo, DI Yogyakarta" },
    { name: "Resepsi di Bawah Bintang", date: "2027-08-07T19:30:00+07:00", time: "19.30 – 22.00 WIB", venue: "Pendapa Langit Menoreh", address: "Jl. Nanggulan–Mendut Km 6, Kembang, Nanggulan, Kulon Progo, DI Yogyakarta" },
  ],
  gallery: ["/themes/img/a110.webp", "/themes/img/r81.webp", "/themes/img/a122.webp", "/themes/img/r10.webp", "/themes/img/r38.webp", "/themes/img/r102.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0372 1908 77", account_name: "Alya Paramitha Santoso" },
    { id: "demo-ovo", type: "ewallet", ewallet_provider: "ovo", ewallet_number: "0811 2803 1907", account_name: "Raditya Pratama Wijaya" },
    { id: "demo-kado", type: "address", address: "Jl. Kaliurang Km 7,5, Gg. Bintang No. 12, Sleman, DI Yogyakarta 55581" },
  ],
  guestName: "Bapak Yohanes Prasetyo & Keluarga",
  guestTable: "Orion 3",
  extras: {
    quote: { text: "Bintang-bintang tidak pernah tergesa, namun selalu tiba tepat pada malamnya. Begitu pula kita.", source: "Catatan Alya & Radit" },
    rundown: { items: [
      { time: "19.30", title: "Kedatangan tamu", note: "Minuman hangat di taman" },
      { time: "20.00", title: "Kirab pengantin", note: "Lampu taman diredupkan" },
      { time: "20.30", title: "Makan malam & cerita" },
      { time: "21.15", title: "Melihat bintang bersama", note: "Teleskop disiapkan di halaman" },
    ] },
    dressCode: { note: "Nuansa langit malam: biru tua, krem, dan sentuhan emas. Bawa jaket tipis, malam di Menoreh sejuk.", colors: ["#13224a", "#efe5cf", "#c9a45a", "#5a6f9e"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-08-07T16:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Hendra Santoso", "Kel. Besar Bpk. Antonius Wijaya", "Komunitas Astronomi Amatir Jogja"] },
    faq: { items: [
      { q: "Acaranya di luar ruangan?", a: "Resepsi di pendapa terbuka. Bila hujan, tirai samping ditutup dan acara tetap berjalan." },
      { q: "Boleh membawa anak?", a: "Tentu. Ada sudut teleskop kecil untuk anak-anak bersama pemandu." },
    ] },
  },
});

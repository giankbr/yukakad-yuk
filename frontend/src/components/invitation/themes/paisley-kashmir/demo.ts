import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Zahira", groom: "Ilham",
    brideFull: "Zahira Putri Ramadhani, S.Ds.", groomFull: "Muhammad Ilham Prasetyo, S.E.",
    brideParents: "Putri pertama dari\nBapak H. Rahmat Hidayat & Ibu Hj. Siti Khadijah", groomParents: "Putra kedua dari\nBapak Drs. Bambang Prasetyo & Ibu Endang Lestari",
    bridePhoto: "/themes/img/a28.webp", groomPhoto: "/themes/img/a29.webp",
    note: "Dua helai benang yang berbeda warna, ditenun sabar menjadi satu kain yang hangat.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-06-12T08:00:00+07:00",
  place: "Balai Sudirman",
  address: "Jl. Dr. Saharjo No. 268, Menteng Dalam, Tebet, Jakarta Selatan",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2019", title: "Pameran Wastra", body: "Zahira menjaga stan selendang tenun di sebuah pameran kriya di Jakarta. Ilham datang mencari hadiah untuk ibunya." },
    { date: "2023", title: "Ta'aruf", body: "Bertahun kemudian kami dipertemukan lagi lewat sahabat keluarga, lalu berta'aruf dengan niat yang baik." },
    { date: "2026", title: "Lamaran", body: "Keluarga Ilham datang melamar membawa seserahan, termasuk selendang bermotif boteh pilihan ibunda." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-12T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Al-Azhar", address: "Jl. Sisingamangaraja, Kebayoran Baru, Jakarta Selatan" },
    { name: "Walimatul 'Ursy", date: "2027-06-12T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Balai Sudirman", address: "Jl. Dr. Saharjo No. 268, Menteng Dalam, Tebet, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/a28.webp", "/themes/img/a27.webp", "/themes/img/a29.webp", "/themes/img/a26.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7203 5518 40", account_name: "Zahira Putri Ramadhani" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1270 0098 3321", account_name: "Muhammad Ilham Prasetyo" },
    { id: "demo-kado", type: "address", address: "Jl. Tebet Barat Dalam VI No. 21, Tebet, Jakarta Selatan 12810" },
  ],
  guestName: "Ibu Hj. Maryam Syarif & Keluarga",
  guestTable: "Meja Kunyit 5",
  extras: {
    quote: { text: "Mereka adalah pakaian bagimu, dan kamu pun adalah pakaian bagi mereka.", source: "QS. Al-Baqarah: 187" },
    rundown: { items: [
      { time: "08.00", title: "Pembacaan ayat suci Al-Qur'an" },
      { time: "08.20", title: "Ijab kabul", note: "Keluarga inti & saksi" },
      { time: "08.50", title: "Khutbah nikah & doa" },
      { time: "11.00", title: "Walimah dibuka", note: "Jamuan & ramah tamah" },
    ] },
    dressCode: { note: "Busana muslim santun bernuansa kunyit, merah bata, atau hijau tua. Selendang bermotif sangat dipersilakan.", colors: ["#d9962c", "#a3302a", "#1f4b3a", "#f2e7cf"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Rahmat Hidayat", "Kel. Besar Drs. Bambang Prasetyo"] },
  },
});

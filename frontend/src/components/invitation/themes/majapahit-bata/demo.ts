import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kartika", groom: "Bagas",
    brideFull: "Ayu Kartika Ningrum, S.Pd.", groomFull: "Bagas Wicaksono Putra, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Suharto Wiryo & Ibu Hj. Sri Wahyuni", groomParents: "Putra sulung dari\nBapak Drs. Imam Basuki & Ibu Endang Lestari",
    bridePhoto: "/themes/img/a28.webp", groomPhoto: "/themes/img/a29.webp",
    note: "Seperti bata yang direkatkan satu demi satu, kami ingin membangun rumah yang kokoh, hangat, dan bertahan lama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-14T08:00:00+07:00",
  place: "Pendopo Agung Trowulan",
  address: "Jl. Raya Trowulan, Trowulan, Kabupaten Mojokerto, Jawa Timur",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2018", title: "Kuliah Lapangan di Trowulan", body: "Kartika mahasiswi pendidikan sejarah, Bagas relawan pemandu di situs Candi Tikus. Kami berkenalan di antara petak bata kuno." },
    { date: "2022", title: "Pulang ke Mojokerto", body: "Setelah merantau ke Surabaya, kami sama-sama kembali: Kartika mengajar di SMA, Bagas merintis usaha bata ekspos di Jatisari." },
    { date: "2026", title: "Lamaran di Kolam Segaran", body: "Disaksikan dua keluarga, Bagas datang melamar pada sore yang teduh di tepi Kolam Segaran." },
    { date: "2027", title: "Membangun Rumah Bersama", body: "Dengan restu orang tua, kami menyempurnakan separuh agama dan memulai rumah tangga di kota kelahiran kami." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-14T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Al-Fattah", address: "Jl. KH. Hasyim Asy'ari, Kauman, Prajurit Kulon, Kota Mojokerto" },
    { name: "Resepsi Pernikahan", date: "2027-08-14T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Pendopo Agung Trowulan", address: "Jl. Raya Trowulan, Trowulan, Kabupaten Mojokerto, Jawa Timur" },
  ],
  gallery: ["/themes/img/a43.webp", "/themes/img/a50.webp", "/themes/img/a27.webp", "/themes/img/a38.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0451 0102 7781 503", account_name: "Ayu Kartika Ningrum" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "142 00 1987 6543", account_name: "Bagas Wicaksono Putra" },
    { id: "demo-kado", type: "address", address: "Dusun Kedaton RT 02 RW 03, Desa Sentonorejo, Kec. Trowulan, Kab. Mojokerto 61362" },
  ],
  guestName: "Bapak H. Mulyono & Keluarga",
  guestTable: "Pendopo 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Kirab pengantin memasuki pendopo", note: "Diiringi hadrah" },
      { time: "11.30", title: "Sambutan keluarga & doa" },
      { time: "12.00", title: "Ramah tamah", note: "Hidangan khas Mojokerto" },
      { time: "13.00", title: "Foto bersama", note: "Per rombongan" },
    ] },
    dressCode: { note: "Batik atau busana muslim. Nuansa bata, krem, dan hijau kolam dipersilakan.", colors: ["#9c3d29", "#efe0c8", "#3f6f68", "#c98a45"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-08-14T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. H. Suharto Wiryo", "Kel. Besar Bpk. Drs. Imam Basuki"] },
    travel: { note: "Untuk tamu dari luar kota, berikut pilihan terdekat.", items: [
      { name: "Stasiun Mojokerto", detail: "± 13 km dari Trowulan · taksi daring tersedia" },
      { name: "Parkir pendopo", detail: "Halaman Pendopo Agung dan lapangan sebelah selatan" },
    ] },
  },
});

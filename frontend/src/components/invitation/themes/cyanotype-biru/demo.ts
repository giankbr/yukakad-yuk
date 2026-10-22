import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kirana", groom: "Rafi",
    brideFull: "Kirana Ayu Lestari, S.Si.", groomFull: "Muhammad Rafi Hidayat, S.Hut.",
    brideParents: "Putri kedua dari\nBapak Ir. Asep Sunarya & Ibu Euis Komalasari",
    groomParents: "Putra pertama dari\nBapak Dedi Hidayat & Ibu Siti Nurjanah",
    note: "Seperti daun yang dijemur di bawah matahari, kami belajar sabar menunggu sampai jejaknya tercetak. Kini kami ingin mencetak lembar baru bersama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-12T08:00:00+07:00",
  place: "Pendopo Taman Kenari",
  address: "Jl. Kenari No. 8, Paledang, Bogor Tengah, Kota Bogor",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2020", title: "Lembar Herbarium", body: "Kirana sedang menata spesimen paku-pakuan di herbarium kebun raya ketika Rafi datang membawa sampel yang salah label. Mereka menertawakan kesalahan itu sampai sore." },
    { date: "2023", title: "Musim Kemarau", body: "Rafi mengajak Kirana mencoba cetak cyanotype di halaman rumahnya. Cetakan pertama gagal, yang kedua miring, yang ketiga mereka bingkai berdua." },
    { date: "Januari 2027", title: "Lamaran", body: "Di bawah pohon kenari yang sama, keluarga Rafi datang bersilaturahmi dan meminang Kirana dengan restu kedua orang tua." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-12T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Masjid Raya Bogor", address: "Jl. Raya Pajajaran No. 10, Baranangsiang, Bogor Timur, Kota Bogor" },
    { name: "Resepsi", date: "2027-06-12T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Pendopo Taman Kenari", address: "Jl. Kenari No. 8, Paledang, Bogor Tengah, Kota Bogor" },
  ],
  gallery: ["/themes/img/r89.webp", "/themes/img/a30.webp", "/themes/img/r102.webp", "/themes/img/a140.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7134 5520 98", account_name: "Kirana Ayu Lestari" },
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0661 2398 41", account_name: "Muhammad Rafi Hidayat" },
    { id: "demo-kado", type: "address", address: "Jl. Pangrango No. 14, Babakan, Bogor Tengah, Kota Bogor 16128" },
  ],
  guestName: "Ibu Dr. Wulan Purnamasari & Keluarga",
  guestTable: "Meja Paku 3",
  extras: {
    quote: { text: "Mahasuci (Allah) yang telah menciptakan semuanya berpasang-pasangan, baik dari apa yang ditumbuhkan oleh bumi dan dari diri mereka sendiri, maupun dari apa yang tidak mereka ketahui.", source: "QS. Yasin: 36" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu", note: "Taman depan pendopo" },
      { time: "11.30", title: "Kirab pengantin & doa bersama" },
      { time: "12.00", title: "Ramah tamah", note: "Hidangan Sunda & prasmanan" },
      { time: "13.00", title: "Foto bersama keluarga & sahabat" },
    ] },
    dressCode: { note: "Nuansa biru prusia, biru muda, dan putih. Kebaya atau batik dipersilakan.", colors: ["#1f4a80", "#5a83b4", "#c9d8e8", "#eef1ee"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-06-12T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Ir. Asep Sunarya", "Kel. Besar Bpk. Dedi Hidayat"] },
    travel: { note: "Untuk tamu dari luar kota, berikut pilihan menginap di sekitar Kebun Raya.", items: [
      { name: "Penginapan di sekitar Jl. Pajajaran", detail: "± 1 km dari masjid" },
      { name: "KRL Commuter Line", detail: "Turun di Stasiun Bogor, 10 menit dengan angkot ke pendopo" },
    ] },
    wishlist: { items: [
      { id: "w1", name: "Bingkai kayu untuk cetakan", price: "± Rp450.000" },
      { id: "w2", name: "Set gelas teh kaca", price: "± Rp380.000", claimed_by: "Teh Rani" },
      { id: "w3", name: "Tabungan rumah pertama", price: "Bebas" },
    ] },
    faq: { items: [
      { q: "Boleh membawa anak?", a: "Tentu, anak-anak sangat diterima. Area taman aman untuk bermain." },
      { q: "Apakah tersedia parkir?", a: "Parkir tersedia di halaman pendopo dan sepanjang Jl. Kenari." },
    ] },
  },
});

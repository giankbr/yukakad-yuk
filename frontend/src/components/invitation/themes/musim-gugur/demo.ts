import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Anin", groom: "Bagas",
    brideFull: "Theresia Anindya Putri, M.Sc.", groomFull: "Yohanes Bagas Prasetyo, M.Eng.",
    brideParents: "Putri pertama dari\nBapak Fransiskus Xaverius Suharno & Ibu Maria Goretti Endang Lestari",
    groomParents: "Putra ketiga dari\nBapak Antonius Sugiyanto & Ibu Caecilia Sri Wahyuni",
    note: "Kami jatuh cinta di musim ketika daun-daun berguguran. Ternyata yang gugur bukan akhir, melainkan awal dari musim yang baru.",
  },
  eventLabel: "Pernikahan",
  date: "2027-10-23T10:00:00+07:00",
  place: "Omah Kenari Kaliurang",
  address: "Jl. Kaliurang Km 22, Hargobinangun, Pakem, Kabupaten Sleman, DI Yogyakarta",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "Oktober 2021", title: "Musim Gugur Pertama", body: "Dua mahasiswa Indonesia di Freiburg bertemu di misa bahasa Indonesia. Sepulang gereja mereka berjalan menyusuri taman yang dipenuhi daun maple jingga." },
    { date: "2024", title: "Pulang ke Jogja", body: "Setelah lulus, Anin dan Bagas sama-sama kembali ke Yogyakarta. Setiap Oktober mereka tetap merayakan musim gugur dengan secangkir wedang jahe." },
    { date: "April 2027", title: "Lamaran", body: "Di teras rumah keluarga Anin, Bagas menyerahkan sehelai daun maple kering yang ia simpan sejak 2021, terselip di dalam kotak cincin." },
  ],
  events: [
    { name: "Sakramen Perkawinan", date: "2027-10-23T10:00:00+07:00", time: "10.00 – 12.00 WIB", venue: "Gereja Hati Kudus Tuhan Yesus Pugeran", address: "Jl. Suryaden No. 63, Suryodiningratan, Mantrijeron, Kota Yogyakarta" },
    { name: "Resepsi", date: "2027-10-23T17:00:00+07:00", time: "17.00 – 20.00 WIB", venue: "Omah Kenari Kaliurang", address: "Jl. Kaliurang Km 22, Hargobinangun, Pakem, Kabupaten Sleman, DI Yogyakarta" },
  ],
  gallery: ["/themes/img/a132.webp", "/themes/img/a124.webp", "/themes/img/r84.webp", "/themes/img/r86.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "4451 0927 33", account_name: "Theresia Anindya Putri" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0029 0110 4471 508", account_name: "Yohanes Bagas Prasetyo" },
    { id: "demo-kado", type: "address", address: "Jl. Kenanga No. 7, Condongcatur, Depok, Kabupaten Sleman, DI Yogyakarta 55283" },
  ],
  guestName: "Bapak Ignatius Hendro & Keluarga",
  guestTable: "Meja Maple 6",
  extras: {
    quote: { text: "Kasih itu sabar; kasih itu murah hati; ia tidak cemburu. Ia menutupi segala sesuatu, percaya segala sesuatu, mengharapkan segala sesuatu, sabar menanggung segala sesuatu.", source: "1 Korintus 13:4, 7" },
    rundown: { items: [
      { time: "17.00", title: "Penyambutan tamu", note: "Teh jahe & kue hangat di taman" },
      { time: "17.30", title: "Doa syukur & sambutan keluarga" },
      { time: "18.00", title: "Santap malam", note: "Hidangan Jawa & barat" },
      { time: "19.15", title: "Foto bersama keluarga & sahabat" },
    ] },
    dressCode: { note: "Nuansa musim gugur: jingga bata, kuning mustard, cokelat, dan hijau zaitun. Bawa jaket tipis, udara Kaliurang sejuk.", colors: ["#b4462a", "#d9832b", "#e2b33c", "#7a4a2a"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-10-23T10:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. F.X. Suharno", "Kel. Besar Bpk. Antonius Sugiyanto"] },
    travel: { note: "Untuk tamu dari luar kota, berikut pilihan menginap di kawasan Kaliurang.", items: [
      { name: "Penginapan di Jl. Kaliurang atas", detail: "± 1 km dari Omah Kenari" },
      { name: "Shuttle tamu", detail: "Dari gereja ke Kaliurang pukul 15.30 WIB, mohon konfirmasi" },
    ] },
    wishlist: { items: [
      { id: "w1", name: "Selimut rajut wol", price: "± Rp600.000" },
      { id: "w2", name: "Set teko keramik & cangkir", price: "± Rp550.000", claimed_by: "Mbak Sekar" },
      { id: "w3", name: "Tabungan rumah pertama", price: "Bebas" },
    ] },
    faq: { items: [
      { q: "Apakah tamu boleh mengikuti Misa?", a: "Tentu. Misa Sakramen Perkawinan terbuka untuk semua tamu, mohon datang 15 menit lebih awal." },
      { q: "Apakah udaranya dingin?", a: "Kaliurang sejuk di sore hari, sekitar 20 derajat. Kami sarankan membawa jaket atau syal." },
    ] },
  },
});

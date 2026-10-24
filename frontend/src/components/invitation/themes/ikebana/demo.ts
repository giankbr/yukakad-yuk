import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Kinanti", groom: "Arya",
    brideFull: "Kinanti Larasati", groomFull: "Arya Pradipta Nugraha",
    brideParents: "Putri dari\nBapak Hendro Wibisono & Ibu Ratih Kusumaningrum", groomParents: "Putra dari\nBapak Gunawan Nugraha & Ibu Melani Santoso",
    bridePhoto: "/themes/img/a77.webp", groomPhoto: "/themes/img/a76.webp",
    note: "Sedikit, tetapi cukup. Ruang kosong pun bagian dari keindahan.",
  },
  eventLabel: "Pernikahan",
  date: "2027-04-24T16:00:00+07:00",
  place: "Plataran Menteng",
  address: "Jl. HOS. Cokroaminoto No. 42, Menteng, Jakarta Pusat",
  stories: [
    { date: "2021", title: "Kelas Hari Minggu", body: "Arya ikut kelas merangkai bunga karena kalah taruhan dengan adiknya. Kinanti pengajarnya, dan rangkaian pertama Arya miring ke mana-mana." },
    { date: "2023", title: "Musim yang Sama", body: "Dua tahun kemudian Arya masih datang setiap Minggu. Rangkaiannya sudah lurus, alasannya datang yang berubah." },
    { date: "2026", title: "Satu Vas", body: "Di sebuah sore yang tenang, Arya menyelipkan cincin di antara tangkai iris. Kinanti menjawab sebelum rangkaiannya selesai." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-04-24T16:00:00+07:00", time: "16.00 – 17.00 WIB", venue: "Plataran Menteng, Taman Belakang", address: "Jl. HOS. Cokroaminoto No. 42, Menteng, Jakarta Pusat" },
    { name: "Jamuan Malam", date: "2027-04-24T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Plataran Menteng, Pendopo", address: "Jl. HOS. Cokroaminoto No. 42, Menteng, Jakarta Pusat" },
  ],
  gallery: ["/themes/img/a22.webp", "/themes/img/a77.webp", "/themes/img/a76.webp", "/themes/img/a30.webp", "/themes/img/a116.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "5271 0388 14", account_name: "Kinanti Larasati" },
    { id: "demo-kado", type: "address", address: "Jl. Kemang Timur No. 7B, Bangka, Mampang Prapatan, Jakarta Selatan 12730" },
  ],
  guestName: "Ibu Maya Anggraini & Partner",
  guestTable: "Meja Iris 2",
  extras: {
    quote: { text: "Bunga tidak tergesa untuk mekar. Ia menunggu musimnya, lalu mekar dengan tenang.", source: "Catatan kelas merangkai bunga" },
    rundown: { items: [
      { time: "16.00", title: "Upacara pernikahan", note: "Taman belakang, mohon hadir 15 menit lebih awal" },
      { time: "17.00", title: "Teh sore & foto bersama" },
      { time: "18.30", title: "Jamuan malam" },
      { time: "20.00", title: "Dansa pertama" },
    ] },
    dressCode: { note: "Semi formal. Warna lembut: gading, abu batu, ungu iris, dan hijau daun.", colors: ["#f1ebde", "#a8a39a", "#5a4a96", "#6f8f5a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Keluarga Hendro Wibisono", "Keluarga Gunawan Nugraha"] },
  },
});

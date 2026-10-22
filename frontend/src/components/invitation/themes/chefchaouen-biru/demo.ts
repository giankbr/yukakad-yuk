import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Hana", groom: "Rasyid",
    brideFull: "Hana Salsabila Putri, M.A.", groomFull: "Rasyid Abdurrahman, Lc.",
    brideParents: "Putri sulung dari\nBapak H. Syarifuddin Lubis & Ibu Hj. Rosmawati", groomParents: "Putra ketiga dari\nBapak K.H. Abdul Hakim & Ibu Hj. Fatimah Az-Zahra",
    bridePhoto: "/themes/img/r100.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Kami pertama kali berpapasan di sebuah tangga biru yang curam, sama-sama tersesat mencari jalan pulang. Ternyata jalan pulang itu adalah satu sama lain.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-09-25T09:00:00+07:00",
  place: "Masjid Cut Meutia",
  address: "Jl. Cut Meutia No. 1, Gondangdia, Menteng, Jakarta Pusat",
  stories: [
    { date: "2023", title: "Tangga Biru", body: "Dalam program pertukaran studi bahasa Arab di Maroko, kami tersesat di lorong-lorong biru kota tua dan saling menunjukkan arah yang sama-sama salah." },
    { date: "2025", title: "Pulang ke Tanah Air", body: "Kembali ke Jakarta, kami dipertemukan lagi di kajian pekanan. Lewat ustazah pembimbing, kami memulai proses ta'aruf." },
    { date: "Februari 2027", title: "Khitbah", body: "Keluarga Rasyid datang ke rumah di Rawamangun. Lamaran diterima dengan teh mint dan doa bersama." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-25T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Masjid Cut Meutia", address: "Jl. Cut Meutia No. 1, Gondangdia, Menteng, Jakarta Pusat" },
    { name: "Walimatul 'Ursy", date: "2027-09-25T12:00:00+07:00", time: "12.00 – 15.00 WIB", venue: "Aula Riad Nila", address: "Jl. Kemang Selatan Raya No. 27, Bangka, Mampang Prapatan, Jakarta Selatan" },
  ],
  gallery: ["/themes/img/a31.webp", "/themes/img/a43.webp", "/themes/img/r75.webp", "/themes/img/r55.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7230 5511 0896", account_name: "Hana Salsabila Putri" },
    { id: "demo-muamalat", type: "bank", bank_name: "Muamalat", account_number: "3420 0112 75", account_name: "Rasyid Abdurrahman" },
    { id: "demo-kado", type: "address", address: "Jl. Balai Pustaka Timur No. 18, Rawamangun, Pulo Gadung, Jakarta Timur 13220", account_name: "Keluarga H. Syarifuddin Lubis" },
  ],
  guestName: "Bapak Dr. H. Ahmad Fauzi & Keluarga",
  guestTable: "Meja Biru 5",
  extras: {
    quote: { text: "Dan Allah menjadikan bagimu rumah-rumahmu sebagai tempat tinggal.", source: "QS. An-Nahl: 80" },
    rundown: { items: [
      { time: "12.00", title: "Penyambutan tamu", note: "Teh mint & kurma" },
      { time: "12.30", title: "Tausiyah walimah" },
      { time: "13.00", title: "Ramah tamah", note: "Hidangan Nusantara & Maghribi" },
      { time: "14.30", title: "Doa penutup" },
    ] },
    dressCode: { note: "Busana muslim santun bernuansa kota biru: biru kobalt, biru langit, putih kapur, dan aksen kuning.", colors: ["#24508f", "#7fb0e0", "#eef3f6", "#e8b33a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Syarifuddin Lubis", "Kel. Besar K.H. Abdul Hakim"] },
  },
});

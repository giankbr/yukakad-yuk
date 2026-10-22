import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Alya", groom: "Rafi",
    brideFull: "Alya Syahidah Rahmani, S.Ds.", groomFull: "Muhammad Rafi Al-Ghifari, S.Ars.",
    brideParents: "Putri pertama dari\nBapak H. Ahmad Rahmani & Ibu Hj. Siti Nurhaliza", groomParents: "Putra kedua dari\nBapak Drs. Hasan Basri & Ibu Fauziah Lubis",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Seperti warna di atas air ebru, kami bertemu tanpa rencana lalu menyatu dalam satu lembar.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-12T08:00:00+07:00",
  place: "Paviliun Kertas Senayan",
  address: "Jl. Asia Afrika No. 19, Gelora, Tanah Abang, Jakarta Pusat",
  stories: [
    { date: "2020", title: "Kelas Ebru Akhir Pekan", body: "Kami duduk bersebelahan di kelas melukis di atas air. Lembar pertama Alya rusak, Rafi menawarkan setengah kertasnya." },
    { date: "2023", title: "Pameran Kecil Berdua", body: "Lembar-lembar marmer kami dipajang di sebuah galeri kecil di Kemang. Di sana Rafi pertama kali bertemu keluarga Alya." },
    { date: "2026", title: "Khitbah", body: "Dengan restu kedua orang tua, keluarga Rafi datang melamar. Cincinnya dibungkus selembar kertas ebru buatan sendiri." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-12T08:00:00+07:00", time: "08.00 – 10.00 WIB", venue: "Masjid Nurul Ilmi", address: "Jl. Ampera Raya No. 12, Cilandak Timur, Pasar Minggu, Jakarta Selatan" },
    { name: "Walimatul 'Ursy", date: "2027-09-12T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Paviliun Kertas Senayan", address: "Jl. Asia Afrika No. 19, Gelora, Tanah Abang, Jakarta Pusat" },
  ],
  gallery: ["/themes/img/a131.webp", "/themes/img/a122.webp", "/themes/img/a100.webp", "/themes/img/r56.webp", "/themes/img/a121.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7140 2299 81", account_name: "Alya Syahidah Rahmani" },
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "0613 4471 20", account_name: "Muhammad Rafi Al-Ghifari" },
    { id: "demo-kado", type: "address", address: "Jl. Kemang Timur Raya No. 7, Bangka, Mampang Prapatan, Jakarta Selatan 12730" },
  ],
  guestName: "Bapak Fadli Ramadhan & Keluarga",
  guestTable: "Meja Lembar 5",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan hidup dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu", note: "Teh dan kue di serambi galeri" },
      { time: "11.30", title: "Kirab kedua mempelai" },
      { time: "12.00", title: "Ramah tamah & santap siang" },
      { time: "13.15", title: "Foto bersama keluarga dan sahabat" },
    ] },
    dressCode: { note: "Busana santun bernuansa marmer: merah muda dusty, hijau teal, oker, atau gading.", colors: ["#e3a79c", "#3f8582", "#c9973f", "#f4ece0"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. H. Ahmad Rahmani", "Kel. Besar Bpk. Drs. Hasan Basri"] },
  },
});

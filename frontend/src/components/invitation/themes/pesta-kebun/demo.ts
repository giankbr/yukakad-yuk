import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Laras", groom: "",
    brideFull: "Larasati Dewi Anindya",
    brideParents: "Bersama keluarga & sahabat",
    bridePhoto: "/themes/img/r100.webp",
    note: "Tiga puluh tahun, banyak cerita, dan orang-orang baik yang selalu menemani. Mari makan malam bersama di kebun.",
  },
  eventLabel: "Pesta Ulang Tahun",
  date: "2027-09-18T17:00:00+07:00",
  place: "Kebun Kenanga",
  address: "Jl. Kaliurang Km. 13,5, Sardonoharjo, Ngaglik, Kabupaten Sleman, DI Yogyakarta",
  story: { title: "Perjalanan Laras", body: "" },
  stories: [
    { date: "1997", title: "Lahir di Kotagede", body: "Anak pertama yang lahir menjelang senja, kata Ibu tangisnya kalah keras dengan suara azan magrib." },
    { date: "2015", title: "Merantau ke Bandung", body: "Kuliah arsitektur lanskap, jatuh cinta pada kebun, dan belajar memasak untuk teman satu kos." },
    { date: "2022", title: "Pulang dan menanam", body: "Kembali ke Jogja, membuka studio taman kecil, dan menanam bunga-bunga liar di halaman belakang rumah." },
    { date: "2027", title: "Tiga puluh!", body: "Satu meja panjang, lampu-lampu kecil, dan semua orang yang membuat tiga puluh tahun ini berarti." },
  ],
  events: [
    { name: "Makan Malam di Kebun", date: "2027-09-18T17:00:00+07:00", time: "17.00 – 21.00 WIB", venue: "Kebun Kenanga", address: "Jl. Kaliurang Km. 13,5, Sardonoharjo, Ngaglik, Kabupaten Sleman, DI Yogyakarta" },
  ],
  gallery: ["/themes/img/r77.webp", "/themes/img/a140.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "0373 1189 54", account_name: "Larasati Dewi Anindya" },
    { id: "demo-gopay", type: "ewallet", ewallet_provider: "gopay", ewallet_number: "0812 2734 5590", account_name: "Larasati Dewi Anindya" },
  ],
  guestName: "Mbak Sekar & Mas Dimas",
  guestTable: "",
  extras: {
    child: { name: "Larasati Dewi Anindya", nickname: "Laras", birthDate: "1997-09-18T17:40:00+07:00", parents: "Bersama keluarga & sahabat", photo: "/themes/img/r100.webp" },
    rundown: { items: [
      { time: "17.00", title: "Datang & minuman sambutan", note: "Wedang uwuh dingin & limun serai" },
      { time: "17.45", title: "Matahari terbenam di kebun" },
      { time: "18.30", title: "Makan malam di meja panjang", note: "Masakan rumahan dari dapur Ibu" },
      { time: "20.00", title: "Tiup lilin & potong kue", note: "Dilanjutkan akustik bersama teman-teman" },
    ] },
    dressCode: { note: "Santai rapi bernuansa senja: krem, terakota, lavender, atau hijau zaitun. Alas kaki nyaman untuk rumput.", colors: ["#efe4d6", "#e8735a", "#9b8ac4", "#6d8a54"] },
    guestPass: {},
    rsvpDietary: {},
    family: { title: "Disiapkan dengan sayang oleh", names: ["Ibu & Bapak Anindya", "Dik Bagas", "Geng Kos Dago"] },
    wishlist: { note: "Datang saja sudah cukup. Tapi kalau ingin membawa sesuatu, ini yang sedang Laras butuhkan untuk kebunnya.", items: [
      { id: "w1", name: "Bibit bunga cosmos & zinnia", price: "± Rp50.000" },
      { id: "w2", name: "Gunting dahan yang bagus", price: "± Rp250.000", claimed_by: "Mas Dimas" },
      { id: "w3", name: "Buku resep sayur kebun", price: "± Rp150.000" },
    ] },
    faq: { items: [
      { q: "Acaranya di luar ruangan?", a: "Ya, di kebun. Bila hujan, meja dipindah ke pendopo yang beratap." },
      { q: "Boleh membawa pasangan atau anak?", a: "Boleh sekali. Konfirmasikan jumlah tamu agar kursi cukup." },
    ] },
  },
});

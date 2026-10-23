import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadine", groom: "Arga",
    brideFull: "Nadine Puspitasari, S.Par.", groomFull: "Arga Mahendra Wiratama, S.T.",
    brideParents: "Putri bungsu dari\nBapak Wahyu Setiadi & Ibu Endang Puspita", groomParents: "Putra sulung dari\nBapak Made Wiratama & Ibu Sri Rahayu",
    bridePhoto: "/themes/img/r107.webp", groomPhoto: "/themes/img/r106.webp",
    note: "Dua pelancong yang bertemu di dermaga, lalu sepakat bahwa perjalanan terbaik adalah perjalanan berdua.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-21T16:00:00+08:00",
  place: "Teras Samudra, Senggigi",
  address: "Jl. Raya Senggigi Km. 12, Batu Layar, Kabupaten Lombok Barat, NTB",
  stories: [
    { date: "Juli 2019", title: "Kapal Pagi ke Gili", body: "Kursi kami bersebelahan di kapal penyeberangan. Nadine mabuk laut, Arga punya permen jahe. Sisa perjalanan kami habiskan dengan mengobrol." },
    { date: "2022", title: "Menyusuri Nusantara", body: "Dari kereta lembah di Jawa Barat sampai sabana di Sumba, kami mengoleksi kartu pos dari setiap kota yang kami singgahi." },
    { date: "Januari 2027", title: "Lamaran di Bukit Senja", body: "Di puncak bukit menghadap laut, Arga menyerahkan kartu pos terakhir. Isinya hanya satu pertanyaan, dan jawabannya ya." },
  ],
  events: [
    { name: "Janji Suci di Tepi Pantai", date: "2027-08-21T16:00:00+08:00", time: "16.00 – 17.00 WITA", venue: "Dek Kayu, Teras Samudra", address: "Jl. Raya Senggigi Km. 12, Batu Layar, Kabupaten Lombok Barat, NTB" },
    { name: "Resepsi Senja", date: "2027-08-21T18:00:00+08:00", time: "18.00 – 21.30 WITA", venue: "Taman Kelapa, Teras Samudra", address: "Jl. Raya Senggigi Km. 12, Batu Layar, Kabupaten Lombok Barat, NTB" },
  ],
  gallery: ["/themes/img/r11.webp", "/themes/img/r103.webp", "/themes/img/r104.webp", "/themes/img/r12.webp", "/themes/img/r109.webp", "/themes/img/r110.webp"],
  gifts: [
    { id: "demo-bni", type: "bank", bank_name: "BNI", account_number: "0712 5588 21", account_name: "Nadine Puspitasari" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0219 0100 7731 508", account_name: "Arga Mahendra Wiratama" },
    { id: "demo-kado", type: "address", address: "Jl. Pejanggik No. 45, Cakranegara, Kota Mataram, NTB 83231" },
  ],
  guestName: "Bapak Yohanes Lomi & Keluarga",
  guestTable: "Meja Dermaga 2",
  extras: {
    quote: { text: "Kami sudah melihat banyak pelabuhan, gunung, dan matahari terbenam. Tetapi pemandangan terindah selalu ada di kursi sebelah.", source: "Buku harian perjalanan Nadine & Arga" },
    rundown: { items: [
      { time: "18.00", title: "Minuman sambutan & musik akustik", note: "Taman Kelapa" },
      { time: "18.30", title: "Kedua mempelai tiba dengan perahu" },
      { time: "19.00", title: "Makan malam hidangan laut" },
      { time: "20.30", title: "Dansa di bawah lampu gantung" },
    ] },
    dressCode: { note: "Pesta pantai sore: linen, warna laut dan senja. Sepatu datar atau sandal, karena kita akan berdiri di pasir.", colors: ["#1d4f5c", "#5fa3a3", "#f3c46e", "#ee8a4a", "#f6e7c8"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Wahyu Setiadi", "Kel. Besar Bpk. Made Wiratama"] },
    travel: { note: "Bandara Lombok ± 50 menit berkendara ke Senggigi. Kapal cepat dari Bali tiba di Teluk Kodek.", items: [
      { name: "Antar-jemput", detail: "Shuttle dari Hotel Senggigi pukul 17.15 WITA" },
      { name: "Menginap", detail: "Hotel & vila di sepanjang Pantai Senggigi" },
    ] },
  },
});

import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Valerie", groom: "Nathaniel",
    brideFull: "Valerie Anindya Kusnadi", groomFull: "Nathaniel Prasetya Gunawan",
    brideParents: "Putri tunggal dari\nBapak Robert Kusnadi & Ibu Melinda Hartanto",
    groomParents: "Putra pertama dari\nBapak Dr. Hendra Gunawan & Ibu Yuliana Setiadi",
    bridePhoto: "/themes/img/r27.webp", groomPhoto: "/themes/img/r106.webp",
    note: "Seperti batu yang terbentuk lapis demi lapis selama bertahun-tahun, cinta kami tumbuh pelan, dan di dalamnya kami menemukan sesuatu yang berkilau.",
  },
  eventLabel: "Pernikahan",
  date: "2027-11-20T16:00:00+07:00",
  place: "Sapphire Ballroom, Hotel Nirwana Senayan",
  address: "Jl. Asia Afrika No. 8, Gelora, Tanah Abang, Jakarta Pusat",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2019", title: "Ruang Pameran", body: "Kami bertemu di pameran batu mulia di Jakarta. Valerie menunjuk sebuah geode biru, Nathaniel bilang itu favoritnya juga." },
    { date: "2022", title: "Lapis demi Lapis", body: "Dua kota, satu kebiasaan: telepon setiap Minggu malam, dan kartu pos dari setiap perjalanan dinas." },
    { date: "Februari 2027", title: "Sebuah Pertanyaan", body: "Di bawah langit malam Bromo, Nathaniel membuka kotak kecil berisi cincin dengan batu biru. Jawabannya: ya." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-11-20T16:00:00+07:00", time: "16.00 – 17.00 WIB", venue: "Taman Kaca, Hotel Nirwana Senayan", address: "Jl. Asia Afrika No. 8, Gelora, Tanah Abang, Jakarta Pusat" },
    { name: "Resepsi Malam", date: "2027-11-20T18:30:00+07:00", time: "18.30 – 21.30 WIB", venue: "Sapphire Ballroom, Hotel Nirwana Senayan", address: "Jl. Asia Afrika No. 8, Gelora, Tanah Abang, Jakarta Pusat" },
  ],
  gallery: ["/themes/img/a110.webp", "/themes/img/a131.webp", "/themes/img/r84.webp", "/themes/img/a124.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "5271 0938 44", account_name: "Valerie Anindya Kusnadi" },
    { id: "demo-cimb", type: "bank", bank_name: "CIMB Niaga", account_number: "7060 1123 9850", account_name: "Nathaniel Prasetya Gunawan" },
  ],
  guestName: "Bapak Andreas Wijaya & Partner",
  guestTable: "Meja Safir 7",
  extras: {
    quote: { text: "Waktu membentuk batu menjadi permata, lapis demi lapis. Kesetiaan membentuk dua hati menjadi satu rumah." },
    rundown: { items: [
      { time: "16.00", title: "Upacara pernikahan", note: "Taman Kaca, keluarga & sahabat dekat" },
      { time: "18.30", title: "Resepsi dibuka", note: "Welcome drink di foyer" },
      { time: "19.15", title: "Dansa pertama" },
      { time: "20.00", title: "Makan malam & sambutan keluarga" },
    ] },
    dressCode: { note: "Formal malam: gaun panjang dan jas, nuansa biru safir, perak, dan emas.", colors: ["#0e1b35", "#24508f", "#8fb5e2", "#f4f2ee", "#caa24c"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-11-20T16:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Robert Kusnadi", "Kel. Besar Bpk. Dr. Hendra Gunawan"] },
    faq: { items: [
      { q: "Apakah tersedia valet parking?", a: "Ya, valet tersedia di lobi utama hotel untuk seluruh tamu undangan." },
      { q: "Bolehkah membawa anak?", a: "Dengan senang hati. Mohon cantumkan jumlah tamu saat konfirmasi kehadiran." },
    ] },
  },
});

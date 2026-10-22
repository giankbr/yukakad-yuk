import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Ayu", groom: "Wira",
    brideFull: "Ni Luh Putu Ayu Saraswati, S.Ds.", groomFull: "I Gede Wira Pratama, S.T.",
    brideParents: "Putri sulung dari\nBapak I Made Suarjana & Ibu Ni Ketut Sriani",
    groomParents: "Putra pertama dari\nBapak I Wayan Darma Putra & Ibu Ni Made Rai Astiti",
    bridePhoto: "/themes/img/a62.webp", groomPhoto: "/themes/img/a60.webp",
    note: "Seperti bambu yang tumbuh berumpun: akarnya saling menggenggam di bawah tanah, batangnya menjulang bersama menuju cahaya.",
  },
  eventLabel: "Pawiwahan",
  date: "2027-07-17T09:00:00+08:00",
  place: "Bale Bambu Sayan",
  address: "Jl. Raya Sayan No. 27, Sayan, Ubud, Kabupaten Gianyar, Bali",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "Maret 2020", title: "Lokakarya anyaman bambu", body: "Ayu datang untuk belajar menganyam, Wira mengajar membelah bilah bambu. Tangan Ayu tergores, Wira yang paling panik mencari plester." },
    { date: "2021 – 2025", title: "Tumbuh perlahan", body: "Denpasar dan Ubud, studio desain dan lokasi proyek. Kami selalu bertemu di warung kopi yang sama setiap Minggu pagi." },
    { date: "Januari 2027", title: "Ngidih", body: "Keluarga Wira datang secara resmi memadik Ayu. Kedua keluarga sepakat, dan hari baik pun dipilih bersama sulinggih." },
  ],
  events: [
    { name: "Upacara Pawiwahan", date: "2027-07-17T09:00:00+08:00", time: "09.00 – 12.00 WITA", venue: "Kediaman Keluarga I Wayan Darma Putra", address: "Banjar Kutuh Kaja, Petulu, Ubud, Kabupaten Gianyar, Bali" },
    { name: "Resepsi di Hutan Bambu", date: "2027-07-17T17:00:00+08:00", time: "17.00 – 20.00 WITA", venue: "Bale Bambu Sayan", address: "Jl. Raya Sayan No. 27, Sayan, Ubud, Kabupaten Gianyar, Bali" },
  ],
  gallery: ["/themes/img/a30.webp", "/themes/img/a64.webp", "/themes/img/r89.webp"],
  gifts: [
    { id: "demo-bpd", type: "bank", bank_name: "BPD Bali", account_number: "0180 2021 5467 8", account_name: "Ni Luh Putu Ayu Saraswati" },
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "7710 3348 92", account_name: "I Gede Wira Pratama" },
  ],
  guestName: "Bapak I Ketut Sudarsana & Keluarga",
  guestTable: "",
  extras: {
    quote: { text: "Semoga para dewa menyatukan hati kami berdua; semoga air menyatukan kami. Semoga angin, pencipta, dan dewi kebijaksanaan mengikat kami berdua.", source: "Rgveda X.85.47" },
    rundown: { items: [
      { time: "17.00", title: "Penyambutan tamu", note: "Iringan rindik di jalan setapak bambu" },
      { time: "17.45", title: "Kedatangan kedua mempelai" },
      { time: "18.15", title: "Santap malam", note: "Hidangan Bali & pilihan vegetarian" },
      { time: "19.30", title: "Foto bersama di bawah rumpun bambu" },
    ] },
    dressCode: { note: "Nuansa alam: hijau bambu, krem, dan emas lembut. Kebaya atau busana adat madya dipersilakan.", colors: ["#5f8436", "#cfae46", "#efe8d2", "#3a4a2c"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar I Made Suarjana", "Kel. Besar I Wayan Darma Putra", "Sanggar Anyam Bambu Petulu"] },
    travel: { note: "Jalan menuju Sayan sempit dan berliku. Kami sarankan berangkat lebih awal.", items: [
      { name: "Parkir tamu", detail: "Lapangan Desa Sayan, shuttle ke venue tiap 15 menit" },
      { name: "Penginapan", detail: "Beberapa homestay di Jl. Raya Sayan, ± 5 menit berjalan kaki" },
    ] },
    faq: { items: [
      { q: "Apakah tamu boleh menghadiri upacara pawiwahan?", a: "Upacara pagi khusus keluarga. Tamu undangan kami nantikan di resepsi sore." },
      { q: "Apakah venue ramah lansia?", a: "Jalan setapak bambu landai dan tersedia kursi roda di pintu masuk." },
    ] },
  },
});

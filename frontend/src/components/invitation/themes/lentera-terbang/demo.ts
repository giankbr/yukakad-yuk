import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Aruna", groom: "Bastian",
    brideFull: "Aruna Kirana Maheswari", groomFull: "Bastian Adi Nugroho",
    brideParents: "Putri pertama dari\nBapak Yohanes Setiadi & Ibu Maria Kristina",
    groomParents: "Putra kedua dari\nBapak Robertus Nugroho & Ibu Agnes Wulandari",
    bridePhoto: "/themes/img/a83.webp", groomPhoto: "/themes/img/a84.webp",
    note: "Setiap lentera membawa satu harapan. Malam itu, kami akan melepaskan ratusan, dan semuanya bertuliskan nama kalian.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-21T16:00:00+07:00",
  place: "Paviliun Tepi Telaga, Sarangan",
  address: "Jl. Raya Telaga Sarangan, Ngerong, Plaosan, Kabupaten Magetan",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2018", title: "Festival Lampion", body: "Kami berdiri bersebelahan di tepi telaga, sama-sama gagal menyalakan lentera. Bastian meminjamkan korek, Aruna meminjamkan tawa." },
    { date: "2022", title: "Arah yang Sama", body: "Empat tahun, dua kota, dan entah berapa panggilan video tengah malam. Kami belajar bahwa jarak hanya soal sabar." },
    { date: "2026", title: "Satu Lentera Lagi", body: "Di telaga yang sama, Bastian menuliskan satu pertanyaan di kertas lentera. Aruna menjawabnya sebelum lentera itu sempat terbang." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-08-21T16:00:00+07:00", time: "16.00 – 17.00 WIB", venue: "Dermaga Timur Telaga Sarangan", address: "Jl. Raya Telaga Sarangan, Ngerong, Plaosan, Kabupaten Magetan" },
    { name: "Resepsi & Pelepasan Lentera", date: "2027-08-21T18:30:00+07:00", time: "18.30 – 21.30 WIB", venue: "Paviliun Tepi Telaga", address: "Jl. Raya Telaga Sarangan, Ngerong, Plaosan, Kabupaten Magetan" },
  ],
  gallery: ["/themes/img/a110.webp", "/themes/img/a86.webp", "/themes/img/a87.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "2290 4417 60", account_name: "Aruna Kirana Maheswari" },
    { id: "demo-kado", type: "address", address: "Jl. Kawi No. 22, Klojen, Kota Malang 65119" },
  ],
  guestName: "Bapak Yosef Hartanto & Keluarga",
  guestTable: "Meja Lentera 9",
  extras: {
    quote: { text: "Cinta tidak meminta kita menatap satu sama lain, tetapi bersama-sama memandang ke arah yang sama.", source: "Aruna & Bastian" },
    rundown: { items: [
      { time: "16.00", title: "Upacara di dermaga", note: "Mohon hadir 30 menit sebelumnya" },
      { time: "17.15", title: "Senja & foto bersama" },
      { time: "18.30", title: "Makan malam di paviliun" },
      { time: "20.30", title: "Pelepasan lentera", note: "Lentera kertas ramah lingkungan, dibagikan panitia" },
    ] },
    dressCode: { note: "Semi formal bernuansa malam: biru tua, plum, dan sentuhan jingga keemasan. Udara telaga dingin, bawa jaket atau selendang.", colors: ["#171a45", "#4a2f5c", "#f3b25a", "#f6ead6"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bapak Yohanes Setiadi", "Kel. Besar Bapak Robertus Nugroho"] },
    travel: { note: "Telaga Sarangan berada di ketinggian ± 1.200 mdpl, suhu malam bisa 14°C.", items: [
      { name: "Shuttle dari Magetan", detail: "Berangkat 14.30 dari Alun-alun Magetan, kembali 22.00" },
      { name: "Penginapan", detail: "Hotel dan homestay di sekitar telaga, ± 5 menit berjalan kaki" },
    ] },
  },
});

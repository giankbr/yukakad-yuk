import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Panitia 17-an", groom: "",
    brideFull: "Panitia HUT RI ke-82 RT 05 / RW 03 Sukamaju",
    brideParents: "Ketua Panitia: Yoga Pratama\nKetua RT 05: Bapak H. Darmawan Saputra\nBendahara: Ibu Sri Wahyuni",
    note: "Lomba untuk anak-anak, remaja, sampai bapak-ibu. Hadiah menarik sudah tergantung di puncak pinang. Ayo ramaikan!",
  },
  eventLabel: "Lomba 17-an",
  date: "2027-08-17T07:30:00+07:00",
  place: "Lapangan Voli RT 05",
  address: "Gg. Melati III, Kel. Sukamaju, Kec. Cilodong, Kota Depok",
  story: { title: "Dari Tahun ke Tahun", body: "" },
  stories: [
    { date: "2019", title: "Pinang pertama", body: "Batang pinang setinggi delapan meter pertama kali berdiri di lapangan voli. Butuh tiga tim dan dua ember oli sampai hadiahnya turun." },
    { date: "2023", title: "Tarik tambang ibu-ibu", body: "Tim PKK Gang Melati menang telak melawan tim bapak-bapak. Sampai sekarang masih jadi bahan cerita di pos ronda." },
    { date: "2026", title: "Juara bertahan", body: "Dimas kelas 4 SD menang balap karung tiga tahun berturut-turut. Tahun ini, siapa yang berani menantang?" },
  ],
  events: [
    { name: "Lomba Anak-anak", date: "2027-08-17T07:30:00+07:00", time: "07.30 – 11.00 WIB", venue: "Lapangan Voli RT 05", address: "Gg. Melati III, Kel. Sukamaju, Kec. Cilodong, Kota Depok" },
    { name: "Lomba Dewasa & Panjat Pinang", date: "2027-08-17T13:00:00+07:00", time: "13.00 – 17.00 WIB", venue: "Lapangan Voli RT 05", address: "Gg. Melati III, Kel. Sukamaju, Kec. Cilodong, Kota Depok" },
    { name: "Malam Tasyakuran & Pembagian Hadiah", date: "2027-08-17T19:30:00+07:00", time: "19.30 – 22.00 WIB", venue: "Balai Warga RW 03", address: "Jl. Raya Sukamaju No. 12, Kel. Sukamaju, Kec. Cilodong, Kota Depok" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "3412 0110 8765 507", account_name: "Sri Wahyuni (Bendahara Panitia)" },
    { id: "demo-hadiah", type: "address", address: "Pos Ronda RT 05, Gg. Melati III No. 1, Sukamaju, Cilodong, Depok", account_name: "Pak Darmawan (Ketua RT 05)" },
  ],
  guestName: "Keluarga Bapak Sutrisno",
  guestTable: "Blok C No. 14",
  extras: {
    quote: { text: "Merdeka itu bergembira bersama: bergotong royong, saling menyemangati, dan menjaga kampung kita tetap rukun.", source: "Panitia 17-an RT 05" },
    rundown: { items: [
      { time: "06.30", title: "Kerja bakti & pasang umbul-umbul", note: "Kumpul di pos ronda" },
      { time: "07.30", title: "Lomba anak", note: "Balap karung, makan kerupuk, kelereng dalam sendok" },
      { time: "13.00", title: "Lomba dewasa", note: "Tarik tambang, bakiak, panjat pinang" },
      { time: "19.30", title: "Tasyakuran & pembagian hadiah", note: "Nasi tumpeng bersama" },
    ] },
    dressCode: { note: "Kaos merah atau putih, celana yang nyaman, dan jangan lupa topi. Siap kotor di panjat pinang!", colors: ["#d7262e", "#fbf6ea", "#f6c343", "#2a1d17"] },
    family: { title: "Didukung oleh", names: ["Karang Taruna Tunas Merdeka", "Ibu-ibu PKK RT 05", "Pemuda Masjid Al-Ikhlas", "Warung Bu Tini & Toko Berkah"] },
    faq: { items: [
      { q: "Siapa saja yang boleh ikut lomba?", a: "Semua warga RT 05 / RW 03 dan keluarganya. Pendaftaran di meja panitia pagi hari, gratis." },
      { q: "Apakah ada konsumsi?", a: "Ada air minum dan snack untuk peserta. Malamnya tumpeng bersama di Balai Warga." },
      { q: "Bolehkah menyumbang hadiah?", a: "Boleh sekali. Hadiah barang bisa dititipkan di pos ronda, iuran lewat rekening bendahara di bawah." },
    ] },
  },
});

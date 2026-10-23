import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Natalia", groom: "Yohanes",
    brideFull: "Natalia Endu Ak. Jimbun", groomFull: "Yohanes Bujang Ak. Langgi",
    brideParents: "Putri dari Bapak Jimbun Anyau\n& Ibu Rosalia Sumbang", groomParents: "Putra dari Bapak Langgi Ensiring\n& Ibu Maria Ngumbang",
    note: "Seperti benang lungsin dan pakan yang ditenun menjadi pua, dua keluarga dari hulu dan hilir Kapuas kini disatukan dalam kasih Tuhan.",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-17T09:00:00+07:00",
  place: "Rumah Panjai Sungai Utik",
  address: "Dusun Sungai Utik, Desa Batu Lintang, Kec. Embaloh Hulu, Kapuas Hulu, Kalimantan Barat",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "Mei 2021", title: "Gawai di Putussibau", body: "Kami pertama bertemu di Gawai Dayak Kapuas Hulu. Natalia menenun di stan kain, Yohanes menabuh gendang di panggung sebelah." },
    { date: "2023", title: "Menyusuri Kapuas", body: "Berkali-kali naik speedboat dari Sintang ke Putussibau untuk berkunjung, belajar mengenal keluarga besar di rumah panjai." },
    { date: "Des 2026", title: "Bertanya ke Orang Tua", body: "Selepas misa Natal, keluarga Yohanes datang membawa tanda bertanya. Kedua keluarga sepakat menyatukan kami." },
    { date: "Juli 2027", title: "Melah Pinang", body: "Kami diberkati di gereja lalu dirayakan secara adat Iban bersama seluruh penghuni rumah panjai." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-07-17T09:00:00+07:00", time: "09.00 – 11.00 WIB", venue: "Gereja Katolik Santo Martinus Putussibau", address: "Jl. Kom. Yos Sudarso No. 12, Putussibau Kota, Kapuas Hulu" },
    { name: "Gawai Melah Pinang", date: "2027-07-17T16:00:00+07:00", time: "16.00 WIB – selesai", venue: "Rumah Panjai Sungai Utik", address: "Dusun Sungai Utik, Desa Batu Lintang, Kec. Embaloh Hulu, Kapuas Hulu" },
    { name: "Syukuran Keluarga", date: "2027-07-24T18:30:00+07:00", time: "18.30 – 21.00 WIB", venue: "Balai Pertemuan Umum Sintang", address: "Jl. Lintas Melawi, Kapuas Kanan Hulu, Sintang" },
  ],
  gallery: ["/themes/img/a30.webp", "/themes/img/r89.webp", "/themes/img/a22.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0451 0102 7781 503", account_name: "Natalia Endu" },
    { id: "demo-bni", type: "bank", bank_name: "BNI", account_number: "0987 2027 17", account_name: "Yohanes Bujang" },
    { id: "demo-kado", type: "address", address: "Jl. Lintas Utara No. 8, Kedamin Hulu, Putussibau Selatan, Kapuas Hulu 78714" },
  ],
  guestName: "Bapak Fransiskus Unyang & Keluarga",
  guestTable: "Ruai 3",
  extras: {
    quote: { text: "Demikianlah mereka bukan lagi dua, melainkan satu. Karena itu, apa yang telah dipersatukan Allah, tidak boleh diceraikan manusia.", source: "Matius 19:6" },
    rundown: { items: [
      { time: "16.00", title: "Penyambutan rombongan di tangga rumah panjai" },
      { time: "16.45", title: "Upacara melah pinang", note: "Dipimpin tuai rumah" },
      { time: "18.00", title: "Makan bersama di ruai" },
      { time: "19.30", title: "Tarian ngajat & petikan sape" },
    ] },
    dressCode: { note: "Busana adat atau kain tenun dipersilakan. Nuansa merah tanah, hitam, dan krem.", colors: ["#7a2e1c", "#1c1310", "#eadbbd", "#b9853f"] },
    rsvpDietary: {},
    family: { names: ["Keluarga Besar Jimbun Anyau", "Keluarga Besar Langgi Ensiring", "Warga Rumah Panjai Sungai Utik"] },
    travel: { note: "Untuk tamu dari Pontianak dan Sintang.", items: [
      { name: "Penerbangan Pontianak – Putussibau", detail: "Bandara Pangsuma, sekitar 1 jam 20 menit" },
      { name: "Antar-jemput ke Sungai Utik", detail: "Mobil keluarga berangkat dari gereja pukul 13.30" },
    ] },
    faq: { items: [
      { q: "Apakah boleh membawa anak?", a: "Tentu. Ruai rumah panjai luas dan anak-anak sangat diterima." },
      { q: "Bagaimana jalan menuju Sungai Utik?", a: "Sekitar 1,5 jam dari Putussibau lewat jalan lintas utara. Rombongan keluarga akan memandu." },
    ] },
  },
});

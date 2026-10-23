import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Maharani", groom: "Raditya",
    brideFull: "Maharani Kirana Wijaya", groomFull: "Raditya Pradipta Halim",
    brideParents: "Putri dari\nBapak Johan Wijaya & Ibu Liliana Santoso",
    groomParents: "Putra dari\nBapak Hendra Halim & Ibu Margaretha Susanti",
    bridePhoto: "/themes/img/a83.webp", groomPhoto: "/themes/img/a84.webp",
    note: "Seperti seikat bunga dalam lukisan lama: dikumpulkan dari musim yang berbeda, lalu disatukan dalam satu jambangan.",
  },
  eventLabel: "Pernikahan",
  date: "2027-11-13T16:00:00+07:00",
  place: "Rumah Kaca Bloemenhof",
  address: "Jl. Maribaya No. 41, Langensari, Lembang, Kabupaten Bandung Barat",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2020", title: "Di Ruang Pamer", body: "Kami berdiri di depan lukisan yang sama di sebuah museum di Jakarta, sama-sama terlalu lama, sampai petugas mengingatkan bahwa museum akan tutup." },
    { date: "2023", title: "Kebun di Lembang", body: "Raditya merawat kebun bunga keluarga; Maharani datang untuk melukis peoni pertama yang mekar di sana." },
    { date: "2026", title: "Lamaran", body: "Di bawah lampu rumah kaca, sebuah kanvas kecil bergambar seikat bunga dengan satu pertanyaan di sudutnya." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-11-13T16:00:00+07:00", time: "16.00 – 17.00 WIB", venue: "Rumah Kaca Bloemenhof", address: "Jl. Maribaya No. 41, Langensari, Lembang, Kabupaten Bandung Barat" },
    { name: "Makan Malam Resepsi", date: "2027-11-13T18:30:00+07:00", time: "18.30 – 21.30 WIB", venue: "Paviliun Taman Bloemenhof", address: "Jl. Maribaya No. 41, Langensari, Lembang, Kabupaten Bandung Barat" },
  ],
  gallery: ["/themes/img/a86.webp", "/themes/img/a85.webp", "/themes/img/a87.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BCA", account_number: "8020 4417 63", account_name: "Maharani Kirana Wijaya" },
    { id: "demo-address", type: "address", address: "Jl. Maribaya No. 41, Langensari, Lembang, Kabupaten Bandung Barat 40391", account_name: "Maharani & Raditya" },
  ],
  guestName: "Bapak Antonius Gunawan & Keluarga",
  guestTable: "Meja Peoni 4",
  extras: {
    rundown: { items: [
      { time: "16.00", title: "Upacara pernikahan", note: "Di rumah kaca utama" },
      { time: "17.00", title: "Ramah tamah & foto senja", note: "Taman peoni" },
      { time: "18.30", title: "Makan malam resepsi", note: "Paviliun taman" },
      { time: "20.30", title: "Pemotongan kue & dansa" },
    ] },
    dressCode: { note: "Formal malam dengan nuansa gelap: hitam, burgundi, hijau lumut, atau krem. Udara Lembang dingin, bawalah jas atau syal.", colors: ["#0d0b0a", "#6e1f2a", "#3a4a2a", "#efe4cf"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Johan Wijaya", "Kel. Besar Hendra Halim"] },
    travel: { note: "Lokasi berada di dataran tinggi Lembang, sekitar 45 menit dari pusat Kota Bandung.", items: [
      { name: "Parkir", detail: "Area parkir tamu di gerbang utara, shuttle setiap 10 menit" },
    ] },
  },
});

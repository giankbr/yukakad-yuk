import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Tiara", groom: "Johan",
    brideFull: "Tiara Puspita Larasati", groomFull: "Johan Prasetya Nugroho",
    brideParents: "Putri pertama dari\nBapak Agus Setiawan & Ibu Rina Puspitasari", groomParents: "Putra ketiga dari\nBapak Bambang Nugroho & Ibu Yuliana Sari",
    bridePhoto: "/themes/img/r100.webp", groomPhoto: "/themes/img/r101.webp",
    note: "Seperti umbi tulip yang ditanam di musim dingin, cinta kami tumbuh pelan-pelan dan kini mekar di musim semi.",
  },
  eventLabel: "Pernikahan",
  date: "2027-04-17T09:00:00+07:00",
  place: "Taman Bunga Nusantara",
  address: "Jl. Mariwati KM 7, Kawungluwuk, Sukaresmi, Cianjur, Jawa Barat",
  story: { title: "", body: "" },
  stories: [
    { date: "Maret 2021", title: "Pasar Bunga Pagi", body: "Johan salah membeli seikat tulip plastik untuk ibunya. Tiara, penjual bunga di lapak sebelah, menukarnya dengan tulip asli sambil tertawa." },
    { date: "2022 – 2025", title: "Kebun Kecil di Balkon", body: "Kami menanam bibit bunga di pot-pot kecil di balkon kontrakan. Banyak yang gagal, tapi kami tidak pernah berhenti menanam lagi." },
    { date: "April 2026", title: "Di Tengah Ladang", body: "Di antara barisan tulip merah di Cipanas, Johan berlutut dengan cincin yang ia sembunyikan di dalam pot bunga." },
  ],
  events: [
    { name: "Janji Pernikahan", date: "2027-04-17T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Taman Mawar, Taman Bunga Nusantara", address: "Jl. Mariwati KM 7, Kawungluwuk, Sukaresmi, Cianjur, Jawa Barat" },
    { name: "Resepsi Taman", date: "2027-04-17T11:30:00+07:00", time: "11.30 – 15.00 WIB", venue: "Lapangan Kincir, Taman Bunga Nusantara", address: "Jl. Mariwati KM 7, Kawungluwuk, Sukaresmi, Cianjur, Jawa Barat" },
  ],
  gallery: ["/themes/img/a111.webp", "/themes/img/r16.webp", "/themes/img/r108.webp", "/themes/img/r14.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "2830 6619 54", account_name: "Tiara Puspita Larasati" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0412 0109 8823 501", account_name: "Johan Prasetya Nugroho" },
    { id: "demo-kado", type: "address", address: "Jl. Cempaka Putih Tengah No. 21, Cempaka Putih, Jakarta Pusat 10510" },
  ],
  guestName: "Ibu Margaretha Siregar & Keluarga",
  guestTable: "Meja Tulip 6",
  extras: {
    quote: { text: "Cinta adalah bunga yang harus kau biarkan tumbuh.", source: "Pepatah lama" },
    rundown: { items: [
      { time: "09.00", title: "Janji pernikahan di Taman Mawar" },
      { time: "10.30", title: "Ramah tamah & foto keluarga" },
      { time: "11.30", title: "Resepsi taman dibuka", note: "Lapangan Kincir" },
      { time: "13.00", title: "Lempar bunga & potong kue" },
    ] },
    dressCode: { note: "Warna musim semi: merah tulip, merah muda, kuning, atau putih. Sepatu nyaman untuk berjalan di rumput.", colors: ["#e0453a", "#f08bb0", "#f4c542", "#fbf4ea", "#4f8a3c"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Agus Setiawan", "Kel. Besar Bpk. Bambang Nugroho"] },
    faq: { items: [
      { q: "Apakah acaranya di luar ruangan?", a: "Ya, di taman terbuka. Tersedia tenda bila hujan, dan payung di pintu masuk." },
      { q: "Bagaimana dengan tiket masuk taman?", a: "Tunjukkan kartu masuk tamu di gerbang utama, tamu undangan tidak perlu membeli tiket." },
    ] },
  },
});

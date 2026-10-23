import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Mentari", groom: "Bayu",
    brideFull: "Mentari Ayu Kusumawardani", groomFull: "Bayu Satria Nugroho, S.P.",
    brideParents: "Putri sulung dari\nBapak Agus Kusnadi & Ibu Wening Handayani", groomParents: "Putra ketiga dari\nBapak Darmanto & Ibu Christina Puji Astuti",
    bridePhoto: "/themes/img/r91.webp", groomPhoto: "/themes/img/r90.webp",
    note: "Seperti bunga matahari, kami memilih untuk selalu menghadap ke arah cahaya, bersama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-10T09:00:00+07:00",
  place: "Ladang Kencana",
  address: "Jl. Raya Bumiaji No. 18, Bumiaji, Kota Batu, Jawa Timur",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2019", title: "Satu Kebun Percobaan", body: "Bayu meneliti tanaman pangan, Mentari memotret untuk buletin kampus. Kami bertemu di antara petak bunga matahari percobaan." },
    { date: "2024", title: "Musim Tanam Pertama", body: "Kami menyewa sepetak lahan kecil di Batu dan menanam bunga matahari bersama. Panen pertama kami bagikan ke tetangga." },
    { date: "Agustus 2026", title: "Di Tengah Ladang", body: "Di bawah langit biru tanpa awan, Bayu melamar dengan seikat bunga matahari yang diikat tali rami." },
  ],
  events: [
    { name: "Upacara Pernikahan", date: "2027-07-10T09:00:00+07:00", time: "09.00 – 10.30 WIB", venue: "Paviliun Ladang Kencana", address: "Jl. Raya Bumiaji No. 18, Bumiaji, Kota Batu, Jawa Timur" },
    { name: "Resepsi di Ladang", date: "2027-07-10T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Ladang Kencana", address: "Jl. Raya Bumiaji No. 18, Bumiaji, Kota Batu, Jawa Timur" },
  ],
  gallery: ["/themes/img/r8.webp", "/themes/img/r16.webp", "/themes/img/r14.webp", "/themes/img/a64.webp", "/themes/img/r104.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0215 0110 4478 509", account_name: "Mentari Ayu Kusumawardani" },
    { id: "demo-dana", type: "ewallet", ewallet_provider: "dana", ewallet_number: "0857 3312 9046", account_name: "Bayu Satria Nugroho" },
  ],
  guestName: "Keluarga Bapak Slamet Riyadi",
  guestTable: "Meja Kencana 3",
  extras: {
    quote: { text: "Tetaplah menghadap matahari, maka bayang-bayang akan jatuh di belakangmu.", source: "Pepatah" },
    rundown: { items: [
      { time: "09.00", title: "Upacara pernikahan", note: "Di paviliun kayu" },
      { time: "11.00", title: "Resepsi dibuka", note: "Jamuan di bawah tenda ladang" },
      { time: "12.30", title: "Petik bunga bersama", note: "Setiap tamu membawa pulang setangkai" },
      { time: "13.30", title: "Foto bersama di ladang" },
    ] },
    dressCode: { note: "Kuning cerah, biru langit, krem, dan hijau daun. Topi lebar sangat disarankan.", colors: ["#f2b705", "#5d93cf", "#fbf3df", "#4f7a24"] },
    guestPass: {},
    rsvpDietary: {},
    faq: { items: [
      { q: "Apakah acara di ruang terbuka?", a: "Ya, resepsi di ladang dengan tenda. Sinar matahari cukup terik, bawalah topi dan kacamata hitam." },
      { q: "Apakah ada parkir?", a: "Tersedia parkir luas di sisi timur ladang, dengan petugas yang mengarahkan." },
    ] },
  },
});

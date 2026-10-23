import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Marthina", groom: "Yosua",
    brideFull: "Marthina Itlay, S.Kep.", groomFull: "Yosua Wetipo, S.Hut.",
    brideParents: "Putri ketiga dari\nBapak Pdt. Yakobus Itlay & Ibu Ruth Lokobal", groomParents: "Putra sulung dari\nBapak Agus Wetipo & Ibu Maria Asso",
    note: "Tali tiga lembar tak mudah diputuskan. Seperti noken yang dirajut sabar, kami merajut hidup bersama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-09-25T10:00:00+09:00",
  place: "Kampung Wesaput, Wamena",
  address: "Kampung Wesaput, Distrik Wesaput, Kabupaten Jayawijaya, Papua Pegunungan",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2018", title: "Pelayanan pemuda", body: "Kami bertemu di persekutuan pemuda gereja di Wamena, sama-sama melayani di paduan suara Natal." },
    { date: "2022", title: "Kebun di Hubikosi", body: "Yosua mengajar warga merawat bibit kopi, Marthina bertugas di puskesmas. Akhir pekan kami habiskan di kebun ubi keluarga." },
    { date: "2027", title: "Restu dua keluarga", body: "Setelah musyawarah keluarga besar, kami diberkati untuk melangkah bersama dan berbagi syukur dalam bakar batu." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-09-25T10:00:00+09:00", time: "10.00 – 12.00 WIT", venue: "Gereja GIDI Jemaat Elim Wamena", address: "Jl. Yos Sudarso, Wamena Kota, Kabupaten Jayawijaya, Papua Pegunungan" },
    { name: "Syukuran Bakar Batu", date: "2027-09-25T13:30:00+09:00", time: "13.30 – selesai", venue: "Halaman Honai Keluarga Wetipo", address: "Kampung Wesaput, Distrik Wesaput, Kabupaten Jayawijaya, Papua Pegunungan" },
  ],
  gallery: ["/themes/img/r104.webp", "/themes/img/a22.webp", "/themes/img/r108.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "Bank Papua", account_number: "2210 4455 0193", account_name: "Yosua Wetipo" },
    { id: "demo-kado", type: "address", address: "Jl. Homhom No. 8, Wamena Kota, Kabupaten Jayawijaya, Papua Pegunungan 99511" },
  ],
  guestName: "Bapak Nikolaus Kossay & Keluarga",
  guestTable: "Honai 2",
  extras: {
    quote: { text: "Dan bilamana seorang dapat dialahkan, dua orang akan dapat bertahan. Tali tiga lembar tak mudah diputuskan.", source: "Pengkhotbah 4:12" },
    rundown: { items: [
      { time: "13.30", title: "Penyambutan keluarga dan tamu" },
      { time: "14.00", title: "Doa syukur dan pembukaan bakar batu", note: "Dipimpin para tua-tua adat" },
      { time: "16.00", title: "Makan bersama", note: "Ubi, sayur, dan hasil kebun" },
      { time: "17.00", title: "Nyanyian syukur dan foto bersama" },
    ] },
    dressCode: { note: "Busana rapi dan hangat, udara Wamena sejuk. Nuansa tanah, hijau lumut, dan warna noken dipersilakan.", colors: ["#2c4a36", "#9a4a2a", "#c9a46a", "#6a3a68"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Pdt. Yakobus Itlay", "Kel. Besar Agus Wetipo", "Keluarga Besar Lokobal & Asso"] },
    faq: { items: [
      { q: "Bagaimana cuaca di Wamena?", a: "Pagi dan sore cukup dingin, sekitar 15–20 °C. Bawalah jaket atau syal." },
      { q: "Apakah tersedia penjemputan dari bandara?", a: "Keluarga menyiapkan kendaraan dari Bandara Wamena ke gereja. Hubungi panitia sehari sebelumnya." },
    ] },
  },
});

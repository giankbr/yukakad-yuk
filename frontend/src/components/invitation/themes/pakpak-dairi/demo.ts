import { makeDemo } from "../demo-base";

// Pakpak (Kristen), Dairi: pemberkatan nikah di gereja → merbayo (pesta adat Pakpak) di jambur, Sidikalang.
export const demo = makeDemo({
  couple: {
    bride: "Sinta", groom: "Rikardo",
    brideFull: "Sinta Kristina br. Solin, S.Pd.", groomFull: "Rikardo Hotman Angkat, S.T.",
    brideParents: "Putri sulung dari\nBapak Jahotman Solin & Ibu Lasmaria br. Berutu", groomParents: "Putra kedua dari\nBapak St. Robinson Angkat & Ibu Rosdiana br. Padang",
    bridePhoto: "/themes/img/r107.webp", groomPhoto: "/themes/img/r106.webp",
    note: "Seperti kabut pagi yang setia turun di perbukitan Dairi, kiranya kasih kami pun setia, sederhana, dan terus bertumbuh dalam Tuhan.",
  },
  eventLabel: "Pernikahan",
  date: "2027-10-02T09:00:00+07:00",
  place: "Jambur Lae Renun",
  address: "Jl. Pakpak No. 21, Kel. Batang Beruh, Kec. Sidikalang, Kabupaten Dairi",
  stories: [
    { date: "2019", title: "Satu Koor di Sidikalang", body: "Kami bertemu di latihan koor pemuda gereja. Sinta di alto, Rikardo di bas yang selalu datang paling akhir tetapi pulang paling belakang." },
    { date: "2022", title: "Pagi Berkabut di Sitinjo", body: "Sebuah perjalanan pemuda ke Taman Wisata Iman Sitinjo. Di bawah kabut, obrolan sederhana menjadi janji untuk saling menunggu." },
    { date: "Mei 2027", title: "Kedua Keluarga Bersepakat", body: "Keluarga Angkat datang menyampaikan maksud baik kepada keluarga Solin, dan kedua pihak sepakat melangkah ke pesta merbayo." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-10-02T09:00:00+07:00", time: "09.00 – 11.00 WIB", venue: "Gereja GKPPD Sidikalang", address: "Jl. Sisingamangaraja No. 45, Kec. Sidikalang, Kabupaten Dairi" },
    { name: "Merbayo (Pesta Adat Pakpak)", date: "2027-10-02T12:00:00+07:00", time: "12.00 WIB – selesai", venue: "Jambur Lae Renun", address: "Jl. Pakpak No. 21, Kel. Batang Beruh, Kec. Sidikalang, Kabupaten Dairi" },
  ],
  gallery: ["/themes/img/a116.webp", "/themes/img/a30.webp", "/themes/img/a64.webp", "/themes/img/r81.webp"],
  gifts: [
    { id: "demo-sumut", type: "bank", bank_name: "Bank Sumut", account_number: "2030 1144 5678", account_name: "Sinta Kristina Solin" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0129 0100 4471 502", account_name: "Rikardo Hotman Angkat" },
    { id: "demo-kado", type: "address", address: "Jl. Sudirman Gg. Kopi No. 7, Kel. Bintang Hulu, Kec. Sidikalang, Kabupaten Dairi 22212", account_name: "Keluarga Jahotman Solin" },
  ],
  guestName: "Bapak Pdt. Marulam Berutu & Keluarga",
  guestTable: "Meja Oles 4",
  extras: {
    quote: { text: "Dan bilamana seorang dapat dialahkan, dua orang akan dapat bertahan. Tali tiga lembar tak mudah diputuskan.", source: "Pengkhotbah 4:12" },
    rundown: { items: [
      { time: "12.00", title: "Penyambutan rombongan kedua keluarga", note: "Diiringi gendang dan gong Pakpak" },
      { time: "12.45", title: "Penyerahan oles", note: "Kain oles diselempangkan kepada kedua pengantin" },
      { time: "13.30", title: "Makan bersama", note: "Pelleng dan nditak khas Pakpak" },
      { time: "15.00", title: "Menari bersama & doa penutup" },
    ] },
    dressCode: { note: "Busana rapi. Nuansa hijau lembut, merah oles, hitam, atau putih dipersilakan.", colors: ["#3f6b45", "#b2302a", "#1d1a1a", "#f2ece0"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Solin – Berutu", "Kel. Besar Angkat – Padang"] },
  },
});

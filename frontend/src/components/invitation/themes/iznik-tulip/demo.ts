import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Aisyah", groom: "Rizal",
    brideFull: "Aisyah Nur Rahmania, S.Sn.", groomFull: "Rizal Maulana Pratama, S.E.",
    brideParents: "Putri kedua dari\nBapak H. Mukhlis Effendi & Ibu Hj. Ratna Juwita",
    groomParents: "Putra ketiga dari\nBapak Drs. H. Syamsul Arifin & Ibu Hj. Nurul Hikmah",
    bridePhoto: "/themes/img/a19.webp", groomPhoto: "/themes/img/a20.webp",
    note: "Seperti tulip yang tumbuh dari satu tangkai, semoga cinta kami tumbuh lurus dalam naungan ridha-Nya.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-04-17T10:00:00+07:00",
  place: "Masjid Pusdai Jawa Barat",
  address: "Jl. Diponegoro No. 63, Cihaur Geulis, Cibeunying Kaler, Bandung",
  stories: [
    { date: "2020", title: "Kelas Keramik", body: "Aisyah mengajar melukis keramik di Bandung, Rizal datang sebagai murid yang paling sering memecahkan cangkir." },
    { date: "2025", title: "Ta'aruf", body: "Lewat kakak Rizal, kami dipertemukan kembali dan berkenalan dengan cara yang baik." },
    { date: "Januari 2027", title: "Lamaran", body: "Dua keluarga bertemu, menyatukan niat, dan menetapkan hari bahagia." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-04-17T08:00:00+07:00", time: "08.00 – 09.00 WIB", venue: "Masjid Pusdai Jawa Barat", address: "Jl. Diponegoro No. 63, Cihaur Geulis, Cibeunying Kaler, Bandung" },
    { name: "Walimah", date: "2027-04-17T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Sate — Aula Barat", address: "Jl. Diponegoro No. 22, Citarum, Bandung Wetan, Bandung" },
  ],
  gallery: ["/themes/img/a18.webp", "/themes/img/a19.webp", "/themes/img/a20.webp", "/themes/img/a26.webp"],
  gifts: [
    { id: "demo-bca", type: "bank", bank_name: "BCA Syariah", account_number: "0612 3344 55", account_name: "Aisyah Nur Rahmania" },
    { id: "demo-ovo", type: "ewallet", ewallet_provider: "ovo", ewallet_number: "085722110099", account_name: "Rizal Maulana Pratama" },
  ],
  guestName: "Bapak Dr. Hendra Gunawan & Keluarga",
  guestTable: "Meja Lale 7",
  extras: {
    quote: { text: "Dan nikahkanlah orang-orang yang masih membujang di antara kamu... Jika mereka miskin, Allah akan memberi kemampuan kepada mereka dengan karunia-Nya.", source: "QS. An-Nur: 32" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "09.00", title: "Sungkeman & doa" },
      { time: "11.00", title: "Walimah dibuka" },
      { time: "12.30", title: "Foto bersama" },
    ] },
    dressCode: { note: "Busana muslim santun. Biru kobalt, toska, putih, atau merah bata dipersilakan.", colors: ["#1f3f9a", "#2a95a3", "#f7f4ec", "#c43a2c"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-04-17T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Mukhlis Effendi", "Kel. Besar Drs. H. Syamsul Arifin"] },
  },
});

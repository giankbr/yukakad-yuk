import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Lestari", groom: "Jonatan",
    brideFull: "Lestari Natalia br. Purba, S.Pd.", groomFull: "Jonatan Hamonangan Saragih, S.T.",
    brideParents: "Putri sulung dari\nBapak Japaten Purba & Ibu Marlina br. Damanik", groomParents: "Putra kedua dari\nBapak St. Mansen Saragih & Ibu Rosmawati br. Sinaga",
    bridePhoto: "/themes/img/r28.webp", groomPhoto: "/themes/img/r29.webp",
    note: "Seperti hiou yang ditenun benang demi benang, biarlah kasih kami dirajut dengan sabar dan diberkati Tuhan sepanjang hidup.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-14T10:00:00+07:00",
  place: "GKPS Parapat",
  address: "Jl. Sisingamangaraja, Parapat, Girsang Sipangan Bolon, Simalungun, Sumatera Utara",
  stories: [
    { date: "2020", title: "Paduan Suara Naposo", body: "Kami bertemu saat latihan paduan suara pemuda gereja. Jonatan di barisan tenor, Lestari yang selalu memegang partitur." },
    { date: "2025", title: "Lamaran", body: "Keluarga kami bertemu dan berbincang dengan hangat. Restu orang tua dan sanak saudara mengantar langkah kami." },
    { date: "2027", title: "Pemberkatan Nikah", body: "Di tepi Danau Toba, kami mengikat janji di hadapan Tuhan dan jemaat, didampingi keluarga besar." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-08-14T10:00:00+07:00", time: "10.00 – 11.30 WIB", venue: "GKPS Parapat", address: "Jl. Sisingamangaraja, Parapat, Girsang Sipangan Bolon, Simalungun" },
    { name: "Pesta Adat Simalungun", date: "2027-08-14T13:00:00+07:00", time: "13.00 – selesai", venue: "Gedung Serbaguna GKPS Parapat", address: "Jl. Kolonel Simanjuntak, Parapat, Girsang Sipangan Bolon, Simalungun" },
  ],
  gallery: ["/themes/img/r104.webp", "/themes/img/a23.webp", "/themes/img/r13.webp", "/themes/img/r79.webp", "/themes/img/r82.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "3301 0102 7741 508", account_name: "Lestari Natalia Purba" },
    { id: "demo-sumut", type: "bank", bank_name: "Bank Sumut", account_number: "220 01 04 118823 7", account_name: "Jonatan H. Saragih" },
  ],
  guestName: "Bapak Pdt. Rudolf Sinaga & Keluarga",
  guestTable: "Meja Tondong 4",
  extras: {
    quote: { text: "Demikianlah mereka bukan lagi dua, melainkan satu. Karena itu, apa yang telah dipersatukan Allah, tidak boleh diceraikan manusia.", source: "Matius 19:6" },
    rundown: { items: [
      { time: "13.00", title: "Penyambutan rombongan keluarga", note: "Diiringi gonrang sipitu-pitu" },
      { time: "13.45", title: "Doa makan & santap bersama" },
      { time: "14.30", title: "Penyerahan hiou dan ucapan adat" },
      { time: "16.30", title: "Foto bersama" },
    ] },
    dressCode: { note: "Busana resmi. Hiou dan bulang dipersilakan; merah tua, hitam, dan putih gading.", colors: ["#7a1a22", "#221a18", "#efe6d2", "#4f6e7e"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-08-14T10:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Japaten Purba", "Kel. Besar St. Mansen Saragih"] },
  },
});

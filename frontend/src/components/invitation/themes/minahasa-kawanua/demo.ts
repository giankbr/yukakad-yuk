import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Gracia", groom: "Kevin",
    brideFull: "Gracia Natalia Rumengan, S.E.", groomFull: "Kevin Alfrits Pangemanan, S.T.",
    brideParents: "Putri kedua dari\nBapak Johny Rumengan & Ibu Meiske Lumanauw", groomParents: "Putra sulung dari\nBapak Ferry Pangemanan & Ibu Deetje Sumampouw",
    bridePhoto: "/themes/img/a77.webp", groomPhoto: "/themes/img/a76.webp",
    note: "Seperti mapalus, kami percaya rumah tangga dibangun bersama-sama: saling menopang, saling bekerja, saling mendoakan.",
  },
  eventLabel: "Pernikahan",
  date: "2027-05-15T10:00:00+08:00",
  place: "Gedung Kawanua Convention, Manado",
  address: "Jl. Piere Tendean No. 88, Wenang, Kota Manado, Sulawesi Utara",
  stories: [
    { date: "2018", title: "Festival Bunga Tomohon", body: "Kevin menjadi relawan di parade bunga; Gracia menghias kendaraan hias jemaat. Kami berkenalan di antara ribuan krisan." },
    { date: "2022", title: "Pantai Malalayang", body: "Setiap Sabtu sore kami duduk di Malalayang menunggu matahari tenggelam di balik Manado Tua, ditemani pisang goroho." },
    { date: "2026", title: "Maso Minta", body: "Keluarga Pangemanan datang dari Tomohon untuk meminang. Dua keluarga besar sepakat dan saling berpelukan." },
  ],
  events: [
    { name: "Pemberkatan Nikah", date: "2027-05-15T10:00:00+08:00", time: "10.00 – 11.30 WITA", venue: "Gereja GMIM Sion Tomohon", address: "Jl. Raya Tomohon, Kolongan, Tomohon Tengah, Kota Tomohon" },
    { name: "Resepsi", date: "2027-05-15T18:00:00+08:00", time: "18.00 – 21.00 WITA", venue: "Gedung Kawanua Convention", address: "Jl. Piere Tendean No. 88, Wenang, Kota Manado" },
  ],
  gallery: ["/themes/img/a18.webp", "/themes/img/r8.webp", "/themes/img/a77.webp", "/themes/img/r1.webp", "/themes/img/a76.webp", "/themes/img/a26.webp"],
  gifts: [
    { id: "demo-bni", type: "bank", bank_name: "BNI", account_number: "0812 3456 78", account_name: "Gracia Natalia Rumengan" },
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0071 0100 4521 507", account_name: "Kevin Alfrits Pangemanan" },
    { id: "demo-kado", type: "address", address: "Jl. Walanda Maramis No. 12, Matani, Tomohon 95441" },
  ],
  guestName: "Bapak Hendrik Mandagi & Keluarga",
  guestTable: "Meja Lokon 4",
  extras: {
    rundown: { items: [
      { time: "18.00", title: "Kedatangan pengantin", note: "Diiringi tari Maengket" },
      { time: "18.30", title: "Doa & sambutan keluarga" },
      { time: "19.00", title: "Makan bersama", note: "Tinutuan, ayam woku, dan klappertaart" },
      { time: "20.00", title: "Dansa & foto bersama" },
    ] },
    dressCode: { note: "Batik atau kain bentenan. Merah, hitam, dan emas dipersilakan.", colors: ["#a8231f", "#17100d", "#bf8f3a", "#efe2c6"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-05-15T10:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Rumengan – Lumanauw (Manado)", "Kel. Besar Pangemanan – Sumampouw (Tomohon)"] },
  },
});

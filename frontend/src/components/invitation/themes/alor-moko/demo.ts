import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nurhayati", groom: "Rizal",
    brideFull: "Nurhayati Bota, S.Pd.", groomFull: "Muhammad Rizal Djou, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Abdullah Bota & Ibu Siti Aminah Lakapu", groomParents: "Putra sulung dari\nBapak Usman Djou & Ibu Hadijah Maro",
    bridePhoto: "/themes/img/r57.webp", groomPhoto: "/themes/img/r58.webp",
    note: "Seperti moko yang diwariskan turun-temurun, semoga ikatan ini terjaga dan bernilai sepanjang hayat.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-21T08:00:00+08:00",
  place: "Gedung Serbaguna Kalabahi",
  address: "Jl. Soekarno-Hatta, Kalabahi Kota, Teluk Mutiara, Kabupaten Alor",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2019", title: "Senja di Pantai Maimol", body: "Kami berkenalan saat bersih-bersih pantai bersama komunitas pemuda Kalabahi. Air yang jernih jadi saksi obrolan pertama." },
    { date: "2024", title: "Merantau dan pulang", body: "Rizal bertugas di Kupang, Nurhayati mengajar di Alor Kecil. Jarak membuat kami belajar setia dan sabar." },
    { date: "2027", title: "Moko diantar", body: "Keluarga besar duduk bersama, belis moko diantar dengan hormat, dan kedua keluarga sepakat menyatukan kami." },
  ],
  events: [
    { name: "Antar Belis Moko", date: "2027-08-20T16:00:00+08:00", time: "16.00 – 18.00 WITA", venue: "Kediaman Keluarga Bota", address: "Jl. Diponegoro, Kel. Kalabahi Tengah, Teluk Mutiara, Kabupaten Alor" },
    { name: "Akad Nikah", date: "2027-08-21T08:00:00+08:00", time: "08.00 – 09.30 WITA", venue: "Masjid Al-Ikhlas Binongko", address: "Kel. Binongko, Teluk Mutiara, Kalabahi, Kabupaten Alor" },
    { name: "Resepsi", date: "2027-08-21T11:00:00+08:00", time: "11.00 – 14.00 WITA", venue: "Gedung Serbaguna Kalabahi", address: "Jl. Soekarno-Hatta, Kalabahi Kota, Teluk Mutiara, Kabupaten Alor" },
  ],
  gallery: ["/themes/img/r110.webp", "/themes/img/r109.webp", "/themes/img/r38.webp", "/themes/img/r105.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0412 0100 5566 501", account_name: "Nurhayati Bota" },
    { id: "demo-kado", type: "address", address: "Jl. Diponegoro No. 21, Kel. Kalabahi Tengah, Teluk Mutiara, Kabupaten Alor, NTT 85811" },
  ],
  guestName: "Bapak Hamzah Lamma & Keluarga",
  guestTable: "Meja Moko 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Kedatangan tamu", note: "Disambut tarian lego-lego" },
      { time: "11.30", title: "Doa dan sambutan keluarga" },
      { time: "12.00", title: "Ramah tamah dan santap siang" },
      { time: "13.15", title: "Foto bersama per rombongan" },
    ] },
    dressCode: { note: "Busana muslim atau tenun ikat Alor. Biru laut, merah karat, dan krem dipersilakan.", colors: ["#0f5e66", "#a8462a", "#efe2c6", "#1c2440"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Abdullah Bota", "Kel. Besar Usman Djou", "Keluarga Besar Lakapu & Maro"] },
    faq: { items: [
      { q: "Apakah tamu dari luar Alor perlu menginap?", a: "Penerbangan Kupang–Kalabahi tersedia setiap hari. Keluarga membantu informasi penginapan di sekitar Kalabahi." },
      { q: "Bolehkah membawa anak?", a: "Tentu, anak-anak sangat diterima. Tersedia tempat duduk keluarga di gedung." },
    ] },
  },
});

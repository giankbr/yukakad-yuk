import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Zahira", groom: "Fadli",
    brideFull: "Nyimas Ayu Zahira Ramadhani, S.E.", groomFull: "Kemas Muhammad Fadli Akbar, S.T.",
    brideParents: "Putri kedua dari\nBapak Kgs. H. Abdul Rozak & Ibu Nyimas Hj. Fatimah", groomParents: "Putra sulung dari\nBapak Kms. H. Syamsul Bahri & Ibu Hj. Rosmala Dewi",
    bridePhoto: "/themes/img/a62.webp", groomPhoto: "/themes/img/a63.webp",
    note: "Seperti rumah limas yang berdiri di atas tiang-tiang kokoh di tepi Musi, semoga rumah tangga kami teguh, teduh, dan terbuka bagi keluarga.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-19T08:00:00+07:00",
  place: "Gedung Serbaguna Musi Raya",
  address: "Jl. Merdeka No. 11, Talang Semut, Bukit Kecil, Kota Palembang",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2020", title: "Bertemu di Tepian Musi", body: "Kami berkenalan saat sama-sama menjadi panitia lomba perahu bidar di depan Benteng Kuto Besak." },
    { date: "2025", title: "Berkenalan Keluarga", body: "Keluarga Fadli datang bersilaturahmi ke rumah di 26 Ilir, disambut pempek dan kue maksuba buatan nenek." },
    { date: "2027", title: "Mutus Kato", body: "Kedua keluarga sepakat menentukan hari baik. Insyaallah kami melangkah ke akad dengan restu orang tua." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-19T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Palembang", address: "Jl. Jenderal Sudirman, 19 Ilir, Bukit Kecil, Kota Palembang" },
    { name: "Resepsi", date: "2027-06-19T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Serbaguna Musi Raya", address: "Jl. Merdeka No. 11, Talang Semut, Bukit Kecil, Kota Palembang" },
  ],
  gallery: ["/themes/img/a40.webp", "/themes/img/a62.webp", "/themes/img/a63.webp", "/themes/img/a26.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7140 2027 19", account_name: "Nyimas Ayu Zahira Ramadhani" },
    { id: "demo-kado", type: "address", address: "Jl. Kapten Rivai Lr. Limas No. 8, 26 Ilir, Bukit Kecil, Kota Palembang 30121" },
  ],
  guestName: "Bapak H. Hendra Saputra & Keluarga",
  guestTable: "Meja Limas 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Arak-arakan pengantin", note: "Disambut tari Gending Sriwijaya" },
      { time: "11.30", title: "Pengantin duduk bersanding" },
      { time: "12.00", title: "Ramah tamah & santap siang", note: "Pindang patin dan pempek khas Palembang" },
      { time: "13.00", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Busana muslim resmi. Merah marun, emas, dan hitam dipersilakan; songket sangat dinanti.", colors: ["#8e1c1c", "#d4a343", "#1c0f0c", "#f3e6cc"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-06-19T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Kgs. H. Abdul Rozak", "Kel. Besar Kms. H. Syamsul Bahri", "Zuriat Kemas & Kiagus 26 Ilir"] },
  },
});

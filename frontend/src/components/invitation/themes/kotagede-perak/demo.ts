import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Galuh", groom: "Fajar",
    brideFull: "Galuh Ratnaningtyas, S.Sn.", groomFull: "Muhammad Fajar Prasetyo, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Suharjono & Ibu Hj. Siti Rahayu", groomParents: "Putra sulung dari\nBapak Drs. Bambang Wiryawan & Ibu Endang Sulastri",
    bridePhoto: "/themes/img/a28.webp", groomPhoto: "/themes/img/a29.webp",
    note: "Seperti perak yang ditempa dengan sabar menjadi filigri, semoga cinta kami ditempa waktu menjadi indah dan kuat.",
  },
  eventLabel: "Pernikahan",
  date: "2027-08-14T08:00:00+07:00",
  place: "Pendapa Omah Kalang",
  address: "Jl. Tegalgendu No. 20, Prenggan, Kotagede, Yogyakarta",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "2020", title: "Bengkel Perak di Gang Rukunan", body: "Fajar datang memesan cincin untuk ibunya; Galuh yang sedang belajar memilin kawat perak di bengkel ayahnya melayani pesanan itu." },
    { date: "2023", title: "Memilin Kawat, Merangkai Rencana", body: "Setiap Sabtu pagi kami menyusuri gang-gang Kotagede, sarapan kipo dan bercerita tentang rumah yang ingin kami bangun." },
    { date: "2027", title: "Akad di Masjid Gedhe", body: "Dengan restu kedua keluarga, kami memilih Masjid Gedhe Mataram untuk mengikat janji suci." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-08-14T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Gedhe Mataram Kotagede", address: "Jl. Watu Gilang, Jagalan, Banguntapan, Bantul, Yogyakarta" },
    { name: "Resepsi", date: "2027-08-14T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Pendapa Omah Kalang", address: "Jl. Tegalgendu No. 20, Prenggan, Kotagede, Yogyakarta" },
  ],
  gallery: ["/themes/img/a31.webp", "/themes/img/a24.webp", "/themes/img/a28.webp", "/themes/img/a29.webp", "/themes/img/r56.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7123 4567 89", account_name: "Galuh Ratnaningtyas" },
    { id: "demo-bpd", type: "bank", bank_name: "BPD DIY", account_number: "001 211 004567", account_name: "Muhammad Fajar Prasetyo" },
    { id: "demo-kado", type: "address", address: "Jl. Mondorakan No. 51, Prenggan, Kotagede, Yogyakarta 55172" },
  ],
  guestName: "Bapak H. Joko Santoso & Keluarga",
  guestTable: "Meja Filigri 4",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kebesaran-Nya ialah Dia menciptakan pasangan-pasangan untukmu dari jenismu sendiri, agar kamu cenderung dan merasa tenteram kepadanya, dan Dia menjadikan di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "11.00", title: "Kirab pengantin dari ujung gang", note: "Diiringi gamelan pakurmatan" },
      { time: "11.30", title: "Upacara panggih" },
      { time: "12.00", title: "Ramah tamah & santap siang" },
      { time: "13.30", title: "Foto bersama keluarga" },
    ] },
    dressCode: { note: "Batik atau busana Jawa. Nuansa abu perak, hijau toska, dan putih tulang dipersilakan.", colors: ["#9aa3a3", "#2c5a5c", "#e9ece6", "#24393b"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-08-14T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Suharjono (Prenggan, Kotagede)", "Kel. Besar Drs. Bambang Wiryawan (Banguntapan)"] },
    travel: { note: "Gang Kotagede sempit; kendaraan roda empat sebaiknya parkir di luar kawasan.", items: [
      { name: "Parkir Pasar Legi Kotagede", detail: "± 5 menit jalan kaki ke Pendapa Omah Kalang" },
      { name: "Dari Stasiun Tugu", detail: "± 25 menit berkendara ke Kotagede" },
    ] },
  },
});

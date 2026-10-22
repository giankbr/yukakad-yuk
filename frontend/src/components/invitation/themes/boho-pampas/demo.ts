import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Ayu", groom: "Wira",
    brideFull: "Ni Luh Putu Ayu Saraswati, S.Ds.", groomFull: "I Made Wira Adnyana, S.T.",
    brideParents: "Putri pertama dari\nBapak I Nyoman Sudarsana & Ibu Ni Made Rai Wartini", groomParents: "Putra kedua dari\nBapak I Wayan Sukerta & Ibu Ni Ketut Sriasih",
    bridePhoto: "/themes/img/r107.webp", groomPhoto: "/themes/img/r106.webp",
    note: "Sederhana seperti rumput kering di tepi tebing: ringan, hangat, dan selalu menari bersama angin.",
  },
  eventLabel: "Pawiwahan",
  date: "2027-07-24T09:00:00+08:00",
  place: "Tebing Karang Boma, Uluwatu",
  address: "Jl. Pantai Suluban, Pecatu, Kuta Selatan, Badung, Bali",
  stories: [
    { date: "2019", title: "Lokakarya Rotan di Ubud", body: "Ayu mengajar menganyam rotan, Wira datang sebagai murid yang paling sering salah simpul." },
    { date: "2022", title: "Studio Kecil di Canggu", body: "Kami membuka studio dekorasi bersama: makrame, bunga kering, dan banyak kopi sore." },
    { date: "2026", title: "Ngidih di Rumah Keluarga", body: "Keluarga Wira datang memohon restu. Pampas pertama di rumah kami berasal dari hari itu." },
  ],
  events: [
    { name: "Upacara Pawiwahan", date: "2027-07-24T09:00:00+08:00", time: "09.00 – 11.30 WITA", venue: "Griya Keluarga Sukerta", address: "Jl. Tukad Badung No. 18, Renon, Denpasar Selatan, Bali" },
    { name: "Resepsi Senja", date: "2027-07-24T17:00:00+08:00", time: "17.00 – 20.30 WITA", venue: "Tebing Karang Boma, Uluwatu", address: "Jl. Pantai Suluban, Pecatu, Kuta Selatan, Badung, Bali" },
  ],
  gallery: ["/themes/img/r10.webp", "/themes/img/r16.webp", "/themes/img/r108.webp", "/themes/img/r15.webp", "/themes/img/r109.webp", "/themes/img/r11.webp"],
  gifts: [
    { id: "demo-bpd", type: "bank", bank_name: "BPD Bali", account_number: "0180 2011 5531", account_name: "Ni Luh Putu Ayu Saraswati" },
    { id: "demo-bca", type: "bank", bank_name: "BCA", account_number: "6110 4478 02", account_name: "I Made Wira Adnyana" },
    { id: "demo-kado", type: "address", address: "Jl. Tukad Badung No. 18, Renon, Denpasar Selatan, Bali 80226" },
  ],
  guestName: "Bapak Komang Arya & Keluarga",
  guestTable: "Meja Pampas 4",
  extras: {
    quote: { text: "Wahai pasangan suami istri, semoga kalian tetap bersatu dan tidak pernah terpisahkan. Semoga kalian mencapai hidup penuh kebahagiaan, tinggal di rumah yang penuh kegembiraan bersama anak dan cucu.", source: "Rgveda X.85.42" },
    rundown: { items: [
      { time: "17.00", title: "Welcome drink & musik akustik", note: "Taman tebing" },
      { time: "17.45", title: "Prosesi masuk pengantin" },
      { time: "18.15", title: "Makan malam saat matahari terbenam" },
      { time: "19.30", title: "Dansa & api unggun" },
    ] },
    dressCode: { note: "Boho santai bernuansa pasir, krem, dan kayu manis. Sepatu datar disarankan karena area rumput.", colors: ["#f1e8da", "#dcc9a8", "#a8673f", "#5b4636"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. I Nyoman Sudarsana", "Kel. Besar Bpk. I Wayan Sukerta"] },
    travel: { note: "Untuk tamu dari luar Bali, berikut beberapa pilihan terdekat dari lokasi resepsi.", items: [
      { name: "Bandara I Gusti Ngurah Rai", detail: "± 35 menit berkendara ke Uluwatu" },
      { name: "Shuttle tamu", detail: "Dari Jimbaran pukul 16.00 dan 16.30 WITA" },
    ] },
  },
});

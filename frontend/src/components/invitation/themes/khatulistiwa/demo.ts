import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadia", groom: "Haikal",
    brideFull: "Dayang Nadia Safitri, S.Pd.", groomFull: "Wan Muhammad Haikal, S.T.",
    brideParents: "Putri bungsu dari\nBapak H. Abang Ismail & Ibu Hj. Dayang Rosnah", groomParents: "Putra sulung dari\nBapak Wan Zulkifli & Ibu Siti Aminah",
    bridePhoto: "/themes/img/a72.webp", groomPhoto: "/themes/img/a63.webp",
    note: "Di hari matahari tegak di atas khatulistiwa, kami memulai satu bayangan bersama.",
  },
  eventLabel: "Pernikahan",
  date: "2027-03-21T08:00:00+07:00",
  place: "Rumah Adat Melayu Kalimantan Barat",
  address: "Jl. Sutan Syahrir No. 1, Kota Baru, Pontianak Selatan, Kota Pontianak",
  stories: [
    { date: "2019", title: "Satu Speedboat", body: "Kami pertama bertemu di dermaga Kapuas Indah, berbagi bangku speedboat menuju Siantan saat hujan sore." },
    { date: "2024", title: "Merisik & Meminang", body: "Keluarga Haikal datang merisik, lalu meminang dengan tepak sirih dan restu kedua keluarga besar." },
    { date: "2027", title: "Hari Kulminasi", body: "Kami memilih hari ketika bayangan tugu menghilang di siang hari: hari baik untuk memulai yang baru." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-03-21T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Raya Mujahidin", address: "Jl. Jenderal Ahmad Yani, Bansir Laut, Pontianak Tenggara, Kota Pontianak" },
    { name: "Resepsi & Makan Saprahan", date: "2027-03-21T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Rumah Adat Melayu Kalimantan Barat", address: "Jl. Sutan Syahrir No. 1, Kota Baru, Pontianak Selatan, Kota Pontianak" },
  ],
  gallery: ["/themes/img/a118.webp", "/themes/img/a72.webp", "/themes/img/a63.webp", "/themes/img/a26.webp"],
  gifts: [
    { id: "demo-kalbar", type: "bank", bank_name: "Bank Kalbar", account_number: "1012 3456 78", account_name: "Dayang Nadia Safitri" },
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7123 4567 89", account_name: "Wan Muhammad Haikal" },
    { id: "demo-kado", type: "address", address: "Jl. Tanjung Raya II Gg. Saleh No. 12, Parit Mayor, Pontianak Timur 78232" },
  ],
  guestName: "Bapak H. Syarif Hamid & Keluarga",
  guestTable: "Saprah 7",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Masjid Raya Mujahidin" },
      { time: "10.30", title: "Arak-arakan pengantin", note: "Diiringi tar dan hadrah" },
      { time: "11.00", title: "Tepung tawar" },
      { time: "12.00", title: "Makan saprahan", note: "Duduk bersila, satu saprah enam orang" },
    ] },
    dressCode: { note: "Busana Melayu: teluk belanga, baju kurung, atau tenun corak insang.", colors: ["#a8322b", "#d6a53a", "#1d5b5e", "#f4ead2"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-03-21T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Abang Ismail", "Kel. Besar Wan Zulkifli"] },
    travel: { note: "Untuk tamu dari luar Pontianak, berikut beberapa pilihan.", items: [
      { name: "Penginapan di Jl. Gajah Mada", detail: "± 10 menit dari lokasi resepsi" },
      { name: "Wisata Tugu Khatulistiwa", detail: "Sehari sebelum acara, rombongan keluarga berkunjung pukul 11.00 WIB" },
    ] },
  },
});

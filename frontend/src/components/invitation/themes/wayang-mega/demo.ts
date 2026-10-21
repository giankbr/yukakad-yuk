import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Ratri", groom: "Satriya",
    brideFull: "Ratri Wening Ayu, S.Pd.", groomFull: "Satriya Bagus Wicaksana, S.T.",
    brideParents: "Putri kedua dari\nBapak Sugiyanto & Ibu Warsini", groomParents: "Putra bungsu dari\nBapak Tarjo Atmojo & Ibu Sumiyati",
  },
  eventLabel: "Pernikahan",
  date: "2027-07-10T09:00:00+07:00",
  place: "Pendopo Kabupaten Cirebon",
  address: "Jl. Kartini No. 1, Kebonbaru, Kejaksan, Kota Cirebon",
  stories: [
    { date: "2018", title: "Pentas Wayang", body: "Dipertemukan di pentas wayang semalam suntuk di alun-alun. Satriya menabuh, Ratri menyanyikan sinden." },
    { date: "2022", title: "Lakon Kami", body: "Seperti lakon yang panjang, kami belajar sabar menunggu waktu yang tepat." },
    { date: "2026", title: "Lamaran", body: "Dua keluarga berkumpul di Cirebon, menyepakati hari yang baik untuk kami." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-07-10T09:00:00+07:00", time: "09.00 – 10.00 WIB", venue: "Masjid At-Taqwa", address: "Jl. Kartini No. 4, Kebonbaru, Kejaksan, Kota Cirebon" },
    { name: "Resepsi", date: "2027-07-10T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Pendopo Kabupaten Cirebon", address: "Jl. Kartini No. 1, Kebonbaru, Kejaksan, Kota Cirebon" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7123 4567 89", account_name: "Ratri Wening Ayu" },
    { id: "demo-kado", type: "address", address: "Jl. Pekiringan No. 21, Kesepuhan, Lemahwungkuk, Kota Cirebon" },
  ],
  guestName: "Bapak Darsono & Keluarga",
  extras: {
    dressCode: { note: "Batik mega mendung atau nuansa terakota, krem, dan sogan.", colors: ["#b4532f", "#e6d8b8", "#7a4a26", "#2f5a4a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar Bpk. Sugiyanto", "Kel. Besar Bpk. Tarjo Atmojo", "Sanggar Wayang Kulit Purbalingga"] },
  },
});

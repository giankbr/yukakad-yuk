import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Hanum", groom: "Fathan",
    brideFull: "Hanum Salsabila Az-Zahra, S.Psi.", groomFull: "Muhammad Fathan Al-Ghifari, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Ridwan Kamaluddin & Ibu Hj. Siti Maryam", groomParents: "Putra sulung dari\nBapak Drs. Ahmad Syarifuddin & Ibu Nur Aini",
    note: "Seperti sakura yang mekar pada musimnya, kami percaya setiap pertemuan datang tepat pada waktu yang Allah tetapkan.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-04-17T08:00:00+07:00",
  place: "Graha Kemuning",
  address: "Jl. Dipatiukur No. 88, Lebakgede, Coblong, Kota Bandung",
  story: { title: "Kisah Kami", body: "" },
  stories: [
    { date: "Ramadan 2024", title: "Satu Majelis Ilmu", body: "Kami pertama kali mengenal nama satu sama lain sebagai panitia kajian remaja masjid di Bandung." },
    { date: "Syawal 2026", title: "Ta'aruf", body: "Dengan perantara guru ngaji kami, Fathan menyampaikan niat baiknya. Kami bertukar biodata dan sama-sama memohon petunjuk." },
    { date: "Rabiul Awal 2027", title: "Khitbah", body: "Keluarga Fathan datang bersilaturahmi ke rumah. Lamaran diterima dengan penuh syukur." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-04-17T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Al-Ukhuwwah", address: "Jl. Wastukencana No. 27, Babakan Ciamis, Sumur Bandung, Kota Bandung" },
    { name: "Walimah", date: "2027-04-17T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Graha Kemuning", address: "Jl. Dipatiukur No. 88, Lebakgede, Coblong, Kota Bandung" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7204 1188 52", account_name: "Hanum Salsabila Az-Zahra" },
    { id: "demo-kado", type: "address", address: "Jl. Cisitu Lama No. 14, Dago, Coblong, Kota Bandung 40135" },
  ],
  guestName: "Ibu Hj. Khadijah Rahmawati & Keluarga",
  guestTable: "Meja Kemuning 3",
  extras: {
    quote: { text: "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu pasangan dari jenismu sendiri, supaya kamu merasa tenteram kepadanya, dan dijadikan-Nya di antaramu rasa kasih dan sayang.", source: "QS. Ar-Rum: 21" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "09.00", title: "Tausiyah pernikahan" },
      { time: "11.00", title: "Walimah dibuka", note: "Tamu putra dan putri di ruang terpisah" },
      { time: "13.30", title: "Doa penutup" },
    ] },
    dressCode: { note: "Busana muslim yang sopan. Nuansa merah muda pucat, krem, dan hijau sage dipersilakan.", colors: ["#f2c9d2", "#f6ece3", "#a7b298", "#8e4358"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Ridwan Kamaluddin", "Kel. Besar Drs. Ahmad Syarifuddin"] },
    faq: { items: [
      { q: "Apakah tamu putra dan putri dipisah?", a: "Ya, ruang walimah dibagi untuk tamu putra dan putri, masing-masing dengan pintu masuk sendiri." },
      { q: "Apakah tersedia musala?", a: "Tersedia musala dan tempat wudu di lantai dasar Graha Kemuning." },
    ] },
  },
});

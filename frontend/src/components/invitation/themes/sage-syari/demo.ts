import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Alya", groom: "Rasyid",
    brideFull: "Alya Nur Hasanah, S.Pd.", groomFull: "Muhammad Rasyid Ridha, S.T.",
    brideParents: "Putri ketiga dari\nBapak H. Abdul Karim & Ibu Hj. Siti Mardiyah", groomParents: "Putra pertama dari\nBapak Drs. Ahmad Fauzi & Ibu Nur Aini",
    note: "Seperti daun yang mengering tanpa kehilangan wanginya, semoga cinta kami tetap teduh dan tenang di setiap musim.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-09-18T08:00:00+07:00",
  place: "Masjid Agung Jawa Tengah",
  address: "Jl. Gajah Raya, Sambirejo, Gayamsari, Kota Semarang",
  stories: [
    { date: "2023", title: "Satu Majelis", body: "Kami sama-sama mengajar di rumah tahfiz anak di Gayamsari, tanpa banyak bicara selain soal jadwal dan hafalan murid." },
    { date: "2026", title: "Ta'aruf", body: "Melalui ustazah pembimbing, biodata kami dipertukarkan. Dua keluarga bertemu dalam suasana yang hangat dan sederhana." },
    { date: "Maret 2027", title: "Khitbah", body: "Keluarga Rasyid datang ke Pedurungan membawa doa dan seikat daun kayu putih dari kebun ibunya." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-09-18T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Jawa Tengah", address: "Jl. Gajah Raya, Sambirejo, Gayamsari, Kota Semarang" },
    { name: "Walimatul 'Ursy", date: "2027-09-18T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Gedung Grha Sabha Nalendra", address: "Jl. Supriyadi No. 48, Kalicari, Pedurungan, Kota Semarang" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7180 2245 6631", account_name: "Alya Nur Hasanah" },
    { id: "demo-muamalat", type: "bank", bank_name: "Bank Muamalat", account_number: "3310 0087 1452", account_name: "Muhammad Rasyid Ridha" },
    { id: "demo-kado", type: "address", address: "Jl. Pedurungan Kidul IV No. 17, Pedurungan, Kota Semarang 50192", account_name: "Keluarga H. Abdul Karim" },
  ],
  guestName: "Ibu Hj. Fatimah Azzahra & Keluarga",
  guestTable: "Meja Kayu Putih 2",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat kebesaran Allah.", source: "QS. Adz-Dzariyat: 49" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "09.00", title: "Tausiyah pernikahan", note: "Ustaz H. Mahfudz Siddiq" },
      { time: "11.00", title: "Walimah dibuka", note: "Ruang tamu putra & putri terpisah" },
      { time: "13.30", title: "Doa penutup" },
    ] },
    dressCode: { note: "Busana muslim santun bernuansa tenang: sage, krem linen, dan cokelat daun kering.", colors: ["#ecebe2", "#a3b6aa", "#6f8566", "#a77c4a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Abdul Karim", "Kel. Besar Drs. Ahmad Fauzi", "Rumah Tahfiz Al-Hikmah Gayamsari"] },
    faq: { items: [
      { q: "Apakah area tamu putra dan putri dipisah?", a: "Ya, walimah menggunakan ruang terpisah dengan sekat kain linen untuk tamu putra dan putri." },
      { q: "Apakah tersedia tempat salat?", a: "Tersedia musala dan tempat wudu di lantai dasar gedung." },
    ] },
  },
});

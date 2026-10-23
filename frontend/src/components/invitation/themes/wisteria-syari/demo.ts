import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Wardah", groom: "Hafiz",
    brideFull: "Wardah Nur Azizah, S.Pd.", groomFull: "Muhammad Hafiz Ramadhan, S.T.",
    brideParents: "Putri ketiga dari\nBapak H. Imam Syafi'i & Ibu Hj. Siti Maesaroh", groomParents: "Putra pertama dari\nBapak Drs. Abdul Karim & Ibu Nurul Hidayati",
    note: "Seperti untaian wisteria yang tumbuh perlahan pada tiangnya, semoga cinta kami tumbuh bersandar pada rida Allah.",
  },
  eventLabel: "Walimatul 'Ursy",
  date: "2027-04-24T08:00:00+07:00",
  place: "Masjid Raden Patah Universitas Brawijaya",
  address: "Jl. Veteran No. 10, Ketawanggede, Lowokwaru, Kota Malang",
  stories: [
    { date: "2023", title: "Satu Halaqah", body: "Kami dipertemukan sebagai pengajar TPQ di masjid kampus, saling mengenal lewat jadwal mengajar dan rapat wali santri." },
    { date: "2026", title: "Ta'aruf", body: "Melalui ustazah pembimbing, biodata kami dipertukarkan. Setelah istikharah, kedua keluarga bersilaturahmi di Batu." },
    { date: "Januari 2027", title: "Khitbah", body: "Keluarga Hafiz datang ke rumah di Sukun membawa doa, kurma, dan seikat bunga ungu dari kebun nenek." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-04-24T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Raden Patah Universitas Brawijaya", address: "Jl. Veteran No. 10, Ketawanggede, Lowokwaru, Kota Malang" },
    { name: "Walimatul 'Ursy", date: "2027-04-24T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Graha Sakinah Malang", address: "Jl. Soekarno Hatta No. 25, Mojolangu, Lowokwaru, Kota Malang" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "Bank Syariah Indonesia", account_number: "7183 0462 9150", account_name: "Wardah Nur Azizah" },
    { id: "demo-muamalat", type: "bank", bank_name: "Bank Muamalat", account_number: "3410 0275 88", account_name: "Muhammad Hafiz Ramadhan" },
    { id: "demo-kado", type: "address", address: "Jl. Gadang Gg. 3 No. 17, Sukun, Kota Malang 65149", account_name: "Keluarga H. Imam Syafi'i" },
  ],
  guestName: "Ibu Hj. Rofi'ah & Keluarga",
  guestTable: "Meja Wisteria 2",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat kebesaran Allah.", source: "QS. Az-Zariyat: 49" },
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "09.00", title: "Tausiyah pernikahan" },
      { time: "11.00", title: "Walimah dibuka", note: "Area tamu putra & putri terpisah" },
      { time: "13.30", title: "Doa penutup" },
    ] },
    dressCode: { note: "Busana muslim santun bernuansa lembut: ungu muda, lilak, krem, dan hijau sage.", colors: ["#b79ddd", "#5c3f91", "#f4ecdf", "#8fa77a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Imam Syafi'i", "Kel. Besar Drs. Abdul Karim"] },
    faq: { items: [
      { q: "Apakah area tamu putra dan putri dipisah?", a: "Ya, ruang walimah dibagi dengan sekat untuk tamu putra dan putri." },
      { q: "Apakah tersedia tempat salat?", a: "Tersedia musala di lantai dua Graha Sakinah, lengkap dengan mukena." },
    ] },
  },
});

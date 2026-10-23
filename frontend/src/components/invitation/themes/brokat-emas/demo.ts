import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Nadhira", groom: "Rayyan",
    brideFull: "Nadhira Az-Zahra Hamdani", groomFull: "Muhammad Rayyan Alfarizi",
    brideParents: "Putri dari Bapak H. Lutfi Hamdani\n& Ibu Hj. Farida Rachmawati", groomParents: "Putra dari Bapak Ir. H. Arif Budiman\n& Ibu Hj. Sarah Nuraini",
    note: "Dengan izin Allah, dua hati yang saling mendoakan kini dipertemukan dalam ikatan yang suci.",
  },
  eventLabel: "Pernikahan",
  date: "2027-10-16T08:00:00+07:00",
  place: "Masjid Nasional Al-Akbar Surabaya",
  address: "Jl. Masjid Al-Akbar Timur No. 1, Pagesangan, Jambangan, Surabaya",
  story: { title: "Kisah kami", body: "" },
  stories: [
    { date: "2022", title: "Kajian Sabtu Pagi", body: "Kami pertama kali saling tahu di kajian pekanan masjid kampus, duduk di sisi yang berbeda dengan buku catatan yang sama." },
    { date: "2025", title: "Ta'aruf", body: "Melalui perantara guru ngaji, kami bertukar biodata dan bertemu ditemani keluarga." },
    { date: "Mei 2027", title: "Khitbah", body: "Keluarga Rayyan datang melamar. Alhamdulillah diterima dengan penuh kehangatan." },
    { date: "Oktober 2027", title: "Akad", body: "Insyaallah kami menunaikan sunnah, memohon doa agar menjadi keluarga yang sakinah." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-10-16T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Nasional Al-Akbar Surabaya", address: "Jl. Masjid Al-Akbar Timur No. 1, Pagesangan, Jambangan, Surabaya" },
    { name: "Walimatul 'Urs", date: "2027-10-16T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Grand Ballroom Hotel Majapahit", address: "Jl. Tunjungan No. 65, Genteng, Surabaya" },
  ],
  gallery: [],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7161 0201 66", account_name: "Nadhira Az-Zahra Hamdani" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1420 0271 0160", account_name: "Muhammad Rayyan Alfarizi" },
  ],
  guestName: "Ibu Hj. Khadijah Assegaf & Keluarga",
  guestTable: "Meja Zamrud 3",
  extras: {
    quote: { text: "Dan segala sesuatu Kami ciptakan berpasang-pasangan agar kamu mengingat kebesaran Allah.", source: "QS. Adz-Dzariyat: 49" },
    rundown: { items: [
      { time: "11.00", title: "Penyambutan tamu" },
      { time: "11.30", title: "Kirab pengantin & tilawah" },
      { time: "12.00", title: "Tausiyah pernikahan", note: "Ustaz H. Abdullah Mahfudz" },
      { time: "12.30", title: "Ramah tamah & foto bersama" },
    ] },
    dressCode: { note: "Busana muslim formal. Nuansa marun, emas, dan gading.", colors: ["#4a0d1c", "#c99a3e", "#f7efe0", "#2c0610"] },
    rsvpDietary: {},
    family: { names: ["Keluarga Besar H. Lutfi Hamdani", "Keluarga Besar Ir. H. Arif Budiman"] },
    faq: { items: [
      { q: "Apakah tamu pria dan wanita dipisah?", a: "Ya, area resepsi dibagi dua sisi dengan pelaminan di tengah." },
      { q: "Apakah tersedia musala?", a: "Musala tersedia di lantai dasar hotel, dekat lobi utama." },
    ] },
  },
});

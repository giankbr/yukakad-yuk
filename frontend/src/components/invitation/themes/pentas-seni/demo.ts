import { makeDemo } from "../demo-base";

const ART = "/themes/art/pentas-seni";

export const demo = makeDemo({
  couple: {
    bride: "Ibu Ratna", groom: "Pak Bagus",
    brideFull: "Ratna Wulandari, S.Pd., M.Pd.", groomFull: "Bagus Pranowo, S.Sn.",
    brideParents: "Kepala SD Tunas Cendekia, Sleman", groomParents: "Guru Seni Budaya, bersama 24 wali murid relawan",
    note: "Enam bulan latihan, ratusan langkah tari yang diulang, dan satu panggung untuk merayakan keberanian anak-anak kita.",
  },
  eventLabel: "Pentas Seni",
  date: "2027-06-12T08:00:00+07:00",
  place: "Aula SD Tunas Cendekia",
  address: "Jl. Kaliurang Km. 7,5 No. 12, Sinduadi, Mlati, Sleman, Yogyakarta",
  story: { title: "Panggung Pelangi Nusantara", body: "" },
  stories: [
    { date: "08.00", title: "Tari Kipas Kelas 2", body: "Dua puluh penari cilik membuka acara dengan kipas merah-kuning, diiringi gamelan rekaman dari Sanggar Sekar Kedhaton." },
    { date: "08.30", title: "Orkes Angklung Kelas 4", body: "Lagu 'Gundul-Gundul Pacul' dan 'Ampar-Ampar Pisang' dimainkan dengan 36 angklung pinjaman sanggar kecamatan." },
    { date: "09.15", title: "Drama Musikal Kelas 5", body: "Kisah 'Kancil dan Buaya' versi murid sendiri: naskah, kostum kardus, dan lagu-lagunya karya kelas 5." },
    { date: "10.00", title: "Paduan Suara & Penutupan", body: "Seluruh kelas bernyanyi bersama 'Indonesia Pusaka', disusul pembagian piagam untuk semua penampil." },
  ],
  events: [
    { name: "Pentas Seni Akhir Tahun", date: "2027-06-12T08:00:00+07:00", time: "08.00 – 10.30 WIB (pintu dibuka 07.30)", venue: "Aula SD Tunas Cendekia", address: "Jl. Kaliurang Km. 7,5 No. 12, Sinduadi, Mlati, Sleman, Yogyakarta" },
    { name: "Pameran Karya Murid", date: "2027-06-12T10:30:00+07:00", time: "10.30 – 12.00 WIB", venue: "Koridor & Ruang Kelas Lantai 1", address: "SD Tunas Cendekia, Jl. Kaliurang Km. 7,5 No. 12, Sleman" },
  ],
  gallery: [`${ART}/matahari.webp`, `${ART}/pelangi.webp`, `${ART}/rumah.webp`],
  gifts: [
    { id: "demo-komite", type: "bank", bank_name: "BPD DIY", account_number: "0012 3456 7890", account_name: "Komite SD Tunas Cendekia" },
  ],
  guestName: "Bapak/Ibu Wali Murid Ananda Kirana (4B)",
  guestTable: "Baris C",
  extras: {
    faq: { items: [
      { q: "Bolehkah membawa adik atau kakek-nenek?", a: "Boleh sekali. Kursi keluarga tersedia di baris belakang; mohon jaga adik kecil agar tidak naik ke panggung." },
      { q: "Bolehkah merekam penampilan?", a: "Silakan merekam dari tempat duduk tanpa lampu kilat. Rekaman lengkap juga akan dibagikan lewat grup kelas." },
      { q: "Di mana parkir kendaraan?", a: "Parkir motor di halaman sekolah, mobil di lapangan RW sebelah timur sekolah. Dipandu petugas satpam dan wali murid." },
    ] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-06-12T08:00:00+07:00" },
  },
});

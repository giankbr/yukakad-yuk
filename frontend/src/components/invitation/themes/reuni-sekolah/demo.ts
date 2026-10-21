import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Rizky", groom: "Dewi",
    brideFull: "Rizky Aditya Nugroho", groomFull: "Dewi Kartika Sari",
    brideParents: "Alumni XII IPA 2\nKetua OSIS 2006", groomParents: "Alumni XII IPS 1\nRedaksi Majalah Dinding",
    bridePhoto: "/themes/img/a96.webp", groomPhoto: "/themes/img/a99.webp",
    note: "Angkatan 2007 — dua puluh tahun sejak seragam putih abu-abu. Saatnya pulang ke kelas, tertawa lagi bersama.",
  },
  eventLabel: "Reuni Akbar",
  date: "2027-08-14T09:00:00+07:00",
  place: "SMA Tunas Bangsa Malang",
  address: "Jl. Ijen Boulevard No. 27, Oro-oro Dowo, Klojen, Kota Malang",
  story: { title: "Buku Kenangan", body: "" },
  stories: [
    { date: "2004", title: "Hari pertama MOS", body: "Topi kerucut dari karton, papan nama di dada, dan kakak OSIS yang galak tapi baik." },
    { date: "2006", title: "Pentas seni & study tour", body: "Panggung pensi di lapangan basket, lalu bus rombongan ke Bali yang mogok di Banyuwangi." },
    { date: "2007", title: "Lulus bersama", body: "Seragam dicoret pilok warna-warni, janji untuk saling kabar meski merantau jauh." },
    { date: "2027", title: "Dua dekade kemudian", body: "Ada yang jadi dokter, guru, pengusaha, ada yang sudah mengantar anak ke sekolah. Kita kumpul lagi." },
  ],
  events: [
    { name: "Napak Tilas Sekolah", date: "2027-08-14T09:00:00+07:00", time: "09.00 – 12.00 WIB", venue: "SMA Tunas Bangsa Malang", address: "Jl. Ijen Boulevard No. 27, Oro-oro Dowo, Klojen, Kota Malang" },
    { name: "Malam Reuni Akbar", date: "2027-08-14T18:30:00+07:00", time: "18.30 – 22.00 WIB", venue: "Aula Graha Cakrawala", address: "Jl. Semeru No. 5, Kauman, Klojen, Kota Malang" },
  ],
  gallery: ["/themes/img/a101.webp", "/themes/img/a121.webp", "/themes/img/a100.webp", "/themes/img/a115.webp", "/themes/img/a132.webp", "/themes/img/a131.webp"],
  gifts: [
    { id: "demo-bank", type: "bank", bank_name: "BRI", account_number: "0058 0100 2207 509", account_name: "Sinta Maharani (Bendahara Reuni)" },
  ],
  guestName: "Bapak Yoga Pratama",
  guestTable: "XII IPA 2",
  extras: {
    rundown: { items: [
      { time: "09.00", title: "Registrasi & ambil kaos angkatan", note: "Meja registrasi di depan ruang guru" },
      { time: "09.30", title: "Upacara mini & sambutan guru", note: "Bersama Ibu Wahyuni, wali kelas legendaris" },
      { time: "10.30", title: "Jelajah kelas & kantin lama" },
      { time: "18.30", title: "Malam reuni, makan malam & band angkatan" },
    ] },
    dressCode: { note: "Pagi: kaos angkatan. Malam: semi formal bernuansa putih & abu-abu, seperti dulu.", colors: ["#f5f2ea", "#8e9196", "#23377e", "#c8423a"] },
    guestPass: {},
    rsvpDietary: {},
    family: { title: "Panitia Reuni", names: ["Rizky Aditya (Ketua)", "Dewi Kartika (Sekretaris)", "Sinta Maharani (Bendahara)", "Bayu & Fajar (Acara)"] },
    faq: { items: [
      { q: "Boleh membawa pasangan & anak?", a: "Boleh sekali. Mohon isi jumlah tamu di form kehadiran agar konsumsi cukup." },
      { q: "Apakah ada iuran?", a: "Iuran sukarela untuk konsumsi dan donasi perpustakaan sekolah, rekening tercantum di bawah." },
      { q: "Parkir di mana?", a: "Pagi di halaman sekolah, malam di basement Graha Cakrawala." },
    ] },
  },
});

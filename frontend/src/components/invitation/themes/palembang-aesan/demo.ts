import { makeDemo } from "../demo-base";

const base = makeDemo();

export const demo = makeDemo({
  couple: {
    bride: "Ayu", groom: "Rizky",
    brideFull: "Nyimas Ayu Rahmawati, S.Farm.", groomFull: "Kemas Muhammad Rizky, S.T.",
    brideParents: "Putri kedua dari\nBapak Kemas H. Abdullah Syukri & Ibu Nyimas Hj. Rosmiati",
    groomParents: "Putra sulung dari\nBapak Masagus H. Ahmad Fauzi & Ibu Hj. Siti Aminah",
    bridePhoto: "/themes/img/a72.webp", groomPhoto: "/themes/img/a63.webp",
    note: "Dua keluarga Wong Kito yang dipersatukan di tepian Musi.",
  },
  eventLabel: "Pernikahan",
  date: "2027-05-15T08:00:00+07:00",
  place: "Balai Limas Sriwijaya",
  address: "Jl. Demang Lebar Daun No. 21, Ilir Barat I, Palembang",
  stories: [
    { date: "2019", title: "Bertemu di Tepian Musi", body: "Berkenalan saat festival perahu bidar di depan Benteng Kuto Besak, berbagi sepiring pempek di tengah sorak penonton." },
    { date: "2023", title: "Madik & Menyenggung", body: "Keluarga Rizky datang bersilaturahmi untuk mengenal keluarga Ayu, membuka jalan menuju lamaran." },
    { date: "2026", title: "Berasan & Mutus Kato", body: "Kedua keluarga bermufakat, lalu menetapkan hari baik serta seserahan dalam adat mutus kato." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-05-15T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Sultan Mahmud Badaruddin I", address: "Jl. Merdeka No. 1, 19 Ilir, Bukit Kecil, Palembang" },
    { name: "Munggah & Resepsi", date: "2027-05-15T11:00:00+07:00", time: "11.00 – 15.00 WIB", venue: "Balai Limas Sriwijaya", address: "Jl. Demang Lebar Daun No. 21, Ilir Barat I, Palembang" },
  ],
  gallery: ["/themes/img/a40.webp", "/themes/img/a61.webp", "/themes/img/a72.webp", "/themes/img/a63.webp", "/themes/img/a118.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7123456789", account_name: "Nyimas Ayu Rahmawati" },
    { id: "demo-dana", type: "ewallet", ewallet_provider: "dana", ewallet_number: "0812 7345 6789", account_name: "Kemas Muhammad Rizky" },
    { id: "demo-kado", type: "address", address: "Jl. Mayor Ruslan No. 45, 9 Ilir, Ilir Timur II, Palembang" },
  ],
  guestName: "Bapak Hendra Saputra & Keluarga",
  extras: {
    ...base.extras,
    rundown: { items: [
      { time: "08.00", title: "Akad nikah", note: "Keluarga inti & saksi" },
      { time: "10.30", title: "Arak-arakan munggah", note: "Rombongan mempelai pria tiba" },
      { time: "11.00", title: "Cacap-cacapan & suap-suapan", note: "Doa restu orang tua" },
      { time: "12.00", title: "Timbang pengantin & ramah tamah" },
    ] },
    dressCode: { note: "Songket, batik, atau busana bernuansa merah dan emas.", colors: ["#7a0f17", "#b81d2a", "#d6a548", "#f3e3bd"] },
    family: { names: ["Kel. Besar Kemas H. Abdullah Syukri", "Kel. Besar Masagus H. Ahmad Fauzi", "Keluarga Besar Kampung 9 Ilir", "Rekan sejawat RSUD Palembang Bari"] },
    travel: { note: "Untuk tamu dari luar kota, berikut beberapa pilihan terdekat.", items: [
      { name: "Hotel di kawasan Demang Lebar Daun", detail: "± 1 km dari lokasi resepsi" },
      { name: "LRT Sumsel", detail: "Turun di Stasiun Demang, lanjut 5 menit berkendara" },
    ] },
    faq: { items: [
      { q: "Apakah ada area parkir?", a: "Tersedia parkir di halaman Balai Limas Sriwijaya." },
      { q: "Sampai jam berapa resepsi?", a: "Resepsi berlangsung hingga pukul 15.00 WIB." },
    ] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-05-15T08:00:00+07:00" },
  },
});

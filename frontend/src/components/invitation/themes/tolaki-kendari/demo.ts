import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Wulan", groom: "Arya",
    brideFull: "Nur Wulandari Tamburaka, S.Farm.", groomFull: "Muh. Arya Laosa, S.Kom.",
    brideParents: "Putri ketiga dari\nBapak H. Abdul Rahman Tamburaka & Ibu Hj. Sitti Hasnah Mekuo", groomParents: "Putra kedua dari\nBapak Drs. Yusuf Laosa & Ibu Nurmala Lapadi",
    bridePhoto: "/themes/img/a99.webp", groomPhoto: "/themes/img/a96.webp",
    note: "Di tepi Teluk Kendari, saat matahari tenggelam, kami belajar bahwa hari yang selesai selalu memberi janji pagi yang baru.",
  },
  eventLabel: "Pernikahan",
  date: "2027-10-16T09:00:00+08:00",
  place: "Gedung Pertemuan Kendari Beach, Kendari",
  address: "Jl. Ir. H. Alala, Kendari Caddi, Kendari, Sulawesi Tenggara",
  stories: [
    { date: "2019", title: "Satu Kampus", body: "Kami sama-sama kuliah di Kendari. Pertemuan pertama terjadi di perpustakaan, berebut satu buku yang sama." },
    { date: "2022", title: "Senja di Kendari Beach", body: "Sore yang jingga di tepi teluk menjadi tempat kami bercerita tentang keluarga, pekerjaan, dan rencana sederhana." },
    { date: "2026", title: "Datang Melamar", body: "Keluarga Arya datang bersilaturahmi ke Konawe untuk meminang. Dengan restu kedua keluarga, hari baik pun ditentukan." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-10-16T09:00:00+08:00", time: "09.00 – 10.30 WITA", venue: "Masjid Al-Ikhlas Unaaha", address: "Jl. Inolobunggadue, Unaaha, Kabupaten Konawe" },
    { name: "Resepsi", date: "2027-10-17T19:00:00+08:00", time: "19.00 – 22.00 WITA", venue: "Gedung Pertemuan Kendari Beach", address: "Jl. Ir. H. Alala, Kendari Caddi, Kendari" },
  ],
  gallery: ["/themes/img/r38.webp", "/themes/img/r61.webp", "/themes/img/r6.webp", "/themes/img/a99.webp", "/themes/img/a96.webp"],
  gifts: [
    { id: "demo-bsi", type: "bank", bank_name: "BSI", account_number: "7311 2045 88", account_name: "Nur Wulandari Tamburaka" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "1610 0022 8173 4", account_name: "Muh. Arya Laosa" },
    { id: "demo-kado", type: "address", address: "Jl. Bunggasi No. 14, Anduonohu, Poasia, Kota Kendari 93231" },
  ],
  guestName: "Ibu Hj. Ratna Tosepu & Keluarga",
  guestTable: "Meja Teluk 5",
  extras: {
    rundown: { items: [
      { time: "19.00", title: "Kedatangan pengantin", note: "Diiringi tari Lulo penyambutan" },
      { time: "19.30", title: "Tilawah & doa" },
      { time: "20.00", title: "Ramah tamah & lulo bersama", note: "Sinonggi, kambuse, dan kue tradisional" },
    ] },
    dressCode: { note: "Busana muslim atau tenun. Nuansa merah, hitam, dan emas dipersilakan.", colors: ["#a8231f", "#17110f", "#c9963a", "#f3e6cc"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-10-16T09:00:00+08:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Abdul Rahman Tamburaka (Unaaha)", "Kel. Besar Drs. Yusuf Laosa (Kendari)"] },
  },
});

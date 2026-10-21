import { makeDemo } from "../demo-base";

export const demo = makeDemo({
  couple: {
    bride: "Laila", groom: "Rofiq",
    brideFull: "Lailatul Fitriyah, S.Pd.", groomFull: "Moh. Rofiqi Hasan, S.T.",
    brideParents: "Putri kedua dari\nBapak H. Abd. Rahman & Ibu Hj. Siti Maimunah", groomParents: "Putra sulung dari\nBapak H. Moh. Syamsul Arifin & Ibu Hj. Nur Hasanah",
    bridePhoto: "/themes/img/a72.webp", groomPhoto: "/themes/img/a63.webp",
    note: "Semoga rumah tangga kami kokoh seperti tanean lanjang: satu halaman panjang yang menyatukan keluarga besar.",
  },
  eventLabel: "Pernikahan",
  date: "2027-06-26T08:00:00+07:00",
  place: "Pendopo Agung Bangkalan",
  address: "Jl. Letnan Abdullah No. 1, Mlajah, Bangkalan, Jawa Timur",
  stories: [
    { date: "2019", title: "Pasar Tanjungbumi", body: "Rofiq menemani ibunya membeli batik tulis di Tanjungbumi; Laila sedang menjaga lapak batik milik keluarganya." },
    { date: "2023", title: "Jembatan Suramadu", body: "Bolak-balik Surabaya–Bangkalan setiap akhir pekan, kami belajar bahwa jarak hanya soal kesabaran." },
    { date: "2026", title: "Lamaran", body: "Keluarga Rofiq datang dari Sumenep membawa seserahan. Dua keluarga besar sepakat menentukan hari baik." },
  ],
  events: [
    { name: "Akad Nikah", date: "2027-06-26T08:00:00+07:00", time: "08.00 – 09.30 WIB", venue: "Masjid Agung Syaikhona Kholil", address: "Jl. Sultan Abdul Kadirun, Kemayoran, Bangkalan" },
    { name: "Resepsi", date: "2027-06-26T11:00:00+07:00", time: "11.00 – 14.00 WIB", venue: "Pendopo Agung Bangkalan", address: "Jl. Letnan Abdullah No. 1, Mlajah, Bangkalan" },
    { name: "Ngunduh Mantu", date: "2027-07-03T10:00:00+07:00", time: "10.00 – 13.00 WIB", venue: "Graha Adipoday Sumenep", address: "Jl. Trunojoyo No. 42, Bangselok, Kota Sumenep" },
  ],
  gallery: ["/themes/img/a72.webp", "/themes/img/a63.webp", "/themes/img/a27.webp", "/themes/img/a61.webp", "/themes/img/a34.webp"],
  gifts: [
    { id: "demo-bri", type: "bank", bank_name: "BRI", account_number: "0412 0100 2345 503", account_name: "Lailatul Fitriyah" },
    { id: "demo-mandiri", type: "bank", bank_name: "Mandiri", account_number: "142 00 1234567 8", account_name: "Moh. Rofiqi Hasan" },
    { id: "demo-kado", type: "address", address: "Jl. Halim Perdana Kusuma No. 27, Kraton, Bangkalan 69112" },
  ],
  guestName: "Bapak H. Fathorrahman & Keluarga",
  guestTable: "Tanean 3",
  extras: {
    rundown: { items: [
      { time: "11.00", title: "Kirab pengantin", note: "Diiringi musik saronen" },
      { time: "11.30", title: "Sambutan keluarga" },
      { time: "12.00", title: "Ramah tamah", note: "Soto & sate Madura" },
    ] },
    dressCode: { note: "Busana muslim atau batik Madura. Merah, hitam, dan putih dipersilakan.", colors: ["#c3262c", "#160d0b", "#f3e6cc", "#e9b42c"] },
    livestream: { url: "https://www.youtube.com/@rawuh", platform: "YouTube Live", startsAt: "2027-06-26T08:00:00+07:00" },
    guestPass: {},
    rsvpDietary: {},
    family: { names: ["Kel. Besar H. Abd. Rahman (Bangkalan)", "Kel. Besar H. Moh. Syamsul Arifin (Sumenep)"] },
  },
});
